#!/usr/bin/env python3
"""
Base template for the Event driven application
"""
from super_admin_1 import db
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


def get_uuid():
    """Generate a unique id using uuid4()"""
    return uuid4().hex


# Create a base model class that will contain common functionality
class BaseModel(db.Model):
    """BaseClass for all models"""

    # Make this class abstract so it won't be mapped to a database table
    __abstract__ = True

    # Define a primary key column with a default value of a generated UUID
    # id = db.Column(db.uuid(60), primary_key=True, default=get_uuid(), nullable=False)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=get_uuid(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    
    
    def __init__(self):
      self.id = get_uuid()
      self.created_at = datetime.utcnow()
      self.updated_at = datetime.utcnow()

    def insert(self):
        """Insert the current object into the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update the current object in the database"""
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        """Delete the current object from the database"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """Format the object's attributes as a dictionary"""
        # This method should be overridden in subclasses
        raise NotImplementedError(
            "Subclasses must implement the 'format' method"
        )
