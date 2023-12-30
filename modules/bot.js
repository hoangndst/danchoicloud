import TelegramBot from "node-telegram-bot-api";
import dotenv from "dotenv";
import schedule from "node-schedule";
import { COMMANDS } from "./message.js";
dotenv.config();

const TOKEN = process.env.TELEGRAM_TOKEN;
const bot = new TelegramBot(TOKEN, { polling: true });
bot.setMyCommands(COMMANDS);
console.log("Current  date time: " + new Date().toLocaleString());
console.log("Bot server started, token: " + bot.token);

export const sendMessage = async (options) => {
  try {
    const message = await bot.sendMessage(options.chat_id, options.text, {
      ...options.options,
    });
    console.log("Message sent successfully", message);
  } catch (error) {
    console.log("Error sending message: ", error);
  }
};

export const sendMessageWithMedia = async (options) => {
  try {
    if (options.photo) {
      const message = await bot.sendPhoto(options.chat_id, options.photo, {
        ...options.options,
      });
      console.log("Message sent successfully", message);
    } else if (options.video) {
      const message = await bot.sendVideo(options.chat_id, options.video, {
        ...options.options,
      });
      console.log("Message sent successfully", message);
    } else if (options.audio) {
      const message = await bot.sendAudio(options.chat_id, options.audio, {
        ...options.options,
      });
      console.log("Message sent successfully", message);
    } else if (options.document) {
      const message = await bot.sendDocument(
        options.chat_id,
        options.document,
        {
          ...options.options,
        }
      );
      console.log("Message sent successfully", message);
    } else if (options.animation) {
      const message = await bot.sendAnimation(
        options.chat_id,
        options.animation,
        {
          ...options.options,
        }
      );
      console.log("Message sent successfully", message);
    } else if (options.voice) {
      const message = await bot.sendVoice(options.chat_id, options.voice, {
        ...options.options,
      });
      console.log("Message sent successfully", message);
    } 

  } catch (error) {
    console.log("Error sending message: ", error);
  }
}

export const sendMessageWithQuiz = async (optionsQuiz) => {
  try {
    const message = await bot.sendPoll(
      optionsQuiz.chat_id,
      optionsQuiz.text,
      optionsQuiz.poll_options,
      { ...optionsQuiz.options }
    );
    console.log("Quiz sent successfully", message);
  } catch (error) {
    console.log("Error sending quiz: ", error);
  }
};

export const sendMarkdownMessage = async (options) => {
  try {
    const message = await bot.sendMessage(options.chat_id, options.text, {
      ...options.options,
      parse_mode: "Markdown",
    });
    console.log("Message sent successfully", message);
  } catch (error) {
    console.log("Error sending message: ", error);
  }
};

export const sendMessageWithSchedule = async (options, asyncFunction, asyncGetMessageFunction) => {
  try {
    const j = schedule.scheduleJob(
      `${options.minute} ${options.hour} * * *`,
      async () => {
        asyncGetMessageFunction && (options.text = await asyncGetMessageFunction());
        await asyncFunction(options);
        console.log("Message sent successfully");
      }
    );
  } catch (error) {
    console.log("Error sending message: ", error);
  }
};

export const sendMessageWeekdayWithSchedule = async (
  options,
  asyncFunction
) => {
  try {
    const j = schedule.scheduleJob(
      `${options.minute} ${options.hour} * * 1-5`,
      async () => {
        await asyncFunction(options);
        console.log("Message sent successfully");
      }
    );
  } catch (error) {
    console.log("Error sending message: ", error);
  }
};

export const onCommand = async (command, asyncFunction, asyncGetMessageFunction, subOptions) => {
  bot.onText(command, (response) => {
    let options = {
      chat_id: response.chat.id,
      options: {
        ...subOptions,
        message_thread_id: response.message_thread_id || null,  
      },
    };
    asyncGetMessageFunction().then((additionalOption) => {
      options = {
        ...options,
        ...additionalOption,
      };
      asyncFunction(options).then(() => {
        console.log("Message sent successfully");
      }).catch((error) => {
        console.log(error);
      })
    }).catch((error) => {
      console.log(error);
    })
  });
};
