import io
import requests
import warcio
import csv
from bs4 import BeautifulSoup
from datetime import datetime

# Define the input CSV file and output CSV file
input_csv = 'commoncrawl_ncsu_data.csv'
output_csv = 'output.csv'

def logger(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_line = f"{timestamp} - {text}\n"
    with open("logger.txt", "a") as file:
        file.write(new_line)

def extract_html_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    article_title = soup.title.string if soup.title else 'No Title'
    images = [(img.get('src'), img.get('alt')) for img in soup.find_all('img')]
    return article_title, images

# Read the input CSV file
with open(input_csv, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    records = list(reader)

logger("Started processing")

# Open the output CSV file for writing
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'urlkey', 'article_title', 'image_url', 'image_alt', 'article_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    unique_id = 1  # Initialize a unique ID counter

    # Loop through each record in the input CSV
    for idx, csv_record in enumerate(records):
        print("processing", csv_record['urlkey'])
        warc_filename = csv_record['filename']
        warc_record_offset = int(csv_record['offset'])
        warc_record_length = int(csv_record['length'])

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
                    article_title, images = extract_html_data(html)

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

logger("Processing completed")

