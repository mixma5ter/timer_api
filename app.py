import threading
import time

from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='static')

timer_state = {
    'minutes': 0,
    'seconds': 0,
    'initial_time': 0,
    'is_running': False,
    'start_time': None,
    'is_reversed': False
}

timer_lock = threading.RLock()
timer_thread = None


def update_timer():
    with timer_lock:
        if timer_state['is_running']:
            elapsed_time = time.time() - timer_state['start_time']
            current_time_seconds = timer_state['initial_time']

            if timer_state['is_reversed']:
                current_time_seconds -= elapsed_time
            else:
                current_time_seconds += elapsed_time

            timer_state['minutes'] = max(0, int(current_time_seconds // 60))
            timer_state['seconds'] = max(0, int(current_time_seconds % 60))

            if timer_state['is_reversed'] and current_time_seconds <= 0:
                timer_state['minutes'] = 0
                timer_state['seconds'] = 0
                timer_state['is_running'] = False
                timer_state['start_time'] = None
                timer_state['initial_time'] = 0


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/timer', methods=['GET'])
def timer():
    return render_template('timer/timer.html')


@app.route('/timer_api_help')
def my_api_doc():
    return render_template('timer/timer_api_help.html')


@app.route('/timer/api', methods=['GET', 'POST'])
def timer_api():
    global timer_state
    with timer_lock:
        if request.method == 'POST':
            action = request.args.get('action')

            if action == 'reset':
                minutes = int(request.args.get('minutes', 0))
                seconds = int(request.args.get('seconds', 0))
                timer_state.update({
                    'minutes': minutes,
                    'seconds': seconds,
                    'initial_time': minutes * 60 + seconds,
                    'is_running': False,
                    'start_time': None,
                    'is_reversed': False
                })

            elif action == 'start':
                if not timer_state['is_running']:
                    timer_state['is_reversed'] = False
                    start_timer()

            elif action == 'reverse':
                if not timer_state['is_running']:
                    timer_state['is_reversed'] = True
                    start_timer()

            elif action == 'pause':
                timer_state['is_running'] = False
                timer_state['start_time'] = None

            elif action.startswith(('add', 'subtract')):
                if not timer_state['is_running']:
                    value = int(action[3:]) if action.startswith('add') else -int(action[8:])
                    current_seconds = timer_state['minutes'] * 60 + timer_state['seconds']
                    new_seconds = max(0, current_seconds + value)
                    timer_state['minutes'] = int(new_seconds // 60)
                    timer_state['seconds'] = int(new_seconds % 60)
                    timer_state['initial_time'] = new_seconds

        formatted_time = "{:02d}:{:02d}".format(timer_state['minutes'], timer_state['seconds'])
        return jsonify({'time': formatted_time})


def start_timer():
    global timer_thread

    if not timer_state['is_running']:
        if timer_state['start_time'] is not None:
            elapsed_time = time.time() - timer_state['start_time']
            current_seconds = timer_state['initial_time']

            if timer_state['is_reversed']:
                current_seconds += elapsed_time
            else:
                current_seconds -= elapsed_time
            timer_state['initial_time'] = max(0, current_seconds)

        else:
            timer_state['initial_time'] = timer_state['minutes'] * 60 + timer_state['seconds']

        timer_state['start_time'] = time.time()
        timer_state['is_running'] = True

        if timer_thread is None or not timer_thread.is_alive():
            timer_thread = threading.Thread(target=update_timer_loop)
            timer_thread.daemon = True
            timer_thread.start()


def update_timer_loop():
    while True:
        with timer_lock:
            if not timer_state['is_running']:
                break
        update_timer()
        time.sleep(0.1)


if __name__ == '__main__':
    app.run(debug=True)
