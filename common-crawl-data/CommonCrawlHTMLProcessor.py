"""
Common Crawl HTML Processor

This script processes Common Crawl data based on an input CSV file, fetches the corresponding WARC files, 
extracts HTML data, and writes the results to a new CSV file with successful entries. It also updates the 
original input CSV with status and remarks for each record, indicating whether the processing was completed 
successfully or encountered an error.

Features:
- Reads records from an input CSV file and fetches the specified WARC files.
- Extracts HTML content and image data from WARC files.
- Writes successful entries to an output CSV file.
- Updates the original input CSV with processing status and error details.

Usage:
1. Provide the input CSV filename, which should include columns such as 'filename', 'offset', 'length', and 'urlkey'.
2. Specify an output CSV filename (default: commoncrawl_processed_data.csv) where successful entries will be saved.
3. Choose the mode for writing to the output file (overwrite 'w' or append 'a').
4. The script will process each record, handle errors gracefully, and update both the output and input CSV files.

Dependencies:
- requests
- warcio
- beautifulsoup4
- csv
- io
- datetime
- os

Example usage:
    python CommonCrawlHTMLProcessor.py
"""

import io
import requests
import warcio
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import os

class CommonCrawlHTMLProcessor:
    def __init__(self, input_csv, output_csv="commoncrawl_processed_data.csv", mode="w"):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.log_file = "logger.txt"
        self.mode = mode if mode in ["w", "a"] else "w"

    def logger(self, text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_line = f"{timestamp} - {text}\n"
        with open(self.log_file, "a") as file:
            file.write(new_line)

    def extract_html_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        article_title = soup.title.string if soup.title else 'No Title'
        images = [(img.get('src'), img.get('alt')) for img in soup.find_all('img')]
        return article_title, images

    def process_records(self):
        # Read the input CSV file and add status and remark columns
        with open(self.input_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_fieldnames = reader.fieldnames
            
            # Ensure 'status' and 'remark' are included
            if 'status' not in existing_fieldnames:
                existing_fieldnames.append('status')
            if 'remark' not in existing_fieldnames:
                existing_fieldnames.append('remark')
            
            records = list(reader)

        self.logger("Started processing")

        # Create or open the output CSV file for writing successful entries
        write_header = not os.path.exists(self.output_csv) or self.mode == "w"
        with open(self.output_csv, self.mode, newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'urlkey', 'article_title', 'image_url', 'image_alt', 'article_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()

            unique_id = 1  # Initialize a unique ID counter

            # Loop through each record in the input CSV
            for idx, csv_record in enumerate(records):
                print(f"Processing record {idx + 1}/{len(records)}: {csv_record['urlkey']}")
                warc_filename = csv_record['filename']
                warc_record_offset = int(csv_record['offset'])
                warc_record_length = int(csv_record['length'])

                try:
                    # Fetch the specified range of bytes from the WARC file
                    response = requests.get(f'https://data.commoncrawl.org/{warc_filename}',
                                            headers={'Range': f'bytes={warc_record_offset}-{warc_record_offset + warc_record_length - 1}'})

                    # Open the response content as a byte stream
                    with io.BytesIO(response.content) as stream:
                        # Iterate over the records in the WARC file
                        for record in warcio.ArchiveIterator(stream):
                            if record.rec_type == 'response':
                                # Read the HTML content from the record
                                html = record.content_stream().read()

                                # Extract the required data from the HTML
                                article_title, images = self.extract_html_data(html)

                                # Write each image data to the output CSV
                                for image_url, image_alt in images:
                                    writer.writerow({
                                        'id': unique_id,
                                        'urlkey': csv_record['urlkey'],
                                        'article_title': article_title,
                                        'image_url': image_url,
                                        'image_alt': image_alt,
                                        'article_url': csv_record['url']
                                    })
                                    unique_id += 1  # Increment the unique ID counter

                    # Update the record with status and remark
                    csv_record['status'] = 'Completed'
                    csv_record['remark'] = ''
                except Exception as e:
                    # Log the error
                    self.logger(f"Error processing record {csv_record['urlkey']}: {str(e)}")

                    # Update the record with status and remark
                    csv_record['status'] = 'Error'
                    csv_record['remark'] = str(e)

        # Write updated records with status and remark back to the input CSV
        with open(self.input_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=existing_fieldnames)
            writer.writeheader()
            writer.writerows(records)

        self.logger("Processing completed")

# Example usage:
if __name__ == "__main__":
    input_csv = input("Enter input CSV filename: ")
    if not input_csv:
        print("Input CSV filename is required.")
        exit(1)
    
    output_csv = input("Enter output CSV filename (default: commoncrawl_processed_data.csv): ")
    if not output_csv:
        output_csv = "commoncrawl_processed_data.csv"

    mode = input("Enter mode (w for overwrite, a for append) [default: w]: ")
    if not mode:
        mode = "w"

    processor = CommonCrawlHTMLProcessor(input_csv, output_csv, mode)
    processor.process_records()

