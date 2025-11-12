import httpx
from typing import Optional, Dict, Any, List

from config.settings import settings


class GenkitService:
    """Service for interacting with Genkit API."""

    def __init__(self):
        """Initialize the Genkit service."""
        self.client = httpx.AsyncClient(timeout=60.0, follow_redirects=True)
        self.api_url = settings.genkit_api_url

    async def chat(
        self,
        message: str,
        username: str,
        platform: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """
        Send a chat message to Genkit API.

        Args:
            message: User's message
            username: Telegram username (used as user identifier for AI API)
            platform: Platform of the user (telegram, facebook, instagram, etc.)
            history: Optional conversation history in format [{"role": "user"/"model", "message": "..."}]

        Returns:
            AI response text or None if error
        """
        try:
            # Convert history format from {"role": "user"/"model", "message": "..."}
            # to format expected by Genkit API (messageSchema format)
            genkit_history = None
            if history:
                genkit_history = []
                for msg in history:
                    genkit_history.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("message", "")
                    })

            payload = {
                "message": message,
                "username": username,
                "platform": platform,
            }
            if genkit_history:
                payload["history"] = genkit_history

            response = await self.client.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract response text from API response
            if isinstance(data, dict):
                # Check success field first
                if data.get("success") is False:
                    print(f"Genkit API returned success=false: {data}")
                    return None
                
                # Get response field
                ai_response = data.get("response")
                if ai_response:
                    return ai_response
                
                # Fallback to other possible fields
                return data.get("message") or data.get("text") or None
            elif isinstance(data, str):
                return data
            else:
                print(f"Unexpected response format from Genkit API: {type(data)}")
                return None
        except Exception as e:
            print(f"Error calling Genkit API: {e}")
            return None

    async def close(self):
        """Close the Genkit service."""
        await self.client.aclose()


# Global Genkit service instance
genkit_service = GenkitService()

