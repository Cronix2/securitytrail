from flask import Flask, render_template, jsonify, Response, request
from flask_socketio import SocketIO
import socket
import sys
import threading
import time
import docker
import os
import re
from datetime import datetime
from random import randint


app = Flask(__name__)
socketio = SocketIO(app)

ENV_FILE_PATH = ".env"

log_history = []  # Historique des logs
log_timestamp = []  # Liste des timestamps des logs
last_minute_timestamp = None  # Stocke le dernier timestamp utilisé pour logs_per_minute
last_hour_timestamp = None  # Stocke le dernier timestamp utilisé pour logs_per_hour
last_day_timestamp = None  # Stocke le dernier timestamp utilisé pour logs_per_day
last_week_timestamp = None  # Stocke le dernier timestamp utilisé pour logs_per_week
last_month_timestamp = None  # Stocke le dernier timestamp utilisé pour logs_per_month

# Stockage des logs et moyennes
# Stockage des logs et moyennes
log_entries = []  # Stocke chaque log avec son timestamp
log_count = 0  # Compteur total de logs
logs_per_second = []  # Dernières 60 secondes
logs_per_minute = []  # Dernières 60 minutes
logs_per_hour = []  # Dernières 24 heures
logs_per_day = []  # Derniers 7 jours
logs_per_week = []  # Dernières 4 semaines
logs_per_month = []  # Derniers 12 mois


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Vérification stricte des lignes du .env
EXPECTED_KEYS = ["API_KEY=", "DB_USER=", "DB_PASSWORD=", "DB_HOST="]
VALID_CHARS = re.compile(r"^[a-zA-Z0-9\s\-_,.=@\"]+$")

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
            add_log()
            current_time = time.time()
            log_timestamp.append(current_time)
            log_timestamp = [t for t in log_timestamp if t > current_time - 60]  # Conserve les logs des 60 dernières secondes

    def flush(self):
        pass  # Évite les erreurs avec stdout

sys.stdout = StreamToSocketIO()  # Redirige print() vers WebSocket

# Fonction d'ajout et de gestion des limites
def update_log_storage(log_list, new_value, max_size):
    if len(log_list) >= max_size:
        log_list.pop(0)  # Supprime la plus ancienne valeur
    log_list.append(new_value)  # Ajoute la nouvelle valeur


# Fonction d'ajout et de gestion des limites
def update_log_averages():
    global logs_per_second, logs_per_minute, logs_per_hour, logs_per_day, logs_per_week, logs_per_month
    global last_minute_timestamp, last_hour_timestamp, last_day_timestamp, last_week_timestamp, last_month_timestamp

    current_time = time.time()
    timestamp_str = datetime.fromtimestamp(current_time).strftime('%Y/%m/%d-%H:%M:%S')

    # Logs/sec : Comptage des logs dans la dernière seconde
    logs_per_second_value = len([t for t in log_entries if current_time - t < 1])
    update_log_storage(logs_per_second, [logs_per_second_value, timestamp_str], 60)

    # * Vérifie si **exactement 60 secondes** se sont écoulées pour logs_per_minute
    current_minute = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M')
    if len(logs_per_second) == 60 and last_minute_timestamp != current_minute:
        logs_per_minute_value = round(sum(l[0] for l in logs_per_second), 2)
        update_log_storage(logs_per_minute, [logs_per_minute_value, timestamp_str], 60)
        last_minute_timestamp = current_minute  # Met à jour le dernier timestamp

    # * Vérifie si **exactement 60 minutes** se sont écoulées pour logs_per_hour
    current_hour = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H')
    if len(logs_per_minute) == 60 and last_hour_timestamp != current_hour:
        logs_per_hour_value = round(sum(l[0] for l in logs_per_minute), 2)
        update_log_storage(logs_per_hour, [logs_per_hour_value, timestamp_str], 24)
        last_hour_timestamp = current_hour  # Met à jour le dernier timestamp

    # * Vérifie si **exactement 24 heures** se sont écoulées pour logs_per_day
    current_day = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d')
    if len(logs_per_hour) == 24 and last_day_timestamp != current_day:
        logs_per_day_value = round(sum(l[0] for l in logs_per_hour), 2)
        update_log_storage(logs_per_day, [logs_per_day_value, timestamp_str], 7)
        last_day_timestamp = current_day  # Met à jour le dernier timestamp

    # * Vérifie si **exactement 7 jours** se sont écoulés pour logs_per_week
    current_week = datetime.fromtimestamp(current_time).strftime('%Y-W%W')  # Format YYYY-WW (semaine de l'année)
    if len(logs_per_day) == 7 and last_week_timestamp != current_week:
        logs_per_week_value = round(sum(l[0] for l in logs_per_day), 2)
        update_log_storage(logs_per_week, [logs_per_week_value, timestamp_str], 4)
        last_week_timestamp = current_week  # Met à jour le dernier timestamp

    # * Vérifie si **exactement 4 semaines** se sont écoulées pour logs_per_month
    current_month = datetime.fromtimestamp(current_time).strftime('%Y-%m')  # Format YYYY-MM
    if len(logs_per_week) == 4 and last_month_timestamp != current_month:
        logs_per_month_value = round(sum(l[0] for l in logs_per_week), 2)
        update_log_storage(logs_per_month, [logs_per_month_value, timestamp_str], 12)
        last_month_timestamp = current_month  # Met à jour le dernier timestamp



