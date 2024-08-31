import requests
import html2text
from bs4 import BeautifulSoup

class StackExchangeFetcher:
    def __init__(self, site='codereview', pagesize=10):
        self.site = site
        self.pagesize = pagesize
        self.base_url = "https://api.stackexchange.com/2.3/"
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False  # Keep links in the markdown output
    
    def fetch_top_questions(self, page=1):
        url = f"{self.base_url}questions?order=desc&sort=votes&site={self.site}&page={page}&pagesize={self.pagesize}&filter=withbody"
        response = requests.get(url)
        if response.status_code == 200:
            questions = response.json().get('items', [])
            for question in questions:
                question['body'] = self.convert_html_to_text(question.get('body', ''))
            return questions
        else:
            print(f"Failed to fetch questions. Status code: {response.status_code}")
            return []

    def fetch_answers_for_question(self, question_id):
        url = f"{self.base_url}questions/{question_id}/answers?order=desc&sort=votes&site={self.site}&filter=withbody"
        response = requests.get(url)
        if response.status_code == 200:
            answers = response.json().get('items', [])
            for answer in answers:
                answer['body'] = self.convert_html_to_markdown(answer.get('body', ''))
            return answers
        else:
            print(f"Failed to fetch answers for question {question_id}. Status code: {response.status_code}")
            return []

    def convert_html_to_text(self, html_content):
        """Convert HTML to plain text."""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text().strip()

    def convert_html_to_markdown(self, html_content):
        """Convert HTML to Markdown."""
        return self.html_converter.handle(html_content).strip()

# Example usage
if __name__ == "__main__":
    fetcher = StackExchangeFetcher()
    
    # Fetch top questions
    top_questions = fetcher.fetch_top_questions()
    for question in top_questions:
        title = question.get('title')
        question_body = question.get('body')
        print(f"Title: {title}\nBody (Text):\n{question_body}\n{'-'*80}")

        # Fetch answers for the question
        answers = fetcher.fetch_answers_for_question(question.get('question_id'))
        for answer in answers:
            answer_body = answer.get('body')
            print(f"Answer (Markdown):\n{answer_body}\n{'-'*80}")
