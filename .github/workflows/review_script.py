import os
import sys
import requests
from google import genai
from google.genai import types

def main():
    # 1. Grab environment variables supplied by GitHub Actions
    gemini_key = os.getenv("GEMINI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("REPO_NAME")
    pr_number = os.getenv("PR_NUMBER")

    if not all([gemini_key, github_token, repo, pr_number]):
        print("Missing required environment variables.")
        sys.exit(1)

    # 2. Correctly target the GitHub API endpoint
    diff_url = f"https://github.com{repo}/pulls/{pr_number}"
    print(f"Targeting API Endpoint: {diff_url}")
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3.diff" 
    }
    
    response = requests.get(diff_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch PR diff: {response.status_code} - {response.text}")
        sys.exit(1)
        
    pr_diff = response.text
    if not pr_diff.strip():
        print("No code changes detected in this PR.")
        sys.exit(0)

    # 3. Initialize Gemini Client and request code analysis
    print("Sending code changes to Gemini AI...")
    client = genai.Client(api_key=gemini_key)
    
    system_instruction = (
        "You are an expert DevOps engineer and Senior Software Developer. "
        "Review the following Git diff code changes. Point out potential bugs, "
        "security vulnerabilities, or bad habits. Provide constructive feedback "
        "and code snippets for fixes where appropriate. Keep your response concise, "
        "clean, and organized with markdown headers."
    )
    
    try:
        ai_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Please review this Git diff:\n\n{pr_diff}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
            )
        )
        review_text = ai_response.text
    except Exception as e:
        print(f"Error communicating with Gemini API: {e}")
        sys.exit(1)

    # 4. Post the AI Review back to the GitHub PR as a comment
    print("Posting review comment back to GitHub...")
    comment_url = f"https://github.com{repo}/issues/{pr_number}/comments"
    comment_headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    comment_body = {
        "body": f"### 🤖 AI Code Reviewer Report\n\n{review_text}"
    }
    
    post_response = requests.post(comment_url, headers=comment_headers, json=comment_body)
    
    if post_response.status_code == 201:
        print("Successfully posted AI review comment!")
    else:
        print(f"Failed to post comment: {post_response.status_code} - {post_response.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()
