import { scheduleWeekday, scheduleDay } from "./schedule/daily.js";
import { features } from "./features/message.js";

scheduleDay().then(() => {
  console.log("Schedule day successfully");
}).catch((error) => {
  console.log("Error scheduling day: ", error);
})

scheduleWeekday().then(() => {
  console.log("Schedule weekday successfully");
}).catch((error) => {
  console.log("Error scheduling weekday: ", error);
})


features().then(() => {
  console.log("Features successfully");
}).catch((error) => {
  console.log("Error features: ", error);
})