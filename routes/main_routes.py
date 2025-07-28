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
from datetime import datetime
from models import PhishingModel, SecurityTipsModel, AnalyticsModel
from models.scan_history_model import ScanHistoryModel
from utils.phishing_detector import PhishingDetector
from utils.validation import validate_url
import logging
import os

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
        featured_tip = SecurityTipsModel.get_featured_tip()

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

        # Initialize ML detector and analyze content
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
    Text Analysis page for plagiarism and AI detection

    GET: Show the text analysis form
    POST: Process text and return analysis results
    """
    if request.method == 'GET':
        return render_template('analyze_text.html')

    try:
        # Import the text analyzer
        from utils.text_analysis import TextAnalyzer

        # Get form data
        text_content = request.form.get('text_content', '').strip()
        check_plagiarism = request.form.get('check_plagiarism') == 'on'
        check_ai = request.form.get('check_ai') == 'on'

        # Validate input
        if not text_content:
            return render_template('analyze_text.html', 
                                 error="Please enter text content to analyze")

        if len(text_content) < 50:
            return render_template('analyze_text.html',
                                 error="Text must be at least 50 characters long")

        if len(text_content) > 50000:
            return render_template('analyze_text.html',
                                 error="Text must be less than 50,000 characters")

        # Ensure at least one analysis type is selected
        if not check_plagiarism and not check_ai:
            return render_template('analyze_text.html',
                                 error="Please select at least one analysis type")

        logger.info(f"Starting text analysis: {len(text_content)} characters")

        # Initialize text analyzer and perform analysis
        analyzer = TextAnalyzer()
        result = analyzer.analyze_text(text_content)

        # Check for analysis errors
        if result.get('error'):
            logger.error(f"Text analyzer error: {result.get('explanation', 'Unknown error')}")
            return render_template('analyze_text.html',
                                 error=f"Analysis failed: {result.get('explanation', 'Unknown error')}")

        # Save analysis result to user history if logged in
        try:
            from models.scan_history_model import ScanHistoryModel

            # Get current user ID from session
            current_user_id = session.get('user_id')

            # Create a simplified result for history
            history_result = {
                'analysis_type': 'text_analysis',
                'plagiarism_score': result['plagiarism']['score'],
                'ai_score': result['ai_detection']['score'],
                'explanation': result['explanation']
            }

            # Save analysis result
            scan_id = ScanHistoryModel.save_scan_result(
                content=text_content[:200] + '...' if len(text_content) > 200 else text_content,
                content_type='text_analysis',
                result=history_result,
                user_id=current_user_id
            )

            # Log success with context
            user_context = f"user {current_user_id}" if current_user_id else "anonymous user"
            logger.info(f"Text analysis saved (ID: {scan_id}) for {user_context}")

            # Update system-wide analytics
            AnalyticsModel.update_scan_count()

        except Exception as log_error:
            logger.error(f"Failed to save text analysis result: {log_error}")

        logger.info(f"Text analysis complete - Plagiarism: {result['plagiarism']['score']:.2f}, AI: {result['ai_detection']['score']:.2f}")

        return render_template('analyze_text.html', result=result)

    except ImportError as e:
        logger.error(f"Text analyzer import error: {e}")
        return render_template('analyze_text.html',
                             error="Text analysis system is currently unavailable. Please try again later.")

    except Exception as e:
        logger.error(f"Error processing text analysis: {str(e)}")
        return render_template('analyze_text.html',
                             error=f"Analysis error: {str(e)}. Please check your input and try again.")

@main_bp.route('/api/scan', methods=['POST'])
def api_scan_content():
    """
    API endpoint for content scanning (URL, Email, or Message)

    Returns JSON response for AJAX requests or API clients.
    Supports all three content types with comprehensive ML analysis.
    """
    try:
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

@main_bp.route('/analyze')
def analyze_media():
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

        if analysis_type not in ['text', 'image', 'video', 'audio']:
            return jsonify({'error': 'Invalid analysis type'}), 400

        result = None

        if analysis_type == 'text':
            # Handle text analysis
            text_content = request.form.get('text_content', '').strip()
            if not text_content:
                return jsonify({'error': 'Please enter text content'}), 400
            if len(text_content) < 10:
                return jsonify({'error': 'Text must be at least 10 characters long'}), 400

            result = analyzer.analyze_content('text', text_content)

        elif analysis_type in ['image', 'video', 'audio']:
            # Handle file uploads
            file_key = f'{analysis_type}_file'
            if file_key not in request.files:
                return jsonify({'error': f'No {analysis_type} file uploaded'}), 400

            file = request.files[file_key]
            if file.filename == '':
                return jsonify({'error': f'No {analysis_type} file selected'}), 400

            # Validate file type
            allowed_extensions = {
                'image': ['.jpg', '.jpeg', '.png', '.gif'],
                'video': ['.mp4', '.avi', '.mov', '.mkv'],
                'audio': ['.mp3', '.wav', '.m4a', '.ogg']
            }

            filename = file.filename or ''
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in allowed_extensions[analysis_type]:
                return jsonify({'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions[analysis_type])}'}), 400

            # Check file size (30MB limit)
            file_data = file.read()
            if len(file_data) > 30 * 1024 * 1024:
                return jsonify({'error': 'File too large. Maximum size: 30MB'}), 400

            result = analyzer.analyze_content(analysis_type, file_data, filename)

        if result and 'error' not in result:
            # Save analysis result to history
            try:
                from models.scan_history_model import ScanHistoryModel

                user_id = session.get('user_id')
                scan_id = ScanHistoryModel.save_scan_result(
                    content=f"{analysis_type} analysis",
                    content_type=f'multimedia_{analysis_type}',
                    result=result,
                    user_id=user_id
                )
                logger.info(f"Multimedia analysis saved (ID: {scan_id})")
            except Exception as save_error:
                logger.error(f"Failed to save multimedia analysis: {save_error}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Media analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@main_bp.route('/analytics')
def analytics():
    """Analytics page - redirect to analyze for now"""
    return redirect(url_for('main.analyze'))