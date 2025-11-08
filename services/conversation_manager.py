from typing import Dict, List, Optional

MAX_HISTORY_MESSAGES = 100


class ConversationManager:
    """Manages conversation state and history for each user."""

    def __init__(self):
        """Initialize the conversation manager."""
        # Store conversations: {user_id: {"active": bool, "history": [...]}}
        self._conversations: Dict[int, Dict] = {}

    def start_conversation(self, user_id: int) -> None:
        """
        Start a new conversation for a user.

        Args:
            user_id: Telegram user ID
        """
        self._conversations[user_id] = {
            "active": True,
            "history": []
        }

    def add_message(self, user_id: int, role: str, message: str) -> None:
        """
        Add a message to conversation history.

        Args:
            user_id: Telegram user ID
            role: Message role ("user" or "ai")
            message: Message content
        """
        if user_id not in self._conversations:
            self.start_conversation(user_id)

        history = self._conversations[user_id]["history"]
        history.append({"role": role, "message": message})

        # Limit history to MAX_HISTORY_MESSAGES (FIFO - remove oldest)
        if len(history) > MAX_HISTORY_MESSAGES:
            # Remove oldest messages until we're at the limit
            excess = len(history) - MAX_HISTORY_MESSAGES
            self._conversations[user_id]["history"] = history[excess:]

    def get_history(self, user_id: int) -> List[Dict[str, str]]:
        """
        Get conversation history for a user.

        Args:
            user_id: Telegram user ID

        Returns:
            List of messages in format [{"role": "user"/"ai", "message": "..."}]
        """
        if user_id not in self._conversations:
            return []
        return self._conversations[user_id]["history"].copy()

    def end_conversation(self, user_id: int) -> None:
        """
        End conversation for a user and clear history.

        Args:
            user_id: Telegram user ID
        """
        if user_id in self._conversations:
            del self._conversations[user_id]

    def is_active(self, user_id: int) -> bool:
        """
        Check if user has an active conversation.

        Args:
            user_id: Telegram user ID

        Returns:
            True if conversation is active, False otherwise
        """
        return (
            user_id in self._conversations
            and self._conversations[user_id].get("active", False)
        )


# Global conversation manager instance
conversation_manager = ConversationManager()

