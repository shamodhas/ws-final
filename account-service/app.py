from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.account import Account
from service.account_service import AccountService

app = Flask(__name__)

# Configure the database
DATABASE_URL = 'postgresql://user:password@localhost/account_db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/account', methods=['POST'])
def create_account():
    data = request.json
    try:
        db = SessionLocal()
        account = AccountService.create_account(balance_usd=data['balance_usd'], balance_btc=data['balance_btc'], db=db)
        return jsonify({"account_id": account.id, "balance_usd": account.balance_usd, "balance_btc": account.balance_btc}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@app.route('/account/<int:account_id>', methods=['GET'])
def get_account(account_id: int):
    try:
        db = SessionLocal()
        account = AccountService.get_account(account_id=account_id, db=db)
        if account:
            return jsonify({"account_id": account.id, "balance_usd": account.balance_usd, "balance_btc": account.balance_btc})
        else:
            return jsonify({"error": "Account not found"}), 404
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
