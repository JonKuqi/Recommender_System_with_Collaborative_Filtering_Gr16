import json
import math
from DataFetcher import DataFetcher

class PearsonCorrelation:

    @staticmethod
    def load_data():
        return DataFetcher.getAllData()

    @staticmethod
    def pearson_correlation(user1, user2, avg_user1, avg_user2):
        numerator = 0.0
        sum_sq_diff_user1 = 0.0
        sum_sq_diff_user2 = 0.0

        for u1, u2 in zip(user1, user2):
            diff_user1 = u1 - avg_user1
            diff_user2 = u2 - avg_user2

            numerator += diff_user1 * diff_user2
            sum_sq_diff_user1 += diff_user1 ** 2
            sum_sq_diff_user2 += diff_user2 ** 2

        if sum_sq_diff_user1 == 0.0 or sum_sq_diff_user2 == 0.0:
            return 0.0

        denominator = math.sqrt(sum_sq_diff_user1 * sum_sq_diff_user2)
        return numerator / denominator

    @staticmethod
    def predict_rating(avg_ratings, correlations, other_ratings, total_users, target_user_avg):
        numerator = 0.0
        denominator = 0.0

        for avg_rating, correlation, other_rating in zip(avg_ratings, correlations, other_ratings):
            if other_rating > 0:  
                weight = correlation
                numerator += weight * (other_rating - avg_rating)
                denominator += abs(weight)

        predicted_rating = target_user_avg + (numerator / denominator if denominator != 0 else 0)

        
        predicted_rating = max(0.0, min(5.0, predicted_rating))
        return predicted_rating

    @staticmethod
    def predict_for_user(user_id):
        data = PearsonCorrelation.load_data()
        users = data['users']
        books = data['items']
        ratings = data['user-items']

        target_user_ratings = {rating['bookId']: float(rating['rating']) for rating in ratings if rating['userId'] == str(user_id)}
        if not target_user_ratings:
            print(f"Përdoruesi me ID {user_id} nuk ka asnjë vlerësim.")
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
                prediction = PearsonCorrelation.predict_rating(
                    list(user_means.values()), correlations, relevant_ratings, len(user_means), target_user_mean
                )
                predictions[book_id] = prediction

        return predictions



