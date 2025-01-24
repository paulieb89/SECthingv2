import pandas as pd
import zipfile
import os

def search_first_rows(zip_path, search_term, max_rows=50000):
    """
    Search only the first N rows of a file for quick testing.
    """
    print(f"Analyzing first {max_rows} rows of: {zip_path}")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get the first CSV/TSV file in the ZIP
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv') or f.endswith('.tsv')]
            if not csv_files:
                print("No CSV/TSV files found in ZIP")
                return
                
            csv_file = csv_files[0]
            print(f"Reading {csv_file}")
            
            # Read only specified number of rows
            try:
                df = pd.read_csv(zip_ref.open(csv_file), 
                               delimiter='\t' if csv_file.endswith('.tsv') else ',',
                               nrows=max_rows,
                               low_memory=False,
                               on_bad_lines='skip')
                
                # Convert all columns to string for searching
                for col in df.columns:
                    df[col] = df[col].astype(str)
                
                # Search across all columns
                matches = df[df.apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
                
                if matches.empty:
                    print("No matches found")
                    return
                
                print(f"\nFound {len(matches)} matches:")
                for idx, row in matches.iterrows():
                    print("\nMatch Details:")
                    print(f"ID: {row.get('Dissemination Identifier', 'Unknown')}")
                    print(f"Type: {row.get('Event type', 'Unknown')}")
                    print(f"Timestamp: {row.get('Event timestamp', 'Unknown')}")
                    print(f"UPI: {row.get('Unique Product Identifier', 'Unknown')}")
                    print(f"FISN: {row.get('UPI FISN', 'Unknown')}")
                    print(f"Underlier: {row.get('UPI Underlier Name', 'Unknown')}")
                    print("-" * 80)
                
            except pd.errors.EmptyDataError:
                print("File is empty")
            except Exception as read_error:
                print(f"Error reading file: {read_error}")
            
    except Exception as e:
        print(f"Error processing file: {e}")

# Example usage
if __name__ == "__main__":
    # Get the most recent equity swap file
    equity_dir = "EQUITY"
    zip_files = [f for f in os.listdir(equity_dir) if f.endswith('.zip')]
    if not zip_files:
        print("No ZIP files found in EQUITY directory")
        exit()
        
    # Sort by date and get most recent
    latest_file = sorted(zip_files)[-1]
    zip_path = os.path.join(equity_dir, latest_file)
    
    # Search term
    search_term = input("Enter search term (e.g., 'SWAP' or 'XRT'): ")
    
    # Perform quick search
    search_first_rows(zip_path, search_term)