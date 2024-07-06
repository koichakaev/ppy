from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb+srv://user1:TgfT63GeR679O5J5@cluster0.dydrioq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    return client.parser

def save_vacancy(vacancy):
    db = get_db()
    vacancies_collection = db.vacancies
    vacancies_collection.insert_one(vacancy)
