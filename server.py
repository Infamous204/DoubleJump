import os
import json
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Path to store users
USERS_FILE = 'users.json'

# Load users from file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save users to file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Hash password with SHA256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password_hash = data.get('password')  # Already hashed from client

    if not username or not password_hash:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    users = load_users()
    if username in users:
        return jsonify({"success": False, "message": "Username already exists"}), 409

    # Store the hashed password
    users[username] = password_hash
    save_users(users)

    return jsonify({"success": True, "message": "Account created"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password_hash = data.get('password')  # Already hashed from client

    if not username or not password_hash:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    users = load_users()
    if username not in users or users[username] != password_hash:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    return jsonify({"success": True, "message": "Login successful"}), 200

if __name__ == '__main__':
    # Run on all interfaces (0.0.0.0) so client can connect from network
    # Use port 5000 as in the client code
    app.run(host='0.0.0.0', port=5000, debug=True)