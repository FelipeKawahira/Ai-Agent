import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("key not found")

prompt = argparse.ArgumentParser(description="Chatbot")
prompt.add_argument("user_prompt", type=str, help="User prompt")
prompt.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = prompt.parse_args()

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

if response.usage_metadata is None:
    raise RuntimeError("Failed API request")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if not response.function_calls:
    print(response.text)
else:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")