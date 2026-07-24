"""
Database initialization script.
Run this once to create the MySQL database and tables.

Usage:
    python init_db.py

Prerequisites:
    - MySQL server must be running
    - Update config.py with your MySQL credentials
"""
import pymysql
from config import Config

def create_database():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="suraj4511",
        database="resume.db",
        port=3306
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{Config.MYSQL_DB}' created successfully (or already exists).")
    finally:
        connection.close()

def create_tables():
    from app import app
    from models import db
    
    with app.app_context():
        db.create_all()
        print("All tables created successfully.")

if __name__ == '__main__':
    print("=" * 50)
    print("Resume Builder - Database Initialization")
    print("=" * 50)
    
    print("\n[1/2] Creating database...")
    create_database()
    
    print("\n[2/2] Creating tables...")
    create_tables()
    
    print("\nDatabase initialization complete!")
    print("You can now run the application with: python app.py")
