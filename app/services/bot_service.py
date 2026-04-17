import telebot
from app.core.config import settings

# Khởi tạo Bot instance
bot = telebot.TeleBot(settings.telegram_token)

def send_message(chat_id: int, text: str):
    """
    Gửi tin nhắn qua Telegram
    """
    bot.send_message(chat_id, text)

def send_chat_action(chat_id: int, action: str = 'typing'):
    """
    Gửi hành động (vd: đang gõ...)
    """
    bot.send_chat_action(chat_id, action)

def send_photo(chat_id: int, photo_url: str, caption: str = ""):
    """
    Gửi hình ảnh (mã QR) qua Telegram
    """
    bot.send_photo(chat_id, photo_url, caption=caption)
