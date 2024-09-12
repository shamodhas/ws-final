from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from model.user import User

class UserService:

    @staticmethod
    def create_user(email: str, password: str, db: Session):
        user = User(email=email, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(email: str, password: str, db: Session):
        try:
            user = db.query(User).filter(User.email == email, User.password == password).one()
            return user
        except NoResultFound:
            return None
