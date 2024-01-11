# SQLite database initialization
from datetime import datetime
import random
import sqlite3
import os


def get_db():
    return sqlite3.connect("../delivery.db", check_same_thread=False)


# cur = db.cursor()
# cur.row_factory = sqlite3.Row


def start_db():
    # Create a products table
    db = get_db()
    cur = db.cursor()

    stat = cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_service_provider TEXT NOT NULL,
            product_service_provider_image TEXT NOT NULL,
            product_name TEXT NOT NULL,
            product_price REAL NOT NULL,
            product_description TEXT NOT NULL,
            product_image_url TEXT NOT NULL,
            product_rating_sum INTEGER DEFAULT 3 ,
            created_at TEXT
        )
    """
    )
    db.commit()
    print("from stat: ", stat)


start_db()


def orders_table():
    # Create a products table
    db = get_db()
    cur = db.cursor()

    stat = cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        user_id VARCHAR(255) NOT NULL,
        delivery_guy_id VARCHAR(255) NULL,
        delivery_guy_accepts BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TEXT
    )
    """
    )
    db.commit()
    print("from order table creation stat: ", stat)


orders_table()


# orders detail table creation
def orders_deatil_table():
    db = get_db()
    cur = db.cursor()
    stat = cur.execute(
        """
        CREATE TABLE IF NOT EXISTS order_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """
    )
    db.commit()
    print("stat from order deatail table", stat)


orders_deatil_table()


# cart Table
def create_cart_table():
    db = get_db()
    cur = db.cursor()
    stat = cur.execute(
        """
    CREATE TABLE IF NOT EXISTS cart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(255) NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """
    )
    db.commit()
    print("stat from cart table:", stat)


create_cart_table()


def delivery_guy_table():
    # Create a products table
    db = get_db()
    cur = db.cursor()

    stat = cur.execute(
        """
        CREATE TABLE IF NOT EXISTS delivery_person_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                phoneNumber VARCHAR(255) NOT NULL,
                chapa_account VARCHAR(255)  NULL,
                photoURL VARCHAR(255) NOT NULL,
                longtiude VARCHAR(255) NULL,
                latitude VARCHAR(255) NULL,
                pending_money BIGINT NULL DEFAULT 0,
                processed_amount BIGINT NULL DEFAULT 0,
                ratings_sum INTEGER NULL,
                working BOOLEAN NOT NULL,
                is_offline BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TEXT
            )
    """
    )
    db.commit()
    print("from stat: ", stat)


# orders_table()
delivery_guy_table()


def create_product(
    productName,
    productDescription,
    productPrice,
    createdAt,
    productImg,
    product_service_prodvider,
    product_service_prodvider_image,
):
    db = get_db()
    cur = db.cursor()
    try:
        status = cur.execute(
            """
            INSERT INTO products (product_name, product_price, product_description, product_image_url, created_at, product_service_provider, product_service_provider_image)
            VALUES (?, ?, ?, ?, ?, ?, ? )
            """,
            (
                productName,
                productPrice,
                productDescription,
                productImg,
                createdAt,
                product_service_prodvider,
                product_service_prodvider_image,
            ),
        )

        db.commit()
        print(status)
        return status
    except Exception as e:
        print("error: ", e)
        return {}


companies = os.listdir("images")
for company in companies:
    if company == "logo" or company == "users_image":
        continue
    com_items = os.listdir("images/" + company)
    for item in com_items:
        name = item.split(".")[0].split("burger-")[-1].title().replace("-", " ")
        product_img = company + "/" + item
        product_service_prodvider = company
        product_service_prodvider_image = "images/logo/logo_" + company + ".png"
        burger_descriptions = [
            "Classic beef burger with lettuce, tomatoes, and cheese.",
            "Spicy chicken burger with jalapeños and chipotle mayo.",
            "Vegetarian burger with a mix of grilled vegetables and hummus.",
            "Double cheeseburger with special sauce and pickles.",
            "Bacon and avocado burger for a savory and creamy delight.",
            "Mushroom Swiss burger with sautéed mushrooms and melted Swiss cheese.",
            "BBQ pulled pork burger topped with coleslaw.",
            "Teriyaki pineapple burger for a sweet and tangy twist.",
            "Gourmet truffle burger with truffle aioli and arugula.",
            "Buffalo chicken burger with blue cheese dressing.",
        ]

        burger_prices = [
            250.00,
            160.00,
            245.00,
            375.00,
            470.00,
            355.00,
            265.00,
            280.00,
            190.00,
            470.00,
        ]

        product_description = name.split("burger-")[-1].title() + random.choice(
            burger_descriptions
        )
        product_price = random.choice(burger_prices)
        created_at = datetime.now().isoformat()

        create_product(name, product_description, product_price, created_at, product_img, product_service_prodvider, product_service_prodvider_image)


