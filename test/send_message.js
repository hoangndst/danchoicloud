import {
  sendMessageWithSchedule,
  sendMarkdownMessage,
  sendMessage,
  sendMessageWithMedia,
  onCommand 
} from "../modules/bot.js";
import { a1y } from "../modules/channel.js";
// import { getCompetitionStandings, getCompetitionMatches, getWeatherForecast } from "../modules/api.js";
// import { table } from "table";
import { DAY, getEPLStandings, getWeatherForecastMessage, getCommands, getEPLMatches } from "../modules/message.js";

const options = {
  hour: 23,
  minute: 45,
  chat_id: a1y.chat_id,
  video: "https://i0.wp.com/www.printmag.com/wp-content/uploads/2021/02/4cbe8d_f1ed2800a49649848102c68fc5a66e53mv2.gif",
  options: {
    disable_notification: true,
  },
};

// sendMessageWithMedia(options).then((res) => {
//   console.log("Message sent successfully");
// }).catch((error) => {
//   console.log("Error sending message: ", error);
// })

// sendMessageWithSchedule(options, sendMessage).then(() => {
//   console.log("Schedule successfully");
// }).catch((error) => {
//   console.log(error);
// })

// getEPLStandings().then((data) => {
//   let config, messageTable, output;

//   messageTable = [];
//   messageTable.push(['idx', 'Team', 'Point']);

//   for (let i = 0; i < data.standings[0].table.length; i++) {
//     messageTable.push([data.standings[0].table[i].position, data.standings[0].table[i].team.name, data.standings[0].table[i].points]);
//   }

//   config = {
//     header: {
//       alignment: 'center',
//       content: 'EPL Standings',
//     },
//     columns: {
//       0: {
//         alignment: 'center',
//         width: 3,
//       },
//       1: {
//         alignment: 'left',
//         width: 20,
//       },
//       2: {
//         alignment: 'center',
//         width: 5,
//       },
//     },
//     border: {
//       topBody: `-`,
//       topJoin: `+`,
//       topLeft: `+`,
//       topRight: `+`,

//       bottomBody: `-`,
//       bottomJoin: `+`,
//       bottomLeft: `+`,
//       bottomRight: `+`,

//       bodyLeft: `|`,
//       bodyRight: `|`,
//       bodyJoin: `|`,

//       joinBody: `-`,
//       joinLeft: `+`,
//       joinRight: `+`,
//       joinJoin: `+`,
//     },
//   };

//   output = table(messageTable, config);
//   const options = {
//     hour: 21,
//     minute: 47,
//     chat_id: a1y.chat_id,
//     text: `<pre>${output}</pre>`,
//     options: {
//       parse_mode: "HTML",
//     },
//   };
//   sendMessage(options).then((res) => {
//     console.log("Message sent successfully");
//   }).catch((error) => {
//     console.log("Error sending message: ", error);
//   });
// }).catch((error) => {
//   console.log(error);
// })

// onCommand(/\/epl @danchoicloud/, (msg) => {
//   console.log("Command received: ", msg.text);
// });

// getEPLStandings().then((data) => {
//   console.log(data);
// }).catch((error) => {
//   console.log(error);
// })


// onCommand(/\/ok/, sendMessage, getEPLMatches, "HTML", (msg) => {
//   console.log("Command received: ", msg.text);
// }).catch((error) => {
//   console.log(error);
// })

// 


// YYYY-MM-DD
// let dateFrom = new Date()
// let dateTo = new Date()
// dateTo.setDate(dateTo.getDate() + 2)
// dateFrom = dateFrom.toISOString().slice(0, 10)
// dateTo = dateTo.toISOString().slice(0, 10)
// getCompetitionMatches("PL", dateFrom, dateTo).then((data) => {
//   let config, messageTable, output;
//   messageTable = [];
//   messageTable.push(['Match', 'Time']);
//   for (let i = 0; i < data.matches.length; i++) {
//     let match = data.matches[i].homeTeam.name + '\n' + data.matches[i].awayTeam.name;
//     let time = data.matches[i].utcDate;
//     messageTable.push([match, time]);
//   }

//   config = {
//     header: {
//       alignment: 'center',
//       content: 'EPL Today Matches',
//     },
//     columns: {
//       0: {
//         alignment: 'left',
//         width: 26,
//       },
//       1: {
//         alignment: 'center',
//         width: 12,
//       },
//     },
//     border: {
//       topBody: `-`,
//       topJoin: `+`,
//       topLeft: `+`,
//       topRight: `+`,

//       bottomBody: `-`,
//       bottomJoin: `+`,
//       bottomLeft: `+`,
//       bottomRight: `+`,

//       bodyLeft: `|`,
//       bodyRight: `|`,
//       bodyJoin: `|`,

//       joinBody: `-`,
//       joinLeft: `+`,
//       joinRight: `+`,
//       joinJoin: `+`,
//     },
//   };
//   output = table(messageTable, config);
//   console.log(output);
// }).catch((error) => {
//   console.log(error);
// })

// getWeatherForecast("Hanoi").then((data) => {
//   const day = new Date().getDay();
//   let newDayMessage = "👋 Xin chào các người anh em!\n"
//   newDayMessage += `Buổi sáng ${DAY[day]} tốt lành! 😄.\n\n`
//   newDayMessage += "🌤️ Dự báo thời tiết Hà Nội hôm nay:\n"
//   newDayMessage += `Cập nhật gần nhất: ${data.current.last_updated}\n`
//   newDayMessage += `Tình trạng thời tiết: ${data.current.condition.text}\n`
//   newDayMessage += `Nhiệt độ: ${data.current.temp_c}°C\n`
//   newDayMessage += `Nhiệt độ cảm giác: ${data.current.feelslike_c}°C\n`
//   newDayMessage += `Tốc độ gió: ${data.current.wind_kph} km/h\n`
//   newDayMessage += `Độ ẩm: ${data.current.humidity}%\n`
//   newDayMessage += `Áp suất: ${data.current.pressure_mb} mb\n`
//   newDayMessage += `Tầm nhìn: ${data.current.vis_km} km\n`
//   newDayMessage += `Chỉ số UV: ${data.current.uv}\n`
//   newDayMessage += `👉 Chi tiết: https:${data.current.condition.icon}\n`
//   console.log(newDayMessage);
// })