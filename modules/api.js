import axios from "axios";
import moment from "moment";

export const getWeatherForecast = async (location) => {
  const options = {
    method: 'GET',
    url: 'https://weatherapi-com.p.rapidapi.com/current.json',
    params: {q: location, lang: 'vi'},
    headers: {
      'X-RapidAPI-Key': 'fd29828369msh6ecbf93e3a975ccp132c46jsn1396d8957227',
      'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'
    }
  };
  try {
    const response = await axios.request(options);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

export const getCompetitionStandings = async (competitionId) => {
  const options = {
    method: 'GET',
    url: `http://api.football-data.org/v4/competitions/${competitionId}/standings`,
    headers: {
      'X-Auth-Token': 'fd206c7fc72449a199f8b8a2e91ef5f5'
    }
  };
  try {
    const response = await axios.request(options);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

export const getCompetitionMatches = async (competitionId, dateFrom, dateTo) => {
  const options = {
    method: 'GET',
    url: 'http://api.football-data.org/v4/matches',
    params: {dateFrom: dateFrom, dateTo: dateTo, competitions: competitionId},
    headers: {
      'X-Auth-Token': 'fd206c7fc72449a199f8b8a2e91ef5f5',
      'timezone': 'Asia/Ho_Chi_Minh'
      // 'X-Unfold-Goals': true
    }
  };
  try {
    const response = await axios.request(options);
    const data = response.data;
    let from = new Date(dateFrom);
    let to = new Date(dateTo)
    to.setDate(to.getDate() - 1);
    for (let i = 0; i < data.matches.length; i++) {
      // "DD/MM/YYYY\nhh:mm AM"
      let utc = new Date(data.matches[i].utcDate);
      if (utc > to) {
        data.matches.splice(i, 1);
        i--;
      } else {
        let utcDate = moment(new Date(data.matches[i].utcDate)).format('DD/MM/YYYY hh:mm');
        data.matches[i].utcDate = utcDate.slice(0, 10) + '\n' + utcDate.slice(utcDate.length - 5, utcDate.length);
      }
    }
    return data;
  } catch (error) {
    console.error(error);
  }
}

export const getCatImage = async () => {
  const options = {
    method: 'GET',
    url: 'https://api.thecatapi.com/v1/images/search',
    headers: {
      'x-api-key': 'DEMO-API-KEY'
    }
  };
  try {
    const response = await axios.request(options);
    if (response.data[0].url.slice(response.data[0].url.length - 3, response.data[0].url.length) === 'gif' || 
        response.data[0].url.slice(response.data[0].url.length - 3, response.data[0].url.length) === 'mp4' ||
        response.data[0].url.slice(response.data[0].url.length - 3, response.data[0].url.length) === 'webm' ||
        response.data[0].url.slice(response.data[0].url.length - 3, response.data[0].url.length) === 'ogg') {
      return { video: response.data[0].url };
    }
    return { photo: response.data[0].url };
  } catch (error) {
    console.error(error);
  }
}

export const getDogImage = async () => {
  const options = {
    method: 'GET',
    url: 'https://dog.ceo/api/breeds/image/random'
  };
  try {
    const response = await axios.request(options);
    // check if the image is a gif or mp4 set { video: response.data.message } else set { photo: response.data.message }
    if (response.data.message.slice(response.data.message.length - 3, response.data.message.length) === 'gif' || 
        response.data.message.slice(response.data.message.length - 3, response.data.message.length) === 'mp4' ||
        response.data.message.slice(response.data.message.length - 3, response.data.message.length) === 'webm' ||
        response.data.message.slice(response.data.message.length - 3, response.data.message.length) === 'ogg') {
      return { video: response.data.message };
    }
    return { photo: response.data.message };
  } catch (error) {
    console.error(error);
  }
}

export const getGaiImage = async () => {
  const options = {
    method: 'GET',
    url: 'https://script.google.com/macros/s/AKfycbyGg3Wk3hWnLTGw_PLkNTFqAhpdln-pg9tkJlBGLn8MafiElQsi89QwtEQP2GfFMBxQ/exec'
  };
  try {
    const response = await axios.request(options);
    return { photo: response.data.image };
  } catch (error) {
    console.error(error);
  }
}

export const updateGaiImage = async () => {
  const options = {
    method: 'GET',
    url: 'https://script.google.com/macros/s/AKfycbyGg3Wk3hWnLTGw_PLkNTFqAhpdln-pg9tkJlBGLn8MafiElQsi89QwtEQP2GfFMBxQ/exec?action=loadImage'
  };
  try {
    const response = await axios.request(options);
    if (response.data.updated) {
      return { text: 'Cập nhật tài liệu học tập thành công 🥰' };
    } 
    return { text: 'Cập nhật tài liệu không thành công 🥲, liên hệ @hoangndst hoặc mở issues tại: https://github.com/hoangndst/danchoicloud/issues' };
  } catch (error) {
    console.error(error);
  }
}

export const getKCNARandomQuestion = async () => {
  const options = {
    method: 'GET',
    url: 'https://script.google.com/macros/s/AKfycbyrRs_UXyaalfu2KDHZXOJPrJzlSpdRH5d_e6IZcVR0H1kAkes3nL8FOA7vH6TfXnlkkQ/exec'
  };
  try {
    const response = await axios.request(options);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

