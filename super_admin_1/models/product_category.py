#!/usr/bin/env python3
"""Template for the Product_category Class"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class Product_category(BaseModel):
    """Product category class"""
    __tablename__ = "product_category"
    updatedAt = None
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(60), db.ForeignKey( "product.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey( "user.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(225), nullable=False)

    def __init__(self, name):
        """Object constructor"""
        super().__init__()
        self.name = name
    
    def __repr__(self):
        """official object representation"""
        return f"(id: {self.id}, name: {self.name})"
    
    def format(self):
        """Format the object's attributes as a dictionary"""
        return ({
            "id": self.id,
            "name": self.name
        })