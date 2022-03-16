const http = require("http");

const server = http.createServer((req, res) => {
    res.end(`
        <!doctype html>
        <html>
        <body style="font-size: 30px; font-family: sans-serif; margin: 0;">
        <div style="display: flex; flex-direction: column; width: 100vw; height: 100vh; align-items: center; justify-content: center;">
            <div>Hello world!</div>
        </div>
        </body>
        </html>
    `)
});

server.listen(80)
