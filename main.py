import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
    function_results_list = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)
        if not function_call_result.parts: 
            raise Exception("Error: parts list empty")
        if function_call_result.parts[0].function_response is None:
            raise Exception("Error: .parts[0].function_response property can't be None")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("Error: .parts[0].function_response.response property can't be None")
        function_results_list.append(function_call_result.parts[0])

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")