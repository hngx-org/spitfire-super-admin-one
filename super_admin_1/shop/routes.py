from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from super_admin_1 import db
from super_admin_1.models.shop import Shop

