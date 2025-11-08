from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.genkit_service import genkit_service
from services.conversation_manager import conversation_manager


# Callback data for exit button
CALLBACK_GENKIT_EXIT = "genkit_exit"

# Telegram message length limit (safe limit to avoid issues)
MAX_MESSAGE_LENGTH = 4000


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

    user_id = update.message.from_user.id
    user_name = update.message.from_user.username

    # Check if user has active conversation
    if not conversation_manager.is_active(user_id):
        return

    # Only process messages that are replies
    if not update.message.reply_to_message:
        return

    # Get user message
    user_message = update.message.text.strip()
    if not user_message:
        return

    history = conversation_manager.get_history(user_id)

    conversation_manager.add_message(user_id, "user", user_message)

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
    user_id: int,
    user_message: str,
    history: list
) -> None:
    """
    Process chat with Genkit API and send response.

    Args:
        update: Telegram update
        context: Bot context
        user_id: Telegram user ID
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

        # Call Genkit API (userId as string)
        # History is already without current message (we got it before adding user message)
        ai_response = await genkit_service.chat(
            message=user_message,
            userId=str(user_id),
            history=history if history else None
        )

        if not ai_response:
            # When replying, don't pass message_thread_id - Telegram auto-detects from reply
            await update.message.reply_text(
                "Sorry, an error occurred while calling AI. Please try again.",
                reply_to_message_id=update.message.message_id
            )
            return

        # Add AI response to history
        conversation_manager.add_message(user_id, "ai", ai_response)

        # Split response into chunks if too long
        message_chunks = split_message(ai_response)
        
        # Create exit button (only for last message)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ End conversation", callback_data=CALLBACK_GENKIT_EXIT)]
        ])

        # Send all message chunks
        last_message = None
        for i, chunk in enumerate(message_chunks):
            is_last = (i == len(message_chunks) - 1)
            
            if i == 0:
                last_message = await update.message.reply_text(
                    chunk,
                    reply_to_message_id=update.message.message_id,
                    reply_markup=keyboard if is_last else None
                )
            else:
                last_message = await last_message.reply_text(
                    chunk,
                    reply_markup=keyboard if is_last else None
                )

    except Exception as e:
        print(f"Error in process_genkit_chat: {e}")
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
                    current_pos += MAX_MESSAGE_LENGTH
        else:
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

    user_id = query.from_user.id

    # Check if user has active conversation
    if not conversation_manager.is_active(user_id):
        await query.answer("Yo bro, no active conversation!", show_alert=True)
        return

    try:
        # End conversation
        conversation_manager.end_conversation(user_id)

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

