import axios from "axios";

export const getWeatherForecast = async () => {
  const options = {
    method: 'GET',
    url: 'https://weatherapi-com.p.rapidapi.com/current.json',
    params: {q: 'Hanoi'},
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

export const getEPLStandings = async () => {
  const options = {
    method: 'GET',
    url: 'http://api.football-data.org/v4/competitions/PL/standings',
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

// getEPLStandings().then(data => {
//   console.log(data.standings[0].table);
// })

export const getEPLTodayMatches = async (dateFrom, dateTo) => {
  const options = {
    method: 'GET',
    url: 'http://api.football-data.org/v4/matches',
    params: {dateFrom: dateFrom, dateTo: dateTo, competitions: 'PL'},
    headers: {
      'X-Auth-Token': 'fd206c7fc72449a199f8b8a2e91ef5f5',
      'timezone': 'Asia/Ho_Chi_Minh'
      // 'X-Unfold-Goals': true
    }
  };
  try {
    const response = await axios.request(options);
    const data = response.data;
    const formatOptions = {timeZone: 'Asia/Ho_Chi_Minh', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'};
    let from = new Date(dateFrom).toLocaleString('en-US', formatOptions).slice(0, 10);
    let to = new Date(dateTo)
    to.setDate(to.getDate() - 1);
    to = to.toLocaleString('en-US', formatOptions).slice(0, 10);
    for (let i = 0; i < data.matches.length; i++) {
      data.matches[i].utcDate = new Date(data.matches[i].utcDate).toLocaleString('en-US', formatOptions);
      if (data.matches[i].utcDate.slice(0, 10) !== from && data.matches[i].utcDate.slice(0, 10) !== to) {
        data.matches.splice(i, 1);
        i--;
      }
    }
    return data;
  } catch (error) {
    console.error(error);
  }
}

// getEPLTodayMatches('2023-12-29', '2023-12-31').then(data => {
//   console.log(data.matches);
// })
