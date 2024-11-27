function sendAction(action) {
    fetch('/timer?action=' + action, { method: 'POST' })
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

    fetch(`/timer?action=reset&minutes=${minutes}&seconds=${seconds}`, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            document.getElementById('timer').textContent = data.time;
        });
}

function modifyTime(operation, value) {
    fetch(`/timer?action=${operation}${value}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('timer').textContent = data.time;
        });
}

setInterval(() => {
    fetch('/timer')
        .then(response => response.json())
        .then(data => {
            document.getElementById('timer').textContent = data.time;
        });
}, 100);