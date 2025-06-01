import openai
import os
import requests
import anthropic
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

def call_openai_api():
    # Load environment variables and set OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Load environment variables and set OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Hello, OpenAI GPT-4o! Can you tell me a joke?"}
            ]
        )
        print(f"OPENAI gpt-4o Response: {response.choices[0].message.content} \n==========")
    except Exception as e:
        print(f"OpenAI API call failed: {e}")

        
def call_llama_api():
    """
    Calls the Meta Llama 4-Scout-17B-16E-Instruct model using the Groq API and prints the response.
    """
    from groq._exceptions import GroqError

    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": "Who are you? Respond as a pirate chatbot!"
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        print("LLAMA Response: ", end="")
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
        print("\n==========")
    except GroqError as e:
        print(f"Llama API call failed: {e}")

def call_gemini_api():
    """
    Calls the Google Gemini API and prints the response.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Explain how AI works in a few words"
                    }
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Extract and print the generated text
        content = result.get("candidates", [{}])[0].get("content", {})
        parts = content.get("parts", [])
        if parts and "text" in parts[0]:
            print(f"GEMINI Response: {parts[0]['text']}\n==========")
        else:
            print("GEMINI Response: No content returned.\n==========")
    except Exception as e:
        print(f"Gemini API call failed: {e}")

def call_claude_api():
    """
    Calls the Anthropic Claude API and prints the response.
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Claude API call failed: ANTHROPIC_API_KEY not set.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    try:
        message = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=1000,
            temperature=1,
            system="You are a world-class poet. Respond only with short poems.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Why is the ocean salty?"
                        }
                    ]
                }
            ]
        )
        # message.content is a list of content blocks; join text blocks for output
        poem = "".join(block.text for block in message.content if hasattr(block, "text"))
        print(f"CLAUDE Response: {poem}\n==========")
    except Exception as e:
        print(f"Claude API call failed: {e}")

def main():
    # Load environment variables from .env file
    load_dotenv()

    print("OpenAI-Llama-Gemini-Claude Integration Project")
    print("=========================================")
    
    call_openai_api()
    print("=========================================")

    call_llama_api()
    print("=========================================")

    call_gemini_api()
    print("=========================================")

    call_claude_api()

if __name__ == "__main__":
    main()