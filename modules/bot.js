import TelegramBot from "node-telegram-bot-api";
import dotenv from 'dotenv';
import schedule from "node-schedule";
dotenv.config();

const TOKEN = process.env.TELEGRAM_TOKEN;
const bot = new TelegramBot(TOKEN, { polling: true });
console.log("Current  date time: " + new Date().toLocaleString());
console.log("Bot server started, token: " + bot.token);

export const sendMessage = async (options) => {
  try {
    const message = await bot.sendMessage(options.chat_id, options.text, { ...options.options })
    console.log("Message sent successfully", message);
  } catch (error) {
    console.log("Error sending message: ", error)
  }
};

export const sendMessageWithQuiz = async (optionsQuiz) => {
  try {
    const message = await bot.sendPoll(optionsQuiz.chat_id, optionsQuiz.text, optionsQuiz.poll_options, { ...optionsQuiz.options })
    console.log("Quiz sent successfully", message);
  } catch (error) {
    console.log("Error sending quiz: ", error)
  }
}

export const sendMessageWithSchedule = async (options, asyncFunction) => {
  try {
    const j = schedule.scheduleJob(`${options.minute} ${options.hour} * * *`, async () => {
      await asyncFunction(options);
      console.log("Message sent successfully")
    });
  } catch (error) {
    console.log("Error sending message: ", error)
  }
}

export const sendMessageWeekdayWithSchedule = async (options, asyncFunction) => {
  try {
    const j = schedule.scheduleJob(`${options.minute} ${options.hour} * * 1-5`, async () => {
      await asyncFunction(options);
      console.log("Message sent successfully")
    });
  } catch (error) {
    console.log("Error sending message: ", error)
  }
}
