from flask import Flask, render_template, jsonify, Response
from flask_socketio import SocketIO
import sys
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

log_count = 0
log_timestamp = []
log_history = []

class StreamToSocketIO:
    def __init__(self):
        self.buffer = ""

    def write(self, message):
        global log_count, log_timestamp
        if message.strip():  # Évite les lignes vides
            socketio.emit('log', message.strip())
            log_history.append(str(message.strip()))
            log_count += 1
            current_time = time.time()
            log_timestamp.append(current_time)
            log_timestamp = [t for t in log_timestamp if t > current_time - 60]  # Conserve les logs des 60 dernières secondes

    def flush(self):
        pass  # Évite les erreurs avec stdout

sys.stdout = StreamToSocketIO()  # Redirige print() vers WebSocket

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/stats-data')
def get_stats():
    global log_timestamp, log_count  # Correction ici : cohérence des noms
    current_time = time.time()

    # Nettoyage des logs des 60 dernières secondes
    log_timestamp = [t for t in log_timestamp if current_time - t < 60]
    logs_per_minute = len(log_timestamp)

    return jsonify({
        "total_logs": log_count,
        "logs_per_minute": logs_per_minute
    })

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/logs-data')
def get_logs():
    return jsonify({"logs": log_history})

@app.route('/download-logs')
def download_logs():
    log_text = "\n".join(log_history)
    return Response(
        log_text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=logs.txt"}
    )

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
