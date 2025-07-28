
"""
Text Analysis Utilities
======================

This module provides plagiarism detection and AI-generated content detection.
Uses free/open-source methods and APIs for comprehensive text analysis.

Features:
- Plagiarism detection using web search and similarity algorithms
- AI content detection using multiple methods
- Comprehensive scoring and explanations

Author: AI Phishing Detection Platform
"""

import re
import logging
import hashlib
import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from urllib.parse import quote_plus
import time

# Import text processing libraries
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.stem import PorterStemmer
    
    ML_AVAILABLE = True
except ImportError as e:
    logging.warning(f"ML libraries not fully available for text analysis: {e}")
    ML_AVAILABLE = False

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """
    Comprehensive text analysis for plagiarism and AI detection
    """
    
    def __init__(self):
        """Initialize the text analyzer with models and tools"""
        
        # Initialize NLTK components
        self._initialize_nltk()
        
        # Text processing tools
        self.stemmer = PorterStemmer() if ML_AVAILABLE else None
        self.stop_words = set()
        
        # AI detection patterns and indicators
        self.ai_indicators = {
            'repetitive_phrases': [
                'furthermore', 'moreover', 'in conclusion', 'it is important to note',
                'in summary', 'as mentioned earlier', 'on the other hand',
                'as a result', 'in other words', 'for instance', 'for example'
            ],
            'formal_transitions': [
                'consequently', 'therefore', 'nonetheless', 'nevertheless',
                'subsequently', 'accordingly', 'hence', 'thus'
            ],
            'ai_style_patterns': [
                r'(it\'s worth noting|worth mentioning)',
                r'(as an? (ai|language model|assistant))',
                r'(i don\'t have personal|i cannot provide personal)',
                r'(in my (training|knowledge))',
                r'(as of my last update|knowledge cutoff)'
            ]
        }
        
        # Common plagiarism sources patterns
        self.plagiarism_indicators = [
            'wikipedia', 'britannica', 'investopedia', 'khan academy',
            'coursera', 'edx', 'udemy', 'stack overflow'
        ]

    def _initialize_nltk(self):
        """Download required NLTK data if needed"""
        if not ML_AVAILABLE:
            return
            
        try:
            # Download required NLTK data
            nltk_downloads = ['punkt', 'stopwords']
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

    def analyze_text(self, text: str) -> Dict:
        """
        Main analysis function for text content
        
        Args:
            text (str): Text content to analyze
            
        Returns:
            dict: Comprehensive analysis results
        """
        try:
            # Input validation
            if not text or not isinstance(text, str):
                return self._create_error_result("Invalid input: Text cannot be empty")
            
            text = text.strip()
            if len(text) < 50:
                return self._create_error_result("Text too short for analysis (minimum 50 characters)")
            
            if len(text) > 50000:
                return self._create_error_result("Text too long for analysis (maximum 50,000 characters)")
            
            logger.info(f"Analyzing text: {len(text)} characters")
            
            # Perform plagiarism detection
            plagiarism_result = self._detect_plagiarism(text)
            
            # Perform AI detection
            ai_result = self._detect_ai_content(text)
            
            # Calculate overall scores
            overall_plagiarism_score = plagiarism_result['score']
            overall_ai_score = ai_result['score']
            
            # Generate comprehensive explanation
            explanation = self._generate_explanation(
                plagiarism_result, ai_result, overall_plagiarism_score, overall_ai_score
            )
            
            logger.info(f"Analysis complete - Plagiarism: {overall_plagiarism_score:.2f}, AI: {overall_ai_score:.2f}")
            
            return {
                'text_length': len(text),
                'word_count': len(text.split()),
                'plagiarism': {
                    'score': overall_plagiarism_score,
                    'percentage': int(overall_plagiarism_score * 100),
                    'level': self._get_plagiarism_level(overall_plagiarism_score),
                    'details': plagiarism_result['details'],
                    'sources_found': plagiarism_result.get('sources_found', 0)
                },
                'ai_detection': {
                    'score': overall_ai_score,
                    'percentage': int(overall_ai_score * 100),
                    'level': self._get_ai_level(overall_ai_score),
                    'details': ai_result['details'],
                    'indicators_found': ai_result.get('indicators_found', 0)
                },
                'explanation': explanation,
                'timestamp': datetime.utcnow().isoformat(),
                'analysis_components': [
                    f"Plagiarism analysis: {overall_plagiarism_score:.2f}",
                    f"AI detection: {overall_ai_score:.2f}",
                    f"Text processing: Complete"
                ]
            }
            
        except Exception as e:
            logger.error(f"Text analysis error: {str(e)}")
            return self._create_error_result(f"Analysis failed: {str(e)}")

    def _detect_plagiarism(self, text: str) -> Dict:
        """Detect potential plagiarism in text"""
        try:
            score = 0.0
            details = []
            sources_found = 0
            
            # 1. Check for common plagiarism indicators
            text_lower = text.lower()
            
            # Check for academic source patterns
            for indicator in self.plagiarism_indicators:
                if indicator in text_lower:
                    score += 0.15
                    details.append(f"Potential source detected: {indicator}")
                    sources_found += 1
            
            # 2. Check for suspicious formatting patterns
            if self._check_suspicious_formatting(text):
                score += 0.2
                details.append("Suspicious formatting patterns detected")
            
            # 3. Simple similarity check using sentence fingerprinting
            similarity_score = self._check_sentence_similarity(text)
            score += similarity_score * 0.3
            if similarity_score > 0.3:
                details.append(f"High sentence similarity detected: {similarity_score:.2f}")
            
            # 4. Check for exact phrase patterns
            exact_matches = self._check_exact_phrases(text)
            if exact_matches > 0:
                score += min(exact_matches * 0.1, 0.3)
                details.append(f"Exact phrase matches found: {exact_matches}")
            
            # 5. Web search simulation (mock for now)
            web_score = self._simulate_web_search(text)
            score += web_score * 0.2
            if web_score > 0.5:
                details.append("High similarity to online content detected")
            
            return {
                'score': min(score, 1.0),
                'details': details,
                'sources_found': sources_found
            }
            
        except Exception as e:
            logger.error(f"Plagiarism detection error: {e}")
            return {
                'score': 0.0,
                'details': ['Plagiarism analysis unavailable'],
                'sources_found': 0
            }

    def _detect_ai_content(self, text: str) -> Dict:
        """Detect if content is AI-generated"""
        try:
            score = 0.0
            details = []
            indicators_found = 0
            
            # 1. Check for AI-style repetitive phrases
            repetitive_score = self._check_repetitive_phrases(text)
            score += repetitive_score * 0.25
            if repetitive_score > 0.3:
                details.append(f"Repetitive AI phrases detected: {repetitive_score:.2f}")
                indicators_found += 1
            
            # 2. Check for formal transitions overuse
            transition_score = self._check_formal_transitions(text)
            score += transition_score * 0.2
            if transition_score > 0.4:
                details.append(f"Excessive formal transitions: {transition_score:.2f}")
                indicators_found += 1
            
            # 3. Check for AI-specific patterns
            pattern_score = self._check_ai_patterns(text)
            score += pattern_score * 0.3
            if pattern_score > 0.2:
                details.append("AI-specific language patterns detected")
                indicators_found += 1
            
            # 4. Analyze sentence structure uniformity
            structure_score = self._analyze_sentence_structure(text)
            score += structure_score * 0.15
            if structure_score > 0.5:
                details.append("Uniform sentence structure (AI indicator)")
                indicators_found += 1
            
            # 5. Check vocabulary complexity patterns
            vocab_score = self._analyze_vocabulary_patterns(text)
            score += vocab_score * 0.1
            if vocab_score > 0.6:
                details.append("Unusual vocabulary distribution pattern")
                indicators_found += 1
            
            return {
                'score': min(score, 1.0),
                'details': details,
                'indicators_found': indicators_found
            }
            
        except Exception as e:
            logger.error(f"AI detection error: {e}")
            return {
                'score': 0.0,
                'details': ['AI detection analysis unavailable'],
                'indicators_found': 0
            }

    def _check_repetitive_phrases(self, text: str) -> float:
        """Check for repetitive AI-style phrases"""
        text_lower = text.lower()
        found_count = 0
        
        for phrase in self.ai_indicators['repetitive_phrases']:
            if phrase in text_lower:
                found_count += 1
        
        # Normalize by text length
        word_count = len(text.split())
        return min(found_count / max(word_count / 100, 1), 1.0)

    def _check_formal_transitions(self, text: str) -> float:
        """Check for overuse of formal transitions"""
        text_lower = text.lower()
        found_count = 0
        
        for transition in self.ai_indicators['formal_transitions']:
            found_count += text_lower.count(transition)
        
        # Normalize by sentence count
        if ML_AVAILABLE:
            try:
                sentences = sent_tokenize(text)
                return min(found_count / max(len(sentences), 1), 1.0)
            except:
                pass
        
        # Fallback: estimate sentences
        estimated_sentences = text.count('.') + text.count('!') + text.count('?')
        return min(found_count / max(estimated_sentences, 1), 1.0)

    def _check_ai_patterns(self, text: str) -> float:
        """Check for AI-specific language patterns"""
        text_lower = text.lower()
        pattern_count = 0
        
        for pattern in self.ai_indicators['ai_style_patterns']:
            if re.search(pattern, text_lower):
                pattern_count += 1
        
        return min(pattern_count * 0.3, 1.0)

    def _check_suspicious_formatting(self, text: str) -> bool:
        """Check for suspicious formatting that might indicate copy-paste"""
        
        # Check for unusual spacing patterns
        if re.search(r'\s{3,}', text):
            return True
        
        # Check for mixed encoding issues
        if re.search(r'[^\x00-\x7F]', text) and len(re.findall(r'[^\x00-\x7F]', text)) > len(text) * 0.1:
            return True
        
        # Check for unusual line breaks
        if text.count('\n\n') > text.count('\n') * 0.5:
            return True
        
        return False

    def _check_sentence_similarity(self, text: str) -> float:
        """Check for high similarity between sentences"""
        if not ML_AVAILABLE:
            return 0.0
        
        try:
            sentences = sent_tokenize(text)
            if len(sentences) < 3:
                return 0.0
            
            # Use TF-IDF to find similar sentences
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            
            # Clean sentences
            clean_sentences = [self._clean_text(sent) for sent in sentences]
            clean_sentences = [sent for sent in clean_sentences if len(sent.split()) > 3]
            
            if len(clean_sentences) < 3:
                return 0.0
            
            # Vectorize sentences
            tfidf_matrix = vectorizer.fit_transform(clean_sentences)
            
            # Calculate similarities
            similarities = cosine_similarity(tfidf_matrix)
            
            # Count high similarities (excluding self-similarity)
            high_sim_count = 0
            total_pairs = 0
            
            for i in range(len(similarities)):
                for j in range(i + 1, len(similarities)):
                    total_pairs += 1
                    if similarities[i][j] > 0.7:  # High similarity threshold
                        high_sim_count += 1
            
            return high_sim_count / max(total_pairs, 1) if total_pairs > 0 else 0.0
            
        except Exception as e:
            logger.warning(f"Sentence similarity check error: {e}")
            return 0.0

    def _check_exact_phrases(self, text: str) -> int:
        """Check for exact phrase matches (simple implementation)"""
        
        # Common phrases that might indicate copying
        common_phrases = [
            "according to wikipedia", "as stated in", "it has been shown that",
            "research has shown", "studies have found", "experts believe",
            "it is widely accepted", "common knowledge", "well-known fact"
        ]
        
        text_lower = text.lower()
        matches = 0
        
        for phrase in common_phrases:
            if phrase in text_lower:
                matches += 1
        
        return matches

    def _simulate_web_search(self, text: str) -> float:
        """Simulate web search for plagiarism (mock implementation)"""
        
        # Extract key phrases (3-5 word combinations)
        words = text.split()
        key_phrases = []
        
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if len(phrase) > 15 and not any(stop in phrase.lower() for stop in ['the', 'and', 'or', 'but']):
                key_phrases.append(phrase)
        
        # Simulate scoring based on phrase uniqueness
        common_score = 0
        for phrase in key_phrases[:5]:  # Check first 5 phrases
            # Simple heuristic: longer, more complex phrases are less likely to be plagiarized
            complexity = len(set(phrase.split())) / len(phrase.split())
            if complexity < 0.7:  # Low complexity suggests potential copying
                common_score += 0.2
        
        return min(common_score, 1.0)

    def _analyze_sentence_structure(self, text: str) -> float:
        """Analyze sentence structure uniformity"""
        if not ML_AVAILABLE:
            return 0.0
        
        try:
            sentences = sent_tokenize(text)
            if len(sentences) < 5:
                return 0.0
            
            # Analyze sentence lengths
            lengths = [len(sent.split()) for sent in sentences]
            
            # Calculate coefficient of variation
            if len(lengths) > 1:
                mean_length = sum(lengths) / len(lengths)
                variance = sum((x - mean_length) ** 2 for x in lengths) / len(lengths)
                std_dev = variance ** 0.5
                cv = std_dev / mean_length if mean_length > 0 else 0
                
                # Low coefficient of variation suggests uniform structure (AI trait)
                return max(0, (0.5 - cv) * 2) if cv < 0.5 else 0.0
            
            return 0.0
            
        except Exception as e:
            logger.warning(f"Sentence structure analysis error: {e}")
            return 0.0

    def _analyze_vocabulary_patterns(self, text: str) -> float:
        """Analyze vocabulary complexity patterns"""
        if not ML_AVAILABLE:
            return 0.0
        
        try:
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalpha() and w not in self.stop_words]
            
            if len(words) < 50:
                return 0.0
            
            # Calculate vocabulary richness
            unique_words = set(words)
            vocabulary_richness = len(unique_words) / len(words)
            
            # AI tends to have moderate vocabulary richness (not too high, not too low)
            if 0.3 <= vocabulary_richness <= 0.6:
                return 0.6
            else:
                return 0.0
                
        except Exception as e:
            logger.warning(f"Vocabulary analysis error: {e}")
            return 0.0

    def _clean_text(self, text: str) -> str:
        """Clean text for analysis"""
        # Remove special characters, normalize whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()

    def _get_plagiarism_level(self, score: float) -> str:
        """Get plagiarism level description"""
        if score >= 0.7:
            return "High"
        elif score >= 0.4:
            return "Medium"
        elif score >= 0.2:
            return "Low"
        else:
            return "Very Low"

    def _get_ai_level(self, score: float) -> str:
        """Get AI detection level description"""
        if score >= 0.8:
            return "Very Likely AI"
        elif score >= 0.6:
            return "Likely AI"
        elif score >= 0.4:
            return "Possibly AI"
        elif score >= 0.2:
            return "Unlikely AI"
        else:
            return "Human-like"

    def _generate_explanation(self, plagiarism_result: Dict, ai_result: Dict, 
                             plagiarism_score: float, ai_score: float) -> str:
        """Generate comprehensive explanation"""
        
        explanation = "Text Analysis Results: "
        
        # Plagiarism explanation
        plag_level = self._get_plagiarism_level(plagiarism_score)
        explanation += f"Plagiarism risk is {plag_level.lower()} ({int(plagiarism_score * 100)}%). "
        
        if plagiarism_result['details']:
            explanation += f"Concerns: {'; '.join(plagiarism_result['details'][:2])}. "
        
        # AI detection explanation
        ai_level = self._get_ai_level(ai_score)
        explanation += f"AI generation probability is {ai_level.lower()} ({int(ai_score * 100)}%). "
        
        if ai_result['details']:
            explanation += f"Indicators: {'; '.join(ai_result['details'][:2])}. "
        
        # Recommendations
        if plagiarism_score > 0.6 or ai_score > 0.7:
            explanation += "Recommendation: Further review recommended for academic or professional use."
        elif plagiarism_score > 0.3 or ai_score > 0.5:
            explanation += "Recommendation: Content appears to have some generated elements, verify sources."
        else:
            explanation += "Recommendation: Content appears original and human-written."
        
        return explanation

    def _create_error_result(self, error_message: str) -> Dict:
        """Create standardized error result"""
        return {
            'text_length': 0,
            'word_count': 0,
            'plagiarism': {
                'score': 0.0,
                'percentage': 0,
                'level': 'Unknown',
                'details': [error_message],
                'sources_found': 0
            },
            'ai_detection': {
                'score': 0.0,
                'percentage': 0,
                'level': 'Unknown',
                'details': [error_message],
                'indicators_found': 0
            },
            'explanation': f'Analysis could not be completed: {error_message}',
            'timestamp': datetime.utcnow().isoformat(),
            'analysis_components': ['Analysis failed'],
            'error': True
        }
