import json
import ctypes
from DataFetcher import DataFetcher

class PearsonCorrelation:
    lib = ctypes.CDLL('../CFiles/PearsonCorrelation.dll')

    lib.PearsonCorrelation.argtypes = [
        ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), 
        ctypes.c_double, ctypes.c_double, ctypes.c_int
    ]
    lib.PearsonCorrelation.restype = ctypes.c_double

    lib.predict_rating.argtypes = [
        ctypes.POINTER(ctypes.c_double),  
        ctypes.POINTER(ctypes.c_double),  
        ctypes.POINTER(ctypes.c_double),  
        ctypes.c_int,                     
        ctypes.c_double                   
    ]
    lib.predict_rating.restype = ctypes.c_double

    @staticmethod
    def load_data():
        return DataFetcher.getAllData()

    @staticmethod
    def pearson_correlation(user1, user2, avg_user1, avg_user2):
        user1_arr = (ctypes.c_double * len(user1))(*user1)
        user2_arr = (ctypes.c_double * len(user2))(*user2)

        return PearsonCorrelation.lib.PearsonCorrelation(
            user1_arr, user2_arr, ctypes.c_double(avg_user1), ctypes.c_double(avg_user2), len(user1)
        )

    @staticmethod
    def predict_rating(avg_ratings, correlations, other_ratings, total_users, target_user_avg):
        avg_ratings_arr = (ctypes.c_double * len(avg_ratings))(*avg_ratings)
        correlations_arr = (ctypes.c_double * len(correlations))(*correlations)
        other_ratings_arr = (ctypes.c_double * len(other_ratings))(*other_ratings)

        return PearsonCorrelation.lib.predict_rating(
            avg_ratings_arr, correlations_arr, other_ratings_arr, total_users, ctypes.c_double(target_user_avg)
        )