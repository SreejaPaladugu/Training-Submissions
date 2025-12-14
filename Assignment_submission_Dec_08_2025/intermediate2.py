from sklearn.feature_extraction import DictVectorizer

# NoSQL-style documents
documents = [
    {"product": "Laptop", "price": 900},
    {"product": "Phone", "price": 600},
    {"product": "Laptop", "price": 950}
]

vectorizer = DictVectorizer(sparse=False)
numeric_data = vectorizer.fit_transform(documents)

print("Feature Names:", vectorizer.get_feature_names_out())
print("Vectorized Data:\n", numeric_data)