# Fonction d'ajout d'un log
def add_log():
    global log_count
    current_time = time.time()
    log_entries.append(current_time)
    log_count += 1
    update_log_averages()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/stats-data')
def get_stats():
    return jsonify({
        "total_logs": log_count,
        "logs_per_second": logs_per_second,
        "logs_per_minute": logs_per_minute,
        "log_average_per_hour": logs_per_hour,
        "log_average_per_day": logs_per_day,
        "log_average_per_week": logs_per_week,
        "log_average_per_month": logs_per_month
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

@app.route('/settings')
def settings():
    return render_template('env_create.html')


@app.route('/upload-env', methods=['POST'])
def upload_env():
    if 'file' not in request.files:
        return jsonify({"message": "Aucun fichier reçu"}), 400

    file = request.files['file']

    print(f"Fichier reçu : {file.filename}")

    if not file.filename.endswith(".env"):
        return jsonify({"message": "Le fichier doit être un .env"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, ".env")
    file.save(file_path)

    print("Fichier sauvegardé, vérification du contenu...")

    with open(file_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    print("Contenu du fichier reçu :")
    for i, line in enumerate(lines):
        print(f"Ligne {i+1}: {line.strip()}")

    if len(lines) != 4:
        return jsonify({"message": "Le fichier doit contenir exactement 4 lignes"}), 400

    for i, line in enumerate(lines):
        line = line.strip()
        if not line.startswith(EXPECTED_KEYS[i]) or len(line) > 100 or not VALID_CHARS.match(line):
            print(f"Erreur format ligne {i+1}: {line}")
            return jsonify({"message": f"Erreur format à la ligne {i+1}"}), 400

    print("Fichier .env valide ✅")
    # Si tout est bon, on remplace le .env actuel
    # Open the file and write the content
    with open(ENV_FILE_PATH, 'w', encoding="utf-8") as f:
        f.writelines(lines)
    return jsonify({"message": "Fichier .env valide !"}), 200

@app.route('/info-env', methods=['GET'])
def info_env():
    """ Route pour récupérer le contenu du fichier .env en JSON """
    if not os.path.exists(ENV_FILE_PATH):
        return jsonify({"error": "Fichier .env introuvable"}), 404

    env_data = {}
    # create random data for not leak the real data
    with open(ENV_FILE_PATH, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            key, value = line.strip().split("=")
            if i == 0:
                env_data[key] = "".join([chr(randint(65, 90)) for _ in range(15)])
            else:
                env_data[key] = "".join([chr(randint(65, 90)) for _ in range(randint(4, 8))])

    return jsonify([env_data])  # Renvoie un tableau JSON contenant un objet

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
