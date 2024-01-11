import sqlite3 as sq 
import os 

async def start_db():
    global db, cur 
    db = sq.connect('delivery.db')
    cur = db.cursor()
    cur.row_factory = sq.Row 

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                phoneNumber VARCHAR(255) NOT NULL,
                photoURL VARCHAR(255) NOT NULL,
                longtiude VARCHAR(255) NULL,
                latitude VARCHAR(255) NULL,
                created_at TEXT
            )
        """)

        db.commit()
        print("Database table created successfully.")
    except Exception as e:
        print(f"Error creating database table: {e}")

async def update_profile(user_id, firstName, lastName, bio, phoneNumber, photoURL): 
    cur.execute(
        """
        UPDATE accounts SET firstName = ?, lastName = ?, bio = ?, phoneNumber = ?, photoURL = ? WHERE user_id = ?
        """,
        (firstName, lastName, bio, phoneNumber, photoURL, user_id)
    )
    db.commit()
    return True

async def create_profile(user_id, firstName, lastName, phoneNumber, photoURL, longtiude, latitude, created_at):
    try:
        status = cur.execute(
            """
            INSERT INTO accounts (user_id, firstName, lastName, phoneNumber, photoURL, longtiude, latitude, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, firstName, lastName, phoneNumber, photoURL, longtiude, latitude, created_at)
        )

        db.commit()
        print(status)
        return status
    except Exception as e: 
        print(e)
        return None

async def delete_profile(user_id):
    cur.execute(
        """
        DELETE FROM accounts WHERE user_id = ?
        """, 
        (user_id,)
    )
    db.commit()
    return True

async def get_profile(user_id):
    try:
        user = cur.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,)).fetchall()
        db.commit()
        # print("inside the db", user)
        result = [dict(obj) for obj in user]
        return result
    except Exception as e:
        print(e)
        return {}
    
async def get_providers():
    
    try:
        providers = cur.execute("SELECT DISTINCT product_service_provider FROM products")
        db.commit()
        result = [dict(provider) for provider in providers]
        print(result)
        return result
    except Exception as e:
        print("error on getting provider: ", e)
        return None
# async def get_products