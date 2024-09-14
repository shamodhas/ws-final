from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Account, Base
from service import AccountService

app = Flask(__name__)
DATABASE_URL = "mssql+pyodbc://username:password@server.database.windows.net/dbname?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@app.route('/account', methods=['POST'])
def create_account():
    db = SessionLocal()
    balance_usd = request.json.get('balance_usd')
    balance_btc = request.json.get('balance_btc')
    account = AccountService.create_account(balance_usd, balance_btc, db)
    db.close()
    return jsonify(account), 201

@app.route('/account/<int:account_id>', methods=['GET'])
def get_account(account_id):
    db = SessionLocal()
    account = AccountService.get_account(account_id, db)
    db.close()
    if account:
        return jsonify(account), 200
    return jsonify({"error": "Account not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
