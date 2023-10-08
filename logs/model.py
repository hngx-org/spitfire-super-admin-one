"""The model for the product_logs table"""
from super_admin_1 import db


class ProductLogs(db.Model):
    """create the product_logs table"""
    __tablename__ = 'product_logs'
    user_id = db.Column(db.String(60), db.ForeignKey('user.id'),
                        nullable=False, primary_key=True)
    action = db.Column(db.String(20), nullable=False)
    product_id = db.Column(db.String(60), db.ForeignKey('product.id'),
                           nullable=False, primary_key=True)
    log_date = db.Column(db.DateTime(), nullable=False)

    def __init__(self, user_id, action, product_id):
        """Instantiate a model"""
        self.user_id = user_id
        self.action = action
        self.product_id = product_id

    def insert(self):
        """Insert the current object into the database"""
        db.session.add(self)
        db.session.commit()
