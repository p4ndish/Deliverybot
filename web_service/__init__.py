# import os
# from flask import Flask
# from database.productsModel import Product, db


# app = Flask(__name__, static_url_path='/static')
# app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'images')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../delivery.db'
# db.init_app(app)

# # Import the routes

# from routes import delivery_guy_routes
