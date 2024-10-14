"""
This script processes a CSV file containing image URLs and associated article URLs to calculate the black-and-white (BW) ratio of each image.

### Key Features:
1. **Black-and-White Ratio Calculation**:
   - Calculates the ratio of black-and-white pixels in each image.
   - Handles both standard images and SVG files (converted to PNG for processing).

2. **Command-Line Arguments**:
   - `file`: Path to the CSV file to be processed.
   - `--tolerance`: Optional tolerance level for non-black and white pixels (default is 0.1).

3. **Multithreading**:
   - Uses multithreading to process image URLs concurrently, improving performance.

4. **Logging**:
   - Logs processing start and end times, as well as any errors encountered, to `process_log.txt`.

5. **Output**:
   - Saves the processed data to a new CSV file with `_bw_ratio` appended to the original file name.

### Usage:
To run the script, use the command line to specify the file and tolerance level (if desired). For example:

    python BWRatioFinderAndCSVInsertor.py path/to/your_file.csv --tolerance 0.1

Replace `BWRatioFinderAndCSVInsertor.py` with the name of your script file and adjust the `path/to/your_file.csv` and `--tolerance` values as needed.
"""


import argparse
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import os
from datetime import datetime
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import cairosvg

def is_black_and_white(url, tolerance=0):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Check the content type
        content_type = response.headers.get('Content-Type', '')
        if 'svg' in content_type:
            # Convert SVG to PNG
            png_data = cairosvg.svg2png(bytestring=response.content)
            img = Image.open(BytesIO(png_data))
        else:
            img = Image.open(BytesIO(response.content))

        img = img.convert('RGB')
        pixels = list(img.getdata())
        
        bw_count = 0
        total_pixels = len(pixels)
        for pixel in pixels:
            r, g, b = pixel
            if abs(r - g) <= tolerance and abs(g - b) <= tolerance and abs(b - r) <= tolerance:
                bw_count += 1

        bw_ratio = bw_count / total_pixels
        return bw_ratio
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

def process_record(index, row, df, tolerance):
    try:
        image_url = row['image_url']
        
        # Check if image_url starts with "/"
        if image_url.startswith('/'):
            article_url = row['article_url']
            # Extract domain from article_url
            parsed_url = urlparse(article_url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            # Join the domain with the image_url
            image_url = urljoin(base_url, image_url)
        
        bw_ratio = is_black_and_white(image_url, tolerance)
        df.at[index, 'bw_ratio'] = bw_ratio
    except Exception as e:
        print(f"Error processing record {index+1}: {e}")
        df.at[index, 'bw_ratio'] = None  # Set a default value in case of error
    return index

def process_csv_file(file_path, tolerance=0):
    log_file = "process_log.txt"
    
    with open(log_file, "a") as log:
        try:
            # Log the start time for the file
            start_time = datetime.now()
            log.write(f"Processing started for {file_path} at {start_time}\n")

            # Load the input CSV file
            df = pd.read_csv(file_path)

            # Ensure there's an 'image_url', 'article_url', and 'id' column
            if 'image_url' not in df.columns or 'article_url' not in df.columns or 'id' not in df.columns:
                print(f"No 'image_url', 'article_url', or 'id' column found in {file_path}. Skipping this file.")
                return

            # Check if the output file exists
            output_file_path = os.path.splitext(file_path)[0] + "_bw_ratio.csv"
            if os.path.exists(output_file_path):
                # Load the output CSV to find the last processed ID
                df_output = pd.read_csv(output_file_path)
                last_processed_id = df_output['id'].max()

                # Filter the input CSV to start processing from the last processed ID
                df = df[df['id'] > last_processed_id]
                print(f"Resuming processing from ID {last_processed_id + 1} for {file_path}.")
            else:
                print(f"No output file found. Starting from the beginning for {file_path}.")
            
            total_records = len(df)
            if total_records == 0:
                print(f"All records have already been processed for {file_path}.")
                return

            # Process each image URL using multithreading
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {
                    executor.submit(process_record, i, row, df, tolerance): i
                    for i, row in df.iterrows()
                }

                for future in as_completed(futures):
                    i = futures[future]
                    try:
                        # Check if the future was completed successfully
                        future.result()
                        # Save the CSV after processing each record
                        df_output = pd.concat([df_output, df], ignore_index=True) if os.path.exists(output_file_path) else df
                        df_output.to_csv(output_file_path, index=False)
                        print(f"Record {i+1}/{total_records} in {file_path} processed and saved.")
                    except Exception as e:
                        print(f"Error in processing thread for record {i+1}: {e}")

            print(f"Completed processing {file_path}. Output saved to {output_file_path}")

            # Log the end time for the file
            end_time = datetime.now()
            log.write(f"Processing completed for {file_path} at {end_time}\n")
            log.write(f"Total records processed: {total_records}\n")

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            log.write(f"Error processing file {file_path}: {e}\n")

def main():
    parser = argparse.ArgumentParser(description="Process CSV files and calculate black-and-white ratio for images.")
    parser.add_argument("file", type=str, help="Path to the CSV file to be processed.")
    parser.add_argument("--tolerance", type=float, default=0.1, help="Tolerance level for non-black and white pixels (default is 0.1).")
    
    args = parser.parse_args()
    process_csv_file(args.file, args.tolerance)

if __name__ == "__main__":
    main()
