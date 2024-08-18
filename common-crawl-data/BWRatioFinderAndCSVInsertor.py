import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import os
from datetime import datetime
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_black_and_white(url, tolerance=0):
    try:
        response = requests.get(url)
        response.raise_for_status()

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

def process_csv_files(file_paths, tolerance=0):
    log_file = "process_log.txt"
    
    with open(log_file, "a") as log:
        for file_path in file_paths:
            try:
                # Log the start time for the file
                start_time = datetime.now()
                log.write(f"Processing started for {file_path} at {start_time}\n")

                # Load the CSV file
                df = pd.read_csv(file_path)

                # Ensure there's an 'image_url' and 'article_url' column
                if 'image_url' not in df.columns or 'article_url' not in df.columns:
                    print(f"No 'image_url' or 'article_url' column found in {file_path}. Skipping this file.")
                    continue

                # Process each image URL using multithreading
                total_records = len(df)
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
                            new_file_path = os.path.splitext(file_path)[0] + "_bw_ratio.csv"
                            df.to_csv(new_file_path, index=False)
                            print(f"Record {i+1}/{total_records} in {file_path} processed and saved.")
                        except Exception as e:
                            print(f"Error in processing thread for record {i+1}: {e}")

                print(f"Completed processing {file_path}. Output saved to {new_file_path}")

                # Log the end time for the file
                end_time = datetime.now()
                log.write(f"Processing completed for {file_path} at {end_time}\n")
                log.write(f"Total records processed: {total_records}\n")

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                log.write(f"Error processing file {file_path}: {e}\n")

# Example usage
csv_files = [
    # "ncsu_processed_data.csv",
    "stanford_processed_data.csv",
    # "wikilinks_processed_data.csv"
]
tolerance = 0.1  # 10% tolerance for non-black and white pixels
process_csv_files(csv_files, tolerance)
