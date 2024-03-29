import { sendMessage, onCommand, sendMessageWithMedia, sendMessageWithQuiz } from "../modules/bot.js";
import { getEPLStandings, getCommands, getEPLMatches, getWeatherForecastMessage } from "../modules/message.js";
import { getCatImage, getDogImage, getGaiImage, updateGaiImage, getKCNARandomQuestion, getSieuNhanImage, updateSieuNhanImage } from "../modules/api.js";

export const eplStandings = async () => {
  onCommand(/\/epl$|epl@danchoicloud_bot$/, sendMessage, getEPLStandings, { parse_mode: "HTML" }, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const eplMatches = async () => {
  onCommand(/\/eplmatches$|eplmatches@danchoicloud_bot$/, sendMessage, getEPLMatches, { parse_mode: "HTML" }, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const commands = async () => {
  onCommand(/\/help$|help@danchoicloud_bot/, sendMessage, getCommands, { parse_mode: "HTML", disable_web_page_preview: true }, (msg) => {
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

export const cat = async () => {
  onCommand(/\/cat$|cat@danchoicloud_bot/, sendMessageWithMedia, getCatImage, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const dog = async () => {
  onCommand(/\/dog$|dog@danchoicloud_bot/, sendMessageWithMedia, getDogImage, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const gai = async () => {
  onCommand(/\/hoctap$|hoctap@danchoicloud_bot/, sendMessageWithMedia, getGaiImage, { has_spoiler: true }, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const updateGai = async () => {
  onCommand(/\/updatehoctap$|updatehoctap@danchoicloud_bot/, sendMessage, updateGaiImage, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const kcna = async () => {
  onCommand(/\/kcna$|kcna@danchoicloud_bot/, sendMessageWithQuiz, getKCNARandomQuestion, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const sieuNhan = async () => {
  onCommand(/\/sieunhan$|sieunhan@danchoicloud_bot/, sendMessageWithMedia, getSieuNhanImage, { has_spoiler: true }, (msg) => {
    console.log("Command received: ", msg.text);
  }).catch((error) => {
    console.log(error);
  })
}

export const updateSieuNhan = async () => {
  onCommand(/\/updatesieunhan$|updatesieunhan@danchoicloud_bot/, sendMessage, updateSieuNhanImage, (msg) => {
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

  await cat().then(() => {
    console.log("Cat feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await dog().then(() => {
    console.log("Dog feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await gai().then(() => {
    console.log("Gai feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await updateGai().then(() => {
    console.log("Update Gai feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await kcna().then(() => {
    console.log("KCNA feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await sieuNhan().then(() => {
    console.log("Sieu Nhan feature enabled");
  }).catch((error) => {
    console.log(error);
  })

  await updateSieuNhan().then(() => {
    console.log("Update Sieu Nhan feature enabled");
  }).catch((error) => {
    console.log(error);
  })
}