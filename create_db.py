import pymysql
from config import Config

def create_database():
    try:
        # Connect to MySQL server (no database selected)
        conn = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        print(f"Database '{Config.DB_NAME}' checked/created successfully.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        print("Please ensure your MySQL server is running and credentials in config.py are correct.")

if __name__ == "__main__":
    create_database()
