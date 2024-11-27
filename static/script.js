let timerInterval;
let startTime;
let isRunning = false;
let isReverse = false;
let elapsedTime = 0;

const clockDisplay = document.getElementById('clock');
const minutesInput = document.getElementById('minutesBox');
const secondsInput = document.getElementById('secondsBox');
const resetButton = document.getElementById('resetButton');
const startButton = document.getElementById('startButton');
const pauseButton = document.getElementById('pauseButton');
const reverseCheckbox = document.getElementById('reverseCheckbox');
const add30sButton = document.getElementById('add30sButton');
const subtract30sButton = document.getElementById('subtract30sButton');
const add1mButton = document.getElementById('add1mButton');
const subtract1mButton = document.getElementById('subtract1mButton');
const add5mButton = document.getElementById('add5mButton');
const subtract5mButton = document.getElementById('subtract5mButton');


function updateTimerDisplay() {
    let currentTime = 0

    if (isReverse && startTime) {
        currentTime = startTime - Date.now()
    } else {
        currentTime = elapsedTime;
    }

    const minutes = Math.floor(currentTime / 60000);
    const seconds = Math.floor((currentTime % 60000) / 1000);
    const displayMinutes = isReverse ? Math.max(0, minutes) : minutes; // не показывать отрицательные значения
    const displaySeconds = isReverse ? Math.max(0, seconds) : seconds;

    clockDisplay.textContent = `${String(displayMinutes).padStart(2, '0')}:${String(displaySeconds).padStart(2, '0')}`;
}

function startTimer() {
    if (!isRunning) {
        isReverse = reverseCheckbox.checked;

        if (isReverse) {
            if (!startTime) { //Если startTime не задан - задаем его.
                startTime = Date.now() + elapsedTime;
            }
        } else {
            if (!startTime) { //Если startTime не задан - задаем его.
                startTime = Date.now() - elapsedTime;
            }
        }

        timerInterval = setInterval(updateTimer, 10);
        isRunning = true;

        if (startButton) {
            startButton.classList.add('blinking');
        }
    }
}

function pauseTimer() {
    if (isRunning) {
        clearInterval(timerInterval);
        isRunning = false;
        elapsedTime = Math.abs(Date.now() - startTime); // Сохраняем прошедшее время
        startTime = null;
        if (startButton) {
            startButton.classList.remove('blinking');
        }
    }
}

function resetTimer() {
    clearInterval(timerInterval);
    isRunning = false;
    startTime = null;
    if (startButton) {
        startButton.classList.remove('blinking');
    }
    const minutes = parseInt(minutesInput.value) || 0;
    const seconds = parseInt(secondsInput.value) || 0;
    elapsedTime = (minutes * 60 + seconds) * 1000;
    isReverse = reverseCheckbox.checked;

    updateTimerDisplay();
}

function updateTimer() {
    if (isReverse) {
        elapsedTime = startTime - Date.now();
        if (elapsedTime <= 0) {
            pauseTimer()
            elapsedTime = 0;
            updateTimerDisplay();
            return;
        }
    } else {
        elapsedTime = Date.now() - startTime;
    }
    updateTimerDisplay();
}

function addTime(seconds) {
    elapsedTime += seconds * 1000;
    updateTimerDisplay();
}

function subtractTime(seconds) {
    elapsedTime -= seconds * 1000;
    if (elapsedTime < 0) {
        elapsedTime = 0;
    }
    updateTimerDisplay();
}

resetButton.addEventListener('click', resetTimer);
startButton.addEventListener('click', startTimer);
pauseButton.addEventListener('click', pauseTimer);

add30sButton.addEventListener('click', () => addTime(30));
subtract30sButton.addEventListener('click', () => subtractTime(30));
add1mButton.addEventListener('click', () => addTime(60));
subtract1mButton.addEventListener('click', () => subtractTime(60));
add5mButton.addEventListener('click', () => addTime(300));
subtract5mButton.addEventListener('click', () => subtractTime(300));

// Инициализация таймера при загрузке страницы
resetTimer();