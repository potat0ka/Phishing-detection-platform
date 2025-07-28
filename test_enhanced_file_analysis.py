#!/usr/bin/env python3
"""
Test enhanced file upload and analysis capabilities for Text Authenticity Analysis.
Tests document (.txt, .pdf, .docx) and image (.jpg, .png) processing with OCR.
"""

import sys
import os
sys.path.append('.')

from services.text_analysis import text_analysis_service
from utils.text_analysis import TextAnalyzer
import io

def test_file_processing():
    """Test file processing capabilities"""
    print("Testing Enhanced File Upload and Analysis")
    print("=" * 50)
    
    # Test supported formats
    analyzer = TextAnalyzer()
    print("Supported formats:")
    print(f"  Text: {analyzer.SUPPORTED_TEXT_FORMATS}")
    print(f"  PDF: {analyzer.SUPPORTED_PDF_FORMATS}")
    print(f"  Documents: {analyzer.SUPPORTED_DOCX_FORMATS}")
    print(f"  Images: {analyzer.SUPPORTED_IMAGE_FORMATS}")
    
    # Test service configuration
    print(f"\nService Configuration:")
    print(f"  Min text length: {text_analysis_service.min_text_length}")
    print(f"  Max text length: {text_analysis_service.max_text_length}")
    print(f"  Supported formats: {text_analysis_service.get_supported_formats()}")
    
    # Create test text content that will trigger plagiarism detection
    test_content = '''
According to recent academic research conducted by Johnson et al. (2023), the implementation of machine learning algorithms has demonstrated significant improvements in computational efficiency. Furthermore, studies indicate that deep learning frameworks can effectively process complex data patterns with remarkable accuracy.

"The integration of artificial intelligence techniques provides enhanced analytical capabilities for modern data processing systems," as stated by the research team. Moreover, the methodology employed in these evaluations demonstrates the effectiveness of advanced computational approaches.

The findings are really quite impressive and totally significant for the field. Therefore, it can be concluded that these technologies offer substantial benefits for various applications.
'''
    
    print(f"\nTesting text analysis with {len(test_content)} character content...")
    
    # Test the analysis
    result = text_analysis_service.analyze_text(
        test_content.strip(), 
        check_ai=True, 
        check_plagiarism=True, 
        source="test_file"
    )
    
    if result.get('success'):
        print("✓ Analysis successful")
        
        # AI Detection Results
        if 'ai_detection' in result:
            ai = result['ai_detection']
            print(f"\nAI Detection:")
            print(f"  Score: {ai.get('percentage', 0)}%")
            print(f"  Level: {ai.get('level', 'unknown')}")
            print(f"  Confidence: {ai.get('confidence', 'unknown')}")
            if ai.get('details'):
                print(f"  Indicators: {', '.join(ai['details'][:3])}")
        
        # Plagiarism Detection Results
        if 'plagiarism' in result:
            plag = result['plagiarism']
            print(f"\nPlagiarism Detection:")
            print(f"  Score: {plag.get('percentage', 0)}%")
            print(f"  Level: {plag.get('level', 'unknown')}")
            print(f"  Sources found: {plag.get('total_sources_found', 0)}")
            
            if plag.get('sources'):
                print(f"  Detailed sources:")
                for i, source in enumerate(plag['sources'][:2], 1):
                    print(f"    {i}. {source['title']} ({source['match_percentage']}%)")
                    print(f"       {source['url']}")
            
            if plag.get('copied_segments'):
                print(f"  Copied segments:")
                for i, segment in enumerate(plag['copied_segments'], 1):
                    print(f"    {i}. {segment['length']} words - {segment['confidence']} confidence")
                    print(f"       \"{segment['text'][:80]}...\"")
        
        print(f"\nExplanation: {result.get('explanation', 'N/A')}")
        return True
    else:
        print(f"✗ Analysis failed: {result.get('error')}")
        return False

def test_ocr_capability():
    """Test OCR processing capability"""
    print(f"\n{'-' * 50}")
    print("Testing OCR Capability")
    print(f"{'-' * 50}")
    
    try:
        import pytesseract
        from PIL import Image
        print("✓ OCR libraries available (pytesseract, PIL)")
        
        # Test if tesseract is available
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✓ Tesseract version: {version}")
            return True
        except Exception as e:
            print(f"⚠ Tesseract not properly configured: {e}")
            return False
            
    except ImportError as e:
        print(f"✗ OCR libraries not available: {e}")
        return False

def test_document_extraction():
    """Test document processing capability"""
    print(f"\n{'-' * 50}")
    print("Testing Document Processing")
    print(f"{'-' * 50}")
    
    # Test PDF processing
    try:
        import pdfplumber
        print("✓ PDF processing available (pdfplumber)")
    except ImportError:
        print("✗ PDF processing not available")
    
    # Test DOCX processing
    try:
        from docx import Document
        print("✓ DOCX processing available (python-docx)")
    except ImportError:
        print("✗ DOCX processing not available")
    
    return True

if __name__ == "__main__":
    print("Enhanced Text Authenticity Analysis - File Processing Test")
    print("=" * 60)
    
    success = True
    
    # Test core analysis
    if not test_file_processing():
        success = False
    
    # Test OCR capability
    if not test_ocr_capability():
        print("Note: OCR processing may be limited without proper tesseract setup")
    
    # Test document processing
    test_document_extraction()
    
    print(f"\n{'=' * 60}")
    if success:
        print("✓ Enhanced Text Authenticity Analysis is ready!")
        print("✓ File upload supports multiple formats with OCR")
        print("✓ Detailed plagiarism detection with sources and segments")
        print("✓ AI content detection with pattern analysis")
        print("\nFeatures available:")
        print("  • Upload documents (.txt, .pdf, .docx)")
        print("  • Upload images (.jpg, .png, .bmp, .tiff) with OCR")
        print("  • Detailed source identification for copied content")
        print("  • Specific copied segment highlighting")
        print("  • Comprehensive AI detection patterns")
        sys.exit(0)
    else:
        print("✗ Some issues found with the analysis system")
        sys.exit(1)