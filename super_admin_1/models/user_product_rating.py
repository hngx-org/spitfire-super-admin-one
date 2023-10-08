#!/usr/bin/env python3
"""Template for the user_product_rating Class"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class User_Product_Rating(BaseModel):
    """User_Product_Rating class"""
    __tablename__ = "user_product_rating"
    user_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.String(60), db.ForeignKey("product.id"), nullable=False)
    rating = db.Column(db.Numeric(5, 2), nullable=False, default=0)


    def __init__(self, user_id, product_id, rating):
        """Object constructor"""
        super().__init__()
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating

    def __repr__(self):
        """official object representation"""
        return f"(\
            user_id: {self.user_id},\
            product_id: {self.product_id},\
            rating: {self.rating}\
        )"
    
    def format(self):
        """Format the object's attributes as a dictionary"""
        return ({
            "user_id": self.user_id,
            "product_id": self.product_id,
            "rating": self.rating
        })