import zmq from 'zeromq';
import { Server } from 'socket.io';
import { createServer } from 'http';

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

const modelManagerPort = 5600;
const classifyPort = 5700;
const listen = 6100;
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
    reqModelManger.connect(`tcp://localhost:${modelManagerPort}`);
    socket.on('load model', loadModel(reqModelManger));
    const reqClassify = new zmq.Request();
    reqClassify.connect(`tcp://localhost:${classifyPort}`);
    socket.on('image classification', classify(reqClassify));
    socket.on('disconnect', () => {
        reqModelManger.close();
        reqClassify.close();
        console.log(`A user disconnected (${socket.id})`);
    });
});
httpServer.listen(listen);
console.log(`Server listening on port ${listen}`);
