"""Model for Shops Logs Table"""
from datetime import datetime
from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class ShopsLogs(db.Model):
    """
    ShopsLogs Model.
    """

    __tablename__ = "shop_logs"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    shop_id = db.Column(db.String(60), db.ForeignKey("shop.id"), nullable=False)

    user_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)

    action = db.Column(db.String(20), nullable=False)

    log_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    def __init__(self, shop_id, user_id, action):
        self.shop_id = shop_id

        self.user_id = user_id

        self.action = action

    def __repr__(self):
        return f"{format(self.log_date)}: User({self.user_id}) {self.action} on Shop({self.shop_id})"

    def insert(self):
        """Insert the current object into the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update the current object in the database"""
        db.session.commit()

    def delete(self):
        """Delete the current object from the database"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return f"{format(self.log_date)}: User({self.user_id}) {self.action} on Shop({self.shop_id})"
