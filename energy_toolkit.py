"""
Energy Data Analysis Toolkit
A professional toolkit for analyzing industrial energy and production data.
Designed for oil & gas industry data processing and analysis.
"""

import csv
import re
from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict
import statistics


class ProductionDataProcessor:
    """
    Process and analyze daily production data from CSV files.
    Handles data validation, aggregation, and trend analysis.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = []
        self.load_data()

    def load_data(self) -> None:
        """Load production data from CSV file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
        except FileNotFoundError:
            raise Exception(f"File not found: {self.filepath}")

    def validate_data(self) -> List[Dict]:
        """
        Validate production data for errors and anomalies.
        Returns list of validation errors found.
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
        """Calculate average daily production."""
        productions = []
        for row in self.data:
            try:
                productions.append(float(row.get('production', 0)))
            except ValueError:
                continue
        return statistics.mean(productions) if productions else 0.0

    def get_top_days(self, n: int = 5) -> List[Dict]:
        """Get top N production days."""
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
    """
    Analyze system log files for errors, warnings, and patterns.
    Useful for monitoring industrial control systems.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.logs = []
        self.load_logs()

    def load_logs(self) -> None:
        """Load log file content."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.logs = f.readlines()
        except FileNotFoundError:
            raise Exception(f"Log file not found: {self.filepath}")

    def count_by_level(self) -> Dict[str, int]:
        """Count log entries by severity level (ERROR, WARNING, INFO)."""
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
        """Extract all error messages from logs."""
        return [log.strip() for log in self.logs if 'ERROR' in log.upper()]

    def find_pattern(self, pattern: str) -> List[Tuple[int, str]]:
        """
        Find specific pattern in logs.
        Returns list of (line_number, log_line) tuples.
        """
        matches = []
        for i, log in enumerate(self.logs):
            if re.search(pattern, log, re.IGNORECASE):
                matches.append((i + 1, log.strip()))
        return matches


class TimeSeriesAnalyzer:
    """
    Analyze time-series production data for trends and anomalies.
    Detects sudden drops, spikes, and calculates moving averages.
    """

    def __init__(self, data: List[float]):
        self.data = data

    def moving_average(self, window: int = 7) -> List[float]:
        """Calculate moving average with specified window size."""
        if len(self.data) < window:
            return self.data

        return [
            sum(self.data[i:i + window]) / window
            for i in range(len(self.data) - window + 1)
        ]

    def detect_anomalies(self, threshold: float = 2.0) -> List[int]:
        """
        Detect anomalies using standard deviation method.
        Returns indices of anomalous data points.
        """
        if len(self.data) < 2:
            return []

        mean = statistics.mean(self.data)
        stdev = statistics.stdev(self.data)

        anomalies = []
        for i, val in enumerate(self.data):
            z_score = abs((val - mean) / stdev) if stdev > 0 else 0
            if z_score > threshold:
                anomalies.append(i)
        return anomalies

    def calculate_trend(self) -> str:
        """Determine overall trend (increasing, decreasing, stable)."""
        if len(self.data) < 2:
            return "insufficient_data"

        mid = len(self.data) // 2
        avg_first = statistics.mean(self.data[:mid])
        avg_second = statistics.mean(self.data[mid:])

        diff_percent = ((avg_second - avg_first) / avg_first * 100) if avg_first > 0 else 0

        if diff_percent > 5:
            return "increasing"
        elif diff_percent < -5:
            return "decreasing"
        return "stable"


class ReportGenerator:
    """
    Generate professional analysis reports from processed data.
    Outputs formatted text reports suitable for management review.
    """

    @staticmethod
    def generate_production_report(processor: ProductionDataProcessor) -> str:
        report = [
            "=" * 60,
            "PRODUCTION DATA ANALYSIS REPORT",
            "=" * 60,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]

        avg = processor.calculate_daily_average()
        report.append(f"Average Daily Production: {avg:.2f} barrels\n")

        report.append("Top 5 Production Days:")
        report.append("-" * 40)
        for i, day in enumerate(processor.get_top_days(5), 1):
            report.append(f"{i}. {day['date']}: {day['production']:.2f} barrels")

        errors = processor.validate_data()
        report.append(f"\nData Quality: {len(errors)} errors found")
        for err in errors[:5]:
            report.append(f"  - Row {err['row']}: {err['error']}")

        report.append("=" * 60)
        return "\n".join(report)

    @staticmethod
    def generate_log_report(analyzer: LogFileAnalyzer) -> str:
        report = [
            "=" * 60,
            "SYSTEM LOG ANALYSIS REPORT",
            "=" * 60,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]

        counts = analyzer.count_by_level()
        report.append("Log Summary:")
        for level, count in counts.items():
            report.append(f"  {level}: {count} entries")

        errors = analyzer.extract_errors()
        report.append(f"\nTotal Errors: {len(errors)}")
        for err in errors[-5:]:
            report.append(f"  - {err[:80]}...")

        report.append("=" * 60)
        return "\n".join(report)


if __name__ == "__main__":
    print("Energy Data Analysis Toolkit")
    print("Ready for production data analysis!")
    print("\nExample usage:")
    print("  processor = ProductionDataProcessor('production_data.csv')")
    print("  report = ReportGenerator.generate_production_report(processor)")
    print("  print(report)")
