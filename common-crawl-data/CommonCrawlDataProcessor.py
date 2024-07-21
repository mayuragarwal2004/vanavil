"""
This script processes data from Common Crawl based on a specified search query.
It fetches the data, parses the JSON format, and saves it to a CSV file.
The user can specify the input search query, the output CSV filename, and whether to overwrite or append to the CSV file.

Classes:
    - CommonCrawlDataProcessor: Handles fetching, parsing, and saving the data.

Usage:
    - Enter your search query when prompted.
    - Specify the output CSV filename (defaults to commoncrawl_preprocessed_data.csv if left blank).
    - Choose whether to overwrite or append to the output CSV file (defaults to overwrite if left blank).
"""

import pandas as pd
import json
import requests
import os

class CommonCrawlDataProcessor:
    def __init__(self, search_query, csv_filename="commoncrawl_preprocessed_data.csv", mode="w"):
        self.search_query = search_query
        self.csv_filename = csv_filename
        self.mode = mode if mode in ["w", "a"] else "w"
    
    def fetch_commoncrawl_data(self):
        url = f"https://index.commoncrawl.org/CC-MAIN-2024-26-index?url={self.search_query}&output=json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
    
    def parse_json_data(self, data):
        data_lines = data.strip().split('\n')
        json_data = [json.loads(line) for line in data_lines]
        return json_data
    
    def create_dataframe(self, json_data):
        df = pd.DataFrame(json_data)
        df['warc_file_downloaded'] = False
        return df
    
    def save_to_csv(self, df):
        if self.mode == "a" and os.path.exists(self.csv_filename):
            existing_df = pd.read_csv(self.csv_filename)
            df = pd.concat([existing_df, df], ignore_index=True)
        df.to_csv(self.csv_filename, index=False)
        print(f"Data has been saved to {self.csv_filename}")
    
    def process_data(self):
        data = self.fetch_commoncrawl_data()
        json_data = self.parse_json_data(data)
        df = self.create_dataframe(json_data)
        self.save_to_csv(df)

# Example usage:
if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    csv_filename = input("Enter CSV filename (default: commoncrawl_preprocessed_data.csv): ")
    if not csv_filename:
        csv_filename = "commoncrawl_preprocessed_data.csv"

    mode = input("Enter mode (w for overwrite, a for append) [default: w]: ")
    if not mode:
        mode = "w"

    processor = CommonCrawlDataProcessor(search_query, csv_filename, mode)
    processor.process_data()

