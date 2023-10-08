from super_admin_1 import db
from datetime import datetime


class ShopLog(db.Model):
    """Shop log class"""

    __tablename__ = "shop_logs"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey(
        "user.id"), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    shop_id = db.Column(db.String(60), db.ForeignKey(
        "shop.id"), nullable=False)
    log_date = db.Column(
        db.DateTime(), default=datetime.utcnow, nullable=False)

    def __init__(self, user_id, action, shop_id):
        self.user_id = user_id
        self.action = action
        self.shop_id = shop_id
        self.log_date = datetime.utcnow()

    def __repr__(self):
        return "user_id: {}, action: {}, shop_id: {}, log_date: {}".format(self.user_id, self.action, self.shop_id, self.log_date)

    def insert(self):
        """Insert the current object into the database"""
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "user_id": self.user_id,
            "action": self.action,
            "shop_id": self.shop_id,
            "log_date": self.log_date
        }
