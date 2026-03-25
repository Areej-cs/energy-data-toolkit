"""
Energy Data Analysis Toolkit
Created by: Areej | KKU Computer Science

A Python-based toolkit for analyzing energy production data.
Developed as part of my learning in data analysis and industrial applications.

What it does:

- Process production data from CSV files
- Analyze system logs for errors
- Detect trends and anomalies
- Generate analysis reports

"""

import csv
import re
from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict
import statistics
import json


class ProductionDataProcessor:
    """Process and analyze daily production data from CSV files"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = []
        self.load_data()

    def load_data(self) -> None:
        """Load production data from CSV file"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
        except FileNotFoundError:
            raise Exception(f"File not found: {self.filepath}")

    def validate_data(self) -> List[Dict]:
        """
        Check production data for common errors.
        """
        errors = []
        for i, row in enumerate(self.data):
            if 'production' in row:
                try:
                    prod = float(row['production'])
                    if prod < 0:
                        errors.append({
                            'row': i + 1,
                            'error': 'Negative production value',
                            'value': prod
                        })
                except ValueError:
                    errors.append({
                        'row': i + 1,
                        'error': 'Invalid production value',
                        'value': row['production']
                    })
        return errors

    def calculate_daily_average(self) -> float:
        """Calculate average daily production"""
        productions = []
        for row in self.data:
            try:
                productions.append(float(row.get('production', 0)))
            except ValueError:
                continue

        if len(productions) == 0:
            return 0.0

        return statistics.mean(productions)

    def get_top_days(self, n: int = 5) -> List[Dict]:
        """Get top N production days"""
        valid_data = []

        for row in self.data:
            try:
                prod = float(row.get('production', 0))
                valid_data.append({
                    'date': row.get('date', 'Unknown'),
                    'production': prod
                })
            except ValueError:
                continue

        sorted_data = sorted(valid_data, key=lambda x: x['production'], reverse=True)
        return sorted_data[:n]


class LogFileAnalyzer:
    """Analyze system log files for errors and patterns"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.logs = []
        self.load_logs()

    def load_logs(self) -> None:
        """Load log file content"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.logs = f.readlines()
        except FileNotFoundError:
            raise Exception(f"Log file not found: {self.filepath}")

    def count_by_level(self) -> Dict[str, int]:
        """Count log entries by severity"""
        counts = defaultdict(int)

        for log in self.logs:
            log_upper = log.upper()
            if 'ERROR' in log_upper:
                counts['ERROR'] += 1
            elif 'WARNING' in log_upper:
                counts['WARNING'] += 1
            elif 'INFO' in log_upper:
                counts['INFO'] += 1

        return dict(counts)

    def extract_errors(self) -> List[str]:
        """Get all error messages from logs"""
        return [log.strip() for log in self.logs if 'ERROR' in log.upper()]

    def find_pattern(self, pattern: str) -> List[Tuple[int, str]]:
        """Search for pattern in logs"""
        matches = []
        for i, log in enumerate(self.logs):
            if re.search(pattern, log, re.IGNORECASE):
                matches.append((i + 1, log.strip()))
        return matches


class TimeSeriesAnalyzer:
    """Analyze time-series data for trends and anomalies"""

    def __init__(self, data: List[float]):
        self.data = data

    def moving_average(self, window: int = 7) -> List[float]:
        if len(self.data) < window:
            return self.data

        result = []
        for i in range(len(self.data) - window + 1):
            window_data = self.data[i:i + window]
            result.append(sum(window_data) / window)

        return result

    def detect_anomalies(self, threshold: float = 2.0) -> List[int]:
        if len(self.data) < 2:
            return []

        mean = statistics.mean(self.data)
        stdev = statistics.stdev(self.data)

        anomalies = []
        for i, val in enumerate(self.data):
            if stdev > 0:
                z_score = abs((val - mean) / stdev)
                if z_score > threshold:
                    anomalies.append(i)

        return anomalies

    def calculate_trend(self) -> str:
        if len(self.data) < 2:
            return "insufficient_data"

        mid = len(self.data) // 2
        avg_first = statistics.mean(self.data[:mid])
        avg_second = statistics.mean(self.data[mid:])

        if avg_first > 0:
            diff_percent = ((avg_second - avg_first) / avg_first * 100)
        else:
            diff_percent = 0

        if diff_percent > 5:
            return "increasing"
        elif diff_percent < -5:
            return "decreasing"
        else:
            return "stable"


class ReportGenerator:

    @staticmethod
    def generate_production_report(processor: ProductionDataProcessor) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("PRODUCTION DATA ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        avg = processor.calculate_daily_average()
        lines.append(f"Average Daily Production: {avg:.2f} barrels\n")

        lines.append("Top 5 Production Days:")
        lines.append("-" * 40)
        for i, day in enumerate(processor.get_top_days(5), 1):
            lines.append(f"{i}. {day['date']}: {day['production']:.2f} barrels")

        lines.append("")
        errors = processor.validate_data()
        lines.append(f"Data Quality: {len(errors)} errors found")

        if errors:
            for err in errors[:5]:
                lines.append(f"  - Row {err['row']}: {err['error']}")

        lines.append("=" * 60)
        return "\n".join(lines)

    @staticmethod
    def generate_log_report(analyzer: LogFileAnalyzer) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("SYSTEM LOG ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        counts = analyzer.count_by_level()
        for level, count in counts.items():
            lines.append(f"{level}: {count}")

        errors = analyzer.extract_errors()
        lines.append(f"\nTotal Errors: {len(errors)}")

        for err in errors[-5:]:
            lines.append(f"- {err[:80]}")

        lines.append("=" * 60)
        return "\n".join(lines)

    @staticmethod
    def export_to_json(processor: ProductionDataProcessor, filepath: str) -> None:
        report_data = {
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'average_production': processor.calculate_daily_average(),
            'top_days': processor.get_top_days(5),
            'validation_errors': processor.validate_data(),
            'total_records': len(processor.data)
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print("Energy Data Analysis Toolkit")
    print("By: Areej - KKU CS Student")
    print("=" * 50)
    print("\nReady for data analysis!")

    try:
        processor = ProductionDataProcessor('examples/production_data.csv')
        report = ReportGenerator.generate_production_report(processor)

        print("\n" + "=" * 50)
        print(report)

    except Exception as e:
        print(f"\nError: {e}")

    print("\n" + "=" * 50)
    print("TODO - Features I want to add:")
    print("  - Database integration")
    print("  - Data visualization charts")
    print("  - Email notifications")
    print("  - Web dashboard interface")
    