
from flask import Flask, request, jsonify

app = Flask(__name__)

device_commands = {}

@app.route('/')
def home():
    return "Gurleen IoT Server Running!"

@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    device_id = data.get('device_id')
    command = data.get('command')

    if device_id and command:
        device_commands[device_id] = command.upper()
        return jsonify({'status': 'success', 'message': f'{command.upper()} sent to {device_id}'})
    else:
        return jsonify({'status': 'error', 'message': 'Missing device_id or command'}), 400

@app.route('/control/<device_id>/<command>', methods=['GET'])
def control_clean(device_id, command):
    if command.upper() not in ["ON", "OFF"]:
        return jsonify({'status': 'error', 'message': 'Command must be ON or OFF'}), 400

    device_commands[device_id] = command.upper()
    return jsonify({'status': 'success', 'message': f'{command.upper()} sent to {device_id}'})

@app.route('/get_command/<device_id>', methods=['GET'])
def get_command(device_id):
    command = device_commands.get(device_id, "OFF")
    return jsonify({'device_id': device_id, 'command': command})

if __name__ == '__main__':
    app.run(debug=True)
