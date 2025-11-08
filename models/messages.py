"""Message templates and constants."""

from dataclasses import dataclass
from typing import Dict, Any

# Day names in Vietnamese
DAY = [
    "chủ nhật",
    "thứ Hai",
    "thứ Ba",
    "thứ Tư",
    "thứ Năm",
    "thứ Sáu",
    "thứ Bảy",
]

# General messages
ALARM = {
    "time": "7:00:00 AM",
    "message": "𝗟𝗢𝗔𝗟𝗢𝗔𝗟𝗢𝗔 📢📢📢\nDậy đi làm đi các con vợ ☀️📣 mất hơn 6 lít bây giờ :)\n@hoangndst @amunn35 @tuda_2 @sonbm1 @crvt4722 @duongtm3 @ndvinhcn",
}

LUNCH = {
    "time": "8:00:00 AM",
    "message": "Đặt cơm đi các con vợ, quên là ra ngoài ăn cơm tấm nhé! 🙂🍚🍌",
}

LEAVE = {
    "time": "5:30:00 AM",
    "message": "Đến giờ về rồi, về thôi các người anh em 😏, không về thì xuống A1Y cơ sở tầng 12 để high nào 🙂",
}

HIGH_1 = {
    "time": "9:30:00 AM",
    "message": "Đến giờ đi ngắm trời ngắm mây rồi các người anh em 😶‍🌫️. Tầng 12 nhé!",
}

HIGH_2 = {
    "time": "3:30:00 PM",
    "message": "Happy time rồi các con vợ, xuống tầng 12 cùng high nào 😶‍🌫️",
}

# Bot commands
COMMANDS = [
    {
        "command": "start",
        "description": "Start with @danchoicloud",
    },
]

