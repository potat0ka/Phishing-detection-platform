import logging
import re
import hashlib
import hmac
import base64
import json
import time
import os
import tempfile
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from urllib.parse import urlparse, parse_qs
import secrets
import string

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    encryption_key: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = None
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    sandbox_timeout: int = 30
    enable_virus_scan: bool = False
    max_url_length: int = 2048
    max_text_length: int = 100000
    
    def __post_init__(self):
        if self.allowed_file_types is None:
            self.allowed_file_types = ['.txt', '.pdf', '.doc', '.docx', '.html', '.htm']
        if self.encryption_key is None:
            self.encryption_key = self._generate_key()
    
    def _generate_key(self) -> str:
        """Generate a random encryption key"""
        return base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')

@dataclass
class ValidationResult:
    """Result of data validation"""
    is_valid: bool
    sanitized_data: Optional[str] = None
    issues: List[str] = None
    risk_score: float = 0.0
    metadata: Optional[Dict] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []
        if self.metadata is None:
            self.metadata = {}

@dataclass
class SandboxResult:
    """Result of sandbox analysis"""
    is_safe: bool
    analysis_time: float
    findings: List[str]
    risk_score: float
    metadata: Dict[str, Any]
    error: Optional[str] = None

class DataValidator:
    """Comprehensive data validation and sanitization"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        
        # Malicious patterns
        self.malicious_patterns = {
            'sql_injection': [
                r"('|(\-\-)|(;)|(\||\|)|(\*|\*))",
                r"(union|select|insert|delete|update|drop|create|alter|exec|execute)",
                r"(script|javascript|vbscript|onload|onerror|onclick)"
            ],
            'xss': [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe[^>]*>",
                r"<object[^>]*>",
                r"<embed[^>]*>"
            ],
            'command_injection': [
                r"(;|\||&|`|\$\(|\${)",
                r"(rm|del|format|fdisk|mkfs)",
                r"(wget|curl|nc|netcat|telnet)"
            ],
            'path_traversal': [
                r"\.\./",
                r"\.\.\\",
                r"%2e%2e%2f",
                r"%2e%2e%5c"
            ],
            'suspicious_urls': [
                r"bit\.ly|tinyurl|t\.co|goo\.gl",
                r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",  # IP addresses
                r"[a-z0-9]{20,}\.com",  # Long random domains
                r"(phishing|scam|fake|malware|virus)"
            ]
        }
        
        # Compile patterns for performance
        self.compiled_patterns = {}
        for category, patterns in self.malicious_patterns.items():
            self.compiled_patterns[category] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    
    def validate_url(self, url: str) -> ValidationResult:
        """Validate and sanitize URL"""
        issues = []
        risk_score = 0.0
        metadata = {}
        
        try:
            # Basic length check
            if len(url) > self.config.max_url_length:
                issues.append(f"URL too long: {len(url)} > {self.config.max_url_length}")
                risk_score += 0.3
            
            # Parse URL
            try:
                parsed = urlparse(url)
                metadata['scheme'] = parsed.scheme
                metadata['netloc'] = parsed.netloc
                metadata['path'] = parsed.path
            except Exception as e:
                issues.append(f"Invalid URL format: {e}")
                risk_score += 0.5
                return ValidationResult(False, None, issues, risk_score, metadata)
            
            # Check for malicious patterns
            for category, patterns in self.compiled_patterns.items():
                for pattern in patterns:
                    if pattern.search(url):
                        issues.append(f"Suspicious pattern detected ({category}): {pattern.pattern}")
                        risk_score += 0.2
            
            # Check scheme
            if parsed.scheme not in ['http', 'https', 'ftp']:
                issues.append(f"Suspicious scheme: {parsed.scheme}")
                risk_score += 0.3
            
            # Check for IP addresses
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', parsed.netloc.split(':')[0]):
                issues.append("Direct IP address used instead of domain")
                risk_score += 0.2
                metadata['uses_ip'] = True
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.top', '.click']
            for tld in suspicious_tlds:
                if parsed.netloc.endswith(tld):
                    issues.append(f"Suspicious TLD: {tld}")
                    risk_score += 0.1
            
            # Sanitize URL
            sanitized_url = url.strip()
            
            # Remove dangerous parameters
            if parsed.query:
                query_params = parse_qs(parsed.query)
                safe_params = {}
                for key, values in query_params.items():
                    if not any(pattern.search(key) or any(pattern.search(v) for v in values) 
                              for patterns in self.compiled_patterns.values() 
                              for pattern in patterns):
                        safe_params[key] = values
                
                if len(safe_params) != len(query_params):
                    issues.append("Removed suspicious query parameters")
                    risk_score += 0.1
            
            is_valid = risk_score < 0.7
            
            return ValidationResult(
                is_valid=is_valid,
                sanitized_data=sanitized_url if is_valid else None,
                issues=issues,
                risk_score=min(risk_score, 1.0),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error validating URL: {e}")
            return ValidationResult(
                is_valid=False,
                issues=[f"Validation error: {e}"],
                risk_score=1.0
            )
    
    def validate_email(self, email: str) -> ValidationResult:
        """Validate and sanitize email"""
        issues = []
        risk_score = 0.0
        metadata = {}
        
        try:
            # Basic format validation
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(email):
                issues.append("Invalid email format")
                risk_score += 0.5
            
            # Check for malicious patterns
            for category, patterns in self.compiled_patterns.items():
                for pattern in patterns:
                    if pattern.search(email):
                        issues.append(f"Suspicious pattern detected ({category})")
                        risk_score += 0.3
            
            # Extract domain
            if '@' in email:
                domain = email.split('@')[1]
                metadata['domain'] = domain
                
                # Check for suspicious domains
                suspicious_domains = ['tempmail', 'guerrillamail', '10minutemail', 'mailinator']
                for sus_domain in suspicious_domains:
                    if sus_domain in domain.lower():
                        issues.append(f"Temporary/suspicious email domain: {domain}")
                        risk_score += 0.2
            
            # Sanitize email
            sanitized_email = email.strip().lower()
            
            is_valid = risk_score < 0.6
            
            return ValidationResult(
                is_valid=is_valid,
                sanitized_data=sanitized_email if is_valid else None,
                issues=issues,
                risk_score=min(risk_score, 1.0),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error validating email: {e}")
            return ValidationResult(
                is_valid=False,
                issues=[f"Validation error: {e}"],
                risk_score=1.0
            )
    
    def validate_text(self, text: str) -> ValidationResult:
        """Validate and sanitize text content"""
        issues = []
        risk_score = 0.0
        metadata = {}
        
        try:
            # Length check
            if len(text) > self.config.max_text_length:
                issues.append(f"Text too long: {len(text)} > {self.config.max_text_length}")
                risk_score += 0.2
            
            # Check for malicious patterns
            pattern_counts = defaultdict(int)
            for category, patterns in self.compiled_patterns.items():
                for pattern in patterns:
                    matches = pattern.findall(text)
                    if matches:
                        pattern_counts[category] += len(matches)
                        issues.append(f"Suspicious pattern detected ({category}): {len(matches)} matches")
                        risk_score += min(len(matches) * 0.1, 0.3)
            
            metadata['pattern_counts'] = dict(pattern_counts)
            
            # Check for excessive special characters
            special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
            special_ratio = special_chars / max(len(text), 1)
            if special_ratio > 0.3:
                issues.append(f"High special character ratio: {special_ratio:.2f}")
                risk_score += 0.1
            
            metadata['special_char_ratio'] = special_ratio
            
            # Basic sanitization
            sanitized_text = text
            
            # Remove potential script tags
            sanitized_text = re.sub(r'<script[^>]*>.*?</script>', '', sanitized_text, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove potential iframe/object/embed tags
            sanitized_text = re.sub(r'<(iframe|object|embed)[^>]*>.*?</\1>', '', sanitized_text, flags=re.IGNORECASE | re.DOTALL)
            
            if sanitized_text != text:
                issues.append("Removed potentially dangerous HTML tags")
                risk_score += 0.1
            
            is_valid = risk_score < 0.8
            
            return ValidationResult(
                is_valid=is_valid,
                sanitized_data=sanitized_text if is_valid else None,
                issues=issues,
                risk_score=min(risk_score, 1.0),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error validating text: {e}")
            return ValidationResult(
                is_valid=False,
                issues=[f"Validation error: {e}"],
                risk_score=1.0
            )
    
    def validate_file(self, file_path: str, file_content: Optional[bytes] = None) -> ValidationResult:
        """Validate file for security issues"""
        issues = []
        risk_score = 0.0
        metadata = {}
        
        try:
            # Check file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.config.allowed_file_types:
                issues.append(f"File type not allowed: {file_ext}")
                risk_score += 0.5
            
            metadata['file_extension'] = file_ext
            
            # Check file size if content provided
            if file_content:
                file_size = len(file_content)
                if file_size > self.config.max_file_size:
                    issues.append(f"File too large: {file_size} > {self.config.max_file_size}")
                    risk_score += 0.3
                
                metadata['file_size'] = file_size
                
                # Check for malicious content in text files
                if file_ext in ['.txt', '.html', '.htm', '.js', '.css']:
                    try:
                        text_content = file_content.decode('utf-8', errors='ignore')
                        text_validation = self.validate_text(text_content)
                        issues.extend(text_validation.issues)
                        risk_score += text_validation.risk_score * 0.5
                    except Exception as e:
                        issues.append(f"Error reading file content: {e}")
                        risk_score += 0.2
                
                # Basic virus scan simulation (placeholder)
                if self.config.enable_virus_scan:
                    virus_scan_result = self._simulate_virus_scan(file_content)
                    if not virus_scan_result['clean']:
                        issues.extend(virus_scan_result['threats'])
                        risk_score += 0.8
            
            # Check filename for suspicious patterns
            filename = os.path.basename(file_path)
            for category, patterns in self.compiled_patterns.items():
                for pattern in patterns:
                    if pattern.search(filename):
                        issues.append(f"Suspicious filename pattern ({category})")
                        risk_score += 0.2
            
            is_valid = risk_score < 0.7
            
            return ValidationResult(
                is_valid=is_valid,
                sanitized_data=file_path if is_valid else None,
                issues=issues,
                risk_score=min(risk_score, 1.0),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error validating file: {e}")
            return ValidationResult(
                is_valid=False,
                issues=[f"Validation error: {e}"],
                risk_score=1.0
            )
    
    def _simulate_virus_scan(self, content: bytes) -> Dict[str, Any]:
        """Simulate virus scanning (placeholder implementation)"""
        # This is a placeholder - in production, integrate with actual antivirus
        threats = []
        
        # Check for common malware signatures (simplified)
        malware_signatures = [
            b'eval(',
            b'exec(',
            b'system(',
            b'shell_exec(',
            b'<script>alert(',
            b'document.cookie'
        ]
        
        for signature in malware_signatures:
            if signature in content:
                threats.append(f"Potential threat detected: {signature.decode('utf-8', errors='ignore')}")
        
        return {
            'clean': len(threats) == 0,
            'threats': threats,
            'scan_time': time.time()
        }

class DataEncryption:
    """Data encryption and decryption utilities"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.key = config.encryption_key.encode('utf-8')
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt string data"""
        try:
            # Simple encryption using HMAC (for demonstration)
            # In production, use proper encryption like AES
            timestamp = str(int(time.time()))
            message = f"{timestamp}:{data}"
            
            signature = hmac.new(
                self.key,
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            encrypted = base64.b64encode(f"{message}:{signature}".encode('utf-8')).decode('utf-8')
            return encrypted
            
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        try:
            # Decode and verify
            decoded = base64.b64decode(encrypted_data.encode('utf-8')).decode('utf-8')
            parts = decoded.rsplit(':', 1)
            
            if len(parts) != 2:
                raise ValueError("Invalid encrypted data format")
            
            message, signature = parts
            
            # Verify signature
            expected_signature = hmac.new(
                self.key,
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                raise ValueError("Invalid signature")
            
            # Extract timestamp and data
            timestamp_str, data = message.split(':', 1)
            timestamp = int(timestamp_str)
            
            # Check if not too old (24 hours)
            if time.time() - timestamp > 86400:
                raise ValueError("Encrypted data too old")
            
            return data
            
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise
    
    def encrypt_file(self, file_path: str, output_path: str) -> bool:
        """Encrypt file"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Convert to base64 and encrypt
            b64_content = base64.b64encode(content).decode('utf-8')
            encrypted_content = self.encrypt_data(b64_content)
            
            with open(output_path, 'w') as f:
                f.write(encrypted_content)
            
            return True
            
        except Exception as e:
            logger.error(f"File encryption error: {e}")
            return False
    
    def decrypt_file(self, encrypted_file_path: str, output_path: str) -> bool:
        """Decrypt file"""
        try:
            with open(encrypted_file_path, 'r') as f:
                encrypted_content = f.read()
            
            # Decrypt and decode
            b64_content = self.decrypt_data(encrypted_content)
            content = base64.b64decode(b64_content.encode('utf-8'))
            
            with open(output_path, 'wb') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            logger.error(f"File decryption error: {e}")
            return False

