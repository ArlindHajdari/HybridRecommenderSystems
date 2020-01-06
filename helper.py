import pandas as pd
import numpy as np
from ast import literal_eval


# Helper function to convert NaN to 0 and all other years to integers.
def convert_int(x):
    try:
        return int(x)
    except:
        return 0


def clean_dataset(full_dataset_path="../data/movies_metadata.csv"):
    full_dataset = pd.read_csv(full_dataset_path)

    # Only keep those features that we require
    full_dataset = full_dataset[['title', 'genres', 'release_date', 'runtime', 'vote_average', 'vote_count']]

    # Convert release_date into pandas datetime format
    full_dataset['release_date'] = pd.to_datetime(full_dataset['release_date'], errors='coerce')

    # Extract year from the datetime
    full_dataset['year'] = full_dataset['release_date'].apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

    # Apply convert_int to the year feature
    full_dataset['year'] = full_dataset['year'].apply(self.convert_int)

    # Drop the release_date column
    full_dataset = full_dataset.drop('release_date', axis=1)

    # Convert all NaN into stringified empty lists
    full_dataset['genres'] = full_dataset['genres'].fillna('[]')

    # Apply literal_eval to convert stringified empty lists to the list object
    full_dataset['genres'] = full_dataset['genres'].apply(literal_eval)

    # Convert list of dictionaries to a list of strings
    full_dataset['genres'] = full_dataset['genres'].apply(lambda x: [i['name'].lower() for i in x] if isinstance(x, list) else [])

    return full_dataset


def read_in_chunks(file_object, chunk_size=1024):
    """ Read the file in chunks (for big files) """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data