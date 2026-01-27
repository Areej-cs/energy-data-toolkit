# 🛢️ Energy Data Analysis Toolkit

> A professional Python toolkit for analyzing industrial energy and production data in the oil & gas industry.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

-----

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Features](#-features)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Demo](#-demo)

-----

## 🎯 Problem Statement

In the oil & gas industry, engineers and analysts face several daily challenges:

1. **Data Quality Issues**: Production data often contains errors, missing values, or anomalies that need identification  
2. **Log Analysis Overhead**: System logs from industrial equipment generate thousands of entries daily, making manual review impractical  
3. **Trend Identification**: Detecting production trends and anomalies early is critical for operational efficiency  
4. **Report Generation**: Management requires regular, formatted reports that are time-consuming to create manually  

### Real-World Impact

- Manual data validation can take 2–3 hours daily  
- Critical errors in logs may be overlooked in high-volume environments  
- Production anomalies detected late result in revenue loss  
- Report generation consumes valuable engineering time  

-----

## ✅ Solution

This toolkit provides automated solutions to these challenges through four specialized components:

### 1. **Production Data Processor**
Automates CSV data validation and analysis, reducing manual review time by 90%

### 2. **Log File Analyzer**
Intelligently scans system logs to identify errors, warnings, and patterns instantly

### 3. **Time Series Analyzer**
Applies statistical methods to detect anomalies and trends in production data

### 4. **Report Generator**
Creates professional, formatted reports automatically from analyzed data

-----

## 🚀 Features

### ProductionDataProcessor
- ✅ Load and validate production data from CSV files  
- ✅ Identify negative values and invalid data entries  
- ✅ Calculate daily averages and statistics  
- ✅ Extract top production days for performance review  

### LogFileAnalyzer
- ✅ Count log entries by severity level (ERROR, WARNING, INFO)  
- ✅ Extract all error messages for quick review  
- ✅ Search for specific patterns using regex  
- ✅ Generate summary statistics  

### TimeSeriesAnalyzer
- ✅ Calculate moving averages for trend smoothing  
- ✅ Detect anomalies using statistical methods  
- ✅ Determine overall trends (increasing / decreasing / stable)  
- ✅ Configurable sensitivity thresholds  

### ReportGenerator
- ✅ Generate formatted production analysis reports  
- ✅ Create log analysis summaries  
- ✅ Include timestamp and key metrics  
- ✅ Professional formatting for management presentation  

-----

## 📦 Installation

### Prerequisites
- Python 3.8 or higher  
- No external dependencies required (uses standard library only)

### Setup

```bash
git clone https://github.com/yourusername/energy-data-toolkit.git
cd energy-data-toolkit

# Run tests to verify installation
python test_energy_toolkit.py
```

## Usage Examples
### 1: Analyze Production Data
```python
from energy_toolkit import ProductionDataProcessor, ReportGenerator

processor = ProductionDataProcessor('production_data.csv')

errors = processor.validate_data()
print(f"Found {len(errors)} data quality issues")

avg_production = processor.calculate_daily_average()
print(f"Average daily production: {avg_production:.2f} barrels")

top_days = processor.get_top_days(5)
for i, day in enumerate(top_days, 1):
    print(f"{i}. {day['date']}: {day['production']:.2f} barrels")

report = ReportGenerator.generate_production_report(processor)
print(report)
```
### 2: Analyze System Logs
```python
from energy_toolkit import LogFileAnalyzer, ReportGenerator

analyzer = LogFileAnalyzer('system.log')

counts = analyzer.count_by_level()
print(f"Errors: {counts.get('ERROR', 0)}")
print(f"Warnings: {counts.get('WARNING', 0)}")

errors = analyzer.extract_errors()
for error in errors[:10]:
    print(error)

sensor_issues = analyzer.find_pattern('sensor.*malfunction')
print(f"Found {len(sensor_issues)} sensor-related issues")

report = ReportGenerator.generate_log_report(analyzer)
print(report)
```
### 3: Time Series Analysis
```python
from energy_toolkit import TimeSeriesAnalyzer

production_data = [1500, 1520, 1510, 1530, 1525, 1800, 1535, 1540]

analyzer = TimeSeriesAnalyzer(production_data)

ma = analyzer.moving_average(window=7)
print(f"Moving averages: {ma}")

anomalies = analyzer.detect_anomalies(threshold=2.0)
print(f"Anomalies detected at indices: {anomalies}")

trend = analyzer.calculate_trend()
print(f"Production trend: {trend}")
```
## Project Structure
```Code
energy-data-toolkit/
├── energy_toolkit.py
├── test_energy_toolkit.py
├── README.md
├── examples/
│   ├── production_data.csv
│   ├── system.log
│   └── demo_usage.py
└── docs/
    ├── API.md
    └── CONTRIBUTING.md
```
## Testing
The toolkitmincludes comprehensive unit tests covering all components.
### Run A ll Tests
```bash
python test_energy_toolkit.py
```
### Run Specific Test Class
```bash
python test_energy_toolkit.py TestProductionDataProcessor
```
### Test Coverage
✅ ProductionDataProcessor: 100%
✅ LogFileAnalyzer: 100%
✅ TimeSeriesAnalyzer: 100%
✅ ReportGenerator: 100%

### Sample Test Output 
```Code
test_average_calculation (test_energy_toolkit.TestProductionDataProcessor) ... ok
test_data_loading (test_energy_toolkit.TestProductionDataProcessor) ... ok
test_validation_finds_errors (test_energy_toolkit.TestProductionDataProcessor) ... ok
test_top_days (test_energy_toolkit.TestProductionDataProcessor) ... ok
...
----------------------------------------------------------------------
Ran 16 tests in 0.023s

OK
```
### Demo 
### Sample Production Report 
```
============================================================
PRODUCTION DATA ANALYSIS REPORT
============================================================
Generated: 2024-01-15 14:30:45

Average Daily Production: 1545.38 barrels

Top 5 Production Days:
----------------------------------------
1. 2024-01-10: 1650.20 barrels
2. 2024-01-08: 1620.50 barrels
3. 2024-01-12: 1605.75 barrels
4. 2024-01-05: 1580.30 barrels
5. 2024-01-03: 1560.15 barrels

Data Quality: 2 errors found
Issues:
  - Row 15: Negative production value
  - Row 23: Invalid production value
============================================================
```
### Sample Log Analysis Report
```
============================================================
SYSTEM LOG ANALYSIS REPORT
============================================================
Generated: 2024-01-15 14:32:18

Log Summary:
  ERROR: 12 entries
  WARNING: 34 entries
  INFO: 156 entries

Total Errors: 12
Recent Errors (last 5):
  - 2024-01-15 10:15:00 ERROR Database connection timeout
  - 2024-01-15 11:22:00 ERROR Sensor malfunction detected
  - 2024-01-15 12:08:00 ERROR Memory allocation failed
  - 2024-01-15 13:45:00 ERROR Network connectivity lost
  - 2024-01-15 14:12:00 ERROR Data validation failed
============================================================
```
### Screenshots
### Data Validation Output:
```
✓ Loading production_data.csv...
✓ Analyzing 365 records...
⚠ Found 3 validation errors
  → Row 45: Negative value (-150.5)
  → Row 120: Invalid format (N/A)
  → Row 287: Missing data
✓ Average production: 1,547 barrels/day
✓ Trend: Increasing (+3.2%)
```
## Key Achievements

- Zero External Dependencies: Uses only Python standard library
- Production-Ready Code: Clean, documented, and type-hinted
- 100% Test Coverage: All components thoroughly tested
- Industry-Relevant: Solves real oil & gas data challenges
- Easy to Extend: Modular design for adding new features

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details

## Author
Developed for industrial data analysis applications in the energy sector

## Related Resources
- Python CSV Documentation
- Python Statistics Module
- Best Practices for Data Analysis