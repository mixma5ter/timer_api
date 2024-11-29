function sendAction(action) {
    fetch('/timer/api?action=' + action, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('timer').textContent = data.time;
        });
}

function resetWithValues() {
    let minutes = document.getElementById('minutes').value;
    let seconds = document.getElementById('seconds').value;

    // Проверка на корректность ввода. Ограничиваем от 0 до 60
    minutes = Math.min(Math.max(0, minutes), 60);
    seconds = Math.min(Math.max(0, seconds), 60);

    fetch(`/timer/api?action=reset&minutes=${minutes}&seconds=${seconds}`, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            document.getElementById('timer').textContent = data.time;
        });
}

function modifyTime(operation, value) {
    fetch(`/timer/api?action=${operation}${value}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('timer').textContent = data.time;
        });
}

setInterval(() => {
    fetch('/timer/api')
        .then(response => response.json())
        .then(data => {
            document.getElementById('timer').textContent = data.time;
        });
}, 100);