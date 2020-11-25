const cheerio = require('cheerio');
const axios = require('axios');
const fs = require('fs');
const url = require('url');
const http = require('http');
const https = require('https');
var sizeOfImg = require('image-size');

const hostname = '127.0.0.1'
const port = process.env.PORT || 3000;
// console.log(process.env);
// console.log('The value of PORT is:', process.env.PORT);

const server = http.createServer((req, res) => {
  res.statusCode = 200
  res.setHeader('Content-Type', 'text/plain')
  res.end('Resource Tool\n')
})

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`)
})

const externalURL = [  {
  "category": "Food",
  "website": "https://www.cunyurbanfoodpolicy.org/",
  "tags": ["food", "nutrition"]
}];

let readJSONFile = (r) => {
  let linkdata = fs.readFileSync('links.json');
  let resource_links = JSON.parse(linkdata);
  // let resource_links = externalURL;

  resource_links.map(function (propObj) {
    let externalURL = propObj.website;
    // Using Axios
    axios.get(externalURL)
    .then(response => {
      getData(response.data, propObj);
    })
    .catch(error => {
      console.log("error",error);
    });
  });
}
readJSONFile();

// Using Cheerio
data = [];
let getData = (html, pObj) => {
  const $ = cheerio.load(html);
  $('body').each( (i,elem) => {
    let dataTITLE = $(elem.parent).find('title')[0] ? $(elem.parent).find('title')[0].children[0].data : pObj.category;
    let dataTXT = $(elem).find('p');

    let strLong = [];
    dataTXT.map(function (p,txt) {
      let pText = $(this).text();
      if (pText.length > 300 && !pText.includes('function')) {
        strLong.push(pText);
      }
      return true;
    });

    data.push({
      website: pObj.website,
      title: dataTITLE,
      description: (strLong[0] == null) ? "&nbsp;" : strLong[0],
      extImg: "",
      category: pObj.category
    });
  });
  // console.log("data", data);
  createJSONFile(data);
}

let createJSONFile = (d) => {
  let data = JSON.stringify(d);
  fs.writeFileSync('resources.json', data);
}
