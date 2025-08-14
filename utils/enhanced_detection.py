"""Enhanced Detection Algorithms for AI Content and Plagiarism
===============================================================

This module provides advanced detection algorithms with improved accuracy:
- Enhanced AI-generated content detection using multiple analysis layers
- Advanced plagiarism detection with semantic similarity
- Statistical analysis and linguistic pattern recognition
- Machine learning-inspired scoring mechanisms

Author: AI Phishing Detection Platform
"""

import re
import math
import logging
import statistics
from typing import Dict, List, Tuple, Any
from datetime import datetime
from collections import Counter
import hashlib

logger = logging.getLogger(__name__)

class EnhancedAIDetector:
    """Enhanced AI content detection with multiple analysis layers"""
    
    def __init__(self):
        # Advanced AI patterns with weighted scoring
        self.ai_patterns = {
            # High confidence AI indicators (weight: 3.0)
            'formal_transitions': {
                'patterns': [
                    r'\b(?:furthermore|moreover|consequently|therefore|nonetheless|nevertheless|additionally|subsequently)\b',
                    r'\b(?:in conclusion|in summary|to summarize|in essence|ultimately)\b',
                    r'\b(?:it is important to note|it should be noted|it is worth mentioning)\b'
                ],
                'weight': 3.0,
                'threshold': 2
            },
            # Medium confidence indicators (weight: 2.0)
            'structured_language': {
                'patterns': [
                    r'\b(?:various|numerous|several|multiple|different)\s+(?:aspects|factors|elements|components)\b',
                    r'\b(?:comprehensive|thorough|extensive|detailed)\s+(?:analysis|overview|examination|approach)\b',
                    r'\b(?:it is crucial|it is essential|it is vital|it is imperative)\b'
                ],
                'weight': 2.0,
                'threshold': 1
            },
            # Low confidence indicators (weight: 1.0)
            'generic_phrases': {
                'patterns': [
                    r'\b(?:as mentioned earlier|as previously discussed|as we have seen)\b',
                    r'\b(?:in today\'s world|in modern society|in contemporary times)\b',
                    r'\b(?:plays a crucial role|serves as|acts as)\b'
                ],
                'weight': 1.0,
                'threshold': 1
            }
        }
        
        # Human writing indicators
        self.human_patterns = {
            'personal_expressions': {
                'patterns': [
                    r'\b(?:I think|I feel|I believe|in my opinion|personally|from my perspective)\b',
                    r'\b(?:you know|basically|actually|literally|totally|honestly)\b',
                    r'\b(?:gonna|wanna|gotta|kinda|sorta|dunno)\b'
                ],
                'weight': 2.5,
                'threshold': 1
            },
            'informal_language': {
                'patterns': [
                    r'[.!?]{2,}',  # Multiple punctuation
                    r'\b(?:lol|haha|omg|wtf|tbh|imo|btw|fyi)\b',
                    r'\b(?:super|really|pretty|quite)\s+(?:good|bad|nice|cool|awesome)\b'
                ],
                'weight': 2.0,
                'threshold': 1
            }
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Enhanced AI content analysis with multiple detection layers"""
        if not text or len(text.strip()) < 50:
            return {
                'is_ai_generated': False,
                'confidence_score': 0.0,
                'ai_probability': 0.0,
                'analysis_details': {'reason': 'Text too short for reliable analysis'},
                'indicators': []
            }
        
        try:
            # Layer 1: Pattern-based analysis
            pattern_score, pattern_indicators = self._analyze_patterns(text)
            
            # Layer 2: Statistical analysis
            stats_score, stats_indicators = self._analyze_statistics(text)
            
            # Layer 3: Linguistic analysis
            linguistic_score, linguistic_indicators = self._analyze_linguistics(text)
            
            # Layer 4: Structural analysis
            structure_score, structure_indicators = self._analyze_structure(text)
            
            # Combine scores with weighted averaging
            weights = {'patterns': 0.3, 'statistics': 0.25, 'linguistics': 0.25, 'structure': 0.2}
            
            final_score = (
                pattern_score * weights['patterns'] +
                stats_score * weights['statistics'] +
                linguistic_score * weights['linguistics'] +
                structure_score * weights['structure']
            )
            
            # Apply confidence calibration
            calibrated_score = self._calibrate_score(final_score, len(text))
            
            # Determine final verdict
            is_ai = calibrated_score > 0.6
            confidence = min(abs(calibrated_score - 0.5) * 2, 1.0)
            
            all_indicators = pattern_indicators + stats_indicators + linguistic_indicators + structure_indicators
            
            return {
                'is_ai_generated': is_ai,
                'confidence_score': round(confidence, 3),
                'ai_probability': round(calibrated_score, 3),
                'analysis_details': {
                    'pattern_score': round(pattern_score, 3),
                    'statistics_score': round(stats_score, 3),
                    'linguistic_score': round(linguistic_score, 3),
                    'structure_score': round(structure_score, 3),
                    'text_length': len(text),
                    'word_count': len(text.split())
                },
                'indicators': all_indicators[:10],
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Enhanced AI detection error: {e}")
            return {
                'is_ai_generated': False,
                'confidence_score': 0.0,
                'ai_probability': 0.0,
                'analysis_details': {'error': str(e)},
                'indicators': []
            }
    
    def _analyze_patterns(self, text: str) -> Tuple[float, List[str]]:
        """Pattern-based analysis using weighted indicators"""
        ai_score = 0
        human_score = 0
        indicators = []
        
        # Check AI patterns
        for category, config in self.ai_patterns.items():
            matches = 0
            for pattern in config['patterns']:
                pattern_matches = len(re.findall(pattern, text, re.IGNORECASE))
                matches += pattern_matches
            
            if matches >= config['threshold']:
                weighted_score = matches * config['weight']
                ai_score += weighted_score
                indicators.append(f"AI pattern ({category}): {matches} matches")
        
        # Check human patterns
        for category, config in self.human_patterns.items():
            matches = 0
            for pattern in config['patterns']:
                pattern_matches = len(re.findall(pattern, text, re.IGNORECASE))
                matches += pattern_matches
            
            if matches >= config['threshold']:
                weighted_score = matches * config['weight']
                human_score += weighted_score
                indicators.append(f"Human pattern ({category}): {matches} matches")
        
        # Normalize score
        total_score = ai_score + human_score
        if total_score == 0:
            return 0.5, indicators
        
        pattern_score = ai_score / total_score
        return pattern_score, indicators
    
    def _analyze_statistics(self, text: str) -> Tuple[float, List[str]]:
        """Statistical analysis of text properties"""
        indicators = []
        score = 0.5  # Start neutral
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 3:
            return score, indicators
        
        # Sentence length analysis
        sentence_lengths = [len(s.split()) for s in sentences]
        if sentence_lengths:
            avg_length = statistics.mean(sentence_lengths)
            std_dev = statistics.stdev(sentence_lengths) if len(sentence_lengths) > 1 else 0
            
            # AI tends to have consistent sentence lengths
            if 15 <= avg_length <= 25 and std_dev < 8:
                score += 0.15
                indicators.append(f"Consistent sentence length (avg: {avg_length:.1f}, std: {std_dev:.1f})")
            
            # Very uniform lengths are suspicious
            if std_dev < 3 and len(sentences) > 5:
                score += 0.1
                indicators.append("Extremely uniform sentence lengths")
        
        # Vocabulary diversity analysis
        words = re.findall(r'\b\w+\b', text.lower())
        if words:
            unique_words = len(set(words))
            total_words = len(words)
            diversity_ratio = unique_words / total_words
            
            # AI often has lower vocabulary diversity
            if diversity_ratio < 0.6:
                score += 0.1
                indicators.append(f"Low vocabulary diversity ({diversity_ratio:.2f})")
            elif diversity_ratio > 0.8:
                score -= 0.1
                indicators.append(f"High vocabulary diversity ({diversity_ratio:.2f})")
        
        return min(max(score, 0), 1), indicators
    
    def _analyze_linguistics(self, text: str) -> Tuple[float, List[str]]:
        """Linguistic pattern analysis"""
        indicators = []
        score = 0.5
        
        # Pronoun usage analysis
        personal_pronouns = ['i', 'me', 'my', 'myself', 'we', 'us', 'our', 'you', 'your']
        pronoun_count = sum(1 for word in text.lower().split() if word in personal_pronouns)
        word_count = len(text.split())
        
        if word_count > 0:
            pronoun_ratio = pronoun_count / word_count
            
            # AI tends to avoid personal pronouns
            if pronoun_ratio < 0.02 and word_count > 100:
                score += 0.15
                indicators.append(f"Very low personal pronoun usage ({pronoun_ratio:.3f})")
            elif pronoun_ratio > 0.08:
                score -= 0.1
                indicators.append(f"High personal pronoun usage ({pronoun_ratio:.3f})")
        
        # Passive voice detection
        passive_patterns = [
            r'\b(?:is|are|was|were|being|been)\s+\w+ed\b',
            r'\b(?:is|are|was|were)\s+\w+en\b'
        ]
        
        passive_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in passive_patterns)
        if passive_count > len(text.split()) * 0.1:  # More than 10% passive voice
            score += 0.1
            indicators.append(f"High passive voice usage ({passive_count} instances)")
        
        return min(max(score, 0), 1), indicators
    
    def _analyze_structure(self, text: str) -> Tuple[float, List[str]]:
        """Structural analysis of text organization"""
        indicators = []
        score = 0.5
        
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if len(paragraphs) > 1:
            para_lengths = [len(p.split()) for p in paragraphs]
            
            if para_lengths:
                # Check for uniform paragraph structure
                avg_para_length = statistics.mean(para_lengths)
                std_dev = statistics.stdev(para_lengths) if len(para_lengths) > 1 else 0
                
                if std_dev < avg_para_length * 0.3 and len(paragraphs) > 2:
                    score += 0.1
                    indicators.append("Uniform paragraph structure")
        
        # Check for logical flow indicators
        transition_words = ['first', 'second', 'third', 'finally', 'next', 'then', 'however', 'therefore']
        transition_count = sum(1 for word in transition_words if word in text.lower())
        
        if transition_count > len(paragraphs) * 0.5:  # Many transitions relative to paragraphs
            score += 0.05
            indicators.append(f"High transition word usage ({transition_count} instances)")
        
        return min(max(score, 0), 1), indicators
    
    def _calibrate_score(self, raw_score: float, text_length: int) -> float:
        """Calibrate score based on text length and other factors"""
        # Adjust confidence based on text length
        if text_length < 200:
            # Less confident for short texts
            return raw_score * 0.8 + 0.1
        elif text_length > 1000:
            # More confident for longer texts
            return raw_score * 1.1 - 0.05
        
        return raw_score

class EnhancedPlagiarismDetector:
    """Enhanced plagiarism detection with semantic analysis"""
    
    def __init__(self):
        self.suspicious_patterns = {
            'citation_indicators': [
                r'\(\d{4}\)',  # (2023)
                r'\w+\s+et\s+al\.?',  # Smith et al.
                r'\w+\s+\(\d{4}\)',  # Author (2023)
                r'according\s+to\s+\w+',  # according to Smith
                r'as\s+(?:stated|mentioned|noted)\s+by\s+\w+'
            ],
            'academic_phrases': [
                r'research\s+(?:shows|indicates|suggests|demonstrates)',
                r'studies\s+(?:show|indicate|suggest|demonstrate)',
                r'it\s+has\s+been\s+(?:established|proven|shown)',
                r'evidence\s+(?:suggests|indicates|shows)',
                r'findings\s+(?:suggest|indicate|show)'
            ],
            'copy_indicators': [
                r'see\s+(?:figure|table|appendix)\s+\d+',
                r'as\s+shown\s+in\s+(?:figure|table)\s+\d+',
                r'refer\s+to\s+(?:section|chapter)\s+\d+',
                r'\[\d+\]',  # Reference numbers [1]
                r'\(see\s+\w+\)'
            ]
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Enhanced plagiarism detection analysis"""
        if not text or len(text.strip()) < 100:
            return {
                'has_plagiarism': False,
                'confidence_score': 0.0,
                'plagiarism_probability': 0.0,
                'analysis_details': {'reason': 'Text too short for plagiarism analysis'},
                'indicators': []
            }
        
        try:
            # Multiple analysis layers
            pattern_score, pattern_indicators = self._analyze_patterns(text)
            style_score, style_indicators = self._analyze_writing_style(text)
            structure_score, structure_indicators = self._analyze_text_structure(text)
            semantic_score, semantic_indicators = self._analyze_semantic_consistency(text)
            
            # Weighted combination
            weights = {'patterns': 0.3, 'style': 0.3, 'structure': 0.2, 'semantic': 0.2}
            
            final_score = (
                pattern_score * weights['patterns'] +
                style_score * weights['style'] +
                structure_score * weights['structure'] +
                semantic_score * weights['semantic']
            )
            
            # Calibrate based on text characteristics
            calibrated_score = self._calibrate_plagiarism_score(final_score, text)
            
            has_plagiarism = calibrated_score > 0.4
            confidence = min(abs(calibrated_score - 0.3) * 1.5, 1.0)
            
            all_indicators = pattern_indicators + style_indicators + structure_indicators + semantic_indicators
            
            return {
                'has_plagiarism': has_plagiarism,
                'confidence_score': round(confidence, 3),
                'plagiarism_probability': round(calibrated_score, 3),
                'analysis_details': {
                    'pattern_score': round(pattern_score, 3),
                    'style_score': round(style_score, 3),
                    'structure_score': round(structure_score, 3),
                    'semantic_score': round(semantic_score, 3),
                    'text_length': len(text),
                    'sentence_count': len(re.split(r'[.!?]+', text))
                },
                'indicators': all_indicators[:10],
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Enhanced plagiarism detection error: {e}")
            return {
                'has_plagiarism': False,
                'confidence_score': 0.0,
                'plagiarism_probability': 0.0,
                'analysis_details': {'error': str(e)},
                'indicators': []
            }
    
    def _analyze_patterns(self, text: str) -> Tuple[float, List[str]]:
        """Analyze suspicious patterns that indicate plagiarism"""
        indicators = []
        total_score = 0
        
        for category, patterns in self.suspicious_patterns.items():
            category_matches = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                category_matches += matches
            
            if category_matches > 0:
                if category == 'citation_indicators' and category_matches > 3:
                    total_score += 0.3
                    indicators.append(f"Multiple citation patterns ({category_matches} found)")
                elif category == 'academic_phrases' and category_matches > 5:
                    total_score += 0.2
                    indicators.append(f"Excessive academic phrases ({category_matches} found)")
                elif category == 'copy_indicators' and category_matches > 2:
                    total_score += 0.4
                    indicators.append(f"Reference indicators suggest copying ({category_matches} found)")
        
        return min(total_score, 1.0), indicators
    
    def _analyze_writing_style(self, text: str) -> Tuple[float, List[str]]:
        """Analyze writing style consistency"""
        indicators = []
        score = 0
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 3]
        
        if len(sentences) < 5:
            return 0, indicators
        
        # Analyze sentence complexity variation
        complexities = []
        for sentence in sentences:
            # Simple complexity measure: subordinate clauses, commas, etc.
            complexity = (
                sentence.count(',') +
                sentence.count(';') +
                len(re.findall(r'\b(?:which|that|who|where|when)\b', sentence, re.IGNORECASE)) +
                len(re.findall(r'\b(?:although|because|since|while|whereas)\b', sentence, re.IGNORECASE))
            )
            complexities.append(complexity)
        
        if complexities:
            complexity_std = statistics.stdev(complexities) if len(complexities) > 1 else 0
            avg_complexity = statistics.mean(complexities)
            
            # Sudden changes in complexity might indicate different sources
            if complexity_std > avg_complexity * 1.5:
                score += 0.3
                indicators.append(f"Inconsistent sentence complexity (std: {complexity_std:.2f})")
        
        # Check for vocabulary level inconsistencies
        words = re.findall(r'\b\w+\b', text.lower())
        if words:
            # Simple vocabulary sophistication measure
            long_words = [w for w in words if len(w) > 7]
            sophistication_ratio = len(long_words) / len(words)
            
            # Analyze sophistication by paragraph
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            if len(paragraphs) > 2:
                para_sophistications = []
                for para in paragraphs:
                    para_words = re.findall(r'\b\w+\b', para.lower())
                    if para_words:
                        para_long_words = [w for w in para_words if len(w) > 7]
                        para_soph = len(para_long_words) / len(para_words)
                        para_sophistications.append(para_soph)
                
                if para_sophistications and len(para_sophistications) > 1:
                    soph_std = statistics.stdev(para_sophistications)
                    if soph_std > 0.1:  # Significant variation
                        score += 0.2
                        indicators.append(f"Inconsistent vocabulary sophistication across paragraphs")
        
        return min(score, 1.0), indicators
    
    def _analyze_text_structure(self, text: str) -> Tuple[float, List[str]]:
        """Analyze structural inconsistencies"""
        indicators = []
        score = 0
        
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        if len(paragraphs) > 2:
            # Check for abrupt topic changes
            # This is a simplified approach - in practice, you'd use more sophisticated NLP
            
            # Analyze paragraph length consistency
            para_lengths = [len(p.split()) for p in paragraphs]
            if para_lengths:
                length_std = statistics.stdev(para_lengths) if len(para_lengths) > 1 else 0
                avg_length = statistics.mean(para_lengths)
                
                # Very inconsistent paragraph lengths might indicate copying from different sources
                if length_std > avg_length * 0.8 and len(paragraphs) > 3:
                    score += 0.25
                    indicators.append(f"Highly inconsistent paragraph lengths")
        
        # Check for formatting inconsistencies
        lines = text.split('\n')
        empty_line_patterns = []
        for i, line in enumerate(lines[:-1]):
            if not line.strip() and lines[i+1].strip():
                empty_line_patterns.append(i)
        
        # Irregular spacing patterns might indicate copy-paste from different sources
        if len(empty_line_patterns) > len(paragraphs) * 1.5:
            score += 0.15
            indicators.append("Irregular spacing patterns detected")
        
        return min(score, 1.0), indicators
    
    def _analyze_semantic_consistency(self, text: str) -> Tuple[float, List[str]]:
        """Analyze semantic consistency and coherence"""
        indicators = []
        score = 0
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 5:
            return 0, indicators
        
        # Simple coherence check using word overlap between adjacent sentences
        coherence_scores = []
        for i in range(len(sentences) - 1):
            words1 = set(re.findall(r'\b\w+\b', sentences[i].lower()))
            words2 = set(re.findall(r'\b\w+\b', sentences[i+1].lower()))
            
            if words1 and words2:
                overlap = len(words1.intersection(words2))
                union = len(words1.union(words2))
                coherence = overlap / union if union > 0 else 0
                coherence_scores.append(coherence)
        
        if coherence_scores:
            avg_coherence = statistics.mean(coherence_scores)
            coherence_std = statistics.stdev(coherence_scores) if len(coherence_scores) > 1 else 0
            
            # Low average coherence might indicate text from different sources
            if avg_coherence < 0.1:
                score += 0.2
                indicators.append(f"Low semantic coherence between sentences ({avg_coherence:.3f})")
            
            # High variation in coherence might indicate mixed sources
            if coherence_std > 0.15:
                score += 0.15
                indicators.append(f"Inconsistent semantic coherence patterns")
        
        return min(score, 1.0), indicators
    
    def _calibrate_plagiarism_score(self, raw_score: float, text: str) -> float:
        """Calibrate plagiarism score based on text characteristics"""
        # Adjust based on text length
        text_length = len(text)
        if text_length < 300:
            # Less confident for short texts
            return raw_score * 0.7
        elif text_length > 2000:
            # More confident for longer texts
            return min(raw_score * 1.2, 1.0)
        
        return raw_score

# Global instances
enhanced_ai_detector = EnhancedAIDetector()
enhanced_plagiarism_detector = EnhancedPlagiarismDetector()

def analyze_content_enhanced(text: str, check_ai: bool = True, check_plagiarism: bool = True) -> Dict[str, Any]:
    """Enhanced content analysis using improved algorithms"""
    results = {
        'success': True,
        'text_length': len(text),
        'word_count': len(text.split()),
        'timestamp': datetime.utcnow().isoformat(),
        'enhanced_analysis': True
    }
    
    try:
        if check_ai:
            ai_result = enhanced_ai_detector.analyze_text(text)
            results['ai_detection'] = {
                'percentage': round(ai_result['ai_probability'] * 100, 1),
                'is_ai_generated': ai_result['is_ai_generated'],
                'confidence': ai_result['confidence_score'],
                'details': ai_result['analysis_details'],
                'indicators': ai_result['indicators']
            }
        
        if check_plagiarism:
            plag_result = enhanced_plagiarism_detector.analyze_text(text)
            results['plagiarism'] = {
                'percentage': round(plag_result['plagiarism_probability'] * 100, 1),
                'has_plagiarism': plag_result['has_plagiarism'],
                'confidence': plag_result['confidence_score'],
                'details': plag_result['analysis_details'],
                'indicators': plag_result['indicators']
            }
        
        return results
        
    except Exception as e:
        logger.error(f"Enhanced analysis error: {e}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }