import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.typing_indicator import with_typing
from bot.handlers import send_message
from services.conversation_manager import conversation_manager
from . import commands


CALLBACK_WEATHER = "weather"
CALLBACK_IMAGES = "images"
CALLBACK_IMAGES_CAT = "images_cat"
CALLBACK_IMAGES_DOG = "images_dog"
CALLBACK_IMAGES_SIEUNHAN = "images_sieunhan"
CALLBACK_IMAGES_HOCTAP = "images_hoctap"
CALLBACK_UTILS_HELP = "utils_help"
CALLBACK_GENKIT_CHAT = "genkit_chat"
CALLBACK_BACK = "back"
CALLBACK_EXIT = "exit"


def encode_callback(action: str, user_id: int) -> str:
    """
    Encode callback data with user_id.
    
    Args:
        action: Action name (e.g., "images_dog")
        user_id: User ID
        
    Returns:
        Encoded callback data: "menu_{action}_{user_id}"
    """
    return f"menu_{action}_{user_id}"


def decode_callback(callback_data: str) -> tuple[str, int]:
    """
    Decode callback data to extract action and user_id.
    
    Args:
        callback_data: Encoded callback data
        
    Returns:
        Tuple of (action, user_id)
        
    Raises:
        ValueError: If callback_data format is invalid
    """
    # Pattern: menu_{action}_{user_id}
    match = re.match(r"^menu_([^_]+(?:_[^_]+)*)_(\d+)$", callback_data)
    if not match:
        raise ValueError(f"Invalid callback data format: {callback_data}")
    
    action = match.group(1)
    user_id = int(match.group(2))
    return action, user_id


def get_user_id_from_update(update: Update) -> int:
    """
    Get user ID from update (supports both message and callback_query).
    
    Args:
        update: Telegram update
        
    Returns:
        User ID
    """
    if update.callback_query:
        return update.callback_query.from_user.id
    elif update.message:
        return update.message.from_user.id
    elif update.effective_user:
        return update.effective_user.id
    else:
        raise ValueError("Cannot extract user_id from update")


