from flask import Flask
import threading
import cv2

def create_app():
    app = Flask(__name__)

    from src.bluebrints.api import bp as api_bp
    from src.bluebrints.video import bp as video_bp, read_frames

    app.register_blueprint(api_bp)
    app.register_blueprint(video_bp)
    
    cap = cv2.VideoCapture(0)
    thread = threading.Thread(target=read_frames, args=[cap], daemon=True)
    thread.start()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()