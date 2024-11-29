function sendAction(timerId, action) {
    fetch(`/timer${timerId}/api`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: action }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById(`timer-${timerId}`).textContent = data.time;
        });
}

function resetWithValues(timerId) {
    const minutes = parseInt(document.getElementById(`minutes-${timerId}`).value, 10) || 0;
    const seconds = parseInt(document.getElementById(`seconds-${timerId}`).value, 10) || 0;
    fetch(`/timer${timerId}/api`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'reset', minutes: minutes, seconds: seconds }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById(`timer-${timerId}`).textContent = data.time;
        });
}

function modifyTime(timerId, operation, value) {
    fetch(`/timer${timerId}/api`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: operation, value: value }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById(`timer-${timerId}`).textContent = data.time;
        });
}

function updateTimer(timerId) {
    fetch(`/timer${timerId}/api`)
        .then(response => response.json())
        .then(data => {
            document.getElementById(`timer-${timerId}`).textContent = data.time;
        });
}

setInterval(() => updateTimer(timerId), 100);