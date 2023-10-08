"""Model for Shops Logs Table"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class ShopsLogs(BaseModel):
    """
    ShopsLogs Model.
    """

    __tablename__ = "shops_logs"

    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"),nullable=False)
    shop_name = db.Column(db.String(60), db.ForeignKey("shop.name"),nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    admin_name= db.Column(db.String(32),db.ForeignKey("user.username"),nullable=False)
    action = db.Column(db.String(20),nullable=False)

    def __init__(self, shop_id, shop_name, admin_id, admin_name, action):
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.action = action

    def __repr__(self):
        return f"{format(self.created_at)}: Admin({self.admin_id}:{self.admin_name}) {self.action} on Shop({self.shop_id}:{self.shop_name})"

    def format(self):
        return f"{format(self.created_at)}: Admin({self.admin_id}:{self.admin_name}) {self.action} on Shop({self.shop_id}:{self.shop_name})"


