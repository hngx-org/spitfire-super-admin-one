#!/usr/bin/env python3
"""Template for the Shop Class"""
from super_admin_1 import db
from super_admin_1.models.base import BaseModel


class Shop(BaseModel):
  """Shop class"""
  __tablename__ = "shop"

  merchant_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
  name = db.Column(db.String(60), nullable=False)
  policy_confimation = db.Column(db.Boolean, nullable=False)
  restricted = db.Column(db.Enum('no', 'temporary', 'permanent', name="Restricted"), server_default="no" , nullable=False)
  admin_status = db.Column(db.Enum('pending', 'review', 'approved', 'blacklist', name="AdminStatus"), server_default="pending", nullable=False,)
  is_deleted = db.Column(db.Enum("active", "temporary", name="shop_status"), server_default="active", nullable=False)
  reviewed = db.Column(db.Boolean, nullable=True, default=False)
  rating = db.Column(db.Numeric(10, 2), nullable=True, default=0)
 
  
  
  def __init__(self, merchand_id, product_id, name, policy_confimation, restricted, admin_status, is_deleted, reviewed, rating):
    """object constructor"""
    self.merchand_id = merchand_id
    self.product_id = product_id
    self.name = name
    self.policy_confimation = policy_confimation
    self.restricted = restricted or "no"
    self.admin_status = admin_status or "pending"
    self.is_deleted = is_deleted or "active"
    self.reviewed = reviewed 
    self.rating = rating
    
  def __repr__(self):
    """official object representation"""
    return ({
      "id": self.id,
      "merchand_id": self.merchand_id,
      "product_id": self.product_id,
      "name": self.name,
      "policy_confimation": self.policy_confimation,
      "restricted": self.restricted,
      "admin_status": self.admin_status,
      "is_deleted": self.is_deleted,
      "reviewed": self.reviewed,
      "rating": self.rating,
    })
    
  def format(self):
    """Format the object's attributes as a dictionary"""
    return ({
      "id": self.id,
      "merchand_id": self.merchand_id,
      "product_id": self.product_id,
      "name": self.name,
      "policy_confimation": self.policy_confimation,
      "restricted": self.restricted,
      "admin_status": self.admin_status,
      "is_deleted": self.is_deleted,
      "reviewed": self.reviewed,
      "rating": self.rating,
    })  
