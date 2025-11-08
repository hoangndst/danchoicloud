from typing import Optional, Dict, Any
from telegram import Update, Message
from telegram.ext import ContextTypes


async def send_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    parse_mode: Optional[str] = None,
    disable_web_page_preview: bool = False,
    message_thread_id: Optional[int] = None,
) -> Optional[Message]:
    """
    Send a text message.

    Args:
        update: Telegram update
        context: Bot context
        text: Message text
        parse_mode: Parse mode (HTML, Markdown, etc.)
        disable_web_page_preview: Disable web page preview
        message_thread_id: Thread ID for forum topics

    Returns:
        Sent message or None if error
    """
    try:
        chat_id = update.effective_chat.id
        reply_to_message_id = update.message.message_id if update.message else None

        final_thread_id = None
        if not reply_to_message_id:
            final_thread_id = message_thread_id
            if not final_thread_id:
                if update.message:
                    final_thread_id = update.message.message_thread_id
                elif update.callback_query and update.callback_query.message:
                    final_thread_id = update.callback_query.message.message_thread_id

        return await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            message_thread_id=final_thread_id,
            reply_to_message_id=reply_to_message_id,
        )
    except Exception as e:
        print(f"Error sending message: {e}")
        return None


async def send_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    photo: str,
    caption: Optional[str] = None,
    has_spoiler: bool = False,
    message_thread_id: Optional[int] = None,
) -> Optional[Message]:
    """
    Send a photo.

    Args:
        update: Telegram update
        context: Bot context
        photo: Photo URL or file ID
        caption: Photo caption
        has_spoiler: Whether photo has spoiler
        message_thread_id: Thread ID for forum topics

    Returns:
        Sent message or None if error
    """
    try:
        chat_id = update.effective_chat.id
        # Get message_thread_id from update (supports both message and callback_query)
        final_thread_id = message_thread_id
        if not final_thread_id:
            if update.message:
                final_thread_id = update.message.message_thread_id
            elif update.callback_query and update.callback_query.message:
                final_thread_id = update.callback_query.message.message_thread_id
        return await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            has_spoiler=has_spoiler,
            message_thread_id=final_thread_id,
        )
    except Exception as e:
        print(f"Error sending photo: {e}")
        return None


async def send_video(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    video: str,
    caption: Optional[str] = None,
    has_spoiler: bool = False,
    message_thread_id: Optional[int] = None,
) -> Optional[Message]:
    """
    Send a video.

    Args:
        update: Telegram update
        context: Bot context
        video: Video URL or file ID
        caption: Video caption
        has_spoiler: Whether video has spoiler
        message_thread_id: Thread ID for forum topics

    Returns:
        Sent message or None if error
    """
    try:
        chat_id = update.effective_chat.id
        # Get message_thread_id from update (supports both message and callback_query)
        final_thread_id = message_thread_id
        if not final_thread_id:
            if update.message:
                final_thread_id = update.message.message_thread_id
            elif update.callback_query and update.callback_query.message:
                final_thread_id = update.callback_query.message.message_thread_id
        return await context.bot.send_video(
            chat_id=chat_id,
            video=video,
            caption=caption,
            has_spoiler=has_spoiler,
            message_thread_id=final_thread_id,
        )
    except Exception as e:
        print(f"Error sending video: {e}")
        return None


async def send_poll(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    question: str,
    options: list[str],
    is_anonymous: bool = False,
    message_thread_id: Optional[int] = None,
) -> Optional[Message]:
    """
    Send a poll/quiz.

    Args:
        update: Telegram update
        context: Bot context
        question: Poll question
        options: List of poll options
        is_anonymous: Whether poll is anonymous
        message_thread_id: Thread ID for forum topics

    Returns:
        Sent message or None if error
    """
    try:
        chat_id = update.effective_chat.id
        # Get message_thread_id from update (supports both message and callback_query)
        final_thread_id = message_thread_id
        if not final_thread_id:
            if update.message:
                final_thread_id = update.message.message_thread_id
            elif update.callback_query and update.callback_query.message:
                final_thread_id = update.callback_query.message.message_thread_id
        return await context.bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=options,
            is_anonymous=is_anonymous,
            message_thread_id=final_thread_id,
        )
    except Exception as e:
        print(f"Error sending poll: {e}")
        return None

