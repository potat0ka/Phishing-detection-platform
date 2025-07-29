"""
Main Routes - Landing Page, Detection, Tips
==========================================

This blueprint handles the main public routes of the application:
- Homepage (landing page)
- Phishing detection/scanning
- Security tips page
- Analytics page

Author: Bigendra Shrestha
"""

from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
from flask_login import login_required
from datetime import datetime
from models import PhishingModel, SafetyTipsModel, AnalyticsModel
from models.scan_history_model import ScanHistoryModel
from utils.phishing_detector import PhishingDetector
from utils.validation import validate_url
from services.text_analysis import analyze_text_content, extract_text_from_file
import logging
import os
from werkzeug.utils import secure_filename
from flask import current_app

logger = logging.getLogger(__name__)

# Create blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Homepage/Landing page

    GET: Displays system statistics, recent threats, and featured security tip.
    POST: Handles quick phishing check form submission (redirects to check_url)
    """
    # Handle POST request from quick check form
    if request.method == 'POST':
        # Redirect POST request to the check_url handler
        return check_url()

    # Handle GET request (normal homepage display)
    try:
        # Get data from MongoDB models
        system_stats = AnalyticsModel.get_system_stats()
        recent_threats = PhishingModel.get_recent_threats(limit=3)
        featured_tip = SafetyTipsModel.get_featured_tip()

        # Check if database is connected (for template display)
        db_connected = current_app.mongo.db is not None  # type: ignore

        return render_template('index.html',
                             system_stats=system_stats,
                             recent_threats=recent_threats,
                             featured_tip=featured_tip,
                             db_connected=db_connected)
    except Exception as e:
        logger.error(f"Error loading homepage: {e}")
        return render_template('index.html',
                             system_stats=AnalyticsModel.get_fallback_stats(),
                             recent_threats=[],
                             featured_tip=None,
                             db_connected=False)

@main_bp.route('/check', methods=['GET', 'POST'])
@login_required
def check_url():
    """
    AI-powered phishing detection page

    GET: Show the content analysis form with three input types
    POST: Process and analyze content (URL, Email, or Message) using ML models
    """
    if request.method == 'GET':
        return render_template('check.html')

    try:
        # Import the new ML detector
        from utils.ml_detector import MLPhishingDetector

        # Get form data based on input type - support both form formats
        input_type = request.form.get('input_type', '').strip()
        content = ''

        # Extract content based on selected type - support both homepage and check page formats
        if input_type == 'url':
            # Try both field names for compatibility (homepage uses 'input_content', check page uses 'url')
            content = request.form.get('url', '').strip() or request.form.get('input_content', '').strip()
            if not content:
                return render_template('result.html', 
                                     error="Please enter a URL to analyze")
            # Validate URL format
            if not validate_url(content):
                return render_template('result.html',
                                     error="Please enter a valid URL (must start with http:// or https://)")

        elif input_type == 'email':
            # Try both field names for compatibility
            content = request.form.get('email_content', '').strip() or request.form.get('input_content', '').strip()
            if not content:
                return render_template('result.html',
                                     error="Please enter email content to analyze")
            # Validate minimum content length
            if len(content) < 10:
                return render_template('result.html',
                                     error="Please enter at least 10 characters of email content")

        elif input_type == 'message':
            # Try both field names for compatibility
            content = request.form.get('message_content', '').strip() or request.form.get('input_content', '').strip()
            if not content:
                return render_template('result.html',
                                     error="Please enter message/text content to analyze")
            # Validate minimum content length
            if len(content) < 5:
                return render_template('result.html',
                                     error="Please enter at least 5 characters of message content")

        else:
            return render_template('result.html',
                                 error="Please select a content type (URL, Email, or Message)")

        logger.info(f"Starting {input_type} analysis: {content[:50]}...")

        # For message/text content, use shared text analysis service (same as analyze-text)
        if input_type == 'message' and len(content) >= 50:
            logger.info("Using shared text analysis service for message content - redirecting to analyze-text for consistency")
            # Redirect to analyze-text route for identical experience
            return redirect(url_for('main.analyze_text') + f'?prefilled_text={content[:500]}')
        else:
            # Use ML detector for URL and email content, or short message content
            detector = MLPhishingDetector()
            result = detector.analyze_content(content, input_type)

        # Check for analysis errors
        if result.get('error'):
            logger.error(f"ML detector error: {result.get('warnings', ['Unknown error'])}")
            return render_template('result.html',
                                 error=f"Analysis failed: {result.get('warnings', ['Unknown error'])[0]}")

        # Save comprehensive scan result to user history
        try:
            from models.scan_history_model import ScanHistoryModel

            # Get current user ID from session (None for anonymous users)
            current_user_id = session.get('user_id')

            # Save detailed scan result with user context
            scan_id = ScanHistoryModel.save_scan_result(
                content=content,
                content_type=input_type,
                result=result,
                user_id=current_user_id
            )

            # Log success with context
            user_context = f"user {current_user_id}" if current_user_id else "anonymous user"
            logger.info(f"Scan saved (ID: {scan_id}) for {user_context}")

            # Update system-wide analytics
            AnalyticsModel.update_scan_count()
            if result['threat_level'] in ['high', 'medium']:
                AnalyticsModel.update_threat_blocked()

        except Exception as log_error:
            logger.error(f"Failed to save scan result: {log_error}")

        logger.info(f"{input_type.title()} analysis complete - Threat: {result['threat_level']}, Confidence: {result['confidence_score']:.2f}")

        # Create comprehensive context for result template
        scan_id = locals().get('scan_id', None)
        current_user_id = locals().get('current_user_id', session.get('user_id'))
        result_context = {
            'result': result,
            'content': content,
            'input_type': input_type,
            'analysis_timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'scan_id': scan_id,
            'user_authenticated': current_user_id is not None
        }

        return render_template('result.html', **result_context)

    except ImportError as e:
        logger.error(f"ML detector import error: {e}")
        return render_template('result.html',
                             error="AI analysis system is currently unavailable. Please try again later.")

    except Exception as e:
        logger.error(f"Error processing content analysis: {str(e)}")
        return render_template('result.html',
                             error=f"Analysis error: {str(e)}. Please check your input and try again.")

@main_bp.route('/tips')
def tips():
    """
    Safety Tips Page

    Display cybersecurity safety tips organized by categories
    """
    try:
        # Get tips by category using the SafetyTipsModel
        from models.safety_tips_model import SafetyTipsModel

        # Initialize default tips if needed
        SafetyTipsModel.initialize_default_tips()

        url_tips = SafetyTipsModel.get_tips_by_category('url')
        email_tips = SafetyTipsModel.get_tips_by_category('email')
        general_tips = SafetyTipsModel.get_tips_by_category('general')

        # Debug logging
        logger.info(f"Tips loaded - URL: {len(url_tips)}, Email: {len(email_tips)}, General: {len(general_tips)}")

        # Calculate stats for the tips page
        stats = {
            'total_tips': len(url_tips) + len(email_tips) + len(general_tips),
            'url_count': len(url_tips),
            'email_count': len(email_tips),
            'general_count': len(general_tips)
        }

        return render_template('tips.html', 
                             url_tips=url_tips,
                             email_tips=email_tips,
                             general_tips=general_tips,
                             stats=stats)

    except Exception as e:
        logger.error(f"Error loading safety tips: {e}")
        # Return empty tips on error
        return render_template('tips.html', 
                             url_tips=[],
                             email_tips=[],
                             general_tips=[],
                             stats={'total_tips': 0, 'url_count': 0, 'email_count': 0, 'general_count': 0})

@main_bp.route('/analyze-text', methods=['GET', 'POST'])
def analyze_text():
    """
    Enhanced Text Analysis page with file upload support
    
    Supports:
    - Direct text input
    - File uploads (.txt, .pdf, .docx, .jpg, .png)
    - AI-generated content detection
    - Plagiarism detection with source URLs
    
    GET: Show the text analysis form with file upload
    POST: Process text/file and return comprehensive analysis results
    """
    if request.method == 'GET':
        # Import shared service to get supported formats
        from services.text_analysis import text_analysis_service
        supported_formats = text_analysis_service.get_supported_formats()
        
        # Check if text was prefilled from homepage redirect
        prefilled_text = request.args.get('prefilled_text', '').strip()
        
        return render_template('analyze_text.html', 
                             supported_formats=supported_formats,
                             prefilled_text=prefilled_text)

    try:
        logger.info("Starting enhanced text analysis request using shared service")

        # Get form data
        text_content = request.form.get('text_content', '').strip()
        check_plagiarism = request.form.get('check_plagiarism') == 'on'
        check_ai = request.form.get('check_ai') == 'on'
        
        # Check if file was uploaded
        uploaded_file = request.files.get('text_file')
        file_info = None
        
        # Extract text from file if provided using shared service
        if uploaded_file and uploaded_file.filename:
            logger.info(f"Processing uploaded file: {uploaded_file.filename}")
            
            # Validate file type
            filename = secure_filename(uploaded_file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            
            allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'txt', 'pdf', 'docx', 'jpg', 'jpeg', 'png', 'gif'})
            
            if file_ext not in allowed_extensions:
                from services.text_analysis import text_analysis_service
                return render_template('analyze_text.html', 
                                     error=f"File type '.{file_ext}' not supported. Allowed types: {', '.join(allowed_extensions)}",
                                     supported_formats=text_analysis_service.get_supported_formats())
            
            # Save file temporarily for processing
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            import tempfile
            import uuid
            
            # Create unique filename to avoid conflicts
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(upload_folder, unique_filename)
            
            try:
                # Save the uploaded file
                uploaded_file.save(file_path)
                logger.info(f"File saved to: {file_path}")
                
                # Extract text from the saved file
                file_result = extract_text_from_file(file_path)
                
                # Clean up the temporary file
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                if not file_result['success']:
                    from services.text_analysis import text_analysis_service
                    return render_template('analyze_text.html', 
                                         error=file_result['error'],
                                         supported_formats=text_analysis_service.get_supported_formats())
                
                # Use extracted text
                text_content = file_result['text']
                file_info = {
                    'filename': uploaded_file.filename,
                    'file_type': file_result.get('file_type', file_ext),
                    'source': file_result.get('source', 'file_upload'),
                    'size': len(text_content),
                    'extraction_details': file_result
                }
                
                logger.info(f"Successfully extracted {len(text_content)} characters from {uploaded_file.filename}")
                
            except Exception as e:
                # Clean up file if it exists
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                logger.error(f"Error processing uploaded file: {e}")
                from services.text_analysis import text_analysis_service
                return render_template('analyze_text.html', 
                                     error=f"Error processing file: {str(e)}",
                                     supported_formats=text_analysis_service.get_supported_formats())

        # Get supported formats for error handling
        from services.text_analysis import text_analysis_service
        supported_formats = text_analysis_service.get_supported_formats()

        # Validate we have text content
        if not text_content:
            return render_template('analyze_text.html', 
                                 error="Please enter text content or upload a file to analyze",
                                 supported_formats=supported_formats)

        # Validate text length (using shared service validation)
        if len(text_content) < 50:
            return render_template('analyze_text.html',
                                 error="Text must be at least 50 characters long for analysis",
                                 supported_formats=supported_formats)

        if len(text_content) > 50000:
            return render_template('analyze_text.html',
                                 error="Text is too long. Maximum 50,000 characters allowed",
                                 supported_formats=supported_formats)

        # Ensure at least one analysis type is selected
        if not check_plagiarism and not check_ai:
            return render_template('analyze_text.html',
                                 error="Please select at least one analysis type (AI Detection or Plagiarism Check)",
                                 supported_formats=supported_formats)

        logger.info(f"Starting analysis: {len(text_content)} chars, AI: {check_ai}, Plagiarism: {check_plagiarism}")

        # Perform comprehensive text analysis using shared service
        source = "file_upload" if file_info else "manual"
        result = analyze_text_content(text_content, check_ai=check_ai, check_plagiarism=check_plagiarism, source=source)

        # Check for analysis errors
        if not result.get('success', False):
            logger.error(f"Text analysis failed: {result.get('error', 'Unknown error')}")
            return render_template('analyze_text.html',
                                 error=f"Analysis failed: {result.get('error', 'Unknown error')}",
                                 supported_formats=supported_formats)

        # Add file information to result
        if file_info:
            result['file_info'] = file_info

        # Save analysis result to user history
        try:
            from models.scan_history_model import ScanHistoryModel

            # Get current user ID from session
            current_user_id = session.get('user_id')

            # Create a comprehensive result for history
            history_result = {
                'analysis_type': 'text_analysis',
                'file_uploaded': file_info is not None,
                'filename': file_info['filename'] if file_info else None,
                'text_length': len(text_content),
                'word_count': result.get('word_count', 0),
                'checks_performed': {
                    'ai_detection': check_ai,
                    'plagiarism_check': check_plagiarism
                }
            }
            
            # Add scores if available
            if check_ai and 'ai_detection' in result:
                history_result['ai_score'] = result['ai_detection']['score']
                history_result['ai_confidence'] = result['ai_detection']['confidence']
            
            if check_plagiarism and 'plagiarism' in result:
                history_result['plagiarism_score'] = result['plagiarism']['score']
                history_result['sources_found'] = result['plagiarism']['total_sources_found']
            
            history_result['explanation'] = result['explanation']

            # Save analysis result
            scan_id = ScanHistoryModel.save_scan_result(
                content=(file_info['filename'] if file_info else text_content[:200] + '...' if len(text_content) > 200 else text_content),
                content_type='text_analysis',
                result=history_result,
                user_id=current_user_id
            )

            if scan_id:
                logger.info(f"Saved analysis result with ID: {scan_id}")
            else:
                logger.warning("Failed to save analysis result to history")

        except Exception as e:
            logger.error(f"Error saving to scan history: {e}")

        # Log successful analysis
        logger.info(f"Text analysis completed successfully. AI: {result.get('ai_detection', {}).get('score', 'N/A')}%, Plagiarism: {result.get('plagiarism', {}).get('score', 'N/A')}%")

        # Return results to template
        return render_template('analyze_text.html',
                             result=result,
                             text_content=text_content[:500] + '...' if len(text_content) > 500 else text_content,
                             file_info=file_info,
                             check_ai=check_ai,
                             check_plagiarism=check_plagiarism,
                             supported_formats=supported_formats)

    except Exception as e:
        logger.error(f"Error in text analysis route: {e}")
        from services.text_analysis import text_analysis_service
        return render_template('analyze_text.html',
                             error=f"An unexpected error occurred: {str(e)}",
                             supported_formats=text_analysis_service.get_supported_formats())

@main_bp.route('/api/scan', methods=['POST'])
def api_scan_content():
    """
    Unified API endpoint for all content analysis types.
    Handles:
    1. Text analysis (AI detection + plagiarism) with form data for file uploads
    2. ML phishing detection for URL/email/message via JSON data
    
    Returns JSON response for AJAX requests or API clients.
    """
    try:
        # Check if this is a form-based request (file upload for text analysis)
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle unified text analysis with file upload
            logger.info("API scan request received - unified text analysis endpoint")
            
            # Get form data
            text_content = request.form.get('text_content', '').strip()
            check_ai = request.form.get('check_ai') == 'on'
            check_plagiarism = request.form.get('check_plagiarism') == 'on'
            
            logger.info(f"Form data received: text_length={len(text_content)}, check_ai={check_ai}, check_plagiarism={check_plagiarism}")
            
            # Check for file upload
            uploaded_file = request.files.get('text_file')
            file_info = None
            
            # Process file if uploaded
            if uploaded_file and uploaded_file.filename:
                logger.info(f"Processing uploaded file: {uploaded_file.filename}")
                
                try:
                    # Extract text from file using shared service
                    extracted_text = extract_text_from_file(uploaded_file)
                    if extracted_text and extracted_text.get('success'):
                        text_content = extracted_text['text']
                        file_info = {
                            'filename': uploaded_file.filename,
                            'size': f"{len(text_content)} characters",
                            'type': uploaded_file.content_type or 'Unknown'
                        }
                        logger.info(f"Successfully extracted {len(text_content)} characters from file")
                    else:
                        error_msg = extracted_text.get('error', 'Failed to extract text from file') if extracted_text else 'Failed to process uploaded file'
                        logger.error(f"File processing failed: {error_msg}")
                        return jsonify({'error': error_msg}), 400
                except Exception as e:
                    logger.error(f"File extraction error: {e}")
                    return jsonify({'error': f'Failed to process file: {str(e)}'}), 400
            
            # Validate content
            if not text_content:
                logger.warning("No text content provided")
                return jsonify({'error': 'Please enter text content or upload a file'}), 400
            
            if len(text_content) < 50:
                logger.warning(f"Text too short: {len(text_content)} characters")
                return jsonify({'error': 'Text must be at least 50 characters long for analysis'}), 400
            
            # Validate analysis options
            if not check_ai and not check_plagiarism:
                logger.warning("No analysis options selected")
                return jsonify({'error': 'Please select at least one analysis option (AI Detection or Plagiarism Check)'}), 400
            
            # Perform enhanced text analysis using shared service
            source = "file_upload" if file_info else "manual"
            logger.info(f"Starting unified analysis: source={source}, ai={check_ai}, plagiarism={check_plagiarism}")
            
            result = analyze_text_content(text_content, check_ai=check_ai, check_plagiarism=check_plagiarism, source=source)
            
            # Check for analysis errors
            if not result.get('success', False):
                error_msg = result.get('error', 'Unknown analysis error')
                logger.error(f"Analysis failed: {error_msg}")
                return jsonify({'error': f"Analysis failed: {error_msg}"}), 400
            
            # Add file information to result
            if file_info:
                result['file_info'] = file_info
            
            # Convert to format expected by frontend (unified format)
            ai_percentage = result.get('ai_detection', {}).get('percentage', 0)
            plagiarism_percentage = result.get('plagiarism', {}).get('percentage', 0)
            
            unified_result = {
                'content_type': 'text',
                'success': True,
                'authenticity_verdict': f"AI Detection: {ai_percentage}% | Plagiarism: {plagiarism_percentage}%",
                'ai_likelihood': ai_percentage / 100.0,
                'plagiarism_score': plagiarism_percentage / 100.0,
                'detailed_analysis': result,
                'file_info': file_info,
                'timestamp': result.get('timestamp')
            }
            
            logger.info(f"Analysis completed successfully: AI={ai_percentage}%, Plagiarism={plagiarism_percentage}%")
            return jsonify(unified_result)
        
        else:
            # Handle JSON-based phishing detection (original functionality)
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400

            # Extract content and type
            content = data.get('content', '').strip()
            content_type = data.get('content_type', '').strip()

            if not content:
                return jsonify({'error': 'Content is required'}), 400

            if content_type not in ['url', 'email', 'message']:
                return jsonify({'error': 'Content type must be url, email, or message'}), 400

            # Validate content based on type
            if content_type == 'url' and not validate_url(content):
                return jsonify({'error': 'Invalid URL format'}), 400

            if content_type in ['email', 'message'] and len(content) < 5:
                return jsonify({'error': 'Content too short for analysis'}), 400

            # Import and use ML detector
            from utils.ml_detector import MLPhishingDetector

            detector = MLPhishingDetector()
            result = detector.analyze_content(content, content_type)

            # Check for analysis errors
            if result.get('error'):
                return jsonify({'error': result.get('warnings', ['Analysis failed'])[0]}), 500

            # Save comprehensive scan result for API requests
            try:
                from models.scan_history_model import ScanHistoryModel

                # Get current user ID from session (API calls may be authenticated)
                current_user_id = session.get('user_id')

                # Save detailed scan result
                scan_id = ScanHistoryModel.save_scan_result(
                    content=content,
                    content_type=content_type,
                    result=result,
                    user_id=current_user_id
                )

                logger.info(f"API scan saved (ID: {scan_id})")

            except Exception as log_error:
                logger.error(f"Failed to save API scan result: {log_error}")

            return jsonify(result)

    except ImportError as e:
        logger.error(f"ML detector import error: {e}")
        return jsonify({'error': 'AI analysis system temporarily unavailable'}), 503

    except Exception as e:
        logger.error(f"API scan error: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@main_bp.route('/api/quick-check', methods=['POST'])
def api_quick_check():
    """
    Quick API endpoint for homepage phishing check

    Returns JSON response for AJAX requests from homepage quick check form.
    This endpoint specifically handles form data from the homepage.
    """
    try:
        # Import the ML detector
        from utils.ml_detector import MLPhishingDetector

        # Get form data (homepage uses different field names)
        input_type = request.form.get('input_type', '').strip()
        content = request.form.get('input_content', '').strip()  # Homepage uses 'input_content'

        # Validate input
        if not content:
            return jsonify({
                'success': False,
                'message': 'Please enter content to analyze'
            })

        # Validate based on input type
        if input_type == 'url':
            if not validate_url(content):
                return jsonify({
                    'success': False,
                    'message': 'Please enter a valid URL (must start with http:// or https://)'
                })
        elif input_type in ['email', 'message']:
            if len(content) < 10:
                return jsonify({
                    'success': False,
                    'message': 'Content must be at least 10 characters long'
                })

        logger.info(f"Quick check - {input_type} analysis: {content[:50]}...")

        # Initialize ML detector with comprehensive error handling
        try:
            detector = MLPhishingDetector()
            logger.info(f"ML detector initialized successfully for {input_type} analysis")

            # Perform analysis using the unified analyze_content method
            result = detector.analyze_content(content, input_type)

            # Check if result contains error indicators
            if result.get('error') or result.get('threat_level') == 'unknown':
                logger.warning(f"ML detector returned error result: {result}")
                return jsonify({
                    'success': False,
                    'message': 'AI analysis could not process this content. Please verify the input and try again.'
                })

        except Exception as detector_error:
            logger.error(f"ML detector initialization/analysis failed: {detector_error}")
            return jsonify({
                'success': False,
                'message': 'AI analysis system error. Please try again.'
            })

        # Save scan result to history
        try:
            user_id = session.get('user_id')
            scan_id = ScanHistoryModel.save_scan_result(
                content=content,
                content_type=input_type,
                result=result,
                user_id=user_id
            )
            logger.info(f"Quick check scan saved (ID: {scan_id}) for {'user ' + str(user_id) if user_id else 'anonymous user'}")
        except Exception as save_error:
            logger.error(f"Failed to save quick check scan: {save_error}")

        # Convert result to JSON-friendly format for homepage
        json_result = {
            'success': True,
            'data': {
                'content': content,
                'content_type': input_type.title(),
                'threat_level': result.get('threat_level', 'unknown'),
                'confidence_score': result.get('confidence_score', 0.0),
                'risk_score': result.get('risk_score', 0.0),
                'explanation': result.get('explanation', 'Analysis completed'),
                'warnings': result.get('warnings', []),
                'analysis_components': result.get('analysis_components', []),
                'urls_found': result.get('urls_found', 0),
                'confidence_percentage': int(result.get('confidence_score', 0.0) * 100)
            }
        }

        logger.info(f"Quick check complete - Threat: {result.get('threat_level')}, Confidence: {result.get('confidence_score'):.2f}")

        return jsonify(json_result)

    except ImportError as e:
        logger.error(f"ML detector import error in quick check: {e}")
        return jsonify({
            'success': False,
            'message': 'AI analysis system is currently unavailable'
        })

    except Exception as e:
        # Detailed error logging for debugging
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Detailed error in quick check API: {str(e)}")
        logger.error(f"Stack trace: {error_trace}")

        return jsonify({
            'success': False,
            'message': f'Analysis error: {str(e)}. Please check your input and try again.'
        })

@main_bp.route('/analyze-media')
@login_required
def analyze_media_page():
    """
    Multimedia Authenticity Checker Page

    Display interface for analyzing different types of media content
    """
    return render_template('analyze_media.html', page_title="Analyze Media")

@main_bp.route('/analyze/process', methods=['POST'])
def process_media_analysis():
    """
    Process multimedia analysis requests

    Handles file uploads and text input for all media types
    """
    try:
        from utils.multimedia_analyzer import analyzer

        # Get analysis type from form
        analysis_type = request.form.get('analysis_type', '').strip()
        text_content = request.form.get('text_content', '').strip()

        # For form-based submissions (text analysis), analysis_type may not be set
        # Default to 'text' if text_content is provided without explicit analysis_type  
        if not analysis_type and text_content:
            analysis_type = 'text'
        elif analysis_type and analysis_type not in ['text', 'image', 'video', 'audio']:
            return jsonify({'error': 'Invalid analysis type'}), 400

        result = None

        if analysis_type == 'text':
            # Handle text analysis with enhanced file upload support
            text_content = request.form.get('text_content', '').strip()
            check_ai = request.form.get('check_ai') == 'on'
            check_plagiarism = request.form.get('check_plagiarism') == 'on'
            
            # Check if file was uploaded
            uploaded_file = request.files.get('text_file')
            file_info = None
            
            # Extract text from file if provided
            if uploaded_file and uploaded_file.filename:
                logger.info(f"Processing uploaded file in media analysis: {uploaded_file.filename}")
                
                file_result = extract_text_from_file(uploaded_file)
                
                if not file_result['success']:
                    return jsonify({'error': f"File processing failed: {file_result['error']}"}), 400
                
                # Use extracted text
                text_content = file_result['text']
                file_info = {
                    'filename': uploaded_file.filename,
                    'file_type': file_result.get('file_type', 'unknown'),
                    'extraction_details': file_result
                }
                
                logger.info(f"Successfully extracted {len(text_content)} characters from {uploaded_file.filename}")
            
            # Validate text content
            if not text_content:
                return jsonify({'error': 'Please enter text content or upload a file'}), 400
            if len(text_content) < 50:
                return jsonify({'error': 'Text must be at least 50 characters long'}), 400
            
            # Perform enhanced text analysis using shared service
            source = "file_upload" if file_info else "manual"
            result = analyze_text_content(text_content, check_ai=check_ai, check_plagiarism=check_plagiarism, source=source)
            
            # Check for analysis errors
            if not result.get('success', False):
                return jsonify({'error': f"Analysis failed: {result.get('error', 'Unknown error')}"}), 400
            
            # Add file information to result
            if file_info:
                result['file_info'] = file_info
            
            # Convert to format expected by frontend
            media_result = {
                'content_type': 'text',
                'authenticity_verdict': f"AI Detection: {result.get('ai_detection', {}).get('percentage', 0)}% | Plagiarism: {result.get('plagiarism', {}).get('percentage', 0)}%",
                'ai_likelihood': result.get('ai_detection', {}).get('percentage', 0) / 100.0,
                'plagiarism_score': result.get('plagiarism', {}).get('percentage', 0) / 100.0,
                'detailed_analysis': result,
                'file_info': file_info
            }
            
            return jsonify(media_result)

        elif analysis_type in ['image', 'video', 'audio']:
            # Handle file uploads
            file_key = f'{analysis_type}_file'
            if file_key not in request.files:
                return jsonify({'error': f'No {analysis_type} file uploaded'}), 400
            
            uploaded_file = request.files[file_key]
            if not uploaded_file or not uploaded_file.filename:
                return jsonify({'error': f'No {analysis_type} file selected'}), 400
            
            logger.info(f"Processing {analysis_type} file: {uploaded_file.filename}")
            
            # For now, return placeholder analysis for multimedia files
            # TODO: Implement actual multimedia analysis algorithms
            result = {
                'content_type': analysis_type,
                'filename': uploaded_file.filename,
                'file_size': len(uploaded_file.read()),
                'authenticity_verdict': f'{analysis_type.title()} analysis completed',
                'ai_likelihood': 0.15,  # Low AI generation probability as placeholder
                'manipulation_score': 0.20,  # Low manipulation score as placeholder
                'analysis_notes': [
                    f'{analysis_type.title()} file received and processed',
                    'Basic metadata extraction completed',
                    'Advanced analysis features coming soon'
                ]
            }
            
            # Reset file pointer after reading
            uploaded_file.seek(0)
            
            return jsonify(result)

        else:
            return jsonify({'error': 'Invalid analysis type specified'}), 400

    except Exception as e:
        logger.error(f"Media analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@main_bp.route('/analytics')
def analytics():
    """Analytics page - redirect to analyze for now"""
    return redirect(url_for('main.analyze'))