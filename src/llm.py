import logging
import pathlib
from functools import cache
from typing import List, Dict

from google import genai
from google.genai import types
from google.genai.types import Content, Part

from settings import Settings

# Set up logging
logger = logging.getLogger(__name__)

# Global variable to store the cache
_pdf_cache = None
_gemini_client = None


@cache
def initialize_client():
    global _gemini_client
    settings = Settings()
    if _gemini_client is None:
        _gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _gemini_client


@cache
def cache_llm():
    settings = Settings()
    global _pdf_cache

    if _pdf_cache is not None:
        # print("PDF cache already exists")
        return _pdf_cache
    try:
        client = initialize_client()
        pdf_path = pathlib.Path("user_manual.pdf")

        if not pdf_path.exists():
            logger.error(f"PDF file not found at {pdf_path}")
            return

        user_manual_file = client.files.upload(file=pdf_path)

        _pdf_cache = client.caches.create(
            model=settings.LLM_MODEL,
            config=types.CreateCachedContentConfig(
                contents=user_manual_file,
                system_instruction=settings.DEFAULT_SYSTEM_CONTENT,
                display_name="pdf_cache",
                ttl="3600s",
            ),
        )
        logger.info("PDF cache created successfully")
        return _pdf_cache
    except Exception as e:
        logger.error(f"Error creating PDF cache: {e}")
        return


def call_llm(
    messages_in_thread: List[Dict[str, str]],
) -> str:
    settings = Settings()

    if _pdf_cache is None:
        cache_llm()

    client = initialize_client()

    messages = []
    for message in messages_in_thread:
        role = message["role"]
        parts = [Part(text=message["parts"])]
        messages.append(Content(role=role, parts=parts))

    response = client.models.generate_content(
        model=settings.LLM_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            cached_content=_pdf_cache.name,
            max_output_tokens=200,
        ),
    )
    # print(response.usage_metadata)
    return response.text


def call_llm_no_cache(
    messages_in_thread: List[Dict[str, str]],
) -> str:
    settings = Settings()
    client = initialize_client()
    pdf_path = pathlib.Path("user_manual.pdf")

    if not pdf_path.exists():
        logger.error(f"PDF file not found at {pdf_path}")

    uploaded_file = client.files.upload(file=pdf_path)

    file_data = {"mime_type": "application/pdf", "file_uri": uploaded_file.uri}

    messages = [Content(role="user", parts=[Part(file_data=file_data)])]
    for message in messages_in_thread:
        role = message["role"]
        parts = [Part(text=message["parts"])]
        messages.append(Content(role=role, parts=parts))

    response = client.models.generate_content(
        model=settings.LLM_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=settings.DEFAULT_SYSTEM_CONTENT,
            max_output_tokens=200,
        ),
    )
    # print(response.usage_metadata)
    return response.text
