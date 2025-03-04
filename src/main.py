import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from assistant import assistant
from settings import get_settings
from src.llm import cache_llm

# logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# main))
def main():
    try:
        settings = get_settings()

        # initialize app
        slackapp = App(token=settings.SLACK_BOT_TOKEN)
        # add assistant functionality
        slackapp.assistant(assistant)

        cache_llm()

        handler = SocketModeHandler(slackapp, settings.SLACK_APP_TOKEN)
        handler.start()

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise


if __name__ == "__main__":
    main()
