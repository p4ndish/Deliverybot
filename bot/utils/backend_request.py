import json
from dotenv import load_dotenv
load_dotenv()
import os 
import requests 

url = os.environ.get('APP_URL')
JSON_HEADER ={'Content-Type': 'application/json'} 
async def get_products_by_providers(provider, page, per_page):
    response = requests.get(url + '/products/' + provider,
                       params={'page': page, 'per_page': per_page}
    )
    print("inside backend: ", response)

    if response.status_code == 200:
        return response.json().get('products', [])
    else:
        return []

async def get_product(product_id):
    response = requests.get(url + f"/product/{product_id}" )
    return response.json()
    
async def query_product(q):
    response = requests.get(url + "/search?query=" + q)
    if response.status_code == 200:
        return response.json()
    else:
        return {}
    



# delivery guy profile

async def get_delivery_profile(userid):
    endpoint = f"/delivery/profile/{userid}"
    
    try:
        response = requests.get(url  + endpoint)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return {"error": "Failed to make the request."}
    


async def register_delivery_profile(user_data):
    
    try:
        print("Registering delivery profile : ", user_data)
        response = requests.post(url + '/delivery/register', json=user_data)
        response.raise_for_status()  
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
async def delete_delivery_profile(userid):
    endpoint = f"/delivery/delete/{userid}"
    
    try:
        response = requests.delete(url + endpoint)
        response.raise_for_status()  
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None 
 

# async def wrap_delivery_requests_get(data, 
async def is_user_working(userid):
    endpoint = f"/delivery/working/{userid}"
    
    try:
        response = requests.get(url + endpoint)
        response.raise_for_status()  
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error on user_working:", e)
        return None
async def is_user_offline(userid):
    endpoint = f"/delivery/offline/{userid}"
    
    try:
        response = requests.get(url + endpoint)
        print('response from go offline', response.text)
        response.raise_for_status()  
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error on user_working:", e)
        return None

        
async def update_user_onoff_status(userid, data):
    endpoint = f"/delivery/update/visibility/{userid}"
    
    try:
        response = requests.post(url + endpoint, json=data)

        response.raise_for_status()  
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error on user_working:", e)
        return None

async def update_user_working_status(userid, data):
    endpoint = f"/delivery/update/working/{userid}"
    
    try:
        response = requests.post(url + endpoint, json=data)

        response.raise_for_status()  
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error on user_working:", e)
        return None

        
async def get_delivery_user_status(userid):
    endpoint = f"/delivery/get_status/{userid}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on user_working:", e)
        return None
    


# cart requests 
async def get_cart_items(user_id):
    endpoint = f"/user/cart/show/{user_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        print('what the result :', result)
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on user_working:", e)
        return None

        
async def add_to_cart(user_id, product_id, quantity):
    endpoint = f"/user/cart/add"
    
    try:
        data = {'user_id': user_id, 'product_id': product_id, 'quantity': quantity}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url + endpoint, data=json.dumps(data), headers=headers)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on adding to cart:", e)
        return None
    
async def delete_from_user_cart(user_id, product_id):
    endpoint = f"/user/cart/delete_products"
    
    try:
        data = {'user_id': user_id, 'product_id': product_id,}
        response = requests.post(url + endpoint, data=data)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on adding to cart:", e)
        return None
    
async def delete_user_cart(user_id):
    endpoint = f"/user/cart/empty_cart/{user_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on adding to cart:", e)
        return None
    
    
async def user_exists(user_id):
    endpoint = f"/user/exists/{user_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        print('response from user exists: ', result)
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on adding to cart:", e)
        return None
    

async def delivery_exists(user_id):
    endpoint = f"/delivery/exists/{user_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        print('response from user exists: ', result)
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on adding to cart:", e)
        return None
    





# order requests 
    
async def create_order(data):
    endpoint = f"/user/order/create_order"
    
    try:
        response = requests.post(url + endpoint, data=json.dumps(data), headers=JSON_HEADER)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except Exception as e:
        print("Error on adding to cart:", e)
        return None
    

# check if uuid exists 
async def check_if_not_exist(uuid):
    endpoint = f"/check_uuid/{uuid}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on checking uuid:", e)
        return None
    


# find_delivery_guy

async def find_delivery_guy():
    endpoint = f"/user/find_delivery"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        print("printing finding_delivery:", result)
        return result
    except Exception  as e:
        print("Error on adding to cart:", e)
        return None
    

async def move_user_cart_to_order_details(user_id, order_uuid):
    endpoint = f"/user/move_cart/{user_id}/{order_uuid}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except Exception as e:
        print("Error on moving from cart to order_list :", e)
        return None
    


async def fetch_who_accepts(order_id):
    endpoint = f"/order/check_accept/{order_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        print("whooooo", result)
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on moving from cart to order_list :", e)
        return None

        
async def accept_order(delivery_user_id, order_id):
    endpoint = f"/delivery/order/accept/{delivery_user_id}/{order_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on accepting order :", e)
        return None
        
async def get_products_from_order_details(order_id):
    endpoint = f"/order/get_products/{order_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on accepting order :", e)
        return None
        
async def add_delivery_person_to_orders(user_id, order_id):
    endpoint = f"/order/add_delivery_to_order/{user_id}/{order_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on accepting order :", e)
        return None
    

async def get_customer_profile_details(order_id):
    endpoint = f"/order/customer_detail/{order_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except requests.exceptions.RequestException as e:
        print("Error on accepting order :", e)
        return None


async def move_product_to_orders_detail(product_id, quantity, order_id):
    endpoint = f"/order/move_product/{product_id}/{quantity}/{order_id}"
    
    try:
        response = requests.get(url + endpoint)

        response.raise_for_status()  
        
        result = response.json()
        # result = result[0]
        return result
    except Exception as e:
        print("Error on accepting order :", e)
        return None
