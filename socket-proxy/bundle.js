import { createServer } from 'http';
import zmq from 'zeromq';
import { Server } from 'socket.io';
import WebSocket from 'ws';

const toBool = (data) => !!data.readUInt8(0);

const loadModel = (req) => async (id, callback) => {
    console.log(`Load model with id (${id})`);
    await req.send(id);
    const [success] = await req.receive();
    callback(toBool(success));
};

const classify = (request) => async ({ image, format }, callback) => {
    await request.send([image, format]);
    console.log(image);
    const [results] = await request.receive();
    const data = JSON.parse(results.toString());
    callback(data);
};

function apiStart() {
    const MODL_MANAGER_PORT = 7100;
    const CLASSIFY_PORT = 7200;
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
        const reqModelManger = new zmq.Request();
        reqModelManger.connect(`tcp://localhost:${MODL_MANAGER_PORT}`);
        socket.on('load model', loadModel(reqModelManger));
        const reqClassify = new zmq.Request();
        reqClassify.connect(`tcp://localhost:${CLASSIFY_PORT}`);
        socket.on('classify', classify(reqClassify));
        socket.on('disconnect', () => {
            reqModelManger.close();
            reqClassify.close();
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
