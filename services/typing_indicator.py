from contextlib import asynccontextmanager
from typing import AsyncGenerator, Awaitable, Callable, Any

from telegram import Update
from telegram.ext import ContextTypes


@asynccontextmanager
async def typing_indicator(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> AsyncGenerator[None, None]:
    """
    Context manager that shows typing indicator during async operations.

    Args:
        update: Telegram update object
        context: Bot context

    Yields:
        None
    """
    try:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
        yield
    finally:
        pass


def with_typing(
    func: Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[Any]]
) -> Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[Any]]:
    """
    Decorator that automatically shows typing indicator during command execution.

    Usage:
        @with_typing
        async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Your command logic here
            pass
    """
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        async with typing_indicator(update, context):
            return await func(update, context)

    return wrapper

