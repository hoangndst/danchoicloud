import TelegramBot from "node-telegram-bot-api";
import dotenv from 'dotenv';
dotenv.config();

const TOKEN = process.env.TELEGRAM_TOKEN;
const bot = new TelegramBot(TOKEN, { polling: true });

export const sendMessage = async (options, isTopicMessage = false) => {
  try {
    const message = await bot.sendMessage(options.chat_id, options.text,
      isTopicMessage ? { reply_to_message_id: options.message_thread_id } : {});
    console.log("Message sent successfully")
  } catch (error) {
    console.log(error);
  }
};