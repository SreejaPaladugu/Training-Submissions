#Hard 2: Build a mini project applying Python Data Structures end-to-end
#Mini Project – Movie Ratings Analyzer

movies = [
    {"title": "Inception", "ratings": [9, 10, 9, 8]},
    {"title": "Interstellar", "ratings": [10, 9, 9, 10]},
    {"title": "Dunkirk", "ratings": [8, 7, 8, 7]}
]

# Compute average rating per movie
average_ratings = {m["title"]: sum(m["ratings"]) / len(m["ratings"]) for m in movies}
top_movie = max(average_ratings, key=average_ratings.get)

print(average_ratings)
print(f"Top Rated Movie: {top_movie}")
