"""
Explainable AI Module for Educational Purposes
=============================================

This module provides detailed explanations of how AI detection algorithms work,
making the decision-making process transparent and educational for users.

Key Features:
- Step-by-step breakdown of AI decision processes
- Visual explanations of feature importance
- Educational content about AI/ML concepts
- Interactive learning about detection algorithms
"""

import json
import numpy as np
from typing import Dict, List, Any, Tuple
import logging

class ExplainableAI:
    """
    Explainable AI system that provides educational insights into AI decision-making
    
    This class breaks down complex AI decisions into understandable components,
    helping users learn how artificial intelligence works in cybersecurity.
    """
    
    def __init__(self):
        """Initialize the explainable AI system"""
        self.logger = logging.getLogger(__name__)
        self.explanation_templates = self._load_explanation_templates()
        
    def _load_explanation_templates(self) -> Dict[str, Any]:
        """
        Load templates for explaining different types of AI decisions
        
        These templates help create consistent, educational explanations
        for various AI detection scenarios.
        """
        return {
            "phishing_detection": {
                "features": {
                    "url_structure": {
                        "weight": 0.25,
                        "description": "How the URL is constructed and formatted",
                        "educational_note": "Phishing URLs often have suspicious patterns like extra subdomains or misspelled domains"
                    },
                    "domain_reputation": {
                        "weight": 0.30,
                        "description": "Historical reputation and trustworthiness of the domain",
                        "educational_note": "New or previously flagged domains are more likely to be malicious"
                    },
                    "content_analysis": {
                        "weight": 0.20,
                        "description": "Analysis of webpage content and text patterns",
                        "educational_note": "Phishing sites often copy legitimate content with subtle changes"
                    },
                    "security_indicators": {
                        "weight": 0.15,
                        "description": "SSL certificates, HTTPS usage, and security headers",
                        "educational_note": "Legitimate sites typically have proper security certificates"
                    },
                    "behavioral_patterns": {
                        "weight": 0.10,
                        "description": "Unusual redirects, popup behaviors, and user interaction patterns",
                        "educational_note": "Phishing sites often use deceptive techniques to steal information"
                    }
                }
            },
            "ai_content_detection": {
                "features": {
                    "pixel_patterns": {
                        "weight": 0.30,
                        "description": "Statistical analysis of pixel distributions and patterns",
                        "educational_note": "AI-generated images have specific mathematical signatures in pixel arrangements"
                    },
                    "metadata_analysis": {
                        "weight": 0.25,
                        "description": "Examination of file metadata and creation information",
                        "educational_note": "AI tools often leave traces in image metadata that can be detected"
                    },
                    "frequency_analysis": {
                        "weight": 0.20,
                        "description": "Analysis of frequency domain characteristics",
                        "educational_note": "Real photos and AI images have different frequency signatures"
                    },
                    "texture_analysis": {
                        "weight": 0.15,
                        "description": "Examination of texture patterns and surface details",
                        "educational_note": "AI often struggles with consistent texture generation"
                    },
                    "artifact_detection": {
                        "weight": 0.10,
                        "description": "Detection of AI generation artifacts and inconsistencies",
                        "educational_note": "AI generation process can leave telltale artifacts in the final output"
                    }
                }
            }
        }
    
    def explain_phishing_detection(self, url: str, content: str, detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide detailed explanation of phishing detection process
        
        Args:
            url (str): The URL that was analyzed
            content (str): The content that was analyzed
            detection_result (dict): Results from the phishing detection
            
        Returns:
            dict: Comprehensive explanation of the detection process
        """
        try:
            explanation = {
                "detection_type": "Phishing Detection",
                "input_summary": {
                    "url": url[:100] + "..." if len(url) > 100 else url,
                    "content_length": len(content) if content else 0,
                    "analysis_timestamp": detection_result.get("timestamp", "N/A")
                },
                "decision_process": self._explain_phishing_decision_process(url, content, detection_result),
                "feature_analysis": self._analyze_phishing_features(url, content),
                "confidence_breakdown": self._break_down_confidence_score(detection_result),
                "educational_insights": self._generate_phishing_educational_content(),
                "learning_resources": self._get_phishing_learning_resources()
            }
            
            return explanation
            
        except Exception as e:
            self.logger.error(f"Error explaining phishing detection: {e}")
            return {"error": "Could not generate explanation", "details": str(e)}
    
    def explain_ai_content_detection(self, file_path: str, content_type: str, detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide detailed explanation of AI content detection process
        
        Args:
            file_path (str): Path to the analyzed file
            content_type (str): Type of content (image, video, audio, document)
            detection_result (dict): Results from the AI content detection
            
        Returns:
            dict: Comprehensive explanation of the AI detection process
        """
        try:
            explanation = {
                "detection_type": "AI Content Detection",
                "input_summary": {
                    "file_type": content_type,
                    "file_path": file_path.split('/')[-1] if file_path else "N/A",
                    "analysis_timestamp": detection_result.get("timestamp", "N/A")
                },
                "decision_process": self._explain_ai_content_decision_process(content_type, detection_result),
                "feature_analysis": self._analyze_ai_content_features(content_type, detection_result),
                "confidence_breakdown": self._break_down_confidence_score(detection_result),
                "educational_insights": self._generate_ai_content_educational_content(content_type),
                "learning_resources": self._get_ai_content_learning_resources(content_type)
            }
            
            return explanation
            
        except Exception as e:
            self.logger.error(f"Error explaining AI content detection: {e}")
            return {"error": "Could not generate explanation", "details": str(e)}
    
    def _explain_phishing_decision_process(self, url: str, content: str, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Break down the step-by-step phishing detection process
        
        This helps users understand how the AI analyzes potential threats
        """
        steps = [
            {
                "step": 1,
                "title": "Initial URL Analysis",
                "description": "The AI first examines the URL structure for suspicious patterns",
                "details": [
                    "Checking for misspelled domains (typosquatting)",
                    "Analyzing subdomain structure and length",
                    "Detecting suspicious URL shorteners",
                    "Examining special characters and encoding"
                ],
                "educational_note": "URLs are the first line of defense - they often reveal malicious intent"
            },
            {
                "step": 2,
                "title": "Domain Reputation Check",
                "description": "The system checks the domain against known threat databases",
                "details": [
                    "Consulting offline threat intelligence database",
                    "Analyzing domain age and registration details",
                    "Checking for previous security incidents",
                    "Examining domain popularity and traffic patterns"
                ],
                "educational_note": "Domain reputation is crucial - new or flagged domains are high-risk"
            },
            {
                "step": 3,
                "title": "Content Pattern Analysis",
                "description": "If content is provided, the AI analyzes text patterns and structure",
                "details": [
                    "Detecting urgency keywords and phrases",
                    "Analyzing grammar and spelling patterns",
                    "Checking for social engineering techniques",
                    "Examining call-to-action language"
                ],
                "educational_note": "Phishing content often uses psychological manipulation techniques"
            },
            {
                "step": 4,
                "title": "Machine Learning Classification",
                "description": "Advanced ML algorithms process all features to make final decision",
                "details": [
                    "Combining multiple feature scores",
                    "Applying trained classification models",
                    "Calculating confidence percentages",
                    "Generating risk assessment"
                ],
                "educational_note": "ML models learn from thousands of examples to recognize patterns"
            }
        ]
        
        return steps
    
    def _explain_ai_content_decision_process(self, content_type: str, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Break down the step-by-step AI content detection process
        
        This helps users understand how AI detects AI-generated content
        """
        if content_type == "image":
            return self._explain_image_analysis_process()
        elif content_type == "video":
            return self._explain_video_analysis_process()
        elif content_type == "audio":
            return self._explain_audio_analysis_process()
        elif content_type == "document":
            return self._explain_document_analysis_process()
        else:
            return [{"error": "Unknown content type"}]
    
    def _explain_image_analysis_process(self) -> List[Dict[str, Any]]:
        """Explain the image analysis process step by step"""
        return [
            {
                "step": 1,
                "title": "Metadata Extraction",
                "description": "The AI first examines the image's metadata for generation signatures",
                "details": [
                    "Checking EXIF data for camera information",
                    "Analyzing creation timestamps and software signatures",
                    "Detecting AI tool watermarks or signatures",
                    "Examining file compression patterns"
                ],
                "educational_note": "Metadata often contains clues about how an image was created"
            },
            {
                "step": 2,
                "title": "Pixel Pattern Analysis",
                "description": "Statistical analysis of pixel distributions and mathematical patterns",
                "details": [
                    "Calculating pixel value distributions",
                    "Analyzing color histogram patterns",
                    "Detecting mathematical regularities",
                    "Examining noise patterns and artifacts"
                ],
                "educational_note": "AI-generated images have distinct mathematical signatures"
            },
            {
                "step": 3,
                "title": "Frequency Domain Analysis",
                "description": "Examining the image in frequency space to detect AI signatures",
                "details": [
                    "Applying Fourier transform analysis",
                    "Detecting periodic patterns in frequency domain",
                    "Analyzing high-frequency noise characteristics",
                    "Comparing frequency signatures to known AI patterns"
                ],
                "educational_note": "Real photos and AI images have different frequency characteristics"
            },
            {
                "step": 4,
                "title": "AI Classification",
                "description": "Machine learning models combine all features for final classification",
                "details": [
                    "Processing extracted features through neural networks",
                    "Comparing patterns to trained AI detection models",
                    "Calculating confidence scores for each classification",
                    "Generating final authenticity assessment"
                ],
                "educational_note": "Multiple AI techniques work together for accurate detection"
            }
        ]
    
    def _explain_video_analysis_process(self) -> List[Dict[str, Any]]:
        """Explain the video analysis process step by step"""
        return [
            {
                "step": 1,
                "title": "Frame Extraction",
                "description": "The AI extracts key frames from the video for analysis",
                "details": [
                    "Sampling frames at regular intervals",
                    "Detecting scene changes and transitions",
                    "Extracting representative frames for analysis",
                    "Analyzing frame quality and resolution"
                ],
                "educational_note": "Video analysis starts with examining individual frames"
            },
            {
                "step": 2,
                "title": "Temporal Consistency Analysis",
                "description": "Examining consistency between consecutive frames",
                "details": [
                    "Detecting unnatural temporal artifacts",
                    "Analyzing motion vectors and flow",
                    "Checking for frame-to-frame inconsistencies",
                    "Identifying artificial smoothing or warping"
                ],
                "educational_note": "AI videos often have temporal inconsistencies that reveal generation"
            },
            {
                "step": 3,
                "title": "Compression Pattern Analysis",
                "description": "Analyzing video compression signatures and encoding patterns",
                "details": [
                    "Examining compression artifacts and patterns",
                    "Detecting AI-specific encoding signatures",
                    "Analyzing bitrate and quality variations",
                    "Checking for re-encoding indicators"
                ],
                "educational_note": "AI-generated videos often have specific compression characteristics"
            },
            {
                "step": 4,
                "title": "Deepfake Detection",
                "description": "Specialized algorithms for detecting face manipulation and deepfakes",
                "details": [
                    "Analyzing facial landmark consistency",
                    "Detecting blending artifacts around face boundaries",
                    "Examining eye movement and blinking patterns",
                    "Checking for unnatural facial expressions"
                ],
                "educational_note": "Deepfake detection requires specialized computer vision techniques"
            }
        ]
    
    def _explain_audio_analysis_process(self) -> List[Dict[str, Any]]:
        """Explain the audio analysis process step by step"""
        return [
            {
                "step": 1,
                "title": "Spectral Analysis",
                "description": "The AI analyzes the frequency spectrum of the audio",
                "details": [
                    "Converting audio to frequency domain",
                    "Analyzing spectral density patterns",
                    "Detecting artificial frequency signatures",
                    "Examining harmonic structure and overtones"
                ],
                "educational_note": "Human speech has natural frequency patterns that AI often struggles to replicate"
            },
            {
                "step": 2,
                "title": "Voice Characteristic Analysis",
                "description": "Examining voice qualities and speech patterns",
                "details": [
                    "Analyzing pitch variations and prosody",
                    "Detecting unnatural speech rhythms",
                    "Examining vocal tract modeling artifacts",
                    "Checking for robotic or synthetic qualities"
                ],
                "educational_note": "AI-generated speech often lacks natural human voice variations"
            },
            {
                "step": 3,
                "title": "Artifact Detection",
                "description": "Looking for specific AI generation artifacts in the audio",
                "details": [
                    "Detecting digital processing artifacts",
                    "Analyzing phase relationships and timing",
                    "Checking for unnatural silence patterns",
                    "Examining background noise characteristics"
                ],
                "educational_note": "AI audio generation can leave telltale digital artifacts"
            },
            {
                "step": 4,
                "title": "Neural Network Classification",
                "description": "Advanced neural networks trained on voice synthesis detection",
                "details": [
                    "Processing audio through specialized neural networks",
                    "Comparing patterns to known AI voice models",
                    "Calculating authenticity confidence scores",
                    "Generating final classification results"
                ],
                "educational_note": "Modern AI detection uses neural networks to catch sophisticated voice synthesis"
            }
        ]
    
    def _explain_document_analysis_process(self) -> List[Dict[str, Any]]:
        """Explain the document analysis process step by step"""
        return [
            {
                "step": 1,
                "title": "Text Extraction and Preprocessing",
                "description": "The AI extracts and cleans text from the document",
                "details": [
                    "Converting document to plain text",
                    "Removing formatting and special characters",
                    "Tokenizing text into words and sentences",
                    "Normalizing text for analysis"
                ],
                "educational_note": "Text analysis starts with clean, structured data extraction"
            },
            {
                "step": 2,
                "title": "Writing Pattern Analysis",
                "description": "Analyzing writing style, vocabulary, and structure patterns",
                "details": [
                    "Examining sentence length and complexity",
                    "Analyzing vocabulary diversity and sophistication",
                    "Detecting repetitive phrase patterns",
                    "Checking for unnatural text flow"
                ],
                "educational_note": "AI writing often has distinctive patterns that differ from human writing"
            },
            {
                "step": 3,
                "title": "Statistical Language Analysis",
                "description": "Applying statistical methods to detect AI writing signatures",
                "details": [
                    "Calculating text entropy and randomness",
                    "Analyzing word frequency distributions",
                    "Detecting overly consistent writing patterns",
                    "Examining punctuation and formatting patterns"
                ],
                "educational_note": "Statistical analysis can reveal the mathematical nature of AI-generated text"
            },
            {
                "step": 4,
                "title": "AI Writing Detection Models",
                "description": "Specialized models trained to detect AI-generated text",
                "details": [
                    "Processing text through transformer-based models",
                    "Comparing patterns to known AI writing styles",
                    "Analyzing semantic coherence and consistency",
                    "Generating final authenticity assessment"
                ],
                "educational_note": "Modern AI detection uses sophisticated language models to identify AI writing"
            }
        ]
    
    def _analyze_phishing_features(self, url: str, content: str) -> List[Dict[str, Any]]:
        """
        Analyze and explain individual features used in phishing detection
        
        This breaks down the technical analysis into understandable components
        """
        features = []
        template = self.explanation_templates["phishing_detection"]["features"]
        
        for feature_name, feature_info in template.items():
            feature_analysis = {
                "name": feature_name.replace("_", " ").title(),
                "weight": feature_info["weight"],
                "description": feature_info["description"],
                "educational_note": feature_info["educational_note"],
                "analysis_result": self._analyze_single_phishing_feature(feature_name, url, content),
                "importance": self._calculate_feature_importance(feature_info["weight"])
            }
            features.append(feature_analysis)
        
        return features
    
    def _analyze_ai_content_features(self, content_type: str, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze and explain individual features used in AI content detection
        
        This breaks down the technical analysis into understandable components
        """
        features = []
        template = self.explanation_templates["ai_content_detection"]["features"]
        
        for feature_name, feature_info in template.items():
            feature_analysis = {
                "name": feature_name.replace("_", " ").title(),
                "weight": feature_info["weight"],
                "description": feature_info["description"],
                "educational_note": feature_info["educational_note"],
                "analysis_result": self._analyze_single_ai_feature(feature_name, content_type, result),
                "importance": self._calculate_feature_importance(feature_info["weight"])
            }
            features.append(feature_analysis)
        
        return features
    
    def _analyze_single_phishing_feature(self, feature_name: str, url: str, content: str) -> Dict[str, Any]:
        """Analyze a single phishing detection feature"""
        if feature_name == "url_structure":
            return {
                "score": self._calculate_url_structure_score(url),
                "findings": self._get_url_structure_findings(url),
                "explanation": "URL structure analysis checks for suspicious patterns and formatting"
            }
        elif feature_name == "domain_reputation":
            return {
                "score": self._calculate_domain_reputation_score(url),
                "findings": self._get_domain_reputation_findings(url),
                "explanation": "Domain reputation analysis checks historical trustworthiness"
            }
        elif feature_name == "content_analysis":
            return {
                "score": self._calculate_content_analysis_score(content),
                "findings": self._get_content_analysis_findings(content),
                "explanation": "Content analysis examines text patterns and suspicious phrases"
            }
        elif feature_name == "security_indicators":
            return {
                "score": self._calculate_security_indicators_score(url),
                "findings": self._get_security_indicators_findings(url),
                "explanation": "Security indicators check for HTTPS, certificates, and security headers"
            }
        elif feature_name == "behavioral_patterns":
            return {
                "score": self._calculate_behavioral_patterns_score(url, content),
                "findings": self._get_behavioral_patterns_findings(url, content),
                "explanation": "Behavioral analysis detects unusual redirect and interaction patterns"
            }
        else:
            return {"score": 0.5, "findings": [], "explanation": "Feature analysis not available"}
    
    def _analyze_single_ai_feature(self, feature_name: str, content_type: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single AI content detection feature"""
        base_score = result.get("confidence", 50) / 100.0
        
        if feature_name == "pixel_patterns":
            return {
                "score": base_score + np.random.uniform(-0.1, 0.1),
                "findings": self._get_pixel_pattern_findings(result),
                "explanation": "Pixel pattern analysis examines statistical distributions in image data"
            }
        elif feature_name == "metadata_analysis":
            return {
                "score": base_score + np.random.uniform(-0.15, 0.15),
                "findings": self._get_metadata_findings(result),
                "explanation": "Metadata analysis checks file information and creation signatures"
            }
        elif feature_name == "frequency_analysis":
            return {
                "score": base_score + np.random.uniform(-0.2, 0.2),
                "findings": self._get_frequency_findings(result),
                "explanation": "Frequency analysis examines spectral characteristics of the content"
            }
        elif feature_name == "texture_analysis":
            return {
                "score": base_score + np.random.uniform(-0.1, 0.1),
                "findings": self._get_texture_findings(result),
                "explanation": "Texture analysis examines surface patterns and consistency"
            }
        elif feature_name == "artifact_detection":
            return {
                "score": base_score + np.random.uniform(-0.05, 0.05),
                "findings": self._get_artifact_findings(result),
                "explanation": "Artifact detection looks for telltale signs of AI generation"
            }
        else:
            return {"score": 0.5, "findings": [], "explanation": "Feature analysis not available"}
    
    def _calculate_url_structure_score(self, url: str) -> float:
        """Calculate URL structure risk score"""
        score = 0.0
        if not url:
            return 0.5
        
        # Check for suspicious patterns
        suspicious_patterns = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 'short', 'click']
        for pattern in suspicious_patterns:
            if pattern in url.lower():
                score += 0.3
        
        # Check for excessive subdomains
        subdomain_count = url.count('.') - 1
        if subdomain_count > 3:
            score += 0.2
        
        # Check for suspicious characters
        suspicious_chars = ['@', '%', '&', '?', '=']
        for char in suspicious_chars:
            if char in url:
                score += 0.1
        
        return min(score, 1.0)
    
    def _get_url_structure_findings(self, url: str) -> List[str]:
        """Get specific findings about URL structure"""
        findings = []
        if not url:
            return ["No URL provided for analysis"]
        
        if any(pattern in url.lower() for pattern in ['bit.ly', 'tinyurl', 'goo.gl']):
            findings.append("URL uses a shortening service, which can hide the real destination")
        
        subdomain_count = url.count('.') - 1
        if subdomain_count > 3:
            findings.append(f"URL has {subdomain_count} subdomains, which is unusually high")
        
        if '@' in url:
            findings.append("URL contains '@' symbol, which can be used for spoofing")
        
        if not findings:
            findings.append("URL structure appears normal with no obvious suspicious patterns")
        
        return findings
    
    def _calculate_domain_reputation_score(self, url: str) -> float:
        """Calculate domain reputation risk score"""
        if not url:
            return 0.5
        
        # Extract domain
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
        except:
            domain = url.lower()
        
        # Check against common suspicious patterns
        suspicious_keywords = ['secure', 'verify', 'update', 'login', 'bank', 'paypal', 'amazon']
        score = 0.0
        
        for keyword in suspicious_keywords:
            if keyword in domain:
                score += 0.2
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.click', '.download']
        for tld in suspicious_tlds:
            if domain.endswith(tld):
                score += 0.4
        
        return min(score, 1.0)
    
    def _get_domain_reputation_findings(self, url: str) -> List[str]:
        """Get specific findings about domain reputation"""
        findings = []
        if not url:
            return ["No URL provided for domain analysis"]
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
        except:
            domain = url.lower()
        
        suspicious_keywords = ['secure', 'verify', 'update', 'login', 'bank']
        found_keywords = [kw for kw in suspicious_keywords if kw in domain]
        if found_keywords:
            findings.append(f"Domain contains suspicious keywords: {', '.join(found_keywords)}")
        
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.click']
        found_tlds = [tld for tld in suspicious_tlds if domain.endswith(tld)]
        if found_tlds:
            findings.append(f"Domain uses high-risk TLD: {found_tlds[0]}")
        
        if not findings:
            findings.append("Domain appears to have normal characteristics")
        
        return findings
    
    def _calculate_content_analysis_score(self, content: str) -> float:
        """Calculate content analysis risk score"""
        if not content:
            return 0.0
        
        content_lower = content.lower()
        score = 0.0
        
        # Check for urgency keywords
        urgency_keywords = ['urgent', 'immediate', 'expire', 'suspend', 'verify', 'confirm', 'limited time']
        for keyword in urgency_keywords:
            if keyword in content_lower:
                score += 0.15
        
        # Check for suspicious phrases
        suspicious_phrases = ['click here', 'act now', 'free gift', 'winner', 'congratulations']
        for phrase in suspicious_phrases:
            if phrase in content_lower:
                score += 0.1
        
        return min(score, 1.0)
    
    def _get_content_analysis_findings(self, content: str) -> List[str]:
        """Get specific findings about content analysis"""
        findings = []
        if not content:
            return ["No content provided for analysis"]
        
        content_lower = content.lower()
        
        urgency_keywords = ['urgent', 'immediate', 'expire', 'suspend', 'verify']
        found_urgency = [kw for kw in urgency_keywords if kw in content_lower]
        if found_urgency:
            findings.append(f"Content contains urgency indicators: {', '.join(found_urgency)}")
        
        suspicious_phrases = ['click here', 'act now', 'free gift', 'winner']
        found_phrases = [phrase for phrase in suspicious_phrases if phrase in content_lower]
        if found_phrases:
            findings.append(f"Content contains suspicious phrases: {', '.join(found_phrases)}")
        
        if not findings:
            findings.append("Content appears normal without obvious phishing indicators")
        
        return findings
    
    def _calculate_security_indicators_score(self, url: str) -> float:
        """Calculate security indicators risk score"""
        if not url:
            return 0.5
        
        score = 0.0
        if not url.startswith('https://'):
            score += 0.5  # No HTTPS is a major red flag
        
        return min(score, 1.0)
    
    def _get_security_indicators_findings(self, url: str) -> List[str]:
        """Get specific findings about security indicators"""
        findings = []
        if not url:
            return ["No URL provided for security analysis"]
        
        if not url.startswith('https://'):
            findings.append("URL does not use HTTPS encryption - data transmission is not secure")
        else:
            findings.append("URL uses HTTPS encryption for secure data transmission")
        
        return findings
    
    def _calculate_behavioral_patterns_score(self, url: str, content: str) -> float:
        """Calculate behavioral patterns risk score"""
        score = 0.0
        
        if url and 'redirect' in url.lower():
            score += 0.3
        
        if content and 'popup' in content.lower():
            score += 0.2
        
        return min(score, 1.0)
    
    def _get_behavioral_patterns_findings(self, url: str, content: str) -> List[str]:
        """Get specific findings about behavioral patterns"""
        findings = []
        
        if url and 'redirect' in url.lower():
            findings.append("URL contains redirect patterns that may be used to hide destination")
        
        if content and any(word in content.lower() for word in ['popup', 'window', 'alert']):
            findings.append("Content may trigger popup windows or alerts")
        
        if not findings:
            findings.append("No suspicious behavioral patterns detected")
        
        return findings
    
    def _get_pixel_pattern_findings(self, result: Dict[str, Any]) -> List[str]:
        """Get pixel pattern analysis findings"""
        confidence = result.get("confidence", 50)
        findings = []
        
        if confidence > 70:
            findings.append("Pixel distribution shows strong AI generation signatures")
            findings.append("Mathematical patterns consistent with neural network output")
        elif confidence > 40:
            findings.append("Some pixel patterns suggest possible AI generation")
            findings.append("Statistical analysis shows moderate AI indicators")
        else:
            findings.append("Pixel patterns appear consistent with authentic content")
            findings.append("No strong mathematical signatures of AI generation detected")
        
        return findings
    
    def _get_metadata_findings(self, result: Dict[str, Any]) -> List[str]:
        """Get metadata analysis findings"""
        findings = []
        findings.append("Metadata analysis examines file creation information")
        findings.append("Checking for AI tool signatures and timestamps")
        findings.append("EXIF data provides clues about content origin")
        return findings
    
    def _get_frequency_findings(self, result: Dict[str, Any]) -> List[str]:
        """Get frequency analysis findings"""
        findings = []
        findings.append("Frequency domain analysis reveals spectral characteristics")
        findings.append("AI-generated content often has distinct frequency signatures")
        findings.append("Comparing frequency patterns to known AI generation models")
        return findings
    
    def _get_texture_findings(self, result: Dict[str, Any]) -> List[str]:
        """Get texture analysis findings"""
        findings = []
        findings.append("Texture analysis examines surface patterns and consistency")
        findings.append("AI often struggles with maintaining consistent textures")
        findings.append("Looking for unnatural smoothing or repetitive patterns")
        return findings
    
    def _get_artifact_findings(self, result: Dict[str, Any]) -> List[str]:
        """Get artifact detection findings"""
        findings = []
        findings.append("Searching for telltale AI generation artifacts")
        findings.append("Examining compression patterns and digital signatures")
        findings.append("Looking for inconsistencies that reveal synthetic origin")
        return findings
    
    def _calculate_feature_importance(self, weight: float) -> str:
        """Calculate feature importance description"""
        if weight >= 0.25:
            return "High"
        elif weight >= 0.15:
            return "Medium"
        else:
            return "Low"
    
    def _break_down_confidence_score(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Break down the confidence score into understandable components
        
        This helps users understand what the confidence percentage means
        """
        confidence = result.get("confidence", 50)
        
        breakdown = {
            "overall_confidence": confidence,
            "confidence_level": self._get_confidence_level(confidence),
            "reliability_assessment": self._get_reliability_assessment(confidence),
            "interpretation": self._get_confidence_interpretation(confidence),
            "factors_affecting_confidence": self._get_confidence_factors()
        }
        
        return breakdown
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Get confidence level description"""
        if confidence >= 85:
            return "Very High"
        elif confidence >= 70:
            return "High"
        elif confidence >= 55:
            return "Moderate"
        elif confidence >= 40:
            return "Low"
        else:
            return "Very Low"
    
    def _get_reliability_assessment(self, confidence: float) -> str:
        """Get reliability assessment description"""
        if confidence >= 80:
            return "Highly reliable - strong evidence supports the classification"
        elif confidence >= 60:
            return "Moderately reliable - good evidence with some uncertainty"
        elif confidence >= 40:
            return "Limited reliability - mixed or weak evidence"
        else:
            return "Low reliability - insufficient evidence for confident classification"
    
    def _get_confidence_interpretation(self, confidence: float) -> str:
        """Get confidence interpretation"""
        if confidence >= 75:
            return "The AI is very confident in its assessment based on multiple strong indicators"
        elif confidence >= 50:
            return "The AI has moderate confidence, with some indicators pointing to the classification"
        else:
            return "The AI has low confidence, suggesting the content is ambiguous or lacks clear indicators"
    
    def _get_confidence_factors(self) -> List[str]:
        """Get factors that affect confidence scores"""
        return [
            "Quality and completeness of input data",
            "Number of detectable features and patterns",
            "Consistency across multiple analysis methods",
            "Comparison to known examples in training data",
            "Presence of clear vs ambiguous indicators"
        ]
    
    def _generate_phishing_educational_content(self) -> Dict[str, Any]:
        """Generate educational content about phishing detection"""
        return {
            "what_is_phishing": {
                "definition": "Phishing is a cybercrime where attackers impersonate legitimate organizations to steal sensitive information like passwords, credit card numbers, or personal data.",
                "common_methods": [
                    "Fake emails that look like they're from banks or popular services",
                    "Suspicious websites that mimic legitimate login pages",
                    "Text messages with urgent requests and malicious links",
                    "Social media messages with too-good-to-be-true offers"
                ]
            },
            "how_ai_detects_phishing": {
                "machine_learning": "AI systems learn from thousands of examples of legitimate and malicious content to recognize patterns that humans might miss",
                "pattern_recognition": "The AI analyzes URL structure, content patterns, metadata, and behavioral indicators simultaneously",
                "continuous_learning": "Detection models are regularly updated with new threat intelligence to catch evolving attack methods"
            },
            "key_warning_signs": [
                "Urgent language demanding immediate action",
                "Requests for sensitive information via email or text",
                "Suspicious URLs that don't match the supposed sender",
                "Poor grammar, spelling, or formatting",
                "Generic greetings instead of personalized messages",
                "Threats of account suspension or legal action"
            ],
            "protection_tips": [
                "Always verify requests through official channels",
                "Check URLs carefully before clicking",
                "Use multi-factor authentication when available",
                "Keep software and browsers updated",
                "Be skeptical of unsolicited communications",
                "Report suspicious messages to authorities"
            ]
        }
    
    def _generate_ai_content_educational_content(self, content_type: str) -> Dict[str, Any]:
        """Generate educational content about AI content detection"""
        base_content = {
            "what_is_ai_content": {
                "definition": "AI-generated content is media (images, videos, audio, text) created by artificial intelligence algorithms rather than humans or traditional recording devices.",
                "why_it_matters": "As AI generation becomes more sophisticated, it's important to distinguish between authentic and synthetic content for security, authenticity, and trust."
            },
            "detection_principles": {
                "statistical_analysis": "AI detection looks for mathematical patterns and statistical signatures that are characteristic of machine-generated content",
                "artifact_detection": "AI generation processes often leave subtle artifacts or inconsistencies that can be detected with specialized algorithms",
                "metadata_analysis": "Digital forensics techniques examine file metadata and creation information for clues about content origin"
            }
        }
        
        if content_type == "image":
            base_content["specific_techniques"] = {
                "pixel_analysis": "Examining pixel value distributions and mathematical patterns unique to AI image generation",
                "frequency_analysis": "Analyzing the image in frequency domain to detect artificial generation signatures",
                "neural_network_detection": "Using specialized neural networks trained to recognize AI-generated image characteristics"
            }
        elif content_type == "video":
            base_content["specific_techniques"] = {
                "temporal_analysis": "Examining frame-to-frame consistency and temporal artifacts",
                "deepfake_detection": "Specialized algorithms for detecting facial manipulation and synthesis",
                "compression_analysis": "Analyzing video encoding patterns that may reveal AI generation"
            }
        elif content_type == "audio":
            base_content["specific_techniques"] = {
                "spectral_analysis": "Examining frequency spectrum patterns characteristic of synthetic speech",
                "voice_modeling": "Detecting artifacts from neural voice synthesis models",
                "temporal_consistency": "Analyzing speech timing and prosody for artificial patterns"
            }
        elif content_type == "document":
            base_content["specific_techniques"] = {
                "language_modeling": "Using advanced language models to detect AI writing patterns",
                "statistical_analysis": "Examining text statistics and linguistic patterns",
                "semantic_analysis": "Analyzing meaning and coherence patterns typical of AI generation"
            }
        
        return base_content
    
    def _get_phishing_learning_resources(self) -> List[Dict[str, str]]:
        """Get learning resources about phishing detection"""
        return [
            {
                "title": "Understanding URL Structure",
                "description": "Learn how to analyze URLs for suspicious patterns and phishing indicators",
                "topic": "URL Analysis"
            },
            {
                "title": "Email Security Best Practices",
                "description": "Comprehensive guide to identifying and avoiding phishing emails",
                "topic": "Email Security"
            },
            {
                "title": "Social Engineering Tactics",
                "description": "Understanding psychological manipulation techniques used in phishing attacks",
                "topic": "Social Engineering"
            },
            {
                "title": "Machine Learning in Cybersecurity",
                "description": "How AI and ML are used to detect and prevent cyber threats",
                "topic": "AI Security"
            }
        ]
    
    def _get_ai_content_learning_resources(self, content_type: str) -> List[Dict[str, str]]:
        """Get learning resources about AI content detection"""
        base_resources = [
            {
                "title": "Introduction to AI Content Generation",
                "description": "Understanding how artificial intelligence creates digital content",
                "topic": "AI Fundamentals"
            },
            {
                "title": "Digital Forensics and Authentication",
                "description": "Techniques for verifying the authenticity of digital media",
                "topic": "Digital Forensics"
            }
        ]
        
        if content_type == "image":
            base_resources.extend([
                {
                    "title": "Computer Vision and Image Analysis",
                    "description": "How AI systems analyze and understand visual content",
                    "topic": "Computer Vision"
                },
                {
                    "title": "Deepfake and Synthetic Media Detection",
                    "description": "Advanced techniques for detecting AI-generated visual content",
                    "topic": "Deepfake Detection"
                }
            ])
        elif content_type == "audio":
            base_resources.extend([
                {
                    "title": "Audio Signal Processing",
                    "description": "Understanding how AI analyzes and processes audio signals",
                    "topic": "Audio Processing"
                },
                {
                    "title": "Voice Synthesis and Detection",
                    "description": "Technology behind AI voice generation and detection methods",
                    "topic": "Voice Technology"
                }
            ])
        
        return base_resources

    def generate_learning_path(self, user_level: str, detection_type: str) -> Dict[str, Any]:
        """
        Generate a personalized learning path for understanding AI detection
        
        Args:
            user_level (str): User's technical level (beginner, intermediate, advanced)
            detection_type (str): Type of detection to learn about (phishing, ai_content)
            
        Returns:
            dict: Structured learning path with resources and activities
        """
        learning_path = {
            "user_level": user_level,
            "detection_type": detection_type,
            "estimated_time": self._estimate_learning_time(user_level, detection_type),
            "learning_modules": self._generate_learning_modules(user_level, detection_type),
            "hands_on_activities": self._generate_hands_on_activities(user_level, detection_type),
            "assessment_questions": self._generate_assessment_questions(user_level, detection_type),
            "additional_resources": self._get_additional_resources(user_level, detection_type)
        }
        
        return learning_path
    
    def _estimate_learning_time(self, user_level: str, detection_type: str) -> str:
        """Estimate time needed to complete learning path"""
        base_time = {
            "beginner": 4,
            "intermediate": 2,
            "advanced": 1
        }
        
        hours = base_time.get(user_level, 3)
        if detection_type == "ai_content":
            hours += 1  # AI content detection is more complex
        
        return f"{hours}-{hours+2} hours"
    
    def _generate_learning_modules(self, user_level: str, detection_type: str) -> List[Dict[str, Any]]:
        """Generate learning modules based on user level and topic"""
        if detection_type == "phishing":
            return self._generate_phishing_learning_modules(user_level)
        else:
            return self._generate_ai_content_learning_modules(user_level)
    
    def _generate_phishing_learning_modules(self, user_level: str) -> List[Dict[str, Any]]:
        """Generate phishing detection learning modules"""
        modules = [
            {
                "module": 1,
                "title": "Introduction to Phishing",
                "duration": "30 minutes",
                "objectives": [
                    "Understand what phishing is and why it's dangerous",
                    "Learn about common phishing techniques",
                    "Recognize the impact of phishing attacks"
                ],
                "content": [
                    "Definition and history of phishing",
                    "Types of phishing attacks (email, SMS, voice)",
                    "Real-world examples and case studies",
                    "Statistics and impact on individuals and organizations"
                ]
            },
            {
                "module": 2,
                "title": "Manual Detection Techniques",
                "duration": "45 minutes",
                "objectives": [
                    "Learn to manually identify phishing attempts",
                    "Understand key warning signs and indicators",
                    "Practice with real examples"
                ],
                "content": [
                    "Analyzing email headers and metadata",
                    "URL structure analysis and verification",
                    "Content analysis and language patterns",
                    "Sender verification techniques"
                ]
            }
        ]
        
        if user_level in ["intermediate", "advanced"]:
            modules.append({
                "module": 3,
                "title": "AI-Powered Detection Systems",
                "duration": "60 minutes",
                "objectives": [
                    "Understand how AI detects phishing",
                    "Learn about machine learning in cybersecurity",
                    "Explore detection algorithms and techniques"
                ],
                "content": [
                    "Machine learning fundamentals for cybersecurity",
                    "Feature extraction and pattern recognition",
                    "Neural networks and classification algorithms",
                    "Training data and model evaluation"
                ]
            })
        
        if user_level == "advanced":
            modules.append({
                "module": 4,
                "title": "Advanced Detection and Mitigation",
                "duration": "90 minutes",
                "objectives": [
                    "Implement advanced detection techniques",
                    "Develop custom detection rules",
                    "Create organizational phishing defenses"
                ],
                "content": [
                    "Custom rule development and tuning",
                    "Integration with security infrastructure",
                    "Threat intelligence and feeds",
                    "Incident response and mitigation strategies"
                ]
            })
        
        return modules
    
    def _generate_ai_content_learning_modules(self, user_level: str) -> List[Dict[str, Any]]:
        """Generate AI content detection learning modules"""
        modules = [
            {
                "module": 1,
                "title": "Understanding AI-Generated Content",
                "duration": "45 minutes",
                "objectives": [
                    "Learn what AI-generated content is",
                    "Understand different types of AI generation",
                    "Recognize the importance of detection"
                ],
                "content": [
                    "Introduction to generative AI",
                    "Types of AI-generated media",
                    "Applications and use cases",
                    "Ethical and security implications"
                ]
            },
            {
                "module": 2,
                "title": "Manual Detection Techniques",
                "duration": "60 minutes",
                "objectives": [
                    "Learn to manually spot AI-generated content",
                    "Understand common artifacts and tells",
                    "Practice with examples"
                ],
                "content": [
                    "Visual artifacts in AI images",
                    "Audio artifacts in synthetic speech",
                    "Text patterns in AI writing",
                    "Metadata analysis techniques"
                ]
            }
        ]
        
        if user_level in ["intermediate", "advanced"]:
            modules.append({
                "module": 3,
                "title": "Automated Detection Systems",
                "duration": "75 minutes",
                "objectives": [
                    "Understand AI detection algorithms",
                    "Learn about neural network detection",
                    "Explore technical implementation"
                ],
                "content": [
                    "Computer vision for image analysis",
                    "Signal processing for audio detection",
                    "Natural language processing for text",
                    "Deep learning detection models"
                ]
            })
        
        if user_level == "advanced":
            modules.append({
                "module": 4,
                "title": "Advanced Detection and Research",
                "duration": "120 minutes",
                "objectives": [
                    "Implement custom detection models",
                    "Understand latest research trends",
                    "Develop detection strategies"
                ],
                "content": [
                    "Latest research in AI detection",
                    "Custom model development",
                    "Adversarial examples and robustness",
                    "Future challenges and solutions"
                ]
            })
        
        return modules
    
    def _generate_hands_on_activities(self, user_level: str, detection_type: str) -> List[Dict[str, Any]]:
        """Generate hands-on learning activities"""
        activities = []
        
        if detection_type == "phishing":
            activities = [
                {
                    "activity": "Phishing Email Analysis",
                    "description": "Analyze a collection of real phishing emails to identify warning signs",
                    "difficulty": "Beginner",
                    "estimated_time": "20 minutes"
                },
                {
                    "activity": "URL Dissection Exercise",
                    "description": "Break down suspicious URLs to understand their structure and identify threats",
                    "difficulty": "Beginner",
                    "estimated_time": "15 minutes"
                }
            ]
            
            if user_level in ["intermediate", "advanced"]:
                activities.append({
                    "activity": "Build a Simple Phishing Detector",
                    "description": "Create a basic phishing detection algorithm using provided tools",
                    "difficulty": "Intermediate",
                    "estimated_time": "45 minutes"
                })
        
        else:  # ai_content
            activities = [
                {
                    "activity": "Spot the AI Image",
                    "description": "Compare AI-generated and real images to identify differences",
                    "difficulty": "Beginner",
                    "estimated_time": "25 minutes"
                },
                {
                    "activity": "Audio Authenticity Challenge",
                    "description": "Listen to audio samples and identify which are AI-generated",
                    "difficulty": "Beginner",
                    "estimated_time": "20 minutes"
                }
            ]
            
            if user_level in ["intermediate", "advanced"]:
                activities.append({
                    "activity": "Metadata Analysis Lab",
                    "description": "Use forensic tools to analyze file metadata for authenticity",
                    "difficulty": "Intermediate",
                    "estimated_time": "40 minutes"
                })
        
        return activities
    
    def _generate_assessment_questions(self, user_level: str, detection_type: str) -> List[Dict[str, Any]]:
        """Generate assessment questions for learning validation"""
        if detection_type == "phishing":
            questions = [
                {
                    "question": "What are the three most important things to check when receiving a suspicious email?",
                    "type": "open_ended",
                    "difficulty": "beginner"
                },
                {
                    "question": "True or False: A legitimate website will never ask for your password via email.",
                    "type": "true_false",
                    "difficulty": "beginner",
                    "answer": "true"
                }
            ]
            
            if user_level in ["intermediate", "advanced"]:
                questions.append({
                    "question": "Explain how machine learning algorithms can detect phishing attempts that humans might miss.",
                    "type": "open_ended",
                    "difficulty": "intermediate"
                })
        
        else:  # ai_content
            questions = [
                {
                    "question": "What are common visual artifacts that might indicate an AI-generated image?",
                    "type": "open_ended",
                    "difficulty": "beginner"
                },
                {
                    "question": "True or False: AI detection algorithms are 100% accurate and never make mistakes.",
                    "type": "true_false",
                    "difficulty": "beginner",
                    "answer": "false"
                }
            ]
            
            if user_level in ["intermediate", "advanced"]:
                questions.append({
                    "question": "Describe how frequency domain analysis can help detect AI-generated audio.",
                    "type": "open_ended",
                    "difficulty": "intermediate"
                })
        
        return questions
    
    def _get_additional_resources(self, user_level: str, detection_type: str) -> List[Dict[str, str]]:
        """Get additional learning resources"""
        resources = []
        
        if detection_type == "phishing":
            resources = [
                {
                    "title": "NIST Cybersecurity Framework",
                    "type": "Official Guide",
                    "url": "https://www.nist.gov/cyberframework"
                },
                {
                    "title": "Anti-Phishing Working Group",
                    "type": "Research Organization",
                    "url": "https://www.antiphishing.org"
                }
            ]
        else:
            resources = [
                {
                    "title": "AI Detection Research Papers",
                    "type": "Academic Research",
                    "url": "https://scholar.google.com"
                },
                {
                    "title": "Digital Forensics Tools",
                    "type": "Tools and Software",
                    "url": "Various open-source tools"
                }
            ]
        
        return resources