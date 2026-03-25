"""
Test Suite for Energy Data Analysis Toolkit
Testing all components to make sure everything works correctly
"""

import unittest
import os
import tempfile
from energy_toolkit import (
    ProductionDataProcessor,
    LogFileAnalyzer,
    TimeSeriesAnalyzer,
    ReportGenerator
)


class TestProductionDataProcessor(unittest.TestCase):
    """Tests for ProductionDataProcessor class"""

    def setUp(self):
        """Create test CSV file before each test"""
        self.test_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.csv'
        )

        self.test_file.write("date,production,well_id\n")
        self.test_file.write("2024-01-01,1500.5,WELL-001\n")
        self.test_file.write("2024-01-02,1600.2,WELL-001\n")
        self.test_file.write("2024-01-03,-100,WELL-001\n")
        self.test_file.write("2024-01-04,1550.8,WELL-001\n")
        self.test_file.write("2024-01-05,invalid,WELL-001\n")
        self.test_file.close()

        self.processor = ProductionDataProcessor(self.test_file.name)

    def tearDown(self):
        """Clean up test file after each test"""
        os.unlink(self.test_file.name)

    def test_data_loading(self):
        self.assertEqual(len(self.processor.data), 5)

    def test_validation_finds_errors(self):
        errors = self.processor.validate_data()
        self.assertGreater(len(errors), 0)

    def test_average_calculation(self):
        avg = self.processor.calculate_daily_average()
        self.assertGreater(avg, 0)

    def test_top_days(self):
        top = self.processor.get_top_days(3)
        self.assertLessEqual(len(top), 3)

        if len(top) > 1:
            self.assertGreaterEqual(
                top[0]['production'],
                top[1]['production']
            )


class TestLogFileAnalyzer(unittest.TestCase):
    """Tests for LogFileAnalyzer class"""

    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.log'
        )

        self.test_file.write("2024-01-01 10:00:00 INFO System started\n")
        self.test_file.write("2024-01-01 10:05:00 ERROR Database connection failed\n")
        self.test_file.write("2024-01-01 10:10:00 WARNING High CPU usage\n")
        self.test_file.write("2024-01-01 10:15:00 ERROR Sensor malfunction\n")
        self.test_file.write("2024-01-01 10:20:00 INFO Processing complete\n")
        self.test_file.close()

        self.analyzer = LogFileAnalyzer(self.test_file.name)

    def tearDown(self):
        os.unlink(self.test_file.name)

    def test_log_loading(self):
        self.assertEqual(len(self.analyzer.logs), 5)

    def test_count_by_level(self):
        counts = self.analyzer.count_by_level()
        self.assertEqual(counts.get('ERROR', 0), 2)
        self.assertEqual(counts.get('WARNING', 0), 1)
        self.assertEqual(counts.get('INFO', 0), 2)

    def test_extract_errors(self):
        errors = self.analyzer.extract_errors()
        self.assertEqual(len(errors), 2)

    def test_pattern_search(self):
        matches = self.analyzer.find_pattern('sensor')
        self.assertGreater(len(matches), 0)


class TestTimeSeriesAnalyzer(unittest.TestCase):
    """Tests for TimeSeriesAnalyzer class"""

    def setUp(self):
        self.normal_data = [100, 105, 103, 107, 106, 108, 110]
        self.anomaly_data = [100, 105, 103, 500, 106, 108, 110]

    def test_moving_average(self):
        analyzer = TimeSeriesAnalyzer(self.normal_data)
        ma = analyzer.moving_average(window=3)

        self.assertGreater(len(ma), 0)
        self.assertLess(len(ma), len(self.normal_data))

    def test_anomaly_detection(self):
        analyzer = TimeSeriesAnalyzer(self.anomaly_data)
        anomalies = analyzer.detect_anomalies(threshold=2.0)

        self.assertIn(3, anomalies)

    def test_trend_increasing(self):
        increasing_data = [100, 110, 120, 130, 140]
        analyzer = TimeSeriesAnalyzer(increasing_data)
        trend = analyzer.calculate_trend()

        self.assertEqual(trend, "increasing")

    def test_trend_stable(self):
        stable_data = [100, 102, 101, 103, 102]
        analyzer = TimeSeriesAnalyzer(stable_data)
        trend = analyzer.calculate_trend()

        self.assertEqual(trend, "stable")


class TestReportGenerator(unittest.TestCase):
    """Tests for ReportGenerator class"""

    def setUp(self):
        self.prod_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.csv'
        )
        self.prod_file.write("date,production,well_id\n")
        self.prod_file.write("2024-01-01,1500.5,WELL-001\n")
        self.prod_file.write("2024-01-02,1600.2,WELL-001\n")
        self.prod_file.close()

        self.log_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.log'
        )
        self.log_file.write("2024-01-01 10:00:00 INFO System started\n")
        self.log_file.write("2024-01-01 10:05:00 ERROR Connection failed\n")
        self.log_file.close()

    def tearDown(self):
        os.unlink(self.prod_file.name)
        os.unlink(self.log_file.name)

    def test_production_report(self):
        processor = ProductionDataProcessor(self.prod_file.name)
        report = ReportGenerator.generate_production_report(processor)

        self.assertIn("PRODUCTION DATA ANALYSIS REPORT", report)
        self.assertIn("Average Daily Production", report)

    def test_log_report(self):
        analyzer = LogFileAnalyzer(self.log_file.name)
        report = ReportGenerator.generate_log_report(analyzer)

        self.assertIn("SYSTEM LOG ANALYSIS REPORT", report)
        self.assertIn("ERROR", report)


if __name__ == "__main__":
    print("Running test suite...")
    print("=" * 50)
    unittest.main(verbosity=2)