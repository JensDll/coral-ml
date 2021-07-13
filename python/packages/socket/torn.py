from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
import cv2
import simplejpeg


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")


class StreamHandler(RequestHandler):
    def initialize(self, cap) -> None:
        self.cap = cap

    def get(self):
        has_frame, frame = self.cap.read()
        self.set_header(
            "mimetype", "multipart/x-mixed-replace; boundary=frame")
        self.set_header("")

        jpg = simplejpeg.encode_jpeg(
            frame, quality=95, colorspace="rgb", fastdct=True)

        return b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n"


def make_app():
    cap = cv2.VideoCapture(0)

    return Application([
        (r"/", MainHandler, dict(cap=cap)),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()
