import os
from typing import List, Dict

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import Content, Part

load_dotenv()

DEFAULT_SYSTEM_CONTENT = """
You're an assistant in a Slack workspace.
Users in the workspace will ask you to help them write something or to think better about a [USER MANUAL].              #TODO: IMPLEMENT USER MANUAL PDF
You'll respond to those questions in a professional way.
When you include markdown text, convert them to Slack compatible ones.
When a prompt has Slack's special syntax like <@USER_ID> or <#CHANNEL_ID>, you must keep them as-is in your response.
"""


def call_llm(
    messages_in_thread: List[Dict[str, str]],
    system_content: str = DEFAULT_SYSTEM_CONTENT,
) -> str:
    try:
        client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))

        messages = []
        for message in messages_in_thread:
            role = message["role"]
            text = message["content"]

            # Create a content object
            messages.append(Content(role=role, parts=[Part.from_text(text)]))

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_content,
                max_output_tokens=200,
            ),
        )
        bot_response = response.choices[0].message.content
        print(bot_response)
        return bot_response
        # return markdown_to_slack(response.choices[0].message.content)
    except Exception as e:
        print(f"Error in call_llm: {e}")
        return f":warning: Something went wrong! {str(e)}"


# def markdown_to_slack(markdown_text: str) -> str:
#     pass
