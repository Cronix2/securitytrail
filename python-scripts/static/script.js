// Sample log data
const logs = [];

// DOM Elements
const logContainer = document.getElementById('logContainer');
const scrollBottomBtn = document.getElementById('scrollBottom');
const clearLogsBtn = document.getElementById('clearLogs');

// Function to create a log entry element
function createLogEntry(log) {
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    
    const user = document.createElement('span');
    user.className = 'log-user';
    user.textContent = log.user;
    
    const time = document.createElement('span');
    time.className = 'log-time';
    time.textContent = log.time;
    
    const message = document.createElement('span');
    message.textContent = `${log.timestamp} ${log.message}`;
    
    logEntry.appendChild(user);
    logEntry.appendChild(time);
    logEntry.appendChild(message);
    
    return logEntry;
}

// Function to render logs
function renderLogs() {
    logContainer.innerHTML = '';
    logs.forEach(log => {
        logContainer.appendChild(createLogEntry(log));
    });
}

// Function to scroll to bottom
function scrollToBottom() {
    window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: 'smooth'
    });
}

// Function to clear logs
function clearLogs() {
    logs.length = 0;
    renderLogs();
}

// Event listeners
scrollBottomBtn.addEventListener('click', scrollToBottom);
clearLogsBtn.addEventListener('click', clearLogs);

// Initial render
renderLogs();