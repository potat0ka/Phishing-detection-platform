"""
AI Services - Text Analysis and Content Detection
===============================================

This module provides AI-powered analysis services including:
- AI-generated content detection
- Plagiarism detection
- Text authenticity analysis
- Content quality assessment

Author: Bigendra Shrestha
"""

import logging
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class AIContentDetector:
    """AI-generated content detection service"""
    
    def __init__(self):
        self.ai_indicators = [
            # Common AI-generated content patterns
            r'\b(?:as an AI|I cannot|I am not able to|I don\'t have the ability)\b',
            r'\b(?:in conclusion|furthermore|moreover|however|nevertheless)\b',
            r'\b(?:it is worth noting|it should be noted|it is important to)\b',
            r'\b(?:various|numerous|several|multiple|different)\b.*\b(?:aspects|factors|elements)\b',
            r'\b(?:comprehensive|thorough|extensive|detailed)\b.*\b(?:analysis|overview|examination)\b'
        ]
        
        self.human_indicators = [
            # Patterns more common in human writing
            r'\b(?:I think|I feel|I believe|in my opinion|personally)\b',
            r'\b(?:you know|basically|actually|literally|totally)\b',
            r'\b(?:gonna|wanna|gotta|kinda|sorta)\b',
            r'[.!?]{2,}',  # Multiple punctuation marks
            r'\b(?:lol|haha|omg|wtf|tbh|imo)\b'
        ]
    
    def analyze_text_authenticity(self, text: str) -> Dict:
        """
        Analyze text for AI-generated content indicators
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dict containing analysis results
        """
        if not text or len(text.strip()) < 50:
            return {
                'is_ai_generated': False,
                'confidence_score': 0.0,
                'reason': 'Text too short for analysis',
                'indicators': []
            }
        
        try:
            # Count AI and human indicators
            ai_score = 0
            human_score = 0
            found_indicators = []
            
            # Check for AI patterns
            for pattern in self.ai_indicators:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    ai_score += len(matches)
                    found_indicators.extend([f"AI pattern: {match}" for match in matches])
            
            # Check for human patterns
            for pattern in self.human_indicators:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    human_score += len(matches)
                    found_indicators.extend([f"Human pattern: {match}" for match in matches])
            
            # Additional checks
            sentences = text.split('.')
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
            
            # Very uniform sentence length can indicate AI
            if avg_sentence_length > 20:
                ai_score += 1
                found_indicators.append("Uniform long sentences")
            
            # Calculate confidence
            total_score = ai_score + human_score
            if total_score == 0:
                confidence = 0.5  # Neutral
                is_ai = False
            else:
                ai_probability = ai_score / total_score
                confidence = abs(ai_probability - 0.5) * 2  # Scale to 0-1
                is_ai = ai_probability > 0.6
            
            return {
                'is_ai_generated': is_ai,
                'confidence_score': round(confidence, 2),
                'ai_score': ai_score,
                'human_score': human_score,
                'reason': f"Analysis based on {total_score} indicators",
                'indicators': found_indicators[:10],  # Limit to top 10
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in AI content analysis: {e}")
            return {
                'is_ai_generated': False,
                'confidence_score': 0.0,
                'reason': f'Analysis error: {str(e)}',
                'indicators': []
            }

class PlagiarismDetector:
    """Plagiarism detection service"""
    
    def __init__(self):
        self.common_sources = [
            "wikipedia.org",
            "britannica.com",
            "academic.edu",
            "researchgate.net",
            "scholar.google.com"
        ]
    
    def check_plagiarism(self, text: str, check_online: bool = False) -> Dict:
        """
        Check text for potential plagiarism
        
        Args:
            text: Text content to check
            check_online: Whether to check against online sources
            
        Returns:
            Dict containing plagiarism analysis results
        """
        if not text or len(text.strip()) < 100:
            return {
                'has_plagiarism': False,
                'confidence_score': 0.0,
                'sources_found': [],
                'reason': 'Text too short for plagiarism detection'
            }
        
        try:
            # Basic plagiarism indicators
            plagiarism_score = 0
            found_sources = []
            indicators = []
            
            # Check for common academic phrases that might indicate copying
            academic_phrases = [
                r'\b(?:according to|as stated by|as mentioned in)\b',
                r'\b(?:research shows|studies indicate|data suggests)\b',
                r'\b(?:it has been established|it is well known)\b'
            ]
            
            for pattern in academic_phrases:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                if matches > 3:  # Too many academic phrases might indicate copying
                    plagiarism_score += matches
                    indicators.append(f"Excessive academic language: {matches} instances")
            
            # Check for repetitive patterns
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            if len(sentences) > 5:
                similar_sentences = 0
                for i, sentence in enumerate(sentences[:-1]):
                    for j, other_sentence in enumerate(sentences[i+1:], i+1):
                        if len(sentence) > 20 and len(other_sentence) > 20:
                            # Simple similarity check
                            words1 = set(sentence.lower().split())
                            words2 = set(other_sentence.lower().split())
                            similarity = len(words1.intersection(words2)) / len(words1.union(words2))
                            if similarity > 0.7:
                                similar_sentences += 1
                
                if similar_sentences > 2:
                    plagiarism_score += similar_sentences
                    indicators.append(f"Similar sentence patterns: {similar_sentences}")
            
            # Calculate confidence
            confidence = min(plagiarism_score / 10, 1.0)  # Scale to 0-1
            has_plagiarism = confidence > 0.3
            
            return {
                'has_plagiarism': has_plagiarism,
                'confidence_score': round(confidence, 2),
                'plagiarism_score': plagiarism_score,
                'sources_found': found_sources,
                'indicators': indicators,
                'reason': f"Analysis based on {len(indicators)} indicators",
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in plagiarism detection: {e}")
            return {
                'has_plagiarism': False,
                'confidence_score': 0.0,
                'sources_found': [],
                'reason': f'Detection error: {str(e)}'
            }

class TextQualityAnalyzer:
    """Text quality and readability analyzer"""
    
    def analyze_quality(self, text: str) -> Dict:
        """
        Analyze text quality and readability
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dict containing quality analysis results
        """
        if not text or len(text.strip()) < 50:
            return {
                'quality_score': 0.0,
                'readability': 'Unknown',
                'issues': ['Text too short for analysis']
            }
        
        try:
            issues = []
            quality_score = 100  # Start with perfect score and deduct points
            
            # Word and sentence counts
            words = text.split()
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            # Average sentence length
            avg_sentence_length = len(words) / len(sentences) if sentences else 0
            
            if avg_sentence_length < 5:
                quality_score -= 10
                issues.append("Very short sentences")
            elif avg_sentence_length > 30:
                quality_score -= 15
                issues.append("Very long sentences")
            
            # Check for grammar issues (basic)
            if text.count('  ') > 5:  # Multiple spaces
                quality_score -= 5
                issues.append("Formatting issues")
            
            # Check capitalization
            if text.islower() or text.isupper():
                quality_score -= 20
                issues.append("Poor capitalization")
            
            # Vocabulary diversity
            unique_words = len(set(word.lower() for word in words))
            vocabulary_ratio = unique_words / len(words) if words else 0
            
            if vocabulary_ratio < 0.3:
                quality_score -= 15
                issues.append("Limited vocabulary")
            
            # Determine readability
            if avg_sentence_length < 15 and vocabulary_ratio > 0.4:
                readability = "Easy"
            elif avg_sentence_length < 20 and vocabulary_ratio > 0.3:
                readability = "Medium"
            else:
                readability = "Hard"
            
            quality_score = max(quality_score, 0)  # Don't go below 0
            
            return {
                'quality_score': round(quality_score, 1),
                'readability': readability,
                'avg_sentence_length': round(avg_sentence_length, 1),
                'vocabulary_ratio': round(vocabulary_ratio, 2),
                'word_count': len(words),
                'sentence_count': len(sentences),
                'issues': issues,
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in quality analysis: {e}")
            return {
                'quality_score': 0.0,
                'readability': 'Unknown',
                'issues': [f'Analysis error: {str(e)}']
            }

# Global service instances
ai_detector = AIContentDetector()
plagiarism_detector = PlagiarismDetector()
quality_analyzer = TextQualityAnalyzer()

def analyze_text_comprehensive(text: str) -> Dict:
    """
    Comprehensive text analysis combining all services
    
    Args:
        text: Text content to analyze
        
    Returns:
        Dict containing complete analysis results
    """
    try:
        # Run all analyses
        ai_analysis = ai_detector.analyze_text_authenticity(text)
        plagiarism_analysis = plagiarism_detector.check_plagiarism(text)
        quality_analysis = quality_analyzer.analyze_quality(text)
        
        # Combine results
        return {
            'success': True,
            'text_length': len(text),
            'ai_detection': ai_analysis,
            'plagiarism_check': plagiarism_analysis,
            'quality_analysis': quality_analysis,
            'overall_score': {
                'authenticity': 100 - (ai_analysis['confidence_score'] * 100) if ai_analysis['is_ai_generated'] else 50 + (ai_analysis['confidence_score'] * 50),
                'originality': 100 - (plagiarism_analysis['confidence_score'] * 100),
                'quality': quality_analysis['quality_score']
            },
            'analysis_timestamp': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in comprehensive text analysis: {e}")
        return {
            'success': False,
            'error': str(e),
            'analysis_timestamp': datetime.utcnow().isoformat()
        }