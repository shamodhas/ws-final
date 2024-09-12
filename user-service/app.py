from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.user import User
from service.user_service import UserService

app = Flask(__name__)

# Configure the database
DATABASE_URL = 'postgresql://user:password@localhost/user_db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        db = SessionLocal()
        user = UserService.create_user(email=data['email'], password=data['password'], db=db)
        return jsonify({"user_id": user.id, "email": user.email}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    try:
        db = SessionLocal()
        user = UserService.authenticate_user(email=data['email'], password=data['password'], db=db)
        if user:
            return jsonify({"user_id": user.id, "email": user.email})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    finally:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
