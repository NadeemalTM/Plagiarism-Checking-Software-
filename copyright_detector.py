"""
Copyright Content Identifier
Detects and identifies copyrighted content in documents
"""

import re
from typing import List, Dict, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CopyrightMatch:
    """Represents detected copyrighted content"""
    content: str
    copyright_type: str  # 'notice', 'trademark', 'patent', 'licensed', 'quoted'
    confidence: float
    position: int
    details: str = ""
    owner: str = ""
    year: str = ""
    license_type: str = ""


@dataclass
class CopyrightReport:
    """Complete copyright analysis report"""
    has_copyright_content: bool = False
    copyright_matches: List[CopyrightMatch] = field(default_factory=list)
    copyright_notices: List[str] = field(default_factory=list)
    trademarks: List[str] = field(default_factory=list)
    licenses: List[Dict] = field(default_factory=list)
    quoted_sources: List[Dict] = field(default_factory=list)
    total_copyrighted_content: int = 0
    
    def add_match(self, match: CopyrightMatch):
        """Add a copyright match"""
        self.copyright_matches.append(match)
        self.has_copyright_content = True


class CopyrightDetector:
    """Detect copyrighted content and licensing information"""
    
    def __init__(self):
        self.copyright_patterns = self._build_copyright_patterns()
        self.trademark_patterns = self._build_trademark_patterns()
        self.license_patterns = self._build_license_patterns()
        self.known_copyrighted_phrases = self._load_known_phrases()
    
    def _build_copyright_patterns(self) -> List[Dict]:
        """Build patterns for copyright detection"""
        return [
            {
                'pattern': r'©\s*(\d{4}(?:-\d{4})?)\s*([^.]+)',
                'type': 'copyright_symbol',
                'description': 'Copyright symbol with year'
            },
            {
                'pattern': r'Copyright\s*©?\s*(\d{4}(?:-\d{4})?)\s*([^.]+)',
                'type': 'copyright_text',
                'description': 'Copyright text with year'
            },
            {
                'pattern': r'All\s+rights\s+reserved',
                'type': 'rights_reserved',
                'description': 'All rights reserved notice'
            },
            {
                'pattern': r'(?:Copyrighted|Protected)\s+(?:material|content|work)',
                'type': 'protected_content',
                'description': 'Protected content notice'
            },
            {
                'pattern': r'No\s+part\s+of\s+this\s+(?:publication|work|book)\s+may\s+be\s+reproduced',
                'type': 'reproduction_restriction',
                'description': 'Reproduction restriction'
            }
        ]
    
    def _build_trademark_patterns(self) -> List[Dict]:
        """Build patterns for trademark detection"""
        return [
            {
                'pattern': r'([A-Z][a-zA-Z0-9]+)(?:\s+|)(?:™|®|℠)',
                'type': 'trademark_symbol',
                'description': 'Trademark symbol'
            },
            {
                'pattern': r'(?:Trademark|TM|Registered\s+trademark)\s+of\s+([^.]+)',
                'type': 'trademark_notice',
                'description': 'Trademark notice'
            }
        ]
    
    def _build_license_patterns(self) -> List[Dict]:
        """Build patterns for license detection"""
        return [
            {
                'pattern': r'Licensed\s+under\s+(?:the\s+)?([^.]+)',
                'type': 'license',
                'description': 'License declaration'
            },
            {
                'pattern': r'(?:MIT|GPL|Apache|BSD|Creative\s+Commons)\s+License',
                'type': 'specific_license',
                'description': 'Specific license type'
            },
            {
                'pattern': r'CC\s+BY(?:-NC)?(?:-SA)?(?:-ND)?\s+\d\.\d',
                'type': 'creative_commons',
                'description': 'Creative Commons license'
            }
        ]
    
    def _load_known_phrases(self) -> Set[str]:
        """Load known copyrighted phrases and terms"""
        return {
            'proprietary and confidential',
            'trade secret',
            'confidential information',
            'intellectual property',
            'patent pending',
            'patented technology',
            'licensed content',
            'authorized use only'
        }
    
    def analyze(self, text: str, citations: List[str]) -> CopyrightReport:
        """Perform comprehensive copyright analysis"""
        print("\n=== Analyzing Copyright Content ===")
        
        report = CopyrightReport()
        
        # Detect copyright notices
        print("Detecting copyright notices...")
        copyright_matches = self._detect_copyright_notices(text)
        for match in copyright_matches:
            report.add_match(match)
            report.copyright_notices.append(match.content)
        
        # Detect trademarks
        print("Detecting trademarks...")
        trademark_matches = self._detect_trademarks(text)
        for match in trademark_matches:
            report.add_match(match)
            report.trademarks.append(match.content)
        
        # Detect licenses
        print("Detecting licenses...")
        license_matches = self._detect_licenses(text)
        for match in license_matches:
            report.add_match(match)
            report.licenses.append({
                'type': match.license_type,
                'content': match.content
            })
        
        # Detect quoted content
        print("Detecting quoted sources...")
        quoted_matches = self._detect_quoted_content(text, citations)
        for match in quoted_matches:
            report.add_match(match)
            report.quoted_sources.append({
                'content': match.content,
                'position': match.position
            })
        
        # Detect known copyrighted phrases
        print("Checking known copyrighted phrases...")
        phrase_matches = self._detect_copyrighted_phrases(text)
        for match in phrase_matches:
            report.add_match(match)
        
        # Calculate total copyrighted content
        report.total_copyrighted_content = len(report.copyright_matches)
        
        print(f"Found {report.total_copyrighted_content} copyright-related items")
        
        return report
    
    def _detect_copyright_notices(self, text: str) -> List[CopyrightMatch]:
        """Detect copyright notices in text"""
        matches = []
        
        for pattern_info in self.copyright_patterns:
            pattern = pattern_info['pattern']
            
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group(0)
                position = match.start()
                
                # Extract year and owner if available
                year = ""
                owner = ""
                
                if match.groups():
                    if len(match.groups()) >= 1:
                        year = match.group(1)
                    if len(match.groups()) >= 2:
                        owner = match.group(2).strip()
                
                copyright_match = CopyrightMatch(
                    content=content,
                    copyright_type=pattern_info['type'],
                    confidence=0.95,
                    position=position,
                    details=pattern_info['description'],
                    owner=owner,
                    year=year
                )
                matches.append(copyright_match)
        
        return matches
    
    def _detect_trademarks(self, text: str) -> List[CopyrightMatch]:
        """Detect trademark notices in text"""
        matches = []
        
        for pattern_info in self.trademark_patterns:
            pattern = pattern_info['pattern']
            
            for match in re.finditer(pattern, text):
                content = match.group(0)
                position = match.start()
                
                owner = ""
                if match.groups():
                    owner = match.group(1).strip()
                
                trademark_match = CopyrightMatch(
                    content=content,
                    copyright_type='trademark',
                    confidence=0.9,
                    position=position,
                    details=pattern_info['description'],
                    owner=owner
                )
                matches.append(trademark_match)
        
        return matches
    
    def _detect_licenses(self, text: str) -> List[CopyrightMatch]:
        """Detect license declarations in text"""
        matches = []
        
        for pattern_info in self.license_patterns:
            pattern = pattern_info['pattern']
            
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group(0)
                position = match.start()
                
                license_type = ""
                if match.groups():
                    license_type = match.group(1).strip()
                
                license_match = CopyrightMatch(
                    content=content,
                    copyright_type='license',
                    confidence=0.85,
                    position=position,
                    details=pattern_info['description'],
                    license_type=license_type
                )
                matches.append(license_match)
        
        return matches
    
    def _detect_quoted_content(self, text: str, citations: List[str]) -> List[CopyrightMatch]:
        """Detect properly quoted and cited content"""
        matches = []
        
        # Find quoted text
        quote_pattern = r'"([^"]{50,})"'
        
        for match in re.finditer(quote_pattern, text):
            quoted_text = match.group(1)
            position = match.start()
            
            # Check if there's a nearby citation
            nearby_text = text[position:min(position+200, len(text))]
            has_citation = any(citation in nearby_text for citation in citations)
            
            confidence = 0.7 if has_citation else 0.5
            
            quote_match = CopyrightMatch(
                content=quoted_text,
                copyright_type='quoted',
                confidence=confidence,
                position=position,
                details='Quoted content' + (' with citation' if has_citation else ' without citation')
            )
            matches.append(quote_match)
        
        return matches
    
    def _detect_copyrighted_phrases(self, text: str) -> List[CopyrightMatch]:
        """Detect known copyrighted phrases"""
        matches = []
        text_lower = text.lower()
        
        for phrase in self.known_copyrighted_phrases:
            if phrase in text_lower:
                position = text_lower.index(phrase)
                
                phrase_match = CopyrightMatch(
                    content=phrase,
                    copyright_type='copyrighted_phrase',
                    confidence=0.8,
                    position=position,
                    details='Known copyrighted or proprietary phrase'
                )
                matches.append(phrase_match)
        
        return matches
    
    def identify_fair_use(self, text: str, citations: List[str]) -> Dict:
        """Analyze if usage might qualify as fair use"""
        fair_use_indicators = {
            'has_citations': len(citations) > 0,
            'citation_count': len(citations),
            'has_quotes': '"' in text,
            'quote_count': text.count('"') // 2,
            'has_commentary': any(word in text.lower() for word in 
                                 ['analysis', 'critique', 'commentary', 'review', 'discuss']),
            'transformative_language': any(word in text.lower() for word in 
                                          ['however', 'in contrast', 'alternatively', 'argue']),
            'educational_context': any(word in text.lower() for word in 
                                      ['research', 'study', 'educational', 'academic'])
        }
        
        # Calculate fair use score
        score = sum([
            fair_use_indicators['has_citations'] * 25,
            min(fair_use_indicators['citation_count'] * 5, 25),
            fair_use_indicators['has_commentary'] * 20,
            fair_use_indicators['transformative_language'] * 15,
            fair_use_indicators['educational_context'] * 15
        ])
        
        fair_use_indicators['fair_use_score'] = min(score, 100)
        fair_use_indicators['likely_fair_use'] = score > 50
        
        return fair_use_indicators


if __name__ == "__main__":
    # Test the copyright detector
    test_text = """
    Copyright © 2024 Example Corporation. All rights reserved.
    
    This document contains proprietary and confidential information.
    No part of this publication may be reproduced without permission.
    
    Python™ is a registered trademark of the Python Software Foundation.
    
    Licensed under the MIT License.
    """
    
    detector = CopyrightDetector()
    report = detector.analyze(test_text, [])
    
    print(f"\nCopyright items found: {report.total_copyrighted_content}")
    print(f"Has copyright content: {report.has_copyright_content}")
    
    for match in report.copyright_matches:
        print(f"\n- Type: {match.copyright_type}")
        print(f"  Content: {match.content}")
        print(f"  Confidence: {match.confidence}")
