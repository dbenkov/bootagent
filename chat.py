from openai import OpenAI

from call_function import available_functions, call_function


def chat(
    client: OpenAI,
    messages: list,
    verbose: bool = False,
) -> str | None:
    """Run ONE agent step.

    Returns the model's final text when it's done,
    or None when it called tools and needs another turn.
    """
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("Response usage is None. Please check the API response.")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message

    # The assistant's turn goes into the history, tool requests included.
    # Pylance may flag this (message object vs. dict type); it works at runtime.
    messages.append(message)  # type: ignore

    # No tool calls means the model has its final answer: hand it back.
    if not message.tool_calls:
        return message.content or ""

    # Otherwise run each requested tool and add one tool message per call.
    for tool_call in message.tool_calls:
        if tool_call.type == "function":
            result_message = call_function(tool_call, verbose=verbose)
            if not result_message["content"]:
                raise Exception("Function call returned no content.")
            if verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    return None  # not done yet, the loop should call chat() again