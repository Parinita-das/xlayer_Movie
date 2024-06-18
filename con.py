import motor.motor_asyncio

class Database:
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        db = client['movie_book']
        print("Database connection established successfully") 
    except Exception as e:
        print(f"Error connecting to Database: {e}")
        db = None