from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_service_provider = db.Column(db.String(255), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_description = db.Column(db.Text, nullable=False)
    product_image_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.String(255))

    @classmethod
    def search_by_name(cls, query):
        return cls.query.filter(or_(cls.product_name.like(f'%{query}%'))).all()
