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
    
    @staticmethod
    def predict_for_user(user_id):
        data = PearsonCorrelation.load_data()
        users = data['users']
        books = data['items']
        ratings = data['user-items']

        target_user_ratings = {rating['bookId']: float(rating['rating']) for rating in ratings if rating['userId'] == str(user_id)}
        if not target_user_ratings:
            print(f"Perdoruesi me ID {user_id} nuk ka asnje rating.")
            return {}

        target_user_mean = sum(target_user_ratings.values()) / len(target_user_ratings)

        user_means = {}
        for user_key, user_value in users.items():
            if int(user_key) == user_id:
                continue

            user_ratings = {rating['bookId']: float(rating['rating']) for rating in ratings if rating['userId'] == user_key}
            if user_ratings:
                user_means[user_key] = sum(user_ratings.values()) / len(user_ratings)

        predictions = {}
        for book_id in books.keys():
            if book_id in target_user_ratings:
                continue

            relevant_ratings = [float(rating['rating']) for rating in ratings if rating['bookId'] == book_id and rating['userId'] != str(user_id)]
            if not relevant_ratings:
                continue

            correlations = []
            for user_key, mean in user_means.items():
                user_ratings = {rating['bookId']: float(rating['rating']) for rating in ratings if rating['userId'] == user_key}
                common_items = set(target_user_ratings.keys()).intersection(user_ratings.keys())
                if not common_items:
                    continue

                user1_ratings = [target_user_ratings[item] for item in common_items]
                user2_ratings = [user_ratings[item] for item in common_items]
                correlation = PearsonCorrelation.pearson_correlation(user1_ratings, user2_ratings, target_user_mean, mean)
                correlations.append(correlation)

            if correlations:
                prediction =PearsonCorrelation.predict_rating(
                    list(user_means.values()), correlations, relevant_ratings, len(user_means), target_user_mean
                )
                predictions[book_id] = prediction

        return predictions