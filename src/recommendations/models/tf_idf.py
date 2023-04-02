import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.infra.postgres_connector import get_df_from
from src.recommendations.consts import ALL_RECIPES_QUERY, RECIPE_COLUMNS, GET_USER_TOP_RATED_RECIPES_QUERY, \
    RECIPE_AMOUNT


FILENAME = 'notebooks/tf_idf.joblib'


# TODO: This model receives a recipe title (I think I can change it to recipe index),
#       and returns the top 12 recipes that has the most similar description, using tf-idf.
#       I suppose there are several ways to get the recipe title. Currently, I will do:
#       1. get all of the user's ratings from the ratings table.
#       2. get the top X recipes with the highest rating
#       3. run the model on each recipe
#       4. combine the results and drop duplicates
def generate_tf_idf_recommendations(user_id):
    all_recipes = get_df_from(ALL_RECIPES_QUERY, RECIPE_COLUMNS)
    cosine_similarity_matrix = _load_model()
    user_liked_recipes_df = get_df_from(GET_USER_TOP_RATED_RECIPES_QUERY.format(user_id, RECIPE_AMOUNT),
                                        ['recipe_title'])

    return [_build_section(recipe_title, all_recipes, cosine_similarity_matrix, index + 1) for index, recipe_title in
            enumerate(user_liked_recipes_df['recipe_title'])]


def _load_model():
    # TODO: when saving the model in a data structure, the load it from it
    return joblib.load(FILENAME)


def _process_text(text):
    text = ' '.join(text.split())
    text = text.lower()

    return text


def _index_from_title(df, title):
    return df[df['recipe_title'] == title].index.values[0]


def _title_from_index(df, index):
    return df[df.index == index].recipe_title.values[0]


def _recommendations(recipe_title, df, cosine_similarity_matrix, number_of_recommendations):
    index = _index_from_title(df, recipe_title)
    similarity_scores = list(enumerate(cosine_similarity_matrix[index]))
    similarity_scores_sorted = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommendations_indices = [t[0] for t in similarity_scores_sorted[1:(number_of_recommendations + 1)]]

    return df.iloc[recommendations_indices]


def _build_section(recipe_title, all_recipes, cosine_similarity_matrix, rank):
    df = _recommendations(recipe_title, all_recipes, cosine_similarity_matrix, 12)
    recipes_json = json.loads(df.to_json(orient='records'))

    return {'name': 'Because You Liked {}'.format(recipe_title), 'recipes': recipes_json, 'rank': rank}


def _calc_model(all_recipes):
    df = all_recipes[all_recipes['description'].notna()]
    df['description'] = df.apply(lambda x: _process_text(x.description), axis=1)

    tf_idf = TfidfVectorizer(stop_words='english')
    tf_idf_matrix = tf_idf.fit_transform(df['description'])
    cosine_similarity_matrix = cosine_similarity(tf_idf_matrix, tf_idf_matrix)

    joblib.dump(cosine_similarity_matrix, FILENAME)
