import os
import requests
from dotenv import load_dotenv

class IBSConnector:
    def __init__(self, token):
        self.base_url = "https://backend.interviewblindspots.com/displaycode/"
        self.cookies = {"token": token}

    def send_request(self, endpoint, payload):
        url = self.base_url + endpoint
        try:
            response = requests.post(url, cookies=self.cookies, data=payload)
            response.raise_for_status()
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def create_snippet(self, title, text):
        payload = {
            "title": title,
            "text": text
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

    def create_snippet_with_comments(self, title, text, comments):
        snippet_response = self.create_snippet(title, text)
        if snippet_response:
            snippet_id = snippet_response.get("id")
            if snippet_id:
                self.add_comments(snippet_id, comments)
            else:
                print("Failed to retrieve snippet ID.")
        else:
            print("Failed to create snippet.")

# Load environment variables from .env file
load_dotenv()

# Example usage in other files
if __name__ == "__main__":
    tokenidfromenv = os.getenv("TOKEN_ID")

    if not tokenidfromenv:
        raise ValueError("TOKEN_ID not found in the environment variables.")

    ibs_connector = IBSConnector(tokenidfromenv)

    title = "new trial from python"
    text = "\"here \\n\\nwill \\n\\nbe solution \\n\\n\\nof the \\n\\nquestion\""

    comments = [
        {"line": 1, "text": "This is the first comment."},
        {"line": 2, "text": "This is the second comment."},
        {"line": 3, "text": "This is the third comment."}
    ]

    ibs_connector.create_snippet_with_comments(title, text, comments)
