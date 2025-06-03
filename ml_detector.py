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
            'user_friendly_reasons': [],
            'ai_analysis': {},
            'risk_score': 0.0
        }
        
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            path = parsed_url.path.lower()
            query = parsed_url.query.lower()
            
            risk_factors = []
            user_explanations = []
            risk_score = 0.0
            
            # Check for IP address instead of domain
            if self.url_patterns['ip_pattern'].search(domain):
                risk_factors.append("Uses IP address instead of domain name")
                user_explanations.append({
                    'issue': 'Website uses numbers instead of a name',
                    'explanation': 'Legitimate websites use names like "google.com", not numbers like "192.168.1.1". This is a common trick scammers use.',
                    'safety_tip': 'Always look for proper website names. Avoid clicking links with only numbers.',
                    'severity': 'high'
                })
                risk_score += 0.3
            
            # Check for suspicious domains
            for suspicious_domain in self.url_patterns['suspicious_domains']:
                if suspicious_domain in domain:
                    risk_factors.append(f"Uses URL shortening service: {suspicious_domain}")
                    user_explanations.append({
                        'issue': f'Link is shortened using {suspicious_domain}',
                        'explanation': 'Shortened links hide the real destination. Scammers often use these to trick you into visiting dangerous websites.',
                        'safety_tip': 'Be very careful with shortened links. Use a URL expander tool to see where they really go first.',
                        'severity': 'medium'
                    })
                    risk_score += 0.2
            
            # Check for suspicious TLDs
            for tld in self.url_patterns['suspicious_tld']:
                if domain.endswith(tld):
                    risk_factors.append(f"Uses suspicious top-level domain: {tld}")
                    user_explanations.append({
                        'issue': f'Website ends with "{tld}" which is often used by scammers',
                        'explanation': f'Many scam websites use "{tld}" domains because they\'re cheap and easy to get. Legitimate businesses usually use .com, .org, or their country\'s domain.',
                        'safety_tip': f'Be extra careful with {tld} websites. Check if the company has an official .com website instead.',
                        'severity': 'medium'
                    })
                    risk_score += 0.15
            
            # Check for typosquatting
            for typo in self.url_patterns['typosquatting_patterns']:
                if typo in domain:
                    risk_factors.append(f"Possible typosquatting detected: {typo}")
                    user_explanations.append({
                        'issue': f'Website name looks like a misspelled version of a popular site',
                        'explanation': f'This website uses "{typo}" which looks similar to a well-known company name but with small changes. This is called "typosquatting" - a common scammer trick.',
                        'safety_tip': 'Always double-check website names carefully. Type the correct company website directly in your browser instead.',
                        'severity': 'high'
                    })
                    risk_score += 0.4
            
            # Check for suspicious keywords in URL
            full_url = f"{path} {query}".lower()
            suspicious_found = []
            for keyword in self.url_patterns['suspicious_keywords']:
                if keyword in full_url:
                    suspicious_found.append(keyword)
                    risk_score += 0.1
            
            if suspicious_found:
                risk_factors.append(f"Contains suspicious keywords: {', '.join(suspicious_found)}")
                user_explanations.append({
                    'issue': 'URL contains urgent or suspicious words',
                    'explanation': f'The link contains words like "{", ".join(suspicious_found)}" which scammers often use to create panic and make you act quickly without thinking.',
                    'safety_tip': 'Be suspicious of any link that tries to create urgency. Legitimate companies don\'t pressure you with urgent language in URLs.',
                    'severity': 'medium'
                })
            
            # Check URL length (very long URLs can be suspicious)
            if len(url) > 200:
                risk_factors.append("Unusually long URL")
                user_explanations.append({
                    'issue': 'This link is extremely long',
                    'explanation': 'Scammers sometimes create very long URLs to hide malicious parts or confuse people. Normal websites have shorter, cleaner addresses.',
                    'safety_tip': 'Be cautious of very long links. They might be trying to hide something suspicious.',
                    'severity': 'low'
                })
                risk_score += 0.1
            
            # Check for excessive subdomains
            subdomains = domain.split('.')
            if len(subdomains) > 4:
                risk_factors.append("Excessive number of subdomains")
                user_explanations.append({
                    'issue': 'Website address has too many dots and parts',
                    'explanation': 'This URL has many parts separated by dots. Scammers sometimes create complex addresses to make fake sites look official.',
                    'safety_tip': 'Simple is better. Official company websites usually have simple addresses like "company.com".',
                    'severity': 'medium'
                })
                risk_score += 0.15
            
            # Check for suspicious characters
            if re.search(r'[^\w\.\-:/\?&=]', url):
                risk_factors.append("Contains suspicious characters")
                user_explanations.append({
                    'issue': 'Link contains unusual symbols or characters',
                    'explanation': 'The URL has strange characters that normal websites don\'t use. This could be an attempt to disguise a malicious link.',
                    'safety_tip': 'Stick to links with normal letters, numbers, and common symbols. Avoid links with unusual characters.',
                    'severity': 'medium'
                })
                risk_score += 0.1
            
            result['reasons'] = risk_factors
            result['user_friendly_reasons'] = user_explanations
            result['risk_score'] = min(risk_score, 1.0)
            
        except Exception as e:
            logging.error(f"URL analysis error: {e}")
            result['reasons'] = ['URL parsing failed']
            result['user_friendly_reasons'] = [{
                'issue': 'Could not analyze this link properly',
                'explanation': 'There was a technical problem analyzing this URL. This could mean the link is malformed or contains unusual formatting.',
                'safety_tip': 'When in doubt, don\'t click. Contact the sender through a different method to verify the link.',
                'severity': 'high'
            }]
            result['risk_score'] = 0.3
        
        return result
    
    def _analyze_email(self, email_content):
        """Analyze email content for phishing indicators"""
        result = {
            'classification': 'safe',
            'confidence': 0.5,
            'reasons': [],
            'user_friendly_reasons': [],
            'ai_analysis': {},
            'risk_score': 0.0
        }
        
        content_lower = email_content.lower()
        risk_factors = []
        user_explanations = []
        risk_score = 0.0
        
        # Check for urgent phrases
        urgent_found = []
        for phrase in self.email_patterns['urgent_phrases']:
            if phrase in content_lower:
                urgent_found.append(phrase)
                risk_score += 0.2
        
        if urgent_found:
            risk_factors.append(f"Uses urgent language: {', '.join(urgent_found)}")
            user_explanations.append({
                'issue': 'Message uses urgent or threatening language',
                'explanation': f'This message contains phrases like "{urgent_found[0]}" that try to pressure you into acting quickly. Scammers use urgency to stop you from thinking carefully.',
                'safety_tip': 'Legitimate companies rarely demand immediate action. Take time to verify before responding to urgent requests.',
                'severity': 'high'
            })
        
        # Check for suspicious phrases
        suspicious_found = []
        for phrase in self.email_patterns['suspicious_phrases']:
            if phrase in content_lower:
                suspicious_found.append(phrase)
                risk_score += 0.25
        
        if suspicious_found:
            risk_factors.append(f"Contains suspicious phrases: {', '.join(suspicious_found)}")
            user_explanations.append({
                'issue': 'Message contains common scam phrases',
                'explanation': f'This message uses phrases like "{suspicious_found[0]}" which are commonly found in scam emails promising unrealistic rewards or deals.',
                'safety_tip': 'Be skeptical of "too good to be true" offers. Research any offers independently before responding.',
                'severity': 'high'
            })
        
        # Check for requests for personal information
        info_requests = []
        for phrase in self.email_patterns['request_info_patterns']:
            if phrase in content_lower:
                info_requests.append(phrase)
                risk_score += 0.3
        
        if info_requests:
            risk_factors.append(f"Requests sensitive information: {', '.join(info_requests)}")
            user_explanations.append({
                'issue': 'Asks for personal or financial information',
                'explanation': f'This message asks for sensitive details like "{info_requests[0]}". Legitimate companies never ask for passwords, PINs, or credit card details via email.',
                'safety_tip': 'Never provide personal information via email. Contact the company directly using official phone numbers or websites.',
                'severity': 'critical'
            })
        
        # Check for poor grammar/spelling (simplified)
        grammar_issues = self._check_grammar_issues(email_content)
        if grammar_issues > 3:
            risk_factors.append(f"Multiple grammar/spelling issues detected ({grammar_issues})")
            user_explanations.append({
                'issue': 'Poor grammar and spelling throughout message',
                'explanation': f'Found {grammar_issues} grammar or spelling errors. Professional companies usually have well-written communications.',
                'safety_tip': 'Be suspicious of messages with many spelling mistakes. Legitimate companies proofread their communications.',
                'severity': 'medium'
            })
        
        # Check for suspicious links in content
        urls_in_content = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content)
        suspicious_urls = []
        for url in urls_in_content:
            url_result = self._analyze_url(url)
            if url_result['risk_score'] > 0.3:
                suspicious_urls.append(url[:50] + "..." if len(url) > 50 else url)
                risk_score += 0.2
        
        if suspicious_urls:
            risk_factors.append(f"Contains suspicious URLs: {len(suspicious_urls)} found")
            user_explanations.append({
                'issue': 'Contains suspicious or dangerous links',
                'explanation': f'This message has {len(suspicious_urls)} suspicious links. These could lead to fake websites designed to steal your information.',
                'safety_tip': 'Never click suspicious links. Hover over links to see where they really go, or type official websites directly into your browser.',
                'severity': 'high'
            })
        
        # Check for generic greetings
        if any(greeting in content_lower for greeting in ['dear customer', 'dear user', 'dear sir/madam', 'dear valued customer']):
            risk_factors.append("Uses generic greeting instead of your name")
            user_explanations.append({
                'issue': 'Uses generic greeting instead of your name',
                'explanation': 'This message uses "Dear Customer" or similar generic greetings. Companies you have accounts with usually know and use your real name.',
                'safety_tip': 'Be suspicious of emails that don\'t address you by name, especially from companies where you have an account.',
                'severity': 'medium'
            })
            risk_score += 0.15
        
        # Check for fake sender information
        if any(indicator in content_lower for indicator in ['sent from my', 'this email was sent automatically', 'do not reply']):
            risk_factors.append("Contains sender authenticity concerns")
            user_explanations.append({
                'issue': 'Sender information seems fake or automated',
                'explanation': 'This message contains phrases that suggest it might be automatically generated or from a fake source.',
                'safety_tip': 'Verify the sender through official channels. Don\'t trust "do not reply" messages asking for personal information.',
                'severity': 'medium'
            })
            risk_score += 0.1
        
        result['reasons'] = risk_factors
        result['user_friendly_reasons'] = user_explanations
        result['risk_score'] = min(risk_score, 1.0)
        
        return result
    
    def _analyze_message(self, message_content):
        """Analyze general message content for phishing indicators"""
        # Use email analysis logic but add message-specific checks
        result = self._analyze_email(message_content)
        
        # Add message-specific patterns
        content_lower = message_content.lower()
        
        # Check for common SMS/text message scam patterns
        sms_scam_patterns = [
            'congratulations you\'ve won', 'click link to claim', 'text stop to unsubscribe',
            'reply with ssn', 'call this number now', 'limited time offer expires',
            'verify your account by clicking', 'your package is waiting'
        ]
        
        for pattern in sms_scam_patterns:
            if pattern in content_lower:
                result['reasons'].append(f"Contains SMS scam pattern: '{pattern}'")
                result['user_friendly_reasons'].append({
                    'issue': 'Message uses common text message scam tactics',
                    'explanation': f'This message contains "{pattern}" which is commonly used in text message scams to trick people.',
                    'safety_tip': 'Be skeptical of unexpected prize notifications or urgent requests via text. Verify independently before responding.',
                    'severity': 'high'
                })
                result['risk_score'] = min(result['risk_score'] + 0.2, 1.0)
        
        return result
    
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