def get_all_products():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM products ORDER BY created_at DESC")
    products = cur.fetchall()


def get_product(product_id):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    item = cur.execute(
        "SELECT * FROM products WHERE product_id = ?", (product_id,)
    ).fetchone()
    result = [dict(item)]
    return result


def search_product(keyword):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    item = cur.execute(
        "SELECT * FROM products WHERE product_id = ?", (keyword,)
    ).fetchone()
    result = [dict(item)]
    return result


def get_products_by_provider(provider):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        # Make sure to pass the parameter as a tuple (provider,)
        products = cur.execute(
            "SELECT * FROM products WHERE product_service_provider = ?", (provider,)
        ).fetchall()
        # print(dir(products),)
        # print("products: ", products.fetchall())
        result = [dict(row) for row in products]
        # print("fetching products", result)
        db.commit()
        # print(dir(products))
        return result
    except Exception as e:
        print("error on: ", e)
        return dict({"result": None})


# get_products_by_provider('kfc')


# delivery guy requests


def get_delivery_guy_profile(userid):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        # Make sure to pass the parameter as a tuple (provider,)
        userData = cur.execute(
            "SELECT * FROM delivery_person_accounts WHERE user_id = ?", (userid,)
        ).fetchone()
        # print(dir(products),)
        # print("products: ", products.fetchall())
        result = [dict(userData)]
        # print(result)
        db.commit()
        print("delivery guy profile results: ", result)
        return result
    except Exception as e:
        print("error on: ", e)
        return dict({"result": None})


