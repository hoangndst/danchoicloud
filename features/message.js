import { sendMessage, onCommand } from "../modules/bot.js";
import { getEPLStandings, getCommands, getEPLMatches, getWeatherForecastMessage } from "../modules/message.js";

export const eplStandings = async () => {
  onCommand(/\/epl$|epl@danchoicloud_bot$/, sendMessage, getEPLStandings, "HTML", (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const eplMatches = async () => {
  onCommand(/\/eplmatches$|eplmatches@danchoicloud_bot$/, sendMessage, getEPLMatches, "HTML", (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const commands = async () => {
  onCommand(/\/help$|help@danchoicloud_bot/, sendMessage, getCommands, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const weather = async () => {
  onCommand(/\/weather$|weather@danchoicloud_bot/, sendMessage, getWeatherForecastMessage, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const features = async () => {
  await eplStandings().then(() => {
    console.log("EPL Standings feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await commands().then(() => {
    console.log("Commands feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await eplMatches().then(() => {
    console.log("EPL Matches feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await weather().then(() => {
    console.log("Weather feature enabled");
  }).catch((error) => {
    console.log(error);
  })
}