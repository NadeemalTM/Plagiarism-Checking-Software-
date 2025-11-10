# Installation and Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 500MB free disk space for libraries and models

## Step-by-Step Installation

### 1. Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This will install all required packages including:
- PDF processing libraries (PyPDF2, pdfplumber, PyMuPDF)
- NLP libraries (NLTK, spaCy, sentence-transformers)
- Text analysis tools
- Reporting libraries

### 2. Download NLP Models

#### Download NLTK Data

Run Python and execute:

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

Or run the setup script:

```powershell
python setup_nltk.py
```

#### Download spaCy Model (Optional but recommended)

```powershell
python -m spacy download en_core_web_sm
```

### 3. Verify Installation

Test the installation:

```powershell
python plagiarism_checker.py --help
```

You should see the help menu with all available options.

## Quick Start

### Basic Usage

1. **Check a single PDF file:**

```powershell
python plagiarism_checker.py --file "your_document.pdf"
```

2. **Generate HTML report:**

```powershell
python plagiarism_checker.py --file "your_document.pdf" --format html --output report.html
```

3. **Compare against reference documents:**

```powershell
python plagiarism_checker.py --file "your_document.pdf" --references reference1.pdf reference2.pdf
```

### Advanced Usage

4. **Enable web search (slower but more comprehensive):**

```powershell
python plagiarism_checker.py --file "your_document.pdf" --web-search
```

5. **Adjust similarity threshold:**

```powershell
python plagiarism_checker.py --file "your_document.pdf" --threshold 0.8
```

6. **Export as JSON for further processing:**

```powershell
python plagiarism_checker.py --file "your_document.pdf" --format json --output results.json
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Reinstall requirements
```powershell
pip install --upgrade -r requirements.txt
```

### Issue: PDF extraction fails

**Solution:** The system tries multiple extraction methods. If all fail:
- Ensure the PDF is not encrypted
- Check if the PDF is text-based (not scanned images)
- Try converting to a different PDF format

### Issue: Out of memory errors

**Solution:** 
- Process smaller PDFs
- Reduce the number of reference documents
- Close other applications

### Issue: Slow performance

**Solution:**
- Disable web search (`--web-search` flag)
- Reduce reference documents
- Use a machine with more RAM

## System Requirements

- **Minimum:**
  - CPU: Dual-core 2.0 GHz
  - RAM: 4 GB
  - Storage: 1 GB free space

- **Recommended:**
  - CPU: Quad-core 2.5 GHz or better
  - RAM: 8 GB or more
  - Storage: 2 GB free space
  - SSD for faster processing

## Support

For issues, questions, or contributions:
1. Check this documentation
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify Python version compatibility

## Next Steps

After installation:
1. Test with a sample PDF document
2. Review the generated report
3. Adjust settings based on your needs
4. Explore advanced features
