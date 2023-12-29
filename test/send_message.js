import {
  sendMessageWithSchedule,
  sendMarkdownMessage,
  sendMessage
} from "../modules/bot.js";
import { a1y } from "../modules/channel.js";
import { getEPLStandings } from "../modules/api.js";
import { table } from "table";

const options = {
  hour: 23,
  minute: 45,
  chat_id: a1y.chat_id,
  text: "danchoicloud release v0.1.1\nimage: hoangndst/danchoicloud:v0.1.1\ngithub: https://github.com/hoangndst/danchoicloud",
};

// sendMessageWithSchedule(options, sendMessage).then(() => {
//   console.log("Schedule successfully");
// }).catch((error) => {
//   console.log(error);
// })

getEPLStandings().then((data) => {
  let config, messageTable, output;

  messageTable = [];
  messageTable.push(['Position', 'Team', 'Point']);

  for (let i = 0; i < data.standings[0].table.length; i++) {
    messageTable.push([data.standings[0].table[i].position, data.standings[0].table[i].team.name, data.standings[0].table[i].points]);
  }

  config = {
    header: {
      alignment: 'center',
      content: 'EPL Standings',
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
  const options = {
    hour: 21,
    minute: 47,
    chat_id: a1y.chat_id,
    text: `<pre>${output}</pre>`,
    options: {
      parse_mode: "HTML",
    },
  };
  sendMessage(options).then((res) => {
    console.log("Message sent successfully");
  }).catch((error) => {
    console.log("Error sending message: ", error);
  });
}).catch((error) => {
  console.log(error);
})
