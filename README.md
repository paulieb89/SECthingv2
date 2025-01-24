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
