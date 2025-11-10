import traceback
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import telegramify_markdown

from services.genkit_service import genkit_service
from services.conversation_manager import conversation_manager


# Callback data for exit button
CALLBACK_GENKIT_EXIT = "genkit_exit"

# Telegram message length limit
MAX_MESSAGE_LENGTH = 4000


async def send_message_with_markdown(
    message_obj,
    text: str,
    reply_to_message_id: int = None,
    reply_markup: InlineKeyboardMarkup = None
):
    """
    Send a message with markdown formatting, with automatic fallback to plain text.
    
    Args:
        message_obj: Message object to reply to (update.message or last_message)
        text: Message text to send
        reply_to_message_id: Message ID to reply to (only for first message)
        reply_markup: Inline keyboard markup
        
    Returns:
        Sent message object
    """
    # Try to convert to markdown first
    try:
        content = telegramify_markdown.markdownify(text)
    except Exception as e:
        print(f"Markdown conversion failed, using plain text: {e}")
        content = text
    
    # Try sending with markdown
    try:
        if reply_to_message_id:
            return await message_obj.reply_text(
                content,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        else:
            return await message_obj.reply_text(
                content,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN_V2
            )
    except Exception as e:
        # Fallback to plain text if markdown parsing fails
        print(f"Markdown parsing failed, using plain text: {e}")
        if reply_to_message_id:
            return await message_obj.reply_text(
                text,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                parse_mode=None
            )
        else:
            return await message_obj.reply_text(
                text,
                reply_markup=reply_markup,
                parse_mode=None
            )


async def handle_genkit_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle messages when user is in active Genkit conversation.
    Only processes messages that are replies.

    Args:
        update: Telegram update
        context: Bot context
    """
    if not update.message or not update.message.text:
        return

    # Get user_id for bot operations (if needed) and username for database/AI
    user_id = update.message.from_user.id  # Used only for fallback if username is None
    user_name = update.message.from_user.username or f"user_{user_id}"  # Username for database and AI API

    # Check if user has active conversation (using username)
    if not await conversation_manager.is_active(user_name):
        return

    # Only process messages that are replies
    if not update.message.reply_to_message:
        return

    # Get user message
    user_message = update.message.text.strip()
    if not user_message:
        return

    history = await conversation_manager.get_history(user_name)

    await conversation_manager.add_message(user_name, "user", user_message)

    reply_to_message = update.message.reply_to_message
    if reply_to_message:
        if reply_to_message.reply_markup:
            try:
                # Edit the previous bot message to remove the button
                await context.bot.edit_message_reply_markup(
                    chat_id=update.effective_chat.id,
                    message_id=reply_to_message.message_id,
                    reply_markup=None
                )
            except Exception as e:
                print(f"Could not remove button from previous message: {e}")

    await process_genkit_chat(update, context, user_name, user_message, history)


async def process_genkit_chat(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    username: str,
    user_message: str,
    history: list
) -> None:
    """
    Process chat with Genkit API and send response.

    Args:
        update: Telegram update
        context: Bot context
        username: Telegram username
        user_message: User's message
        history: Conversation history
    """
    try:
        # Get message_thread_id for forum topics
        message_thread_id = update.message.message_thread_id if update.message else None
        
        # Show typing indicator (with thread ID for forum topics)
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing",
            message_thread_id=message_thread_id
        )
        
        # Call Genkit API with username (username is used for both database and AI API)
        ai_response = await genkit_service.chat(
            message=user_message,
            userId=username,
            history=history if history else None
        )

        if not ai_response:
            # Log error for debugging
            print(f"ERROR: Genkit API returned no response for user {username}")
            print(f"User message: {user_message}")
            
            # Error message to send to user
            error_message = "⚠️ Sorry bro, I'm having issues right now. Please try again!"
            
            # Save error message to history for tracking
            try:
                await conversation_manager.add_message(username, "model", error_message)
            except Exception as db_error:
                print(f"ERROR saving error message to database: {db_error}")
            
            # Notify user about the error
            await update.message.reply_text(
                error_message,
                reply_to_message_id=update.message.message_id
            )
            return

        try:
            await conversation_manager.add_message(username, "model", ai_response)
            print(f"Successfully added AI response to database for user {username}")
        except Exception as db_error:
            print(f"ERROR adding message to database: {db_error}")
            print(f"Error type: {type(db_error).__name__}")
            print(f"Traceback: {traceback.format_exc()}")
            raise
        
        # Debug: Print history after adding AI response
        try:
            updated_history = await conversation_manager.get_history(username)
            print(f"History after adding AI response: {len(updated_history)} messages")
        except Exception as history_error:
            print(f"ERROR getting history: {history_error}")
            print(f"Error type: {type(history_error).__name__}")
            print(f"Traceback: {traceback.format_exc()}")
            raise
        
        # Create exit button
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ End conversation", callback_data=CALLBACK_GENKIT_EXIT)]
        ])

        # Split message if it exceeds Telegram's limit
        message_chunks = split_message(ai_response)
        
        # Send all message chunks with markdown support
        last_message = None
        for i, chunk in enumerate(message_chunks):
            is_last = (i == len(message_chunks) - 1)
            current_keyboard = keyboard if is_last else None
            
            try:
                if i == 0:
                    # First chunk replies to user's message
                    last_message = await send_message_with_markdown(
                        update.message,
                        chunk,
                        reply_to_message_id=update.message.message_id,
                        reply_markup=current_keyboard
                    )
                else:
                    # Subsequent chunks reply to previous chunk
                    last_message = await send_message_with_markdown(
                        last_message,
                        chunk,
                        reply_markup=current_keyboard
                    )
            except Exception as send_error:
                # Final fallback if all else fails
                print(f"Error sending message chunk {i}: {send_error}")
                if i == 0:
                    last_message = await update.message.reply_text(
                        chunk,
                        reply_to_message_id=update.message.message_id,
                        reply_markup=current_keyboard,
                        parse_mode=None
                    )
                else:
                    last_message = await last_message.reply_text(
                        chunk,
                        reply_markup=current_keyboard,
                        parse_mode=None
                    )

    except Exception as e:
        print(f"ERROR in process_genkit_chat: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Full traceback:")
        traceback.print_exc()
        print(f"Username: {username}")
        print(f"User message: {user_message}")
        print(f"AI response: {ai_response if 'ai_response' in locals() else 'Not generated'}")
        await update.message.reply_text(
            "Sorry, an error occurred. Please try again.",
            reply_to_message_id=update.message.message_id
        )


def split_message(text: str) -> list[str]:
    """
    Split a long message into chunks that fit within Telegram's message limit.
    
    Args:
        text: Message text to split
        
    Returns:
        List of message chunks
    """
    if len(text) <= MAX_MESSAGE_LENGTH:
        return [text]
    
    chunks = []
    current_pos = 0
    
    while current_pos < len(text):
        chunk = text[current_pos:current_pos + MAX_MESSAGE_LENGTH]
        
        if current_pos + MAX_MESSAGE_LENGTH < len(text):
            # Try to split at newline first
            last_newline = chunk.rfind('\n')
            if last_newline > MAX_MESSAGE_LENGTH * 0.8:  # Only split at newline if it's not too early
                chunk = chunk[:last_newline + 1]
                current_pos += last_newline + 1
            else:
                # Find last space as fallback
                last_space = chunk.rfind(' ')
                if last_space > MAX_MESSAGE_LENGTH * 0.8:
                    chunk = chunk[:last_space]
                    current_pos += last_space + 1
                else:
                    # Force split at max length if no good break point
                    current_pos += MAX_MESSAGE_LENGTH
        else:
            # Last chunk
            current_pos = len(text)
        
        chunks.append(chunk)
    
    return chunks


async def handle_genkit_exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle exit button callback to end conversation.

    Args:
        update: Telegram update
        context: Bot context
    """
    query = update.callback_query
    if not query:
        return

    # Get user_id for bot operations (if needed) and username for database/AI
    user_id = query.from_user.id  # Used only for fallback if username is None
    username = query.from_user.username or f"user_{user_id}"  # Username for database and AI API

    # Check if user has active conversation (using username)
    if not await conversation_manager.is_active(username):
        await query.answer("Yo bro, no active conversation!", show_alert=True)
        return

    try:
        # End conversation
        await conversation_manager.end_conversation(username)

        # Answer callback
        await query.answer("Alright bro!")

        # Remove button from last message (keep the message content)
        if query.message:
            try:
                await query.edit_message_reply_markup(
                    reply_markup=None
                )
            except Exception as e:
                # If editing fails, just continue
                print(f"Could not remove button from message: {e}")
            
            # When replying, don't pass message_thread_id - Telegram auto-detects from reply
            await query.message.reply_text(
                "👋 Peace out bro! Catch you later! ✌️\n\nType /start when you need me bro!"
            )

    except Exception as e:
        print(f"Error in handle_genkit_exit: {e}")
        await query.answer("An error occurred while ending the conversation.")

