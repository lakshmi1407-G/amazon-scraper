from pymongo import MongoClient

client = MongoClient("mongodb+srv://KRISH:krish12345@productreviewdb.emqpfo0.mongodb.net/?retryWrites=true&w=majority")

db = client["product_sentiment_db"]
products_collection = db["products"]
reviews_collection = db["reviews"]

print("Mongo connection OK")