import requests

def fetch_top_questions(site='codereview', page=1, pagesize=10):
    url = f"https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site={site}&page={page}&pagesize={pagesize}&filter=!9_bDE(fI5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Failed to fetch questions. Status code: {response.status_code}")
        return []

def fetch_answers_for_question(question_id, site='codereview'):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers?order=desc&sort=votes&site={site}&filter=!9_bDE(fI5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Failed to fetch answers for question {question_id}. Status code: {response.status_code}")
        return []

def main():
    top_questions = fetch_top_questions()
    
    for idx, question in enumerate(top_questions, start=1):
        title = question.get('title')
        question_id = question.get('question_id')
        link = question.get('link')
        
        print(f"Question {idx}: {title}")
        print(f"Link: {link}")
        
        answers = fetch_answers_for_question(question_id)
        if answers:
            print("Answers:")
            for answer in answers:
                answer_body = answer.get('body', '[No Content]')
                print(f"- {answer_body}")  # Show first 100 characters of the answer
        else:
            print("No answers found.")
        print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    main()
