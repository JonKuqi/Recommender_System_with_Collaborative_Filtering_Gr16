
class ItemBasedFilter:

    @staticmethod
    def cosineSimilarity():
        import ctypes

        c = ctypes.CDLL('../CFiles/CosineSimilarity.dll')
        c.say_hello()


        pass



ItemBasedFilter.cosineSimilarity()