import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from assistant import assistant

load_dotenv()

# logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Initializes your app with your bot token and socket mode handler
slackapp = App(token=os.environ.get("SLACK_BOT_TOKEN"))
# Adds assistant functionality
slackapp.assistant(assistant)

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
# @slackapp.message("hello")
# def message_hello(message, say):
#     # say() sends a message to the channel where the event was triggered
#     say(f"Hey there <@{message['user']}>!")
#     say(f"I am an assistant chatbot for questions about user manuals!")
#     say("Start a thread with me to ask questions, or use the Slack Assistant interface if it's enabled in your workspace.")
#
#
# @slackapp.command("/help")
# def help_command(body, ack, say):
#     ack()
#     logger.info(body)
#     say(f"Available commands: /start, /help, /end")
#
#
# @slackapp.command("/start")
# def start_chat(body, ack, say):
#     ack()
#     logger.info(body)
#     say(f"What is your issue?")
#
#
# @slackapp.command("/end")
# def end_chat(body, ack, say):
#     ack()
#     logger.info(body)
#     say(f"I hope this helped!")


# main))
def main():
    try:
        handler = SocketModeHandler(slackapp, os.environ["SLACK_APP_TOKEN"])
        handler.start()
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
