from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample data stored in an array
accounts = [
    {"account_id": "12345", "balance": "5000"},
    {"account_id": "67890", "balance": "15000"}
]

@app.route("/account", methods=["GET"])
def get_accounts():
    return jsonify(accounts)

@app.route("/account/<account_id>", methods=["GET"])
def get_account(account_id):
    account = next((acc for acc in accounts if acc["account_id"] == account_id), None)
    if account:
        return jsonify(account)
    return jsonify({"error": "Account not found"}), 404

@app.route("/account", methods=["POST"])
def create_account():
    if not request.json or 'account_id' not in request.json or 'balance' not in request.json:
        abort(400)
    new_account = {
        "account_id": request.json['account_id'],
        "balance": request.json['balance']
    }
    accounts.append(new_account)
    return jsonify(new_account), 201

@app.route("/account/<account_id>", methods=["PUT"])
def update_account(account_id):
    account = next((acc for acc in accounts if acc["account_id"] == account_id), None)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    if not request.json or 'balance' not in request.json:
        abort(400)
    account['balance'] = request.json['balance']
    return jsonify(account)

@app.route("/account/<account_id>", methods=["DELETE"])
def delete_account(account_id):
    global accounts
    accounts = [acc for acc in accounts if acc["account_id"] != account_id]
    return jsonify({"result": "Account deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
