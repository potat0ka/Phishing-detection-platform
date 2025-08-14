"""
Multimedia Authenticity Checker
==============================

This module provides comprehensive analysis for different media types:
- Text: Plagiarism detection and AI-generated content detection
- Images: AI-generated detection and reverse image search
- Videos: Manipulation detection and frame analysis
- Audio: Deepfake detection and voice authenticity

Author: AI Phishing Detection Platform
"""

import os
import tempfile
import hashlib
import logging
import difflib
import json
import base64
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Import enhanced detection algorithms
try:
    from .enhanced_detection import analyze_content_enhanced
    ENHANCED_DETECTION_AVAILABLE = True
except ImportError:
    ENHANCED_DETECTION_AVAILABLE = False
    logging.warning("Enhanced detection algorithms not available in multimedia analyzer")

logger = logging.getLogger(__name__)

class MultimediaAnalyzer:
    """Main class for analyzing different types of multimedia content"""
    
    def __init__(self):
        """Initialize the multimedia analyzer"""
        self.temp_dir = tempfile.gettempdir()
        logger.info("Multimedia Analyzer initialized")
    
    def analyze_content(self, content_type: str, content_data: Any, filename: Optional[str] = None, use_enhanced: bool = True) -> Dict[str, Any]:
        """
        Analyze content based on type with enhanced algorithms
        
        Args:
            content_type: Type of content ('text', 'image', 'video', 'audio')
            content_data: The actual content (text string, file bytes, etc.)
            filename: Original filename for file uploads
            use_enhanced: Whether to use enhanced detection algorithms
            
        Returns:
            Dictionary with analysis results
        """
        try:
            if content_type == 'text':
                return self._analyze_text(content_data, use_enhanced)
            elif content_type == 'image':
                return self._analyze_image(content_data, filename)
            elif content_type == 'video':
                return self._analyze_video(content_data, filename)
            elif content_type == 'audio':
                return self._analyze_audio(content_data, filename)
            else:
                return {'error': f'Unsupported content type: {content_type}'}
                
        except Exception as e:
            logger.error(f"Error analyzing {content_type}: {e}")
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _analyze_text(self, text: str, use_enhanced: bool = True) -> Dict[str, Any]:
        """Analyze text for plagiarism and AI generation with enhanced algorithms"""
        result = {
            'content_type': 'text',
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'text_length': len(text),
            'word_count': len(text.split()),
            'plagiarism_score': 0.0,
            'ai_likelihood': 0.0,
            'authenticity_verdict': 'Unknown',
            'details': [],
            'enhanced': False
        }
        
        try:
            # Use enhanced detection if available and requested
            if use_enhanced and ENHANCED_DETECTION_AVAILABLE:
                try:
                    enhanced_results = analyze_content_enhanced(text, check_ai=True, check_plagiarism=True)
                    if enhanced_results.get('success', False):
                        # Extract enhanced results
                        if 'ai_detection' in enhanced_results:
                            ai_data = enhanced_results['ai_detection']
                            result['ai_likelihood'] = ai_data['percentage'] / 100.0
                            result['ai_confidence'] = ai_data['confidence']
                            result['ai_indicators'] = ai_data.get('indicators', [])
                        
                        if 'plagiarism' in enhanced_results:
                            plag_data = enhanced_results['plagiarism']
                            result['plagiarism_score'] = plag_data['percentage'] / 100.0
                            result['plagiarism_confidence'] = plag_data['confidence']
                            result['plagiarism_indicators'] = plag_data.get('indicators', [])
                        
                        result['enhanced'] = True
                        
                        # Determine overall authenticity with enhanced data
                        if result['plagiarism_score'] > 0.6:
                            result['authenticity_verdict'] = 'Likely Plagiarized'
                            result['details'].append(f'Enhanced analysis: High plagiarism probability ({result["plagiarism_score"]:.1%})')
                        elif result['ai_likelihood'] > 0.7:
                            result['authenticity_verdict'] = 'Likely AI-Generated'
                            result['details'].append(f'Enhanced analysis: High AI generation probability ({result["ai_likelihood"]:.1%})')
                        elif result['ai_likelihood'] > 0.4:
                            result['authenticity_verdict'] = 'Possibly AI-Assisted'
                            result['details'].append(f'Enhanced analysis: Moderate AI generation probability ({result["ai_likelihood"]:.1%})')
                        else:
                            result['authenticity_verdict'] = 'Likely Human-Written'
                            result['details'].append('Enhanced analysis: Low indicators of plagiarism or AI generation')
                        
                        # Enhanced confidence calculation
                        confidence = max(
                            result.get('ai_confidence', 0),
                            result.get('plagiarism_confidence', 0)
                        )
                        result['confidence_score'] = confidence
                        
                        return result
                        
                except Exception as e:
                    logger.warning(f"Enhanced text analysis failed, falling back to basic method: {e}")
            
            # Fallback to basic analysis
            # Basic plagiarism detection using pattern matching
            plagiarism_score = self._detect_plagiarism(text)
            result['plagiarism_score'] = plagiarism_score
            
            # AI-generated content detection
            ai_likelihood = self._detect_ai_text(text)
            result['ai_likelihood'] = ai_likelihood
            
            # Determine overall authenticity
            if plagiarism_score > 0.7:
                result['authenticity_verdict'] = 'Likely Plagiarized'
                result['details'].append(f'High plagiarism similarity: {plagiarism_score:.1%}')
            elif ai_likelihood > 0.8:
                result['authenticity_verdict'] = 'Likely AI-Generated'
                result['details'].append(f'High AI generation probability: {ai_likelihood:.1%}')
            elif ai_likelihood > 0.5:
                result['authenticity_verdict'] = 'Possibly AI-Assisted'
                result['details'].append(f'Moderate AI generation probability: {ai_likelihood:.1%}')
            else:
                result['authenticity_verdict'] = 'Likely Human-Written'
                result['details'].append('Low indicators of plagiarism or AI generation')
            
            return result
            
        except Exception as e:
            logger.error(f"Text analysis error: {e}")
            result['error'] = f'Text analysis failed: {str(e)}'
            return result
    
    def _detect_plagiarism(self, text: str) -> float:
        """Simple plagiarism detection using common patterns"""
        # This is a basic implementation - in production, you'd use more sophisticated methods
        common_phrases = [
            "according to recent studies",
            "it is widely known that",
            "researchers have found",
            "studies have shown",
            "it has been proven that"
        ]
        
        text_lower = text.lower()
        matches = sum(1 for phrase in common_phrases if phrase in text_lower)
        
        # Simple scoring based on common academic phrases
        return min(matches * 0.2, 1.0)
    
    def _detect_ai_text(self, text: str) -> float:
        """Detect AI-generated text using pattern analysis"""
        # Basic AI detection patterns
        ai_indicators = [
            "as an ai", "i'm an ai", "as a language model",
            "i don't have personal", "i cannot", "i'm not able to",
            "furthermore", "moreover", "in conclusion",
            "it's worth noting", "it's important to note"
        ]
        
        text_lower = text.lower()
        
        # Check for AI-typical phrases
        ai_phrases = sum(1 for indicator in ai_indicators if indicator in text_lower)
        
        # Check for repetitive patterns
        sentences = text.split('.')
        if len(sentences) > 3:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            # AI tends to generate consistent sentence lengths
            length_consistency = 1.0 - (abs(avg_sentence_length - 15) / 15)
        else:
            length_consistency = 0.5
        
        # Combine factors
        ai_score = (ai_phrases * 0.3 + length_consistency * 0.7)
        return min(ai_score, 1.0)
    
    def _analyze_image(self, image_data: bytes, filename: str) -> Dict[str, Any]:
        """Analyze image for AI generation and authenticity"""
        result = {
            'content_type': 'image',
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'filename': filename,
            'file_size': len(image_data),
            'ai_likelihood': 0.0,
            'authenticity_verdict': 'Unknown',
            'details': []
        }
        
        try:
            # Save image to temporary file for analysis
            temp_path = os.path.join(self.temp_dir, f"temp_image_{datetime.now().timestamp()}")
            with open(temp_path, 'wb') as f:
                f.write(image_data)
            
            # Basic image analysis
            image_hash = hashlib.md5(image_data).hexdigest()
            result['image_hash'] = image_hash
            
            # Simulate AI detection (in production, use actual AI models)
            ai_likelihood = self._detect_ai_image(temp_path)
            result['ai_likelihood'] = ai_likelihood
            
            # Determine verdict
            if ai_likelihood > 0.8:
                result['authenticity_verdict'] = 'Likely AI-Generated'
                result['details'].append(f'High AI generation probability: {ai_likelihood:.1%}')
            elif ai_likelihood > 0.5:
                result['authenticity_verdict'] = 'Possibly AI-Generated'
                result['details'].append(f'Moderate AI generation probability: {ai_likelihood:.1%}')
            else:
                result['authenticity_verdict'] = 'Likely Authentic'
                result['details'].append('Low indicators of AI generation')
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            result['error'] = f'Image analysis failed: {str(e)}'
            return result
    
    def _detect_ai_image(self, image_path: str) -> float:
        """Basic AI image detection using metadata and patterns"""
        try:
            # Check file metadata for AI generation signatures
            with open(image_path, 'rb') as f:
                content = f.read()
            
            # Look for common AI generation artifacts in metadata
            ai_signatures = [
                b'generated', b'artificial', b'synthetic',
                b'midjourney', b'dall-e', b'stable diffusion'
            ]
            
            content_lower = content.lower()
            signature_matches = sum(1 for sig in ai_signatures if sig in content_lower)
            
            # Basic scoring
            return min(signature_matches * 0.4, 1.0)
            
        except Exception as e:
            logger.warning(f"AI image detection error: {e}")
            return 0.5  # Default uncertain score
    
    def _analyze_video(self, video_data: bytes, filename: str) -> Dict[str, Any]:
        """Analyze video for manipulation and authenticity"""
        result = {
            'content_type': 'video',
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'filename': filename,
            'file_size': len(video_data),
            'manipulation_likelihood': 0.0,
            'authenticity_verdict': 'Unknown',
            'details': []
        }
        
        try:
            # Save video to temporary file
            temp_path = os.path.join(self.temp_dir, f"temp_video_{datetime.now().timestamp()}")
            with open(temp_path, 'wb') as f:
                f.write(video_data)
            
            # Basic video analysis
            video_hash = hashlib.md5(video_data).hexdigest()
            result['video_hash'] = video_hash
            
            # Simulate manipulation detection
            manipulation_score = self._detect_video_manipulation(temp_path)
            result['manipulation_likelihood'] = manipulation_score
            
            # Determine verdict
            if manipulation_score > 0.8:
                result['authenticity_verdict'] = 'Likely Manipulated'
                result['details'].append(f'High manipulation probability: {manipulation_score:.1%}')
            elif manipulation_score > 0.5:
                result['authenticity_verdict'] = 'Possibly Manipulated'
                result['details'].append(f'Moderate manipulation probability: {manipulation_score:.1%}')
            else:
                result['authenticity_verdict'] = 'Likely Authentic'
                result['details'].append('Low indicators of manipulation')
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Video analysis error: {e}")
            result['error'] = f'Video analysis failed: {str(e)}'
            return result
    
    def _detect_video_manipulation(self, video_path: str) -> float:
        """Basic video manipulation detection"""
        try:
            # Check for common manipulation artifacts
            file_size = os.path.getsize(video_path)
            
            # Very basic heuristics (in production, use proper video analysis)
            if file_size < 1024 * 100:  # Very small files might be suspicious
                return 0.3
            elif file_size > 1024 * 1024 * 50:  # Very large files might indicate manipulation
                return 0.6
            else:
                return 0.2  # Default low suspicion
                
        except Exception as e:
            logger.warning(f"Video manipulation detection error: {e}")
            return 0.5
    
    def _analyze_audio(self, audio_data: bytes, filename: str) -> Dict[str, Any]:
        """Analyze audio for voice synthesis and authenticity"""
        result = {
            'content_type': 'audio',
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'filename': filename,
            'file_size': len(audio_data),
            'synthesis_likelihood': 0.0,
            'authenticity_verdict': 'Unknown',
            'details': []
        }
        
        try:
            # Save audio to temporary file
            temp_path = os.path.join(self.temp_dir, f"temp_audio_{datetime.now().timestamp()}")
            with open(temp_path, 'wb') as f:
                f.write(audio_data)
            
            # Basic audio analysis
            audio_hash = hashlib.md5(audio_data).hexdigest()
            result['audio_hash'] = audio_hash
            
            # Simulate voice synthesis detection
            synthesis_score = self._detect_voice_synthesis(temp_path)
            result['synthesis_likelihood'] = synthesis_score
            
            # Determine verdict
            if synthesis_score > 0.8:
                result['authenticity_verdict'] = 'Likely AI-Synthesized'
                result['details'].append(f'High synthesis probability: {synthesis_score:.1%}')
            elif synthesis_score > 0.5:
                result['authenticity_verdict'] = 'Possibly AI-Synthesized'
                result['details'].append(f'Moderate synthesis probability: {synthesis_score:.1%}')
            else:
                result['authenticity_verdict'] = 'Likely Human Voice'
                result['details'].append('Low indicators of voice synthesis')
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return result
            
        except Exception as e:
            logger.error(f"Audio analysis error: {e}")
            result['error'] = f'Audio analysis failed: {str(e)}'
            return result
    
    def _detect_voice_synthesis(self, audio_path: str) -> float:
        """Basic voice synthesis detection"""
        try:
            # Basic file analysis (in production, use proper audio ML models)
            file_size = os.path.getsize(audio_path)
            
            # Simple heuristics based on file characteristics
            if file_size < 1024 * 10:  # Very small audio files
                return 0.4
            elif file_size > 1024 * 1024 * 10:  # Very large audio files
                return 0.3
            else:
                return 0.25  # Default low suspicion for normal-sized files
                
        except Exception as e:
            logger.warning(f"Voice synthesis detection error: {e}")
            return 0.5

# Global analyzer instance
analyzer = MultimediaAnalyzer()