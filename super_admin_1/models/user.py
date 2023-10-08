#!/usr/bin/env python3
"""Template for the Shop Class"""
from super_admin_1 import db
from super_admin_1.models.base import BaseModel
from flask import Blueprint
user = Blueprint(
    "user", __name__, url_prefix="/api/user"
)

class User(BaseModel):

    """User class"""

    __tablename__ = "user"
    updated_at = None
    username = db.Column(db.String(32), nullable=False, unique=True)
    first_name = db.Column(db.String(332), nullable=False)
    last_name = db.Column(db.String(332), nullable=False)
    email = db.Column(db.String(332), nullable=False)
    section_order = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    two_factor_auth = db.Column(db.Boolean, nullable=False, default=False)
    provider = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)

    shop = db.relationship(
        "Shop", backref=db.backref("user", lazy=True), cascade="all, delete"
    )

    def __init__(
        self,
        username,
        first_name,
        last_name,
        email,
        section_order,
        password,
        is_verified,
        two_factor_auth,
        provider,
        profile_pic,
        refresh_token,
    ):
        """
        Initializes a new instance of the class.

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
        """
        super().__init__()
        self.updated_at = None
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.section_order = section_order
        self.password = password
        self.is_verified = is_verified
        self.two_factor_auth = two_factor_auth
        self.provider = provider
        self.profile_pic = profile_pic
        self.refresh_token = refresh_token

    def __repr__(self):
        """official object representation"""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "section_order": self.section_order,
            "password": self.password,
            "is_verified": self.is_verified,
            "two_factor_auth": self.two_factor_auth,
            "provider": self.provider,
            "profile_pic": self.profile_pic,
            "refresh_token": self.refresh_token,
        }

    def format(self):
        """Format the object's attributes as a dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "section_order": self.section_order,
            "password": self.password,
            "is_verified": self.is_verified,
            "two_factor_auth": self.two_factor_auth,
            "provider": self.provider,
            "profile_pic": self.profile_pic,
            "refresh_token": self.refresh_token,
            "created_at": self.created_at,
            # "updated_at": self.updated_at
        }
