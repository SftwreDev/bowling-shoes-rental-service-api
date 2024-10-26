import json

from openai import OpenAI

from app.config import settings

gpt_model = settings.GPT_MODEL
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def query_gpt_model(system_message: str, user_prompt: str) -> str:
    """Send a request to the GPT model and return the generated response.

    This function constructs a chat completion request to the OpenAI API using
    the provided system message and user prompt. It returns the content of the
    response after stripping any leading or trailing whitespace.

    Args:
        system_message (str): Instructions for the LLM that define its behavior.
        user_prompt (str): The input prompt from the user that the LLM will respond to.

    Returns:
        str: The generated response from the GPT model, stripped of whitespace.

    Raises:
        ValueError: If the API response is invalid or does not contain the expected structure.
        ConnectionError: If there are issues connecting to the OpenAI API.
        RuntimeError: For other runtime-related errors that may occur during the API call.
    """
    try:
        # Create a completion request to the OpenAI GPT model
        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )

        # Check if the response contains choices and return the content
        if not response.choices:
            raise ValueError("No response choices were returned from the GPT model.")

        return response.choices[0].message.content.strip()

    except ValueError as ve:
        print(f"ValueError encountered: {ve}")
        raise
    except ConnectionError as ce:
        print(
            f"ConnectionError encountered: {ce}. Please check your network connection."
        )
        raise
    except Exception as e:
        print(f"An unexpected error occurred while querying the GPT model: {e}")
        raise
