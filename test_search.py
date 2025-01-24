import pandas as pd
import zipfile
import os
from datetime import datetime

def search_single_file(zip_path, search_term):
    """
    Search a single equity swap file for specific terms.
    """
    print(f"Analyzing file: {zip_path}")
    
    # Create results directory if it doesn't exist
    results_dir = "search_results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(results_dir, f"search_{search_term}_{timestamp}.csv")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get the first CSV/TSV file in the ZIP
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv') or f.endswith('.tsv')]
            if not csv_files:
                print("No CSV/TSV files found in ZIP")
                return
                
            csv_file = csv_files[0]
            print(f"Reading {csv_file}")
            
            # Read in chunks to manage memory
            chunk_size = 10000
            total_matches = 0
            all_matches = []  # Store all matches for saving to CSV
            
            try:
                chunks = pd.read_csv(zip_ref.open(csv_file), 
                                   delimiter='\t' if csv_file.endswith('.tsv') else ',',
                                   chunksize=chunk_size,
                                   low_memory=False,
                                   on_bad_lines='skip')
                
                for i, chunk in enumerate(chunks):
                    try:
                        # Convert all columns to string for searching
                        for col in chunk.columns:
                            chunk[col] = chunk[col].astype(str)
                        
                        # Search across all columns
                        matches = chunk[chunk.apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
                        
                        if not matches.empty:
                            # Add matches to our collection
                            all_matches.append(matches)
                            total_matches += len(matches)
                            
                            # Display match details
                            for idx, row in matches.iterrows():
                                print("\nMatch Details:")
                                print(f"ID: {row.get('Dissemination Identifier', 'Unknown')}")
                                print(f"Type: {row.get('Event type', 'Unknown')}")
                                print(f"Timestamp: {row.get('Event timestamp', 'Unknown')}")
                                print(f"UPI: {row.get('Unique Product Identifier', 'Unknown')}")
                                print(f"FISN: {row.get('UPI FISN', 'Unknown')}")
                                print(f"Underlier: {row.get('UPI Underlier Name', 'Unknown')}")
                                print("-" * 80)
                        
                        print(f"Processed chunk {i+1} ({chunk_size} rows)", end='\r')
                        
                    except Exception as chunk_error:
                        print(f"\nError processing chunk {i+1}: {chunk_error}")
                        continue
                
                # Save all matches to CSV if we found any
                if all_matches:
                    pd.concat(all_matches).to_csv(output_file, index=False)
                    print(f"\nTotal matches found: {total_matches}")
                    print(f"Results saved to: {output_file}")
                else:
                    print("\nNo matches found")
                
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
    
    # Perform search
    search_single_file(zip_path, search_term)