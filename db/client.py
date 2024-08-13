from pymongo import MongoClient

#base de datos local
#db_client = MongoClient().local

#base de datos remota
db_client = MongoClient("mongodb+srv://lologg03:Lorenzo1@cluster0.5goja.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

