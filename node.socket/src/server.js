import zmq from "zeromq";
import { Server } from "socket.io";
import { createServer } from "http";
const port = 5555;
const listen = 5000;
const sock = new zmq.Subscriber();
sock.connect(`tcp://localhost:${port}`);
sock.subscribe("");
console.log(`Subscriber connected to port ${port}`);
const httpServer = createServer();
const io = new Server(httpServer, {
    cors: {
        origin: "*",
    },
});
async function startReading() {
    for await (const [frame] of sock) {
        io.emit("video:stream", frame);
    }
}
startReading();
io.on("connection", socket => {
    console.log(`A user connected (${socket.id})`);
    socket.on("disconnect", () => {
        console.log(`A user disconnected (${socket.id})`);
    });
});
httpServer.listen(listen);
console.log(`Server listening on port ${listen}`);
//# sourceMappingURL=server.js.map