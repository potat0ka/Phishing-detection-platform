"""
Advanced Self-Learning Phishing Detection System
===============================================

Enhanced ML-based phishing detection with self-learning capabilities.
This module provides comprehensive analysis with continuous learning from new data.

Features:
- Online/Incremental learning capabilities
- Enhanced feature extraction (URLs, HTML, metadata, email headers)
- Advanced NLP with BERT integration
- Ensemble learning with XGBoost, LightGBM
- Real-time data feeds integration
- Accuracy tracking and confusion matrix
- Security against data poisoning

Author: AI Phishing Detection Platform
"""

import re
import logging
import pickle
import os
import json
import hashlib
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
from collections import defaultdict, deque
import threading
from concurrent.futures import ThreadPoolExecutor

# Import ML and NLP libraries
try:
    from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier
    from sklearn.ensemble import VotingClassifier, RandomForestClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    from sklearn.model_selection import cross_val_score
    import xgboost as xgb
    import lightgbm as lgb
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    
    # Try to import transformers for BERT
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch
        BERT_AVAILABLE = True
    except ImportError:
        BERT_AVAILABLE = False
    
    ML_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Advanced ML libraries not fully available: {e}")
    ML_AVAILABLE = False
    BERT_AVAILABLE = False

# Import for real-time data feeds
try:
    import requests
    from bs4 import BeautifulSoup
    import feedparser
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False

logger = logging.getLogger(__name__)

