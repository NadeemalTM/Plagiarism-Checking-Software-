"""
Report Generator
Creates comprehensive plagiarism and copyright reports in multiple formats
"""

import json
from datetime import datetime
from typing import Dict, List
from jinja2 import Template
from dataclasses import asdict


class ReportGenerator:
    """Generate comprehensive plagiarism reports"""
    
    def __init__(self):
        self.report_data = {}
    
    def generate_report(self, 
                       pdf_path: str,
                       pdf_stats: Dict,
                       plagiarism_result,
                       copyright_report,
                       format: str = 'text') -> str:
        """Generate comprehensive report in specified format"""
        
        self.report_data = {
            'document_info': {
                'file_path': pdf_path,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'statistics': pdf_stats
            },
            'plagiarism_analysis': {
                'overall_similarity': plagiarism_result.overall_similarity,
                'plagiarism_percentage': plagiarism_result.plagiarism_percentage,
                'total_matches': len(plagiarism_result.matches),
                'analysis_methods': plagiarism_result.analysis_methods,
                'sources': plagiarism_result.sources,
                'matches': []
            },
            'copyright_analysis': {
                'has_copyright_content': copyright_report.has_copyright_content,
                'total_items': copyright_report.total_copyrighted_content,
                'copyright_notices': copyright_report.copyright_notices,
                'trademarks': copyright_report.trademarks,
                'licenses': copyright_report.licenses,
                'matches': []
            }
        }
        
        # Add match details
        for match in plagiarism_result.matches[:50]:  # Limit for readability
            self.report_data['plagiarism_analysis']['matches'].append({
                'matched_text': match.matched_text[:200],
                'source_text': match.source_text[:200],
                'similarity': round(match.similarity * 100, 2),
                'type': match.match_type,
                'source': match.source_title
            })
        
        for match in copyright_report.copyright_matches:
            self.report_data['copyright_analysis']['matches'].append({
                'content': match.content[:200],
                'type': match.copyright_type,
                'confidence': round(match.confidence * 100, 2),
                'details': match.details,
                'owner': match.owner,
                'year': match.year
            })
        
        # Generate report in requested format
        if format == 'html':
            return self._generate_html_report()
        elif format == 'json':
            return self._generate_json_report()
        elif format == 'markdown':
            return self._generate_markdown_report()
        else:
            return self._generate_text_report()
    
    def _generate_text_report(self) -> str:
        """Generate plain text report"""
        report = []
        report.append("=" * 80)
        report.append("PLAGIARISM & COPYRIGHT ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Document Information
        report.append("DOCUMENT INFORMATION")
        report.append("-" * 80)
        doc_info = self.report_data['document_info']
        report.append(f"File: {doc_info['file_path']}")
        report.append(f"Analysis Date: {doc_info['analysis_date']}")
        report.append("")
        
        # Statistics
        stats = doc_info['statistics']
        report.append("Document Statistics:")
        report.append(f"  Total Pages: {stats.get('total_pages', 'N/A')}")
        report.append(f"  Total Words: {stats.get('total_words', 'N/A')}")
        report.append(f"  Total Sentences: {stats.get('total_sentences', 'N/A')}")
        report.append(f"  Total Paragraphs: {stats.get('total_paragraphs', 'N/A')}")
        report.append(f"  Citations Found: {stats.get('citations_found', 'N/A')}")
        report.append("")
        
        # Plagiarism Analysis
        report.append("=" * 80)
        report.append("PLAGIARISM ANALYSIS")
        report.append("=" * 80)
        plag = self.report_data['plagiarism_analysis']
        
        # Overall Score
        report.append(f"\n*** PLAGIARISM PERCENTAGE: {plag['plagiarism_percentage']:.2f}% ***")
        report.append(f"Overall Similarity Score: {plag['overall_similarity']:.2%}")
        report.append(f"Total Matches Found: {plag['total_matches']}")
        report.append("")
        
        # Analysis Methods
        report.append("Analysis Methods Used:")
        for method in plag['analysis_methods']:
            report.append(f"  ✓ {method}")
        report.append("")
        
        # Sources
        if plag['sources']:
            report.append("Top Sources Detected:")
            report.append("-" * 80)
            for i, source in enumerate(plag['sources'][:10], 1):
                report.append(f"\n{i}. {source['title']}")
                if source['url']:
                    report.append(f"   URL: {source['url']}")
                report.append(f"   Matches: {source['match_count']}")
                report.append(f"   Avg Similarity: {source['avg_similarity']:.2%}")
        
        # Sample Matches
        if plag['matches']:
            report.append("\n" + "-" * 80)
            report.append("Sample Plagiarism Matches (Top 10):")
            report.append("-" * 80)
            for i, match in enumerate(plag['matches'][:10], 1):
                report.append(f"\nMatch #{i}:")
                report.append(f"  Type: {match['type'].upper()}")
                report.append(f"  Similarity: {match['similarity']:.1f}%")
                report.append(f"  Source: {match['source']}")
                report.append(f"  Your Text: \"{match['matched_text']}\"")
                if match['source_text'] != match['matched_text']:
                    report.append(f"  Source Text: \"{match['source_text']}\"")
        
        # Copyright Analysis
        report.append("\n" + "=" * 80)
        report.append("COPYRIGHT CONTENT ANALYSIS")
        report.append("=" * 80)
        copyright_info = self.report_data['copyright_analysis']
        
        report.append(f"\nCopyright Content Detected: {'YES' if copyright_info['has_copyright_content'] else 'NO'}")
        report.append(f"Total Copyright Items: {copyright_info['total_items']}")
        report.append("")
        
        # Copyright Notices
        if copyright_info['copyright_notices']:
            report.append("Copyright Notices Found:")
            report.append("-" * 80)
            for notice in copyright_info['copyright_notices']:
                report.append(f"  • {notice}")
            report.append("")
        
        # Trademarks
        if copyright_info['trademarks']:
            report.append("Trademarks Found:")
            report.append("-" * 80)
            for tm in copyright_info['trademarks']:
                report.append(f"  • {tm}")
            report.append("")
        
        # Licenses
        if copyright_info['licenses']:
            report.append("Licenses Identified:")
            report.append("-" * 80)
            for lic in copyright_info['licenses']:
                report.append(f"  • {lic['type']}: {lic['content']}")
            report.append("")
        
        # Detailed Copyright Matches
        if copyright_info['matches']:
            report.append("Detailed Copyright Items:")
            report.append("-" * 80)
            for i, match in enumerate(copyright_info['matches'], 1):
                report.append(f"\n{i}. {match['type'].upper()}")
                report.append(f"   Content: {match['content']}")
                report.append(f"   Confidence: {match['confidence']:.1f}%")
                if match['owner']:
                    report.append(f"   Owner: {match['owner']}")
                if match['year']:
                    report.append(f"   Year: {match['year']}")
                report.append(f"   Details: {match['details']}")
        
        # Summary and Recommendations
        report.append("\n" + "=" * 80)
        report.append("SUMMARY & RECOMMENDATIONS")
        report.append("=" * 80)
        
        plag_pct = plag['plagiarism_percentage']
        if plag_pct > 30:
            report.append("\n⚠️  HIGH PLAGIARISM DETECTED")
            report.append("   - Document shows significant similarity to other sources")
            report.append("   - Immediate revision strongly recommended")
            report.append("   - Review all highlighted matches and cite sources properly")
        elif plag_pct > 15:
            report.append("\n⚠️  MODERATE PLAGIARISM DETECTED")
            report.append("   - Document has notable similarities to other sources")
            report.append("   - Review and revise flagged sections")
            report.append("   - Ensure proper citations and paraphrasing")
        elif plag_pct > 5:
            report.append("\n✓  LOW PLAGIARISM")
            report.append("   - Minor similarities detected (acceptable range)")
            report.append("   - Review flagged sections to ensure proper attribution")
        else:
            report.append("\n✓  MINIMAL/NO PLAGIARISM")
            report.append("   - Document appears to be original")
            report.append("   - Continue maintaining good citation practices")
        
        if copyright_info['has_copyright_content']:
            report.append("\n⚠️  COPYRIGHT CONTENT DETECTED")
            report.append("   - Document contains copyrighted material")
            report.append("   - Ensure you have permission to use this content")
            report.append("   - Consider fair use implications")
            report.append("   - Verify all quotes are properly attributed")
        
        report.append("\n" + "=" * 80)
        report.append("End of Report")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plagiarism & Copyright Analysis Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .section {
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .score-box {
            background: #f8f9fa;
            border-left: 5px solid #dc3545;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .score-box.low {
            border-left-color: #28a745;
        }
        .score-box.medium {
            border-left-color: #ffc107;
        }
        .score-box.high {
            border-left-color: #dc3545;
        }
        .score-value {
            font-size: 3em;
            font-weight: bold;
            color: #dc3545;
        }
        .score-value.low {
            color: #28a745;
        }
        .score-value.medium {
            color: #ffc107;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .match-item {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        .match-type {
            display: inline-block;
            padding: 5px 10px;
            background: #667eea;
            color: white;
            border-radius: 3px;
            font-size: 0.85em;
            margin-right: 10px;
        }
        .similarity {
            display: inline-block;
            padding: 5px 10px;
            background: #28a745;
            color: white;
            border-radius: 3px;
            font-size: 0.85em;
        }
        .copyright-item {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .method-badge {
            display: inline-block;
            background: #e9ecef;
            padding: 5px 10px;
            margin: 5px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
        }
        .alert {
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .alert-danger {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .alert-warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
        .alert-success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📄 Plagiarism & Copyright Analysis Report</h1>
        <p>Analysis Date: {{ doc_info.analysis_date }}</p>
        <p>Document: {{ doc_info.file_path }}</p>
    </div>

    <div class="section">
        <h2>📊 Document Statistics</h2>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{{ stats.total_pages }}</div>
                <div class="stat-label">Pages</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ stats.total_words }}</div>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ stats.total_sentences }}</div>
                <div class="stat-label">Sentences</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ stats.citations_found }}</div>
                <div class="stat-label">Citations</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🔍 Plagiarism Analysis</h2>
        
        {% set plag_class = 'low' if plag.plagiarism_percentage < 5 else ('medium' if plag.plagiarism_percentage < 15 else 'high') %}
        <div class="score-box {{ plag_class }}">
            <div class="score-value {{ plag_class }}">{{ "%.2f"|format(plag.plagiarism_percentage) }}%</div>
            <div>Plagiarism Detected</div>
        </div>

        <p><strong>Overall Similarity:</strong> {{ "%.2f"|format(plag.overall_similarity * 100) }}%</p>
        <p><strong>Total Matches:</strong> {{ plag.total_matches }}</p>

        <h3>Analysis Methods Used:</h3>
        {% for method in plag.analysis_methods %}
        <span class="method-badge">✓ {{ method }}</span>
        {% endfor %}

        {% if plag.sources %}
        <h3>Top Sources:</h3>
        <table>
            <tr>
                <th>#</th>
                <th>Source</th>
                <th>Matches</th>
                <th>Avg Similarity</th>
            </tr>
            {% for source in plag.sources[:10] %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>
                    {{ source.title }}
                    {% if source.url %}
                    <br><small>{{ source.url }}</small>
                    {% endif %}
                </td>
                <td>{{ source.match_count }}</td>
                <td>{{ "%.1f"|format(source.avg_similarity * 100) }}%</td>
            </tr>
            {% endfor %}
        </table>
        {% endif %}

        {% if plag.matches %}
        <h3>Sample Matches (Top 10):</h3>
        {% for match in plag.matches[:10] %}
        <div class="match-item">
            <span class="match-type">{{ match.type }}</span>
            <span class="similarity">{{ match.similarity }}%</span>
            <p><strong>Source:</strong> {{ match.source }}</p>
            <p><strong>Your Text:</strong> "{{ match.matched_text }}"</p>
            {% if match.source_text != match.matched_text %}
            <p><strong>Source Text:</strong> "{{ match.source_text }}"</p>
            {% endif %}
        </div>
        {% endfor %}
        {% endif %}
    </div>

    <div class="section">
        <h2>©️ Copyright Content Analysis</h2>
        
        <p><strong>Copyright Content Detected:</strong> 
            {% if copyright.has_copyright_content %}
            <span style="color: #dc3545;">YES</span>
            {% else %}
            <span style="color: #28a745;">NO</span>
            {% endif %}
        </p>
        <p><strong>Total Items:</strong> {{ copyright.total_items }}</p>

        {% if copyright.copyright_notices %}
        <h3>Copyright Notices:</h3>
        {% for notice in copyright.copyright_notices %}
        <div class="copyright-item">{{ notice }}</div>
        {% endfor %}
        {% endif %}

        {% if copyright.trademarks %}
        <h3>Trademarks:</h3>
        {% for tm in copyright.trademarks %}
        <div class="copyright-item">{{ tm }}</div>
        {% endfor %}
        {% endif %}

        {% if copyright.licenses %}
        <h3>Licenses:</h3>
        {% for lic in copyright.licenses %}
        <div class="copyright-item">
            <strong>{{ lic.type }}</strong><br>
            {{ lic.content }}
        </div>
        {% endfor %}
        {% endif %}
    </div>

    <div class="section">
        <h2>📋 Recommendations</h2>
        
        {% if plag.plagiarism_percentage > 30 %}
        <div class="alert alert-danger">
            <strong>⚠️ HIGH PLAGIARISM DETECTED</strong>
            <ul>
                <li>Document shows significant similarity to other sources</li>
                <li>Immediate revision strongly recommended</li>
                <li>Review all highlighted matches and cite sources properly</li>
            </ul>
        </div>
        {% elif plag.plagiarism_percentage > 15 %}
        <div class="alert alert-warning">
            <strong>⚠️ MODERATE PLAGIARISM DETECTED</strong>
            <ul>
                <li>Document has notable similarities to other sources</li>
                <li>Review and revise flagged sections</li>
                <li>Ensure proper citations and paraphrasing</li>
            </ul>
        </div>
        {% elif plag.plagiarism_percentage > 5 %}
        <div class="alert alert-warning">
            <strong>✓ LOW PLAGIARISM</strong>
            <ul>
                <li>Minor similarities detected (acceptable range)</li>
                <li>Review flagged sections to ensure proper attribution</li>
            </ul>
        </div>
        {% else %}
        <div class="alert alert-success">
            <strong>✓ MINIMAL/NO PLAGIARISM</strong>
            <ul>
                <li>Document appears to be original</li>
                <li>Continue maintaining good citation practices</li>
            </ul>
        </div>
        {% endif %}

        {% if copyright.has_copyright_content %}
        <div class="alert alert-warning">
            <strong>⚠️ COPYRIGHT CONTENT DETECTED</strong>
            <ul>
                <li>Document contains copyrighted material</li>
                <li>Ensure you have permission to use this content</li>
                <li>Consider fair use implications</li>
                <li>Verify all quotes are properly attributed</li>
            </ul>
        </div>
        {% endif %}
    </div>

    <footer style="text-align: center; margin-top: 40px; color: #666;">
        <p>Generated by Advanced PDF Plagiarism Checker</p>
        <p>Report Date: {{ doc_info.analysis_date }}</p>
    </footer>
</body>
</html>
        """
        
        template = Template(html_template)
        html = template.render(
            doc_info=self.report_data['document_info'],
            stats=self.report_data['document_info']['statistics'],
            plag=self.report_data['plagiarism_analysis'],
            copyright=self.report_data['copyright_analysis']
        )
        
        return html
    
    def _generate_json_report(self) -> str:
        """Generate JSON report"""
        return json.dumps(self.report_data, indent=2)
    
    def _generate_markdown_report(self) -> str:
        """Generate Markdown report"""
        md = []
        md.append("# Plagiarism & Copyright Analysis Report\n")
        
        doc_info = self.report_data['document_info']
        md.append(f"**File:** {doc_info['file_path']}")
        md.append(f"**Analysis Date:** {doc_info['analysis_date']}\n")
        
        md.append("## Document Statistics\n")
        stats = doc_info['statistics']
        md.append(f"- **Total Pages:** {stats.get('total_pages', 'N/A')}")
        md.append(f"- **Total Words:** {stats.get('total_words', 'N/A')}")
        md.append(f"- **Total Sentences:** {stats.get('total_sentences', 'N/A')}")
        md.append(f"- **Citations Found:** {stats.get('citations_found', 'N/A')}\n")
        
        plag = self.report_data['plagiarism_analysis']
        md.append("## Plagiarism Analysis\n")
        md.append(f"### **Plagiarism Percentage: {plag['plagiarism_percentage']:.2f}%**\n")
        md.append(f"- Overall Similarity: {plag['overall_similarity']:.2%}")
        md.append(f"- Total Matches: {plag['total_matches']}\n")
        
        if plag['sources']:
            md.append("### Top Sources\n")
            for i, source in enumerate(plag['sources'][:10], 1):
                md.append(f"{i}. **{source['title']}**")
                md.append(f"   - Matches: {source['match_count']}")
                md.append(f"   - Avg Similarity: {source['avg_similarity']:.2%}\n")
        
        copyright_info = self.report_data['copyright_analysis']
        md.append("## Copyright Analysis\n")
        md.append(f"- **Copyright Content Detected:** {'YES' if copyright_info['has_copyright_content'] else 'NO'}")
        md.append(f"- **Total Items:** {copyright_info['total_items']}\n")
        
        return "\n".join(md)
    
    def save_report(self, report: str, output_path: str):
        """Save report to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    print("Report Generator Module")
    print("Use this module through the main plagiarism checker application")
