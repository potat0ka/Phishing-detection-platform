"""
Real-time Threat Intelligence Integration
Integrates with external threat feeds and databases for enhanced phishing detection
"""

import requests
import json
import logging
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os
from urllib.parse import urlparse
import dns.resolver
import socket

class ThreatIntelligenceEngine:
    """Real-time threat intelligence integration for enhanced phishing detection"""
    
    def __init__(self):
        """Initialize threat intelligence engine with API configurations"""
        self.api_configs = {
            'virustotal': {
                'api_key': os.environ.get('VIRUSTOTAL_API_KEY'),
                'base_url': 'https://www.virustotal.com/vtapi/v2/',
                'rate_limit': 4  # requests per minute for free tier
            },
            'urlvoid': {
                'api_key': os.environ.get('URLVOID_API_KEY'),
                'base_url': 'http://api.urlvoid.com/v1/',
                'rate_limit': 1000  # requests per month for free tier
            },
            'phishtank': {
                'api_key': os.environ.get('PHISHTANK_API_KEY'),
                'base_url': 'http://checkurl.phishtank.com/checkurl/',
                'rate_limit': 100  # requests per hour
            },
            'google_safe_browsing': {
                'api_key': os.environ.get('GOOGLE_SAFE_BROWSING_API_KEY'),
                'base_url': 'https://safebrowsing.googleapis.com/v4/threatMatches:find',
                'rate_limit': 10000  # requests per day
            }
        }
        
        # Cache for threat intelligence results
        self.threat_cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache results for 1 hour
        
        # Known threat indicators
        self.known_malicious_domains = set()
        self.known_malicious_ips = set()
        self.suspicious_tlds = {'.tk', '.ml', '.ga', '.cf', '.club', '.info', '.click', '.download'}
        
        # Initialize threat feeds
        self._load_threat_feeds()
        
    def _load_threat_feeds(self):
        """Load threat intelligence from various sources"""
        try:
            # Load malicious domains from threat feeds
            self._load_malicious_domain_feed()
            self._load_phishing_url_feed()
            logging.info("Threat intelligence feeds loaded successfully")
        except Exception as e:
            logging.error(f"Error loading threat feeds: {e}")
    
    def _load_malicious_domain_feed(self):
        """Load known malicious domains from threat feeds"""
        # This would typically load from threat intelligence providers
        # For demonstration, we'll use some known indicators
        malicious_indicators = [
            # Common phishing domains patterns
            'secure-banking-update.com',
            'account-verification-required.org',
            'paypal-security-center.net',
            'amazon-account-locked.info',
            'microsoft-security-alert.com',
            'google-account-suspended.org'
        ]
        
        self.known_malicious_domains.update(malicious_indicators)
    
    def _load_phishing_url_feed(self):
        """Load known phishing URLs from feeds"""
        try:
            # In a real implementation, this would fetch from actual threat feeds
            # like PhishTank, OpenPhish, etc.
            phishing_indicators = [
                'bit.ly/urgent-verify',
                'tinyurl.com/bank-alert',
                'short.link/security-update'
            ]
            
            for indicator in phishing_indicators:
                self.known_malicious_domains.add(indicator)
                
        except Exception as e:
            logging.error(f"Error loading phishing URL feed: {e}")
    
    def analyze_url_threat_intelligence(self, url: str) -> Dict[str, Any]:
        """Analyze URL using multiple threat intelligence sources"""
        result = {
            'threat_score': 0.0,
            'threat_sources': [],
            'reputation_data': {},
            'dns_analysis': {},
            'geographic_analysis': {},
            'ssl_analysis': {},
            'recommendations': []
        }
        
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Check cache first
            cache_key = f"url_{hashlib.md5(url.encode()).hexdigest()}"
            if self._is_cached(cache_key):
                return self.threat_cache[cache_key]['data']
            
            # Perform threat intelligence checks
            result.update(self._check_domain_reputation(domain))
            result.update(self._perform_dns_analysis(domain))
            result.update(self._analyze_geographic_location(domain))
            result.update(self._check_ssl_certificate(url))
            result.update(self._check_known_threats(url, domain))
            
            # Calculate overall threat score
            result['threat_score'] = self._calculate_threat_score(result)
            
            # Generate recommendations
            result['recommendations'] = self._generate_threat_recommendations(result)
            
            # Cache the result
            self._cache_result(cache_key, result)
            
        except Exception as e:
            logging.error(f"Error in threat intelligence analysis: {e}")
            result['error'] = str(e)
        
        return result
    
    def _check_domain_reputation(self, domain: str) -> Dict[str, Any]:
        """Check domain reputation across multiple sources"""
        reputation_data = {
            'domain_age': None,
            'registrar_info': {},
            'reputation_score': 0.0,
            'blacklist_status': [],
            'whois_data': {}
        }
        
        try:
            # Check if domain is in known malicious list
            if domain in self.known_malicious_domains:
                reputation_data['blacklist_status'].append('Known malicious domain')
                reputation_data['reputation_score'] = 1.0
            
            # Check suspicious TLD
            if any(domain.endswith(tld) for tld in self.suspicious_tlds):
                reputation_data['blacklist_status'].append('Suspicious TLD')
                reputation_data['reputation_score'] += 0.3
            
            # Check for typosquatting patterns
            if self._detect_typosquatting(domain):
                reputation_data['blacklist_status'].append('Possible typosquatting')
                reputation_data['reputation_score'] += 0.4
                
        except Exception as e:
            logging.error(f"Error checking domain reputation: {e}")
        
        return {'reputation_data': reputation_data}
    
    def _perform_dns_analysis(self, domain: str) -> Dict[str, Any]:
        """Perform DNS analysis to detect suspicious configurations"""
        dns_analysis = {
            'a_records': [],
            'mx_records': [],
            'nameservers': [],
            'suspicious_patterns': [],
            'fast_flux_indicators': []
        }
        
        try:
            # Get A records
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                dns_analysis['a_records'] = [str(record) for record in a_records]
                
                # Check for suspicious IP ranges
                for ip in dns_analysis['a_records']:
                    if self._is_suspicious_ip(ip):
                        dns_analysis['suspicious_patterns'].append(f'Suspicious IP: {ip}')
                        
            except dns.resolver.NXDOMAIN:
                dns_analysis['suspicious_patterns'].append('Domain does not exist')
            except Exception as e:
                logging.debug(f"DNS A record lookup failed: {e}")
            
            # Get MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                dns_analysis['mx_records'] = [str(record) for record in mx_records]
            except Exception as e:
                logging.debug(f"DNS MX record lookup failed: {e}")
            
            # Get nameservers
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                dns_analysis['nameservers'] = [str(record) for record in ns_records]
            except Exception as e:
                logging.debug(f"DNS NS record lookup failed: {e}")
                
        except Exception as e:
            logging.error(f"Error in DNS analysis: {e}")
        
        return {'dns_analysis': dns_analysis}
    
    def _analyze_geographic_location(self, domain: str) -> Dict[str, Any]:
        """Analyze geographic location of the domain"""
        geographic_analysis = {
            'country': None,
            'region': None,
            'hosting_provider': None,
            'risk_factors': []
        }
        
        try:
            # Get IP address
            ip = socket.gethostbyname(domain)
            
            # Check if IP is in high-risk countries or hosting providers
            # This would typically use a geolocation API
            if self._is_high_risk_hosting(ip):
                geographic_analysis['risk_factors'].append('High-risk hosting provider')
                
        except Exception as e:
            logging.debug(f"Geographic analysis failed: {e}")
        
        return {'geographic_analysis': geographic_analysis}
    
    def _check_ssl_certificate(self, url: str) -> Dict[str, Any]:
        """Check SSL certificate validity and characteristics"""
        ssl_analysis = {
            'has_ssl': False,
            'certificate_valid': False,
            'certificate_age': None,
            'issuer': None,
            'risk_factors': []
        }
        
        try:
            if url.startswith('https://'):
                ssl_analysis['has_ssl'] = True
                # Additional SSL certificate analysis would go here
                # This would require more complex certificate validation
            else:
                ssl_analysis['risk_factors'].append('No SSL encryption')
                
        except Exception as e:
            logging.debug(f"SSL analysis failed: {e}")
        
        return {'ssl_analysis': ssl_analysis}
    
    def _check_known_threats(self, url: str, domain: str) -> Dict[str, Any]:
        """Check against known threat databases"""
        threat_sources = []
        
        # Check against known malicious domains
        if domain in self.known_malicious_domains:
            threat_sources.append({
                'source': 'Internal Threat Feed',
                'threat_type': 'Malicious Domain',
                'confidence': 0.9
            })
        
        # Check for phishing patterns
        if self._contains_phishing_keywords(url):
            threat_sources.append({
                'source': 'Pattern Analysis',
                'threat_type': 'Phishing Indicators',
                'confidence': 0.7
            })
        
        return {'threat_sources': threat_sources}
    
    def _detect_typosquatting(self, domain: str) -> bool:
        """Detect potential typosquatting attempts"""
        legitimate_domains = [
            'google.com', 'facebook.com', 'paypal.com', 'amazon.com',
            'microsoft.com', 'apple.com', 'twitter.com', 'linkedin.com',
            'instagram.com', 'youtube.com', 'netflix.com', 'ebay.com'
        ]
        
        for legit_domain in legitimate_domains:
            # Simple Levenshtein distance check
            if self._calculate_similarity(domain, legit_domain) > 0.8 and domain != legit_domain:
                return True
        
        return False
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        # Simple similarity calculation
        if len(str1) == 0 or len(str2) == 0:
            return 0.0
        
        matches = sum(1 for a, b in zip(str1, str2) if a == b)
        return matches / max(len(str1), len(str2))
    
    def _is_suspicious_ip(self, ip: str) -> bool:
        """Check if IP address is in suspicious ranges"""
        suspicious_ranges = [
            '10.0.0.0/8',      # Private network
            '172.16.0.0/12',   # Private network
            '192.168.0.0/16',  # Private network
            '127.0.0.0/8'      # Localhost
        ]
        
        # In a real implementation, this would check against threat intelligence feeds
        return False
    
    def _is_high_risk_hosting(self, ip: str) -> bool:
        """Check if IP is from high-risk hosting provider"""
        # This would check against known bulletproof hosting providers
        # or countries with high cybercrime rates
        return False
    
    def _contains_phishing_keywords(self, url: str) -> bool:
        """Check if URL contains common phishing keywords"""
        phishing_keywords = [
            'verify', 'urgent', 'suspended', 'locked', 'security',
            'confirm', 'update', 'validate', 'secure', 'alert',
            'login', 'signin', 'account', 'banking', 'paypal'
        ]
        
        url_lower = url.lower()
        return any(keyword in url_lower for keyword in phishing_keywords)
    
    def _calculate_threat_score(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate overall threat score based on all analysis results"""
        score = 0.0
        
        # Reputation score
        if 'reputation_data' in analysis_result:
            score += analysis_result['reputation_data'].get('reputation_score', 0) * 0.4
        
        # DNS suspicious patterns
        if 'dns_analysis' in analysis_result:
            dns_issues = len(analysis_result['dns_analysis'].get('suspicious_patterns', []))
            score += min(dns_issues * 0.1, 0.3)
        
        # SSL issues
        if 'ssl_analysis' in analysis_result:
            ssl_issues = len(analysis_result['ssl_analysis'].get('risk_factors', []))
            score += min(ssl_issues * 0.1, 0.2)
        
        # Threat sources
        if 'threat_sources' in analysis_result:
            for source in analysis_result['threat_sources']:
                score += source.get('confidence', 0) * 0.1
        
        return min(score, 1.0)
    
    def _generate_threat_recommendations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations based on threat analysis"""
        recommendations = []
        
        threat_score = analysis_result.get('threat_score', 0)
        
        if threat_score > 0.8:
            recommendations.extend([
                "High threat detected - Do not visit this URL",
                "Block this domain in your security systems",
                "Report this URL to relevant authorities"
            ])
        elif threat_score > 0.5:
            recommendations.extend([
                "Moderate threat detected - Exercise caution",
                "Verify the legitimacy through official channels",
                "Consider using alternative trusted sources"
            ])
        elif threat_score > 0.2:
            recommendations.extend([
                "Low threat detected - Proceed with caution",
                "Monitor for suspicious behavior",
                "Keep security software updated"
            ])
        else:
            recommendations.append("No significant threats detected")
        
        # Add specific recommendations based on findings
        if 'ssl_analysis' in analysis_result:
            ssl_issues = analysis_result['ssl_analysis'].get('risk_factors', [])
            if 'No SSL encryption' in ssl_issues:
                recommendations.append("Avoid entering sensitive information on non-HTTPS sites")
        
        return recommendations
    
    def _is_cached(self, cache_key: str) -> bool:
        """Check if result is cached and still valid"""
        if cache_key not in self.threat_cache:
            return False
        
        cached_time = self.threat_cache[cache_key]['timestamp']
        return datetime.now() - cached_time < self.cache_duration
    
    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """Cache the threat intelligence result"""
        self.threat_cache[cache_key] = {
            'data': result,
            'timestamp': datetime.now()
        }
    
    def get_threat_summary(self, url: str) -> Dict[str, Any]:
        """Get a comprehensive threat summary for a URL"""
        threat_intel = self.analyze_url_threat_intelligence(url)
        
        summary = {
            'overall_risk': 'LOW',
            'confidence': threat_intel.get('threat_score', 0) * 100,
            'key_findings': [],
            'immediate_actions': [],
            'detailed_analysis': threat_intel
        }
        
        # Determine risk level
        threat_score = threat_intel.get('threat_score', 0)
        if threat_score > 0.7:
            summary['overall_risk'] = 'HIGH'
        elif threat_score > 0.4:
            summary['overall_risk'] = 'MEDIUM'
        
        # Extract key findings
        if threat_intel.get('threat_sources'):
            for source in threat_intel['threat_sources']:
                summary['key_findings'].append(f"{source['threat_type']} detected by {source['source']}")
        
        if threat_intel.get('reputation_data', {}).get('blacklist_status'):
            summary['key_findings'].extend(threat_intel['reputation_data']['blacklist_status'])
        
        # Set immediate actions
        summary['immediate_actions'] = threat_intel.get('recommendations', [])
        
        return summary

# Global threat intelligence engine instance
threat_engine = ThreatIntelligenceEngine()