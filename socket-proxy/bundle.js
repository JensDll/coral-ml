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
    await client.send([image, format]);
    const [result] = await client.receive();
    const data = JSON.parse(result.toString());
    callback(data);
};

const updateVideo = (client) => async (data, callback) => {
    console.log(data);
    await client.send(JSON.stringify(data));
    await client.receive();
    callback();
};

function apiStart() {
    const MODL_MANAGER_PORT = 7100;
    const CLASSIFY_PORT = 7200;
    const VIDEO_PORT = 7300;
    const LISTEN = 5050;
    const httpServer = createServer();
    const io = new Server(httpServer, {
        maxHttpBufferSize: 1e9,
        cors: {
            origin: '*'
        }
    });
    io.on('connection', socket => {
        console.log(`A user connected (${socket.id})`);
        const modelManagerClient = new zmq.Request();
        modelManagerClient.connect(`tcp://localhost:${MODL_MANAGER_PORT}`);
        socket.on('load model', loadModel(modelManagerClient));
        const classifyClient = new zmq.Request();
        classifyClient.connect(`tcp://localhost:${CLASSIFY_PORT}`);
        socket.on('classify', classify(classifyClient));
        const videoClient = new zmq.Request();
        videoClient.connect(`tcp://localhost:${VIDEO_PORT}`);
        socket.on('update video', updateVideo(videoClient));
        socket.on('disconnect', () => {
            classifyClient.close();
            classifyClient.close();
            console.log(`A user disconnected (${socket.id})`);
        });
    });
    httpServer.listen(LISTEN);
    console.log(`API listening on http://127.0.0.1:${LISTEN}`);
}

function videoStart() {
    const SOCKET_PORT = 8080;
    const LISTEN = 5060;
    var wss = new WebSocket.Server({
        port: SOCKET_PORT,
        perMessageDeflate: false
    });
    wss.on('connection', (ws, req) => {
        console.log(`Client connected ${req.socket.remoteAddress}`);
        ws.on('close', () => {
            console.log(`Client disconnected ${req.socket.remoteAddress}`);
        });
    });
    function broadcastData(data) {
        wss.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(data);
            }
        });
    }
    const server = createServer((request, response) => {
        request.on('data', data => {
            broadcastData(data);
        });
    });
    server.headersTimeout = 0;
    server.listen(LISTEN);
    console.log(`Listening for incomming MPEG-TS Stream on http://127.0.0.1:${LISTEN}`);
    console.log(`Awaiting WebSocket connections on ws://127.0.0.1:${SOCKET_PORT}`);
}

apiStart();
videoStart();
