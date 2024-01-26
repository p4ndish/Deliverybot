from flask import Flask, jsonify, render_template, request, redirect, send_from_directory, url_for
from database.functions import delete_delivery_guy_profile, get_delivery_guy_profile, get_product, get_products_by_provider, register_delivery_guy_profile
from database.functions import * 
from database.productsModel import Product, db
from flask import Blueprint
delivery = Blueprint('delivery', __name__, static_folder='/static', template_folder='templates/deliveryPortal/')




# delivery guy routes 
@delivery.route('/u/profile/show/<user_id>', methods=['GET'])
def view_delivery_profile(user_id):
    user_data = get_profile(user_id)
    print(user_id, user_data)
    return render_template('deliveryPortal/view_profile.html', user_data=user_data)

@delivery.route('/delivery/profile_view/<user_id>', methods=['GET'])
def edit_delivery_profile(user_id):
    user_data = get_delivery_guy_profile(user_id)
    user_data = user_data[0]
    print("sssss",user_id, user_data)
    return render_template('deliveryPortal/view_profile.html', user_data=user_data)

@delivery.route('/delivery/profile_edit/<user_id>', methods=['GET'])
def view_customer_profile(user_id):
    # user_data = get_delivery_guy_profile(user_id)
    # print(user_id, user_data)
    user_data = get_delivery_guy_profile(user_id)
    user_data = user_data[0]
    return render_template('deliveryPortal/edit_profile.html',user_data=user_data)
@delivery.route('/u/profile/edit/<user_id>', methods=['GET'])
def edit_customer_profile(user_id):
    # user_data = get_delivery_guy_profile(user_id)
    # print(user_id, user_data)
    user_data = get_profile(user_id)
    print(user_data)
    # user_data = user_data[0]
    return render_template('deliveryPortal/edit_profile.html',user_data=user_data)

@delivery.route('/delivery/rate/<user_id>', methods=['GET'])
def rate_customer_profile(user_id):
    # user_data = get_delivery_guy_profile(user_id)
    # print(user_id, user_data)
    user_data = get_delivery_guy_profile(user_id)
    user_data = user_data[0]
    return render_template('deliveryPortal/rating.html',user_data=user_data)


@delivery.route('/submit_rating', methods=['POST'])
def submit_rate__profile():
    # user_data = get_delivery_guy_profile(user_id)
    # print(user_id, user_data)
    # user_data = get_delivery_guy_profile(user_id)
    # user_data = user_data[0]
    data =  request.form.get('rating')
    user_id =  request.form.get('user_id')
    print(data, user_id)
    return jsonify({'SUCCESS': True})



@delivery.route('/delivery/profile/<userid>', methods=['GET'])
def delivery_guy_profile(userid):
    try:
        # Call the function to get delivery guy profile
        profile_data = get_delivery_guy_profile(userid)
        
        if profile_data:
            return jsonify(profile_data)
        else:
            return jsonify({"error": "Failed to fetch delivery guy profile."}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error."}), 500



@delivery.route('/delivery/delete/<userid>', methods=['DELETE'])
def delete_delivery_guy_route(userid):
    try:
        # Call the function to delete delivery guy profile
        result = delete_delivery_guy_profile(userid)
        
        return jsonify(result)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error."}), 500
    
    

@delivery.route('/delivery/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print("got registration data", data)
        user_id = data['userId']
        print("registered userid", user_id)
        firstName = data['firstName']
        lastName = data['lastName']
        phoneNumber = data['phoneNumber']
        photoURL = data['photoImg']
        longtiude = data['longtiude']
        latitude = data['latitude']
        created_at = data['created_at']
        working = data['is_d_working']
        print(firstName, lastName, phoneNumber, photoURL, longtiude, latitude, created_at)

        if None in (user_id, firstName, lastName, phoneNumber, photoURL, longtiude, latitude, created_at):
            print("something is missing")
            return jsonify({'error': 'All fields are required'}), 400
        

        # Call the function to register the delivery guy profile
        status = register_delivery_guy_profile(user_id, firstName, lastName, phoneNumber, photoURL, longtiude, latitude, created_at, working)
        print("hit db status: ", status)

        if status:
            return jsonify({'success': 'Delivery guy registered successfully'}), 201
        else:
            return jsonify({'error': 'Failed to register delivery guy'}), 500

    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500


@delivery.route('/delivery/working/<userid>', methods=['GET'])
def function_is_user_Working(userid):
    try:
        result = is_user_working(userid)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to fetch user working status."}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error."}), 500
        
@delivery.route('/delivery/offline/<userid>', methods=['GET'])
def function_is_user_offline(userid):
    try:
        result = is_user_offline(userid)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to fetch user working status."}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error."}), 500

@delivery.route('/delivery/update/visibility/<userid>', methods=['POST'])
def function_update_user_onOff_status(userid):
    try:
        data = request.get_json()
        result = update_user_onoff_status(userid, data)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to update user working status."}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error."}), 500

        
@delivery.route('/update_user_working_status/<userid>', methods=['POST'])
def function_update_user_working_status(userid):
    try:
        data = request.get_json()
        result = update_user_working_status(userid, data)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to update user working status."}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error."}), 500

@delivery.route('/delivery/get_status/<userid>', methods=['GET'])
def function_get_delivery_user_status(userid):
    try:
        result = get_delivery_user_status(userid)
        print("results from status :", result)
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Failed to fetch delivery user status."}), 500
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error."}), 500
    

@delivery.route("/delivery/exists/<user_id>")
def check_user_exists(user_id):
    try:
        result = does_delivery_exists(user_id)
        return result, 200
    except Exception as e:
        print("error internal ", e)
        return {}, 500
    
