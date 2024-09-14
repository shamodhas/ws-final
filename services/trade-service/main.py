from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample data stored in an array
trades = [
    {"trade_id": "1", "asset": "BTC", "amount": "0.5", "price": "50000"},
    {"trade_id": "2", "asset": "ETH", "amount": "10", "price": "2000"}
]

@app.route("/trade", methods=["GET"])
def get_trades():
    return jsonify(trades)

@app.route("/trade/<trade_id>", methods=["GET"])
def get_trade(trade_id):
    trade = next((trd for trd in trades if trd["trade_id"] == trade_id), None)
    if trade:
        return jsonify(trade)
    return jsonify({"error": "Trade not found"}), 404

@app.route("/trade", methods=["POST"])
def create_trade():
    if not request.json or 'trade_id' not in request.json or 'asset' not in request.json or 'amount' not in request.json or 'price' not in request.json:
        abort(400)
    new_trade = {
        "trade_id": request.json['trade_id'],
        "asset": request.json['asset'],
        "amount": request.json['amount'],
        "price": request.json['price']
    }
    trades.append(new_trade)
    return jsonify(new_trade), 201

@app.route("/trade/<trade_id>", methods=["PUT"])
def update_trade(trade_id):
    trade = next((trd for trd in trades if trd["trade_id"] == trade_id), None)
    if not trade:
        return jsonify({"error": "Trade not found"}), 404
    if not request.json or 'amount' not in request.json or 'price' not in request.json:
        abort(400)
    trade['amount'] = request.json['amount']
    trade['price'] = request.json['price']
    return jsonify(trade)

@app.route("/trade/<trade_id>", methods=["DELETE"])
def delete_trade(trade_id):
    global trades
    trades = [trd for trd in trades if trd["trade_id"] != trade_id]
    return jsonify({"result": "Trade deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
