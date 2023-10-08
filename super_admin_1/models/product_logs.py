#!/usr/bin/env python3
"""Template for the product Logs"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel
from datetime import datetime

class Product_Logs(BaseModel):
    """Product_Image class"""
    __tablename__ = "product_logs"
    user_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    product_id = db.Column(db.String(60), db.ForeignKey("product.id"), nullable=False)
    log_date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    
    def __init__(self,user_id, action, product_id, log_date=None):
        """Object constructor"""
        super().__init__()
        self.user_id = user_id
        self.action = action
        self.product_id = product_id
        if log_date is None:
            log_date = datetime.utcnow()
        self.log_date = log_date

    def __repr__(self):
        """official object representation"""
        return f"(user_id: {self.user_id}, action: {self.action}, product_id: {self.product_id}, log_date: {self.log_date})"
    
    def format(self):
        """Format the object's attributes as a dictionary"""
        return ({
            "user_id": self.user_id,
            "action": self.action,
            "product_id": self.product_id,
            "log_date": self.log_date
        })