import json

class DataFetcher:

    @staticmethod
    def getBooks():
        with open('../Data/Books.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def getUsers():
        with open('../Data/Users.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def getUserBooks():
        with open('../Data/User-Book.json', 'r') as file:
            return json.load(file)

    #Funksion Ekstra per Kaltrinen
    @staticmethod
    def getAllData():
        return {"users": DataFetcher.getUsers(), "items": DataFetcher.getBooks(), "user-items": DataFetcher.getUserBooks()}




