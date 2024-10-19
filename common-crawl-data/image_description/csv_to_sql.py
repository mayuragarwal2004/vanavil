import sqlite3
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Function to create the table with additional columns and is_locked flag
def create_table(cursor, table_name):
    try:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                url_key TEXT,
                article_title TEXT,
                image_url TEXT,
                image_alt TEXT,
                article_url TEXT,
                bw_ratio REAL,
                caption TEXT,
                detailed_caption TEXT,
                more_detailed_caption TEXT,
                logo_detection_img TEXT,
                objects_detected TEXT,
                human_detected TEXT,  -- New column added here
                is_locked INTEGER DEFAULT 0,  -- Tracks if an entry is sent to a client
                locked_at TIMESTAMP  -- Tracks when the entry was locked
            )
        ''')
        print(f"Table '{table_name}' created successfully (if not existing).")
    except sqlite3.Error as e:
        print(f"Error creating table '{table_name}': {e}")

# Function to insert CSV data into the SQLite database
def insert_csv_to_db(cursor, table_name, csv_file):
    try:
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                cursor.execute(f'''
                    INSERT INTO {table_name} (id, url_key, article_title, image_url, image_alt, article_url, bw_ratio,
                                              caption, detailed_caption, more_detailed_caption, logo_detection_img, 
                                              objects_detected, human_detected)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['id'],
                    row['urlkey'],
                    row['article_title'],
                    row['image_url'],
                    row['image_alt'] if row['image_alt'] else None,  # Handle empty alt
                    row['article_url'],
                    float(row['bw_ratio']) if row['bw_ratio'] else None,  # Handle missing bw_ratio
                    None,  # caption (empty for now)
                    None,  # detailed_caption (empty for now)
                    None,  # more_detailed_caption (empty for now)
                    None,  # logo_detection_img (empty for now)
                    None,  # objects_detected (empty for now)
                    None   # human_detected (empty for now)
                ))
        print(f"Data successfully inserted into table '{table_name}'.")
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found. Please provide a valid file path.")
    except Exception as e:
        print(f"Error inserting data into table '{table_name}': {e}")

# Main function to handle database connection and user inputs
def main():
    # Accept database, table, and CSV file names from user input
    database_name = os.getenv('DATABASE')
    table_name = input("Enter the table name: ")
    csv_file = input("Enter the CSV file name (e.g., 'your_file.csv'): ")

    # Check if the CSV file exists before proceeding
    if not os.path.exists(csv_file):
        print(f"Error: The file '{csv_file}' does not exist. Please check the path.")
        return

    # Create a connection to the SQLite database
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        print(f"Connected to the database '{database_name}'.")

        # Create the table
        create_table(cursor, table_name)

        # Insert data from CSV to the SQLite database
        insert_csv_to_db(cursor, table_name, csv_file)

        # Commit changes and close the connection
        conn.commit()
        print("Changes committed to the database.")
    except sqlite3.Error as e:
        print(f"Error connecting to database '{database_name}': {e}")
    finally:
        if conn:
            conn.close()
            print(f"Connection to '{database_name}' closed.")

if __name__ == "__main__":
    main()
