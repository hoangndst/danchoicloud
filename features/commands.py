from telegram import Update
from telegram.ext import ContextTypes

from services.typing_indicator import with_typing
from services.api_client import api_client
from utils.formatters import (
    format_weather_message,
    format_commands_message,
)
from bot.handlers import send_message, send_photo, send_video, send_poll


@with_typing
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        text = format_commands_message()
        await send_message(
            update, context, text, parse_mode="HTML", disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Error in help_command: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi hiển thị danh sách lệnh.")


@with_typing
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = await api_client.get_weather_forecast("Hanoi")
        if data:
            text = format_weather_message(data)
            await send_message(update, context, text)
        else:
            await send_message(update, context, "Không thể lấy dữ liệu thời tiết.")
    except Exception as e:
        print(f"Error in weather: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi lấy dữ liệu thời tiết.")


@with_typing
async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = await api_client.get_cat_image()
        if data:
            if "photo" in data:
                await send_photo(update, context, data["photo"])
            elif "video" in data:
                await send_video(update, context, data["video"])
            else:
                await send_message(update, context, "Không thể lấy ảnh mèo.")
        else:
            await send_message(update, context, "Không thể lấy ảnh mèo.")
    except Exception as e:
        print(f"Error in cat: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi lấy ảnh mèo.")


@with_typing
async def dog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = await api_client.get_dog_image()
        if data:
            if "photo" in data:
                await send_photo(update, context, data["photo"])
            elif "video" in data:
                await send_video(update, context, data["video"])
            else:
                await send_message(update, context, "Không thể lấy ảnh chó.")
        else:
            await send_message(update, context, "Không thể lấy ảnh chó.")
    except Exception as e:
        print(f"Error in dog: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi lấy ảnh chó.")


@with_typing
async def hoctap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = await api_client.get_gai_image()
        if data and "photo" in data:
            await send_photo(update, context, data["photo"], has_spoiler=True)
        else:
            await send_message(update, context, "Không thể lấy ảnh học tập.")
    except Exception as e:
        print(f"Error in hoctap: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi lấy ảnh học tập.")


@with_typing
async def updatehoctap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = await api_client.update_gai_image()
        if data and "text" in data:
            await send_message(update, context, data["text"])
        else:
            await send_message(update, context, "Không thể cập nhật ảnh học tập.")
    except Exception as e:
        print(f"Error in updatehoctap: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi cập nhật ảnh học tập.")


@with_typing
async def kcna(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = await api_client.get_kcna_random_question()
        if data:
            question = data.get("question", "")
            options = data.get("options", [])
            if question and options:
                await send_poll(
                    update,
                    context,
                    question,
                    options,
                    is_anonymous=data.get("is_anonymous", False),
                )
            else:
                await send_message(update, context, "Không thể lấy câu hỏi KCNA.")
        else:
            await send_message(update, context, "Không thể lấy câu hỏi KCNA.")
    except Exception as e:
        print(f"Error in kcna: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi lấy câu hỏi KCNA.")


@with_typing
async def sieunhan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = await api_client.get_sieu_nhan_image()
        if data and "photo" in data:
            await send_photo(update, context, data["photo"], has_spoiler=True)
        else:
            await send_message(update, context, "Không thể lấy ảnh siêu nhân.")
    except Exception as e:
        print(f"Error in sieunhan: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi lấy ảnh siêu nhân.")


@with_typing
async def updatesieunhan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        data = await api_client.update_sieu_nhan_image()
        if data and "text" in data:
            await send_message(update, context, data["text"])
        else:
            await send_message(update, context, "Không thể cập nhật ảnh siêu nhân.")
    except Exception as e:
        print(f"Error in updatesieunhan: {e}")
        await send_message(update, context, "Đã có lỗi xảy ra khi cập nhật ảnh siêu nhân.")

