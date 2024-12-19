from DataFetcher import DataFetcher
import re
from collections import defaultdict
import ctypes




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

        ItemBasedFilter.filterAndSendToC(allBooks, ratedBooksIds)



    @staticmethod
    def filterAndSendToC(allBooks, ratedBooksId):

        cFunctions = ctypes.CDLL('../CFiles/CosineSimilarity.dll')
        cFunctions.cosineSimilarity.argtypes = [ctypes.POINTER(ctypes.c_double),
                                                ctypes.POINTER(ctypes.c_double),
                                                ctypes.c_int]
        cFunctions.cosineSimilarity.restype = ctypes.c_double

        #Helper function
        def cosine_similarity_py(arrA, arrB):
            n = len(arrA)
            if len(arrB) != n:
                raise ValueError("Input arrays must have the same length")

            # Convert Python lists to ctypes arrays
            arrayA = (ctypes.c_double * n)(*arrA)
            arrayB = (ctypes.c_double * n)(*arrB)

            # Call the C function
            result = cFunctions.cosineSimilarity(arrayA, arrayB, n)
            return result


        titleCategoryMatrix = ItemBasedFilter.createVectorCategory(allBooks, "title", True)
        authorCategoryMatrix = ItemBasedFilter.createVectorCategory(allBooks, "author", True)
        genreCategoryMatrix = ItemBasedFilter.createVectorCategory(allBooks, "genres", False)
        descriptionCategoryMatrix = ItemBasedFilter.createVectorCategory(allBooks, "description", True)

        titleRated = {}
        titleUnrated = {}
        ItemBasedFilter.filterRatedUnrated(titleCategoryMatrix, titleRated, titleUnrated, ratedBooksId)

        authorRated = {}
        authorUnRated = {}
        ItemBasedFilter.filterRatedUnrated(authorCategoryMatrix, authorRated, authorUnRated, ratedBooksId)


        genresRated = {}
        genresUnRated = {}
        ItemBasedFilter.filterRatedUnrated(genreCategoryMatrix, genresRated, genresUnRated, ratedBooksId)
        print(genresRated)
        print(genresUnRated)

        genreCosineSimilarityMatrix = {}


        for bookId in genresRated:
            for bookId_2 in genresUnRated:
                genreCosineSimilarityMatrix.setdefault(bookId, {})
                genreCosineSimilarityMatrix[bookId][bookId_2] = cosine_similarity_py(genresRated[bookId], genresUnRated[bookId_2])

        print(genreCosineSimilarityMatrix)

        descriptionRated = {}
        descriptionUnrated = {}
        ItemBasedFilter.filterRatedUnrated(descriptionCategoryMatrix, descriptionRated, descriptionUnrated, ratedBooksId)


        return None





    @staticmethod
    def filterRatedUnrated(matrix, rated, unrated, ratedBooksRating):
        print("Here", ratedBooksRating)
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
    def createVectorCategoryMatrixSentences(allBooks, category) -> dict:
        returnMatrix = {}

        for bookId in allBooks:

            valueCategory = allBooks[bookId][category]
            words = [word.lower().strip for word in re.findall(r'\w+', valueCategory)]

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




ItemBasedFilter.getRecommendations(1)


