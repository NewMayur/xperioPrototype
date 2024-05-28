from flask import Flask, request, jsonify, render_template
from pydantic import ValidationError

from models import Device

app = Flask(__name__)

# In-memory 'database' for demonstration
devices = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/devices', methods=['POST'])
def add_device():
    # Learning Comment:
    # Flask routes handle HTTP requests. Here, we're defining a route to add a new device.
    device_data = request.json
    try:
        device = Device(**device_data)
        devices.append(device.dict())
        return jsonify(device.dict()), 201
    except ValidationError as e:
        return e.json(), 400

@app.route('/devices', methods=['GET'])
def list_devices():
    return jsonify(devices)

@app.route('/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    update_data = request.json
    for device in devices:
        if device['id'] == device_id:
            device.update(**Device(**update_data).dict())
            return jsonify(device)
    return {"message": "Device not found"}, 404


@app.route('/devices/control', methods=['POST'])
def control_device():
    data = request.json
    device_id = data.get('id')
    new_status = data.get('status')

    # Here, you would add logic to control the actual device based on device_id and new_status
    # For this example, we'll just print the action and return a success message
    print(f"Setting device {device_id} to {new_status}")
    return jsonify({"message": f"Device {device_id} set to {new_status}"}), 200

if __name__ == '__main__':
    app.run(debug=True)

# Learning Comment:
# Flask's `run` method starts the local development server.
# The `debug=True` argument enables debug mode for easier development and testing.
