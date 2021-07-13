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
    const [results] = await request.receive();
    const data = JSON.parse(results.toString());
    callback(data);
};

const subscriberPort = 5500;
const modelManagerPort = 5600;
const classificationPort = 5700;
const listen = 6100;
const httpServer = createServer();
const io = new Server(httpServer, {
    maxHttpBufferSize: 1e9,
    cors: {
        origin: '*'
    }
});
async function readVideo(socket, subscriber) {
    for await (const [frame] of subscriber) {
        console.log(frame);
        // socket.emit('video stream', frame)
    }
}
io.on('connection', socket => {
    console.log(`A user connected (${socket.id})`);
    const subscriber = new zmq.Subscriber();
    subscriber.connect(`tcp://192.168.178.54:${subscriberPort}`);
    subscriber.subscribe('');
    readVideo(socket, subscriber);
    const modelManger = new zmq.Request();
    modelManger.connect(`tcp://localhost:${modelManagerPort}`);
    socket.on('load model', loadModel(modelManger));
    const classification = new zmq.Request();
    classification.connect(`tcp://localhost:${classificationPort}`);
    socket.on('image classification', classify(classification));
    socket.on('disconnect', () => {
        subscriber.close();
        console.log(`A user disconnected (${socket.id})`);
    });
});
httpServer.listen(listen);
console.log(`Server listening on port ${listen}`);
