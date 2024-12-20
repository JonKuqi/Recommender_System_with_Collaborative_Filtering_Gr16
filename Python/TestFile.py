from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example book data
books = {
    "1": {
        "title": "Romeo and Juliet",
        "description": "In Romeo and Juliet, Shakespeare creates a violent world, in which two young people fall in love. The Montagues and the Capulets are engaged in a blood feud."
    },
    "2": {
        "title": "1984",
        "description": "1984 is a chilling portrayal of a totalitarian regime that uses surveillance, censorship, and mind control to maintain power. Winston Smith tries to defy the oppressive government."
    },
    "3": {
        "title": "Hamlet",
        "description": "Hamlet is a tragedy by Shakespeare, where Prince Hamlet seeks revenge against his uncle Claudius, who has murdered Hamlet's father."
    }
}

# Extract descriptions
descriptions = [book["description"] for book in books.values()]
print(descriptions)

titles = [book["title"] for book in books.values()]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(descriptions)

# Display TF-IDF matrix shape
print(f"TF-IDF Matrix Shape: {tfidf_matrix.shape}")

# Compute cosine similarity between all pairs of books
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Print cosine similarity matrix
print("Cosine Similarity Matrix:")
for i, title1 in enumerate(titles):
    for j, title2 in enumerate(titles):
        print(f"Similarity between '{title1}' and '{title2}': {cosine_sim[i][j]:.4f}")