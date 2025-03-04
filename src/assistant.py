import logging
from typing import List, Dict

from slack_bolt import Assistant, BoltContext, Say, SetStatus
from slack_sdk import WebClient

from src.llm import call_llm_no_cache, call_llm

# Refer to https://tools.slack.dev/bolt-python/concepts/assistant/ for more details
assistant = Assistant()


# new assistant thread handler
@assistant.thread_started
def start_assistant_thread(
    say: Say,
    logger: logging.Logger,
):
    try:
        say("How can I help you?")
        # cache_llm()

    except Exception as e:
        logger.exception(f"Failed to handle an assistant_thread_started event: {e}", e)
        say(f":warning: Something went wrong! ({e})")


# assistant message handler
@assistant.user_message
def respond_in_assistant_thread(
    logger: logging.Logger,
    context: BoltContext,
    set_status: SetStatus,
    client: WebClient,
    say: Say,
):
    try:
        set_status("is typing...")

        # saves replies
        replies = client.conversations_replies(
            channel=context.channel_id,
            ts=context.thread_ts,
            oldest=context.thread_ts,
            limit=10,
        )

        messages_in_thread: List[Dict[str, str]] = []
        for message in replies["messages"]:
            if message.get("bot_id") is None:
                role = "user"
            else:
                role = "model"
            messages_in_thread.append({"role": role, "parts": message["text"]})

        # ask llm, optionally can use caching for pdf and starting prompt
        # returned_message_no_cache = call_llm_no_cache(messages_in_thread)
        # say(returned_message_no_cache)
        returned_message = call_llm(messages_in_thread)
        say(returned_message)

    except Exception as e:
        logger.exception(f"Failed to handle a user message event: {e}")
        say(f":warning: Something went wrong! ({e})")
