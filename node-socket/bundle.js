import zmq from 'zeromq';
import { Server } from 'socket.io';
import { createServer } from 'http';

const listen = 6100;
const httpServer = createServer();
new Server(httpServer, {
    maxHttpBufferSize: 1e9,
    cors: {
        origin: '*'
    }
});
const subscriber = new zmq.Subscriber();
subscriber.connect(`tcp://192.168.178.54:5555`);
subscriber.subscribe('');
readVideo(subscriber);
async function readVideo(subscriber) {
    for await (const [frame] of subscriber) {
        console.log(frame.length);
        // socket.emit('video stream', frame)
    }
}
// io.on('connection', socket => {
//   console.log(`A user connected (${socket.id})`)
//   const subscriber = new zmq.Subscriber()
//   subscriber.connect(`tcp://localhost:${subscriberPort}`)
//   subscriber.subscribe('')
//   readVideo(socket, subscriber)
//   const modelManger = new zmq.Request()
//   modelManger.connect(`tcp://localhost:${modelManagerPort}`)
//   socket.on('load model', loadModel(modelManger))
//   const classification = new zmq.Request()
//   classification.connect(`tcp://localhost:${classificationPort}`)
//   socket.on('image classification', classify(classification))
//   socket.on('disconnect', () => {
//     subscriber.close()
//     console.log(`A user disconnected (${socket.id})`)
//   })
// })
httpServer.listen(listen);
console.log(`Server listening on port ${listen}`);
