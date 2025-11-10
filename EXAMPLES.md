# Usage Examples

## Basic Examples

### 1. Check a Single PDF Document

```powershell
python plagiarism_checker.py --file "research_paper.pdf"
```

**Output:**
- Console summary showing plagiarism percentage
- Detailed text report
- List of matched sources
- Copyright content analysis

---

### 2. Generate HTML Report

```powershell
python plagiarism_checker.py --file "thesis.pdf" --format html --output "thesis_report.html"
```

**Result:**
- Beautiful HTML report with charts
- Color-coded matches
- Interactive source listings
- Can be opened in any web browser

---

### 3. Compare Against Reference Documents

```powershell
python plagiarism_checker.py --file "student_essay.pdf" --references "textbook.pdf" "lecture_notes.pdf"
```

**Use Case:**
- Teachers checking student submissions
- Comparing against specific sources
- Institutional document comparison

---

## Advanced Examples

### 4. Comprehensive Analysis with All Features

```powershell
python plagiarism_checker.py --file "document.pdf" --references ref1.pdf ref2.pdf ref3.pdf --web-search --format html --output detailed_report.html
```

**Features Used:**
- Multi-reference comparison
- Web search enabled
- HTML report generation
- Complete analysis

---

### 5. Batch Processing Multiple Documents

Create a PowerShell script `check_batch.ps1`:

```powershell
# Check all PDFs in a folder
Get-ChildItem ".\documents\*.pdf" | ForEach-Object {
    $outputFile = ".\reports\$($_.BaseName)_report.html"
    python plagiarism_checker.py --file $_.FullName --format html --output $outputFile
    Write-Host "Processed: $($_.Name)"
}
```

Run it:
```powershell
.\check_batch.ps1
```

---

### 6. Export Results as JSON

```powershell
python plagiarism_checker.py --file "data.pdf" --format json --output "results.json"
```

**JSON Output Includes:**
- Plagiarism percentage
- All matches with similarity scores
- Source information
- Copyright details
- Statistics

**Use Case:**
- Integration with other systems
- Automated workflows
- Data analysis
- API responses

---

### 7. Academic Paper Check

```powershell
python plagiarism_checker.py --file "research_paper.pdf" --references "literature_review.pdf" --threshold 0.8 --format markdown --output "review.md"
```

**Settings Explained:**
- `--threshold 0.8`: Higher threshold (stricter matching)
- `--format markdown`: Markdown for documentation
- Perfect for academic review processes

---

### 8. Silent Mode (No Console Summary)

```powershell
python plagiarism_checker.py --file "document.pdf" --no-summary --output "report.txt"
```

**Use Case:**
- Automated scripts
- Batch processing
- Integration with CI/CD pipelines

---

## Real-World Scenarios

### Scenario 1: Student Submission Check

**Context:** Teacher checking 30 student essays

```powershell
# Create a directory structure
# .\submissions\     (student PDFs)
# .\reports\         (output reports)
# .\references\      (course materials)

# Process all submissions
$references = Get-ChildItem ".\references\*.pdf" | ForEach-Object { $_.FullName }

Get-ChildItem ".\submissions\*.pdf" | ForEach-Object {
    $student = $_.BaseName
    $reportPath = ".\reports\${student}_report.html"
    
    python plagiarism_checker.py `
        --file $_.FullName `
        --references @references `
        --format html `
        --output $reportPath
    
    Write-Host "✓ Checked: $student"
}

Write-Host "`nAll submissions checked! See .\reports\ for results."
```

---

### Scenario 2: Corporate Document Review

**Context:** Checking internal documents for copyright issues

```powershell
python plagiarism_checker.py `
    --file "company_whitepaper.pdf" `
    --format html `
    --output "compliance_report.html" `
    --threshold 0.85
```

Review the copyright section of the report for:
- Copyright notices
- Trademark usage
- License compliance
- Quoted content

---

### Scenario 3: Research Publication Pre-Check

**Context:** Before submitting to a journal

```powershell
# Comprehensive check
python plagiarism_checker.py `
    --file "manuscript.pdf" `
    --web-search `
    --format html `
    --output "pre_submission_check.html"
```

**Benefits:**
- Catches unintentional plagiarism
- Identifies missing citations
- Detects copyright issues
- Ensures originality

---

## Integration Examples

### Python Script Integration

```python
from plagiarism_checker import PlagiarismChecker

# Initialize
checker = PlagiarismChecker(enable_web_search=False)

# Check file
results = checker.check_file(
    pdf_path="document.pdf",
    reference_paths=["ref1.pdf", "ref2.pdf"]
)

# Get plagiarism percentage
plag_pct = results['plagiarism_result'].plagiarism_percentage

# Make decision
if plag_pct > 30:
    print("Document rejected - high plagiarism")
elif plag_pct > 15:
    print("Document needs review")
else:
    print("Document accepted")

# Generate report
report = checker.generate_report(
    results,
    format='html',
    output_path='result.html'
)
```

---

### Web API Integration (Flask Example)

```python
from flask import Flask, request, jsonify
from plagiarism_checker import PlagiarismChecker
import tempfile
import os

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check_plagiarism():
    # Get uploaded file
    pdf_file = request.files['file']
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        pdf_file.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        # Run check
        checker = PlagiarismChecker()
        results = checker.check_file(tmp_path)
        
        # Return JSON
        return jsonify({
            'plagiarism_percentage': results['plagiarism_result'].plagiarism_percentage,
            'status': 'complete',
            'matches': len(results['plagiarism_result'].matches)
        })
    finally:
        os.unlink(tmp_path)

if __name__ == '__main__':
    app.run(port=5000)
```

---

## Tips and Best Practices

1. **For Large Documents:**
   ```powershell
   # Use without web search for faster processing
   python plagiarism_checker.py --file large_doc.pdf --no-summary
   ```

2. **For Maximum Accuracy:**
   ```powershell
   # Include all available references and enable web search
   python plagiarism_checker.py --file doc.pdf --references *.pdf --web-search
   ```

3. **For Regular Monitoring:**
   - Set up scheduled tasks in Windows
   - Use batch scripts
   - Generate JSON for tracking over time

4. **For Best Reports:**
   - Use HTML format for stakeholders
   - Use JSON for data processing
   - Use Markdown for documentation
   - Use Text for quick reviews
