"""
This script processes a CSV file containing image URLs and associated article URLs. The main tasks performed are:

1. **Whitespace Trimming**: Trims any leading or trailing whitespace from all fields in the CSV file.
2. **URL Validation and Construction**: 
   - Validates the `image_url` in each row.
   - If the `image_url` is invalid, a valid URL is constructed using the corresponding `article_url`.
3. **Duplicate Removal**:
   - After generating valid URLs, the script removes duplicate rows based on the `image_url` and `image_alt` columns.
4. **Invalid Link Removal**:
   - Optionally checks if the `image_url` points to a valid image and removes the row if the link is broken or outdated.
5. **Empty Image URL Removal**:
   - Automatically removes rows with empty `image_url` fields.
6. **ID Regeneration**:
   - The `id` column, representing row numbers, is regenerated after duplicates are removed to ensure it remains sequential.
7. **CSV File Saving**:
   - The processed data is saved to a new CSV file with "_updated" appended to the original file name or overwrites the original file based on user preference.

Usage:
- Specify the CSV file path when prompted.
- Choose whether to overwrite the original file or save the processed data to a new file.
- Optionally choose to remove invalid image URLs.
"""


import pandas as pd
from urllib.parse import urlparse, urljoin
import re
import os
import requests

# Regex pattern for validating URLs
URL_REGEX = re.compile(
    r'^(https?://)?'  # optional scheme
    r'([a-zA-Z0-9.-]+)'  # domain
    r'(:\d+)?'  # optional port
    r'(/.*)?$'  # optional path
)

def is_valid_url(url):
    # Returns False for relative URLs that start with "./" or "/" or "../"
    if pd.isna(url) or url.startswith(('./', '/', '../', "\\")):
        return False
    if not url.startswith(('http://', 'https://')):
        return False
    if url.startswith(('http://', 'https://')):
        return True
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
    elif image_url.startswith('/'):
        pass
    else:
        image_url = urldirpath + image_url

    return urljoin(base_url, os.path.normpath(image_url))

def is_image_url_valid(image_url):
    try:
        response = requests.get(image_url, timeout=5)
        # Check if the content type is an image
        return response.headers['Content-Type'].startswith('image')
    except (requests.RequestException, KeyError):
        return False

def process_csv(file_path, overwrite=False, remove_invalid_links=False):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Trim whitespace from all fields
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Ensure there are 'image_url', 'article_url', and 'id' columns
    if 'image_url' not in df.columns or 'article_url' not in df.columns or 'id' not in df.columns:
        print(f"No 'image_url', 'article_url', or 'id' column found in {file_path}.")
        return

    # Count and drop rows with empty 'image_url'
    initial_count = len(df)
    df = df.dropna(subset=['image_url'])
    empty_count = initial_count - len(df)
    
    if empty_count > 0:
        print(f"Removed {empty_count} rows with empty 'image_url'.")

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

        # Optionally remove rows with invalid image URLs
        if remove_invalid_links and not is_image_url_valid(df.at[i, 'image_url']):
            print(f"Invalid or broken image link found at index {i}: {df.at[i, 'image_url']}")
            df.drop(i, inplace=True)

    # Remove duplicate rows based on the updated image_url and image_alt
    if 'image_url' in df.columns and 'image_alt' in df.columns:
        before_dedup = len(df)
        df = df.drop_duplicates(subset=['image_url', 'image_alt'], keep='first')
        after_dedup = len(df)
        print(f"Removed {before_dedup - after_dedup} duplicate rows based on updated image_url and image_alt.")

    # Regenerate the 'id' column with new row numbers
    df['id'] = range(1, len(df) + 1)

    # Determine file path for saving
    if overwrite:
        new_file_path = file_path
    else:
        new_file_path = os.path.splitext(file_path)[0] + "_updated.csv"

    # Save the updated CSV
    df.to_csv(new_file_path, index=False)
    print(f"Completed processing. Updated file saved to {new_file_path}")

# Example usage
csv_file = input("Enter the path to the CSV file: ")
overwrite_choice = input("Do you want to overwrite the original file? (yes/no): ").strip().lower()
overwrite = overwrite_choice == 'yes'
remove_invalid_links_choice = input("Do you want to remove invalid image links? (yes/no): ").strip().lower()
remove_invalid_links = remove_invalid_links_choice == 'yes'
process_csv(csv_file, overwrite, remove_invalid_links)
