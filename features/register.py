import re
from telegram.ext import filters

from bot.bot import Bot
from . import menu
from . import genkit_chat


def register_features(bot: Bot) -> None:
    """
    Register all handlers with the bot.
    Args:
        bot: Bot instance
    """
 
    bot.add_message_handler(
        genkit_chat.handle_genkit_message,
        filters_obj=filters.TEXT & ~filters.COMMAND
    )
    
    exit_pattern = re.compile(f"^{genkit_chat.CALLBACK_GENKIT_EXIT}$")
    bot.add_callback_query_handler(
        genkit_chat.handle_genkit_exit,
        pattern=exit_pattern
    )
    
    bot.add_command_handler("start", menu.start_command)
    bot.add_callback_query_handler(menu.handle_callback_query, pattern=menu.MENU_CALLBACK_PATTERN)
    
    bot.add_message_handler(menu.show_menu, filters_obj=filters.TEXT & ~filters.COMMAND)
