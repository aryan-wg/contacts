const http = require('http');

const options = {
  hostname: 'http://127.0.0.1:8000',
  path: '/api/v1/auth/test',
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
};


const getPosts = (times) => {
  for (let i = 0; i < times; i++) {
    let data = '';
    const request = http.request(options, (response) => {
      response.setEncoding('utf8');
      response.on('data', (chunk) => {
        data += chunk;
      });

      response.on('end', () => {
        console.log(data);
      });
    });

    request.on('error', (error) => {
      console.error(error);
    });

    request.end();
  }
};

// getPosts(10);

const getRes = (times) => {
  let data = [];
  for (let i = 0; i < times; i++) {
    http.get('http://127.0.0.1:8000/v1/auth/test', (res) => {
      dt = []
      res.on("data", (d) => {
        dt.push(d);
      }).on('end', function() {
        const buffer = Buffer.concat(dt);
        str_buff = buffer.toString()
        console.log(str_buff)
        // const obj = JSON.parse();
        // data.push(obj)
      })
    }).on('error', (err) => {
      console.error(err)
    })
  }
  console.log(data)
  return 0
}

getRes(510)
