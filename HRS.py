import pandas as pd
from surprise import SVD, Reader, Dataset
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from statistics import mean
import pickle
import os

RATINGS_SMALL = "../data/ratings_small.csv"
MOVIES = "../data/movies.csv"
METADATA_CLEAN = "../data/metadata_clean.csv"
ORIGINAL_DATASET = "../data/movies_metadata.csv"
TOP_MOVIES = 3


class HybridRecommenderSystem:
    def __init__(self, movies_path=MOVIES,
                 clean_dataset_path=METADATA_CLEAN, original_dataset_path=ORIGINAL_DATASET, rating_dataset_path=RATINGS_SMALL, top_movies=TOP_MOVIES):
        self.svd = SVD()
        self.reader = Reader()
        id_map = pd.read_csv(movies_path)
        self.id_to_title = id_map.set_index('movieId')
        self.ratings_dataset = pd.read_csv(rating_dataset_path)  # Rating dataset
        self.clean_dataframe = pd.read_csv(clean_dataset_path)  # Clean dataset
        self.original_dataframe = pd.read_csv(original_dataset_path, low_memory=False)  # Original dataset
        self.top_movies = top_movies
        self.train_svd()

    def train_svd(self):
        """ Create/Get the model trained with the ratings """

        if not os.path.exists("../data/svd_model.p"):  # If the model file doesn't exists, create it
            ratings_for_reader = Dataset.load_from_df(self.ratings_dataset[['userId', 'movieId', 'rating']], self.reader)
            trainset = ratings_for_reader.build_full_trainset()
            temp_model = self.svd.fit(trainset)  # Train procedure
            with open("../data/svd_model.p", 'wb') as model:
                pickle.dump(temp_model, model)
        else:  # If the model file exists, load it into svd variable
            with open('../data/svd_model.p', 'rb') as fp:
                self.svd = pickle.load(fp, encoding="utf8")

    def calculate_tfidf(self):
        """ Generatio of TFIDF matrix needed for cosine similarity """

        # Add extra columns to clean_dataset from orignial's one
        self.clean_dataframe['overview'], self.clean_dataframe['id'] = self.original_dataframe['overview'], self.original_dataframe['id']

        # Define a TF-IDF Vectorizer Object
        tfidf = TfidfVectorizer(stop_words='english')  # Remove all english stopwords

        # Replace NaN with an empty string
        self.clean_dataframe['overview'] = self.clean_dataframe['overview'].fillna('')

        # Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
        tfidf_matrix = tfidf.fit_transform(self.clean_dataframe['overview'].head(10000))  # 10000 because of memory error

        return tfidf_matrix

    def calculate_cosine_similarity(self):
        """ Calculation of cosine similarity """
        tfidf_matrix = self.calculate_tfidf()

        cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)  # Cosine similarity matrix calculation

        return cosine_similarity

    def generate_indicies(self, userIds):
        """ Get the top(3) movies from the users selected """

        # From ratings dataset
        # 1. Remove duplicates
        # 2. Fetch the rows that match the selected users
        # 3. Group the results by users
        # 4. Sort the groups from step 3 by movie rating in descending order (Biggest ratings first)
        # 5. Get the Top(3) results from each group
        # 6. Drop the null values
        indices = self.ratings_dataset.drop_duplicates().where(self.ratings_dataset['userId'].isin(userIds)).groupby('userId').apply(lambda _df: _df.sort_values(by=['rating'], ascending=False).head(self.top_movies)).dropna()[['movieId']].astype(int).values.flatten()
        return indices

    def content_based_recommender(self, usersIds):
        """ Fetch the movies by content based filtering """

        # Obtain the index of the movies that matches the users
        indices = self.generate_indicies(usersIds)

        # Calculate cosine similarity (or extract it from file)
        cosine_similarity = self.calculate_cosine_similarity()

        # Get the pairwise similarity scores of all movies with the movies
        # And convert it into a list of list of tuples
        sim_scores = [list(enumerate(cosine_similarity[i])) for i in indices]

        # Sort the movies based on the cosine similarity scores
        sim_scores = [sorted(sim_scores[i], key=lambda x: x[1], reverse=True) for i in range(len(sim_scores))]

        # Get the scores of the 3 most similar movies. Ignore the first movie.
        sim_scores = [sim_scores[i][1:self.top_movies] for i in range(len(sim_scores))]

        # Get the movie indices
        movie_indices = [i[0] for sim_score in sim_scores for i in sim_score]

        return movie_indices

    def hybrid(self, usersIds):
        """ Apply the SVD to the content based filtered movies """

        # Get movies from content based filtering
        movie_indices = self.content_based_recommender(usersIds)

        # Extract the metadata of the aforementioned movies
        # metadata = ['title', 'vote_count', 'vote_average', 'year', 'id']
        movies = self.clean_dataframe.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year', 'id']]

        # Compute the predicted ratings using the SVD filter
        movies['est'] = movies['id'].apply(lambda x: self.predict(usersIds, int(x)))

        # Sort the movies in decreasing order of predicted rating
        movies = movies.sort_values('est', ascending=False)

        # Return the top 10 movies as recommendations
        return movies.head(10)

    def predict(self, users, movieId):
        """ SVD prediction per set of users on a selected movie (movieId)"""

        # This piece of code escapes the not found movieId
        try:
            title = self.id_to_title.loc[movieId]['title']
        except:
            title = ''

        # Return the mean value of svd prediction for all the selected users
        return mean([self.svd.predict(i, title).est for i in users])

