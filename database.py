# import sqlite3
# from config import DATABASE_PATH

# def get_db():
#     conn = sqlite3.connect(DATABASE_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn

# def init_db():
#     db = get_db()
#     db.execute("""
#         CREATE TABLE IF NOT EXISTS destinations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             state TEXT NOT NULL,
#             price INTEGER NOT NULL,
#             rating REAL,
#             description TEXT,
#             image TEXT
#         )
#     """)
#     db.execute("""
#         CREATE TABLE IF NOT EXISTS bookings (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             customer_name TEXT NOT NULL,
#             destination_id INTEGER NOT NULL,
#             adults INTEGER NOT NULL,
#             children INTEGER NOT NULL,
#             total_amount REAL NOT NULL,
#             booking_date TEXT NOT NULL,
#             FOREIGN KEY(destination_id) REFERENCES destinations(id)
#         )
#     """)
#     db.commit()

# import sqlite3
# from flask import g
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()



# # Database file inside instance folder
# DATABASE = "instance/travel.db"

# def get_db():
#     """
#     Get a SQLite database connection for the current Flask request context.
#     """
#     db = getattr(g, "_database", None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         db.row_factory = sqlite3.Row  # Access columns by name
#     return db

# def close_db(e=None):
#     """
#     Close the database connection at the end of request.
#     """
#     db = getattr(g, "_database", None)
#     if db is not None:
#         db.close()

# def init_db():
#     """
#     Initialize all tables from models.
#     This should be called once when starting the app for the first time.
#     """
#     from models.booking import Booking
#     from destination import Destination
#     from user import Home

#     db = get_db()
    
#     # Create tables
#     Booking.create_table()
#     Destination.create_table()
#     Home.create_table()

#     # Optional: Add sample destinations if none exist
#     if not Destination.get_all():
#         Destination.add("Varanasi", "Ancient city, ghats, Hindu temples.", "/static/images/varanasi.jpg")
#         Destination.add("Jaipur", "Pink City, palaces, forts.", "/static/images/jaipur.jpg")
#         Destination.add("Kedarnath", "Himalayan temple of Lord Shiva.", "/static/images/kedarnath.jpg")
#         Destination.add("Somnath", "Jyotirlinga shrine, Gujarat.", "/static/images/somnath.jpg")
#         Destination.add("Khajuraho", "Famous Hindu temples with sculptures.", "/static/images/khajuraho.jpg")

#     # Optional: Add home page content if empty
#     if not Home.get_latest():
#         Home.add(
#             "Explore India’s Ancient Heritage",
#             "Experience the cultural richness of North & West India — temples, palaces, rituals and Himalayan pilgrimage.",
#             "India is known for its vast cultural lineage dating back thousands of years..."
#         )

#     db.commit()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
