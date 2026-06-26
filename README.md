# CLI Automation Toolkit

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Ruff](https://img.shields.io/badge/code%20style-ruff-red)

A production-grade Python CLI toolkit for file processing, data cleaning, and report generation. Built with Click and pandas, supporting stdin/stdout piping for seamless shell integration.

---

## Features

- **CSV processing** — merge multiple CSVs, convert between CSV and JSON
- **Data cleaning** — deduplicate rows, fill missing values, filter by column value
- **Report generation** — summary statistics (JSON), formatted Excel export with styling
- **Pipe support** — all commands accept stdin and stdout via `-`
- **Zero comments** — clean, type-hinted, ruff-compliant codebase

---

## Installation

```bash
git clone <repo-url> && cd cli-automation-toolkit
pip install -r requirements.txt
```

---

## Command Reference

| Command | Description |
|---|---|
| `process merge <files>... -o <output>` | Merge multiple CSV files row-wise |
| `process convert <input> -f json\|csv -o <output>` | Convert between CSV and JSON |
| `clean deduplicate <file> -o <output>` | Remove duplicate rows |
| `clean fillna <file> --strategy mean\|median\|mode [--column <col>] -o <output>` | Fill missing values |
| `clean filter <file> --column <col> --value <val> -o <output>` | Filter rows by column value |
| `report stats <file> -o <output>` | Generate summary statistics as JSON |
| `report excel <file> -o <output>` | Export data to styled Excel workbook |

---

## Usage

### Process

```bash
# Merge multiple CSVs
python -m src.cli process merge data/file1.csv data/file2.csv -o merged.csv

# Convert CSV to JSON
python -m src.cli process convert data/sample.csv -f json -o output.json

# Convert JSON to CSV
python -m src.cli process convert data.json -f csv -o output.csv
```

### Clean

```bash
# Remove duplicate rows
python -m src.cli clean deduplicate data/sample.csv -o clean.csv

# Fill missing values (mean strategy, all numeric columns)
python -m src.cli clean fillna data/sample.csv --strategy mean -o filled.csv

# Fill missing values in a specific column
python -m src.cli clean fillna data/sample.csv --strategy median --column salary -o filled.csv

# Filter rows by value
python -m src.cli clean filter data/sample.csv --column department --value Engineering -o filtered.csv
```

### Report

```bash
# Generate summary statistics
python -m src.cli report stats data/sample.csv -o stats.json

# Export formatted Excel
python -m src.cli report excel data/sample.csv -o report.xlsx
```

### Piping

```bash
# Pipe data between commands
python -m src.cli process convert data/sample.csv -f json | python -m src.cli process convert - -f csv -o roundtrip.csv
```

---

## Development

```bash
pip install -r requirements.txt
python -m pytest tests/ -v --cov=src
ruff check src/ tests/
```

---

## License

MIT
