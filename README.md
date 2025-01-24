# XRT Trading Data Analysis

This directory contains analysis of XRT (Total Return Swaps) trading data from January 2025. This repo is a test on  data from SECthingv2, thanks to artpersonnft for a giving us something really powerful and easy to use!


## Directory Structure

- `/data`: Raw and processed data files
  - Original CSV files
  - Cleaned and transformed datasets
  
- `/scripts`: Analysis scripts and utilities
  - Data cleaning scripts
  - Analysis tools
  - Data transformation utilities
  
- `/reports`: Analysis findings and documentation
  - Data quality reports
  - Outlier analysis
  - Trading patterns
  
- `/visualizations`: Charts and visual analysis
  - Price distribution charts
  - Volume analysis
  - Currency breakdown
  
## Initial Data Overview

The dataset contains equity swap transactions with the following key characteristics:

### Data Fields
- Transaction identifiers
- Trade details (timestamps, amounts, currencies)
- Asset information (ISIN, RIC codes)
- Pricing and quantity data

### Key Findings

1. Currency Distribution
   - Major: USD, JPY, CNY
   - Minor: ZAR (South African Rand)

2. Notable Outliers
   - Notional Amounts: JPY 470,000,000 to ZAR 40
   - Prices: Range from 1.05 to 75,714.33
   - Quantities: 5 to 170,000 shares

3. Date Range
   - Earliest execution: 2015-08-31
   - Latest expiration: 9999-12-31
   - Most activity: 2024-2026

## Research Focus Areas

1. Outlier Analysis
   - Investigate extreme price/quantity relationships
   - Validate unusual currency amounts
   
2. Data Quality
   - Standardize formatting
   - Handle missing values
   - Validate date ranges

3. Trading Patterns
   - Currency correlations
   - Volume analysis
   - Price trends

Forked from:
# SECthingv2
This bad boy scrapes every/any type of archive from the SEC in raw form, turning anyone into an archivist.

## Installation
1. Install Python 3.12
2. Clone this repository
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage
From command line, simply go to the folder containing the script and type:
```bash
python3 gamecockv1.py
```

It will auto install the required modules, and query for which archives to download.

## Analysis Tools
The repository now includes powerful analysis tools for examining trade data:

### Trade Analysis Scripts
Located in `analysis/scripts/`, these tools help analyze trade patterns, modifications, and relationships:

1. **Trade Tracking** (`trade_tracking.py`):
   - Analyzes trade modification chains
   - Identifies patterns in trade modifications
   - Cross-references with known baskets (e.g., GME basket)
   - Generates visualizations of trade networks

### Configuration
All paths and settings are managed in `config.py`. To analyze different data:

1. Update the paths in `config.py`:
   ```python
   XRT_DATA_FILE = '/path/to/your/data.csv'
   GME_BASKET_FILE = '/path/to/your/basket.csv'
   ```

2. Or pass custom paths when running the script:
   ```python
   from analysis.scripts.trade_tracking import main
   main(
       data_file='/path/to/data.csv',
       basket_file='/path/to/basket.csv'
   )
   ```

### Directory Structure
```
SECthingv2/
├── analysis/
│   ├── data/        # Raw data files
│   ├── reports/     # Generated analysis reports
│   ├── scripts/     # Analysis scripts
│   └── visualizations/ # Generated visualizations
├── config.py        # Configuration settings
└── requirements.txt # Project dependencies
```

## Development
Almost everything's broken at the moment after that, but AI is a very powerful tool on how to understand the filings inside the archives.
Explore, poke around in them, and look things up. 
Make learning great again :)

What the original does;

Getting Files

Different ways to download each type of file
Can download multiple files at once
Tries again if downloads fail
Handles network problems
Processing Files

Handles ZIP files efficiently
Reads CSV and TSV files
Processes files in chunks
Can work on multiple files at once
Searching Files

Flexible search options
Pattern matching
Cross-checks between different files
Combines results

Reliability

Handles errors well
Verifies downloads
Checks data is correct
Recovers from problems
Speed

Works on multiple things at once
Uses memory efficiently
Cleans up after itself
Shows progress

Flexibility

Works with many file types
Configurable search options
Different output formats
Works on different computers
