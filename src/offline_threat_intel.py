"""
Offline Threat Intelligence System
Comprehensive threat detection without external API dependencies
"""

import json
import hashlib
import logging
import sqlite3
import threading
import re
import socket
import dns.resolver
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
import ipaddress

class OfflineThreatIntelligence:
    """Comprehensive offline threat intelligence system"""
    
    def __init__(self):
        self.threat_db = self._initialize_threat_database()
        self.malicious_domains = self._load_malicious_domains()
        self.malicious_ips = self._load_malicious_ips()
        self.suspicious_patterns = self._load_suspicious_patterns()
        self.threat_feeds = self._load_local_threat_feeds()
        self.domain_reputation_cache = {}
        
    def _initialize_threat_database(self):
        """Initialize local SQLite threat intelligence database"""
        conn = sqlite3.connect('offline_threat_intel.db', check_same_thread=False)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS threat_indicators (
                id INTEGER PRIMARY KEY,
                indicator TEXT UNIQUE,
                indicator_type TEXT,
                threat_type TEXT,
                confidence REAL,
                source TEXT,
                description TEXT,
                first_seen TEXT,
                last_updated TEXT
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS domain_analysis (
                id INTEGER PRIMARY KEY,
                domain TEXT UNIQUE,
                analysis_data TEXT,
                threat_score REAL,
                last_analyzed TEXT
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS ip_analysis (
                id INTEGER PRIMARY KEY,
                ip_address TEXT UNIQUE,
                analysis_data TEXT,
                threat_score REAL,
                last_analyzed TEXT
            )
        ''')
        
        # Populate with initial threat data
        self._populate_initial_threat_data(conn)
        return conn
    
    def _populate_initial_threat_data(self, conn):
        """Populate database with known threat indicators"""
        threat_indicators = [
            # Known phishing domains
            ('secure-paypal-verification.com', 'domain', 'phishing', 0.95, 'internal', 'PayPal phishing domain'),
            ('amazon-security-alert.net', 'domain', 'phishing', 0.92, 'internal', 'Amazon phishing domain'),
            ('microsoft-account-suspended.org', 'domain', 'phishing', 0.90, 'internal', 'Microsoft phishing domain'),
            ('google-security-warning.info', 'domain', 'phishing', 0.88, 'internal', 'Google phishing domain'),
            ('apple-id-locked.com', 'domain', 'phishing', 0.93, 'internal', 'Apple ID phishing domain'),
            
            # Suspicious IP ranges
            ('192.0.2.0/24', 'ip', 'malicious', 0.85, 'internal', 'Known malicious IP range'),
            ('198.51.100.0/24', 'ip', 'suspicious', 0.70, 'internal', 'Suspicious hosting provider'),
            
            # Malicious file hashes (examples)
            ('d41d8cd98f00b204e9800998ecf8427e', 'hash', 'malware', 0.99, 'internal', 'Known malware hash'),
            
            # URL patterns
            ('bit.ly/urgent-action', 'url', 'phishing', 0.80, 'internal', 'Suspicious shortened URL'),
            ('tinyurl.com/security-alert', 'url', 'phishing', 0.78, 'internal', 'Phishing shortened URL')
        ]
        
        for indicator, ind_type, threat_type, confidence, source, description in threat_indicators:
            try:
                conn.execute('''
                    INSERT OR IGNORE INTO threat_indicators 
                    (indicator, indicator_type, threat_type, confidence, source, description, first_seen, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (indicator, ind_type, threat_type, confidence, source, description, 
                     datetime.now().isoformat(), datetime.now().isoformat()))
            except sqlite3.IntegrityError:
                pass  # Indicator already exists
        
        conn.commit()
    
    def _load_malicious_domains(self) -> set:
        """Load known malicious domains"""
        return {
            # Phishing domains
            'secure-banking-update.com',
            'account-verification-required.org',
            'paypal-security-center.net',
            'amazon-account-locked.info',
            'microsoft-security-alert.com',
            'google-account-suspended.org',
            'apple-id-verification.net',
            'facebook-security-check.com',
            'twitter-account-suspended.org',
            'linkedin-security-alert.net',
            
            # Typosquatting domains
            'g00gle.com', 'gooogle.com', 'googlle.com',
            'payp4l.com', 'paypal1.com', 'paypaI.com',
            'amaz0n.com', 'amazon1.com', 'amazom.com',
            'micr0soft.com', 'microsooft.com', 'microsft.com',
            'app1e.com', 'appl3.com', 'applle.com',
            
            # Banking phishing
            'secure-bank-login.com',
            'bank-security-update.org',
            'online-banking-verification.net',
            'account-security-check.info'
        }
    
    def _load_malicious_ips(self) -> set:
        """Load known malicious IP addresses"""
        return {
            '192.0.2.1', '192.0.2.2', '192.0.2.3',  # Example malicious IPs
            '198.51.100.1', '198.51.100.2',
            '203.0.113.1', '203.0.113.2',
            '10.0.0.1'  # Private IP used maliciously
        }
    
    def _load_suspicious_patterns(self) -> Dict:
        """Load patterns that indicate suspicious activity"""
        return {
            'url_patterns': [
                r'bit\.ly/[a-z0-9]{6,}',
                r'tinyurl\.com/[a-z0-9]{6,}',
                r'goo\.gl/[a-zA-Z0-9]{6,}',
                r'[a-z0-9]+-verification\.[a-z]{2,4}',
                r'[a-z0-9]+-security\.[a-z]{2,4}',
                r'[a-z0-9]+-update\.[a-z]{2,4}',
                r'secure-[a-z0-9]+\.[a-z]{2,4}',
                r'urgent-[a-z0-9]+\.[a-z]{2,4}'
            ],
            'domain_patterns': [
                r'[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}',  # IP-like domains
                r'[a-z]{20,}\.com',  # Very long domains
                r'[a-z0-9]+-[a-z0-9]+-[a-z0-9]+\.[a-z]{2,4}',  # Multiple hyphens
                r'[0-9]{8,}\.[a-z]{2,4}'  # Numeric domains
            ],
            'suspicious_keywords': [
                'verify', 'urgent', 'suspended', 'locked', 'security',
                'confirm', 'update', 'validate', 'secure', 'alert',
                'warning', 'expired', 'limited', 'immediate', 'action'
            ]
        }
    
    def _load_local_threat_feeds(self) -> Dict:
        """Load local threat feed data"""
        return {
            'phishing_domains': self.malicious_domains,
            'malicious_ips': self.malicious_ips,
            'suspicious_tlds': {'.tk', '.ml', '.ga', '.cf', '.club', '.info', '.click', '.download'},
            'legitimate_domains': {
                'paypal.com', 'amazon.com', 'microsoft.com', 'google.com',
                'apple.com', 'facebook.com', 'twitter.com', 'linkedin.com',
                'instagram.com', 'youtube.com', 'netflix.com', 'ebay.com'
            }
        }
    
    def analyze_comprehensive_threat(self, indicator: str, indicator_type: str) -> Dict:
        """Comprehensive offline threat analysis"""
        analysis_result = {
            'indicator': indicator,
            'type': indicator_type,
            'threat_score': 0.0,
            'threat_level': 'LOW',
            'confidence': 0.0,
            'sources': [],
            'findings': [],
            'recommendations': [],
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        try:
            if indicator_type in ['url', 'domain']:
                analysis_result.update(self._analyze_domain_threat(indicator))
            elif indicator_type == 'ip':
                analysis_result.update(self._analyze_ip_threat(indicator))
            
            # Apply pattern analysis
            pattern_analysis = self._analyze_patterns(indicator, indicator_type)
            analysis_result['findings'].extend(pattern_analysis['findings'])
            analysis_result['threat_score'] = max(analysis_result['threat_score'], pattern_analysis['threat_score'])
            
            # Check against local threat database
            db_analysis = self._check_threat_database(indicator)
            if db_analysis:
                analysis_result['findings'].extend(db_analysis['findings'])
                analysis_result['threat_score'] = max(analysis_result['threat_score'], db_analysis['threat_score'])
            
            # Calculate final threat level
            analysis_result['threat_level'] = self._calculate_threat_level(analysis_result['threat_score'])
            analysis_result['confidence'] = min(analysis_result['threat_score'] + 0.2, 1.0)
            
            # Generate recommendations
            analysis_result['recommendations'] = self._generate_offline_recommendations(analysis_result)
            
            # Cache the analysis
            self._cache_analysis(indicator, analysis_result)
            
        except Exception as e:
            logging.error(f"Offline threat analysis error: {e}")
            analysis_result['error'] = str(e)
        
        return analysis_result
    
    def _analyze_domain_threat(self, indicator: str) -> Dict:
        """Analyze domain-specific threats"""
        if indicator.startswith(('http://', 'https://')):
            parsed = urlparse(indicator)
            domain = parsed.netloc.lower()
            path = parsed.path
            query = parsed.query
        else:
            domain = indicator.lower()
            path = ''
            query = ''
        
        analysis = {
            'threat_score': 0.0,
            'findings': [],
            'sources': ['offline_domain_analysis']
        }
        
        # Check against known malicious domains
        if domain in self.malicious_domains:
            analysis['threat_score'] = 0.95
            analysis['findings'].append(f"Domain '{domain}' is in known malicious domains list")
        
        # Check for typosquatting
        typosquat_result = self._detect_typosquatting(domain)
        if typosquat_result:
            analysis['threat_score'] = max(analysis['threat_score'], 0.8)
            analysis['findings'].append(f"Possible typosquatting: {typosquat_result}")
        
        # Check TLD reputation
        tld = '.' + domain.split('.')[-1] if '.' in domain else ''
        if tld in self.threat_feeds['suspicious_tlds']:
            analysis['threat_score'] = max(analysis['threat_score'], 0.4)
            analysis['findings'].append(f"Suspicious TLD: {tld}")
        
        # Analyze domain structure
        structure_analysis = self._analyze_domain_structure(domain)
        analysis['threat_score'] = max(analysis['threat_score'], structure_analysis['threat_score'])
        analysis['findings'].extend(structure_analysis['findings'])
        
        # Analyze URL path and query
        if path or query:
            url_analysis = self._analyze_url_components(path, query)
            analysis['threat_score'] = max(analysis['threat_score'], url_analysis['threat_score'])
            analysis['findings'].extend(url_analysis['findings'])
        
        # DNS analysis
        dns_analysis = self._perform_dns_analysis(domain)
        analysis['threat_score'] = max(analysis['threat_score'], dns_analysis['threat_score'])
        analysis['findings'].extend(dns_analysis['findings'])
        
        return analysis
    
    def _analyze_ip_threat(self, ip: str) -> Dict:
        """Analyze IP-specific threats"""
        analysis = {
            'threat_score': 0.0,
            'findings': [],
            'sources': ['offline_ip_analysis']
        }
        
        # Check against known malicious IPs
        if ip in self.malicious_ips:
            analysis['threat_score'] = 0.95
            analysis['findings'].append(f"IP '{ip}' is in known malicious IPs list")
        
        # Check IP type and ranges
        ip_analysis = self._analyze_ip_characteristics(ip)
        analysis['threat_score'] = max(analysis['threat_score'], ip_analysis['threat_score'])
        analysis['findings'].extend(ip_analysis['findings'])
        
        return analysis
    
    def _detect_typosquatting(self, domain: str) -> Optional[str]:
        """Detect typosquatting against legitimate domains"""
        legitimate_domains = self.threat_feeds['legitimate_domains']
        
        for legit_domain in legitimate_domains:
            similarity = self._calculate_domain_similarity(domain, legit_domain)
            if 0.7 <= similarity < 1.0:  # Similar but not identical
                return f"Similar to legitimate domain '{legit_domain}' (similarity: {similarity:.2f})"
        
        return None
    
    def _calculate_domain_similarity(self, domain1: str, domain2: str) -> float:
        """Calculate similarity between two domains"""
        # Simple similarity based on character overlap
        if len(domain1) == 0 or len(domain2) == 0:
            return 0.0
        
        # Remove TLD for comparison
        d1_base = domain1.split('.')[0]
        d2_base = domain2.split('.')[0]
        
        matches = sum(1 for a, b in zip(d1_base, d2_base) if a == b)
        max_len = max(len(d1_base), len(d2_base))
        
        return matches / max_len if max_len > 0 else 0.0
    
    def _analyze_domain_structure(self, domain: str) -> Dict:
        """Analyze domain structure for suspicious patterns"""
        analysis = {'threat_score': 0.0, 'findings': []}
        
        # Check domain length
        if len(domain) > 50:
            analysis['threat_score'] = max(analysis['threat_score'], 0.3)
            analysis['findings'].append("Unusually long domain name")
        
        # Check for excessive subdomains
        parts = domain.split('.')
        if len(parts) > 4:
            analysis['threat_score'] = max(analysis['threat_score'], 0.4)
            analysis['findings'].append("Excessive number of subdomains")
        
        # Check for suspicious patterns
        if re.search(r'[0-9]{3,}', domain):
            analysis['threat_score'] = max(analysis['threat_score'], 0.3)
            analysis['findings'].append("Contains long numeric sequences")
        
        if domain.count('-') > 3:
            analysis['threat_score'] = max(analysis['threat_score'], 0.3)
            analysis['findings'].append("Excessive use of hyphens")
        
        # Check for IP-like patterns
        if re.match(r'[0-9-]+\.[a-z]{2,4}$', domain):
            analysis['threat_score'] = max(analysis['threat_score'], 0.5)
            analysis['findings'].append("Domain resembles IP address pattern")
        
        return analysis
    
    def _analyze_url_components(self, path: str, query: str) -> Dict:
        """Analyze URL path and query parameters"""
        analysis = {'threat_score': 0.0, 'findings': []}
        
        # Check path for suspicious patterns
        if path:
            if len(path) > 100:
                analysis['threat_score'] = max(analysis['threat_score'], 0.2)
                analysis['findings'].append("Unusually long URL path")
            
            suspicious_keywords = self.suspicious_patterns['suspicious_keywords']
            path_lower = path.lower()
            found_keywords = [kw for kw in suspicious_keywords if kw in path_lower]
            
            if found_keywords:
                analysis['threat_score'] = max(analysis['threat_score'], 0.4)
                analysis['findings'].append(f"Suspicious keywords in path: {', '.join(found_keywords)}")
        
        # Check query parameters
        if query:
            if len(query) > 200:
                analysis['threat_score'] = max(analysis['threat_score'], 0.2)
                analysis['findings'].append("Unusually long query parameters")
            
            # Check for encoded suspicious content
            if '%' in query and query.count('%') > 5:
                analysis['threat_score'] = max(analysis['threat_score'], 0.3)
                analysis['findings'].append("Heavy URL encoding detected")
        
        return analysis
    
    def _perform_dns_analysis(self, domain: str) -> Dict:
        """Perform DNS analysis"""
        analysis = {'threat_score': 0.0, 'findings': []}
        
        try:
            # Try to resolve domain
            ip = socket.gethostbyname(domain)
            
            # Check if resolved IP is suspicious
            if ip in self.malicious_ips:
                analysis['threat_score'] = max(analysis['threat_score'], 0.8)
                analysis['findings'].append(f"Domain resolves to known malicious IP: {ip}")
            
            # Check for private IP ranges
            try:
                ip_obj = ipaddress.ip_address(ip)
                if ip_obj.is_private:
                    analysis['threat_score'] = max(analysis['threat_score'], 0.6)
                    analysis['findings'].append(f"Domain resolves to private IP: {ip}")
            except ValueError:
                pass
                
        except socket.gaierror:
            analysis['threat_score'] = max(analysis['threat_score'], 0.5)
            analysis['findings'].append("Domain does not resolve (NXDOMAIN)")
        except Exception as e:
            logging.debug(f"DNS analysis failed for {domain}: {e}")
        
        return analysis
    
    def _analyze_ip_characteristics(self, ip: str) -> Dict:
        """Analyze IP address characteristics"""
        analysis = {'threat_score': 0.0, 'findings': []}
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            if ip_obj.is_private:
                analysis['threat_score'] = max(analysis['threat_score'], 0.4)
                analysis['findings'].append("Private IP address used in public context")
            
            if ip_obj.is_loopback:
                analysis['threat_score'] = max(analysis['threat_score'], 0.6)
                analysis['findings'].append("Loopback IP address")
            
            if ip_obj.is_multicast:
                analysis['threat_score'] = max(analysis['threat_score'], 0.5)
                analysis['findings'].append("Multicast IP address")
                
        except ValueError:
            analysis['threat_score'] = max(analysis['threat_score'], 0.3)
            analysis['findings'].append("Invalid IP address format")
        
        return analysis
    
    def _analyze_patterns(self, indicator: str, indicator_type: str) -> Dict:
        """Analyze suspicious patterns"""
        analysis = {'threat_score': 0.0, 'findings': []}
        
        if indicator_type in ['url', 'domain']:
            # Check URL patterns
            for pattern in self.suspicious_patterns['url_patterns']:
                if re.search(pattern, indicator, re.IGNORECASE):
                    analysis['threat_score'] = max(analysis['threat_score'], 0.5)
                    analysis['findings'].append(f"Matches suspicious URL pattern: {pattern}")
            
            # Check domain patterns
            if indicator_type == 'domain':
                for pattern in self.suspicious_patterns['domain_patterns']:
                    if re.search(pattern, indicator, re.IGNORECASE):
                        analysis['threat_score'] = max(analysis['threat_score'], 0.4)
                        analysis['findings'].append(f"Matches suspicious domain pattern: {pattern}")
        
        return analysis
    
    def _check_threat_database(self, indicator: str) -> Optional[Dict]:
        """Check indicator against local threat database"""
        cursor = self.threat_db.execute(
            'SELECT threat_type, confidence, description FROM threat_indicators WHERE indicator = ?',
            (indicator,)
        )
        result = cursor.fetchone()
        
        if result:
            threat_type, confidence, description = result
            return {
                'threat_score': confidence,
                'findings': [f"Found in threat database: {description} (Type: {threat_type})"]
            }
        
        return None
    
    def _calculate_threat_level(self, threat_score: float) -> str:
        """Calculate threat level from score"""
        if threat_score >= 0.8:
            return 'CRITICAL'
        elif threat_score >= 0.6:
            return 'HIGH'
        elif threat_score >= 0.4:
            return 'MEDIUM'
        elif threat_score >= 0.2:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def _generate_offline_recommendations(self, analysis_result: Dict) -> List[str]:
        """Generate recommendations based on offline analysis"""
        recommendations = []
        threat_level = analysis_result['threat_level']
        
        if threat_level == 'CRITICAL':
            recommendations.extend([
                "CRITICAL THREAT: Block this indicator immediately",
                "Do not interact with this content under any circumstances",
                "Report to security team for investigation",
                "Check for related indicators in your environment"
            ])
        elif threat_level == 'HIGH':
            recommendations.extend([
                "HIGH RISK: Avoid interaction with this indicator",
                "Implement additional monitoring",
                "Consider blocking in security controls"
            ])
        elif threat_level == 'MEDIUM':
            recommendations.extend([
                "MEDIUM RISK: Exercise caution",
                "Verify through alternative channels",
                "Monitor for suspicious activity"
            ])
        elif threat_level == 'LOW':
            recommendations.extend([
                "LOW RISK: Some suspicious characteristics detected",
                "Proceed with normal security precautions"
            ])
        else:
            recommendations.append("MINIMAL RISK: No significant threats detected")
        
        return recommendations
    
    def _cache_analysis(self, indicator: str, analysis_result: Dict):
        """Cache analysis results for future use"""
        try:
            if analysis_result['type'] == 'domain':
                self.threat_db.execute('''
                    INSERT OR REPLACE INTO domain_analysis 
                    (domain, analysis_data, threat_score, last_analyzed)
                    VALUES (?, ?, ?, ?)
                ''', (indicator, json.dumps(analysis_result), 
                     analysis_result['threat_score'], datetime.now().isoformat()))
            elif analysis_result['type'] == 'ip':
                self.threat_db.execute('''
                    INSERT OR REPLACE INTO ip_analysis 
                    (ip_address, analysis_data, threat_score, last_analyzed)
                    VALUES (?, ?, ?, ?)
                ''', (indicator, json.dumps(analysis_result),
                     analysis_result['threat_score'], datetime.now().isoformat()))
            
            self.threat_db.commit()
        except Exception as e:
            logging.error(f"Error caching analysis: {e}")

# Global offline threat intelligence instance
offline_threat_intel = OfflineThreatIntelligence()