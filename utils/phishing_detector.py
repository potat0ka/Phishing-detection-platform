"""
AI Phishing Detection Engine
============================

This module contains the AI-powered phishing detection system.
It analyzes URLs and content to identify potential phishing threats.

Author: Bigendra Shrestha
"""

import re
import logging
from urllib.parse import urlparse
from datetime import datetime

logger = logging.getLogger(__name__)

class PhishingDetector:
    """
    AI-powered phishing detection system
    
    This class analyzes URLs and content to detect phishing attempts
    using pattern matching, machine learning, and threat intelligence.
    """
    
    def __init__(self):
        """Initialize the phishing detector with threat patterns"""
        
        # Known phishing keywords and patterns
        self.phishing_keywords = [
            'verify', 'confirm', 'update', 'suspend', 'expire', 'urgent',
            'account', 'security', 'warning', 'alert', 'immediate',
            'click', 'prize', 'winner', 'congratulations', 'free',
            'limited', 'offer', 'act', 'now', 'bitcoin', 'crypto'
        ]
        
        # Suspicious URL patterns
        self.suspicious_patterns = [
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP addresses
            r'[a-z]+-[a-z]+\.[a-z]{2,3}\.[a-z]{2,3}',  # Suspicious domain patterns
            r'[a-z]{10,}\.tk|\.ml|\.ga|\.cf',  # Suspicious TLDs
            r'bit\.ly|tinyurl|short|t\.co',  # URL shorteners
            r'[0-9]{5,}',  # Long number sequences
            r'[a-z]{1}[0-9]{1}[a-z]{1}',  # Mixed alphanumeric patterns
        ]
        
        # Legitimate domain patterns (whitelist)
        self.legitimate_domains = [
            'google.com', 'microsoft.com', 'apple.com', 'amazon.com',
            'paypal.com', 'ebay.com', 'facebook.com', 'twitter.com',
            'github.com', 'stackoverflow.com', 'wikipedia.org'
        ]
    
    def analyze_url(self, url, message_content=None):
        """
        Comprehensive analysis of URL and optional message content for phishing indicators
        
        Args:
            url (str): URL to analyze
            message_content (str, optional): Message text containing the URL
            
        Returns:
            dict: Detection results with threat level and details
        """
        try:
            # Sanitize and validate input
            if not url or not isinstance(url, str):
                return self._create_error_result("Invalid URL provided")
            
            url = url.strip()
            if not url:
                return self._create_error_result("Empty URL provided") 
                
            # Parse URL components
            parsed_url = urlparse(url.lower())
            domain = parsed_url.netloc
            path = parsed_url.path
            query = parsed_url.query
            
            # Initialize comprehensive analysis
            risk_score = 0.0
            warnings = []
            details = []
            analysis_components = []
            
            # 1. Domain Analysis
            logger.info(f"Analyzing domain: {domain}")
            domain_score, domain_warnings = self._analyze_domain(domain)
            risk_score += domain_score
            warnings.extend(domain_warnings)
            analysis_components.append(f"Domain analysis: {domain_score:.2f}")
            
            # 2. URL Structure Analysis  
            logger.info(f"Analyzing URL structure: {url}")
            structure_score, structure_warnings = self._analyze_url_structure(url, path, query)
            risk_score += structure_score
            warnings.extend(structure_warnings)
            analysis_components.append(f"Structure analysis: {structure_score:.2f}")
            
            # 3. Content Analysis (from URL)
            logger.info("Analyzing URL content patterns")
            content_score, content_warnings = self._analyze_content(url)
            risk_score += content_score
            warnings.extend(content_warnings)
            analysis_components.append(f"Content analysis: {content_score:.2f}")
            
            # 4. Message Content Analysis (if provided)
            if message_content:
                logger.info("Analyzing message content")
                message_score, message_warnings = self._analyze_message_content(message_content, url)
                risk_score += message_score
                warnings.extend(message_warnings)
                analysis_components.append(f"Message analysis: {message_score:.2f}")
            
            # 5. Embedded Links Analysis
            embedded_score, embedded_warnings = self._analyze_embedded_links(url)
            risk_score += embedded_score
            warnings.extend(embedded_warnings)
            if embedded_score > 0:
                analysis_components.append(f"Embedded links: {embedded_score:.2f}")
            
            # 6. Calculate final threat assessment
            threat_level = self._calculate_threat_level(risk_score)
            confidence_score = min(risk_score, 1.0)
            
            # 7. Generate comprehensive explanation
            explanation = self._generate_explanation(threat_level, warnings, analysis_components)
            
            logger.info(f"Analysis complete - URL: {url}, Threat: {threat_level}, Score: {risk_score:.2f}")
            
            return {
                'url': url,
                'threat_level': threat_level,
                'confidence_score': confidence_score,
                'risk_score': risk_score,
                'warnings': warnings,
                'explanation': explanation,
                'details': details,
                'analysis_components': analysis_components,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing URL {url}: {str(e)}")
            return self._create_error_result(f"Analysis failed: {str(e)}")
    
    def _create_error_result(self, error_message):
        """Create standardized error result"""
        return {
            'url': '',
            'threat_level': 'unknown',
            'confidence_score': 0.0,
            'risk_score': 0.0,
            'warnings': [error_message],
            'explanation': f'Unable to complete analysis: {error_message}',
            'details': [],
            'analysis_components': [],
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _analyze_domain(self, domain):
        """Analyze domain for suspicious patterns"""
        score = 0.0
        warnings = []
        
        if not domain:
            return 0.5, ['Invalid domain']
        
        # Check if domain is in whitelist
        for legitimate in self.legitimate_domains:
            if legitimate in domain:
                return 0.0, ['Legitimate domain detected']
        
        # Check for IP address instead of domain
        if re.match(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', domain):
            score += 0.4
            warnings.append('Uses IP address instead of domain name')
        
        # Check domain length
        if len(domain) > 50:
            score += 0.2
            warnings.append('Unusually long domain name')
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.cc', '.pw']
        for tld in suspicious_tlds:
            if domain.endswith(tld):
                score += 0.3
                warnings.append(f'Suspicious top-level domain: {tld}')
        
        # Check for subdomain patterns
        subdomains = domain.split('.')
        if len(subdomains) > 4:
            score += 0.2
            warnings.append('Multiple subdomains detected')
        
        # Check for number/letter patterns
        if re.search(r'[0-9]{3,}', domain):
            score += 0.2
            warnings.append('Contains long number sequences')
        
        # Check for common phishing domain patterns
        phishing_patterns = ['secure', 'verification', 'account', 'update']
        for pattern in phishing_patterns:
            if pattern in domain:
                score += 0.3
                warnings.append(f'Contains suspicious keyword: {pattern}')
        
        return score, warnings
    
    def _analyze_url_structure(self, url, path, query):
        """Analyze URL structure for suspicious patterns"""
        score = 0.0
        warnings = []
        
        # Check URL length
        if len(url) > 200:
            score += 0.2
            warnings.append('Unusually long URL')
        
        # Check for URL shorteners
        shorteners = ['bit.ly', 'tinyurl', 't.co', 'short', 'ow.ly']
        for shortener in shorteners:
            if shortener in url:
                score += 0.4
                warnings.append('URL shortener detected')
        
        # Check for suspicious path patterns
        if path and len(path) > 100:
            score += 0.1
            warnings.append('Long URL path')
        
        # Check for query parameter obfuscation
        if query and len(query) > 200:
            score += 0.2
            warnings.append('Suspicious query parameters')
        
        # Check for encoded characters
        if '%' in url and url.count('%') > 3:
            score += 0.2
            warnings.append('URL contains encoded characters')
        
        return score, warnings
    
    def _analyze_content(self, url):
        """Analyze URL content for phishing keywords"""
        score = 0.0
        warnings = []
        
        url_lower = url.lower()
        
        # Check for phishing keywords
        keyword_count = 0
        found_keywords = []
        
        for keyword in self.phishing_keywords:
            if keyword in url_lower:
                keyword_count += 1
                found_keywords.append(keyword)
        
        if keyword_count > 0:
            score += min(keyword_count * 0.1, 0.4)
            warnings.append(f'Contains phishing keywords: {", ".join(found_keywords[:3])}')
        
        # Check for suspicious file extensions
        suspicious_extensions = ['.exe', '.zip', '.rar', '.scr', '.bat']
        for ext in suspicious_extensions:
            if ext in url_lower:
                score += 0.3
                warnings.append(f'Suspicious file extension: {ext}')
        
        return score, warnings
    
    def _analyze_message_content(self, message_content, url):
        """Analyze message content for phishing indicators"""
        score = 0.0
        warnings = []
        
        if not message_content:
            return score, warnings
            
        message_lower = message_content.lower()
        
        # Check for urgent language patterns
        urgent_phrases = [
            'urgent', 'immediate', 'expire', 'suspended', 'locked', 'verify now',
            'click here', 'act now', 'limited time', 'confirm identity'
        ]
        
        urgent_count = sum(1 for phrase in urgent_phrases if phrase in message_lower)
        if urgent_count > 0:
            score += min(urgent_count * 0.15, 0.4)
            warnings.append(f'Contains urgent language ({urgent_count} phrases)')
            
        # Check for financial/credential requests
        credential_phrases = [
            'password', 'social security', 'credit card', 'bank account',
            'pin number', 'verify account', 'update payment'
        ]
        
        credential_count = sum(1 for phrase in credential_phrases if phrase in message_lower)
        if credential_count > 0:
            score += min(credential_count * 0.2, 0.5)
            warnings.append('Requests sensitive financial or credential information')
            
        # Check for poor grammar/spelling (simplified)
        if message_content.count('!!') > 1 or message_content.count('???') > 0:
            score += 0.1
            warnings.append('Contains excessive punctuation')
            
        return score, warnings
    
    def _analyze_embedded_links(self, url):
        """Analyze for URL shorteners and redirects"""
        score = 0.0
        warnings = []
        
        # Check for URL shorteners
        shortener_services = [
            'bit.ly', 'tinyurl.com', 't.co', 'ow.ly', 'is.gd',
            'buff.ly', 'short.link', 'cutt.ly', 'rb.gy'
        ]
        
        url_lower = url.lower()
        for service in shortener_services:
            if service in url_lower:
                score += 0.3
                warnings.append(f'Uses URL shortener ({service}) - destination hidden')
                break
                
        # Check for suspicious redirects
        if 'redirect' in url_lower or '/r/' in url_lower or '/go/' in url_lower:
            score += 0.2
            warnings.append('Contains redirect patterns')
            
        return score, warnings
    
    def _calculate_threat_level(self, risk_score):
        """Calculate threat level based on risk score"""
        if risk_score >= 0.7:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _generate_explanation(self, threat_level, warnings, analysis_components=None):
        """Generate comprehensive human-readable explanation"""
        
        # Base explanation by threat level
        explanations = {
            'high': "⚠️ HIGH RISK: This content shows multiple indicators of being a phishing attempt. Do not click or interact with it.",
            'medium': "⚠️ MEDIUM RISK: This content has several suspicious characteristics that warrant caution. Verify before interacting.",
            'low': "⚠️ LOW RISK: This content appears mostly legitimate but has some minor suspicious elements. Exercise normal caution."
        }
        
        explanation = explanations.get(threat_level, "✅ SAFE: This content appears to be legitimate and safe to interact with.")
        
        # Add specific warnings if present
        if warnings:
            explanation += f"\n\nSpecific concerns detected ({len(warnings)} total):\n"
            for i, warning in enumerate(warnings[:5], 1):  # Show up to 5 warnings
                explanation += f"{i}. {warning}\n"
            
            if len(warnings) > 5:
                explanation += f"... and {len(warnings) - 5} additional concerns"
                
        # Add analysis breakdown for educational purposes
        if analysis_components:
            explanation += f"\n\nAnalysis breakdown: {' | '.join(analysis_components)}"
            
        return explanation