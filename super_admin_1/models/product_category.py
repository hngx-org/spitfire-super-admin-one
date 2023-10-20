#!/usr/bin/env python3
"""Template for the Product_category Class"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel
from super_admin_1.models.product_sub_category import Product_Sub_Category  # Import Product_Sub_Category here


class Product_category(BaseModel):
    """Product category class"""
    __tablename__ = "product_category"
    updatedAt = None
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(60), db.ForeignKey( "user.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(225), nullable=False)
    # create a backref to Product
    products = db.relationship("Product", backref="product_category", cascade="all, delete")
    product_sub_categories = db.relationship("Product_Sub_Category", backref="product_category", cascade="all, delete")
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