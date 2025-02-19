document.addEventListener("DOMContentLoaded", function() {
    var socket = io();
    var logContainer = document.getElementById("logContainer");

    socket.on('log', function(msg) {
        var logEntry = document.createElement("div");
        logEntry.className = 'log-entry';
        var timestamp = new Date().toISOString().replace('T', '/').split('.')[0];
        logEntry.innerHTML = `<span class='log-user'>root</span><span class='log-separator'>@</span><span class='log-time'>${timestamp}</span> <span class='log-msg'>${msg}</span>`;
        logContainer.appendChild(logEntry);
        scrollToBottom();
    });
});

function scrollToBottom() {
    var logContainer = document.getElementById("logContainer");
    logContainer.scrollTop = logContainer.scrollHeight;
}

function clearLogs() {
    document.getElementById("logContainer").innerHTML = "";
}

document.getElementById("scrollBottom").addEventListener("click", scrollToBottom);
document.getElementById("clearLogs").addEventListener("click", clearLogs);