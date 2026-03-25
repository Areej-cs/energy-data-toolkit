# Energy Data Analysis Toolkit

A Python toolkit for analyzing industrial energy and production data.

## About

I built this project while learning about data analysis and its applications in the oil & gas industry. As a Computer Science student at KKU, I wanted to create something practical that goes beyond typical academic projects.

**What started it:** Got interested in how the energy sector uses data analysis after reading about industry applications in my Data Structures course.

**Current status:** Working and functional. Still adding features as I learn more.

## Features

The toolkit can:

- Process production data from CSV files
- Validate data and catch common errors
- Analyze system log files
- Calculate statistics (averages, trends, etc.)
- Detect anomalies in time-series data
- Generate formatted reports

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Areej-cs/energy-data-toolkit.git
cd energy-data-toolkit

# No external libraries needed - uses Python standard library
python --version  # Make sure you have Python 3.6+
```
## Basic Usage
from energy_toolkit import ProductionDataProcessor, ReportGenerator

# Load your data
processor = ProductionDataProcessor('production_data.csv')

# Generate analysis report
report = ReportGenerator.generate_production_report(processor)
print(report)

# Check for data quality issues
errors = processor.validate_data()
print(f"Found {len(errors)} errors")
## Working with Logs
from energy_toolkit import LogFileAnalyzer

# Analyze log files
analyzer = LogFileAnalyzer('system.log')

# Count errors by type
counts = analyzer.count_by_level()
print(f"Errors: {counts.get('ERROR', 0)}")

# Find specific issues
sensor_issues = analyzer.find_pattern('sensor.*fault')

## Time Series Analysis
from energy_toolkit import TimeSeriesAnalyzer

# Your production data
daily_production = [1500, 1520, 1510, 1530, 1525, 1540]

analyzer = TimeSeriesAnalyzer(daily_production)

# Check trend
trend = analyzer.calculate_trend()
print(f"Trend: {trend}")  # increasing, decreasing, or stable

# Find anomalies
anomalies = analyzer.detect_anomalies(threshold=2.0)
if anomalies:
    print(f"Found unusual values at: {anomalies}")

    
