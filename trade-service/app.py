from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.trade import Trade
from service.trade_service import TradeService

app = Flask(__name__)

# Configure the database
DATABASE_URL = 'postgresql://user:password@localhost/trade_db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/trade', methods=['POST'])
def create_trade():
    data = request.json
    try:
        db = SessionLocal()
        trade = TradeService.create_trade(
            buy_account_id=data['buy_account_id'],
            sell_account_id=data['sell_account_id'],
            usd_amount=data['usd_amount'],
            btc_amount=data['btc_amount'],
            currency=data['currency'],
            trade_type=data['trade_type'],
            db=db
        )
        return jsonify({"trade_id": trade.id, "usd_amount": trade.usd_amount, "btc_amount": trade.btc_amount}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@app.route('/trade/<int:trade_id>', methods=['GET'])
def get_trade(trade_id: int):
    try:
        db = SessionLocal()
        trade = TradeService.get_trade(trade_id=trade_id, db=db)
        if trade:
            return jsonify({"trade_id": trade.id, "usd_amount": trade.usd_amount, "btc_amount": trade.btc_amount})
        else:
            return jsonify({"error": "Trade not found"}), 404
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
