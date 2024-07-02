import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import re

print("Starting the program")


#=================================================================

books_df = pd.read_csv(r"books.csv")
def preprocess_text(text):
    return str(text).lower().replace('[^a-z\s]', '')

def preprocess_titles(book):
    text = re.sub('\(.*?\)', '', book)  # Remove content inside parentheses
    return text.strip()

books_df['processed_description'] = books_df['Genres'].apply(preprocess_text)
books_df['title'] = books_df['Book'].apply(preprocess_titles)
books_df['processed_genres'] = books_df['Genres'].apply(preprocess_text)
books_df['processed_authors'] = books_df['Author'].apply(preprocess_text)


combined_features = books_df['processed_description'] + ' ' + books_df['processed_genres'] + ' ' + books_df['processed_authors']

vectorizer = TfidfVectorizer(stop_words='english')

#Get the matrices for the model
tfidf_matrix = vectorizer.fit_transform(combined_features)

n_neighbors = 6  # Number of neighbors to return, including the input book
model = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
model.fit(tfidf_matrix) #Train the model for descriptions

# Create a mapping from book titles to their index 
title_to_index = pd.Series(books_df.index, index=books_df['title'].apply(lambda x: x.lower()))
titles_list = books_df['title'].tolist()

#===================================================================


# Recommendation function based on descriptions
def recommend_books(title, n = 6,model=model, books_df=books_df, title_to_index=title_to_index):
    idx = title_to_index[title.lower()]
    distances, indices = model.kneighbors(tfidf_matrix[idx], n_neighbors=n)
    book_indices = []
    # Remove the input book from the recommendations
    for book_index in indices[0]:  
        if (book_index != idx): book_indices.append(book_index)

    book_lists = books_df['title'].iloc[book_indices].values.tolist()
    books = []
    for title in book_lists:
        row = books_df[books_df['title'].str.lower() == title.lower()].iloc[0]
        b1 = (row['Book'], row['Avg_Rating'], row['URL'], row['Description'], row['Author'], row['Genres'])
        books.append(b1)
    return books




