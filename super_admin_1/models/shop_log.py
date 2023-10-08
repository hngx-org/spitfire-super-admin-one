#!/usr/bin/env python3
"""Template for the product Logs"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class Shop_Logs(BaseModel):
    """Shop_Log class"""
    __tablename__ = "product_logs"
    user_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
    shop_id = db.Column(db.String(60), db.ForeignKey("shop.id"), nullable=False)
    log_date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    
    def __init__(self, shop_id, url):
        """Object constructor"""
        super().__init__()
        self.shop_id = shop_id
        self.url = url

    def __repr__(self):
        """official object representation"""
        return f"(shop_id: {self.shop_id}, url: {self.url})"
    
    def format(self):
        """Format the object's attributes as a dictionary"""
        return ({
            "shop_id": self.shop_id,
            "url": self.url
        })￼Enter
