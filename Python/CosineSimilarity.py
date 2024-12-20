import math

from DataFetcher import DataFetcher
import re
from collections import defaultdict
import ctypes
from sklearn.feature_extraction.text import TfidfVectorizer



class ItemBasedFilter:

    categoryImportance = {"title": 0.2,
                          "author": 0.2,
                          "rating": 0.2,
                          "genres": 0.2,
                          "description": 0.2}

    #To return a dict of books and their score from  0 to 5

    cFunctions = ctypes.CDLL('../CFiles/CosineSimilarity.dll')

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
                ratedBooksRatings[allUserBooks[i]['bookId']] = allUserBooks[i]['rating']


        unRatedBooks = {}
        ratedBooks = {}

        for bookId in allBooks:
            if bookId in ratedBooksIds:
                ratedBooks[bookId] = allBooks[bookId]
            else:
                unRatedBooks[bookId] = allBooks[bookId]

        ItemBasedFilter.filterAndSendToC(allBooks, ratedBooksIds, ratedBooksRatings)



    @staticmethod
    def filterAndSendToC(allBooks, ratedBooksId, ratedBookRatings):

        titleCategoryMatrix = ItemBasedFilter.createVectorCategory(allBooks, "title", True)
        authorCategoryMatrix = ItemBasedFilter.createVectorCategory(allBooks, "author", True)
        genreCategoryMatrix = ItemBasedFilter.createVectorCategory(allBooks, "genres", False)
        descriptionCategoryMatrix = ItemBasedFilter.createVectorUsingTfidfVectorizer(allBooks, "description")


        titleRated = {}
        titleUnrated = {}
        ItemBasedFilter.filterRatedUnrated(titleCategoryMatrix, titleRated, titleUnrated, ratedBooksId)
        titleCosineSimilarityMatrix = {}
        ItemBasedFilter.sendToC(titleRated, titleUnrated, titleCosineSimilarityMatrix)
        ItemBasedFilter.getRatingForCategory(titleCosineSimilarityMatrix, ratedBookRatings)
        print(titleCosineSimilarityMatrix['23'])


        authorRated = {}
        authorUnRated = {}
        ItemBasedFilter.filterRatedUnrated(authorCategoryMatrix, authorRated, authorUnRated, ratedBooksId)
        authorCosineSimilarityMatrix = {}
        ItemBasedFilter.sendToC(authorRated, authorUnRated, authorCosineSimilarityMatrix)

        genresRated = {}
        genresUnRated = {}
        ItemBasedFilter.filterRatedUnrated(genreCategoryMatrix, genresRated, genresUnRated, ratedBooksId)
        genreCosineSimilarityMatrix = {}
        ItemBasedFilter.sendToC(genresRated, genresUnRated, genreCosineSimilarityMatrix)

        descriptionRated = {}
        descriptionUnrated = {}
        ItemBasedFilter.filterRatedUnrated(descriptionCategoryMatrix, descriptionRated, descriptionUnrated, ratedBooksId)
        descriptionCosineSimilarityMatrix = {}
        ItemBasedFilter.sendToC(descriptionRated, descriptionUnrated, descriptionCosineSimilarityMatrix)




    #ratedBooksRating {bookId: 0.0-5, ...}
    @staticmethod
    def getRatingForCategory(categoryMatrix, ratedBooksRatings):

        unratedBookLists = {}
        for bookId in categoryMatrix:
            for unRatedBookId in categoryMatrix[bookId]:
                if unRatedBookId in unratedBookLists:
                    unratedBookLists[unRatedBookId].append(categoryMatrix[bookId][unRatedBookId])
                else:
                    unratedBookLists[unRatedBookId] = [categoryMatrix[bookId][unRatedBookId]]

        #print(unratedBookLists)








    @staticmethod
    def sendToC(ratedMap, unRatedMap, resultMatrix):

        ItemBasedFilter.cFunctions.cosineSimilarity.argtypes = [ctypes.POINTER(ctypes.c_double),
                                                ctypes.POINTER(ctypes.c_double),
                                                ctypes.c_int]
        ItemBasedFilter.cFunctions.cosineSimilarity.restype = ctypes.c_double

        ItemBasedFilter.cFunctions.free_array.argtypes = [ctypes.POINTER(ctypes.c_double)]
        ItemBasedFilter.cFunctions.free_array.restype = None

        # Helper function
        def cosine_similarity_py(arrA, arrB):
            n = len(arrA)
            if len(arrB) != n:
                raise ValueError("Input arrays must have the same length")

            # Convert Python lists to ctypes arrays
            arrayA = (ctypes.c_double * n)(*arrA)
            arrayB = (ctypes.c_double * n)(*arrB)

            # Call the C function
            result = ItemBasedFilter.cFunctions.cosineSimilarity(arrayA, arrayB, n)
            return result


        for bookId in ratedMap:
            for bookId_2 in unRatedMap:
                resultMatrix.setdefault(bookId, {})
                resultFromC = cosine_similarity_py(ratedMap[bookId], unRatedMap[bookId_2])
                if  not math.isnan(resultFromC):
                    resultMatrix[bookId][bookId_2] = resultFromC
                else:
                    resultMatrix[bookId][bookId_2] = 0



    @staticmethod
    def filterRatedUnrated(matrix, rated, unrated, ratedBooksRating):
        for bookId in matrix:
            if bookId in ratedBooksRating:
                rated[bookId] = matrix[bookId]
            else:
                unrated[bookId] = matrix[bookId]


    @staticmethod
    def createVectorCategory(allBooks, category, sentence):
        if sentence:
            matrix = ItemBasedFilter.createVectorCategoryMatrixSentences(allBooks, category)
        else:
            matrix = ItemBasedFilter.createVectorCategoryMatrixLists(allBooks, category)

        vectorMatrix = defaultdict(list)

        for bookId in allBooks:
            vector = []
            for word in matrix:
                vector.append(matrix[word].get(bookId, 0))

            vectorMatrix[bookId] = vector
        return vectorMatrix



    @staticmethod
    def createVectorUsingTfidfVectorizer(allBooks, category):

        categoryAll = {}

        for bookId in allBooks:
            categoryAll[bookId] = allBooks[bookId][category]


        category_keys = list(categoryAll.keys())

        vectorizer = TfidfVectorizer(stop_words='english')
        categoryMatrixNoKeys = vectorizer.fit_transform(categoryAll.values())

        toReturn = {}
        for i, bookId in enumerate(category_keys):
            toReturn[bookId] = [float(value) for value in categoryMatrixNoKeys[i].toarray()[0]]

        # for bookId, vector in toReturn.items():
        #     print(f"Book ID: {bookId}\nVector: {vector}\n")

        return toReturn


    @staticmethod
    def createVectorCategoryMatrixSentences(allBooks, category) -> dict:
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


        #print(returnMatrix)
        return returnMatrix


    @staticmethod
    def createVectorCategoryMatrixLists(allBooks, category):
        returnMatrix = {}

        for bookId in allBooks:
            words = allBooks[bookId][category]

            for word in words:
                if word in returnMatrix:
                    if bookId in returnMatrix[word]:
                        returnMatrix[word][bookId] += 1
                    else:
                        returnMatrix[word][bookId] = 1
                else:
                    returnMatrix[word] = {bookId: 1}

        # print(returnMatrix)
        return returnMatrix





    #Just for testing purposes. NOT IN USE
    @staticmethod
    def cosineTest(arrA, arrB):
        if len(arrA) != len(arrB):
            raise ValueError("Input arrays must have the same length")

        # Compute the dot product
        dot_product = sum(a * b for a, b in zip(arrA, arrB))

        # Compute the magnitudes
        sum_a_squared = sum(a * a for a in arrA)
        sum_b_squared = sum(b * b for b in arrB)

        magnitude_a = math.sqrt(sum_a_squared)
        magnitude_b = math.sqrt(sum_b_squared)

        # Handle division by zero
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        # Calculate cosine similarity
        return dot_product / (magnitude_a * magnitude_b)





ItemBasedFilter.getRecommendations(1)


