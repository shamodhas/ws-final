from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Trade, Base
from service import TradeService

app = Flask(__name__)
DATABASE_URL = "mssql+pyodbc://username:password@server.database.windows.net/dbname?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@app.route('/trade', methods=['POST'])
def create_trade():
    db = SessionLocal()
    data = request.json
    trade = TradeService.create_trade(
        buy_account_id=data.get('buy_account_id'),
        sell_account_id=data.get('sell_account_id'),
        usd_amount=data.get('usd_amount'),
        btc_amount=data.get('btc_amount'),
        currency=data.get('currency'),
        trade_type=data.get('trade_type'),
        db=db
    )
    db.close()
    return jsonify(trade), 201

@app.route('/trade/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    db = SessionLocal()
    trade = TradeService.get_trade(trade_id, db)
    db.close()
    if trade:
        return jsonify(trade), 200
    return jsonify({"error": "Trade not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
