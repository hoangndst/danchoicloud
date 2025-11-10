import aiosqlite
from pathlib import Path
from typing import List, Dict, Optional

MAX_HISTORY_MESSAGES = 100  # Maximum messages to return in get_history


class ConversationManager:
    """Manages conversation state and history for each user using SQLite."""

    def __init__(self, db_path: str = "data/conversations.db"):
        """
        Initialize the conversation manager with SQLite database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._db: aiosqlite.Connection = None
        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """Ensure database connection is initialized and tables exist."""
        if self._initialized:
            return

        # Create data directory if it doesn't exist
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

        # Connect to database
        self._db = await aiosqlite.connect(self.db_path)
        self._db.row_factory = aiosqlite.Row
        
        # Enable foreign keys
        await self._db.execute("PRAGMA foreign_keys = ON")

        # Create tables
        await self._create_tables()
        self._initialized = True

    async def _create_tables(self) -> None:
        """Create database tables if they don't exist."""
        async with self._db.cursor() as cursor:
            # Create conversations table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    username TEXT PRIMARY KEY,
                    active INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create messages table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES conversations(username) ON DELETE CASCADE
                )
            """)

            # Create indexes for better query performance
            await cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_username_created_at 
                ON messages(username, created_at DESC)
            """)

            await self._db.commit()

    async def start_conversation(self, username: str) -> None:
        """
        Start a new conversation for a user.

        Args:
            username: Telegram username
        """
        if not username:
            raise ValueError("Username cannot be empty")
            
        await self._ensure_initialized()

        async with self._db.cursor() as cursor:
            # Insert or update conversation
            await cursor.execute("""
                INSERT INTO conversations (username, active, created_at, updated_at)
                VALUES (?, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(username) DO UPDATE SET
                    active = 1,
                    updated_at = CURRENT_TIMESTAMP
            """, (username,))
            await self._db.commit()

    async def add_message(self, username: str, role: str, message: str) -> None:
        """
        Add a message to conversation history.

        Args:
            username: Telegram username
            role: Message role ("user" or "model")
            message: Message content
        """
        if not username:
            raise ValueError("Username cannot be empty")
            
        await self._ensure_initialized()

        # Ensure conversation exists
        await self.start_conversation(username)

        try:
            async with self._db.cursor() as cursor:
                # Insert message
                await cursor.execute("""
                    INSERT INTO messages (username, role, message, created_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (username, role, message))

                # Update conversation updated_at
                await cursor.execute("""
                    UPDATE conversations
                    SET updated_at = CURRENT_TIMESTAMP
                    WHERE username = ?
                """, (username,))

                await self._db.commit()
        except Exception as e:
            print(f"Error adding message to database: {e}")
            print(f"Username: {username}, Role: {role}, Message length: {len(message) if message else 0}")
            raise

    async def get_history(self, username: str) -> List[Dict[str, str]]:
        """
        Get conversation history for a user (max 100 messages).

        Args:
            username: Telegram username

        Returns:
            List of messages in format [{"role": "user"/"model", "message": "..."}]
            Ordered by created_at ASC (oldest first)
        """
        if not username:
            return []
            
        await self._ensure_initialized()

        async with self._db.cursor() as cursor:
            await cursor.execute("""
                SELECT role, message
                FROM messages
                WHERE username = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (username, MAX_HISTORY_MESSAGES))

            rows = await cursor.fetchall()
            # Reverse to get oldest first
            history = [
                {"role": row["role"], "message": row["message"]}
                for row in reversed(rows)
            ]
            return history

    async def end_conversation(self, username: str) -> None:
        """
        End conversation for a user and delete all data.

        Args:
            username: Telegram username
        """
        if not username:
            return
            
        await self._ensure_initialized()

        async with self._db.cursor() as cursor:
            # Delete conversation (CASCADE will delete all messages)
            await cursor.execute("""
                DELETE FROM conversations
                WHERE username = ?
            """, (username,))
            await self._db.commit()

    async def is_active(self, username: str) -> bool:
        """
        Check if user has an active conversation.

        Args:
            username: Telegram username

        Returns:
            True if conversation is active, False otherwise
        """
        if not username:
            return False
            
        await self._ensure_initialized()

        async with self._db.cursor() as cursor:
            await cursor.execute("""
                SELECT active
                FROM conversations
                WHERE username = ?
            """, (username,))
            row = await cursor.fetchone()
            if row is None:
                return False
            # SQLite returns INTEGER, convert to bool
            active_value = row["active"]
            return bool(active_value) if active_value is not None else False

    async def close(self) -> None:
        """Close database connection."""
        if self._db:
            await self._db.close()
            self._initialized = False


# Global conversation manager instance
conversation_manager = ConversationManager()
