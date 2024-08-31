import requests

class StackExchangeFetcher:
    def __init__(self, site='codereview', pagesize=10):
        self.site = site
        self.pagesize = pagesize
        self.base_url = "https://api.stackexchange.com/2.3/"
    
    def fetch_top_questions(self, page=1):
        # The filter includes body, title, and other details for the question
        url = f"{self.base_url}questions?order=desc&sort=votes&site={self.site}&page={page}&pagesize={self.pagesize}&filter=withbody"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            print(f"Failed to fetch questions. Status code: {response.status_code}")
            return []

    def fetch_answers_for_question(self, question_id):
        url = f"{self.base_url}questions/{question_id}/answers?order=desc&sort=votes&site={self.site}&filter=withbody"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            print(f"Failed to fetch answers for question {question_id}. Status code: {response.status_code}")
            return []

# Example usage
if __name__ == "__main__":
    fetcher = StackExchangeFetcher()
    
    # Fetch top questions
    top_questions = fetcher.fetch_top_questions()
    for question in top_questions:
        title = question.get('title')
        question_body = question.get('body')
        print(f"Title: {title}\nBody: {question_body}\n{'-'*80}")
