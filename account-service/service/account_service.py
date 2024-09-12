from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from model.account import Account

class AccountService:

    @staticmethod
    def create_account(balance_usd: float, balance_btc: float, db: Session):
        account = Account(balance_usd=balance_usd, balance_btc=balance_btc)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_account(account_id: int, db: Session):
        try:
            account = db.query(Account).filter(Account.id == account_id).one()
            return account
        except NoResultFound:
            return None
