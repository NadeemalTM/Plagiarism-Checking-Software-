"""
Setup script to download and configure NLTK data
Run this once after installing dependencies
"""

import nltk
import ssl

def setup_nltk():
    """Download required NLTK data packages"""
    
    print("Setting up NLTK data...")
    print("This is a one-time setup process.\n")
    
    # Handle SSL certificate issues
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # List of required NLTK data packages
    packages = [
        ('punkt', 'Punkt Tokenizer'),
        ('stopwords', 'Stopwords'),
        ('averaged_perceptron_tagger', 'POS Tagger'),
        ('maxent_ne_chunker', 'Named Entity Chunker'),
        ('words', 'Word Lists')
    ]
    
    print("Downloading NLTK packages...\n")
    
    for package, description in packages:
        try:
            print(f"Downloading {description} ({package})...", end=' ')
            nltk.download(package, quiet=True)
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("NLTK setup complete!")
    print("="*60)
    print("\nYou can now run the plagiarism checker:")
    print("  python plagiarism_checker.py --file your_document.pdf")
    print()


if __name__ == "__main__":
    setup_nltk()