async def delete_menu_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Delete the menu message from callback query.
    
    Args:
        update: Telegram update
        context: Bot context
    """
    try:
        if update.callback_query and update.callback_query.message:
            await update.callback_query.message.delete()
    except Exception as e:
        print(f"Error deleting menu message: {e}")
        # If deletion fails, try to edit the message to remove keyboard
        try:
            if update.callback_query:
                await update.callback_query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass


async def send_menu_after_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    menu_type: str = "main"
) -> None:
    """
    Send menu after response has been sent.
    First deletes the old menu message, then sends new menu.
    
    Args:
        update: Telegram update
        context: Bot context
        menu_type: Type of menu to send ("main", "sports", "images")
    """
    try:
        # Delete old menu message first
        await delete_menu_message(update, context)
        
        user_id = get_user_id_from_update(update)
        welcome_text = (
            "👋 Yo bro! What's up!\n\n"
            "What you need? Choose a feature from the menu below bro:"
        )
        
        if menu_type == "main":
            keyboard = create_main_menu(user_id)
        elif menu_type == "images":
            keyboard = create_images_menu(user_id)
            welcome_text = "🖼️ Images\n\nChoose an option:"
        else:
            keyboard = create_main_menu(user_id)
        
        chat_id = update.effective_chat.id
        # Get message_thread_id from callback query message for forum topics
        message_thread_id = None
        if update.callback_query and update.callback_query.message:
            message_thread_id = update.callback_query.message.message_thread_id
        elif update.message:
            message_thread_id = update.message.message_thread_id
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_text,
            reply_markup=keyboard,
            message_thread_id=message_thread_id,
        )
    except Exception as e:
        print(f"Error sending menu after response: {e}")


def create_main_menu(user_id: int) -> InlineKeyboardMarkup:
    """
    Create the main menu inline keyboard.

    Args:
        user_id: User ID to encode in callback data

    Returns:
        InlineKeyboardMarkup with menu buttons
    """
    keyboard = [
        [
            InlineKeyboardButton("🌤️ Weather", callback_data=encode_callback(CALLBACK_WEATHER, user_id)),
            InlineKeyboardButton("🖼️ Images", callback_data=encode_callback(CALLBACK_IMAGES, user_id)),
        ],
        [
            InlineKeyboardButton("🤖 AI Bro", callback_data=encode_callback(CALLBACK_GENKIT_CHAT, user_id)),
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data=encode_callback(CALLBACK_UTILS_HELP, user_id)),
        ],
        [
            InlineKeyboardButton("❌ Exit", callback_data=encode_callback(CALLBACK_EXIT, user_id)),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def create_images_menu(user_id: int) -> InlineKeyboardMarkup:
    """
    Create the images submenu.

    Args:
        user_id: User ID to encode in callback data

    Returns:
        InlineKeyboardMarkup with image options
    """
    keyboard = [
        [
            InlineKeyboardButton("🐱 Cat", callback_data=encode_callback(CALLBACK_IMAGES_CAT, user_id)),
            InlineKeyboardButton("🐶 Dog", callback_data=encode_callback(CALLBACK_IMAGES_DOG, user_id)),
            InlineKeyboardButton("🦸 Siêu Nhân", callback_data=encode_callback(CALLBACK_IMAGES_SIEUNHAN, user_id)),
        ],
        [
            InlineKeyboardButton("📖 Học Tập", callback_data=encode_callback(CALLBACK_IMAGES_HOCTAP, user_id)),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data=encode_callback(CALLBACK_BACK, user_id)),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


@with_typing
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command - show main menu.

    Args:
        update: Telegram update
        context: Bot context
    """
    welcome_text = (
        "👋 Yo bro! What's up!\n\n"
        "What you need today? Choose a feature from the menu below bro:\n\n"
        "🌤️ Weather - Hanoi weather forecast\n"
        "🖼️ Images - View cat, dog, siêu nhân, học tập images\n"
        "ℹ️ Help - View usage guide"
    )
    
    user_id = get_user_id_from_update(update)
    keyboard = create_main_menu(user_id)
    
    try:
        await update.message.reply_text(
            welcome_text,
            reply_markup=keyboard,
        )
    except Exception as e:
        print(f"Error in start_command: {e}")
        await send_message(update, context, "An error occurred while displaying the menu.")


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Show main menu (can be called from callback or message).

    Args:
        update: Telegram update
        context: Bot context
    """
    welcome_text = (
        "👋 Yo bro! What's up!\n\n"
        "What you need? Choose a feature from the menu below bro:"
    )
    
    user_id = get_user_id_from_update(update)
    keyboard = create_main_menu(user_id)
    
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                welcome_text,
                reply_markup=keyboard,
            )
            await update.callback_query.answer()
        else:
            await update.message.reply_text(
                welcome_text,
                reply_markup=keyboard,
            )
    except Exception as e:
        print(f"Error in show_menu: {e}")
        if update.callback_query:
            await update.callback_query.answer("An error occurred.")


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle callback queries from inline keyboard buttons.

    Args:
        update: Telegram update
        context: Bot context
    """
    query = update.callback_query
    callback_data = query.data
    
    try:
        # Decode callback data to get action and user_id
        action, callback_user_id = decode_callback(callback_data)
        
        # Check if the user clicking is the owner of the menu
        current_user_id = query.from_user.id
        if current_user_id != callback_user_id:
            await query.answer("This menu doesn't belong to you.", show_alert=True)
            return
        
        await query.answer()  # Acknowledge the callback
        
        # Show typing indicator for actions that will execute commands
        actions_that_need_typing = [
            CALLBACK_WEATHER, CALLBACK_IMAGES_CAT, CALLBACK_IMAGES_DOG,
            CALLBACK_IMAGES_SIEUNHAN, CALLBACK_IMAGES_HOCTAP,
            CALLBACK_UTILS_HELP
        ]
        
        if action in actions_that_need_typing:
            # Get message_thread_id from callback query message for forum topics
            message_thread_id = None
            if query.message:
                message_thread_id = query.message.message_thread_id
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action="typing",
                message_thread_id=message_thread_id
            )
        
        # Get current user_id for new menus
        user_id = current_user_id
        
        # Weather
        if action == CALLBACK_WEATHER:
            await commands.weather(update, context)
            await send_menu_after_response(update, context, "main")
        
        # Images menu
        elif action == CALLBACK_IMAGES:
            # Show images submenu
            keyboard = create_images_menu(user_id)
            await query.edit_message_text(
                "🖼️ Images\n\nChoose an option:",
                reply_markup=keyboard,
            )
        elif action == CALLBACK_IMAGES_CAT:
            await commands.cat(update, context)
            await send_menu_after_response(update, context, "images")
        elif action == CALLBACK_IMAGES_DOG:
            await commands.dog(update, context)
            await send_menu_after_response(update, context, "images")
        elif action == CALLBACK_IMAGES_SIEUNHAN:
            await commands.sieunhan(update, context)
            await send_menu_after_response(update, context, "images")
        elif action == CALLBACK_IMAGES_HOCTAP:
            await commands.hoctap(update, context)
            await send_menu_after_response(update, context, "images")
        
        # Utils
        elif action == CALLBACK_UTILS_HELP:
            await commands.help_command(update, context)
            await send_menu_after_response(update, context, "main")
        
        # Genkit Chat
        elif action == CALLBACK_GENKIT_CHAT:
            # Delete menu message
            await delete_menu_message(update, context)
            # Start conversation
            conversation_manager.start_conversation(user_id)
            # Send welcome message
            welcome_text = "🤖 Starting chat with AI. You can reply to this message to chat."
            # Get message_thread_id from callback query message for forum topics
            message_thread_id = None
            if query.message:
                message_thread_id = query.message.message_thread_id
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=welcome_text,
                message_thread_id=message_thread_id,
            )
        
        # Back to main menu
        elif action == CALLBACK_BACK:
            await show_menu(update, context)
        
        # Exit menu
        elif action == CALLBACK_EXIT:
            try:
                # Remove keyboard and show closing message
                await query.edit_message_text(
                    "👋 Peace out bro! Catch you later! ✌️\n\nType /start when you need me bro!",
                    reply_markup=None,
                )
            except Exception:
                # If editing fails, try to answer with a message
                await query.answer("Alright bro! Type /start when you need me!")
        
    except ValueError as e:
        # Invalid callback format
        print(f"Invalid callback data: {e}")
        await query.answer("Error: Invalid callback data.", show_alert=True)
    except Exception as e:
        print(f"Error in handle_callback_query: {e}")
        try:
            await query.answer("An error occurred. Please try again.")
        except Exception:
            pass


# Pattern for matching all menu callbacks
MENU_CALLBACK_PATTERN = re.compile(r"^menu_")

