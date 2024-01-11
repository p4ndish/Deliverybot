from flask import Flask, jsonify, render_template, request, redirect, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_paginate import Pagination, get_page_args
from database.functions import * 
from database.productsModel import Product, db

#routes register 
from routes.delivery_guy_routes import delivery 
from routes.cart_routes import cart 
# from . import app



app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'images'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../delivery.db'
db.init_app(app)
app.register_blueprint(blueprint=delivery)
app.register_blueprint(blueprint=cart)

@app.route('/')
def index():
    return render_template('index.html',)

@app.route("/images/<path:imgPath>")
def handle_image_request(imgPath):
    return send_from_directory(app.config['UPLOAD_FOLDER'], imgPath)


@app.route('/products/<product_provider>', methods=['GET'])
def all_products( product_provider):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    # Retrieve products for the specified provider
    products = get_products_by_provider(product_provider)

    # Calculate the total number of items
    total = len(products)

    # Paginate the products using the current page and items per page
    start = (page - 1) * per_page
    end = start + per_page
    current_products = products[start:end]

    # Convert the range object to a list
    pages_list = list(range(1, int(total / per_page) + 2))  # Calculate the total number of pages

    # Prepare JSON response
    response_data = {
        'products': current_products,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages_list,
        }
    }

    return jsonify(response_data)


@app.route("/product/<product_id>")
def view_product( product_id):
    result = get_product(product_id)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Product not found"})
    

@app.route('/search')
def search_products():
    search_query = request.args.get('query')

    if search_query:
        results = Product.search_by_name(search_query)
        #print(results)
        results_dict = [{'product_name': result.product_name,
                     'product_price': result.product_price,
                     'product_description': result.product_description,
                     'product_image_url': result.product_image_url} for result in results]
    
        return jsonify(results_dict)
        # return render_template('search_results.html', results=search_results, query=search_query)
    else:
        return {"error": "Product not found"}, 404

# @app.route('/add_product', methods=['POST'])
# def add_product():
#     if request.method == 'POST':
#         # Get product details from the form
#         name = request.form['name']
#         price = float(request.form['price'])

#         # Get the current date and time in ISO format
#         created_at = datetime.now().isoformat()

#         # Insert the product into the database
#         cur.execute('INSERT INTO products (name, price, created_at) VALUES (?, ?, ?)', (name, price, created_at))
#         db.commit()

#         return redirect(url_for('index'))

    

@app.route("/user/find_delivery")
def find_delivery_route():
    try:
        stat = find_delivery_person()
        return jsonify(stat), 200
    except Exception as e:
        return {}, 500
        
    
@app.route("/check_uuid/<uuid>")
def check_uuid_route(uuid):
    try:
        stat = check_if_uuid_exists(uuid)
        print(stat)
        return jsonify(stat), 200
    except Exception as e:
        return {}, 500
        
    
@app.route("/user/move_cart/<user_id>/<order_uuid>")
def move_cart_to_details(user_id, order_uuid):
    try:
        result = move_user_cart_to_order_list(user_id, order_uuid)
        print("result from moving:", result)
        return result, 200
    except:
        return {}, 500




@app.route("/user/order/create_order", methods=["POST"])
def create_order_route():
    try:
        data = request.get_json()
        print("data from creating order", data)
        order_uid = data['order_id']
        customer_id =str(data['customer_id'])
        print("whats they type:", type(customer_id) )
        result = create_order(order_uid, customer_id)
        return result, 200
    except Exception as e:
        print("error creating order", e)
        return {}, 500
    
    
    
    
@app.route("/order/check_accept/<order_id>")
def check_accept_delivery(order_id):
    try:
        result = fetch_who_accepted_order_details(order_id)
        return jsonify(result), 200
    except Exception as e:
        print("error checking delivery", e)
        return {}, 500
    
    
@app.route("/delivery/order/accept/<delivery_user_id>/<order_id>")
def accpet_order_route(delivery_user_id, order_id):
    try:
        result = accept_order(delivery_user_id, order_id)
        return result, 200
    except Exception as e:
        print("error on internal accept order", e)
        return {}, 500
    
    
@app.route("/order/get_products/<order_id>")
def get_products_from_orderlist(order_id):
    try:
        result = get_products_from_order_detail(order_id)
        return jsonify(result), 200
    except Exception as e:
        print("error internal ", e)
        return {}, 500
    
    
@app.route("/order/add_delivery_to_order/<user_id>/<order_id>")
def add_delivery_to_orders_route(user_id, order_id):
    try:
        result = add_delivery_to_orders(user_id, order_id)
        return jsonify(result), 200
    except Exception as e:
        print("error internal ", e)
        return {}, 500
    
@app.route("/order/customer_detail/<order_id>")
def get_customer_detail_route(order_id):
    try:
        result = get_customer_detail(order_id)
        return jsonify(result), 200
    except Exception as e:
        print("error internal ", e)
        return {}, 500
    




@app.route("/order/move_product/<product_id>/<quantity>/<order_id>")
def add_product_to_order_detail_route(product_id, order_id, quantity):
    try:
        result = move_product_to_order_details(product_id, order_id, quantity)
        return jsonify(result), 200
    except Exception as e:
        print("error internal ", e)
        return {}, 500
    



@app.route("/user/exists/<user_id>")
def check_user_exists(user_id):
    try:
        result = does_user_exists(user_id)
        return result, 200
    except Exception as e:
        print("error internal ", e)
        return {}, 500
    

@app.route("/aboutus")
def aboutus_page():
    return render_template("about_us.html")


@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")






if __name__ == '__main__':
    app.run(debug=True)
