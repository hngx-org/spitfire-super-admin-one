#!/usr/bin/env python3
"""Template for the Product_SubCategory Class"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel



class Product_Sub_Category(BaseModel):
    """Product category class"""
    __tablename__ = "product_sub_category"
    updatedAt = None
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), nullable=False)
    parent_category_id = db.Column(db.Integer, db.ForeignKey( "product_category.id", ondelete="CASCADE"), nullable=False)
    
    
    def __init__(self, name):
      """Object constructor"""
      super().__init__()
      self.updatedAt = None
      self.name = name
    
    def __repr__(self):
        """official object representation"""
        return f"(id: {self.id}, name: {self.name})"
    
    def format(self):
        """Format the object's attributes as a dictionary"""
        return ({
            "id": self.id,
            "name": self.name,
        })
    