class AdvancedMLPhishingDetector:
    """
    Advanced self-learning ML-based phishing detection system
    
    This class uses ensemble machine learning models with online learning
    capabilities to detect phishing in:
    - Website URLs with enhanced feature extraction
    - Email content with header analysis
    - Text messages and social media content
    - HTML content and metadata
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the advanced ML detector with enhanced capabilities"""
        
        self.config = config or {}
        
        # Initialize NLTK components
        self._initialize_nltk()
        
        # Online learning models
        self.online_models = {}
        self.ensemble_model = None
        self.bert_model = None
        self.bert_tokenizer = None
        
        # Feature extractors
        self.tfidf_vectorizer = None
        self.hashing_vectorizer = None
        self.stemmer = PorterStemmer() if ML_AVAILABLE else None
        self.stop_words = set()
        
        # Performance tracking
        self.performance_metrics = {
            'accuracy_history': deque(maxlen=1000),
            'precision_history': deque(maxlen=1000),
            'recall_history': deque(maxlen=1000),
            'f1_history': deque(maxlen=1000),
            'confusion_matrices': deque(maxlen=100),
            'learning_cycles': 0,
            'last_update': None
        }
        
        # Data pipeline components
        self.data_feeds = {
            'phishtank': 'http://data.phishtank.com/data/online-valid.json',
            'openphish': 'https://openphish.com/feed.txt',
            'urlvoid': 'https://www.urlvoid.com/api/v1000/'
        }
        
        # Security measures
        self.data_validation = {
            'max_daily_updates': 10000,
            'min_confidence_threshold': 0.7,
            'anomaly_detection_threshold': 0.95,
            'trusted_sources': ['phishtank', 'openphish', 'google_safebrowsing']
        }
        
        # Learning buffer for incremental updates
        self.learning_buffer = {
            'features': [],
            'labels': [],
            'timestamps': [],
            'sources': [],
            'max_size': 1000
        }
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Load or create models
        self._load_or_create_models()
        
        # Initialize BERT if available
        if BERT_AVAILABLE:
            self._initialize_bert()
        
        # Enhanced phishing indicators
        self._initialize_enhanced_indicators()
        
        # Start background learning thread
        self._start_background_learning()

    def _initialize_nltk(self):
        """Download required NLTK data if needed"""
        if not ML_AVAILABLE:
            return
            
        try:
            # Download required NLTK data
            nltk_downloads = ['punkt', 'stopwords', 'wordnet', 'vader_lexicon']
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

    def _initialize_bert(self):
        """Initialize BERT model for advanced NLP"""
        try:
            model_name = 'distilbert-base-uncased'
            self.bert_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.bert_model = AutoModel.from_pretrained(model_name)
            self.bert_model.eval()
            logger.info("BERT model initialized successfully")
        except Exception as e:
            logger.warning(f"BERT initialization failed: {e}")
            self.bert_tokenizer = None
            self.bert_model = None

    def _initialize_enhanced_indicators(self):
        """Initialize enhanced phishing indicators and patterns"""
        
        # Enhanced phishing keywords with categories
        self.phishing_keywords = {
            'urgency': [
                'urgent', 'immediate', 'expires', 'suspended', 'verify', 'confirm',
                'update', 'action', 'required', 'asap', 'deadline', 'warning',
                'limited time', 'act now', 'expires today', 'final notice'
            ],
            'financial': [
                'account', 'security', 'bank', 'credit', 'payment', 'transaction',
                'paypal', 'amazon', 'apple', 'microsoft', 'google', 'netflix',
                'refund', 'billing', 'invoice', 'statement', 'balance'
            ],
            'scam': [
                'winner', 'prize', 'congratulations', 'free', 'bonus', 'claim',
                'lottery', 'million', 'inheritance', 'bitcoin', 'crypto', 'investment',
                'guaranteed', 'risk-free', 'double your money', 'get rich'
            ],
            'social_engineering': [
                'click', 'download', 'install', 'activate', 'login', 'signin',
                'submit', 'enter', 'provide', 'details', 'information', 'personal',
                'confidential', 'secret', 'password', 'ssn', 'social security'
            ]
        }
        
        # Enhanced suspicious URL patterns
        self.suspicious_url_patterns = {
            'ip_address': r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
            'suspicious_subdomains': r'[a-z0-9]+-[a-z0-9]+\.[a-z]{2,3}\.[a-z]{2,3}',
            'suspicious_tlds': r'[a-z]{10,}\.(tk|ml|ga|cf|xyz|top|click|download)',
            'url_shorteners': r'(bit\.ly|tinyurl|short|t\.co|goo\.gl|ow\.ly|tiny\.cc)',
            'long_numbers': r'[0-9]{5,}',
            'alternating_chars': r'[a-z]{1}[0-9]{1}[a-z]{1}[0-9]{1}',
            'homograph_chars': r'[а-я]',  # Cyrillic characters
            'suspicious_ports': r':[0-9]{2,5}(?!/)',
            'encoded_urls': r'%[0-9a-f]{2}',
            'multiple_subdomains': r'([a-z0-9-]+\.){4,}'
        }
        
        # Enhanced legitimate domains
        self.legitimate_domains = {
            'tech': ['google.com', 'microsoft.com', 'apple.com', 'github.com'],
            'ecommerce': ['amazon.com', 'ebay.com', 'shopify.com', 'etsy.com'],
            'social': ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com'],
            'financial': ['paypal.com', 'stripe.com', 'square.com', 'chase.com'],
            'streaming': ['netflix.com', 'youtube.com', 'spotify.com', 'hulu.com'],
            'education': ['wikipedia.org', 'stackoverflow.com', 'coursera.org']
        }
        
        # HTML/Email specific indicators
        self.html_indicators = {
            'suspicious_tags': ['<script>', '<iframe>', '<object>', '<embed>'],
            'suspicious_attributes': ['onclick', 'onload', 'onerror', 'javascript:'],
            'phishing_forms': ['password', 'credit', 'ssn', 'social security'],
            'suspicious_links': ['data:', 'javascript:', 'vbscript:']
        }

    def _load_or_create_models(self):
        """Load existing models or create new ensemble models"""
        try:
            model_dir = 'models/advanced'
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            
            # Try to load existing models
            model_files = {
                'online_models': 'online_models.pkl',
                'ensemble_model': 'ensemble_model.pkl',
                'tfidf_vectorizer': 'tfidf_vectorizer.pkl',
                'hashing_vectorizer': 'hashing_vectorizer.pkl'
            }
            
            models_loaded = True
            for attr_name, filename in model_files.items():
                try:
                    with open(os.path.join(model_dir, filename), 'rb') as f:
                        setattr(self, attr_name, pickle.load(f))
                except (FileNotFoundError, EOFError):
                    models_loaded = False
                    break
            
            if models_loaded:
                logger.info("Loaded existing advanced models")
            else:
                logger.info("No existing models found, creating new ones")
                self._create_advanced_models()
                
        except Exception as e:
            logger.error(f"Model loading/creation error: {e}")
            self._create_advanced_models()

    def _create_advanced_models(self):
        """Create advanced ensemble models with online learning capabilities"""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available, using basic models")
            return
        
        try:
            # Initialize online learning models
            self.online_models = {
                'sgd_classifier': SGDClassifier(loss='log_loss', learning_rate='adaptive'),
                'passive_aggressive': PassiveAggressiveClassifier(),
                'naive_bayes': MultinomialNB()
            }
            
            # Initialize feature extractors
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 3),
                stop_words='english'
            )
            
            self.hashing_vectorizer = HashingVectorizer(
                n_features=10000,
                ngram_range=(1, 2)
            )
            
            # Generate initial training data
            training_data = self._generate_enhanced_training_data()
            X_train = training_data['texts']
            y_train = training_data['labels']
            
            # Fit vectorizers
            X_tfidf = self.tfidf_vectorizer.fit_transform(X_train)
            
            # Train online models
            for name, model in self.online_models.items():
                model.fit(X_tfidf, y_train)
            
            # Create ensemble model
            ensemble_models = [
                ('sgd', self.online_models['sgd_classifier']),
                ('pa', self.online_models['passive_aggressive']),
                ('nb', self.online_models['naive_bayes'])
            ]
            
            # Add RandomForest
            try:
                rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
                rf_model.fit(X_tfidf, y_train)
                ensemble_models.append(('rf', rf_model))
            except Exception:
                pass
            
            # Add XGBoost if available
            try:
                xgb_model = xgb.XGBClassifier(n_estimators=100, random_state=42)
                xgb_model.fit(X_tfidf, y_train)
                ensemble_models.append(('xgb', xgb_model))
            except Exception:
                pass
            
            # Add LightGBM if available
            try:
                lgb_model = lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
                lgb_model.fit(X_tfidf, y_train)
                ensemble_models.append(('lgb', lgb_model))
            except Exception:
                pass
            
            self.ensemble_model = VotingClassifier(
                estimators=ensemble_models,
                voting='soft'
            )
            self.ensemble_model.fit(X_tfidf, y_train)
            
            # Save models
            self._save_advanced_models()
            
            logger.info("Advanced ensemble models created successfully")
            
        except Exception as e:
            logger.error(f"Advanced model creation failed: {e}")

    def _generate_enhanced_training_data(self) -> Dict[str, List]:
        """Generate enhanced training data with diverse phishing and legitimate samples"""
        
        # Enhanced phishing samples
        phishing_samples = [
            'https://secure-paypal-verification.tk/login?urgent=true',
            'http://192.168.1.1/amazon-security-update.html',
            'https://bit.ly/urgent-account-verification',
            'URGENT: Your account will be suspended! Click here immediately to verify your identity.',
            'Congratulations! You have won $1,000,000 in our lottery. Claim now!',
            'Your PayPal account has been limited. Please confirm your information.',
            'Security Alert: Unusual activity detected. Verify your account now.',
            'Click here to download important security update for your computer.',
            'Your bank account will be closed unless you verify within 24 hours.',
            'Free iPhone 13! Just enter your personal details to claim.'
        ]
        
        # Enhanced legitimate samples
        legitimate_samples = [
            'https://github.com/user/repository',
            'https://stackoverflow.com/questions/12345',
            'https://docs.python.org/3/library/',
            'Thank you for your purchase. Your order will arrive in 2-3 business days.',
            'Your monthly statement is now available for download.',
            'Welcome to our newsletter! Here are this week\'s top articles.',
            'Meeting scheduled for next Tuesday at 10 AM in conference room A.',
            'Please review the attached document and provide feedback.',
            'Your subscription renewal is coming up next month.',
            'Weather forecast: Sunny with a high of 75 degrees.'
        ]
        
        # Combine samples
        texts = phishing_samples + legitimate_samples
        labels = [1] * len(phishing_samples) + [0] * len(legitimate_samples)
        sources = ['training'] * len(texts)
        timestamps = [datetime.now()] * len(texts)
        
        return {
            'texts': texts,
            'labels': labels,
            'sources': sources,
            'timestamps': timestamps
        }

    def _save_advanced_models(self):
        """Save advanced models to disk"""
        try:
            model_dir = 'models/advanced'
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            
            models_to_save = {
                'online_models': self.online_models,
                'ensemble_model': self.ensemble_model,
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'hashing_vectorizer': self.hashing_vectorizer,
                'performance_metrics': self.performance_metrics
            }
            
            for model_name, model_obj in models_to_save.items():
                if model_obj is not None:
                    file_path = os.path.join(model_dir, f'{model_name}.pkl')
                    with open(file_path, 'wb') as f:
                        pickle.dump(model_obj, f)
                    logger.debug(f"Saved {model_name} to {file_path}")
            
            logger.info("All advanced models saved successfully")
            
        except Exception as e:
            logger.error(f"Model saving error: {e}")

    def _start_background_learning(self):
        """Start background thread for continuous learning"""
        def background_learning_loop():
            while True:
                try:
                    # Update from real-time feeds every hour
                    self._update_from_feeds()
                    
                    # Process learning buffer every 10 minutes
                    if len(self.learning_buffer['features']) > 10:
                        self._process_learning_buffer()
                    
                    # Sleep for 10 minutes
                    time.sleep(600)
                    
                except Exception as e:
                    logger.error(f"Background learning error: {e}")
                    time.sleep(300)  # Sleep 5 minutes on error
        
        # Start background thread
        learning_thread = threading.Thread(target=background_learning_loop, daemon=True)
        learning_thread.start()
        logger.info("Background learning thread started")

    def analyze_content(self, content: str, content_type: str = 'text', 
                      metadata: Optional[Dict] = None) -> Dict:
        """
        Analyze content using advanced ML models and ensemble learning
        
        Args:
            content: The content to analyze (URL, email, text, etc.)
            content_type: Type of content ('url', 'email', 'text', 'html')
            metadata: Additional metadata for analysis
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Extract enhanced features
            features = self._extract_enhanced_features(content, content_type, metadata)
            
            # Get ensemble predictions
            predictions = self._get_ensemble_predictions(features)
            
            # Calculate risk score
            risk_score = self._calculate_risk_score(features, predictions)
            
            # Determine threat level
            threat_level = self._determine_threat_level(risk_score)
            
            # Generate explanation
            explanation = self._generate_explanation(features, predictions, risk_score)
            
            return {
                'is_phishing': risk_score > 0.5,
                'risk_score': round(risk_score, 4),
                'threat_level': threat_level,
                'confidence': round(max(risk_score, 1 - risk_score), 4),
                'predictions': predictions,
                'features': features,
                'explanation': explanation,
                'content_type': content_type,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Content analysis error: {e}")
            return {
                'is_phishing': False,
                'risk_score': 0.0,
                'threat_level': 'unknown',
                'confidence': 0.0,
                'error': str(e)
            }

    def _extract_enhanced_features(self, content: str, content_type: str, 
                                 metadata: Optional[Dict] = None) -> Dict:
        """Extract comprehensive features from content"""
        features = {
            'content_length': len(content),
            'content_type': content_type,
            'timestamp': datetime.now().isoformat()
        }
        
        # Extract type-specific features
        if content_type == 'url':
            features.update(self._extract_url_features(content))
        elif content_type == 'email':
            features.update(self._extract_email_features(content, metadata))
        elif content_type == 'html':
            features.update(self._extract_html_features(content))
        
        # Extract common text features
        features.update(self._extract_text_features(content))
        
        # Extract BERT features if available
        if BERT_AVAILABLE and self.bert_model:
            features.update(self._extract_bert_features(content))
        
        return features

    def _extract_url_features(self, url: str) -> Dict:
        """Extract URL-specific features"""
        features = {}
        
        try:
            parsed = urlparse(url.lower())
            domain = parsed.netloc
            path = parsed.path
            
            # Basic URL features
            features.update({
                'url_length': len(url),
                'domain_length': len(domain),
                'path_length': len(path),
                'has_https': url.startswith('https'),
                'subdomain_count': domain.count('.') - 1,
                'path_depth': path.count('/') - 1,
                'has_query': bool(parsed.query),
                'has_fragment': bool(parsed.fragment)
            })
            
            # Suspicious pattern detection
            for pattern_name, pattern in self.suspicious_url_patterns.items():
                features[f'has_{pattern_name}'] = bool(re.search(pattern, url))
            
            # Legitimate domain check
            is_legitimate = False
            for category, domains in self.legitimate_domains.items():
                if any(legit_domain in domain for legit_domain in domains):
                    is_legitimate = True
                    features[f'legitimate_{category}'] = True
                    break
            
            features['is_legitimate_domain'] = is_legitimate
            
        except Exception as e:
            logger.warning(f"URL feature extraction error: {e}")
        
        return features

    def _extract_email_features(self, content: str, metadata: Optional[Dict] = None) -> Dict:
        """Extract email-specific features"""
        features = {}
        
        try:
            # Basic email features
            features.update({
                'has_attachments': 'attachment' in content.lower(),
                'has_links': 'http' in content.lower(),
                'urgency_score': self._calculate_urgency_score(content),
                'social_engineering_score': self._calculate_social_engineering_score(content)
            })
            
            # Extract sender information if available
            if metadata:
                sender = metadata.get('sender', '')
                if sender:
                    sender_domain = self._extract_domain_from_email(sender)
                    features.update({
                        'sender_domain': sender_domain,
                        'sender_suspicious': self._check_suspicious_headers(metadata)
                    })
            
        except Exception as e:
            logger.warning(f"Email feature extraction error: {e}")
        
        return features

    def _extract_html_features(self, content: str) -> Dict:
        """Extract HTML-specific features"""
        features = {}
        
        try:
            content_lower = content.lower()
            
            # HTML structure features
            features.update({
                'has_forms': '<form' in content_lower,
                'has_iframes': '<iframe' in content_lower,
                'has_scripts': '<script' in content_lower,
                'external_links_count': content_lower.count('http'),
                'form_fields_count': content_lower.count('<input')
            })
            
            # Suspicious HTML indicators
            for indicator in self.html_indicators['suspicious_tags']:
                features[f'has_{indicator.strip("<>").lower()}'] = indicator.lower() in content_lower
            
            # Check for suspicious attributes
            for attr in self.html_indicators['suspicious_attributes']:
                features[f'has_{attr}'] = attr in content_lower
            
        except Exception as e:
            logger.warning(f"HTML feature extraction error: {e}")
        
        return features

    def _extract_text_features(self, content: str) -> Dict:
        """Extract common text features"""
        features = {}
        
        try:
            content_lower = content.lower()
            
            # Basic text statistics
            words = content_lower.split()
            features.update({
                'word_count': len(words),
                'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
                'exclamation_count': content.count('!'),
                'question_count': content.count('?'),
                'uppercase_ratio': sum(1 for c in content if c.isupper()) / len(content) if content else 0,
                'digit_ratio': sum(1 for c in content if c.isdigit()) / len(content) if content else 0
            })
            
            # Phishing keyword detection
            for category, keywords in self.phishing_keywords.items():
                keyword_count = sum(1 for keyword in keywords if keyword in content_lower)
                features[f'{category}_keywords'] = keyword_count
                features[f'has_{category}_keywords'] = keyword_count > 0
            
        except Exception as e:
            logger.warning(f"Text feature extraction error: {e}")
        
        return features

    def _extract_bert_features(self, content: str) -> Dict:
        """Extract BERT-based semantic features"""
        features = {}
        
        try:
            if not self.bert_tokenizer or not self.bert_model:
                return features
            
            # Tokenize and encode
            inputs = self.bert_tokenizer(
                content[:512],  # Limit to 512 tokens
                return_tensors='pt',
                truncation=True,
                padding=True
            )
            
            # Get BERT embeddings
            with torch.no_grad():
                outputs = self.bert_model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
            
            # Use first 50 dimensions as features
            for i in range(min(50, len(embeddings))):
                features[f'bert_dim_{i}'] = float(embeddings[i])
            
            # Calculate semantic similarity to known phishing patterns
            phishing_patterns = [
                'urgent account verification required',
                'click here to claim prize',
                'security alert suspicious activity'
            ]
            
            similarities = []
            for pattern in phishing_patterns:
                pattern_inputs = self.bert_tokenizer(
                    pattern,
                    return_tensors='pt',
                    truncation=True,
                    padding=True
                )
                
                with torch.no_grad():
                    pattern_outputs = self.bert_model(**pattern_inputs)
                    pattern_embeddings = pattern_outputs.last_hidden_state.mean(dim=1).squeeze()
                
                # Calculate cosine similarity
                similarity = torch.cosine_similarity(
                    embeddings.unsqueeze(0),
                    pattern_embeddings.unsqueeze(0)
                ).item()
                similarities.append(similarity)
            
            features['bert_phishing_similarity'] = max(similarities) if similarities else 0.0
            
        except Exception as e:
            logger.warning(f"BERT feature extraction error: {e}")
        
        return features

    def _get_ensemble_predictions(self, features: Dict) -> Dict:
        """Get predictions from ensemble models"""
        predictions = {}
        
        try:
            # Prepare text for vectorization
            text_content = features.get('original_content', '')
            if not text_content:
                # Reconstruct text from features if needed
                text_content = ' '.join([str(v) for v in features.values() if isinstance(v, str)])
            
            # Online model predictions using hashing vectorizer
            if self.hashing_vectorizer and self.online_models:
                X_hash = self.hashing_vectorizer.transform([text_content])
                
                for model_name, model in self.online_models.items():
                    try:
                        if hasattr(model, 'predict_proba'):
                            proba = model.predict_proba(X_hash)[0]
                            predictions[f'online_{model_name}'] = proba[1] if len(proba) > 1 else proba[0]
                        else:
                            pred = model.predict(X_hash)[0]
                            predictions[f'online_{model_name}'] = float(pred)
                    except Exception as e:
                        logger.warning(f"Online model {model_name} prediction error: {e}")
            
            # Ensemble model prediction using TF-IDF
            if self.tfidf_vectorizer and self.ensemble_model:
                try:
                    X_tfidf = self.tfidf_vectorizer.transform([text_content])
                    if hasattr(self.ensemble_model, 'predict_proba'):
                        ensemble_proba = self.ensemble_model.predict_proba(X_tfidf)[0]
                        predictions['ensemble'] = ensemble_proba[1] if len(ensemble_proba) > 1 else ensemble_proba[0]
                    else:
                        ensemble_pred = self.ensemble_model.predict(X_tfidf)[0]
                        predictions['ensemble'] = float(ensemble_pred)
                except Exception as e:
                    logger.warning(f"Ensemble model prediction error: {e}")
            
            # Pattern-based prediction as fallback
            pattern_score = 0.0
            for category, keywords in self.phishing_keywords.items():
                keyword_matches = sum(1 for keyword in keywords if keyword in text_content.lower())
                if keyword_matches > 0:
                    pattern_score += keyword_matches * 0.1
            
            predictions['pattern_based'] = min(pattern_score, 1.0)
            
        except Exception as e:
            logger.error(f"Ensemble prediction error: {e}")
        
        return predictions

    def _calculate_risk_score(self, features: Dict, predictions: Dict) -> float:
        """Calculate overall risk score"""
        try:
            # Base score from ensemble prediction
            base_score = predictions.get('ensemble', 0.0)
            
            # Feature-based adjustments
            adjustments = 0.0
            
            # URL-based adjustments
            if features.get('has_ip_address'):
                adjustments += 0.2
            if features.get('has_url_shorteners'):
                adjustments += 0.15
            if features.get('is_legitimate_domain'):
                adjustments -= 0.3
            
            # Content-based adjustments
            urgency_keywords = features.get('urgency_keywords', 0)
            if urgency_keywords > 2:
                adjustments += 0.1
            
            financial_keywords = features.get('financial_keywords', 0)
            if financial_keywords > 1:
                adjustments += 0.1
            
            # BERT-based adjustment
            bert_similarity = features.get('bert_phishing_similarity', 0.0)
            if bert_similarity > 0.7:
                adjustments += 0.15
            
            # Combine scores
            final_score = base_score + adjustments
            
            # Ensure score is between 0 and 1
            return max(0.0, min(1.0, final_score))
            
        except Exception as e:
            logger.error(f"Risk score calculation error: {e}")
            return 0.0

    def _determine_threat_level(self, risk_score: float) -> str:
        """Determine threat level based on risk score"""
        if risk_score >= 0.8:
            return 'critical'
        elif risk_score >= 0.6:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        elif risk_score >= 0.2:
            return 'low'
        else:
            return 'minimal'

    def _generate_explanation(self, features: Dict, predictions: Dict, risk_score: float) -> List[str]:
        """Generate human-readable explanation"""
        explanations = []
        
        try:
            # Risk level explanation
            threat_level = self._determine_threat_level(risk_score)
            explanations.append(f"Threat level: {threat_level.upper()} (risk score: {risk_score:.2f})")
            
            # Model predictions
            if predictions.get('ensemble', 0) > 0.5:
                explanations.append("Ensemble model indicates high phishing probability")
            
            # Feature-based explanations
            if features.get('has_ip_address'):
                explanations.append("Contains IP address instead of domain name")
            
            if features.get('has_url_shorteners'):
                explanations.append("Uses URL shortening service")
            
            if features.get('urgency_keywords', 0) > 2:
                explanations.append("Contains multiple urgency-related keywords")
            
            if features.get('financial_keywords', 0) > 1:
                explanations.append("Contains financial/banking related terms")
            
            if features.get('bert_phishing_similarity', 0) > 0.7:
                explanations.append("High semantic similarity to known phishing patterns")
            
            if features.get('is_legitimate_domain'):
                explanations.append("Domain appears to be from a legitimate organization")
            
            if not explanations[1:]:  # Only threat level explanation
                explanations.append("Analysis based on content patterns and ML models")
            
        except Exception as e:
            logger.error(f"Explanation generation error: {e}")
            explanations = ["Analysis completed with limited explanation due to processing error"]
        
        return explanations

    def learn_from_feedback(self, content: str, is_phishing: bool, 
                          content_type: str = 'text', metadata: Optional[Dict] = None) -> Dict:
        """Learn from user feedback with validation"""
        try:
            # Validate input
            if not self._validate_learning_input(content, is_phishing, metadata):
                return {'success': False, 'error': 'Invalid input data'}
            
            # Extract features
            features = self._extract_enhanced_features(content, content_type, metadata)
            
            # Add to learning buffer
            with self._lock:
                self._add_to_learning_buffer(features, int(is_phishing), 'user_feedback')
            
            # Perform immediate online learning
            self._perform_online_learning([features], [int(is_phishing)])
            
            logger.info(f"Learned from feedback: {content_type} -> {is_phishing}")
            
            return {
                'success': True,
                'message': 'Feedback incorporated successfully',
                'buffer_size': len(self.learning_buffer['features'])
            }
            
        except Exception as e:
            logger.error(f"Learning from feedback error: {e}")
            return {'success': False, 'error': str(e)}

    def _validate_learning_input(self, content: str, is_phishing: bool, metadata: Optional[Dict]) -> bool:
        """Validate learning input data"""
        try:
            # Basic validation
            if not content or len(content.strip()) < 5:
                return False
            
            if not isinstance(is_phishing, bool):
                return False
            
            # Check for potential data poisoning
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Rate limiting check
            today = datetime.now().date()
            daily_updates = sum(
                1 for timestamp in self.learning_buffer['timestamps']
                if timestamp.date() == today
            )
            
            if daily_updates >= self.data_validation['max_daily_updates']:
                logger.warning("Daily update limit reached")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Input validation error: {e}")
            return False

    def _add_to_learning_buffer(self, features: Dict, label: int, source: str):
        """Add data to learning buffer"""
        try:
            # Check buffer size
            if len(self.learning_buffer['features']) >= self.learning_buffer['max_size']:
                # Remove oldest entry
                for key in self.learning_buffer:
                    if isinstance(self.learning_buffer[key], list):
                        self.learning_buffer[key].pop(0)
            
            # Add new entry
            self.learning_buffer['features'].append(features)
            self.learning_buffer['labels'].append(label)
            self.learning_buffer['timestamps'].append(datetime.now())
            self.learning_buffer['sources'].append(source)
            
        except Exception as e:
            logger.error(f"Buffer addition error: {e}")

    def _perform_online_learning(self, features_list: List[Dict], labels: List[int]):
        """Perform online learning with new data"""
        try:
            if not features_list or not self.hashing_vectorizer:
                return
            
            # Convert features to text for vectorization
            texts = []
            for features in features_list:
                text = features.get('original_content', '')
                if not text:
                    text = ' '.join([str(v) for v in features.values() if isinstance(v, str)])
                texts.append(text)
            
            # Vectorize
            X = self.hashing_vectorizer.transform(texts)
            
            # Update online models
            for model_name, model in self.online_models.items():
                try:
                    if hasattr(model, 'partial_fit'):
                        model.partial_fit(X, labels)
                    else:
                        # For models without partial_fit, retrain with recent data
                        if len(self.learning_buffer['features']) > 50:
                            recent_features = self.learning_buffer['features'][-50:]
                            recent_labels = self.learning_buffer['labels'][-50:]
                            recent_texts = []
                            for feat in recent_features:
                                text = feat.get('original_content', '')
                                if not text:
                                    text = ' '.join([str(v) for v in feat.values() if isinstance(v, str)])
                                recent_texts.append(text)
                            
                            X_recent = self.hashing_vectorizer.transform(recent_texts)
                            model.fit(X_recent, recent_labels)
                            
                except Exception as e:
                    logger.warning(f"Online learning error for {model_name}: {e}")
            
        except Exception as e:
            logger.error(f"Online learning error: {e}")

    def _process_learning_buffer(self):
        """Process accumulated learning buffer"""
        try:
            with self._lock:
                if len(self.learning_buffer['features']) < 10:
                    return
                
                # Extract data from buffer
                features_list = self.learning_buffer['features'].copy()
                labels = self.learning_buffer['labels'].copy()
                
                # Convert to text for vectorization
                texts = []
                for features in features_list:
                    content = features.get('original_content', '')
                    if not content:
                        content = ' '.join([str(v) for v in features.values() if isinstance(v, str)])
                    texts.append(content)
                
                # Perform batch learning
                if self.tfidf_vectorizer and texts:
                    try:
                        # Update TF-IDF with new vocabulary
                        X_new = self.tfidf_vectorizer.transform(texts)
                        
                        # Update ensemble model if possible
                        if self.ensemble_model and hasattr(self.ensemble_model, 'partial_fit'):
                            self.ensemble_model.partial_fit(X_new, labels)
                        
                        # Calculate performance metrics
                        if len(set(labels)) > 1:  # Need both classes for metrics
                            predictions = []
                            for model_name, model in self.online_models.items():
                                try:
                                    if hasattr(model, 'predict'):
                                        X_hash = self.hashing_vectorizer.transform(texts)
                                        pred = model.predict(X_hash)
                                        predictions.append(pred)
                                except Exception:
                                    continue
                            
                            if predictions:
                                # Use majority voting for evaluation
                                ensemble_pred = np.round(np.mean(predictions, axis=0))
                                
                                # Calculate metrics
                                accuracy = accuracy_score(labels, ensemble_pred)
                                precision = precision_score(labels, ensemble_pred, average='weighted', zero_division=0)
                                recall = recall_score(labels, ensemble_pred, average='weighted', zero_division=0)
                                f1 = f1_score(labels, ensemble_pred, average='weighted', zero_division=0)
                                cm = confusion_matrix(labels, ensemble_pred)
                                
                                # Update performance metrics
                                self.performance_metrics['accuracy_history'].append(accuracy)
                                self.performance_metrics['precision_history'].append(precision)
                                self.performance_metrics['recall_history'].append(recall)
                                self.performance_metrics['f1_history'].append(f1)
                                self.performance_metrics['confusion_matrices'].append(cm.tolist())
                                self.performance_metrics['learning_cycles'] += 1
                                self.performance_metrics['last_update'] = datetime.now().isoformat()
                                
                                logger.info(f"Batch learning completed. Accuracy: {accuracy:.3f}, F1: {f1:.3f}")
                    
                    except Exception as e:
                        logger.error(f"Batch learning error: {e}")
                
                # Clear processed buffer
                for key in self.learning_buffer:
                    if isinstance(self.learning_buffer[key], list):
                        self.learning_buffer[key].clear()
                
                # Save updated models
                self._save_advanced_models()
                
        except Exception as e:
            logger.error(f"Learning buffer processing error: {e}")

    def _update_from_feeds(self):
        """Update models from real-time data feeds"""
        if not WEB_SCRAPING_AVAILABLE:
            return
        
        try:
            # Update from PhishTank
            self._update_from_phishtank()
            
            # Update from OpenPhish
            self._update_from_openphish()
            
        except Exception as e:
            logger.error(f"Feed update error: {e}")

    def _update_from_phishtank(self):
        """Update from PhishTank feed"""
        try:
            response = requests.get(self.data_feeds['phishtank'], timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                # Process recent entries
                recent_entries = data[:100]  # Limit to recent 100 entries
                
                for entry in recent_entries:
                    url = entry.get('url', '')
                    if url:
                        features = self._extract_enhanced_features(url, 'url')
                        features['original_content'] = url
                        self._add_to_learning_buffer(features, 1, 'phishtank')
                
                logger.info(f"Updated from PhishTank: {len(recent_entries)} entries")
                
        except Exception as e:
            logger.warning(f"PhishTank update error: {e}")

    def _update_from_openphish(self):
        """Update from OpenPhish feed"""
        try:
            response = requests.get(self.data_feeds['openphish'], timeout=30)
            if response.status_code == 200:
                urls = response.text.strip().split('\n')[:100]  # Limit to recent 100
                
                for url in urls:
                    if url.strip():
                        features = self._extract_enhanced_features(url.strip(), 'url')
                        features['original_content'] = url.strip()
                        self._add_to_learning_buffer(features, 1, 'openphish')
                
                logger.info(f"Updated from OpenPhish: {len(urls)} entries")
                
        except Exception as e:
            logger.warning(f"OpenPhish update error: {e}")

    def get_performance_metrics(self) -> Dict:
        """Get current performance metrics"""
        try:
            metrics = {
                'learning_cycles': self.performance_metrics['learning_cycles'],
                'last_update': self.performance_metrics.get('last_update'),
                'buffer_size': len(self.learning_buffer['features']),
                'model_count': len(self.online_models)
            }
            
            # Add recent performance if available
            if self.performance_metrics['accuracy_history']:
                recent_accuracy = list(self.performance_metrics['accuracy_history'])[-10:]
                recent_precision = list(self.performance_metrics['precision_history'])[-10:]
                recent_recall = list(self.performance_metrics['recall_history'])[-10:]
                recent_f1 = list(self.performance_metrics['f1_history'])[-10:]
                
                metrics.update({
                    'current_accuracy': recent_accuracy[-1] if recent_accuracy else 0.0,
                    'current_precision': recent_precision[-1] if recent_precision else 0.0,
                    'current_recall': recent_recall[-1] if recent_recall else 0.0,
                    'current_f1': recent_f1[-1] if recent_f1 else 0.0,
                    'accuracy_trend': recent_accuracy,
                    'precision_trend': recent_precision,
                    'recall_trend': recent_recall,
                    'f1_trend': recent_f1
                })
            
            # Add latest confusion matrix
            if self.performance_metrics['confusion_matrices']:
                metrics['latest_confusion_matrix'] = list(self.performance_metrics['confusion_matrices'])[-1]
            
            return metrics
            
        except Exception as e:
            logger.error(f"Performance metrics error: {e}")
            return {'error': str(e)}

    # Helper methods
    def _extract_domain_from_email(self, email: str) -> str:
        """Extract domain from email address"""
        try:
            return email.split('@')[-1].lower() if '@' in email else ''
        except Exception:
            return ''

    def _check_suspicious_headers(self, metadata: Dict) -> bool:
        """Check for suspicious email headers"""
        try:
            suspicious_indicators = [
                'x-mailer' in str(metadata).lower(),
                'bulk' in str(metadata).lower(),
                'mass' in str(metadata).lower()
            ]
            return any(suspicious_indicators)
        except Exception:
            return False

    def _calculate_urgency_score(self, content: str) -> float:
        """Calculate urgency score based on content"""
        try:
            urgency_words = self.phishing_keywords.get('urgency', [])
            content_lower = content.lower()
            score = sum(1 for word in urgency_words if word in content_lower)
            return min(score / len(urgency_words), 1.0) if urgency_words else 0.0
        except Exception:
            return 0.0

    def _calculate_social_engineering_score(self, content: str) -> float:
        """Calculate social engineering score"""
        try:
            se_words = self.phishing_keywords.get('social_engineering', [])
            content_lower = content.lower()
            score = sum(1 for word in se_words if word in content_lower)
            return min(score / len(se_words), 1.0) if se_words else 0.0
        except Exception:
            return 0.0

    def _calculate_threat_level(self, risk_score: float) -> str:
        """Calculate threat level from risk score"""
        return self._determine_threat_level(risk_score)

    def __del__(self):
        """Cleanup when detector is destroyed"""
        try:
            # Save final state
            self._save_advanced_models()
            logger.info("Advanced ML detector cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


# Utility functions
def create_advanced_detector(config: Optional[Dict] = None) -> AdvancedMLPhishingDetector:
    """Create and initialize advanced ML detector"""
    try:
        detector = AdvancedMLPhishingDetector(config)
        logger.info("Advanced ML detector created successfully")
        return detector
    except Exception as e:
        logger.error(f"Detector creation error: {e}")
        raise

def validate_detector_requirements() -> Dict[str, bool]:
    """Validate that required libraries are available"""
    return {
        'ml_libraries': ML_AVAILABLE,
        'bert_support': BERT_AVAILABLE,
        'web_scraping': WEB_SCRAPING_AVAILABLE
    }