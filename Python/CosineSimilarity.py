from DataFetcher import DataFetcher
import re
from collections import defaultdict

class ItemBasedFilter:

    categoryImportance = {"title": 0.2,
                          "author": 0.2,
                          "rating": 0.2,
                          "genres": 0.2,
                          "description": 0.2}

    #To return a dict of books and their score from  0 to 5

    ## MAIN METHOD
    @staticmethod
    def getRecommendations(userId):

        userId = 1 #FIX LATER

        allBooks = DataFetcher.getBooks()
        allUserBooks = DataFetcher.getUserBooks()

        ratedBooksIds = set()
        ratedBooksRatings = {}

        for i in range(len(allUserBooks)):
            if allUserBooks[i]['userId'] == str(userId):
                ratedBooksIds.add(allUserBooks[i]['bookId'])
                ratedBooksRatings['bookId'] = allUserBooks[i]['rating']


        unRatedBooks = {}
        ratedBooks = {}

        for bookId in allBooks:
            if bookId in ratedBooksIds:
                ratedBooks[bookId] = allBooks[bookId]
            else:
                unRatedBooks[bookId] = allBooks[bookId]

        ItemBasedFilter.createVectorCategory(allBooks, "title")



    @staticmethod
    def createVectorCategory(allBooks, category):
        matrix = ItemBasedFilter.createVectorCategoryMatrix(allBooks, category)
        vectorMatrix = defaultdict(list)

        for bookId in allBooks:
            vector = []
            for word in matrix:
                vector.append(matrix[word].get(bookId, 0))

            vectorMatrix[bookId] = vector
        return vectorMatrix


    @staticmethod
    def createVectorCategoryMatrix(allBooks, category) -> dict:
        returnMatrix = {}

        for bookId in allBooks:

            valueCategory = allBooks[bookId][category]
            words = [word.lower() for word in re.findall(r'\w+', valueCategory)]

            for word in words:
                if word in returnMatrix:
                    if bookId in returnMatrix[word]:
                        returnMatrix[word][bookId] += 1
                    else:
                        returnMatrix[word][bookId] = 1
                else:
                    returnMatrix[word] = {bookId:1}


        print(returnMatrix)
        return returnMatrix



    @staticmethod
    def cosineSimilarity():
        import ctypes

        c = ctypes.CDLL('../CFiles/CosineSimilarity.dll')
        c.say_hello()

        pass

ItemBasedFilter.getRecommendations(1)


