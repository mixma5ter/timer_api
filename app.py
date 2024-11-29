from flask import Flask, render_template, jsonify

from tools.timers import formatted_time

app = Flask(__name__, static_folder='static')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/timer<int:timer_id>_api_help')
def timer_api_help(timer_id):
    return render_template('timer/timer_api_help.html', timer_id=timer_id)


@app.route('/timer<int:timer_id>', methods=['GET'])
def timer(timer_id):
    return render_template('timer/timer.html', timer_id=timer_id)


@app.route('/timer<int:timer_id>/api', methods=['GET', 'POST'])
def timer_api(timer_id):
    return jsonify(formatted_time(timer_id))


if __name__ == '__main__':
    app.run(debug=True)
