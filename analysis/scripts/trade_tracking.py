import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(project_root))

from config import (
    ROOT_DIR,
    DATA_DIR,
    REPORTS_DIR,
    VISUALIZATIONS_DIR,
    XRT_DATA_FILE,
    GME_BASKET_FILE
)

class TradeAnalyzer:
    def __init__(self, data_dir=None):
        """Initialize the analyzer with configurable directories"""
        self.data_dir = data_dir or DATA_DIR
        self.reports_dir = REPORTS_DIR
        self.viz_dir = VISUALIZATIONS_DIR
        
        # Create directories if they don't exist
        for dir_path in [self.data_dir, self.reports_dir, self.viz_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def load_data(self, csv_file=None):
        """Load and preprocess the XRT data"""
        self.df = pd.read_csv(csv_file or XRT_DATA_FILE)
        self.clean_data()
        return self.df
    
    def load_gme_basket(self, basket_file=None):
        """Load GME basket data for cross-referencing"""
        self.gme_basket = pd.read_csv(basket_file or GME_BASKET_FILE)
        return self.gme_basket
    
    def clean_data(self):
        """Clean and preprocess the data"""
        # Convert date columns
        date_columns = ['Event timestamp', 'Execution Timestamp', 'Effective Date', 'Expiration Date']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Convert numeric columns
        self.df['Notional_Amount_Numeric'] = pd.to_numeric(
            self.df['Notional amount-Leg 1'].str.replace(',', ''), 
            errors='coerce'
        )
    
    def build_modification_graph(self):
        """Build a directed graph of trade modifications"""
        G = nx.DiGraph()
        
        # Add nodes and edges based on Original Dissemination Identifier
        for _, row in self.df.iterrows():
            dissem_id = row['Dissemination Identifier']
            orig_id = row['Original Dissemination Identifier']
            
            # Add the current trade as a node
            G.add_node(dissem_id, **row.to_dict())
            
            # If it's a modification, add an edge from original to current
            if pd.notna(orig_id):
                G.add_edge(orig_id, dissem_id)
        
        self.mod_graph = G
        return G
    
    def analyze_modification_chains(self):
        """Analyze chains of modifications for each trade"""
        chains = []
        
        # Find all root nodes (trades with no original ID)
        roots = [n for n in self.mod_graph.nodes() if self.mod_graph.in_degree(n) == 0]
        
        for root in roots:
            # Get all descendants (modifications) of this trade
            descendants = nx.descendants(self.mod_graph, root)
            if descendants:  # Only include chains with modifications
                chain = {
                    'root_id': root,
                    'modifications': list(descendants),
                    'chain_length': len(descendants) + 1
                }
                chains.append(chain)
        
        return chains
    
    def cross_reference_gme_basket(self):
        """Cross-reference trades with GME basket securities"""
        # Extract ISINs from the semicolon-separated string in the GME basket file
        gme_isins = set()
        for _, row in self.gme_basket.iterrows():
            isin_col = [col for col in row.index if 'US6541101050' in str(row[col])]
            if isin_col:
                isins = str(row[isin_col[0]]).split(';')
                gme_isins.update(isins)
        
        # Find trades involving GME basket securities
        basket_trades = self.df[self.df['Underlier ID-Leg 1'].isin(gme_isins)].copy()
        
        return basket_trades
    
    def generate_modification_report(self, chains, output_file):
        """Generate a detailed report of trade modification chains"""
        with open(output_file, 'w') as f:
            f.write("# Trade Modification Chain Analysis\n\n")
            f.write(f"Analysis generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Sort chains by length
            chains.sort(key=lambda x: x['chain_length'], reverse=True)
            
            for chain in chains:
                f.write(f"## Chain starting with Trade {chain['root_id']}\n\n")
                f.write(f"- Chain length: {chain['chain_length']}\n")
                f.write("- Modification sequence:\n")
                
                # Get full details for each trade in the chain
                all_trades = [chain['root_id']] + chain['modifications']
                for trade_id in all_trades:
                    trade_rows = self.df[self.df['Dissemination Identifier'].astype(str) == str(trade_id)]
                    if not trade_rows.empty:
                        trade = trade_rows.iloc[0]
                        f.write(f"\n### Trade {trade_id}\n")
                        f.write(f"- Action Type: {trade['Action type']}\n")
                        f.write(f"- Event Type: {trade['Event type']}\n")
                        f.write(f"- Event Timestamp: {trade['Event timestamp']}\n")
                        f.write(f"- Notional Amount: {trade['Notional amount-Leg 1']} {trade['Notional currency-Leg 1']}\n")
                        f.write(f"- Price: {trade['Price']}\n")
                        f.write(f"- Quantity: {trade['Total notional quantity-Leg 1']}\n")
                        f.write(f"- ISIN: {trade['Underlier ID-Leg 1']}\n\n")
                    else:
                        f.write(f"\n### Trade {trade_id}\n")
                        f.write("- Trade details not found in current dataset\n\n")
                
                f.write("---\n\n")
    
    def visualize_modification_network(self, output_file):
        """Create a visualization of the modification network"""
        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(self.mod_graph)
        
        # Draw the network
        nx.draw(self.mod_graph, pos,
                node_color='lightblue',
                node_size=500,
                arrowsize=20,
                with_labels=True,
                font_size=8)
        
        plt.title("Trade Modification Network")
        plt.savefig(output_file)
        plt.close()

def main(data_dir=None, data_file=None, basket_file=None):
    """
    Main function with configurable paths
    
    Args:
        data_dir: Optional override for data directory
        data_file: Optional override for XRT data file
        basket_file: Optional override for GME basket file
    """
    # Initialize analyzer
    analyzer = TradeAnalyzer(data_dir)
    
    # Load XRT data
    print("Loading XRT data...")
    analyzer.load_data(data_file)
    
    # Load GME basket data
    print("Loading GME basket data...")
    analyzer.load_gme_basket(basket_file)
    
    # Build modification graph
    print("Analyzing trade modifications...")
    G = analyzer.build_modification_graph()
    chains = analyzer.analyze_modification_chains()
    
    # Generate reports
    print("Generating reports...")
    report_file = os.path.join(REPORTS_DIR, 'modification_chains.md')
    analyzer.generate_modification_report(chains, report_file)
    
    # Generate visualization
    print("Generating visualizations...")
    viz_file = os.path.join(VISUALIZATIONS_DIR, 'modification_network.png')
    analyzer.visualize_modification_network(viz_file)
    
    # Cross-reference with GME basket
    print("Cross-referencing with GME basket...")
    basket_trades = analyzer.cross_reference_gme_basket()
    
    # Generate GME basket report
    basket_report = os.path.join(REPORTS_DIR, 'gme_basket_trades.md')
    with open(basket_report, 'w') as f:
        f.write("# GME Basket Related Trades\n\n")
        f.write(f"Analysis generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Found {len(basket_trades)} trades related to GME basket securities.\n\n")
        
        if not basket_trades.empty:
            for _, trade in basket_trades.iterrows():
                f.write(f"## Trade {trade['Dissemination Identifier']}\n\n")
                f.write(f"- ISIN: {trade['Underlier ID-Leg 1']}\n")
                f.write(f"- Action Type: {trade['Action type']}\n")
                f.write(f"- Notional Amount: {trade['Notional amount-Leg 1']} {trade['Notional currency-Leg 1']}\n")
                f.write(f"- Event Timestamp: {trade['Event timestamp']}\n")
                f.write(f"- Price: {trade['Price']}\n\n")
    
    print("\nAnalysis complete! Check the reports and visualizations directories for results.")

if __name__ == "__main__":
    # You can override default paths by passing arguments
    main()
