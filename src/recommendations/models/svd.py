import json

import joblib
import pandas as pd
from surprise import SVD, Dataset, Reader

from src.infra.postgres_connector import get_df_from
from src.recommendations.consts import SVD_FILE_LOCATION, RATINGS_PARQUET_LOCATION, RECIPES_BY_INDEXES_QUERY, \
    UPDATED_RECIPE_COLUMNS


def generate_svd_recommendations(user_id, conn, recipes_df):
    ratings_df = pd.read_parquet(RATINGS_PARQUET_LOCATION)

    algo = _load_model()

    recipes_not_rated_by_user = \
        ratings_df[~ratings_df['recipe_index'].isin(ratings_df[ratings_df['user_id'] == user_id]['recipe_index'])][
            'recipe_index']

    recipe_predictions = []
    for recipe_id in recipes_not_rated_by_user.unique():
        predicted_rating = algo.predict(user_id, recipe_id).est
        recipe_predictions.append((predicted_rating, recipes_df[recipes_df['index'] == recipe_id]))

    recipe_predictions.sort(key=lambda x: x[0], reverse=True)
    indexes = [int(recipe[1].index[0]) for recipe in recipe_predictions]

    return [{'name': 'Other Users Liked',
             'recipes': json.loads(
                 get_df_from(RECIPES_BY_INDEXES_QUERY.format(user_id, tuple(indexes)), UPDATED_RECIPE_COLUMNS,
                             conn).to_json(orient='records')),
             'rank': 3}]


def calc_svd_model():
    print('calculating svd')
    ratings_df = pd.read_parquet(RATINGS_PARQUET_LOCATION)

    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(ratings_df[['user_id', 'recipe_index', 'rating']], reader)

    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)
    joblib.dump(algo.fit(trainset), SVD_FILE_LOCATION)

    print('finished calculating svd')


def _load_model():
    return joblib.load(SVD_FILE_LOCATION)
