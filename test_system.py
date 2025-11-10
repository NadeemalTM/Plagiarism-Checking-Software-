"""
Test suite for the plagiarism checker
Run tests to verify installation and functionality
"""

import os
import sys
from io import StringIO

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing module imports...")
    
    modules = [
        ('PyPDF2', 'PyPDF2'),
        ('pdfplumber', 'pdfplumber'),
        ('fitz', 'PyMuPDF'),
        ('nltk', 'NLTK'),
        ('sklearn', 'scikit-learn'),
        ('numpy', 'NumPy'),
        ('simhash', 'simhash'),
        ('jinja2', 'Jinja2'),
    ]
    
    failed = []
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {display_name}")
        except ImportError as e:
            print(f"  ✗ {display_name} - {e}")
            failed.append(display_name)
    
    if failed:
        print(f"\n⚠️  Missing modules: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All required modules are installed!")
        return True


def test_nltk_data():
    """Test if NLTK data is downloaded"""
    print("\nTesting NLTK data...")
    
    import nltk
    
    resources = [
        ('tokenizers/punkt', 'Punkt Tokenizer'),
        ('corpora/stopwords', 'Stopwords'),
    ]
    
    failed = []
    for resource, name in resources:
        try:
            nltk.data.find(resource)
            print(f"  ✓ {name}")
        except LookupError:
            print(f"  ✗ {name}")
            failed.append(name)
    
    if failed:
        print(f"\n⚠️  Missing NLTK data: {', '.join(failed)}")
        print("Run: python setup_nltk.py")
        return False
    else:
        print("\n✓ All NLTK data is available!")
        return True


def test_modules():
    """Test custom modules"""
    print("\nTesting custom modules...")
    
    modules = [
        'pdf_extractor',
        'plagiarism_detector',
        'copyright_detector',
        'report_generator'
    ]
    
    failed = []
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name}.py")
        except Exception as e:
            print(f"  ✗ {module_name}.py - {e}")
            failed.append(module_name)
    
    if failed:
        print(f"\n⚠️  Failed to load: {', '.join(failed)}")
        return False
    else:
        print("\n✓ All custom modules loaded successfully!")
        return True


def test_basic_functionality():
    """Test basic functionality with sample data"""
    print("\nTesting basic functionality...")
    
    try:
        from pdf_extractor import PDFExtractor
        from plagiarism_detector import PlagiarismDetector
        from copyright_detector import CopyrightDetector
        
        # Test plagiarism detector
        detector = PlagiarismDetector()
        detector.add_reference_document(
            "This is a test document for verification.",
            {'title': 'Test', 'url': ''}
        )
        
        test_text = "This is a test document for verification."
        test_sentences = ["This is a test document for verification."]
        
        result = detector.detect(test_text, test_sentences)
        
        print(f"  ✓ Plagiarism detection works")
        print(f"    - Found {len(result.matches)} matches")
        
        # Test copyright detector
        copyright_detector = CopyrightDetector()
        copyright_text = "Copyright © 2024 Test Corp. All rights reserved."
        copyright_report = copyright_detector.analyze(copyright_text, [])
        
        print(f"  ✓ Copyright detection works")
        print(f"    - Found {copyright_report.total_copyrighted_content} items")
        
        print("\n✓ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("PLAGIARISM CHECKER - TEST SUITE")
    print("="*60)
    print()
    
    results = []
    
    results.append(("Import Test", test_imports()))
    results.append(("NLTK Data Test", test_nltk_data()))
    results.append(("Custom Modules Test", test_modules()))
    results.append(("Functionality Test", test_basic_functionality()))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✓ All tests passed! The system is ready to use.")
        print("\nRun the plagiarism checker:")
        print("  python plagiarism_checker.py --file your_document.pdf")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
