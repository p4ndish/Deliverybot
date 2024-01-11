from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    send_from_directory,
    url_for,
)
from database.functions import (
    delete_delivery_guy_profile,
    get_delivery_guy_profile,
    get_product,
    get_products_by_provider,
    register_delivery_guy_profile,
)
from database.functions import *
from database.productsModel import Product, db
from flask import Blueprint

cart = Blueprint(
    "cart", __name__, static_folder="/static", template_folder="/templates"
)


@cart.route("/user/cart/show/<user_id>")
def show_user_cart(user_id):
    try:
        stat = get_user_cart(user_id)
        return stat

    except Exception as e:
        print("got error in show_user_cart:", e)
        return {}

@cart.route("/user/cart/empty_cart/<user_id>")
def remove_user_cart_route(user_id):
    try:
        stat = remove_user_cart(user_id)
        return stat, 200

    except Exception as e:
        print("got error in show_user_cart:", e)
        return {}, 500

@cart.route('/user/cart/add', methods=['POST'])
def add_products_to_cart():
    try:
        data = request.get_json()
        product_id, user_id, quantity = data["product_id"], data["user_id"], data['quantity']
        stat = add_to_cart(user_id, product_id, quantity)
        if stat:
            return {'status': 'success', }
        
    except Exception as e:
        print("got error on add_products_to_cart", e)
        return {}

@cart.route("/user/cart/delete_products", methods=["POST"])
def delete_product_from_cart():
    try:
        data = request.get_json()
        product_id, user_id = data["product_id"], data["user_id"]
        stat = remove_user_cart(product_id, user_id)
        if not stat:
            print("got error on stat", stat)
            return None 
        else:
            print("got stat", stat)
            
            return stat
    except Exception as e:
        return None 
    