from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User, Base
from service import UserService

app = Flask(__name__)
DATABASE_URL = "mssql+pyodbc://username:password@server.database.windows.net/dbname?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@app.route('/user', methods=['POST'])
def create_user():
    db = SessionLocal()
    user_name = request.json.get('user_name')
    user = UserService.create_user(user_name, db)
    db.close()
    return jsonify(user), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = SessionLocal()
    user = UserService.get_user(user_id, db)
    db.close()
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
