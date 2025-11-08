from datetime import datetime
from typing import Dict, Any


def format_weather_message(data: Dict[str, Any]) -> str:
    """
    Format weather forecast message.

    Args:
        data: Weather data from API

    Returns:
        Formatted weather message
    """
    if not data or "current" not in data:
        return "Weather data not available"

    DAY = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    day = datetime.now().weekday()
    current = data["current"]

    message = "👋 Hello everyone!\n"
    message += f"Happy {DAY[day]} everyone — keep up the good work! 🙂\n\n"
    message += "🌤️ Hanoi weather forecast for today:\n"
    message += f"Last updated: {current.get('last_updated', 'N/A')}\n"
    message += f"Weather condition: {current.get('condition', {}).get('text', 'N/A')}\n"
    message += f"Temperature: {current.get('temp_c', 'N/A')}°C\n"
    message += f"Feels like: {current.get('feelslike_c', 'N/A')}°C\n"
    message += f"Wind speed: {current.get('wind_kph', 'N/A')} km/h\n"
    message += f"Humidity: {current.get('humidity', 'N/A')}%\n"
    message += f"Pressure: {current.get('pressure_mb', 'N/A')} mb\n"
    message += f"Visibility: {current.get('vis_km', 'N/A')} km\n"
    message += f"UV index: {current.get('uv', 'N/A')}\n"

    icon_url = current.get('condition', {}).get('icon', '')
    if icon_url:
        message += f"👉 Details: https:{icon_url}\n"

    return message


def format_commands_message() -> str:
    """
    Format help/commands message.

    Returns:
        Formatted commands help message
    """
    message = "ℹ️ <b>Help</b>\n\n"
    message += "👋 Hey there!\n\n"
    message += "I got you — here are some things I can help with:\n"
    message += "Just pick from the menu bro, I got you! 😎\n\n"

    message += "Contribute at 👨‍💻: https://github.com/hoangndst/danchoicloud\n"
    message += "Issues 🥲: contact <tg-spoiler>@hoangndst</tg-spoiler> or open an issue at: <a href='https://github.com/hoangndst/danchoicloud/issues'>issues</a>"

    return message

