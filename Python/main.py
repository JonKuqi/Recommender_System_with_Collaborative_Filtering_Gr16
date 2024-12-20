from PearsonCorrelation import PearsonCorrelation
from CosineSimilarity import ItemBasedFilter
from DataFetcher import DataFetcher


class MergingItemAndUserBased:

    @staticmethod
    def mergeItemAndUserBased(userId, data, automatic, alpha = 0.0):

        itemBasedBookList = ItemBasedFilter.getRecommendations(userId, data)

        #userBasedBookList = PearsonCorrelation.predict_for_user(userId)
        userBasedBookList = ItemBasedFilter.getRecommendations(userId, data)


        if automatic:
            alpha = MergingItemAndUserBased.getAlpha(userId, data)

        beta = 1.0 - alpha
        resultBookList = {}

        for bookId in itemBasedBookList:
            if bookId in userBasedBookList:
                resultBookList[bookId] = itemBasedBookList[bookId] * alpha + userBasedBookList[bookId] * beta
            else:
                resultBookList[bookId] = itemBasedBookList[bookId] * alpha

        sortedResults = dict(sorted(resultBookList.items(), key=lambda item: item[1], reverse=True))

        finalResultOrder = []

        allBooks = data['items']

        for bookId in sortedResults:
            if bookId in allBooks:
                finalResultOrder.append(allBooks[bookId]["title"])

        return finalResultOrder



    @staticmethod
    def getAlpha(userId, data):

        numberOfBooks = len(data['items'])
        numberOfRatingsOfUser = len(data['user-items'])


        alpha = 1 - (numberOfRatingsOfUser / (5 * numberOfBooks))

        print(alpha)
        return alpha





#resultList = MergingItemAndUserBased.mergeItemAndUserBased("1", DataFetcher.getAllData(), False, 0.5)
resultList = MergingItemAndUserBased.mergeItemAndUserBased("1", DataFetcher.getAllData(), True)

for i in range(len(resultList)):
    print(f"{i+1}. {resultList[i]}")

