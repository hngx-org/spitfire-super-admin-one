#!/usr/bin/env python3
"""Template for the Product_category Class"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class Product_category(BaseModel):
    """Product category class"""
    __tablename__ = "product_category"
    name = db.Column(db.String(225), nullable=False)
    status = db.Column(db.Enum("pending", "complete", "failed", name="CategoryStatus"), server_default="pending", nullable=False)

    def __init__(self, name, parent_category=None, status="pending"):
        """Object constructor"""
        super().__init__()
        self.name = name
        self.parent_category = self.id
        self.status = status or "pending"
    
    def __repr__(self):
        """official object representation"""
        return f"(id: {self.id}, parent_category: {self.parent_category}, status: {self.status})"
    
    def format(self):
        """Format the object's attributes as a dictionary"""
        return ({
            "id": self.id,
            "parent_category": self.parent_category,
            "status": self.status
        })