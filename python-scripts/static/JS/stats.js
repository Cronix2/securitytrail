let selectedMetric = "logs_per_minute";
let logChartData = [];
let timeLabels = [];

const ctx = document.getElementById('logChart').getContext('2d');
const logChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: timeLabels,
        datasets: [{
            label: 'Logs',
            data: logChartData,
            borderColor: '#509AF8',
            backgroundColor: 'rgba(80, 154, 248, 0.2)',
            borderWidth: 2,
            fill: true,
            pointRadius: 3,
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: { grid: { color: '#333' }, ticks: { color: '#ffffff' } },
            y: { beginAtZero: true, grid: { color: '#333' }, ticks: { color: '#ffffff' } }
        },
        plugins: { legend: { display: false } }
    }
});

document.getElementById("scaleSelector").addEventListener("change", function() {
    selectedMetric = this.value;
    // Mise à jour de l'affichage de l'échelle sélectionnée
    let scaleText = "Échelle : ";
    switch (selectedMetric) {
        case "logs_per_second":
            scaleText += "Par seconde";
            break;
        case "logs_per_minute":
            scaleText += "Par minute";
            break;
        case "log_average_per_hour":
            scaleText += "Par heure";
            break;
        case "log_average_per_day":
            scaleText += "Par jour";
            break;
        case "log_average_per_week":
            scaleText += "Par semaine";
            break;
        case "log_average_per_month":
            scaleText += "Par mois";
            break;
    }
    document.getElementById("currentScale").textContent = scaleText;

    updateChart();
});

function updateStats() {
    fetch('/stats-data')
        .then(response => response.json())
        .then(data => {
            document.getElementById("totalLogs").textContent = data.total_logs || 0;
            let latestLogsPerMinute = data.logs_per_minute.length > 0 ? data.logs_per_minute[data.logs_per_minute.length - 1][0] : 0;
            document.getElementById("logsPerMinute").textContent = latestLogsPerMinute || 0;
        })
        .catch(error => console.error('Error fetching stats:', error));
}


function updateChart() {
    fetch('/stats-data')
        .then(response => response.json())
        .then(data => {
            logChartData.length = 0;
            timeLabels.length = 0;
            if (data[selectedMetric]) {
                data[selectedMetric].forEach(entry => {
                    let value = entry[0] || 0; // Si la valeur est absente, on met 0
                    let timestamp = entry[1];
                    // Formatage du timestamp en fonction de l'échelle sélectionnée
                    // Pour les échelles inférieures aux minutes, on affiche HH:MM:SS
                    // Pour les échelles inférieures ou égal aux heures on utilise le format HH:MM
                    // Pour les échelles supérieures aux heures, on utilise le format JJ/MM/AAAA
                    let formattedTime = selectedMetric === "logs_per_second" ? new Date(timestamp).toLocaleTimeString() :
                        selectedMetric === "logs_per_minute" ? new Date(timestamp).toLocaleTimeString().slice(0, 5) :
                            selectedMetric === "log_average_per_hour" ? new Date(timestamp).toLocaleTimeString().slice(0, 5) :
                                new Date(timestamp).toLocaleDateString();


                    logChartData.push(value);
                    timeLabels.push(formattedTime);
                });
            }

            logChart.update();
        })
        .catch(error => console.error('Error updating chart:', error));
}

// Rafraîchissement automatique du graphique toutes les secondes
setInterval(updateStats, 1000);
setInterval(updateChart, 10000);
document.addEventListener("DOMContentLoaded", () => {
    updateStats();
    updateChart();
});

// Gestion du bandeau d'information
document.addEventListener("DOMContentLoaded", function () {
    const infoBanner = document.getElementById("infoBanner");
    const closeBanner = document.getElementById("closeBanner");

    setTimeout(() => { infoBanner.classList.add("slideout");}, 10000);

    closeBanner.addEventListener("click", () => {infoBanner.classList.add("slideout");});
});



// Gestion de l'état des services
function updateHealthCheck() {
    fetch('/health-check') // Endpoint Flask qui renvoie l'état des services
        .then(response => response.json())
        .then(data => {
            const healthContainer = document.getElementById("healthStatus");
            healthContainer.innerHTML = "";
            data.forEach(service => {
                const serviceElement = document.createElement("div");
                serviceElement.classList.add("health-item");

                const statusIndicator = document.createElement("div");
                statusIndicator.classList.add("status-indicator");
                statusIndicator.classList.add(service.status === "UP" ? "status-up" : "status-down");

                //create uptimeFormatted if uptime is under 60 seconds print in seconds but if uptime is under 60 minutes print in minutes else print in hours
                const uptimeFormatted = service.uptime > 0 ? service.uptime < 60 ? `${service.uptime} sec` : service.uptime < 3600 ? `${Math.floor(service.uptime / 60)} min` : `${Math.floor(service.uptime / 3600)} h` : "N/A";

                const portDisplay = service.port ? `:${service.port}` : "";
                const portLink = service.host ? `<a href="http://${service.link}/" target="_blank">${portDisplay}</a>` : portDisplay;

                serviceElement.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 10px;">
                        ${statusIndicator.outerHTML}
                        <span class="health-name">${service.name}</span>
                    </div>
                    <span class="health-port">${portLink}</span>
                    <span class="health-uptime">Uptime: ${uptimeFormatted}</span>
                `;
                healthContainer.appendChild(serviceElement);
            });
        })
        .catch(error => console.error('Erreur lors du chargement du health check:', error));
}

setInterval(updateHealthCheck, 1000); // Rafraîchir toutes les secondes
document.addEventListener("DOMContentLoaded", updateHealthCheck);