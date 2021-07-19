import { createServer } from 'http';
import zmq from 'zeromq';
import { Server } from 'socket.io';
import WebSocket from 'ws';

const toBool = (data) => !!data.readUInt8(0);

const loadModel = (client) => async (id, callback) => {
    console.log(`Load model with id (${id})`);
    await client.send(id);
    const [success] = await client.receive();
    callback(toBool(success));
};

const classify = (client) => async ({ image, format }, callback) => {
    console.log(image);
    // await client.send([image, format])
    // const [result] = await client.receive()
    // const data: Response = JSON.parse(result.toString())
    callback({ data: 'auiwzvd' });
};

const updateVideo = (client) => async (data, callback) => {
    console.log(data);
    await client.send(JSON.stringify(data));
    await client.receive();
    callback();
};

function apiStart(host) {
    const MODL_MANAGER_PORT = 7100;
    const CLASSIFY_PORT = 7200;
    const VIDEO_PORT = 7300;
    const LISTEN = 5050;
    const httpServer = createServer();
    const io = new Server(httpServer, {
        maxHttpBufferSize: 1e9,
        cors: {
            origin: '*',
            preflightContinue: true
        }
    });
    io.on('connection', socket => {
        console.log(`A user connected (${socket.id})`);
        const modelManagerClient = new zmq.Request();
        modelManagerClient.connect(`tcp://localhost:${MODL_MANAGER_PORT}`);
        socket.on('load model', loadModel(modelManagerClient));
        const classifyClient = new zmq.Request();
        classifyClient.connect(`tcp://localhost:${CLASSIFY_PORT}`);
        socket.on('classify', classify());
        const videoClient = new zmq.Request();
        videoClient.connect(`tcp://localhost:${VIDEO_PORT}`);
        socket.on('update video', updateVideo(videoClient));
        socket.on('disconnect', () => {
            classifyClient.close();
            classifyClient.close();
            console.log(`A user disconnected (${socket.id})`);
        });
    });
    httpServer.listen(LISTEN, host);
    console.log(`API listening on http://${host}:${LISTEN}`);
}

function videoStart(host) {
    const SOCKET_PORT = 8080;
    const LISTEN = 5060;
    var wss = new WebSocket.Server({
        port: SOCKET_PORT,
        host,
        perMessageDeflate: false
    });
    wss.on('connection', (ws, req) => {
        console.log(`Client connected ${req.socket.remoteAddress}`);
        ws.on('close', () => {
            console.log(`Client disconnected ${req.socket.remoteAddress}`);
        });
    });
    async function broadcastData(data) {
        wss.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(data);
            }
        });
    }
    const server = createServer((request, response) => {
        request.on('data', data => {
            console.log(data);
            broadcastData(data);
        });
    });
    server.headersTimeout = 0;
    server.listen(LISTEN, host);
    console.log(`Listening for incomming MPEG-TS Stream on http://${host}:${LISTEN}`);
    console.log(`Awaiting WebSocket connections on ws://${host}:${SOCKET_PORT}`);
}

apiStart("localhost");
videoStart("localhost");
