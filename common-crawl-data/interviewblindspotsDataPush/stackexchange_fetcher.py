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
        self.allowed_languages = {'java', 'python', 'javascript', 'ruby', 'swift', 'go', 'rust', 'php', 'clike'}

    def fetch_top_questions(self, page=1):
        url = f"{self.base_url}questions?order=desc&sort=votes&site={self.site}&page={page}&pagesize={self.pagesize}&filter=withbody"
        response = requests.get(url)
        if response.status_code == 200:
            questions = response.json().get('items', [])
            for question in questions:
                question['body'] = self.format_question_body(
                    question.get('body', ''), question.get('link', '')
                )
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

    def detect_language_from_tags(self, tags):
        """Detect the programming language based on tags."""
        for tag in tags:
            if tag.lower() in self.allowed_languages:
                return tag.lower()
        return None

    def convert_html_to_text(self, html_content):
        """Convert HTML to plain text."""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text().strip()

    def convert_html_to_markdown(self, html_content):
        """Convert HTML to Markdown."""
        return self.html_converter.handle(html_content).strip()

    def format_question_body(self, html_content, question_link):
        """Convert HTML to plain text and append attribution footer."""
        plain_text_body = self.convert_html_to_text(html_content)
        footer = (
            "\n" * 4 +
            f"This question was originally posted on StackExchange Code Review. \n"
            f"To view the original discussion, visit the {question_link}. \n"
            f"This content is licensed under the Creative Commons Attribution-ShareAlike license https://creativecommons.org/licenses/by-sa/4.0/."
        )
        return plain_text_body + footer
