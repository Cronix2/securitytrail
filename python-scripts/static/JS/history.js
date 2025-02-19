function fetchLogs() {
    fetch('/logs-data')
        .then(response => response.json())
        .then(data => {
            const logContainer = document.getElementById("logHistory");
            logContainer.innerHTML = "";
            data.logs.forEach(log => {
                const logItem = document.createElement("div");
                logItem.classList.add("log-item");
                logItem.textContent = log;
                logContainer.appendChild(logItem);
            });
        })
        .catch(error => console.error('Error fetching logs:', error));
}

function downloadLogs() {
    window.location.href = "/download-logs";
}

// Rafraîchit les logs toutes les 3 secondes
setInterval(fetchLogs, 1000);

// Charge immédiatement les logs au chargement de la page
document.addEventListener("DOMContentLoaded", fetchLogs);