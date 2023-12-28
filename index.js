import { scheduleWeekday } from "./schedule/daily.js";

scheduleWeekday().then(() => {
  console.log("Schedule weekday successfully");
}).catch((error) => {
  console.log("Error scheduling weekday: ", error);
})