from flask import Flask, render_template
from flask_socketio import SocketIO
import sys
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

class StreamToSocketIO:
    def __init__(self):
        self.buffer = ""

    def write(self, message):
        if message.strip():  # Évite les lignes vides
            socketio.emit('log', message.strip())

    def flush(self):
        pass  # Nécessaire pour éviter des erreurs avec stdout

sys.stdout = StreamToSocketIO()  # Redirige print() vers WebSocket

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

def run_script():
    while True:
        print(f"Test print")
        time.sleep(60)  # Simule des logs périodiques

def start():
    threading.Thread(target=run_script, daemon=True).start()
    flask_thread = threading.Thread(target=lambda: socketio.run(app, host='0.0.0.0', port=8081, allow_unsafe_werkzeug=True), daemon=True)
    flask_thread.start()


if __name__ == '__main__':
    start()
