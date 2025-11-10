"""
PDF Text Extraction Module
Extracts text, metadata, and structure from PDF documents
"""

import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class PDFContent:
    """Container for extracted PDF content"""
    text: str
    metadata: Dict
    pages: List[str]
    num_pages: int
    sentences: List[str]
    paragraphs: List[str]
    citations: List[str]
    references: List[str]


class PDFExtractor:
    """Advanced PDF text extraction with structure preservation"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.content = None
        
    def extract(self) -> PDFContent:
        """Extract all content from PDF"""
        print(f"Extracting content from: {self.pdf_path}")
        
        # Try multiple extraction methods for best results
        text = self._extract_with_pdfplumber()
        if not text or len(text.strip()) < 100:
            text = self._extract_with_pymupdf()
        if not text or len(text.strip()) < 100:
            text = self._extract_with_pypdf2()
            
        # Extract metadata
        metadata = self._extract_metadata()
        
        # Extract pages
        pages = self._extract_pages()
        
        # Process text structure
        sentences = self._extract_sentences(text)
        paragraphs = self._extract_paragraphs(text)
        
        # Identify citations and references
        citations = self._extract_citations(text)
        references = self._extract_references(text)
        
        self.content = PDFContent(
            text=text,
            metadata=metadata,
            pages=pages,
            num_pages=len(pages),
            sentences=sentences,
            paragraphs=paragraphs,
            citations=citations,
            references=references
        )
        
        return self.content
    
    def _extract_with_pdfplumber(self) -> str:
        """Extract text using pdfplumber (best for structured PDFs)"""
        try:
            text = ""
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            return text.strip()
        except Exception as e:
            print(f"PDFPlumber extraction failed: {e}")
            return ""
    
    def _extract_with_pymupdf(self) -> str:
        """Extract text using PyMuPDF (best for complex PDFs)"""
        try:
            text = ""
            doc = fitz.open(self.pdf_path)
            for page in doc:
                text += page.get_text() + "\n\n"
            doc.close()
            return text.strip()
        except Exception as e:
            print(f"PyMuPDF extraction failed: {e}")
            return ""
    
    def _extract_with_pypdf2(self) -> str:
        """Extract text using PyPDF2 (fallback method)"""
        try:
            text = ""
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"
            return text.strip()
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
            return ""
    
    def _extract_metadata(self) -> Dict:
        """Extract PDF metadata"""
        metadata = {}
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                info = pdf_reader.metadata
                if info:
                    metadata = {
                        'title': info.get('/Title', ''),
                        'author': info.get('/Author', ''),
                        'subject': info.get('/Subject', ''),
                        'creator': info.get('/Creator', ''),
                        'producer': info.get('/Producer', ''),
                        'creation_date': info.get('/CreationDate', ''),
                        'modification_date': info.get('/ModDate', '')
                    }
        except Exception as e:
            print(f"Metadata extraction failed: {e}")
        
        return metadata
    
    def _extract_pages(self) -> List[str]:
        """Extract text from each page separately"""
        pages = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages.append(page_text)
        except Exception as e:
            print(f"Page extraction failed: {e}")
        
        return pages
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting (will be enhanced with NLTK later)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences
    
    def _extract_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 20]
        return paragraphs
    
    def _extract_citations(self, text: str) -> List[str]:
        """Identify in-text citations"""
        citations = []
        
        # Pattern for (Author, Year) citations
        pattern1 = r'\([A-Z][a-z]+(?:\s+(?:et\s+al\.|&|and)\s+[A-Z][a-z]+)?,\s+\d{4}\)'
        citations.extend(re.findall(pattern1, text))
        
        # Pattern for [Number] citations
        pattern2 = r'\[\d+\]'
        citations.extend(re.findall(pattern2, text))
        
        # Pattern for Author (Year) citations
        pattern3 = r'[A-Z][a-z]+(?:\s+(?:et\s+al\.|&|and)\s+[A-Z][a-z]+)?\s+\(\d{4}\)'
        citations.extend(re.findall(pattern3, text))
        
        return list(set(citations))
    
    def _extract_references(self, text: str) -> List[str]:
        """Extract reference section"""
        references = []
        
        # Look for References or Bibliography section
        ref_pattern = r'(?:References|Bibliography|Works\s+Cited)\s*\n+(.*?)(?:\n\n\n|$)'
        ref_match = re.search(ref_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if ref_match:
            ref_section = ref_match.group(1)
            # Split by line breaks and filter
            ref_lines = ref_section.split('\n')
            references = [line.strip() for line in ref_lines if len(line.strip()) > 20]
        
        return references
    
    def get_text_statistics(self) -> Dict:
        """Calculate text statistics"""
        if not self.content:
            return {}
        
        words = self.content.text.split()
        
        return {
            'total_pages': self.content.num_pages,
            'total_characters': len(self.content.text),
            'total_words': len(words),
            'total_sentences': len(self.content.sentences),
            'total_paragraphs': len(self.content.paragraphs),
            'citations_found': len(self.content.citations),
            'references_found': len(self.content.references),
            'avg_words_per_page': len(words) / max(self.content.num_pages, 1)
        }


if __name__ == "__main__":
    # Test the extractor
    import sys
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        extractor = PDFExtractor(pdf_path)
        content = extractor.extract()
        stats = extractor.get_text_statistics()
        
        print("\n=== PDF Statistics ===")
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        print(f"\n=== First 500 characters ===")
        print(content.text[:500])
    else:
        print("Usage: python pdf_extractor.py <pdf_file>")
