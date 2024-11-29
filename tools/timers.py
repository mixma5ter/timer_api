import threading
import time

from flask import request

timer_lock = threading.RLock()
timer_thread = None

timers = {
    1: {
        'minutes': 0,
        'seconds': 0,
        'initial_time': 0,
        'is_running': False,
        'start_time': None,
        'is_reversed': False,
        "thread": None
    },
    2: {
        'minutes': 0,
        'seconds': 0,
        'initial_time': 0,
        'is_running': False,
        'start_time': None,
        'is_reversed': False,
        "thread": None
    }
}


def update_timer(timer_id):
    with timer_lock:
        timer = timers.get(timer_id)
        if timer and timer['is_running']:
            elapsed_time = time.time() - timer['start_time']
            current_time_seconds = timer['initial_time']

            if timer['is_reversed']:
                current_time_seconds -= elapsed_time
            else:
                current_time_seconds += elapsed_time

            timer['minutes'] = max(0, int(current_time_seconds // 60))
            timer['seconds'] = max(0, int(current_time_seconds % 60))

            if timer['is_reversed'] and current_time_seconds <= 0:
                timer['minutes'] = 0
                timer['seconds'] = 0
                timer['is_running'] = False
                timer['start_time'] = None
                timer['initial_time'] = 0


def start_timer(timer_id):
    global timers

    with timer_lock:
        timer = timers.get(timer_id)
        if not timer:
            return
        if not timer['is_running']:
            if timer['start_time'] is not None:
                elapsed_time = time.time() - timer['start_time']
                current_seconds = timer['initial_time']
                if timer['is_reversed']:
                    current_seconds += elapsed_time
                else:
                    current_seconds -= elapsed_time
                timer['initial_time'] = max(0, current_seconds)
            else:
                timer['initial_time'] = timer['minutes'] * 60 + timer['seconds']

            timer['start_time'] = time.time()
            timer['is_running'] = True

            if timer["thread"] is None or not timer["thread"].is_alive():
                timer["thread"] = threading.Thread(target=update_timer_loop, args=(timer_id,))
                timer["thread"].daemon = True
                timer["thread"].start()


def update_timer_loop(timer_id):
    while True:
        with timer_lock:
            timer = timers.get(timer_id)
            if not timer or not timer['is_running']:
                break
        update_timer(timer_id)
        time.sleep(0.1)


def formatted_time(timer_id):
    with timer_lock:
        timer = timers.get(timer_id)
        if not timer:
            return {'error': 'Timer not found'}

        if request.method == 'POST':
            data = request.get_json()
            action = data.get('action')

            if action == 'reset':
                minutes = int(data.get('minutes', 0))
                seconds = int(data.get('seconds', 0))
                timer.update({
                    'minutes': minutes,
                    'seconds': seconds,
                    'initial_time': minutes * 60 + seconds,
                    'is_running': False,
                    'start_time': None,
                    'is_reversed': False
                })
            elif action == 'start':
                if not timer['is_running']:
                    timer['is_reversed'] = False
                    start_timer(timer_id)
            elif action == 'reverse':
                if not timer['is_running']:
                    timer['is_reversed'] = True
                    start_timer(timer_id)
            elif action == 'pause':
                timer['is_running'] = False
                timer['start_time'] = None

            elif action in ('add', 'subtract'):
                if not timer['is_running']:
                    value = int(data.get('value', 0))
                    current_seconds = timer['minutes'] * 60 + timer['seconds']

                    if action == 'add':
                        new_seconds = max(0, current_seconds + value)
                    elif action == 'subtract':
                        new_seconds = max(0, current_seconds - value)
                    timer['minutes'] = int(new_seconds // 60)
                    timer['seconds'] = int(new_seconds % 60)
                    timer['initial_time'] = new_seconds

        formatted_time = "{:02d}:{:02d}".format(timer['minutes'], timer['seconds'])
        return {'time': formatted_time}
