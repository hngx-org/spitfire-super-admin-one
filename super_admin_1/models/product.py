#!/usr/bin/env python3
"""Template for the User Class"""

from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class Product(BaseModel):
  """ Product class"""
  __tablename__ = "product"  

  name = db.Column(db.String(255), nullable=False)
  description = db.Column(db.String(255), nullable=False)
  quantity = db.Column(db.BigInteger, nullable=False)
  price = db.Column(db.Numeric(10, 2), nullable=False)
  discount_price = db.Column(db.Numeric(10, 2), nullable=False)
  tax = db.Column(db.Numeric(10, 2), nullable=False)
  admin_status = db.Column(db.Enum('pending', 'reviewed', 'approved', 'blacklisted', 'suspended', name="ADMIN_STATUS"), server_default="pending", nullable=False)
  is_deleted = db.Column(db.Enum("active", "temporary", name="product_status"), server_default="active", nullable=False)
  is_published = db.Column(db.Boolean, nullable=False, default=False)
  currency = db.Column(db.String(16), nullable=False)
  shop_id = db.Column(db.String(60), db.ForeignKey("shop.id"), nullable=False) 
  rating_id = db.Column(db.Integer, db.ForeignKey("user_product_rating.id"), nullable=False)
  image_id = db.Column(db.Integer, db.ForeignKey("user_product_rating.id"), nullable=False)
  category_id = db.Column(db.String(60), db.ForeignKey("product_category.id"), nullable=False)  

  def __init__(self, shop_id, rating_id, category_id, name, description, image_id, quantity, price, discount_price, tax, admin_status, is_deleted, currency, is_published=False):
    """ object constructor"""
    super().__init__()
    self.shop_id = shop_id
    self.rating_id = rating_id
    self.category_id = category_id
    self.name = name
    self.description = description
    self.image_id = image_id
    self.quantity = quantity
    self.price = price
    self.discount_price = discount_price
    self.tax = tax
    self.admin_status = admin_status or "pending"
    self.is_published = is_published
    self.is_deleted = is_deleted or "active"
    self.currency = currency
    
    
  def __repr__(self):
    """ official object representation"""
    return ({
      "id": self.id,
      "shop_id": self.shop_id,
      "rating_id": self.rating_id,
      "category_id": self.category_id,
      "name": self.name,
      "description": self.description,
      "quantity": self.quantity,
      "price": self.price,
      "discount_price": self.discount_price,
      "tax": self.tax,
      "admin_status": self.admin_status,
      "is_published": self.is_published,
      "is_deleted": self.is_deleted,
      "currency": self.currency,
      "createdAt": self.createdAt,
      "updatedAt": self.updatedAt
    })
    
  def format(self):
    """Format the object's attributes as a dictionary"""
    return ({
      "id": self.id,
      "shop_id": self.shop_id,
      "rating_id": self.rating_id,
      "image_id": self.image_id,
      "category_id": self.category_id,
      "name": self.name,
      "description": self.description,
      "quantity": self.quantity,
      "price": self.price,
      "discount_price": self.discount_price,
      "tax": self.tax,
      "admin_status": self.admin_status,
      "is_deleted": self.is_deleted,
      "is_published": self.is_published,
      "currency": self.currency,
      "createdAt": self.createdAt,
      "updatedAt": self.updatedAt,
    })
