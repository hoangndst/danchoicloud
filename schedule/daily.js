import { a1y } from "../modules/channel.js";
import { sendMessage, sendMessageWithQuiz, sendMessageWeekdayWithSchedule } from "../modules/bot.js";
import { ALARM, LUNCH, HIGH_1, HIGH_2 } from "../modules/message.js";

// general
const optionsAlarms = {
  hour: 7,
  minute: 0,
  chat_id: a1y.chat_id,
  text: ALARM.message,
}

const optionsLunch = {
  hour: 8,
  minute: 0,
  chat_id: a1y.chat_id,
  text: LUNCH.message,
}

// a1y co so tang 12
const optionsHigh1 = {
  hour: 9,
  minute: 30,
  chat_id: a1y.chat_id,
  text: HIGH_1.message,
  options: {
    message_thread_id: a1y.topics[0].message_thread_id,
  },
}

const optionsHigh2 = {
  hour: 15,
  minute: 30,
  chat_id: a1y.chat_id,
  text: HIGH_2.message,
  options: {
    message_thread_id: a1y.topics[0].message_thread_id,
  },
}

export const scheduleWeekday = async () => {
  await sendMessageWeekdayWithSchedule(optionsAlarms, sendMessage).then(() => {
    console.log("Alarm scheduled");
  }).catch((error) => {
    console.log("Error scheduling alarm: ", error);
  });
  await sendMessageWeekdayWithSchedule(optionsLunch, sendMessage).then(() => {
    console.log("Lunch scheduled");
  }).catch((error) => {
    console.log("Error scheduling lunch: ", error);
  });
  await sendMessageWeekdayWithSchedule(optionsHigh1, sendMessage).then(() => {
    console.log("High 1 scheduled");
  }).catch((error) => {
    console.log("Error scheduling high 1: ", error);
  });
  await sendMessageWeekdayWithSchedule(optionsHigh2, sendMessage).then(() => {
    console.log("High 2 scheduled");
  }).catch((error) => {
    console.log("Error scheduling high 2: ", error);
  });
}
