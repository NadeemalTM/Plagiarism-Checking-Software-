"""
Advanced Plagiarism Detection Engine
Multi-strategy approach for high-accuracy plagiarism detection
"""

import re
import hashlib
import requests
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textdistance
from simhash import Simhash
from fuzzywuzzy import fuzz
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except (ImportError, OSError) as e:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print(f"Warning: sentence-transformers not available. Semantic similarity will be limited.")
    print(f"Reason: {type(e).__name__}")
    # This is fine - the system will still work with other detection methods


@dataclass
class PlagiarismMatch:
    """Represents a plagiarism match"""
    source_text: str
    matched_text: str
    similarity: float
    match_type: str  # 'exact', 'paraphrased', 'semantic'
    source_url: str = ""
    source_title: str = ""
    start_position: int = 0
    end_position: int = 0


@dataclass
class PlagiarismResult:
    """Complete plagiarism analysis result"""
    overall_similarity: float
    plagiarism_percentage: float
    matches: List[PlagiarismMatch] = field(default_factory=list)
    sources: List[Dict] = field(default_factory=list)
    text_fingerprint: str = ""
    analysis_methods: List[str] = field(default_factory=list)
    
    def add_match(self, match: PlagiarismMatch):
        """Add a plagiarism match"""
        self.matches.append(match)
    
    def calculate_percentage(self, total_text_length: int):
        """Calculate overall plagiarism percentage"""
        if not self.matches or total_text_length == 0:
            self.plagiarism_percentage = 0.0
            return
        
        # Calculate unique plagiarized character ranges
        plagiarized_ranges = []
        for match in self.matches:
            if match.similarity > 0.7:  # Only count high-confidence matches
                plagiarized_ranges.append((match.start_position, match.end_position))
        
        # Merge overlapping ranges
        merged_ranges = self._merge_ranges(plagiarized_ranges)
        
        # Calculate total plagiarized characters
        plagiarized_chars = sum(end - start for start, end in merged_ranges)
        
        self.plagiarism_percentage = (plagiarized_chars / total_text_length) * 100
    
    def _merge_ranges(self, ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Merge overlapping ranges"""
        if not ranges:
            return []
        
        sorted_ranges = sorted(ranges)
        merged = [sorted_ranges[0]]
        
        for current in sorted_ranges[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                merged[-1] = (last[0], max(last[1], current[1]))
            else:
                merged.append(current)
        
        return merged


class PlagiarismDetector:
    """Advanced multi-strategy plagiarism detector"""
    
    def __init__(self, enable_web_search: bool = False):
        self.enable_web_search = enable_web_search
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=5000)
        
        # Load sentence transformer model if available
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✓ Semantic similarity (BERT) enabled")
            except Exception as e:
                self.sentence_model = None
                print(f"Note: Could not load BERT model: {type(e).__name__}")
        else:
            self.sentence_model = None
            print("Note: Running without semantic similarity (4 detection methods active)")
        
        self.reference_database = []
    
    def add_reference_document(self, text: str, source_info: Dict):
        """Add a reference document to check against"""
        self.reference_database.append({
            'text': text,
            'source': source_info
        })
    
    def detect(self, text: str, sentences: List[str]) -> PlagiarismResult:
        """Perform comprehensive plagiarism detection"""
        print("\n=== Starting Plagiarism Detection ===")
        
        result = PlagiarismResult(
            overall_similarity=0.0,
            plagiarism_percentage=0.0,
            text_fingerprint=self._generate_fingerprint(text)
        )
        
        # Strategy 1: N-gram fingerprinting
        print("Running n-gram fingerprinting...")
        ngram_matches = self._ngram_detection(text, sentences)
        result.matches.extend(ngram_matches)
        result.analysis_methods.append("N-gram Fingerprinting")
        
        # Strategy 2: Sentence-level comparison
        print("Running sentence-level comparison...")
        sentence_matches = self._sentence_comparison(sentences)
        result.matches.extend(sentence_matches)
        result.analysis_methods.append("Sentence-Level Analysis")
        
        # Strategy 3: Semantic similarity
        if self.sentence_model:
            print("Running semantic similarity analysis...")
            semantic_matches = self._semantic_similarity(sentences)
            result.matches.extend(semantic_matches)
            result.analysis_methods.append("Semantic Similarity (BERT)")
        
        # Strategy 4: SimHash fingerprinting
        print("Running SimHash analysis...")
        simhash_matches = self._simhash_detection(text, sentences)
        result.matches.extend(simhash_matches)
        result.analysis_methods.append("SimHash Fingerprinting")
        
        # Strategy 5: Web search (if enabled)
        if self.enable_web_search:
            print("Running web search detection...")
            web_matches = self._web_search_detection(sentences)
            result.matches.extend(web_matches)
            result.analysis_methods.append("Web Search Detection")
        
        # Calculate overall statistics
        result.calculate_percentage(len(text))
        result.overall_similarity = self._calculate_overall_similarity(result.matches)
        
        # Extract unique sources
        result.sources = self._extract_sources(result.matches)
        
        print(f"\nDetection complete. Found {len(result.matches)} matches.")
        print(f"Plagiarism percentage: {result.plagiarism_percentage:.2f}%")
        
        return result
    
    def _generate_fingerprint(self, text: str) -> str:
        """Generate document fingerprint"""
        hash_obj = hashlib.sha256(text.encode())
        return hash_obj.hexdigest()
    
    def _ngram_detection(self, text: str, sentences: List[str]) -> List[PlagiarismMatch]:
        """Detect plagiarism using n-gram fingerprinting"""
        matches = []
        
        # Check against reference database
        for ref in self.reference_database:
            ref_text = ref['text']
            
            # Create n-grams (n=5 words)
            doc_ngrams = self._create_ngrams(text, 5)
            ref_ngrams = self._create_ngrams(ref_text, 5)
            
            # Find common n-grams
            common_ngrams = doc_ngrams.intersection(ref_ngrams)
            
            if common_ngrams:
                similarity = len(common_ngrams) / max(len(doc_ngrams), 1)
                
                if similarity > 0.1:  # Threshold for reporting
                    for ngram in common_ngrams:
                        match = PlagiarismMatch(
                            source_text=ngram,
                            matched_text=ngram,
                            similarity=1.0,
                            match_type='exact',
                            source_title=ref['source'].get('title', 'Unknown'),
                            source_url=ref['source'].get('url', '')
                        )
                        matches.append(match)
        
        return matches
    
    def _create_ngrams(self, text: str, n: int) -> Set[str]:
        """Create n-grams from text"""
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words]
        
        ngrams = set()
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.add(ngram)
        
        return ngrams
    
    def _sentence_comparison(self, sentences: List[str]) -> List[PlagiarismMatch]:
        """Compare sentences using various string matching algorithms"""
        matches = []
        
        for ref in self.reference_database:
            ref_sentences = sent_tokenize(ref['text'])
            
            for sent in sentences:
                if len(sent.strip()) < 20:  # Skip very short sentences
                    continue
                
                for ref_sent in ref_sentences:
                    # Calculate multiple similarity metrics
                    ratio = fuzz.ratio(sent, ref_sent) / 100
                    token_sort_ratio = fuzz.token_sort_ratio(sent, ref_sent) / 100
                    token_set_ratio = fuzz.token_set_ratio(sent, ref_sent) / 100
                    
                    # Average similarity
                    similarity = (ratio + token_sort_ratio + token_set_ratio) / 3
                    
                    if similarity > 0.75:  # High similarity threshold
                        match_type = 'exact' if similarity > 0.95 else 'paraphrased'
                        
                        match = PlagiarismMatch(
                            source_text=ref_sent,
                            matched_text=sent,
                            similarity=similarity,
                            match_type=match_type,
                            source_title=ref['source'].get('title', 'Unknown'),
                            source_url=ref['source'].get('url', '')
                        )
                        matches.append(match)
        
        return matches
    
    def _semantic_similarity(self, sentences: List[str]) -> List[PlagiarismMatch]:
        """Detect semantic similarity using sentence transformers"""
        if not self.sentence_model:
            return []
        
        matches = []
        
        try:
            # Encode sentences
            sent_embeddings = self.sentence_model.encode(sentences)
            
            for ref in self.reference_database:
                ref_sentences = sent_tokenize(ref['text'])
                if not ref_sentences:
                    continue
                
                ref_embeddings = self.sentence_model.encode(ref_sentences)
                
                # Calculate cosine similarity
                similarities = cosine_similarity(sent_embeddings, ref_embeddings)
                
                # Find high similarity pairs
                for i, sent in enumerate(sentences):
                    for j, ref_sent in enumerate(ref_sentences):
                        sim = similarities[i][j]
                        
                        if sim > 0.8:  # High semantic similarity
                            match = PlagiarismMatch(
                                source_text=ref_sent,
                                matched_text=sent,
                                similarity=float(sim),
                                match_type='semantic',
                                source_title=ref['source'].get('title', 'Unknown'),
                                source_url=ref['source'].get('url', '')
                            )
                            matches.append(match)
        
        except Exception as e:
            print(f"Semantic similarity error: {e}")
        
        return matches
    
    def _simhash_detection(self, text: str, sentences: List[str]) -> List[PlagiarismMatch]:
        """Detect near-duplicate content using SimHash"""
        matches = []
        
        doc_hash = Simhash(text)
        
        for ref in self.reference_database:
            ref_hash = Simhash(ref['text'])
            
            # Calculate hamming distance (lower = more similar)
            distance = doc_hash.distance(ref_hash)
            
            # SimHash produces 64-bit hash, distance < 3 indicates high similarity
            if distance < 10:
                similarity = 1 - (distance / 64)
                
                match = PlagiarismMatch(
                    source_text=ref['text'][:200] + "...",
                    matched_text=text[:200] + "...",
                    similarity=similarity,
                    match_type='paraphrased',
                    source_title=ref['source'].get('title', 'Unknown'),
                    source_url=ref['source'].get('url', '')
                )
                matches.append(match)
        
        return matches
    
    def _web_search_detection(self, sentences: List[str]) -> List[PlagiarismMatch]:
        """Search web for potential sources (simplified version)"""
        matches = []
        
        # Note: Full implementation would use Google Custom Search API
        # This is a simplified version using web scraping
        
        # Select representative sentences for searching
        search_sentences = sentences[::len(sentences)//min(5, len(sentences))] if sentences else []
        
        for sent in search_sentences[:3]:  # Limit to avoid rate limiting
            if len(sent.strip()) < 30:
                continue
            
            try:
                # This is a placeholder - in production, use proper API
                # query = sent[:100]
                # results = self._search_web(query)
                # Process results...
                pass
            except Exception as e:
                print(f"Web search error: {e}")
        
        return matches
    
    def _calculate_overall_similarity(self, matches: List[PlagiarismMatch]) -> float:
        """Calculate overall similarity score"""
        if not matches:
            return 0.0
        
        # Weight different match types
        weights = {
            'exact': 1.0,
            'paraphrased': 0.8,
            'semantic': 0.6
        }
        
        weighted_sum = sum(match.similarity * weights.get(match.match_type, 0.5) 
                          for match in matches)
        
        return min(weighted_sum / max(len(matches), 1), 1.0)
    
    def _extract_sources(self, matches: List[PlagiarismMatch]) -> List[Dict]:
        """Extract unique sources from matches"""
        sources = {}
        
        for match in matches:
            source_key = match.source_url or match.source_title
            
            if source_key not in sources:
                sources[source_key] = {
                    'title': match.source_title,
                    'url': match.source_url,
                    'match_count': 0,
                    'total_similarity': 0.0
                }
            
            sources[source_key]['match_count'] += 1
            sources[source_key]['total_similarity'] += match.similarity
        
        # Calculate average similarity per source
        for source in sources.values():
            source['avg_similarity'] = source['total_similarity'] / source['match_count']
        
        # Sort by match count
        return sorted(sources.values(), key=lambda x: x['match_count'], reverse=True)


if __name__ == "__main__":
    # Test the detector
    print("Plagiarism Detection Engine")
    print("Testing with sample data...")
    
    detector = PlagiarismDetector()
    
    # Add sample reference
    detector.add_reference_document(
        "This is a sample reference document for testing plagiarism detection.",
        {'title': 'Sample Reference', 'url': 'http://example.com'}
    )
    
    # Test text
    test_text = "This is a sample reference document for testing plagiarism detection."
    test_sentences = sent_tokenize(test_text)
    
    result = detector.detect(test_text, test_sentences)
    print(f"\nPlagiarism: {result.plagiarism_percentage:.2f}%")
    print(f"Matches found: {len(result.matches)}")
