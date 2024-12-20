from PearsonCorrelation import PearsonCorrelation
from CosineSimilarity import ItemBasedFilter
from DataFetcher import DataFetcher


class MergingItemAndUserBased:

    @staticmethod
    def mergeItemAndUserBased(userId, data, automatic, alpha = 0.0):

        itemBasedBookList = ItemBasedFilter.getRecommendations(userId, data)

        userBasedBookList = PearsonCorrelation.predict_for_user(userId)


        if automatic:
            alpha = MergingItemAndUserBased.getAlpha(data)

        beta = 1.0 - alpha
        resultBookList = {}

        for bookId in itemBasedBookList:
            if bookId in userBasedBookList:
                resultBookList[bookId] = itemBasedBookList[bookId] * alpha + userBasedBookList[bookId] * beta
            else:
                resultBookList[bookId] = itemBasedBookList[bookId] * alpha

        sortedResults = dict(sorted(resultBookList.items(), key=lambda item: item[1], reverse=True))

        finalResultOrder =

        allBooks = data['items']





    @staticmethod
    def getAlpha(data):
        pass







#MergingItemAndUserBased.mergeItemAndUserBased("1", DataFetcher.getAllData(), False, 0.5)

MergingItemAndUserBased.mergeItemAndUserBased("1", DataFetcher.getAllData(), True)