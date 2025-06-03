import re
import json
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from urllib.parse import urlparse
import logging

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

class PhishingDetector:
    def __init__(self):
        """Initialize the phishing detection system"""
        self.url_patterns = self._load_url_patterns()
        self.email_patterns = self._load_email_patterns()
        self.text_classifier = self._initialize_text_classifier()
        
    def _load_url_patterns(self):
        """Load suspicious URL patterns"""
        return {
            'suspicious_domains': [
                'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly',
                'is.gd', 'buff.ly', 'short.link'
            ],
            'suspicious_keywords': [
                'verify', 'urgent', 'suspended', 'locked', 'security',
                'confirm', 'update', 'validate', 'secure', 'alert'
            ],
            'ip_pattern': re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'suspicious_tld': ['.tk', '.ml', '.ga', '.cf', '.club', '.info'],
            'typosquatting_patterns': [
                'g00gle', 'yah00', 'micr0soft', 'payp4l', 'amaz0n',
                'facebok', 'twiter', 'linkdin', 'instgram'
            ]
        }
    
    def _load_email_patterns(self):
        """Load suspicious email patterns"""
        return {
            'urgent_phrases': [
                'act now', 'urgent action required', 'immediate attention',
                'verify now', 'suspended account', 'click here now',
                'limited time', 'expires today', 'final notice'
            ],
            'suspicious_phrases': [
                'congratulations you have won', 'claim your prize',
                'free money', 'no fees', 'risk free', 'guaranteed',
                'act now', 'limited offer', 'exclusive deal'
            ],
            'request_info_patterns': [
                'social security', 'credit card', 'bank account',
                'password', 'pin number', 'security code',
                'personal information', 'confirm identity'
            ]
        }
    
    def _initialize_text_classifier(self):
        """Initialize a simple text classifier for phishing detection"""
        # Create a simple pipeline with TF-IDF and Naive Bayes
        return Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
    
    def analyze(self, content, input_type='url'):
        """
        Main analysis function that combines rule-based and AI approaches
        """
        result = {
            'classification': 'safe',
            'confidence': 0.0,
            'reasons': [],
            'ai_analysis': {},
            'risk_score': 0.0
        }
        
        try:
            if input_type == 'url':
                result = self._analyze_url(content)
            elif input_type == 'email':
                result = self._analyze_email(content)
            elif input_type == 'message':
                result = self._analyze_message(content)
            
            # Apply AI enhancement
            result = self._enhance_with_ai(content, result, input_type)
            
            # Calculate final classification
            result = self._calculate_final_result(result)
            
        except Exception as e:
            logging.error(f"Analysis error: {e}")
            result['classification'] = 'error'
            result['reasons'] = ['Analysis failed due to technical error']
        
        return result
    
    def _analyze_url(self, url):
        """Analyze URL for phishing indicators"""
        result = {
            'classification': 'safe',
            'confidence': 0.5,
            'reasons': [],
            'ai_analysis': {},
            'risk_score': 0.0
        }
        
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            path = parsed_url.path.lower()
            query = parsed_url.query.lower()
            
            risk_factors = []
            risk_score = 0.0
            
            # Check for IP address instead of domain
            if self.url_patterns['ip_pattern'].search(domain):
                risk_factors.append("Uses IP address instead of domain name")
                risk_score += 0.3
            
            # Check for suspicious domains
            for suspicious_domain in self.url_patterns['suspicious_domains']:
                if suspicious_domain in domain:
                    risk_factors.append(f"Uses URL shortening service: {suspicious_domain}")
                    risk_score += 0.2
            
            # Check for suspicious TLDs
            for tld in self.url_patterns['suspicious_tld']:
                if domain.endswith(tld):
                    risk_factors.append(f"Uses suspicious top-level domain: {tld}")
                    risk_score += 0.15
            
            # Check for typosquatting
            for typo in self.url_patterns['typosquatting_patterns']:
                if typo in domain:
                    risk_factors.append(f"Possible typosquatting detected: {typo}")
                    risk_score += 0.4
            
            # Check for suspicious keywords in URL
            full_url = f"{path} {query}".lower()
            for keyword in self.url_patterns['suspicious_keywords']:
                if keyword in full_url:
                    risk_factors.append(f"Contains suspicious keyword: {keyword}")
                    risk_score += 0.1
            
            # Check URL length (very long URLs can be suspicious)
            if len(url) > 200:
                risk_factors.append("Unusually long URL")
                risk_score += 0.1
            
            # Check for excessive subdomains
            subdomains = domain.split('.')
            if len(subdomains) > 4:
                risk_factors.append("Excessive number of subdomains")
                risk_score += 0.15
            
            # Check for suspicious characters
            if re.search(r'[^\w\.\-:/\?&=]', url):
                risk_factors.append("Contains suspicious characters")
                risk_score += 0.1
            
            result['reasons'] = risk_factors
            result['risk_score'] = min(risk_score, 1.0)
            
        except Exception as e:
            logging.error(f"URL analysis error: {e}")
            result['reasons'] = ['URL parsing failed']
            result['risk_score'] = 0.3
        
        return result
    
    def _analyze_email(self, email_content):
        """Analyze email content for phishing indicators"""
        result = {
            'classification': 'safe',
            'confidence': 0.5,
            'reasons': [],
            'ai_analysis': {},
            'risk_score': 0.0
        }
        
        content_lower = email_content.lower()
        risk_factors = []
        risk_score = 0.0
        
        # Check for urgent phrases
        for phrase in self.email_patterns['urgent_phrases']:
            if phrase in content_lower:
                risk_factors.append(f"Uses urgent language: '{phrase}'")
                risk_score += 0.2
        
        # Check for suspicious phrases
        for phrase in self.email_patterns['suspicious_phrases']:
            if phrase in content_lower:
                risk_factors.append(f"Contains suspicious phrase: '{phrase}'")
                risk_score += 0.25
        
        # Check for requests for personal information
        for phrase in self.email_patterns['request_info_patterns']:
            if phrase in content_lower:
                risk_factors.append(f"Requests sensitive information: '{phrase}'")
                risk_score += 0.3
        
        # Check for poor grammar/spelling (simplified)
        grammar_issues = self._check_grammar_issues(email_content)
        if grammar_issues > 3:
            risk_factors.append(f"Multiple grammar/spelling issues detected ({grammar_issues})")
            risk_score += 0.15
        
        # Check for suspicious links in content
        urls_in_content = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content)
        for url in urls_in_content:
            url_result = self._analyze_url(url)
            if url_result['risk_score'] > 0.3:
                risk_factors.append(f"Contains suspicious URL: {url[:50]}...")
                risk_score += 0.2
        
        result['reasons'] = risk_factors
        result['risk_score'] = min(risk_score, 1.0)
        
        return result
    
    def _analyze_message(self, message_content):
        """Analyze general message content for phishing indicators"""
        # Use similar logic to email analysis but with different weights
        return self._analyze_email(message_content)
    
    def _check_grammar_issues(self, text):
        """Simple grammar issue detection"""
        issues = 0
        
        # Check for multiple punctuation
        if re.search(r'[!]{2,}|[?]{2,}', text):
            issues += 1
        
        # Check for ALL CAPS words
        caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
        if len(caps_words) > 2:
            issues += 1
        
        # Check for common misspellings
        common_errors = ['recieve', 'seperate', 'occured', 'definately', 'neccessary']
        for error in common_errors:
            if error in text.lower():
                issues += 1
        
        return issues
    
    def _enhance_with_ai(self, content, result, input_type):
        """Enhance detection with AI-based analysis"""
        try:
            # Simulate AI text analysis (in a real implementation, you'd use a trained model)
            ai_features = self._extract_ai_features(content)
            ai_confidence = self._calculate_ai_confidence(ai_features)
            
            result['ai_analysis'] = {
                'text_complexity': ai_features.get('complexity', 0.5),
                'sentiment_score': ai_features.get('sentiment', 0.0),
                'keyword_density': ai_features.get('keyword_density', 0.0),
                'ai_confidence': ai_confidence
            }
            
            # Adjust overall confidence based on AI analysis
            result['confidence'] = (result['confidence'] + ai_confidence) / 2
            
        except Exception as e:
            logging.error(f"AI enhancement error: {e}")
        
        return result
    
    def _extract_ai_features(self, content):
        """Extract features for AI analysis"""
        features = {}
        
        # Text complexity
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        
        features['complexity'] = len(words) / max(len(sentences), 1)
        features['word_count'] = len(words)
        features['char_count'] = len(content)
        
        # Keyword density for suspicious terms
        suspicious_count = 0
        all_suspicious = (
            self.email_patterns['urgent_phrases'] + 
            self.email_patterns['suspicious_phrases'] + 
            self.url_patterns['suspicious_keywords']
        )
        
        for phrase in all_suspicious:
            if phrase in content.lower():
                suspicious_count += 1
        
        features['keyword_density'] = suspicious_count / max(len(words), 1)
        
        # Simple sentiment (positive/negative indicator)
        positive_words = ['thank', 'please', 'welcome', 'congratulations']
        negative_words = ['urgent', 'suspended', 'alert', 'warning', 'error']
        
        pos_score = sum(1 for word in positive_words if word in content.lower())
        neg_score = sum(1 for word in negative_words if word in content.lower())
        
        features['sentiment'] = (pos_score - neg_score) / max(len(words), 1)
        
        return features
    
    def _calculate_ai_confidence(self, features):
        """Calculate AI confidence score"""
        # Simple weighted scoring based on features
        confidence = 0.5  # baseline
        
        # High keyword density suggests phishing
        if features.get('keyword_density', 0) > 0.05:
            confidence -= 0.2
        
        # Negative sentiment suggests phishing
        if features.get('sentiment', 0) < -0.01:
            confidence -= 0.15
        
        # Very short or very long content can be suspicious
        word_count = features.get('word_count', 0)
        if word_count < 10 or word_count > 1000:
            confidence -= 0.1
        
        return max(0.0, min(1.0, confidence))
    
    def _calculate_final_result(self, result):
        """Calculate final classification based on all factors"""
        risk_score = result['risk_score']
        ai_confidence = result['ai_analysis'].get('ai_confidence', 0.5)
        
        # Combine risk score and AI confidence
        final_score = (risk_score + (1 - ai_confidence)) / 2
        
        if final_score >= 0.7:
            result['classification'] = 'phishing'
            result['confidence'] = 0.9
        elif final_score >= 0.4:
            result['classification'] = 'suspicious'
            result['confidence'] = 0.7
        else:
            result['classification'] = 'safe'
            result['confidence'] = 0.8
        
        # Add AI explanation to reasons
        if final_score >= 0.4:
            result['reasons'].append(f"AI analysis indicates elevated risk (score: {final_score:.2f})")
        
        return result
