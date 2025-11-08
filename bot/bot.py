import logging
from typing import Optional, Pattern
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from config.settings import settings
from models.messages import COMMANDS

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class Bot:
    """Telegram bot application."""

    def __init__(self):
        """Initialize the bot application."""
        self.application = Application.builder().token(settings.telegram_token).build()
        self._setup_error_handler()
        self._setup_commands()

    def _setup_error_handler(self):
        """Setup error handler for the bot."""

        async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
            """Log the error and send a message to the user."""
            logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

            if isinstance(update, Update) and update.effective_message:
                try:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.",
                    )
                except Exception:
                    pass

        self.application.add_error_handler(error_handler)

    def _setup_commands(self):
        """Setup bot commands menu."""
        from telegram import BotCommand
        bot_commands = [
            BotCommand(cmd["command"], cmd["description"]) for cmd in COMMANDS
        ]
        # Commands will be set when bot starts
        self._bot_commands = bot_commands

    def add_command_handler(self, command: str, handler):
        """
        Add a command handler.

        Args:
            command: Command name (without /)
            handler: Handler function
        """
        self.application.add_handler(CommandHandler(command, handler))

    def add_message_handler(self, handler, filters_obj=None):
        """
        Add a message handler.

        Args:
            handler: Handler function
            filters_obj: Optional filters
        """
        if filters_obj:
            self.application.add_handler(MessageHandler(filters_obj, handler))
        else:
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    def add_callback_query_handler(self, handler, pattern: Optional[Pattern[str]] = None):
        """
        Add a callback query handler.

        Args:
            handler: Handler function
            pattern: Optional regex pattern to match callback data
        """
        if pattern:
            self.application.add_handler(CallbackQueryHandler(handler, pattern=pattern))
        else:
            self.application.add_handler(CallbackQueryHandler(handler))

    async def start_polling(self):
        """Start the bot polling."""
        from datetime import datetime
        logger.info("Bot server started")
        logger.info(f"Current date time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await self.application.initialize()
        await self.application.start()
        # Set bot commands
        if hasattr(self, '_bot_commands'):
            await self.application.bot.set_my_commands(self._bot_commands)
        await self.application.updater.start_polling()
        logger.info("Bot is polling...")

    async def stop(self):
        """Stop the bot."""
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()
        logger.info("Bot stopped")

