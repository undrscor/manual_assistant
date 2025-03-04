from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")
    # slack
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str

    # google gemini
    GEMINI_API_KEY: str

    # llm settings
    LLM_MODEL: str = "gemini-1.5-flash-002"
    LLM_MAX_TOKENS: int = 200
    DEFAULT_SYSTEM_CONTENT: str = """
    You're an assistant in a Slack workspace.
    Users in the workspace will ask you to help them with any questions or inquires regarding the user manual.           
    You'll respond to those questions in an honest, professional way. If you are unsure, please don't make up an answer.
    Every prompt you are given chat history of up to 10 messages, and the last message is the latest and is the highest priority.
    When you include markdown text, convert them to Slack compatible ones.
    When a prompt has Slack's special syntax like <@USER_ID> or <#CHANNEL_ID>, you must keep them as-is in your response.
    """


@lru_cache
def get_settings() -> Settings:
    return Settings()
