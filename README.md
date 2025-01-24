# XRT Trading Data Analysis

This directory contains analysis of XRT (Total Return Swaps) trading data from January 2025.

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
this bad boy scrapes every/any type of archive from the SEC in raw form, turning anyone into an archivist.

install python 3.12.
then from command line, simply go to the folder containing the script and type:
python3 gamecockv1.py

it will auto install the required modules, and query for which archives to download.
almost everythings broken at the moment after that, but, AI is a very powerful tool on how to understand the filings inside the archives.
explore, poke around in the, and look things up. 
make learning great again :)