def register_delivery_guy_profile(
    user_id,
    firstName,
    lastName,
    phoneNumber,
    photoURL,
    longtiude,
    latitude,
    created_at,
    working,
):
    db = get_db()
    cur = db.cursor()
    # cur.row_factory = sqlite3.Row
    try:
        status = cur.execute(
            """
            INSERT INTO delivery_person_accounts (user_id, firstName, lastName, phoneNumber, photoURL, longtiude, latitude, created_at, working)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                firstName,
                lastName,
                phoneNumber,
                photoURL,
                longtiude,
                latitude,
                created_at,
                working,
            ),
        )

        db.commit()
        print("printing delivery registration inside backend: ", status)
        print(dir(status))
        # for row in status:
        #     print(row)
        return status
    except Exception as e:
        print(e)

        return None


def delete_delivery_guy_profile(userid):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        cur.execute(
            """
            DELETE FROM delivery_person_accounts WHERE user_id = ?
            """,
            (userid,),
        )

        db.commit()
        print("user is deleted")
        return {"status": "deleted"}

    except Exception as e:
        print("got error deleting delivery guy profile: ", e)
        return [{}]  # empty json object


def is_user_working(userid):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        status = cur.execute(
            """
            SELECT working FROM delivery_person_accounts WHERE user_id = ?
            """,
            (userid,),
        ).fetchone()
        db.commit()
        print(dict(status))
        return [dict(status)]

    except Exception as e:
        return None


def is_user_offline(userid):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        status = cur.execute(
            """
            SELECT is_offline FROM delivery_person_accounts WHERE user_id = ?
            """,
            (userid,),
        ).fetchone()
        db.commit()
        print(dict(status))
        return [dict(status)]

    except Exception as e:
        return None


def update_user_onoff_status(userid, data):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    to_ = data["to_"]
    try:
        status = cur.execute(
            """
            UPDATE delivery_person_accounts SET is_offline = ?  WHERE user_id = ?
            """,
            (
                to_,
                userid,
            ),
        )
        db.commit()
        print("updated onoff status successfully")
        return [dict(status)]

    except Exception as e:
        print("error on updating user visibility status ", e)
        return None


def update_user_working_status(userid):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        status = cur.execute(
            """
            SELECT working FROM delivery_person_accounts WHERE user_id = ?
            """,
            (userid,),
        )
        db.commit()
        return [dict(status)]

    except Exception as e:
        return None


def get_delivery_user_status(userid):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        status = cur.execute(
            """
            SELECT firstName, is_offline, pending_money, working, ratings_sum, processed_amount FROM delivery_person_accounts WHERE user_id = ?
            """,
            (userid,),
        ).fetchone()
        db.commit()
        print("Success on fetching user status ", dict(status))
        return [dict(status)]

    except Exception as e:
        print("error on internal status fetch:", e)
        return None


## orders table operations
# def create_order()


# cart things
# carts operation


def add_to_cart(userid, productid, quantity):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        status = cur.execute(
            """
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (?, ?, ?)
            """,
            (userid, productid, quantity),
        )
        db.commit()
        print("Success on adding to cart ", dict(status))
        return [dict(status)]

    except Exception as e:
        print("error on internal status fetch:", e)
        return None


def remove_single_product_from_cart(productId):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        status = cur.execute(
            """
            DELETE FROM cart WHERE product_id = ?
            """,
            (productId,),
        )
        db.commit()
        print("Success on cleared from cart ", dict(status))
        return [dict(status)]

    except Exception as e:
        print("error on internal status fetch:", e)
        return None


def get_user_cart(user_id):
    try:
        db = get_db()
        cur = db.cursor()
        cur.row_factory = sqlite3.Row
        stat = cur.execute(
            """
        SELECT cart_id, product_id,quantity FROM cart WHERE user_id = ? 
    
        """,
            (user_id,),
        ).fetchall()

        result = [dict(row) for row in stat]
        print("success on fetching cart", result)
        return result

    except Exception as e:
        print("error on internal status fetch:", e)
        return {}


def remove_user_cart(user_id):
    try:
        db = get_db()
        cur = db.cursor()
        cur.row_factory = sqlite3.Row
        stat = cur.execute(
            """
        DELETE FROM cart WHERE user_id = ? 
    
        """,
            (
                
                user_id,
            ),
        )
        if stat:
            print("success on removing cart items ", user_id)
            return {'status': "success"}
        else:
            return {}
        # result = [dict(row) for row in stat.fetchall()]
        # print("success on fetching cart", result)
        # return result

    except Exception as e:
        print("error on internal status fetch:", e)
        return None


def empty_user_cart(user_id):
    try:
        db = get_db()
        cur = db.cursor()
        cur.row_factory = sqlite3.Row
        stat = cur.execute(
            """
        DELETE FROM cart WHERE user_id = ? 
    
        """,
            (user_id,),
        )
        result = [dict(row) for row in stat.fetchall()]
        print("success on fetching cart", result)
        return result

    except Exception as e:
        print("error on internal status fetch:", e)
        return None


# find delivery guy


def create_order(
    order_id,
    user_id,
):
    db = get_db()
    cur = db.cursor()
    try:
        created_at = str(datetime.now().isoformat())
        stat = cur.execute(
            """
            INSERT INTO orders (order_id, user_id, created_at) VALUES (?, ? , ?)
            """,
            (order_id, user_id, created_at,)
        )
        db.commit()
        print("success on create order", stat)
        return {"status": "created"}
    except Exception as e:
        print("error on create order", e)
        return []


def find_delivery_person():
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row

    try:
        stat = cur.execute(
            """
            SELECT user_id FROM delivery_person_accounts WHERE working = 0 AND is_offline = 0
            """
        ).fetchall()

        db.commit()
        result = [dict(row) for row in stat]
        print("success on internal finding delivery:", result)
        return result
    except Exception as e:
        print("got error on finding delivery,", e)
        return [{}]


def check_if_uuid_exists(uuid):
    db = get_db()
    cur = db.cursor()

    try:
        stat = cur.execute(
            """
            SELECT order_uuid FROM orders WHERE uuid = ?
        """,
            (uuid,),
        )
        result = [dict(row) for row in stat]
        print("sucess on internal checking if uuid exists", result)
        return result
    except Exception as e:
        print("got error on checking if uuid exists", e)
        return [{}]


def move_user_cart_to_order_list(user_id, order_uuid):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        stat = cur.execute(
            """
            INSERT INTO order_details (order_id, product_id, quantity)
            SELECT ?, product_id, quantity FROM cart WHERE user_id = ?
            """,
            (
                order_uuid,
                user_id,
            ),
        )
        db.commit()
        result = [dict(row) for row in stat]
        # now add it to orders deatil
        # for item in result:

        print("sucess on internal copying cart items to order_details", result)
        return result
    except Exception as e:
        print("got error on checking if uuid exists", e)
        return [{}]




def fetch_who_accepted_order_details(order_id):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row 

    try:
        stat = cur.execute(
            """
            SELECT delivery_guy_id FROM orders WHERE delivery_guy_accepts = 1 AND order_id = ? 

            """, (order_id,)

        ).fetchall()
        db.commit()
        
        result = [dict(row) for row in stat]
        print("success on fetching who accepted order details",result)
        return result
        # if stat:
        #     return {'status': "success"}

    except Exception as e:
        print("error on fetching who accepted order details: ", e)
        return {}
    



def get_products_from_order_detail(order_id):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        stat = cur.execute(
            """
            SELECT product_id FROM order_details WHERE  order_id = ? 

            """, (order_id,)

        ).fetchall()
        db.commit()
        
        result = [dict(row) for row in stat]
        print("success on fetching who fetching order details products", result)
        return result
    except Exception as e:
        print("error on fetching who accepted order details: ", e)
        return {}
    

def accept_order(user_id, order_id):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row

    try:
        stat = cur.execute(
            """
            UPDATE orders SET delivery_guy_accepts = 1 WHERE delivery_guy_id = ? AND order_id = ?
            """, (user_id, order_id,)
        )
        db.commit()
        
        # result = [dict(stat)]
        print("success on choosing accepting order details products",)
        if stat:
            return {'status': "success"}
        

    except Exception as e:
        print("error on fetching who accepted order details: ", e)
        return [{}]
    

def add_delivery_to_orders(user_id, order_id):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row

    try:
        stat = cur.execute(
            """
            UPDATE orders SET delivery_guy_id = ? WHERE order_id = ? 
            """, (user_id, order_id,)
        )
        db.commit()
        
        # result = [dict(stat)]
        print("success on adding delivery person to orders ",)
        if stat:
            return {'status': "success"}
        

    except Exception as e:
        print("error on adding delivery person to orders: ", e)
        return [{}]
    
def get_profile(user_id):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row
    try:
        user = cur.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,)).fetchone()
        db.commit()
        # No need to convert to a list of dictionaries, fetchone() already returns a dictionary-like object
        return dict(user) if user else {}
    except Exception as e:
        print(e)
        return {}

def get_customer_detail(order_id):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row

    try:
        stat = cur.execute(
            """
            SELECT user_id FROM orders WHERE order_id = ? 
            """, (order_id,)
        ).fetchone()
        db.commit()
        print("->",type(order_id), stat)
        
        if stat:
            # Directly use stat as it's a dictionary-like object returned by fetchone()
            result = dict(stat)
            print(result)
            profile = get_profile(result['user_id'])
            print("success on viewing customer profile: ", profile)
            return profile
        else:
            print("Order not found.")
            return {}
    except Exception as e:
        print("error on adding delivery person to orders: ", e)
        return {}

# get_customer_detail("51eb8e39-2ec0-44ae-83f6-b54708137a68")

def move_product_to_order_details(product_id, order_id, quantity):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row

    try:
        stat = cur.execute(
            """
            INSERT INTO order_details (product_id, order_id, quantity) values (?, ?, ? ) 
            """, (product_id, order_id, quantity,)
        )
        db.commit()
        print("->",type(order_id), stat)
        
        if stat:
            # Directly use stat as it's a dictionary-like object returned by fetchone()
            
            return {'status' : 'success'}
        else:
            print("Order not found.")
            return {}
    except Exception as e:
        print("error on adding delivery person to orders: ", e)
        return {}
    
def does_user_exists(user_id):
    db = get_db()
    cur = db.cursor()
    cur.row_factory = sqlite3.Row

    try:
        stat = get_profile(user_id)
        if stat:
            # Directly use stat as it's a dictionary-like object returned by fetchone()
            
            return {'status' : 'success'}
        else:
            print("Order not found.")
            return {}
    except Exception as e:
        print("error on adding delivery person to orders: ", e)
        return {}
    