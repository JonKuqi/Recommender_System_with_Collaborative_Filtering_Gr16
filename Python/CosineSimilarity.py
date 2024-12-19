from DataFetcher import DataFetcher


class ItemBasedFilter:

    #To return a dict of books and their score from 0 to 1 || 0 to 5
    @staticmethod
    def getRecommendations(userId):

        userId = 1 #FIX LATER

        allBooks = DataFetcher.getBooks()
        allUserBooks = DataFetcher.getUserBooks()

        print(allBooks)
        print(allUserBooks)

        ratedBooksIds = set()


        for i in range(len(allUserBooks)):
            if allUserBooks[i]['userId'] == str(userId):
                ratedBooksIds.add(allUserBooks[i]['bookId'])

        print(ratedBooksIds)

        unRatedBooks = {}
        ratedBooks = {}

        for bookId in allBooks:
            if bookId in ratedBooksIds:
                ratedBooks[bookId] = allBooks[bookId]
            else:
                unRatedBooks[bookId] = allBooks[bookId]

        print(ratedBooks)
        print(unRatedBooks)




    @staticmethod
    def createVector(text1, text2):
        pass



    @staticmethod
    def cosineSimilarity():
        # import ctypes
        #
        # c = ctypes.CDLL('../CFiles/CosineSimilarity.dll')
        # c.say_hello()



        pass



ItemBasedFilter.getRecommendations(1)


