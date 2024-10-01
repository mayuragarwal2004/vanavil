import os
import requests
from dotenv import load_dotenv

# Modify the sample data in the main function
add_sample_snippet = True  # Set to True to add a sample snippet with comments
delete_sample_snippet = False  # Set to True to delete the sample snippet

class IBSConnector:
    def __init__(self, token):
        self.base_url = "https://backend.interviewblindspots.com/displaycode/"
        self.cookies = {"token": token}
        self.headers = { "Authorization": f"Token {token}" }

    def send_request(self, endpoint, payload=None, method='POST'):
        url = self.base_url + endpoint
        try:
            if method == 'POST':
                response = requests.post(url, cookies=self.cookies, data=payload, headers=self.headers)
            elif method == 'DELETE':
                response = requests.delete(url, cookies=self.cookies, headers=self.headers)
            elif method == 'GET':
                response = requests.get(url, cookies=self.cookies, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_username(self):
        # return "stackoverflow"
        # Fetch the username from the provided route
        endpoint = "api/v1/users/me/"
        response = self.send_request(endpoint, method='GET')
        print(response)
        if response:
            return response.get("username")
        else:
            print("Failed to retrieve username.")
            return None

    def create_snippet(self, title, text, language='clike', author=None):
        payload = {
            "title": title,
            "text": text,
            "language": language,
            "author": "https://backend.interviewblindspots.com/displaycode/users//"  # Include the author in the payload
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
        # Get the username to be used as the author
        author = self.get_username()
        if not author:
            print("Snippet creation aborted due to missing author.")
            return None

        snippet_response = self.create_snippet(title, text, language, author)
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
    
    print(ibs_connector.get_username())
    
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
