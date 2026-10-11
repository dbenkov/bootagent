import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from chat import chat
from prompts import system_prompt

MAX_ITERATIONS = 20


def main():
    # Everything here happens ONCE and survives across loop iterations.
    load_dotenv()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        timeout=60
    )

    parser = argparse.ArgumentParser(description="Chatbot using OpenRouter API")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt for the chatbot")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # Each iteration: one model call. chat() appends to the SAME messages list,
    # so the model sees its earlier tool calls and their results every time.
    for _ in range(MAX_ITERATIONS):
        final_response = chat(client, messages, args.verbose)
        if final_response is not None:
            print("Final response:")
            print(final_response)
            return

    print(f"Agent hasn't produced a final response after {MAX_ITERATIONS} iterations. Exiting.")
    sys.exit(1)


if __name__ == "__main__":
    main()