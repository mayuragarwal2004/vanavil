import os
import requests
from dotenv import load_dotenv

# Modify the sample data in the main function
add_sample_snippet = False  # Set to True to add a sample snippet with comments
delete_sample_snippet = False  # Set to True to delete the sample snippet

class IBSConnector:
    def __init__(self, token):
        self.base_url = "https://backend.interviewblindspots.com/displaycode/"
        self.cookies = {"token": token}

    def send_request(self, endpoint, payload=None, method='POST'):
        url = self.base_url + endpoint
        try:
            if method == 'POST':
                response = requests.post(url, cookies=self.cookies, data=payload)
            elif method == 'DELETE':
                response = requests.delete(url, cookies=self.cookies)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def create_snippet(self, title, text, language='clike'):
        payload = {
            "title": title,
            "text": text,
            "language": language  # Include the language in the payload
        }
        return self.send_request("snippets/", payload)

    def add_comments(self, snippet_id, comments):
        for comment in comments:
            payload = {
                "line": comment["line"],
                "snippetId": snippet_id,
                "text": comment["text"]
            }
            response = self.send_request("comments/", payload)
            if response:
                print(f"Comment added: {response}")
            else:
                print(f"Failed to add comment: {comment}")

    def create_snippet_with_comments(self, title, text, comments, language='clike'):
        snippet_response = self.create_snippet(title, text, language)
        if snippet_response:
            snippet_id = snippet_response.get("id")
            if snippet_id:
                self.add_comments(snippet_id, comments)
            else:
                print("Failed to retrieve snippet ID.")
        else:
            print("Failed to create snippet.")

    def delete_snippet(self, snippet_id):
        endpoint = f"snippets/{snippet_id}"
        response = self.send_request(endpoint, method='DELETE')
        if response:
            print(f"Snippet deleted: {response}")
        else:
            print(f"Failed to delete snippet with ID: {snippet_id}")

# Load environment variables from .env file
load_dotenv()

# Example usage in other files
if __name__ == "__main__":
    tokenidfromenv = os.getenv("TOKEN_ID")

    if not tokenidfromenv:
        raise ValueError("TOKEN_ID not found in the environment variables.")

    ibs_connector = IBSConnector(tokenidfromenv)
    
    
    if add_sample_snippet:
        # Example snippet creation
        title = "new trial from python"
        text = "\"here \\n\\nwill \\n\\nbe solution \\n\\n\\nof the \\n\\nquestion\""
        language = "python"  # Example language

        comments = [
            {"line": 1, "text": "This is the first comment."},
            {"line": 2, "text": "This is the second comment."},
            {"line": 3, "text": "This is the third comment."}
        ]

        snippet_response = ibs_connector.create_snippet_with_comments(title, text, comments, language=language)
        
        
    if delete_sample_snippet:
        # Example snippet deletion
        snippet_ids = ["215", "216"]  # Example snippet IDs to delete
        for snippet_id in snippet_ids:
            ibs_connector.delete_snippet(snippet_id)