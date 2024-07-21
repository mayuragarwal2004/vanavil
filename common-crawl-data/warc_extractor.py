import io
import requests
import warcio

# Define the WARC file details
warc_filename = 'crawl-data/CC-MAIN-2024-26/segments/1718198862425.28/warc/CC-MAIN-20240623001858-20240623031858-00786.warc.gz'
warc_record_offset = 143289137
warc_record_length = 22613

# Send the request to get the specified range of bytes from the WARC file
response = requests.get(f'https://data.commoncrawl.org/{warc_filename}',
                        headers={'Range': f'bytes={warc_record_offset}-{warc_record_offset + warc_record_length - 1}'})

# Open the response content as a byte stream
with io.BytesIO(response.content) as stream:
    # Open a text file in write mode
    with open('output.txt', 'w', encoding='utf-8') as file:
        # Iterate over the records in the WARC file
        for record in warcio.ArchiveIterator(stream):
            # Read the HTML content from the record
            html = record.content_stream().read()
            # Decode the HTML content to a string and write it to the file
            file.write(html.decode('utf-8'))