class SandboxAnalyzer:
    """Simplified sandbox analysis (without Docker dependency)"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
    
    def analyze_url(self, url: str) -> SandboxResult:
        """Analyze URL in sandbox environment"""
        start_time = time.time()
        findings = []
        risk_score = 0.0
        metadata = {}
        
        try:
            # Simulate sandbox analysis
            # In production, this would use actual sandboxing technology
            
            # Basic URL analysis
            parsed = urlparse(url)
            metadata['domain'] = parsed.netloc
            metadata['scheme'] = parsed.scheme
            
            # Simulate network analysis
            if parsed.scheme not in ['http', 'https']:
                findings.append(f"Unusual protocol: {parsed.scheme}")
                risk_score += 0.3
            
            # Simulate domain reputation check
            suspicious_keywords = ['phish', 'scam', 'fake', 'malware', 'virus']
            for keyword in suspicious_keywords:
                if keyword in parsed.netloc.lower():
                    findings.append(f"Suspicious domain keyword: {keyword}")
                    risk_score += 0.4
            
            # Simulate content analysis
            if len(parsed.path) > 100:
                findings.append("Unusually long URL path")
                risk_score += 0.1
            
            # Check for URL shorteners
            shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
            if any(shortener in parsed.netloc for shortener in shorteners):
                findings.append("URL shortener detected")
                risk_score += 0.2
            
            analysis_time = time.time() - start_time
            is_safe = risk_score < 0.6
            
            return SandboxResult(
                is_safe=is_safe,
                analysis_time=analysis_time,
                findings=findings,
                risk_score=min(risk_score, 1.0),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Sandbox analysis error: {e}")
            return SandboxResult(
                is_safe=False,
                analysis_time=time.time() - start_time,
                findings=[f"Analysis error: {e}"],
                risk_score=1.0,
                metadata={},
                error=str(e)
            )
    
    def analyze_file(self, file_path: str) -> SandboxResult:
        """Analyze file in sandbox environment"""
        start_time = time.time()
        findings = []
        risk_score = 0.0
        metadata = {}
        
        try:
            # Basic file analysis
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file_path)[1].lower()
            
            metadata['file_size'] = file_size
            metadata['file_extension'] = file_ext
            
            # Check file size
            if file_size > self.config.max_file_size:
                findings.append(f"File exceeds size limit: {file_size}")
                risk_score += 0.3
            
            # Check file extension
            dangerous_extensions = ['.exe', '.bat', '.cmd', '.scr', '.pif', '.com']
            if file_ext in dangerous_extensions:
                findings.append(f"Dangerous file extension: {file_ext}")
                risk_score += 0.8
            
            # Simulate content analysis for text files
            if file_ext in ['.txt', '.html', '.htm', '.js']:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000)  # Read first 1000 chars
                    
                    # Check for suspicious content
                    suspicious_patterns = ['eval(', 'exec(', '<script>', 'document.cookie']
                    for pattern in suspicious_patterns:
                        if pattern in content.lower():
                            findings.append(f"Suspicious content pattern: {pattern}")
                            risk_score += 0.2
                            
                except Exception as e:
                    findings.append(f"Could not read file content: {e}")
                    risk_score += 0.1
            
            analysis_time = time.time() - start_time
            is_safe = risk_score < 0.7
            
            return SandboxResult(
                is_safe=is_safe,
                analysis_time=analysis_time,
                findings=findings,
                risk_score=min(risk_score, 1.0),
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"File sandbox analysis error: {e}")
            return SandboxResult(
                is_safe=False,
                analysis_time=time.time() - start_time,
                findings=[f"Analysis error: {e}"],
                risk_score=1.0,
                metadata={},
                error=str(e)
            )

class RateLimiter:
    """Simple rate limiting implementation"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.requests = defaultdict(deque)
        self.blocked_ips = defaultdict(float)  # IP -> unblock_time
    
    def is_allowed(self, client_ip: str) -> Tuple[bool, Dict[str, Any]]:
        """Check if request is allowed"""
        current_time = time.time()
        
        # Check if IP is currently blocked
        if client_ip in self.blocked_ips:
            if current_time < self.blocked_ips[client_ip]:
                return False, {
                    'reason': 'IP temporarily blocked',
                    'unblock_time': self.blocked_ips[client_ip],
                    'remaining_time': self.blocked_ips[client_ip] - current_time
                }
            else:
                # Unblock IP
                del self.blocked_ips[client_ip]
        
        # Clean old requests
        window_start = current_time - self.config.rate_limit_window
        while self.requests[client_ip] and self.requests[client_ip][0] < window_start:
            self.requests[client_ip].popleft()
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.config.rate_limit_requests:
            # Block IP for 1 hour
            self.blocked_ips[client_ip] = current_time + 3600
            return False, {
                'reason': 'Rate limit exceeded',
                'requests_in_window': len(self.requests[client_ip]),
                'window_size': self.config.rate_limit_window,
                'blocked_until': self.blocked_ips[client_ip]
            }
        
        # Allow request
        self.requests[client_ip].append(current_time)
        
        return True, {
            'requests_in_window': len(self.requests[client_ip]),
            'remaining_requests': self.config.rate_limit_requests - len(self.requests[client_ip])
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics"""
        current_time = time.time()
        
        active_clients = len([ip for ip, requests in self.requests.items() if requests])
        blocked_clients = len([ip for ip, unblock_time in self.blocked_ips.items() 
                              if unblock_time > current_time])
        
        return {
            'active_clients': active_clients,
            'blocked_clients': blocked_clients,
            'total_tracked_ips': len(self.requests),
            'rate_limit_requests': self.config.rate_limit_requests,
            'rate_limit_window': self.config.rate_limit_window
        }

class SecurityHardening:
    """Main security hardening class"""
    
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or SecurityConfig()
        self.validator = DataValidator(self.config)
        self.encryption = DataEncryption(self.config)
        self.sandbox = SandboxAnalyzer(self.config)
        self.rate_limiter = RateLimiter(self.config)
        
        # Security metrics
        self.metrics = {
            'validations_performed': 0,
            'validations_failed': 0,
            'encryptions_performed': 0,
            'sandbox_analyses': 0,
            'rate_limit_blocks': 0,
            'threats_detected': 0
        }
        
        logger.info("Security hardening initialized")
    
    def validate_input(self, data: str, data_type: str) -> ValidationResult:
        """Validate input data based on type"""
        self.metrics['validations_performed'] += 1
        
        try:
            if data_type == 'url':
                result = self.validator.validate_url(data)
            elif data_type == 'email':
                result = self.validator.validate_email(data)
            elif data_type == 'text':
                result = self.validator.validate_text(data)
            else:
                result = ValidationResult(
                    is_valid=False,
                    issues=[f"Unknown data type: {data_type}"],
                    risk_score=1.0
                )
            
            if not result.is_valid:
                self.metrics['validations_failed'] += 1
                if result.risk_score > 0.5:
                    self.metrics['threats_detected'] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Input validation error: {e}")
            self.metrics['validations_failed'] += 1
            return ValidationResult(
                is_valid=False,
                issues=[f"Validation error: {e}"],
                risk_score=1.0
            )
    
    def secure_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        self.metrics['encryptions_performed'] += 1
        return self.encryption.encrypt_data(data)
    
    def unsecure_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.encryption.decrypt_data(encrypted_data)
    
    def analyze_in_sandbox(self, target: str, target_type: str) -> SandboxResult:
        """Analyze target in sandbox"""
        self.metrics['sandbox_analyses'] += 1
        
        if target_type == 'url':
            return self.sandbox.analyze_url(target)
        elif target_type == 'file':
            return self.sandbox.analyze_file(target)
        else:
            return SandboxResult(
                is_safe=False,
                analysis_time=0.0,
                findings=[f"Unknown target type: {target_type}"],
                risk_score=1.0,
                metadata={},
                error=f"Unknown target type: {target_type}"
            )
    
    def check_rate_limit(self, client_ip: str) -> Tuple[bool, Dict[str, Any]]:
        """Check rate limiting for client"""
        allowed, info = self.rate_limiter.is_allowed(client_ip)
        
        if not allowed:
            self.metrics['rate_limit_blocks'] += 1
        
        return allowed, info
    
    def get_security_metrics(self) -> Dict[str, Any]:
        """Get security metrics"""
        rate_limiter_stats = self.rate_limiter.get_stats()
        
        return {
            'security_metrics': self.metrics.copy(),
            'rate_limiter_stats': rate_limiter_stats,
            'config': {
                'max_file_size': self.config.max_file_size,
                'allowed_file_types': self.config.allowed_file_types,
                'rate_limit_requests': self.config.rate_limit_requests,
                'rate_limit_window': self.config.rate_limit_window,
                'enable_virus_scan': self.config.enable_virus_scan
            },
            'generated_at': datetime.now().isoformat()
        }
    
    def generate_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        metrics = self.get_security_metrics()
        
        # Calculate security scores
        total_validations = metrics['security_metrics']['validations_performed']
        failed_validations = metrics['security_metrics']['validations_failed']
        
        validation_success_rate = 1.0
        if total_validations > 0:
            validation_success_rate = 1.0 - (failed_validations / total_validations)
        
        threat_detection_rate = 0.0
        if total_validations > 0:
            threat_detection_rate = metrics['security_metrics']['threats_detected'] / total_validations
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'security_summary': {
                'validation_success_rate': validation_success_rate,
                'threat_detection_rate': threat_detection_rate,
                'total_validations': total_validations,
                'threats_detected': metrics['security_metrics']['threats_detected'],
                'rate_limit_blocks': metrics['security_metrics']['rate_limit_blocks']
            },
            'detailed_metrics': metrics,
            'recommendations': self._generate_security_recommendations(metrics)
        }
        
        return report
    
    def _generate_security_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate security recommendations based on metrics"""
        recommendations = []
        
        security_metrics = metrics['security_metrics']
        
        # Check validation failure rate
        total_validations = security_metrics['validations_performed']
        failed_validations = security_metrics['validations_failed']
        
        if total_validations > 0:
            failure_rate = failed_validations / total_validations
            if failure_rate > 0.1:
                recommendations.append(
                    f"High validation failure rate ({failure_rate:.1%}). "
                    "Review input validation rules and user education."
                )
        
        # Check threat detection
        threats_detected = security_metrics['threats_detected']
        if threats_detected > 10:
            recommendations.append(
                f"High number of threats detected ({threats_detected}). "
                "Consider implementing additional security measures."
            )
        
        # Check rate limiting
        rate_limit_blocks = security_metrics['rate_limit_blocks']
        if rate_limit_blocks > 50:
            recommendations.append(
                f"High number of rate limit blocks ({rate_limit_blocks}). "
                "Review rate limiting thresholds or investigate potential attacks."
            )
        
        # General recommendations
        if not recommendations:
            recommendations.extend([
                "Security metrics look good. Continue monitoring.",
                "Consider regular security audits and penetration testing.",
                "Keep security configurations up to date."
            ])
        
        return recommendations

# Factory functions
def create_security_hardening(config: Optional[SecurityConfig] = None) -> SecurityHardening:
    """Create security hardening instance"""
    return SecurityHardening(config)

def validate_security_requirements() -> bool:
    """Validate security requirements"""
    try:
        import hashlib
        import hmac
        import base64
        import secrets
        from urllib.parse import urlparse
        return True
    except ImportError as e:
        logger.error(f"Missing required dependency: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Create security hardening instance
    security = create_security_hardening()
    
    # Test URL validation
    url_result = security.validate_input("http://suspicious-site.com/login", "url")
    print(f"URL validation: {url_result.is_valid}, Risk: {url_result.risk_score}")
    
    # Test email validation
    email_result = security.validate_input("user@example.com", "email")
    print(f"Email validation: {email_result.is_valid}, Risk: {email_result.risk_score}")
    
    # Test encryption
    encrypted = security.secure_data("sensitive information")
    decrypted = security.unsecure_data(encrypted)
    print(f"Encryption test: {decrypted == 'sensitive information'}")
    
    # Generate security report
    report = security.generate_security_report()
    print(f"Security report generated with {len(report['recommendations'])} recommendations")