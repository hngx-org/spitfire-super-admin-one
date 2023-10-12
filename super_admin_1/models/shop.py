#!/usr/bin/env python3
"""Template for the Shop Class"""
from super_admin_1 import db
from super_admin_1.models.base import BaseModel
from datetime import datetime

class Shop(BaseModel):
  """Shop class"""
  __tablename__ = "shop"
  merchant_id = db.Column(db.String(60), db.ForeignKey("user.id"), nullable=False)
  name = db.Column(db.String(255))
  policy_confirmation = db.Column(db.Boolean)
  restricted = db.Column(db.Enum('no', 'temporary', 'permanent', name="restricted"), server_default="no")
  admin_status = db.Column(db.Enum('pending', 'reviewed', 'approved', 'suspended', 'blacklisted', name="ADMIN_STATUS"), server_default="pending", nullable=False)
  is_deleted = db.Column(db.Enum("active", "temporary", name="shop_status"), server_default="active")
  reviewed = db.Column(db.Boolean)
  rating = db.Column(db.Numeric(10, 2))
  
  
  def __init__(self, merchant_id, name, policy_confirmation, restricted, admin_status, is_deleted, reviewed, rating):
    """object constructor"""
    super().__init__()
    self.merchant_id = merchant_id
    self.name = name
    self.policy_confirmation = policy_confirmation
    self.restricted = restricted or "no"
    self.admin_status = admin_status or "pending"
    self.is_deleted = is_deleted or "active"
    self.reviewed = reviewed 
    self.rating = rating


  def __repr__(self):
    """official object representation"""
    return f"<Shop(id={self.id}, merchant_id={self.merchant_id}, name={self.name}, admin_status={self.admin_status}, is_deleted={self.is_deleted}, policy_confirmation={self.policy_confirmation}, restricted={self.restricted}, reviewed={self.reviewed}, rating={self.rating})>"


  def format(self):
    """Format the object's attributes as a dictionary"""
    return ({
      "id": self.id,
      "merchant_id": self.merchant_id,
      "name": self.name,
      "policy_confirmation": self.policy_confirmation,
      "restricted": self.restricted,
      "admin_status": self.admin_status,
      "is_deleted": self.is_deleted,
      "reviewed": self.reviewed,
      "rating": self.rating,
      "createdAt": self.createdAt,
      "updatedAt": self.updatedAt,
    })
