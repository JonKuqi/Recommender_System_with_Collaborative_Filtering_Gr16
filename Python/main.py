from PearsonCorrelation import PearsonCorrelation
from CosineSimilarity import ItemBasedFilter
from DataFetcher import DataFetcher
from colorama import init, Fore, Style
init(autoreset=True)

class MergingItemAndUserBased:

    @staticmethod
    def mergeItemAndUserBased(userId, data, numberOf, automatic, alpha = 0.0):
        print()
        itemBasedBookList = ItemBasedFilter.getRecommendations(userId, data)
        print("Item Rating: ",itemBasedBookList)
        print()
        userBasedBookList = PearsonCorrelation.predict_for_user(userId)
        print("User Rating: ", userBasedBookList)
        print()
        #userBasedBookList = ItemBasedFilter.getRecommendations(userId, data)


        if automatic:
            alpha = MergingItemAndUserBased.getAlpha(userId, data)

        print("Alpha:", alpha)
        print()

        beta = 1.0 - alpha
        resultBookList = {}

        for bookId in itemBasedBookList:
            if bookId in userBasedBookList:
                resultBookList[bookId] = itemBasedBookList[bookId] * alpha + userBasedBookList[bookId] * beta
            else:
                resultBookList[bookId] = itemBasedBookList[bookId]

        sortedResults = dict(sorted(resultBookList.items(), key=lambda item: item[1], reverse=True))

        finalResultOrder = []

        allBooks = data['items']

        finalResultOrder.append(('Number', numberOf))

        for bookId in sortedResults:
            if bookId in allBooks:
                finalResultOrder.append((allBooks[bookId]["title"], round(sortedResults[bookId], 2)))

        return finalResultOrder



    @staticmethod
    def getAlpha(data):

        numberOfBooks = len(data['items'])
        numberOfRatingsOfUser = len(data['user-items'])
        alpha =  abs(0.5 - (numberOfRatingsOfUser / (5 * numberOfBooks)))
        return alpha

    @staticmethod
    def displayTable(_resultList):
        numberOf = _resultList[0][1]
        del(_resultList[0])

        headers = ["Index", "Book Title", "Rating"]
        max_title_length = max(len(result[0]) for result in _resultList) + 4

        print(f"{headers[0]:<6} | {headers[1]:<{max_title_length}} | {headers[2]}")
        print("-" * (10 + max_title_length + 15))

        for i, (book_title, rating) in enumerate(_resultList):
            if i < numberOf:
                color = Fore.GREEN
            else:
                color = Fore.YELLOW

            print(f"{color}{i + 1:<6} | {book_title:<{max_title_length}} | {rating}{Style.RESET_ALL}")







resultList = MergingItemAndUserBased.mergeItemAndUserBased("1", DataFetcher.getAllData(), 50, False, 0.5)
#resultList = MergingItemAndUserBased.mergeItemAndUserBased("1", DataFetcher.getAllData(), 20, True)

MergingItemAndUserBased.displayTable(resultList)

