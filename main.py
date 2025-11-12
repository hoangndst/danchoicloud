import asyncio
import logging
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.bot import Bot
from features.register import register_features
from services.api_client import api_client
from services.genkit_service import genkit_service
from services.conversation_manager import conversation_manager

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot."""
    # Initialize bot
    bot_instance = Bot()

    # Register all features
    register_features(bot_instance)
    logger.info("All features registered")

    try:
        # Start bot polling
        await bot_instance.start_polling()

        # Keep the bot running
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Received stop signal, shutting down...")
    finally:
        # Cleanup
        await api_client.close()
        await genkit_service.close()
        await conversation_manager.close()
        await bot_instance.stop()
        logger.info("Bot stopped successfully")


if __name__ == "__main__":
    asyncio.run(main())
