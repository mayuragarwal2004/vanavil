from flask import Flask, jsonify, request, render_template
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the database and table name from .env file
DATABASE = os.getenv('DATABASE')
TABLE_NAME = os.getenv('TABLE_NAME')

app = Flask(__name__)

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows dict-like access to the database rows
    return conn

# Helper function to unlock entries that have been locked for more than 3 hours
def unlock_old_entries(cursor):
    three_hours_ago = datetime.now() - timedelta(hours=3)
    cursor.execute(f'''
        UPDATE {TABLE_NAME}
        SET is_locked = 0, locked_at = NULL
        WHERE is_locked = 1 AND locked_at <= ?
    ''', (three_hours_ago,))
    cursor.connection.commit()

# Route 1: Get top 10 entries where caption is empty and not locked
@app.route('/get_entries', methods=['GET'])
def get_entries():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Unlock old entries
    unlock_old_entries(cursor)

    # Fetch top 10 entries where caption is empty and the entry is not locked
    cursor.execute(f'''
        SELECT * FROM {TABLE_NAME} 
        WHERE caption IS NULL AND is_locked = 0
        LIMIT 10
    ''')

    entries = cursor.fetchall()

    # Mark these entries as locked and set the current timestamp
    ids = [entry['id'] for entry in entries]
    if ids:
        cursor.execute(f'''
            UPDATE {TABLE_NAME}
            SET is_locked = 1, locked_at = ?
            WHERE id IN ({",".join("?" for _ in ids)})
        ''', [datetime.now()] + ids)
        conn.commit()

    conn.close()

    # Convert rows to dictionaries for JSON response
    entries_list = [dict(entry) for entry in entries]
    return jsonify(entries_list), 200

# Route 2: Update entries with provided data
@app.route('/update_entries', methods=['POST'])
def update_entries():
    data = request.json
    if not data or 'entries' not in data:
        return jsonify({"error": "Invalid input, 'entries' required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Iterate over the provided entries and update them in the database
        for entry in data['entries']:
            cursor.execute(f'''
                UPDATE {TABLE_NAME}
                SET caption = ?, detailed_caption = ?, more_detailed_caption = ?, 
                    logo_detection_img = ?, objects_detected = ?, human_detected = ?, 
                    is_locked = 0, locked_at = NULL
                WHERE id = ?
            ''', (
                entry.get('caption'),
                entry.get('detailed_caption'),
                entry.get('more_detailed_caption'),
                entry.get('logo_detection_img'),
                entry.get('objects_detected'),
                entry.get('human_detected'),
                entry.get('id')
            ))
        
        conn.commit()
        return jsonify({"message": "Entries updated successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
# Route to render entry details in an HTML view
@app.route('/view/<int:entry_id>', methods=['GET'])
def view_entry(entry_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the entry data based on the ID
    cursor.execute(f'SELECT * FROM {TABLE_NAME} WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    
    if not entry:
        return f"Entry with ID {entry_id} not found.", 404

    conn.close()

    # Pass the entry to the HTML template and render it
    return render_template('view_entry.html', entry=entry)

# Test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Server is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)
