import os
from dotenv import load_dotenv
from ibs_connector import IBSConnector
from stackexchange_fetcher import StackExchangeFetcher

# Load environment variables from .env file
load_dotenv()

def main():
    tokenidfromenv = os.getenv("TOKEN_ID")

    if not tokenidfromenv:
        raise ValueError("TOKEN_ID not found in the environment variables.")

    ibs_connector = IBSConnector(tokenidfromenv)
    fetcher = StackExchangeFetcher()

    # Fetch top questions
    top_questions = fetcher.fetch_top_questions()
    # top_questions = top_questions[:1] 

    for idx, question in enumerate(top_questions, start=1):
        title = question.get('title')
        question_id = question.get('question_id')
        question_body = question.get('body', '[No Content]')
        link = question.get('link')
        tags = question.get('tags', [])
        
        print(f"Question {idx}: {title}")
        print(f"Link: {link}")
        
        # Detect the programming language from the tags
        detected_language = fetcher.detect_language_from_tags(tags)
        print(f"Detected Language: {detected_language}")
        
        # Create snippet for the question, including the detected language
        snippet_response = ibs_connector.create_snippet(title, question_body, detected_language)
        if snippet_response:
            snippet_id = snippet_response.get('id')
            
            # Fetch answers for the question
            answers = fetcher.fetch_answers_for_question(question_id)
            
            # Prepare comments from answers
            comments = []
            for answer in answers:
                answer_body = answer.get('body', '[No Content]')
                comments.append({"line": 1, "text": answer_body})

            # Add comments to the snippet
            ibs_connector.add_comments(snippet_id, comments)

        else:
            print("Failed to create snippet for the question.")
        print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    main()
