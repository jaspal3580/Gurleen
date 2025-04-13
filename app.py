from flask import Flask, request, jsonify

app = Flask(__name__)
device_commands = {}

@app.route('/')
def home():
    return "Gurleen IoT Server is Running"

@app.route('/control', methods=['POST'])
def control_device():
    data = request.json
    device_id = data.get("device_id")
    command = data.get("command")
    
    if device_id and command:
        device_commands[device_id] = command
        return jsonify({"status": "success", "message": f"{command} sent to {device_id}"})
    return jsonify({"status": "error", "message": "Missing device_id or command"}), 400

@app.route('/get_command/<device_id>', methods=['GET'])
def get_command(device_id):
    command = device_commands.get(device_id, "NO_COMMAND")
    return jsonify({"command": command})