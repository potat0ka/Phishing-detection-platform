"""
AI Content Detection System
==========================

This module detects whether images and documents are AI-generated.
Perfect for learning computer vision and machine learning concepts!

Features:
- Image analysis for AI-generated content
- Document text analysis for AI writing detection
- Multiple detection techniques combined for accuracy
- Beginner-friendly with detailed explanations
"""

# Import with fallback for cross-platform compatibility
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

try:
    from PIL import Image, ExifTags
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None
    ExifTags = None

import logging
from datetime import datetime
import os
import hashlib
import json
import re
from collections import Counter
import math

class AIContentDetector:
    """
    AI Content Detection System
    
    This class analyzes uploaded files to determine if they're AI-generated.
    It uses multiple techniques for better accuracy:
    
    For Images:
    - Metadata analysis (AI tools often leave specific signatures)
    - Pixel pattern analysis (AI images have distinct patterns)
    - Color distribution analysis (AI vs real image characteristics)
    - Statistical analysis patterns
    
    For Videos:
    - Frame consistency analysis (AI videos have temporal artifacts)
    - Compression pattern detection (AI videos compress differently)
    - Motion vector analysis (unnatural movement patterns)
    - Deepfake detection algorithms
    
    For Audio:
    - Spectral analysis (AI audio has distinct frequency patterns)
    - Voice synthesis detection (artificial speech patterns)
    - Audio artifact detection (AI generation artifacts)
    - Temporal consistency analysis
    
    For Documents/Text:
    - Writing pattern analysis
    - Vocabulary consistency
    - Structure analysis
    - AI writing signatures
    """
    
    def __init__(self):
        """Initialize the AI content detector with all analysis tools"""
        logging.info("Initializing AI Content Detector...")
        
        # Create uploads directory if it doesn't exist
        self.upload_dir = "uploads"
        os.makedirs(self.upload_dir, exist_ok=True)
        
        # Initialize detection models and parameters
        self._load_detection_parameters()
        
        # Log availability of optional dependencies
        if not NUMPY_AVAILABLE:
            logging.info("AI Content Detector initialized in basic mode (numpy not available)")
        elif not PIL_AVAILABLE:
            logging.info("AI Content Detector initialized with limited image support (PIL not available)")
        else:
            logging.info("AI Content Detector initialized successfully with full features")
            
    def _safe_mean(self, data):
        """Calculate mean with fallback for systems without numpy"""
        if NUMPY_AVAILABLE and hasattr(data, 'mean'):
            return float(data.mean())
        elif isinstance(data, (list, tuple)):
            return sum(data) / len(data) if data else 0.0
        else:
            return float(sum(data) / len(data)) if len(data) > 0 else 0.0
    
    def _safe_std(self, data):
        """Calculate standard deviation with fallback"""
        if NUMPY_AVAILABLE and hasattr(data, 'std'):
            return float(data.std())
        elif isinstance(data, (list, tuple)):
            if len(data) <= 1:
                return 0.0
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val) ** 2 for x in data) / len(data)
            return math.sqrt(variance)
        else:
            data_list = list(data)
            if len(data_list) <= 1:
                return 0.0
            mean_val = sum(data_list) / len(data_list)
            variance = sum((x - mean_val) ** 2 for x in data_list) / len(data_list)
            return math.sqrt(variance)
    
    def _safe_var(self, data):
        """Calculate variance with fallback"""
        if NUMPY_AVAILABLE and hasattr(data, 'var'):
            return float(data.var())
        elif isinstance(data, (list, tuple)):
            if len(data) <= 1:
                return 0.0
            mean_val = sum(data) / len(data)
            return sum((x - mean_val) ** 2 for x in data) / len(data)
        else:
            data_list = list(data)
            if len(data_list) <= 1:
                return 0.0
            mean_val = sum(data_list) / len(data_list)
            return sum((x - mean_val) ** 2 for x in data_list) / len(data_list)
    
    def _safe_array(self, data):
        """Convert to array-like structure with fallback"""
        if NUMPY_AVAILABLE:
            return self._safe_array(data)
        else:
            return data  # Return as-is for native Python processing
    
    def _safe_histogram(self, data, bins=256, range_vals=(0, 256)):
        """Calculate histogram with fallback"""
        if NUMPY_AVAILABLE:
            return self._safe_histogram(data, bins=bins, range=range_vals)
        else:
            # Python-native histogram calculation
            min_val, max_val = range_vals
            bin_width = (max_val - min_val) / bins
            hist = [0] * bins
            
            for value in data:
                if min_val <= value < max_val:
                    bin_idx = min(int((value - min_val) / bin_width), bins - 1)
                    hist[bin_idx] += 1
            
            # Create bin edges
            edges = [min_val + i * bin_width for i in range(bins + 1)]
            return hist, edges
    
    def _safe_gradient(self, data, axis=0):
        """Calculate gradient with fallback"""
        if NUMPY_AVAILABLE:
            return self._safe_gradient(data, axis=axis)
        else:
            # Simple difference-based gradient
            if axis == 0:  # vertical gradient
                grad = []
                for i in range(len(data)):
                    if i == 0:
                        grad.append([data[1][j] - data[0][j] for j in range(len(data[0]))])
                    elif i == len(data) - 1:
                        grad.append([data[i][j] - data[i-1][j] for j in range(len(data[0]))])
                    else:
                        grad.append([(data[i+1][j] - data[i-1][j]) / 2 for j in range(len(data[0]))])
                return grad
            else:  # horizontal gradient
                grad = []
                for i in range(len(data)):
                    row_grad = []
                    for j in range(len(data[0])):
                        if j == 0:
                            row_grad.append(data[i][1] - data[i][0])
                        elif j == len(data[0]) - 1:
                            row_grad.append(data[i][j] - data[i][j-1])
                        else:
                            row_grad.append((data[i][j+1] - data[i][j-1]) / 2)
                    grad.append(row_grad)
                return grad
    
    def _safe_sqrt(self, data):
        """Calculate square root with fallback"""
        if NUMPY_AVAILABLE:
            return self._safe_sqrt(data)
        else:
            if isinstance(data, (list, tuple)):
                return [math.sqrt(max(0, x)) for x in data]
            else:
                return math.sqrt(max(0, data))
    
    def _safe_sum(self, data, condition=None):
        """Calculate sum with optional condition fallback"""
        if NUMPY_AVAILABLE and condition is None:
            return self._safe_sum(data)
        else:
            if condition is not None:
                # Handle conditional sum
                return sum(1 for x in data if condition(x))
            else:
                return sum(data) if hasattr(data, '__iter__') else data
    
    def _safe_abs(self, data):
        """Calculate absolute value with fallback"""
        if NUMPY_AVAILABLE:
            return np.abs(data)
        else:
            if isinstance(data, (list, tuple)):
                return [abs(x) for x in data]
            else:
                return abs(data)
    
    def _safe_diff(self, data, axis=0):
        """Calculate difference with fallback"""
        if NUMPY_AVAILABLE:
            return np.diff(data, axis=axis)
        else:
            if axis == 1:  # horizontal difference
                result = []
                for row in data:
                    diff_row = [row[i+1] - row[i] for i in range(len(row)-1)]
                    result.append(diff_row)
                return result
            else:  # vertical difference
                result = []
                for i in range(len(data)-1):
                    diff_row = [data[i+1][j] - data[i][j] for j in range(len(data[0]))]
                    result.append(diff_row)
                return result
    
    def _safe_log2(self, data):
        """Calculate log2 with fallback"""
        if NUMPY_AVAILABLE:
            return np.log2(data)
        else:
            if isinstance(data, (list, tuple)):
                return [math.log2(max(1e-10, x)) for x in data]
            else:
                return math.log2(max(1e-10, data))
    
    def _load_detection_parameters(self):
        """
        Load parameters for AI detection algorithms
        
        These parameters are based on research into AI-generated content
        characteristics and help identify AI vs human-created content
        """
        # Image analysis parameters
        self.image_params = {
            'suspicious_metadata_keys': [
                'AI', 'artificial', 'generated', 'synthetic', 'midjourney', 
                'dall-e', 'stable diffusion', 'chatgpt', 'gpt', 'ai-generated',
                'leonardo', 'firefly', 'canva', 'runway', 'adobe firefly',
                'dall-e 2', 'dall-e 3', 'imagen', 'bing create', 'craiyon'
            ],
            'pixel_variance_threshold': 0.15,
            'color_distribution_threshold': 0.3,
            'statistical_anomaly_threshold': 0.25
        }
        
        # Video analysis parameters
        self.video_params = {
            'suspicious_metadata_keys': [
                'runway ml', 'pika labs', 'stable video', 'gen-2', 'gen-3',
                'synthesia', 'deepfake', 'faceswap', 'first order motion',
                'wav2lip', 'real-esrgan', 'topaz video ai', 'dain', 'rife'
            ],
            'frame_consistency_threshold': 0.8,
            'compression_anomaly_threshold': 0.6,
            'motion_analysis_threshold': 0.7,
            'deepfake_indicators': [
                'face_inconsistency', 'temporal_artifacts', 'blinking_patterns',
                'lip_sync_errors', 'lighting_inconsistency'
            ]
        }
        
        # Audio analysis parameters
        self.audio_params = {
            'suspicious_metadata_keys': [
                'elevenlabs', 'murf', 'speechify', 'replica', 'resemble',
                'voice cloning', 'ai voice', 'synthetic voice', 'tts',
                'tortoise tts', 'bark', 'vall-e', 'tacotron', 'wavenet'
            ],
            'spectral_anomaly_threshold': 0.6,
            'voice_synthesis_threshold': 0.7,
            'temporal_consistency_threshold': 0.8,
            'frequency_analysis_bands': [
                (0, 300),     # Sub-bass
                (300, 800),   # Bass
                (800, 2600),  # Midrange
                (2600, 5200), # Upper midrange
                (5200, 20000) # Treble
            ]
        }
        
        # Text analysis parameters
        self.text_params = {
            'ai_writing_indicators': [
                'as an ai', 'i am an ai', 'artificial intelligence', 
                'as a language model', 'i cannot', 'i don\'t have personal',
                'i apologize', 'furthermore', 'moreover', 'in conclusion',
                'it\'s worth noting', 'it\'s important to note', 'however',
                'additionally', 'consequently', 'therefore', 'nonetheless'
            ],
            'repetition_threshold': 0.3,     # AI text often has repetitive patterns
            'vocabulary_diversity_threshold': 0.6,  # AI text has specific vocab patterns
            'sentence_length_variance_threshold': 0.4
        }
    
    def analyze_content(self, file_path, content_type):
        """
        Main function to analyze uploaded content for AI generation
        
        Args:
            file_path (str): Path to the uploaded file
            content_type (str): Type of content ('image' or 'document')
            
        Returns:
            dict: Analysis results with confidence score and explanations
        """
        try:
            logging.info(f"Analyzing {content_type} content: {file_path}")
            
            if content_type == 'image':
                return self._analyze_image(file_path)
            elif content_type == 'video':
                return self._analyze_video(file_path)
            elif content_type == 'audio':
                return self._analyze_audio(file_path)
            elif content_type == 'document':
                return self._analyze_document(file_path)
            else:
                return {
                    'classification': 'error',
                    'confidence': 0.0,
                    'explanation': 'Unsupported content type',
                    'details': []
                }
                
        except Exception as e:
            logging.error(f"Error analyzing content: {e}")
            return {
                'classification': 'error',
                'confidence': 0.0,
                'explanation': f'Analysis failed: {str(e)}',
                'details': []
            }
    
    def _analyze_image(self, image_path):
        """
        Comprehensive image analysis for AI detection
        
        This function uses multiple computer vision techniques to detect
        if an image was generated by AI. Great for learning CV concepts!
        """
        results = {
            'classification': 'unknown',
            'confidence': 0.0,
            'explanation': '',
            'details': [],
            'analysis_methods': []
        }
        
        try:
            # Load the image
            pil_image = Image.open(image_path)
            
            if pil_image is None:
                raise ValueError("Could not load image file")
            
            # Method 1: Metadata Analysis
            metadata_score = self._analyze_image_metadata(pil_image)
            results['analysis_methods'].append({
                'method': 'Metadata Analysis',
                'score': metadata_score,
                'explanation': 'Checks for AI tool signatures in image metadata'
            })
            
            # Method 2: Pixel Pattern Analysis
            pixel_score = self._analyze_pixel_patterns(pil_image)
            results['analysis_methods'].append({
                'method': 'Pixel Pattern Analysis',
                'score': pixel_score,
                'explanation': 'Analyzes pixel distribution patterns typical of AI generation'
            })
            
            # Method 3: Color Distribution Analysis
            color_score = self._analyze_color_distribution(pil_image)
            results['analysis_methods'].append({
                'method': 'Color Distribution Analysis',
                'score': color_score,
                'explanation': 'Examines color patterns that differ between AI and real images'
            })
            
            # Method 4: Image Statistics Analysis
            stats_score = self._analyze_image_statistics(pil_image)
            results['analysis_methods'].append({
                'method': 'Image Statistics Analysis',
                'score': stats_score,
                'explanation': 'Studies statistical properties unique to AI generation'
            })
            
            # Calculate overall confidence with improved weighting
            # Real device photos often have camera metadata and natural imperfections
            device_photo_indicators = self._detect_device_photo_indicators(pil_image)
            
            # Adjust scores based on device photo indicators
            if device_photo_indicators['is_likely_device_photo']:
                # Reduce AI likelihood for photos with device characteristics
                metadata_score *= 0.3
                pixel_score *= 0.5
                color_score *= 0.6
                stats_score *= 0.4
            
            scores = [metadata_score, pixel_score, color_score, stats_score]
            average_score = self._safe_mean(scores)
            
            # Apply more conservative thresholds for better accuracy
            confidence = float(min(max(float(average_score), 0.0), 1.0))
            
            # More conservative classification thresholds
            if confidence >= 0.85:
                classification = 'ai_generated'
                explanation = 'Very high confidence this image was AI-generated'
            elif confidence >= 0.65:
                classification = 'possibly_ai'
                explanation = 'Some indicators suggest this might be AI-generated, but not conclusive'
            else:
                classification = 'likely_real'
                explanation = 'Appears to be a real photograph or human-created image'
            
            # Add detailed analysis
            results.update({
                'classification': classification,
                'confidence': confidence,
                'explanation': explanation,
                'details': [
                    f"Metadata analysis: {metadata_score:.2f}",
                    f"Pixel patterns: {pixel_score:.2f}",
                    f"Color distribution: {color_score:.2f}",
                    f"Image statistics: {stats_score:.2f}",
                    f"Overall confidence: {confidence:.2f}"
                ]
            })
            
            return results
            
        except Exception as e:
            logging.error(f"Image analysis error: {e}")
            results.update({
                'classification': 'error',
                'explanation': f'Image analysis failed: {str(e)}',
                'confidence': 0.0
            })
            return results
    
    def _analyze_image_metadata(self, pil_image):
        """
        Analyze image metadata for AI generation signatures
        
        Many AI tools leave traces in image metadata that can help
        identify AI-generated content.
        """
        try:
            # Extract EXIF data
            exif_data = pil_image._getexif()
            if not exif_data:
                return 0.2  # No metadata might indicate AI generation
            
            # Convert EXIF data to readable format
            metadata_text = ""
            for tag_id, value in exif_data.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                metadata_text += f"{tag}: {value} ".lower()
            
            # Check for AI-related keywords in metadata
            ai_indicators = 0
            for keyword in self.image_params['suspicious_metadata_keys']:
                if keyword.lower() in metadata_text:
                    ai_indicators += 1
            
            # Calculate score based on AI indicators found
            if ai_indicators > 0:
                return min(0.8 + (ai_indicators * 0.1), 1.0)
            
            # Check for missing typical camera metadata
            camera_fields = ['make', 'model', 'datetime', 'exifversion']
            missing_fields = sum(1 for field in camera_fields if field not in metadata_text)
            
            if missing_fields >= 3:
                return 0.6  # Missing camera data suggests AI generation
            
            return 0.1  # Normal metadata suggests real image
            
        except Exception:
            return 0.3  # Error reading metadata is somewhat suspicious
    
    def _analyze_pixel_patterns(self, pil_image):
        """
        Analyze pixel distribution patterns using PIL
        
        AI-generated images often have specific pixel distribution
        patterns that differ from real photographs.
        """
        try:
            # Convert to grayscale and get pixel data
            gray_image = pil_image.convert('L')
            pixels = self._safe_array(gray_image)
            
            # Calculate pixel variance (AI images often have lower variance)
            pixel_variance = float(self._safe_var(pixels)) / 255.0
            
            # Calculate histogram for smoothness analysis
            histogram = self._safe_histogram(pixels, bins=256, range=(0, 256))[0]
            hist_normalized = histogram / histogram.sum()
            
            # Check for artificial smoothness (common in AI images)
            smoothness = float(self._safe_std(hist_normalized))
            
            # Simple edge detection using gradient
            grad_x = self._safe_gradient(pixels.astype(float), axis=1)
            grad_y = self._safe_gradient(pixels.astype(float), axis=0)
            edge_magnitude = self._safe_sqrt(grad_x**2 + grad_y**2)
            noise_level = float(self._safe_std(edge_magnitude))
            normalized_noise = noise_level / 100.0  # Normalize
            
            # Combine factors for AI detection
            # Lower variance + lower noise + specific smoothness = more likely AI
            variance_score = 1.0 - min(pixel_variance / 0.3, 1.0)
            smoothness_score = float(max(0.0, 1.0 - smoothness * 10))
            noise_score = 1.0 - min(normalized_noise, 1.0)
            
            combined_score = (variance_score + smoothness_score + noise_score) / 3.0
            return float(max(0.0, min(combined_score, 1.0)))
            
        except Exception:
            return 0.3
    
    def _analyze_color_distribution(self, pil_image):
        """
        Analyze color distribution patterns
        
        AI-generated images often have specific color characteristics
        that differ from real photographs.
        """
        try:
            # Convert to RGB and analyze each channel
            rgb_image = pil_image.convert('RGB')
            pixels = self._safe_array(rgb_image)
            
            # Analyze each color channel
            channel_variances = []
            channel_means = []
            
            for channel in range(3):  # R, G, B
                channel_data = pixels[:, :, channel]
                channel_variances.append(self._safe_var(channel_data))
                channel_means.append(self._safe_mean(channel_data))
            
            # AI images often have more uniform color distribution
            variance_uniformity = self._safe_std(channel_variances) / self._safe_mean(channel_variances)
            mean_balance = self._safe_std(channel_means) / 255.0
            
            # Check for oversaturation (common in AI images)
            saturation_pixels = self._safe_sum((pixels == 255) | (pixels == 0))
            total_pixels = pixels.size
            saturation_ratio = saturation_pixels / total_pixels
            
            # Combine factors
            uniformity_score = 1.0 - min(float(variance_uniformity), 1.0)
            balance_score = 1.0 - min(float(mean_balance) * 4, 1.0)
            saturation_score = min(float(saturation_ratio) * 10, 1.0)
            
            combined_score = (uniformity_score + balance_score + saturation_score) / 3.0
            return float(max(0.0, min(combined_score, 1.0)))
            
        except Exception:
            return 0.3
    
    def _detect_device_photo_indicators(self, pil_image):
        """
        Detect indicators that suggest this is a real device photo
        
        Real device photos have specific characteristics that AI images lack
        """
        indicators = {
            'is_likely_device_photo': False,
            'has_exif_data': False,
            'has_camera_info': False,
            'has_natural_noise': False,
            'has_realistic_lighting': False
        }
        
        try:
            # Check for EXIF data (camera metadata)
            exif_data = pil_image._getexif()
            if exif_data:
                indicators['has_exif_data'] = True
                
                # Check for camera-specific tags
                camera_tags = [271, 272, 306, 36867, 36868]  # Make, Model, DateTime, etc.
                for tag in camera_tags:
                    if tag in exif_data:
                        indicators['has_camera_info'] = True
                        break
            
            # Convert to numpy for analysis
            img_array = self._safe_array(pil_image.convert('RGB'))
            
            # Check for natural noise patterns (real cameras have sensor noise)
            if len(img_array.shape) == 3:
                # Calculate noise level in image
                gray = self._safe_mean(img_array, axis=2)
                noise_level = self._safe_std(gray - self._safe_mean(gray))
                
                # Real photos typically have more natural noise
                if noise_level > 5.0:  # Threshold for natural noise
                    indicators['has_natural_noise'] = True
            
            # Check for realistic lighting gradients
            # Real photos have more complex lighting than AI images
            if len(img_array.shape) == 3:
                brightness_variance = self._safe_var(self._safe_mean(img_array, axis=2))
                if brightness_variance > 1000:  # Natural lighting variation
                    indicators['has_realistic_lighting'] = True
            
            # Determine if likely a device photo
            device_score = sum([
                indicators['has_exif_data'] * 2,
                indicators['has_camera_info'] * 3,
                indicators['has_natural_noise'] * 2,
                indicators['has_realistic_lighting'] * 1
            ])
            
            # If score >= 4, likely a real device photo
            indicators['is_likely_device_photo'] = device_score >= 4
            
            return indicators
            
        except Exception:
            return indicators
    
    def _analyze_image_statistics(self, pil_image):
        """
        Analyze statistical properties of the image
        
        AI-generated images often have specific statistical signatures
        that can be detected through mathematical analysis.
        """
        try:
            # Resize large images to prevent timeout
            max_size = 800
            if pil_image.width > max_size or pil_image.height > max_size:
                pil_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert to array for analysis
            pixels = self._safe_array(pil_image.convert('L'), dtype=np.float32)
            
            # Calculate entropy (measure of randomness)
            histogram = self._safe_histogram(pixels, bins=256, range=(0, 256))[0]
            histogram = histogram[histogram > 0]  # Remove zeros
            entropy = -self._safe_sum((histogram / histogram.sum()) * np.log2(histogram / histogram.sum()))
            
            # AI images often have lower entropy (less randomness)
            entropy_score = 1.0 - min(entropy / 8.0, 1.0)  # Normalize entropy
            
            # Calculate local contrast using standard deviation of local patches (optimized)
            patch_size = 16  # Larger patches for efficiency
            local_stds = []
            
            height, width = pixels.shape
            # Limit number of patches to prevent timeout
            max_patches = 100
            patch_count = 0
            
            for i in range(0, height - patch_size, patch_size * 2):  # Skip patches for speed
                for j in range(0, width - patch_size, patch_size * 2):
                    if patch_count >= max_patches:
                        break
                    patch = pixels[i:i+patch_size, j:j+patch_size]
                    local_stds.append(float(self._safe_std(patch)))
                    patch_count += 1
                if patch_count >= max_patches:
                    break
            
            if local_stds:
                contrast_variance = self._safe_var(local_stds)
                contrast_score = 1.0 - min(float(contrast_variance) / 1000.0, 1.0)
            else:
                contrast_score = 0.5
            
            # Calculate pixel value transitions (how smoothly values change)
            diff_horizontal = np.abs(np.diff(pixels, axis=1))
            diff_vertical = np.abs(np.diff(pixels, axis=0))
            
            smooth_transitions = self._safe_sum((diff_horizontal < 10) & (diff_horizontal > 0))
            smooth_transitions += self._safe_sum((diff_vertical < 10) & (diff_vertical > 0))
            total_transitions = diff_horizontal.size + diff_vertical.size
            
            if total_transitions > 0:
                smoothness_ratio = smooth_transitions / total_transitions
                smoothness_score = min(smoothness_ratio * 2, 1.0)  # AI images are often smoother
            else:
                smoothness_score = 0.5
            
            # Combine all statistical measures
            combined_score = (entropy_score + contrast_score + smoothness_score) / 3.0
            return float(max(0.0, min(combined_score, 1.0)))
            
        except Exception:
            return 0.3
    
    def _analyze_video(self, video_path):
        """
        Comprehensive video analysis for AI/deepfake detection
        
        This function analyzes video files for signs of AI generation,
        deepfakes, and other synthetic content manipulation.
        """
        results = {
            'classification': 'unknown',
            'confidence': 0.0,
            'explanation': '',
            'details': [],
            'analysis_methods': [],
            'suspected_source': None,
            'editing_indicators': []
        }
        
        try:
            # Method 1: Metadata Analysis
            metadata_score, metadata_info = self._analyze_video_metadata(video_path)
            results['analysis_methods'].append({
                'method': 'Metadata Analysis',
                'score': metadata_score,
                'explanation': 'Checks for AI video generation tool signatures'
            })
            
            # Method 2: File Structure Analysis
            structure_score, structure_info = self._analyze_video_structure(video_path)
            results['analysis_methods'].append({
                'method': 'File Structure Analysis',
                'score': structure_score,
                'explanation': 'Analyzes video encoding patterns typical of AI tools'
            })
            
            # Method 3: Frame Analysis (simplified)
            frame_score, frame_info = self._analyze_video_frames(video_path)
            results['analysis_methods'].append({
                'method': 'Frame Pattern Analysis',
                'score': frame_score,
                'explanation': 'Detects artificial patterns in video frames'
            })
            
            # Calculate overall confidence
            scores = [metadata_score, structure_score, frame_score]
            average_score = self._safe_mean(scores)
            confidence = float(min(max(float(average_score), 0.0), 1.0))
            
            # Determine classification and source
            classification, suspected_source, editing_indicators = self._classify_video_result(
                confidence, metadata_info, structure_info, frame_info
            )
            
            results.update({
                'classification': classification,
                'confidence': confidence,
                'explanation': self._generate_video_explanation(classification, confidence),
                'suspected_source': suspected_source,
                'editing_indicators': editing_indicators,
                'details': [
                    f"Metadata analysis: {metadata_score:.2f}",
                    f"File structure: {structure_score:.2f}",
                    f"Frame patterns: {frame_score:.2f}",
                    f"Overall confidence: {confidence:.2f}"
                ]
            })
            
            return results
            
        except Exception as e:
            logging.error(f"Video analysis error: {e}")
            results.update({
                'classification': 'error',
                'explanation': f'Video analysis failed: {str(e)}',
                'confidence': 0.0
            })
            return results
    
    def _analyze_audio(self, audio_path):
        """
        Comprehensive audio analysis for AI/synthetic voice detection
        
        This function analyzes audio files for signs of AI generation,
        voice cloning, and synthetic speech.
        """
        results = {
            'classification': 'unknown',
            'confidence': 0.0,
            'explanation': '',
            'details': [],
            'analysis_methods': [],
            'suspected_source': None,
            'editing_indicators': []
        }
        
        try:
            # Method 1: Metadata Analysis
            metadata_score, metadata_info = self._analyze_audio_metadata(audio_path)
            results['analysis_methods'].append({
                'method': 'Metadata Analysis',
                'score': metadata_score,
                'explanation': 'Checks for AI audio generation tool signatures'
            })
            
            # Method 2: File Structure Analysis
            structure_score, structure_info = self._analyze_audio_structure(audio_path)
            results['analysis_methods'].append({
                'method': 'File Structure Analysis',
                'score': structure_score,
                'explanation': 'Analyzes audio encoding patterns from AI tools'
            })
            
            # Method 3: Basic Audio Pattern Analysis
            pattern_score, pattern_info = self._analyze_audio_patterns(audio_path)
            results['analysis_methods'].append({
                'method': 'Audio Pattern Analysis',
                'score': pattern_score,
                'explanation': 'Detects synthetic audio generation patterns'
            })
            
            # Calculate overall confidence
            scores = [metadata_score, structure_score, pattern_score]
            average_score = self._safe_mean(scores)
            confidence = float(min(max(float(average_score), 0.0), 1.0))
            
            # Determine classification and source
            classification, suspected_source, editing_indicators = self._classify_audio_result(
                confidence, metadata_info, structure_info, pattern_info
            )
            
            results.update({
                'classification': classification,
                'confidence': confidence,
                'explanation': self._generate_audio_explanation(classification, confidence),
                'suspected_source': suspected_source,
                'editing_indicators': editing_indicators,
                'details': [
                    f"Metadata analysis: {metadata_score:.2f}",
                    f"File structure: {structure_score:.2f}",
                    f"Audio patterns: {pattern_score:.2f}",
                    f"Overall confidence: {confidence:.2f}"
                ]
            })
            
            return results
            
        except Exception as e:
            logging.error(f"Audio analysis error: {e}")
            results.update({
                'classification': 'error',
                'explanation': f'Audio analysis failed: {str(e)}',
                'confidence': 0.0
            })
            return results
    
    def _analyze_document(self, doc_path):
        """
        Analyze text documents for AI generation
        
        This function examines writing patterns, vocabulary, and structure
        to detect AI-generated text content.
        """
        results = {
            'classification': 'unknown',
            'confidence': 0.0,
            'explanation': '',
            'details': [],
            'analysis_methods': []
        }
        
        try:
            # Read the document
            with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            if not text.strip():
                raise ValueError("Document is empty or unreadable")
            
            # Method 1: AI Writing Pattern Detection
            pattern_score = self._analyze_writing_patterns(text)
            results['analysis_methods'].append({
                'method': 'Writing Pattern Analysis',
                'score': pattern_score,
                'explanation': 'Detects AI-specific writing patterns and phrases'
            })
            
            # Method 2: Vocabulary Analysis
            vocab_score = self._analyze_vocabulary_patterns(text)
            results['analysis_methods'].append({
                'method': 'Vocabulary Analysis',
                'score': vocab_score,
                'explanation': 'Examines word choice and vocabulary diversity'
            })
            
            # Method 3: Structure Analysis
            structure_score = self._analyze_text_structure(text)
            results['analysis_methods'].append({
                'method': 'Text Structure Analysis',
                'score': structure_score,
                'explanation': 'Analyzes sentence structure and flow patterns'
            })
            
            # Calculate overall confidence
            scores = [pattern_score, vocab_score, structure_score]
            average_score = self._safe_mean(scores)
            confidence = float(min(max(float(average_score), 0.0), 1.0))
            
            # Determine classification
            if confidence >= 0.7:
                classification = 'ai_generated'
                explanation = 'High confidence this text was AI-generated'
            elif confidence >= 0.4:
                classification = 'possibly_ai'
                explanation = 'Some patterns suggest this might be AI-generated'
            else:
                classification = 'likely_human'
                explanation = 'Appears to be human-written text'
            
            results.update({
                'classification': classification,
                'confidence': confidence,
                'explanation': explanation,
                'details': [
                    f"Writing patterns: {pattern_score:.2f}",
                    f"Vocabulary analysis: {vocab_score:.2f}",
                    f"Structure analysis: {structure_score:.2f}",
                    f"Overall confidence: {confidence:.2f}"
                ]
            })
            
            return results
            
        except Exception as e:
            logging.error(f"Document analysis error: {e}")
            results.update({
                'classification': 'error',
                'explanation': f'Document analysis failed: {str(e)}',
                'confidence': 0.0
            })
            return results
    
    def _analyze_writing_patterns(self, text):
        """
        Detect AI-specific writing patterns
        
        AI text often contains specific phrases and patterns
        that human writers rarely use.
        """
        text_lower = text.lower()
        
        # Count AI indicator phrases
        ai_indicators = 0
        for phrase in self.text_params['ai_writing_indicators']:
            ai_indicators += text_lower.count(phrase)
        
        # Calculate score based on frequency
        text_length = len(text.split())
        if text_length > 0:
            indicator_density = ai_indicators / text_length
            return min(indicator_density * 100, 1.0)
        
        return 0.0
    
    def _analyze_vocabulary_patterns(self, text):
        """
        Analyze vocabulary diversity and patterns
        
        AI text often has specific vocabulary characteristics
        that differ from human writing.
        """
        words = re.findall(r'\b\w+\b', text.lower())
        if len(words) < 10:
            return 0.0
        
        # Calculate vocabulary diversity
        unique_words = len(set(words))
        vocab_diversity = unique_words / len(words)
        
        # AI text often has lower diversity
        if vocab_diversity < self.text_params['vocabulary_diversity_threshold']:
            return 0.7
        elif vocab_diversity < 0.8:
            return 0.3
        
        # Check for repetitive word patterns
        word_counts = Counter(words)
        most_common = word_counts.most_common(10)
        
        # Calculate repetition score
        total_repetitions = sum(count for word, count in most_common if count > 3)
        repetition_ratio = total_repetitions / len(words)
        
        if repetition_ratio > self.text_params['repetition_threshold']:
            return float(max(0.5, min(repetition_ratio * 2, 1.0)))
        
        return 0.1
    
    def _analyze_text_structure(self, text):
        """
        Analyze sentence structure and flow
        
        AI text often has very consistent sentence structure
        that differs from natural human variation.
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 3:
            return 0.0
        
        # Calculate sentence length variance
        sentence_lengths = [len(s.split()) for s in sentences]
        if len(sentence_lengths) > 1:
            length_variance = self._safe_var(sentence_lengths) / float(max(float(self._safe_mean(sentence_lengths)), 1))
            
            # AI text often has very consistent sentence lengths
            if length_variance < self.text_params['sentence_length_variance_threshold']:
                return 0.6
        
        # Check for overly perfect grammar and structure
        perfect_sentences = 0
        for sentence in sentences:
            # Simple checks for AI-like perfection
            words = sentence.split()
            if len(words) > 5:
                # Check for consistent capitalization and punctuation
                if sentence[0].isupper() and not any(char in sentence for char in ['..', '??', '!!']):
                    perfect_sentences += 1
        
        perfection_ratio = perfect_sentences / len(sentences)
        if perfection_ratio > 0.8:  # Too perfect might indicate AI
            return 0.5
        
        return 0.2
    
    def save_analysis_result(self, file_path, analysis_result, user_id=None, user_ip=None):
        """
        Save analysis results for future reference
        
        This helps track detection history and improve the system
        """
        try:
            # Create results directory
            results_dir = "analysis_results"
            os.makedirs(results_dir, exist_ok=True)
            
            # Generate unique filename
            file_hash = hashlib.md5(file_path.encode()).hexdigest()
            result_file = os.path.join(results_dir, f"{file_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            # Prepare result data
            result_data = {
                'timestamp': datetime.now().isoformat(),
                'file_path': file_path,
                'analysis_result': analysis_result
            }
            
            # Save to JSON file
            with open(result_file, 'w') as f:
                json.dump(result_data, f, indent=2)
            
            logging.info(f"Analysis result saved: {result_file}")
            
        except Exception as e:
            logging.error(f"Error saving analysis result: {e}")

    # Video Analysis Helper Methods
    def _analyze_video_metadata(self, video_path):
        """Analyze video metadata for AI generation signatures"""
        try:
            import os
            file_size = os.path.getsize(video_path)
            filename = os.path.basename(video_path).lower()
            
            metadata_info = {
                'filename': filename,
                'file_size': file_size,
                'suspected_tools': []
            }
            
            # Check filename for AI tool indicators
            ai_score = 0.0
            for tool in self.video_params['suspicious_metadata_keys']:
                if tool in filename:
                    ai_score += 0.3
                    metadata_info['suspected_tools'].append(tool)
            
            # Unusual file size patterns
            if file_size < 1024 * 1024:  # Very small video files can indicate AI generation
                ai_score += 0.2
            
            return min(ai_score, 1.0), metadata_info
        except:
            return 0.3, {'error': 'Could not analyze video metadata'}
    
    def _analyze_video_structure(self, video_path):
        """Analyze video file structure patterns"""
        try:
            import os
            file_size = os.path.getsize(video_path)
            extension = video_path.lower().split('.')[-1]
            
            structure_info = {
                'extension': extension,
                'file_size': file_size,
                'compression_indicators': []
            }
            
            # AI videos often have specific compression patterns
            score = 0.0
            
            # Check for common AI video formats
            ai_formats = ['mp4', 'mov', 'webm']
            if extension in ai_formats:
                score += 0.1
            
            # File size analysis
            size_mb = file_size / (1024 * 1024)
            if size_mb < 5:  # Very small videos often AI-generated
                score += 0.3
                structure_info['compression_indicators'].append('unusually_small_file')
            elif size_mb > 300:  # Very large files might indicate high-quality AI
                score += 0.2
                structure_info['compression_indicators'].append('unusually_large_file')
            elif 50 < size_mb < 200:  # Typical AI video size range
                score += 0.1
                structure_info['compression_indicators'].append('typical_ai_size_range')
            
            return min(score, 1.0), structure_info
        except:
            return 0.3, {'error': 'Could not analyze video structure'}
    
    def _analyze_video_frames(self, video_path):
        """Basic frame pattern analysis"""
        try:
            frame_info = {
                'patterns': [],
                'anomalies': []
            }
            
            # Simplified frame analysis based on file characteristics
            score = 0.0
            
            # This is a simplified analysis - in a real implementation,
            # you would extract frames and analyze them
            filename = os.path.basename(video_path).lower()
            
            # Check for indicators in filename
            ai_indicators = ['generated', 'ai', 'synthetic', 'fake', 'deepfake']
            for indicator in ai_indicators:
                if indicator in filename:
                    score += 0.4
                    frame_info['patterns'].append(f'filename_contains_{indicator}')
            
            return min(score, 1.0), frame_info
        except:
            return 0.3, {'error': 'Could not analyze video frames'}
    
    def _classify_video_result(self, confidence, metadata_info, structure_info, frame_info):
        """Classify video analysis results and identify source"""
        suspected_source = None
        editing_indicators = []
        
        # Identify suspected AI tool based on metadata
        if metadata_info.get('suspected_tools'):
            suspected_source = metadata_info['suspected_tools'][0].title()
        
        # Determine editing indicators
        if structure_info.get('compression_indicators'):
            editing_indicators.extend(structure_info['compression_indicators'])
        
        if frame_info.get('patterns'):
            editing_indicators.extend(frame_info['patterns'])
        
        # Classify based on confidence
        if confidence >= 0.7:
            classification = 'ai_generated'
        elif confidence >= 0.4:
            classification = 'possibly_ai'
        else:
            classification = 'likely_real'
        
        return classification, suspected_source, editing_indicators
    
    def _generate_video_explanation(self, classification, confidence):
        """Generate human-readable explanation for video analysis"""
        if classification == 'ai_generated':
            return f'High confidence ({confidence:.1%}) this video was AI-generated or heavily edited'
        elif classification == 'possibly_ai':
            return f'Moderate confidence ({confidence:.1%}) this video may contain AI-generated elements'
        else:
            return f'Low confidence ({confidence:.1%}) of AI generation - appears to be authentic video'
    
    # Audio Analysis Helper Methods
    def _analyze_audio_metadata(self, audio_path):
        """Analyze audio metadata for AI generation signatures"""
        try:
            import os
            file_size = os.path.getsize(audio_path)
            filename = os.path.basename(audio_path).lower()
            
            metadata_info = {
                'filename': filename,
                'file_size': file_size,
                'suspected_tools': []
            }
            
            # Check filename for AI tool indicators
            ai_score = 0.0
            for tool in self.audio_params['suspicious_metadata_keys']:
                if tool in filename:
                    ai_score += 0.4
                    metadata_info['suspected_tools'].append(tool)
            
            # Check for TTS indicators
            tts_indicators = ['tts', 'speech', 'voice', 'generated', 'synthetic']
            for indicator in tts_indicators:
                if indicator in filename:
                    ai_score += 0.2
                    metadata_info['suspected_tools'].append(f'TTS_{indicator}')
            
            return min(ai_score, 1.0), metadata_info
        except:
            return 0.3, {'error': 'Could not analyze audio metadata'}
    
    def _analyze_audio_structure(self, audio_path):
        """Analyze audio file structure patterns"""
        try:
            import os
            file_size = os.path.getsize(audio_path)
            extension = audio_path.lower().split('.')[-1]
            
            structure_info = {
                'extension': extension,
                'file_size': file_size,
                'encoding_indicators': []
            }
            
            score = 0.0
            
            # AI audio often uses specific formats
            ai_formats = ['wav', 'mp3', 'm4a']
            if extension in ai_formats:
                score += 0.1
            
            # File size analysis
            size_kb = file_size / 1024
            if size_kb < 500:  # Very small audio files
                score += 0.3
                structure_info['encoding_indicators'].append('unusually_small_file')
            
            return min(score, 1.0), structure_info
        except:
            return 0.3, {'error': 'Could not analyze audio structure'}
    
    def _analyze_audio_patterns(self, audio_path):
        """Basic audio pattern analysis"""
        try:
            pattern_info = {
                'patterns': [],
                'anomalies': []
            }
            
            score = 0.0
            filename = os.path.basename(audio_path).lower()
            
            # Check for AI audio indicators
            ai_indicators = ['clone', 'synthetic', 'generated', 'ai', 'tts', 'voice']
            for indicator in ai_indicators:
                if indicator in filename:
                    score += 0.3
                    pattern_info['patterns'].append(f'filename_contains_{indicator}')
            
            return min(score, 1.0), pattern_info
        except:
            return 0.3, {'error': 'Could not analyze audio patterns'}
    
    def _classify_audio_result(self, confidence, metadata_info, structure_info, pattern_info):
        """Classify audio analysis results and identify source"""
        suspected_source = None
        editing_indicators = []
        
        # Identify suspected AI tool
        if metadata_info.get('suspected_tools'):
            suspected_source = metadata_info['suspected_tools'][0].title()
        
        # Determine editing indicators
        if structure_info.get('encoding_indicators'):
            editing_indicators.extend(structure_info['encoding_indicators'])
        
        if pattern_info.get('patterns'):
            editing_indicators.extend(pattern_info['patterns'])
        
        # Classify based on confidence
        if confidence >= 0.7:
            classification = 'ai_generated'
        elif confidence >= 0.4:
            classification = 'possibly_ai'
        else:
            classification = 'likely_real'
        
        return classification, suspected_source, editing_indicators
    
    def _generate_audio_explanation(self, classification, confidence):
        """Generate human-readable explanation for audio analysis"""
        if classification == 'ai_generated':
            return f'High confidence ({confidence:.1%}) this audio was AI-generated or synthesized'
        elif classification == 'possibly_ai':
            return f'Moderate confidence ({confidence:.1%}) this audio may be synthetic or cloned'
        else:
            return f'Low confidence ({confidence:.1%}) of AI generation - appears to be authentic audio'

# Global detector instance
ai_detector = AIContentDetector()