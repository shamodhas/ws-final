from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample data stored in an array
users = [
    {"user_id": "1", "name": "Alice", "email": "alice@example.com"},
    {"user_id": "2", "name": "Bob", "email": "bob@example.com"}
]

@app.route("/user", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = next((usr for usr in users if usr["user_id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/user", methods=["POST"])
def create_user():
    if not request.json or 'user_id' not in request.json or 'name' not in request.json or 'email' not in request.json:
        abort(400)
    new_user = {
        "user_id": request.json['user_id'],
        "name": request.json['name'],
        "email": request.json['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/user/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((usr for usr in users if usr["user_id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        abort(400)
    user['name'] = request.json['name']
    user['email'] = request.json['email']
    return jsonify(user)

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [usr for usr in users if usr["user_id"] != user_id]
    return jsonify({"result": "User deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
