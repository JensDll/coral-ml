from src.app import app, capture
import threading

thread = threading.Thread(target=capture, daemon=True)
thread.start()

if __name__ == "__main__":
    app.run()
