from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import zmq


def send_images_to_web():
    print("ljawda")
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        jpg = socket.recv(copy=False)
        yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+jpg+b'\r\n'


@Request.application
def application(request):
    return Response(send_images_to_web(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
