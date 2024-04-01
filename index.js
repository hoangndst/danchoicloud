import { scheduleWeekday, scheduleDay, scheduleRoutine } from "./schedule/daily.js";
import { features } from "./features/message.js";

// scheduleDay().then(() => {
//   console.log("Schedule day successfully");
// }).catch((error) => {
//   console.log("Error scheduling day: ", error);
// })

// scheduleWeekday().then(() => {
//   console.log("Schedule weekday successfully");
// }).catch((error) => {
//   console.log("Error scheduling weekday: ", error);
// })

scheduleRoutine().then(() => {
  console.log("Schedule routine successfully");
}).catch((error) => {
  console.log("Error scheduling routine: ", error);
})

features().then(() => {
  console.log("Features successfully");
}).catch((error) => {
  console.log("Error features: ", error);
})