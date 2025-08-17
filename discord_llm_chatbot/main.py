# main.py
import asyncio
from .bot.bot import MyBot
from .config.config import load_config
from .utils.logger import setup_logger


def main():
    # Setup logging
    logger = setup_logger()

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
