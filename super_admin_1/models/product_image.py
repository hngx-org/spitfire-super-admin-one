#!/usr/bin/env python3
"""Template for the product image Class"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class Product_Image(BaseModel):
    """Product_Image class"""
    __tablename__ = "product_image"
    product_id = db.Column(db.String(60), db.ForeignKey("product.id"), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def __init__(self, product_id, url):
        """Object constructor"""
        super().__init__()
        self.product_id = product_id
        self.url = url

    def __repr__(self):
        """official object representation"""
        return f"(product_id: {self.product_id}, url: {self.url})"
    
    def format(self):
        """Format the object's attributes as a dictionary"""
        return ({
            "product_id": self.product_id,
            "url": self.url
        })