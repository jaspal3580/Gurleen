from flask import Flask, jsonify
import json, os, uuid

app = Flask(__name__)

# Load & Save JSON
def load_data():
    return json.load(open('devices.json')) if os.path.exists('devices.json') else {}

def save_data(data):
    with open('devices.json', 'w') as f:
        json.dump(data, f)

devices = load_data()

# Auto Token Registration
@app.route('/register/<device_id>', methods=['GET'])
def auto_register(device_id):
    token = f"TOKEN_{uuid.uuid4().hex[:8].upper()}"
    devices[token] = {"device_name": device_id}
    save_data(devices)
    return jsonify({"device": device_id, "token": token})

# Manual Token Registration
@app.route('/register/<device_id>/<token>', methods=['GET'])
def manual_register(device_id, token):
    if token in devices:
        return jsonify({"error": "Token already exists!"}), 400
    devices[token] = {"device_name": device_id}
    save_data(devices)
    return jsonify({"device": device_id, "token": token})

# Update Virtual Pin
@app.route('/update/<token>/<pin>/<value>', methods=['GET'])
def update_virtual_pin(token, pin, value):
    if token not in devices:
        return jsonify({"error": "Invalid token"}), 403
    devices[token][pin.upper()] = value
    save_data(devices)
    return jsonify({pin.upper(): value})

# Read Virtual Pin
@app.route('/read/<token>/<pin>', methods=['GET'])
def read_virtual_pin(token, pin):
    if token in devices and pin.upper() in devices[token]:
        return jsonify({pin.upper(): devices[token][pin.upper()]})
    return jsonify({"error": "Pin or token not found"}), 404

# Get All Data of a Token
@app.route('/status/<token>', methods=['GET'])
def get_status(token):
    return jsonify(devices.get(token, {"error": "Invalid token"}))

# All Devices
@app.route('/all', methods=['GET'])
def get_all():
    return jsonify(devices)

if __name__ == "__main__":
    app.run(debug=True)