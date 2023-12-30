import { getCompetitionStandings, getCompetitionMatches, getWeatherForecast } from "./api.js";
import { table } from "table";

// var
export const DAY = [
  "chủ nhật",
  "thứ Hai",
  "thứ Ba",
  "thứ Tư",
  "thứ Năm",
  "thứ Sáu",
  "thứ Bảy",
];

// general
export const ALARM = {
  time: "7:00:00 AM",
  message:
    "𝗟𝗢𝗔𝗟𝗢𝗔𝗟𝗢𝗔 📢📢📢\nDậy đi làm đi các con vợ ☀️📣 mất hơn 6 lít bây giờ :)\n@hoangndst @amunn35 @tuda_2 @sonbm1 @crvt4722 @duongtm3 @ndvinhcn",
};
export const LUNCH = {
  time: "8:00:00 AM",
  message: "Đặt cơm đi các con vợ, quên là ra ngoài ăn cơm tấm nhé! 🙂🍚🍌",
};

export const LEAVE = {
  time: "5:30:00 AM",
  message:
    "Đến giờ về rồi, về thôi các người anh em 😏, không về thì xuống A1Y cơ sở tầng 12 để high nào 🙂",
};

export const HIGH_1 = {
  time: "9:30:00 AM",
  message:
    "Đến giờ đi ngắm trời ngắm mây rồi các người anh em 😶‍🌫️. Tầng 12 nhé!",
};

export const HIGH_2 = {
  time: "3:30:00 PM",
  message: "Happy time rồi các con vợ, xuống tầng 12 cùng high nào 😶‍🌫️",
};

export const COMMANDS = [
  {
    command: "/help",
    description: "Help",
  },
  {
    command: "/epl",
    description: "EPL Standings",
  },
  {
    command: "/eplmatches",
    description: "Today matches",
  },
  {
    command: "/weather",
    description: "Today weather",
  },
];

export const getCommands = async () => {
  let message = "@danchoicloud_bot commands:\n";
  for (let i = 0; i < COMMANDS.length; i++) {
    message += `${COMMANDS[i].command} - ${COMMANDS[i].description}\n`;
  }
  return message;
};

export const getEPLStandings = async () => {
  const data = await getCompetitionStandings("PL");
  let config, messageTable, output;

  messageTable = [];
  messageTable.push(["Id", "Team", "Pts"]);

  for (let i = 0; i < data.standings[0].table.length; i++) {
    messageTable.push([
      data.standings[0].table[i].position,
      data.standings[0].table[i].team.name,
      data.standings[0].table[i].points,
    ]);
  }

  config = {
    header: {
      alignment: "center",
      content: "EPL Standings",
    },
    columns: {
      0: {
        alignment: "center",
        width: 2,
      },
      1: {
        alignment: "left",
        width: 20,
      },
      2: {
        alignment: "center",
        width: 3,
      },
    },
    border: {
      topBody: `-`,
      topJoin: `+`,
      topLeft: `+`,
      topRight: `+`,

      bottomBody: `-`,
      bottomJoin: `+`,
      bottomLeft: `+`,
      bottomRight: `+`,

      bodyLeft: `|`,
      bodyRight: `|`,
      bodyJoin: `|`,

      joinBody: `-`,
      joinLeft: `+`,
      joinRight: `+`,
      joinJoin: `+`,
    },
  };

  output = table(messageTable, config);
  return `<pre>${output}</pre>`;
};

export const getEPLMatches = async () => {
  let dateFrom = new Date();
  let dateTo = new Date();
  dateTo.setDate(dateTo.getDate() + 2);
  dateFrom = dateFrom.toISOString().slice(0, 10);
  dateTo = dateTo.toISOString().slice(0, 10);
  const data = await getCompetitionMatches("PL", dateFrom, dateTo);
  let config, messageTable, output;
  messageTable = [];
  messageTable.push(["Match", "Time"]);
  for (let i = 0; i < data.matches.length; i++) {
    let match =
      data.matches[i].homeTeam.name + "\n" + data.matches[i].awayTeam.name;
    let time = data.matches[i].utcDate;
    messageTable.push([match, time]);
  }

  config = {
    header: {
      alignment: "center",
      content: "EPL Today Matches",
    },
    columns: {
      0: {
        alignment: "left",
        width: 20,
      },
      1: {
        alignment: "left",
        width: 10,
      },
    },
    border: {
      topBody: `-`,
      topJoin: `+`,
      topLeft: `+`,
      topRight: `+`,

      bottomBody: `-`,
      bottomJoin: `+`,
      bottomLeft: `+`,
      bottomRight: `+`,

      bodyLeft: `|`,
      bodyRight: `|`,
      bodyJoin: `|`,

      joinBody: `-`,
      joinLeft: `+`,
      joinRight: `+`,
      joinJoin: `+`,
    },
  };
  output = table(messageTable, config);
  return `<pre>${output}</pre>`;
};

export const getWeatherForecastMessage = async () => {
  const data = await getWeatherForecast("Hanoi");
  const day = new Date().getDay();
  let newDayMessage = "👋 Xin chào các người anh em!\n";
  newDayMessage += `Chúc mừng một ngày ${DAY[day]} các con vợ, hãy cố gắng làm việc chăm chỉ nhé! 🙂\n\n`
  newDayMessage += "🌤️ Dự báo thời tiết Hà Nội hôm nay:\n";
  newDayMessage += `Cập nhật gần nhất: ${data.current.last_updated}\n`;
  newDayMessage += `Tình trạng thời tiết: ${data.current.condition.text}\n`;
  newDayMessage += `Nhiệt độ: ${data.current.temp_c}°C\n`;
  newDayMessage += `Nhiệt độ cảm giác: ${data.current.feelslike_c}°C\n`;
  newDayMessage += `Tốc độ gió: ${data.current.wind_kph} km/h\n`;
  newDayMessage += `Độ ẩm: ${data.current.humidity}%\n`;
  newDayMessage += `Áp suất: ${data.current.pressure_mb} mb\n`;
  newDayMessage += `Tầm nhìn: ${data.current.vis_km} km\n`;
  newDayMessage += `Chỉ số UV: ${data.current.uv}\n`;
  newDayMessage += `👉 Chi tiết: https:${data.current.condition.icon}\n`;
  return newDayMessage;
};
