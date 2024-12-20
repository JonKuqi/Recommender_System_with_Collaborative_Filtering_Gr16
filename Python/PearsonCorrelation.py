import json
import ctypes
from DataFetcher import DataFetcher
import math

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
        #if not (len(avg_ratings) == len(correlations) == len(other_ratings) == total_users):
         #   raise ValueError("Input lists must all have the same length as 'total_users'.")

        avg_ratings_arr = (ctypes.c_double * len(avg_ratings))(*avg_ratings)
        correlations_arr = (ctypes.c_double * len(correlations))(*correlations)
        other_ratings_arr = (ctypes.c_double * len(other_ratings))(*other_ratings)

        #print("Here")
        return PearsonCorrelation.lib.predict_rating(
            avg_ratings_arr, correlations_arr, other_ratings_arr,  ctypes.c_int(total_users),  ctypes.c_double(target_user_avg)
        )
    
    @staticmethod
    def predict_for_user(user_id) -> dict:
        data = PearsonCorrelation.load_data()
        users = data['users']
        books = data['items']
        ratings = data['user-items']


        target_user_ratings = {rating['bookId']: float(rating['rating']) for rating in ratings if rating['userId'] == str(user_id)}
        #print("targetUserrATING: ",target_user_ratings)

        if len(target_user_ratings) <= 0:
            print(f"Perdoruesi me ID {user_id} nuk ka asnje rating.")
            return {}

        target_user_mean = sum(target_user_ratings.values()) / len(target_user_ratings)

        user_means = {}
        for user_key, user_value in users.items():
            if user_key == user_id:
                continue

            user_ratings = {rating['bookId']: float(rating['rating']) for rating in ratings if rating['userId'] == user_key}
            if user_ratings:
                user_means[user_key] = sum(user_ratings.values()) / len(user_ratings)

        #print("UserMeans", user_means)

        predictions = {}
        for book_id in books.keys():
            if book_id in target_user_ratings:
                continue


            relevant_ratings = []
            for rating in ratings:
                if rating['bookId'] == book_id:
                    relevant_ratings.append(float(rating['rating']))


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




    @staticmethod
    def pearson_correlation_formula(user1, user2, avg_user1, avg_user2, n):
        numerator = 0.0
        sum_sq_diff_user1 = 0.0
        sum_sq_diff_user2 = 0.0

        for i in range(n):
            diff_user1 = user1[i] - avg_user1
            diff_user2 = user2[i] - avg_user2

            numerator += diff_user1 * diff_user2
            sum_sq_diff_user1 += diff_user1 ** 2
            sum_sq_diff_user2 += diff_user2 ** 2

        denominator = math.sqrt(sum_sq_diff_user1 * sum_sq_diff_user2)

        if denominator == 0.0:
            return 0.0

        return numerator / denominator

    @staticmethod
    def predict_rating_formula(avg_ratings, correlations, other_ratings, total_users, target_user_avg):
        # Input validation to avoid IndexError


        numerator = 0.0
        denominator = 0.0

        for i in range(total_users):
            if other_ratings[i] > 0:  # Consider only positive ratings
                weight = correlations[i]
                numerator += weight * (other_ratings[i] - avg_ratings[i])
                denominator += abs(weight)

        predicted_rating = target_user_avg + (numerator / denominator if denominator != 0 else 0)
        return predicted_rating

#print(PearsonCorrelation.predict_for_user("1"))

# print(PearsonCorrelation.predict_for_user(2))