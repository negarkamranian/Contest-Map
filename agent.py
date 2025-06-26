import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, Any

load_dotenv()

# Pydantic models for structured output
class TaskResponse(BaseModel):
    """Structured response model for task execution."""
    answer: str = Field(description="The extracted answer from the HTML content")

def get_chat_completion(user_query: str, response_model: BaseModel = TaskResponse) -> BaseModel:
    """Get structured chat completion from OpenAI using Pydantic models."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can analyze HTML content and extract specific information. Provide structured responses."},
            {"role": "user", "content": user_query}
        ],
        response_format=response_model,
    )
    
    return response.choices[0].message.parsed

def execute_task(html_content: str, task: str) -> TaskResponse:
    """Execute the given task on HTML content using OpenAI with structured output."""
    prompt = f"""Your task is: {task}

    HTML Body Content:
    {html_content}

    Please read through the entire HTML content and answer the task. Provide:
    1. The answer to the task"""

    return get_chat_completion(prompt, TaskResponse)

def load_task_from_flags() -> dict:
    """Load task and answer from flags.json file."""
    try:
        with open("flags.json", "r") as f:
            flags_data = json.load(f)
            return flags_data[0]  # Get the first task
    except (FileNotFoundError, json.JSONDecodeError, IndexError) as e:
        print(f"Error loading flags.json: {e}")
        return None

def get_html_from_server(server_url: str = "http://localhost:8000") -> str:
    """Fetch HTML content from the running server."""
    try:
        response = requests.get(server_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching HTML from server: {e}")
        return None

if __name__ == "__main__":
    # Load task from flags.json
    task_data = load_task_from_flags()
    if not task_data:
        print("Failed to load task from flags.json")
        exit(1)
    
    task = task_data["task"]
    expected_answer = task_data["answer"]
    
    print(f"Task: {task}")
    print("Fetching HTML from server...")
    
    html_content = get_html_from_server()
    if not html_content:
        print("Failed to fetch HTML from server. Make sure the server is running on http://localhost:8000")
        exit(1)
    
    print("Executing task with Pydantic structured output...")
    result = execute_task(html_content, task)
    
    print(f"\n=== RESULT ===")
    print(f"Answer: {result.answer}")
    
    print(f"\nExpected Answer: {expected_answer}")
    
    # Check if the result matches the expected answer
    if result.answer.strip() == expected_answer:
        print("✅ SUCCESS: Answer matches expected result!")
    else:
        print("❌ FAILURE: Answer does not match expected result.")