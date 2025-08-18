# main.py
import asyncio

from dotenv import load_dotenv

load_dotenv()

import sys

import jurigged

from .bot.bot import MyBot
from .config.config import load_config
from .utils.logger import setup_logger

logger = setup_logger()


def main():
    logger.info("Starting bot...")

    if "--watch" in sys.argv:
        logger.info("Starting file watcher...")
        jurigged.watch("discord_llm_chatbot/")

    # Load configuration
    config = load_config()

    # Initialize and run bot
    bot = MyBot(config)

    try:
        asyncio.run(bot.start(config.DISCORD_TOKEN))
    except KeyboardInterrupt:
        logger.info("Bot shutdown initiated")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        raise
    finally:
        asyncio.run(bot.close())


if __name__ == "__main__":
    main()
