from flask import Flask, render_template, jsonify, Response
from flask_socketio import SocketIO
import socket
import sys
import threading
import time
import docker
from datetime import datetime


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

# Liste des services à checker avec leur port et type
services = {
    "PHPMyAdmin": {
        "type": "docker",  # On vérifie s'il répond sur son port HTTP
        "host": "supervision-db",  # Nom du conteneur
        "link": "localhost:8080",  # Lien pour accéder à PHPMyAdmin
        "port": 8080,
        "uptime": 0,
        "last_state": False
    },
    "Database": {
        "type": "docker",
        "host": "DB-subdomains",  # Utiliser le nom du conteneur pour accéder à MariaDB
        "link": "localhost:3306",  # Lien pour accéder à MariaDB
        "port": 3306,
        "uptime": 0,
        "last_state": False
    },
    "API Server": {
        "type": "http",  # On vérifie avec une requête HTTP
        "host": "api.securitytrails.com",  # C'est une API HTTP, pas un service TCP
        "link": "api.securitytrails.com",
        "port": "80",
        "uptime": 0,
        "last_state": False
    },
    "Frontend": {
        "type": "tcp",
        "host": "python-scripts",  # Utiliser le nom du conteneur si c'est en Docker
        "link": "localhost:8081",  # Lien pour accéder au Frontend
        "port": 8081,
        "uptime": 0,
        "last_state": False
    }
}

def check_tcp(host, port):
    """ Vérifie si un service TCP est UP (ex: API, Frontend). """
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.timeout, ConnectionRefusedError) as e:
        return (str(e))

def check_docker_container(container_name):
    """ Vérifie si un conteneur Docker tourne en utilisant l'API Docker. """
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        container = client.containers.get(container_name)
        return container.status == "running"
    except docker.errors.NotFound:
        return False  # Le conteneur n'existe pas
    except docker.errors.APIError as e:
        return str(e)  # Erreur de communication avec l'API

def check_http(host, port):
    """ Vérifie si un service HTTP est UP (ex: API, Frontend). """
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.timeout, ConnectionRefusedError) as e:
        return (str(e))

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
    global log_timestamp, log_count, logs_per_minute, log_average_per_hour, log_average_per_day, log_average_per_day_total
    
    current_time = time.time()
    current_time_str = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d-%H-%M-%S')

    # Nettoyage des logs des 60 dernières secondes
    log_timestamp = [t for t in log_timestamp if current_time - t < 60]
    logs_per_minute_value = len(log_timestamp)

    # the average of logs per minute
    logs_per_minutes = logs_per_minute_value

    # Gestion de la liste logs_per_minute (max 60 éléments)
    if len(logs_per_minute) >= 60:
        logs_per_minute.pop(0)
    logs_per_minute.append([logs_per_minute_value, current_time_str])

    # Calcul de la moyenne des logs par heure
    log_average_per_hour_value = round(sum(l[0] for l in logs_per_minute) / len(logs_per_minute), 1) if logs_per_minute else 0

    # Gestion de la liste log_average_per_hour (max 24 éléments)
    if len(log_average_per_hour) >= 24:
        log_average_per_hour.pop(0)
    log_average_per_hour.append([log_average_per_hour_value, current_time_str])

    # Calcul de la moyenne des logs par jour
    log_average_per_day_value = round(sum(l[0] for l in log_average_per_hour) / len(log_average_per_hour), 1) if log_average_per_hour else 0

    # Gestion de la liste log_average_per_day (max 30 éléments)
    if len(log_average_per_day) >= 30:
        log_average_per_day.pop(0)
    log_average_per_day.append([log_average_per_day_value, current_time_str])

    # Ajout de la moyenne journalière dans log_average_per_day_total (sans limite)
    log_average_per_day_total.append([log_average_per_day_value, current_time_str])

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

@app.route('/health-check')
def health_check():
    """ Endpoint Flask pour récupérer l'état des services. """
    try:
        for service, info in services.items():
            if info["type"] == "tcp":
                is_up = check_tcp(info["host"], info["port"])
            elif info["type"] == "http":
                is_up = check_http(info["host"], info["port"])
            elif info["type"] == "docker":
                is_up = check_docker_container(info["host"])
            else:
                is_up = False  # Type inconnu

            uptime_seconds = info["uptime"] + 1 if is_up else 0
            
            info["last_state"] = is_up
            info["uptime"] = uptime_seconds

        return jsonify([
            {
                "name": service,
                "status": "UP" if info["last_state"] else "DOWN",
                "uptime": info["uptime"],
                "port": info.get("port", "N/A"),
                "host": info.get("host", "N/A"),
                "link": info.get("link", "N/A")
            } for service, info in services.items()
        ])
    except Exception as e:
        return jsonify({"error": str(e)})

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
