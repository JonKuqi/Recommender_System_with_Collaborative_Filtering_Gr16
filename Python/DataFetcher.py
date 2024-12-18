import json

class DataFetcher:

    @staticmethod
    def getBooks() -> list:
        with open('../Data/Books.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def getUsers() -> list:
        with open('../Data/Users.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def getUserBooks() -> list:
        with open('../Data/User-Book.json', 'r') as file:
            return json.load(file)
