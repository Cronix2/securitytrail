from flask import Flask, render_template, jsonify, Response
from flask_socketio import SocketIO
import sys
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

log_history = []  # Historique des logs
log_timestamp = []  # Liste des timestamps des logs
log_count = 0  # Compteur total de logs
logs_per_minutes = 0  # Logs par minute
logs_per_minute = []  # Moyenne des logs par minute (max 60 éléments)
log_average_per_hour = []  # Moyenne des logs par heure (max 24 éléments)
log_average_per_day = []  # Moyenne des logs par jour (max 30 éléments)
log_average_per_day_total = []  # Moyenne des logs par jour sans limite

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
    global logs_per_minutes, log_timestamp, log_count, logs_per_minute, log_average_per_hour, log_average_per_day, log_average_per_day_total
    
    current_time = time.time()

    # Nettoyage des logs des 60 dernières secondes
    log_timestamp = [t for t in log_timestamp if current_time - t < 60]
    logs_per_minute_value = len(log_timestamp)

    # the average of logs per minute
    logs_per_minutes = logs_per_minute_value

    # Gestion de la liste logs_per_minute (max 60 éléments)
    if len(logs_per_minute) >= 60:
        logs_per_minute.pop(0)
    logs_per_minute.append(logs_per_minute_value)

    # Calcul de la moyenne des logs par heure
    log_average_per_hour_value = round(sum(logs_per_minute) / len(logs_per_minute), 1) if logs_per_minute else 0

    # Gestion de la liste log_average_per_hour (max 24 éléments)
    if len(log_average_per_hour) >= 24:
        log_average_per_hour.pop(0)
    log_average_per_hour.append(log_average_per_hour_value)

    # Calcul de la moyenne des logs par jour
    log_average_per_day_value = round(sum(log_average_per_hour) / len(log_average_per_hour), 1) if log_average_per_hour else 0

    # Gestion de la liste log_average_per_day (max 30 éléments)
    if len(log_average_per_day) >= 30:
        log_average_per_day.pop(0)
    log_average_per_day.append(log_average_per_day_value)

    # Ajout de la moyenne journalière dans log_average_per_day_total (sans limite)
    log_average_per_day_total.append(log_average_per_day_value)

    return jsonify({
        "total_logs": log_count,
        "logs_per_minutes": logs_per_minutes,
        "logs_per_minute": logs_per_minute,
        "log_average_per_hour": log_average_per_hour,
        "log_average_per_day": log_average_per_day,
        "log_average_per_day_total": log_average_per_day_total
    })

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/test')
def test():
    return render_template('test.html')

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
