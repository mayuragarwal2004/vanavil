"""
This script processes a CSV file containing image data by removing records with empty 'bw_ratio' values.

Usage:
    python remove_empty_bw_ratio.py input_csv output_csv

Arguments:
    input_csv  - Path to the input CSV file containing image data.
    output_csv - Path to save the output CSV file after removing records with empty 'bw_ratio' values.

The script loads the input CSV, removes any rows where the 'bw_ratio' column is empty, and saves the cleaned data
to the specified output CSV file.

Example:
    python remove_empty_bw_ratio.py stanford_processed_data.csv stanford_cleaned_data.csv

Dependencies:
    - pandas
    - argparse
"""


import pandas as pd
import argparse

def remove_empty_bw_ratio(input_csv, output_csv):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # Remove rows where 'bw_ratio' is empty
    df_cleaned = df.dropna(subset=['bw_ratio'])

    # Reset the 'id' column to reflect new row numbers
    df_cleaned.reset_index(drop=True, inplace=True)
    df_cleaned.index += 1
    df_cleaned['id'] = df_cleaned.index

    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_csv, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove records with empty 'bw_ratio' values from a CSV file.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to save the output CSV file")
    args = parser.parse_args()

    remove_empty_bw_ratio(args.input_csv, args.output_csv)
