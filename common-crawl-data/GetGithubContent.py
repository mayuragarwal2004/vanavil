import requests

def fetch_github_file(github_url):
    try:
        # Replace 'github.com' with 'raw.githubusercontent.com' in the URL
        raw_url = github_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        
        # Send a GET request to fetch the raw file contents
        response = requests.get(raw_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            file_content = response.text
            return file_content
        else:
            return f"Failed to fetch file: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
github_file_url = 'https://github.com/mayuragarwal2004/sugam-frontend/blob/main/src/NoPage.jsx'
file_content = fetch_github_file(github_file_url)

print(file_content)
