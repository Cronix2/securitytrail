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
    '''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Live Logs</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.3.2/socket.io.js"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    var socket = io();
                    socket.on('log', function(msg) {
                        var logContainer = document.getElementById("logs");
                        var logEntry = document.createElement("p");
                        logEntry.textContent = msg;
                        logContainer.appendChild(logEntry);
                    });
                });
            </script>
        </head>
        <body>
            <h1>Logs en temps réel</h1>
            <div id="logs" style="background: #000; color: #0f0; padding: 10px; height: 400px; overflow-y: scroll;"></div>
        </body>
        </html>
    '''
def run_script():
    while True:
        print(f"Test print: {time.strftime('%H:%M:%S')}")
        time.sleep(60)  # Simule des logs périodiques

def start():
    threading.Thread(target=run_script, daemon=True).start()
    flask_thread = threading.Thread(target=lambda: socketio.run(app, host='0.0.0.0', port=8081, allow_unsafe_werkzeug=True), daemon=True)
    flask_thread.start()


if __name__ == '__main__':
    start()
