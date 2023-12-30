import axios from "axios";

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

// getEPLStandings().then(data => {
//   console.log(data.standings[0].table);
// })

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
    // DD/MM/YYYY\nHH:mm AM
    const formatOptions = {timeZone: 'Asia/Ho_Chi_Minh', year: 'numeric', month: '2-digit', day: '2-digit', hour: 'numeric', minute: 'numeric', hour12: true};
    let from = new Date(dateFrom).toLocaleString('en-US', formatOptions).slice(0, 10);
    let to = new Date(dateTo)
    to.setDate(to.getDate() - 1);
    to = to.toLocaleString('en-US', formatOptions).slice(0, 10);
    for (let i = 0; i < data.matches.length; i++) {
      // "DD/MM/YYYY\nHH:mm AM"
      let utcDate = new Date(data.matches[i].utcDate).toLocaleString('en-US', formatOptions);
      data.matches[i].utcDate = utcDate.slice(0, 10) + '\n' + utcDate.slice(11, 17) + utcDate.slice(utcDate.length - 2, utcDate.length);
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

// getCompetitionTodayMatches("PL", '2023-12-29', '2023-12-31').then(data => {
//   console.log(data.matches);
// })
