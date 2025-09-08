#!/usr/bin/env python3
"""
Sensitive Data Scanner
Scans files and directories for potentially sensitive information
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import mimetypes

class SensitiveDataScanner:
    def __init__(self):
        # Define regex patterns for sensitive data
        self.patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'),
            'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            'credit_card': re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'),
            'ip_address': re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'api_key': re.compile(r'(?i)(?:api[_-]?key|apikey|access[_-]?token|auth[_-]?token|secret[_-]?key)[\s]*[:=][\s]*[\'"`]?([a-zA-Z0-9_-]{20,})[\'"`]?'),
            'password': re.compile(r'(?i)(?:password|passwd|pwd|pass)[\s]*[:=][\s]*[\'"`]?([^\s\'"`,;]{4,})[\'"`]?'),
            'private_key': re.compile(r'-----BEGIN (?:RSA )?PRIVATE KEY-----'),
            'jwt_token': re.compile(r'eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*'),
            'aws_access_key': re.compile(r'(?i)aws[_-]?access[_-]?key[_-]?id[\s]*[:=][\s]*[\'"`]?(AKIA[0-9A-Z]{16})[\'"`]?'),
            'aws_secret_key': re.compile(r'(?i)aws[_-]?secret[_-]?access[_-]?key[\s]*[:=][\s]*[\'"`]?([A-Za-z0-9/+=]{40})[\'"`]?'),
            'github_token': re.compile(r'(?i)github[_-]?token[\s]*[:=][\s]*[\'"`]?(ghp_[a-zA-Z0-9]{36})[\'"`]?'),
            'slack_token': re.compile(r'xox[baprs]-([0-9a-zA-Z]{10,48})'),
            'url_with_credentials': re.compile(r'https?://[^:\s]+:[^@\s]+@[^\s]+'),
        }
        
        # File extensions to scan (text-based files)
        self.text_extensions = {
            '.txt', '.log', '.conf', '.config', '.ini', '.env', '.json', '.xml', '.yml', '.yaml',
            '.py', '.js', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.go',
            '.sql', '.sh', '.bat', '.ps1', '.md', '.rst', '.csv', '.properties', '.cfg',
            '.dockerfile', '.gitignore', '.htaccess', '.nginx', '.apache'
        }
        
        # Files to always exclude
        self.excluded_files = {
            '.git', '.svn', '.hg', 'node_modules', '__pycache__', '.pyc', '.class',
            'target', 'build', 'dist', '.DS_Store', 'Thumbs.db'
        }
        
        self.results = []
        self.stats = {
            'files_scanned': 0,
            'files_with_sensitive_data': 0,
            'total_findings': 0
        }

    def is_text_file(self, file_path: Path) -> bool:
        """Check if file is likely a text file we should scan"""
        # Check extension
        if file_path.suffix.lower() in self.text_extensions:
            return True
        
        # Check mime type for files without extensions
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and mime_type.startswith('text/'):
            return True
            
        return False

    def should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded from scanning"""
        # Check if any part of the path contains excluded directories
        for part in file_path.parts:
            if part in self.excluded_files:
                return True
        return False

    def scan_file_content(self, file_path: Path) -> List[Dict]:
        """Scan a single file for sensitive data"""
        findings = []
        
        try:
            # Try to read as UTF-8, fallback to other encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                return findings
            
            # Scan content with each pattern
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                for pattern_name, pattern in self.patterns.items():
                    matches = pattern.finditer(line)
                    for match in matches:
                        finding = {
                            'file': str(file_path),
                            'line': line_num,
                            'column': match.start() + 1,
                            'type': pattern_name,
                            'context': line.strip()[:100] + ('...' if len(line.strip()) > 100 else ''),
                            'match': match.group(0)
                        }
                        findings.append(finding)
                        
        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
            
        return findings

    def scan_directory(self, directory: Path, max_file_size: int = 10*1024*1024) -> None:
        """Recursively scan directory for sensitive data"""
        print(f"Scanning directory: {directory}")
        
        for root, dirs, files in os.walk(directory):
            root_path = Path(root)
            
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude_file(root_path / d)]
            
            for file in files:
                file_path = root_path / file
                
                # Skip excluded files
                if self.should_exclude_file(file_path):
                    continue
                
                # Skip non-text files
                if not self.is_text_file(file_path):
                    continue
                
                # Skip large files
                try:
                    if file_path.stat().st_size > max_file_size:
                        print(f"Skipping large file: {file_path}")
                        continue
                except OSError:
                    continue
                
                print(f"Scanning: {file_path}")
                self.stats['files_scanned'] += 1
                
                findings = self.scan_file_content(file_path)
                if findings:
                    self.results.extend(findings)
                    self.stats['files_with_sensitive_data'] += 1
                    self.stats['total_findings'] += len(findings)

    def create_ascii_table(self, headers: List[str], rows: List[List[str]], title: str = None) -> str:
        """Create an ASCII table from headers and rows"""
        if not rows:
            return ""
        
        # Calculate column widths
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Create table
        lines = []
        
        # Title
        if title:
            total_width = sum(col_widths) + len(headers) * 3 + 1
            lines.append("┌" + "─" * (total_width - 2) + "┐")
            title_padding = (total_width - len(title) - 4) // 2
            lines.append(f"│ {' ' * title_padding}{title}{' ' * (total_width - len(title) - title_padding - 4)} │")
            lines.append("├" + "─" * (total_width - 2) + "┤")
        
        # Header separator
        separator = "┌" + "┬".join("─" * (width + 2) for width in col_widths) + "┐"
        lines.append(separator)
        
        # Header row
        header_row = "│" + "│".join(f" {header:<{col_widths[i]}} " for i, header in enumerate(headers)) + "│"
        lines.append(header_row)
        
        # Header bottom
        header_sep = "├" + "┼".join("─" * (width + 2) for width in col_widths) + "┤"
        lines.append(header_sep)
        
        # Data rows
        for row in rows:
            data_row = "│" + "│".join(f" {str(cell):<{col_widths[i]}} " for i, cell in enumerate(row)) + "│"
            lines.append(data_row)
        
        # Bottom border
        bottom = "└" + "┴".join("─" * (width + 2) for width in col_widths) + "┘"
        lines.append(bottom)
        
        return "\n".join(lines)

    def generate_report(self, output_file: str = None) -> str:
        """Generate a report of findings in ASCII table format"""
        report_lines = []
        
        # Header
        report_lines.append("╔" + "═" * 78 + "╗")
        report_lines.append("║" + " " * 25 + "SENSITIVE DATA SCAN REPORT" + " " * 25 + "║")
        report_lines.append("╚" + "═" * 78 + "╝")
        report_lines.append("")
        
        # Summary statistics table
        stats_headers = ["Metric", "Count"]
        stats_rows = [
            ["Files Scanned", str(self.stats['files_scanned'])],
            ["Files with Sensitive Data", str(self.stats['files_with_sensitive_data'])],
            ["Total Findings", str(self.stats['total_findings'])]
        ]
        
        summary_table = self.create_ascii_table(stats_headers, stats_rows, "SCAN SUMMARY")
        report_lines.append(summary_table)
        report_lines.append("")
        
        if not self.results:
            report_lines.append("✅ No sensitive data found!")
            report = "\n".join(report_lines)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"Report saved to: {output_file}")
            
            return report
        
        # Group findings by type
        findings_by_type = {}
        for finding in self.results:
            finding_type = finding['type']
            if finding_type not in findings_by_type:
                findings_by_type[finding_type] = []
            findings_by_type[finding_type].append(finding)
        
        # Summary by type table
        type_headers = ["Data Type", "Count", "Percentage"]
        type_rows = []
        for finding_type, findings in sorted(findings_by_type.items(), key=lambda x: len(x[1]), reverse=True):
            count = len(findings)
            percentage = f"{(count / self.stats['total_findings'] * 100):.1f}%"
            type_name = finding_type.replace('_', ' ').title()
            type_rows.append([type_name, str(count), percentage])
        
        type_summary_table = self.create_ascii_table(type_headers, type_rows, "FINDINGS BY TYPE")
        report_lines.append(type_summary_table)
        report_lines.append("")
        
        # Detailed findings for each type
        for finding_type, findings in sorted(findings_by_type.items()):
            type_name = finding_type.replace('_', ' ').title()
            
            # Create detailed table for this type
            detail_headers = ["File", "Line", "Col", "Match", "Context"]
            detail_rows = []
            
            for finding in findings:
                # Truncate long file paths and contexts for table formatting
                file_path = finding['file']
                if len(file_path) > 40:
                    file_path = "..." + file_path[-37:]
                
                context = finding['context']
                if len(context) > 50:
                    context = context[:47] + "..."
                
                match = finding['match']
                if len(match) > 30:
                    match = match[:27] + "..."
                
                detail_rows.append([
                    file_path,
                    str(finding['line']),
                    str(finding['column']),
                    match,
                    context
                ])
            
            detail_table = self.create_ascii_table(detail_headers, detail_rows, f"{type_name} Details")
            report_lines.append(detail_table)
            report_lines.append("")
        
        report = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report

    def export_json(self, output_file: str) -> None:
        """Export findings as JSON"""
        data = {
            'stats': self.stats,
            'findings': self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"JSON report saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Scan files and directories for sensitive data')
    parser.add_argument('path', help='Path to scan (file or directory)')
    parser.add_argument('--output', '-o', help='Output report file')
    parser.add_argument('--json', help='Export findings as JSON')
    parser.add_argument('--max-size', type=int, default=10*1024*1024, 
                       help='Maximum file size to scan in bytes (default: 10MB)')
    
    args = parser.parse_args()
    
    # Validate path
    scan_path = Path(args.path)
    if not scan_path.exists():
        print(f"Error: Path '{args.path}' does not exist")
        return
    
    # Create scanner
    scanner = SensitiveDataScanner()
    
    # Scan path
    if scan_path.is_file():
        if scanner.is_text_file(scan_path) and not scanner.should_exclude_file(scan_path):
            print(f"Scanning file: {scan_path}")
            findings = scanner.scan_file_content(scan_path)
            scanner.results.extend(findings)
            scanner.stats['files_scanned'] = 1
            scanner.stats['files_with_sensitive_data'] = 1 if findings else 0
            scanner.stats['total_findings'] = len(findings)
        else:
            print("File type not supported for scanning")
    else:
        scanner.scan_directory(scan_path, args.max_size)
    
    # Generate reports
    if scanner.results:
        print(f"\n⚠️  Found {len(scanner.results)} sensitive data items!")
        report = scanner.generate_report(args.output)
        
        if not args.output:
            print("\n" + report)
        
        if args.json:
            scanner.export_json(args.json)
    else:
        print("\n✅ No sensitive data found!")
        
        # Still generate empty report if requested
        if args.output:
            scanner.generate_report(args.output)
        if args.json:
            scanner.export_json(args.json)

if __name__ == "__main__":
    main()