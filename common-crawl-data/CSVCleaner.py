"""
This script processes a CSV file containing image URLs and associated article URLs. The main tasks performed are:

1. **Whitespace Trimming**: Trims any leading or trailing whitespace from all fields in the CSV file.
2. **URL Validation and Construction**: 
   - Validates the `image_url` in each row.
   - If the `image_url` is invalid, a valid URL is constructed using the corresponding `article_url`.
3. **Duplicate Removal**:
   - After generating valid URLs, the script removes duplicate rows based on the `image_url` and `image_alt` columns.
4. **ID Regeneration**:
   - The `id` column, representing row numbers, is regenerated after duplicates are removed to ensure it remains sequential.
5. **CSV File Saving**:
   - The processed data is saved to a new CSV file with "_updated" appended to the original file name.

Usage:
- Specify the CSV file path in the `csv_file` variable.
- Run the script to process the file and generate an updated version with the above modifications.
"""

import pandas as pd
from urllib.parse import urlparse, urljoin
import re
import os

# Regex pattern for validating URLs
URL_REGEX = re.compile(
    r'^(https?://)?'  # optional scheme
    r'([a-zA-Z0-9.-]+)'  # domain
    r'(:\d+)?'  # optional port
    r'(/.*)?$'  # optional path
)

def is_valid_url(url):
    # Returns False for relative URLs that start with "./" or "/" or "../"
    if url.startswith(('./', '/', '../', "\\")):
        return False
    if not url.startswith(('http://', 'https://')):
        return False
    return re.match(URL_REGEX, url) is not None

def construct_valid_image_url(image_url, article_url):
    parsed_article_url = urlparse(article_url)
    base_url = f"{parsed_article_url.scheme}://{parsed_article_url.netloc}"
    
    urldirpath = parsed_article_url.path.split("/")
    if len(urldirpath) >= 1:
        if urldirpath[-1] == '':
            urldirpath.pop()
        if urldirpath[-1].find('.') != -1:
            urldirpath.pop()
    
    urldirpath = "/".join(urldirpath) + "/"
    
    if image_url.startswith('./'):
        # Remove the leading "./"
        image_url = urldirpath + image_url[2:]
    elif image_url.startswith('../'):
        # Handle URLs with "../" by normalizing the path
        combined_url = urljoin(base_url, urldirpath)        
        combined_url = urljoin(combined_url, image_url)
        image_url = os.path.normpath(combined_url.replace(base_url, ''))
        return urljoin(base_url, image_url)
    else:
        image_url = urldirpath + image_url

    return urljoin(base_url, os.path.normpath(image_url))

def process_csv(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Trim whitespace from all fields
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Ensure there are 'image_url', 'article_url', and 'id' columns
    if 'image_url' not in df.columns or 'article_url' not in df.columns or 'id' not in df.columns:
        print(f"No 'image_url', 'article_url', or 'id' column found in {file_path}.")
        return

    # Process each record to update image URLs
    for i, row in df.iterrows():
        image_url = row['image_url']
        article_url = row['article_url']

        # Check if the image_url is valid
        if not is_valid_url(image_url):
            print(f"Invalid image_url found at index {i}: {image_url}")
            # Construct a valid image_url
            valid_image_url = construct_valid_image_url(image_url, article_url)
            df.at[i, 'image_url'] = valid_image_url
            print(f"Updated image_url at index {i}: {valid_image_url}")

    # Remove duplicate rows based on the updated image_url and image_alt
    if 'image_url' in df.columns and 'image_alt' in df.columns:
        before_dedup = len(df)
        df = df.drop_duplicates(subset=['image_url', 'image_alt'], keep='first')
        after_dedup = len(df)
        print(f"Removed {before_dedup - after_dedup} duplicate rows based on updated image_url and image_alt.")

    # Regenerate the 'id' column with new row numbers
    df['id'] = range(1, len(df) + 1)

    # Save the updated CSV
    new_file_path = os.path.splitext(file_path)[0] + "_updated.csv"
    df.to_csv(new_file_path, index=False)
    print(f"Completed processing. Updated file saved to {new_file_path}")

# Example usage
csv_file = input("Enter the path to the CSV file: ")
process_csv(csv_file)
