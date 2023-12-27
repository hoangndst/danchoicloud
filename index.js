// const TelegramBot = require('node-telegram-bot-api');

import dotenv from 'dotenv';
dotenv.config();

const TOKEN = process.env.TELEGRAM_TOKEN;
import { alarm } from './modules/message.js';

console.log(alarm);
// Create a bot that uses 'polling' to fetch new updates
// const bot = new TelegramBot(TOKEN, {polling: true});

function sendMessage() {
  options = {
    "chat_id": "-1002001746838",
    "text": "Dậy đi làm đi các con vợ ☀️📣 mất hơn 6 lít bây giờ :)\n@hoangndst @amunn35 @tuda_2 @sonbm1 @crvt4722 @duongtm3 @ndvinhcn",
    "message_thread_id": 2179,
    "is_topic_message": true
  }
  bot.sendMessage(options.chat_id, options.text, {reply_to_message_id: options.message_thread_id});
}
// sendMessage();
