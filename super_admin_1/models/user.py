#!/usr/bin/env python3
"""Template for the Shop Class"""
from super_admin_1 import db
from super_admin_1.models.base import BaseModel
from datetime import datetime


class User(BaseModel):
  """User class"""
  __tablename__ = "user"
  updatedAt = None
  username = db.Column(db.String(255), nullable=False)
  first_name = db.Column(db.String(255), nullable=False)
  last_name = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  role_id = db.Column(db.Integer)
  section_order = db.Column(db.Text)
  password = db.Column(db.String(255))
  provider = db.Column(db.String(255))
  phone_number = db.Column(db.String(255))
  is_verified = db.Column(db.Boolean, default=False)
  two_factor_auth = db.Column(db.Boolean, default=False)
  location = db.Column(db.String(255))
  country = db.Column(db.String(255))
  profile_pic = db.Column(db.Text)
  profile_cover_photo = db.Column(db.Text)
  refresh_token = db.Column(db.String(255), nullable=False)
  
  shop = db.relationship("Shop", backref=db.backref("user", lazy=True), cascade="all, delete")
  
  def __init__(self, username, first_name, last_name, email, phone_number, role_id, section_order, password, provider, profile_pic, profile_cover_photo, refresh_token, location, country, is_verified=False, two_factor_auth=False):
    """Initializes a new instance of the class.

    Args:
        username (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.
        section_order (list): The section order of the user.
        password (str): The password of the user.
        provider (str): The provider of the user.
        profile_pic (str): The profile picture of the user.
        refresh_token (str): The refresh token of the user.
        location (str): The location of the user.
        country (str): The country of the user.
        is_verified (bool): The is_verified of the user.
        two_factor_auth (bool): The two_factor_auth of the user.
    """
    super().__init__()
    self.updated_at = None
    self.username = username
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.refresh_token = refresh_token
    self.role_id = role_id
    self.section_order = section_order
    self.password = password
    self.provider = provider
    self.phone_number = phone_number
    self.is_verified = is_verified
    self.two_factor_auth = two_factor_auth
    self.location = location
    self.country = country
    self.profile_pic = profile_pic 
    self.profile_cover_photo = profile_cover_photo
    
  def __repr__(self):
    """ official object representation"""
    return (
        f"<User(id={self.id}, username={self.username}, first_name={self.first_name}, "
        f"last_name={self.last_name}, email={self.email}, "
        f"refresh_token={self.refresh_token}, role_id={self.role_id}, "
        f"section_order={self.section_order}, password={self.password}, "
        f"provider={self.provider}, phone_number={self.phone_number}, "
        f"is_verified={self.is_verified}, two_factor_auth={self.two_factor_auth}, "
        f"location={self.location}, country={self.country}, "
        f"profile_pic={self.profile_pic}"
    )
    
  def format(self):
    """ Format the object's attributes as a dictionary"""
    return ({
        "id": self.id,
        "username": self.username,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email,
        "role_id": self.role_id,
        "section_order": self.section_order,
        "password": self.password,
        "provider": self.provider,
        "phone_number": self.phone_number,
        "is_verified": self.is_verified,
        "two_factor_auth": self.two_factor_auth,
        "location": self.location,
        "country": self.country,
        "profile_pic": self.profile_pic,
        "profile_cover_photo": self.profile_cover_photo,
        "refresh_token": self.refresh_token,
        "createdAt": self.createdAt
    })