from typing import List, Dict

from slack_bolt import Assistant, BoltContext, Say, SetStatus
from slack_sdk import WebClient

from llm import cache_llm, call_llm

# Refer to https://tools.slack.dev/bolt-python/concepts/assistant/ for more details
assistant = Assistant()


# new assistant thread handler
@assistant.thread_started
def start_assistant_thread(
    say: Say,
):
    say("How can I help you?")
    cache_llm()


# assistant message handler
@assistant.user_message
def respond_in_assistant_thread(
    context: BoltContext,
    set_status: SetStatus,
    client: WebClient,
    say: Say,
):
    set_status("is typing...")

    # saves replies
    replies = client.conversations_replies(
        channel=context.channel_id,
        ts=context.thread_ts,
        oldest=context.thread_ts,
        limit=10,
    )

    # format replies for llm chat reading
    messages_in_thread: List[Dict[str, str]] = []
    for message in replies["messages"]:
        if message.get("bot_id") is None:
            role = "user"
        else:
            role = "model"
        messages_in_thread.append({"role": role, "parts": message["text"]})

    # ask llm, optionally can use no caching method
    try:
        returned_message = call_llm(messages_in_thread[-10:])
        # returned_message = call_llm_no_cache(messages_in_thread)       #no cache method
    except Exception as e:
        say("Something went wrong")
        return
    say(returned_message)
