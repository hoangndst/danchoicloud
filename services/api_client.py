import httpx
from typing import Dict, Any, Optional

from config.settings import settings


class APIClient:
    """Client for making HTTP requests to external APIs."""

    def __init__(self):
        """Initialize the API client."""
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def get_competition_standings(self, competition_id: str) -> Optional[Dict[str, Any]]:
        """
        Get competition standings.

        Args:
            competition_id: Competition ID (e.g., "PL" for Premier League)

        Returns:
            Standings data dictionary or None if error
        """
        try:
            response = await self.client.get(
                f"{settings.football_api_base_url}/competitions/{competition_id}/standings",
                headers={"X-Auth-Token": settings.football_api_token},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting competition standings: {e}")
            return None

    async def get_competition_matches(
        self, competition_id: str, date_from: str, date_to: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get competition matches within a date range.

        Args:
            competition_id: Competition ID (e.g., "PL")
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)

        Returns:
            Matches data dictionary or None if error
        """
        try:
            response = await self.client.get(
                f"{settings.football_api_base_url}/matches",
                params={
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "competitions": competition_id,
                },
                headers={
                    "X-Auth-Token": settings.football_api_token,
                    "timezone": "Asia/Ho_Chi_Minh",
                },
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting competition matches: {e}")
            return None

    async def get_cat_image(self) -> Optional[Dict[str, str]]:
        """
        Get a random cat image.

        Returns:
            Dictionary with 'photo' or 'video' key, or None if error
        """
        try:
            response = await self.client.get(
                "https://api.thecatapi.com/v1/images/search",
                headers={"x-api-key": "DEMO-API-KEY"},
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                return None

            url = data[0]["url"]
            extension = url[-3:].lower()

            if extension in ["gif", "mp4", "webm", "ogg"]:
                return {"video": url}
            return {"photo": url}
        except Exception as e:
            print(f"Error getting cat image: {e}")
            return None

    async def get_dog_image(self) -> Optional[Dict[str, str]]:
        """
        Get a random dog image.

        Returns:
            Dictionary with 'photo' or 'video' key, or None if error
        """
        try:
            response = await self.client.get("https://dog.ceo/api/breeds/image/random")
            response.raise_for_status()
            data = response.json()
            url = data.get("message")
            if not url:
                return None

            extension = url[-3:].lower()
            if extension in ["gif", "mp4", "webm", "ogg"]:
                return {"video": url}
            return {"photo": url}
        except Exception as e:
            print(f"Error getting dog image: {e}")
            return None

    async def get_gai_image(self) -> Optional[Dict[str, str]]:
        """
        Get a learning image from Google Apps Script.

        Returns:
            Dictionary with 'photo' key, or None if error
        """
        try:
            response = await self.client.get(
                "https://script.google.com/macros/s/AKfycbyGg3Wk3hWnLTGw_PLkNTFqAhpdln-pg9tkJlBGLn8MafiElQsi89QwtEQP2GfFMBxQ/exec"
            )
            response.raise_for_status()
            data = response.json()
            image_url = data.get("image")
            if image_url:
                return {"photo": image_url}
            return None
        except Exception as e:
            print(f"Error getting gai image: {e}")
            return None

    async def update_gai_image(self) -> Optional[Dict[str, str]]:
        """
        Update learning images from Google Drive.

        Returns:
            Dictionary with success/error message, or None if error
        """
        try:
            response = await self.client.get(
                "https://script.google.com/macros/s/AKfycbyGg3Wk3hWnLTGw_PLkNTFqAhpdln-pg9tkJlBGLn8MafiElQsi89QwtEQP2GfFMBxQ/exec?action=loadImage"
            )
            response.raise_for_status()
            data = response.json()
            if data.get("updated"):
                return {
                    "text": "Cập nhật tài liệu học tập thành công 🥰"
                }
            return {
                "text": "Cập nhật tài liệu không thành công 🥲, liên hệ @hoangndst hoặc mở issues tại: https://github.com/hoangndst/danchoicloud/issues"
            }
        except Exception as e:
            print(f"Error updating gai image: {e}")
            return None

    async def get_kcna_random_question(self) -> Optional[Dict[str, Any]]:
        """
        Get a random KCNA question for quiz.

        Returns:
            Quiz data dictionary, or None if error
        """
        try:
            response = await self.client.get(
                "https://script.google.com/macros/s/AKfycbyrRs_UXyaalfu2KDHZXOJPrJzlSpdRH5d_e6IZcVR0H1kAkes3nL8FOA7vH6TfXnlkkQ/exec"
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting KCNA question: {e}")
            return None

    async def get_sieu_nhan_image(self) -> Optional[Dict[str, str]]:
        """
        Get a sieu nhan image from Google Apps Script.

        Returns:
            Dictionary with 'photo' key, or None if error
        """
        try:
            response = await self.client.get(
                "https://script.google.com/macros/s/AKfycbz9Ew7sKBA2ATBe-a60-zYTWDtz1FRZlTQFkruHUVhvUB3ExIQdIQo9RGhMa5oKPaGQSw/exec"
            )
            response.raise_for_status()
            data = response.json()
            image_url = data.get("image")
            if image_url:
                return {"photo": image_url}
            return None
        except Exception as e:
            print(f"Error getting sieu nhan image: {e}")
            return None

    async def update_sieu_nhan_image(self) -> Optional[Dict[str, str]]:
        """
        Update sieu nhan images from Google Drive.

        Returns:
            Dictionary with success/error message, or None if error
        """
        try:
            response = await self.client.get(
                "https://script.google.com/macros/s/AKfycbz9Ew7sKBA2ATBe-a60-zYTWDtz1FRZlTQFkruHUVhvUB3ExIQdIQo9RGhMa5oKPaGQSw/exec?action=loadImage"
            )
            response.raise_for_status()
            data = response.json()
            if data.get("updated"):
                return {
                    "text": "Cập nhật tài liệu học tập thành công 🥰"
                }
            return {
                "text": "Cập nhật tài liệu không thành công 🥲, liên hệ @hoangndst hoặc mở issues tại: https://github.com/hoangndst/danchoicloud/issues"
            }
        except Exception as e:
            print(f"Error updating sieu nhan image: {e}")
            return None


# Global API client instance
api_client = APIClient()

