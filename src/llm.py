import logging
import pathlib
from functools import cache
from typing import List, Dict

from google import genai
from google.genai import types
from google.genai.types import Content, Part, FileData, FileDataDict

from settings import Settings

# Set up logging
logger = logging.getLogger(__name__)


@cache
def initialize_client(
    settings: Settings = Settings(),
) -> genai.Client:
    gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return gemini_client


@cache
def cache_llm(settings: Settings = Settings()):
    client = initialize_client()

    pdf_path = pathlib.Path("user_manual.pdf")
    if not pdf_path.exists():
        logger.error(f"PDF file not found at {pdf_path}")
        return

    user_manual_file = client.files.upload(file=pdf_path)

    pdf_cache = client.caches.create(
        model=settings.LLM_MODEL,
        config=types.CreateCachedContentConfig(
            contents=user_manual_file,
            system_instruction=settings.DEFAULT_SYSTEM_CONTENT,
            display_name="pdf_cache",
            ttl="3600s",
        ),
    )
    logger.info("PDF cache created successfully")
    return pdf_cache


def call_llm(
    messages_in_thread: List[Dict[str, str]],
) -> str:
    settings = Settings()
    pdf_cache = cache_llm()

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
            cached_content=pdf_cache.name if pdf_cache else None,
            max_output_tokens=200,
        ),
    )
    logger.info(response.usage_metadata)
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

    file_data: FileDataDict = {
        "mime_type": "application/pdf",
        "file_uri": uploaded_file.uri,
    }

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
    logger.info(response.usage_metadata)
    return response.text
