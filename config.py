import os
from pathlib import Path

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.absolute()

# Data directories
DATA_DIR = os.path.join(ROOT_DIR, 'analysis', 'data')
REPORTS_DIR = os.path.join(ROOT_DIR, 'analysis', 'reports')
VISUALIZATIONS_DIR = os.path.join(ROOT_DIR, 'analysis', 'visualizations')
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'analysis', 'scripts')
EQUITY_DIR = os.path.join(ROOT_DIR, 'Equity')

# Create directories if they don't exist
for dir_path in [DATA_DIR, REPORTS_DIR, VISUALIZATIONS_DIR, SCRIPTS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# File paths
XRT_DATA_FILE = os.path.join(ROOT_DIR, 'search_results', 'search_xrt_20250121_175907.csv')
GME_BASKET_FILE = os.path.join(ROOT_DIR, 'GMEBASKET-2023-01-31.csv')
