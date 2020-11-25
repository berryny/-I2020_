const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

const url = "https://news.ycombinator.com/";

// Using Axios
axios.get(url)
  .then(response => {
    console.log(response.data);
    getData(response.data);

  })
  .catch(error => {
    console.log("error",error);
  })

// Using Cheerio
let getData = html => {
  data = [];
  const $ = cheerio.load(html);
  $('body').each( (i,elem) => {
    console.log('elem',$(elem).find('img'));
    data.push({
      title: $(elem.parent).find('title').text()
    });
  });
  console.log("data", data);
}
