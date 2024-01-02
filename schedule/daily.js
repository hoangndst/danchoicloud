import { a1y } from "../modules/channel.js";
import { sendMessage, sendMessageWithQuiz, sendMessageWithSchedule, sendMessageWeekdayWithSchedule, sendMessageRoutineWithSchedule } from "../modules/bot.js";
import { ALARM, LUNCH, HIGH_1, HIGH_2, LEAVE, getWeatherForecastMessage } from "../modules/message.js";
import { getKCNARandomQuestion } from "../modules/api.js";
// general
const optionsAlarms = {
  hour: 7,
  minute: 0,
  chat_id: a1y.chat_id,
  text: ALARM.message,
}

const optionsNewDay = {
  hour: 7,
  minute: 30,
  chat_id: a1y.chat_id,
  text: "Chúc mừng một ngày mới các con vợ, hãy cố gắng làm việc chăm chỉ nhé! 🙂",
}

const optionsLunch = {
  hour: 8,
  minute: 0,
  chat_id: a1y.chat_id,
  text: LUNCH.message,
}

const optionsLeave = {
  hour: 17,
  minute: 30,
  chat_id: a1y.chat_id,
  text: LEAVE.message,
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

export const scheduleDay = async () => {
  await sendMessageWithSchedule(optionsNewDay, sendMessage, getWeatherForecastMessage).then(() => {
    console.log("New day scheduled");
  }).catch((error) => {
    console.log("Error scheduling new day: ", error);
  })
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
  await sendMessageWeekdayWithSchedule(optionsLeave, sendMessage).then(() => {
    console.log("Leave scheduled");
  }).catch((error) => {
    console.log("Error scheduling leave: ", error);
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

export const scheduleRoutine = async () => {
  await sendMessageRoutineWithSchedule(sendMessageWithQuiz, getKCNARandomQuestion).then(() => {
    console.log("KCNARandomQuestion scheduled");
  }).catch((error) => {
    console.log("Error scheduling KCNARandomQuestion: ", error);
  })
}
