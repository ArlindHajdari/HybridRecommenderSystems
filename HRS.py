import pandas as pd
from surprise import SVD, Reader, Dataset
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

RATINGS_SMALL = "../data/ratings_small.csv"
MOVIES = "../data/movie_ids.csv"
METADATA_CLEAN = "../data/metadata_clean.csv"
ORIGINAL_DATASET = "../data/movies_metadata.csv"


class HybridRecommenderSystem:
    def __init__(self, movies_path=MOVIES,
                 clean_dataset_path=METADATA_CLEAN, original_dataset_path=ORIGINAL_DATASET):
        self.svd = SVD()
        self.reader = Reader()
        id_map = pd.read_csv(movies_path)
        self.id_to_title = id_map.set_index('id')
        self.clean_dataset_path = clean_dataset_path
        self.original_dataset_path = original_dataset_path

    def initialize(self):
        data = self.load_ratings(RATINGS_SMALL)
        self.train_svd(data)
        self.clean_dataframe = pd.read_csv(self.clean_dataset_path)  # Clean dataset
        self.original_dataframe = pd.read_csv(self.original_dataset_path, low_memory=False)  # Original dataset

    def load_ratings(self, csv_path):
        ratings = pd.read_csv(csv_path)
        data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], self.reader)
        return data

    def train_svd(self, dataset: Dataset):
        trainset = dataset.build_full_trainset()
        self.svd.fit(trainset)

    def calculate_tfidf(self):
        # Add extra columns to clean_dataset from orignial's one
        self.clean_dataframe['overview'], self.clean_dataframe['id'] = self.original_dataframe['overview'], self.original_dataframe['id']

        # Define a TF-IDF Vectorizer Object
        tfidf = TfidfVectorizer(stop_words='english')  # Remove all english stopwords

        # Replace NaN with an empty string
        self.clean_dataframe['overview'] = self.clean_dataframe['overview'].fillna('')

        # Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
        tfidf_matrix = tfidf.fit_transform(self.clean_dataframe['overview'])

        return tfidf_matrix

    def calculate_cosine_similarity(self):
        tfidf_matrix = self.calculate_tfidf()

        cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

        return cosine_similarity

    def generate_indicies(self, movies_dataset):
        indices = pd.Series(movies_dataset.index, index=movies_dataset['title']).drop_duplicates()
        return indices

    def content_based_recommender(self, title, movies_dataset):
        # Obtain the index of the movie that matches the title
        indices = self.generate_indicies(movies_dataset)
        idx = indices[title]

        # Calculate cosine similarity
        cosine_similarity = self.calculate_cosine_similarity()

        # Get the pairwsie similarity scores of all movies with that movie
        # And convert it into a list of tuples as described above
        sim_scores = list(enumerate(cosine_similarity[idx]))

        # Sort the movies based on the cosine similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies. Ignore the first movie.
        sim_scores = sim_scores[1:26]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return movies_dataset['title'].iloc[movie_indices]

    def hybrid(self, userId, title):
        movie_indices = self.content_based_recommender(title, self.original_dataframe)

        #Extract the metadata of the aforementioned movies
        movies = self.original_dataframe.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year', 'id']]

        #Compute the predicted ratings using the SVD filter
        movies['est'] = movies['id'].apply(lambda x: self.svd.predict(userId, self.id_to_title.loc[x]['title']).est)

        #Sort the movies in decreasing order of predicted rating
        movies = movies.sort_values('est', ascending=False)

        #Return the top 10 movies as recommendations
        return movies.head(10)

