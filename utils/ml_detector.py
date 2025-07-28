"""
Machine Learning Phishing Detection System
==========================================

Advanced ML-based phishing detection using scikit-learn and NLTK.
This module provides comprehensive analysis for URLs, emails, and text messages.

Features:
- Text vectorization using TF-IDF
- Machine learning classification 
- Natural language processing
- URL pattern analysis
- Content-based threat scoring

Author: AI Phishing Detection Platform
"""

import re
import logging
import pickle
import os
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Optional

# Import ML and NLP libraries
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    
    ML_AVAILABLE = True
except ImportError as e:
    logging.warning(f"ML libraries not fully available: {e}")
    ML_AVAILABLE = False

logger = logging.getLogger(__name__)

class MLPhishingDetector:
    """
    Advanced ML-based phishing detection system
    
    This class uses machine learning models to detect phishing in:
    - Website URLs
    - Email content  
    - Text messages and social media content
    """
    
    def __init__(self):
        """Initialize the ML detector with models and preprocessing tools"""
        
        # Initialize NLTK components
        self._initialize_nltk()
        
        # ML Models and components
        self.url_model = None
        self.email_model = None
        self.text_model = None
        self.vectorizer = None
        self.stemmer = PorterStemmer() if ML_AVAILABLE else None
        self.stop_words = set()
        
        # Load or create models
        self._load_or_create_models()
        
        # Phishing indicators and patterns
        self.phishing_keywords = [
            # Urgency words
            'urgent', 'immediate', 'expires', 'suspended', 'verify', 'confirm',
            'update', 'action', 'required', 'asap', 'deadline', 'warning',
            
            # Financial/Security words  
            'account', 'security', 'bank', 'credit', 'payment', 'transaction',
            'paypal', 'amazon', 'apple', 'microsoft', 'google', 'netflix',
            
            # Scam words
            'winner', 'prize', 'congratulations', 'free', 'bonus', 'claim',
            'lottery', 'million', 'inheritance', 'bitcoin', 'crypto', 'investment',
            
            # Action words
            'click', 'download', 'install', 'activate', 'login', 'signin',
            'submit', 'enter', 'provide', 'details', 'information'
        ]
        
        # Suspicious URL patterns
        self.suspicious_url_patterns = [
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP addresses
            r'[a-z0-9]+-[a-z0-9]+\.[a-z]{2,3}\.[a-z]{2,3}',     # Suspicious subdomains
            r'[a-z]{10,}\.(tk|ml|ga|cf|xyz)',                    # Suspicious TLDs
            r'(bit\.ly|tinyurl|short|t\.co|goo\.gl)',            # URL shorteners
            r'[0-9]{5,}',                                        # Long number sequences
            r'[a-z]{1}[0-9]{1}[a-z]{1}[0-9]{1}',               # Alternating letters/numbers
        ]
        
        # Legitimate domains (whitelist)
        self.legitimate_domains = [
            'google.com', 'microsoft.com', 'apple.com', 'amazon.com', 'netflix.com',
            'paypal.com', 'ebay.com', 'facebook.com', 'twitter.com', 'instagram.com',
            'github.com', 'stackoverflow.com', 'wikipedia.org', 'youtube.com',
            'linkedin.com', 'reddit.com', 'dropbox.com', 'adobe.com'
        ]

    def _initialize_nltk(self):
        """Download required NLTK data if needed"""
        if not ML_AVAILABLE:
            return
            
        try:
            # Download required NLTK data
            nltk_downloads = ['punkt', 'stopwords', 'wordnet']
            for item in nltk_downloads:
                try:
                    nltk.data.find(f'tokenizers/{item}')
                except LookupError:
                    logger.info(f"Downloading NLTK data: {item}")
                    nltk.download(item, quiet=True)
            
            # Initialize stop words
            self.stop_words = set(stopwords.words('english'))
            
        except Exception as e:
            logger.warning(f"NLTK initialization error: {e}")
            self.stop_words = set()

    def _load_or_create_models(self):
        """Load existing ML models or create new ones with training data"""
        try:
            model_dir = 'models'
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            
            # Try to load existing models
            model_files = {
                'url_model': os.path.join(model_dir, 'url_model.pkl'),
                'email_model': os.path.join(model_dir, 'email_model.pkl'), 
                'text_model': os.path.join(model_dir, 'text_model.pkl'),
                'vectorizer': os.path.join(model_dir, 'vectorizer.pkl')
            }
            
            models_loaded = 0
            for model_name, file_path in model_files.items():
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as f:
                            setattr(self, model_name, pickle.load(f))
                        models_loaded += 1
                        logger.info(f"Loaded {model_name} from {file_path}")
                    except Exception as e:
                        logger.warning(f"Failed to load {model_name}: {e}")
            
            # If no models loaded, create new ones
            if models_loaded == 0:
                logger.info("No existing models found, creating new ML models")
                self._create_default_models()
                
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            self._create_default_models()

    def _create_default_models(self):
        """Create default ML models with sample training data"""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available, using pattern-based detection")
            return
            
        try:
            # Sample training data for different content types
            phishing_samples = [
                "Your account has been suspended. Click here to verify immediately.",
                "Congratulations! You've won $1000000. Claim your prize now.",
                "Urgent: Your payment failed. Update your credit card details.",
                "Security alert: Suspicious activity detected. Login to confirm.",
                "Your PayPal account will be limited. Verify your information.",
                "Bitcoin investment opportunity. Double your money in 24 hours.",
                "Your Netflix subscription expired. Click to renew immediately.",
                "IRS refund pending. Provide your bank details to claim $2500."
            ]
            
            legitimate_samples = [
                "Thank you for your purchase. Your order will arrive in 2-3 days.",
                "Welcome to our newsletter. Here are this week's updates.",
                "Your appointment is confirmed for tomorrow at 2 PM.",
                "Here's your monthly account statement and transaction history.",
                "New features have been added to your dashboard. Check them out.",
                "Your password was successfully changed. Contact us if this wasn't you.",
                "Meeting reminder: Team standup at 10 AM in conference room A.",
                "Thank you for downloading our app. Here's how to get started."
            ]
            
            # Combine training data
            training_texts = phishing_samples + legitimate_samples
            training_labels = [1] * len(phishing_samples) + [0] * len(legitimate_samples)
            
            # Create and train models
            self.vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                lowercase=True
            )
            
            # Fit vectorizer on training data
            X_train = self.vectorizer.fit_transform(training_texts)
            
            # Create different model types
            self.url_model = LogisticRegression(random_state=42)
            self.email_model = MultinomialNB(alpha=1.0)
            self.text_model = LogisticRegression(random_state=42)
            
            # Train all models on the same data (in production, you'd have separate datasets)
            self.url_model.fit(X_train, training_labels)
            self.email_model.fit(X_train, training_labels)
            self.text_model.fit(X_train, training_labels)
            
            # Save models
            self._save_models()
            
            logger.info("Created and trained new ML models successfully")
            
        except Exception as e:
            logger.error(f"Model creation error: {e}")
            # Set models to None so pattern-based detection is used
            self.url_model = None
            self.email_model = None 
            self.text_model = None
            self.vectorizer = None

    def _save_models(self):
        """Save trained models to disk"""
        try:
            model_dir = 'models'
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            
            models_to_save = {
                'url_model': self.url_model,
                'email_model': self.email_model,
                'text_model': self.text_model,
                'vectorizer': self.vectorizer
            }
            
            for model_name, model_obj in models_to_save.items():
                if model_obj is not None:
                    file_path = os.path.join(model_dir, f'{model_name}.pkl')
                    with open(file_path, 'wb') as f:
                        pickle.dump(model_obj, f)
                    logger.info(f"Saved {model_name} to {file_path}")
                    
        except Exception as e:
            logger.error(f"Model saving error: {e}")

    def analyze_content(self, content: str, content_type: str) -> Dict:
        """
        Main analysis function for all content types
        
        Args:
            content (str): Content to analyze (URL, email text, or message)
            content_type (str): Type of content ('url', 'email', 'message')
            
        Returns:
            dict: Comprehensive analysis results
        """
        try:
            # Input validation
            if not content or not isinstance(content, str):
                return self._create_error_result("Invalid input: Content cannot be empty")
            
            content = content.strip()
            if not content:
                return self._create_error_result("Invalid input: Content cannot be empty")
            
            if content_type not in ['url', 'email', 'message']:
                return self._create_error_result(f"Invalid content type: {content_type}")
            
            logger.info(f"Analyzing {content_type}: {content[:100]}...")
            
            # Route to appropriate analysis method
            if content_type == 'url':
                return self._analyze_url(content)
            elif content_type == 'email':
                return self._analyze_email(content)
            elif content_type == 'message':
                return self._analyze_message(content)
            else:
                return self._create_error_result(f"Unsupported content type: {content_type}")
                
        except Exception as e:
            logger.error(f"Analysis error for {content_type}: {str(e)}")
            return self._create_error_result(f"Analysis failed: {str(e)}")

    def _analyze_url(self, url: str) -> Dict:
        """Analyze URL for phishing indicators using ML and pattern matching"""
        try:
            # Parse URL
            parsed = urlparse(url.lower())
            domain = parsed.netloc
            path = parsed.path
            query = parsed.query
            
            risk_score = 0.0
            warnings = []
            analysis_components = []
            
            # 1. Domain Analysis
            domain_score, domain_warnings = self._analyze_domain(domain)
            risk_score += domain_score
            warnings.extend(domain_warnings)
            analysis_components.append(f"Domain analysis: {domain_score:.2f}")
            
            # 2. URL Structure Analysis
            structure_score, structure_warnings = self._analyze_url_structure(url, path, query)
            risk_score += structure_score
            warnings.extend(structure_warnings)
            analysis_components.append(f"Structure analysis: {structure_score:.2f}")
            
            # 3. ML Prediction (if available)
            if self.url_model and self.vectorizer:
                try:
                    # Prepare text for ML analysis (combine URL components)
                    url_text = f"{domain} {path} {query}".replace('/', ' ').replace('?', ' ').replace('&', ' ')
                    
                    # Vectorize and predict
                    X = self.vectorizer.transform([url_text])
                    ml_prediction = self.url_model.predict_proba(X)[0]
                    ml_score = ml_prediction[1]  # Probability of phishing
                    
                    risk_score += ml_score * 0.4  # Weight ML prediction
                    analysis_components.append(f"ML prediction: {ml_score:.2f}")
                    
                    if ml_score > 0.7:
                        warnings.append("Machine learning model detected high phishing probability")
                    elif ml_score > 0.5:  # Raised threshold to 0.5 to be more accurate
                        warnings.append("Machine learning model detected moderate phishing indicators")
                    # Don't add warnings for scores <= 0.5 as they indicate legitimacy
                        
                except Exception as e:
                    logger.warning(f"ML prediction failed for URL: {e}")
                    analysis_components.append("ML prediction: unavailable")
            
            # 4. Calculate final threat level
            threat_level = self._calculate_threat_level(risk_score)
            confidence_score = min(risk_score, 1.0)
            
            # 5. Generate explanation
            explanation = self._generate_explanation(threat_level, warnings, analysis_components, 'URL')
            
            logger.info(f"URL analysis complete - Threat: {threat_level}, Score: {risk_score:.2f}")
            
            return {
                'content': url,
                'content_type': 'url',
                'threat_level': threat_level,
                'confidence_score': confidence_score,
                'risk_score': risk_score,
                'warnings': warnings,
                'explanation': explanation,
                'analysis_components': analysis_components,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"URL analysis error: {e}")
            return self._create_error_result(f"URL analysis failed: {str(e)}")

    def _analyze_email(self, email_content: str) -> Dict:
        """Analyze email content for phishing indicators"""
        try:
            risk_score = 0.0
            warnings = []
            analysis_components = []
            
            # 1. Keyword Analysis
            keyword_score, keyword_warnings = self._analyze_keywords(email_content)
            risk_score += keyword_score
            warnings.extend(keyword_warnings)
            analysis_components.append(f"Keyword analysis: {keyword_score:.2f}")
            
            # 2. URL Extraction and Analysis
            urls_found = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content)
            if urls_found:
                url_score = 0
                for url in urls_found[:3]:  # Analyze first 3 URLs
                    url_result = self._analyze_url(url)
                    url_score += url_result['risk_score']
                    if url_result['threat_level'] == 'high':
                        warnings.append(f"Suspicious URL detected: {url[:50]}...")
                
                risk_score += url_score / len(urls_found) * 0.3
                analysis_components.append(f"Embedded URLs: {url_score/len(urls_found):.2f}")
            
            # 3. ML Prediction (if available)
            if self.email_model and self.vectorizer:
                try:
                    # Preprocess email text
                    processed_text = self._preprocess_text(email_content)
                    
                    # Vectorize and predict
                    X = self.vectorizer.transform([processed_text])
                    ml_prediction = self.email_model.predict_proba(X)[0]
                    ml_score = ml_prediction[1]  # Probability of phishing
                    
                    risk_score += ml_score * 0.5  # Higher weight for email ML
                    analysis_components.append(f"ML prediction: {ml_score:.2f}")
                    
                    if ml_score > 0.8:
                        warnings.append("Machine learning model detected high phishing probability")
                    elif ml_score > 0.5:
                        warnings.append("Machine learning model detected phishing indicators")
                        
                except Exception as e:
                    logger.warning(f"ML prediction failed for email: {e}")
                    analysis_components.append("ML prediction: unavailable")
            
            # 4. Content Pattern Analysis
            pattern_score, pattern_warnings = self._analyze_content_patterns(email_content)
            risk_score += pattern_score
            warnings.extend(pattern_warnings)
            analysis_components.append(f"Pattern analysis: {pattern_score:.2f}")
            
            # 5. Calculate final assessment
            threat_level = self._calculate_threat_level(risk_score)
            confidence_score = min(risk_score, 1.0)
            
            # 6. Generate explanation
            explanation = self._generate_explanation(threat_level, warnings, analysis_components, 'Email')
            
            logger.info(f"Email analysis complete - Threat: {threat_level}, Score: {risk_score:.2f}")
            
            return {
                'content': email_content[:200] + '...' if len(email_content) > 200 else email_content,
                'content_type': 'email',
                'threat_level': threat_level,
                'confidence_score': confidence_score,
                'risk_score': risk_score,
                'warnings': warnings,
                'explanation': explanation,
                'analysis_components': analysis_components,
                'urls_found': len(urls_found),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Email analysis error: {e}")
            return self._create_error_result(f"Email analysis failed: {str(e)}")

    def _analyze_message(self, message_content: str) -> Dict:
        """Analyze text message/social media content for threats"""
        try:
            risk_score = 0.0
            warnings = []
            analysis_components = []
            
            # 1. Keyword Analysis
            keyword_score, keyword_warnings = self._analyze_keywords(message_content)
            risk_score += keyword_score
            warnings.extend(keyword_warnings)
            analysis_components.append(f"Keyword analysis: {keyword_score:.2f}")
            
            # 2. URL Extraction and Analysis (same as email)
            urls_found = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message_content)
            if urls_found:
                url_score = 0
                for url in urls_found[:2]:  # Analyze first 2 URLs
                    url_result = self._analyze_url(url)
                    url_score += url_result['risk_score']
                    if url_result['threat_level'] == 'high':
                        warnings.append(f"Suspicious URL detected: {url[:40]}...")
                
                risk_score += url_score / len(urls_found) * 0.4
                analysis_components.append(f"Embedded URLs: {url_score/len(urls_found):.2f}")
            
            # 3. ML Prediction (if available)
            if self.text_model and self.vectorizer:
                try:
                    # Preprocess message text
                    processed_text = self._preprocess_text(message_content)
                    
                    # Vectorize and predict
                    X = self.vectorizer.transform([processed_text])
                    ml_prediction = self.text_model.predict_proba(X)[0]
                    ml_score = ml_prediction[1]  # Probability of phishing
                    
                    risk_score += ml_score * 0.4
                    analysis_components.append(f"ML prediction: {ml_score:.2f}")
                    
                    if ml_score > 0.7:
                        warnings.append("Machine learning model detected high threat probability")
                    elif ml_score > 0.4:
                        warnings.append("Machine learning model detected potential threats")
                        
                except Exception as e:
                    logger.warning(f"ML prediction failed for message: {e}")
                    analysis_components.append("ML prediction: unavailable")
            
            # 4. Social Engineering Analysis
            social_score, social_warnings = self._analyze_social_engineering(message_content)
            risk_score += social_score
            warnings.extend(social_warnings)
            analysis_components.append(f"Social engineering: {social_score:.2f}")
            
            # 5. Calculate final assessment
            threat_level = self._calculate_threat_level(risk_score)
            confidence_score = min(risk_score, 1.0)
            
            # 6. Generate explanation
            explanation = self._generate_explanation(threat_level, warnings, analysis_components, 'Message')
            
            logger.info(f"Message analysis complete - Threat: {threat_level}, Score: {risk_score:.2f}")
            
            return {
                'content': message_content[:200] + '...' if len(message_content) > 200 else message_content,
                'content_type': 'message',
                'threat_level': threat_level,
                'confidence_score': confidence_score,
                'risk_score': risk_score,
                'warnings': warnings,
                'explanation': explanation,
                'analysis_components': analysis_components,
                'urls_found': len(urls_found),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Message analysis error: {e}")
            return self._create_error_result(f"Message analysis failed: {str(e)}")

    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for ML analysis"""
        if not ML_AVAILABLE or not self.stemmer:
            return text.lower()
            
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove special characters but keep spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
            
            # Tokenize
            tokens = word_tokenize(text)
            
            # Remove stop words and stem
            processed_tokens = []
            for token in tokens:
                if token not in self.stop_words and len(token) > 2:
                    processed_tokens.append(self.stemmer.stem(token))
            
            return ' '.join(processed_tokens)
            
        except Exception as e:
            logger.warning(f"Text preprocessing error: {e}")
            return text.lower()

    def _analyze_domain(self, domain: str) -> Tuple[float, List[str]]:
        """Analyze domain for suspicious patterns"""
        score = 0.0
        warnings = []
        
        if not domain:
            return 0.3, ['Invalid or missing domain']
        
        # Check whitelist first - return empty warnings for legitimate domains
        for legitimate in self.legitimate_domains:
            if legitimate in domain:
                return 0.0, []  # No warnings for legitimate domains
        
        # Check suspicious patterns
        for pattern in self.suspicious_url_patterns:
            if re.search(pattern, domain):
                score += 0.3
                warnings.append(f'Suspicious domain pattern detected')
                break
        
        # Domain length analysis
        if len(domain) > 50:
            score += 0.2
            warnings.append('Unusually long domain name')
        
        # Subdomain analysis
        if domain.count('.') > 3:
            score += 0.2
            warnings.append('Multiple subdomains detected')
        
        return min(score, 1.0), warnings

    def _analyze_url_structure(self, url: str, path: str, query: str) -> Tuple[float, List[str]]:
        """Analyze URL structure for suspicious patterns"""
        score = 0.0
        warnings = []
        
        # Long URLs
        if len(url) > 100:
            score += 0.2
            warnings.append('Unusually long URL')
        
        # Suspicious path patterns
        if any(suspicious in path.lower() for suspicious in ['login', 'verify', 'secure', 'update']):
            score += 0.2
            warnings.append('Suspicious path elements')
        
        # Query parameter analysis
        if len(query) > 200:
            score += 0.2
            warnings.append('Unusually long query parameters')
        
        return min(score, 1.0), warnings

    def _analyze_keywords(self, content: str) -> Tuple[float, List[str]]:
        """Analyze content for phishing keywords"""
        score = 0.0
        warnings = []
        found_keywords = []
        
        content_lower = content.lower()
        
        for keyword in self.phishing_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
                score += 0.1
        
        if found_keywords:
            warnings.append(f'Phishing keywords detected: {", ".join(found_keywords[:5])}')
        
        return min(score, 1.0), warnings

    def _analyze_content_patterns(self, content: str) -> Tuple[float, List[str]]:
        """Analyze content for common phishing patterns"""
        score = 0.0
        warnings = []
        
        # Urgency patterns
        urgency_patterns = [
            r'(expire|suspend|close)\s+(today|soon|immediately)',
            r'(act|respond|click)\s+(now|immediately)',
            r'(limited|final)\s+(time|offer|chance)'
        ]
        
        for pattern in urgency_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 0.2
                warnings.append('Urgency manipulation detected')
                break
        
        # Money/prize patterns
        money_patterns = [
            r'\$[0-9,]+',
            r'(won|win|winner)',
            r'(prize|reward|bonus)',
            r'(million|thousand)\s+(dollar|euro|pound)'
        ]
        
        for pattern in money_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 0.2
                warnings.append('Financial incentive detected')
                break
        
        return min(score, 1.0), warnings

    def _analyze_social_engineering(self, content: str) -> Tuple[float, List[str]]:
        """Analyze for social engineering tactics"""
        score = 0.0
        warnings = []
        
        # Authority impersonation
        authority_terms = ['IRS', 'FBI', 'bank', 'government', 'police', 'court', 'legal']
        if any(term.lower() in content.lower() for term in authority_terms):
            score += 0.3
            warnings.append('Authority impersonation detected')
        
        # Fear tactics
        fear_terms = ['arrest', 'lawsuit', 'penalty', 'investigation', 'fraud', 'criminal']
        if any(term.lower() in content.lower() for term in fear_terms):
            score += 0.3
            warnings.append('Fear-based manipulation detected')
        
        return min(score, 1.0), warnings

    def _calculate_threat_level(self, risk_score: float) -> str:
        """Calculate threat level based on risk score"""
        if risk_score >= 0.7:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        else:
            return 'low'

    def _generate_explanation(self, threat_level: str, warnings: List[str], 
                             components: List[str], content_type: str) -> str:
        """Generate accurate, content-specific explanation of the analysis"""
        
        # Base message based on actual threat level
        if threat_level == 'high':
            base_msg = f"This {content_type.lower()} appears to be a phishing attempt with high confidence."
        elif threat_level == 'medium':
            base_msg = f"This {content_type.lower()} shows suspicious characteristics that warrant caution."
        else:
            base_msg = f"This {content_type.lower()} appears to be legitimate and safe."
        
        explanation = f"AI Analysis: {base_msg}"
        
        # Add specific findings based on actual warnings
        if warnings and len(warnings) > 0:
            explanation += f" Specific concerns detected: {'; '.join(warnings[:3])}."
        else:
            # For safe content, mention positive indicators
            if threat_level == 'low':
                if content_type.lower() == 'url':
                    explanation += " Positive indicators: Recognized legitimate domain; No suspicious URL patterns detected; Clean domain structure."
                elif content_type.lower() == 'email':
                    explanation += " Positive indicators: No urgency keywords found; No suspicious links detected; Normal communication patterns."
                else:
                    explanation += " Positive indicators: No threatening language detected; Clean content structure; Normal communication patterns."
        
        # Add technical analysis breakdown
        if components:
            explanation += f" Technical analysis: {', '.join(components)}."
        
        # Add contextual recommendation
        if threat_level == 'high':
            explanation += " Recommendation: Do not interact with this content. Report as phishing if possible."
        elif threat_level == 'medium':
            explanation += " Recommendation: Exercise caution and verify through official channels before taking any action."
        else:
            explanation += " Recommendation: Content appears safe for normal interaction, but always maintain general online security awareness."
        
        return explanation

    def _create_error_result(self, error_message: str) -> Dict:
        """Create standardized error result"""
        return {
            'content': '',
            'content_type': 'unknown',
            'threat_level': 'unknown',
            'confidence_score': 0.0,
            'risk_score': 0.0,
            'warnings': [error_message],
            'explanation': f'Analysis could not be completed: {error_message}',
            'analysis_components': [],
            'timestamp': datetime.utcnow().isoformat(),
            'error': True
        }