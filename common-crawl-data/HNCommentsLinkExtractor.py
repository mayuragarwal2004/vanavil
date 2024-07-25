import requests
from datetime import datetime, timedelta
import pytz
import re
import html

# Calculate timestamp for 24 hours ago
now = datetime.now(pytz.utc)
twenty_four_hours_ago = now - timedelta(days=1)
timestamp_24_hours_ago = int(twenty_four_hours_ago.timestamp())

# Define the API endpoint and parameters
url = "https://hn.algolia.com/api/v1/search"
params = {
    "tags": "comment",
    "numericFilters": f"created_at_i>{timestamp_24_hours_ago}",
    "query": "http" #youtu.be
}

# Construct the request URL
request_url = f"{url}?tags={params['tags']}&numericFilters={params['numericFilters']}&query={params['query']}"
print(f"Request URL: {request_url}\n")

# Make the request
response = requests.get(url, params=params)

print(response.text)

# youtube title
# youtube link
# HN comment
# type sense

# Check for successful response
if response.status_code == 200:
    data = response.json()
    comments = data.get('hits', [])
    url_pattern = re.compile(r'(https?://[^\s]+)')

    for comment in comments:
        print(f"Comment ID: {comment['objectID']}")
        print(f"Created At: {datetime.fromtimestamp(comment['created_at_i'])}")
        
        # Decode HTML entities
        comment_text = html.unescape(comment['comment_text'])
        print(f"Text: {comment_text}\n")

        # Extract and print links
        links = url_pattern.findall(comment_text)
        if links:
            print("Links:")
            for link in links:
                print(link)
        else:
            print("No links found.")

        print("\n" + "="*40 + "\n")
else:
    print(f"Error: {response.status_code}")
