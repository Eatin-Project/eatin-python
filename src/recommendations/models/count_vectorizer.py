import json

import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.infra.postgres_connector import connect
from src.recommendations.consts import COUNT_VECTORIZER_FILE_LOCATION
from src.recommendations.models.content_based import recommendations

w_ingredients = 10
w_instructions = 2
w_record_health = 2
w_course = 1
w_cuisine = 10
w_diet = 3
w_prep_time = 7
w_cook_time = 7
w_category = 13
w_difficulty = 4
w_tags = 15
w_title = 15


def calc_count_vectorizer_model(all_recipes):
    print('calculating count vectorizer')
    df = all_recipes[~all_recipes['url'].str.contains("in-hindi")].reset_index(drop=True)
    df = _convert_values(df)
    df['features'] = df.apply(_concatenate_features, axis=1)
    df['features'] = df['features'].apply(_process_text)

    vect = CountVectorizer(stop_words='english')
    vect_matrix = vect.fit_transform(df['features'])
    cosine_similarity_matrix = cosine_similarity(vect_matrix, vect_matrix)

    joblib.dump(cosine_similarity_matrix, COUNT_VECTORIZER_FILE_LOCATION)
    print('finished calculating count vectorizer')


def generate_count_vectorizer_recommendations(recipe_index, all_recipes, user_id):
    cosine_similarity_matrix = _load_model()
    recipes_without_hindi = all_recipes[
        ~all_recipes['url'].str.contains("in-hindi")].reset_index(drop=True)

    conn = connect()
    df = recommendations(recipes_without_hindi, cosine_similarity_matrix, 20, user_id, conn, recipe_index=recipe_index)
    conn.close()
    recipes_json = json.loads(df.to_json(orient='records'))

    return [{'name': 'Similar Recipes', 'recipes': recipes_json, 'rank': 0}]


def _concatenate_features(df_row):
    return ' '.join([df_row['record_health']] * w_record_health) + ' ' + \
        ' '.join([df_row['cuisine']] * w_cuisine) + ' ' + \
        ' '.join([df_row['course']] * w_course) + ' ' + \
        ' '.join([df_row['diet']] * w_diet) + ' ' + \
        ' '.join([df_row['ingredients']] * w_ingredients) + ' ' + \
        ' '.join([df_row['instructions']] * w_instructions) + ' ' + \
        ' '.join(str([df_row['prep_time']]) * w_prep_time) + ' ' + \
        ' '.join(str([df_row['cook_time']]) * w_cook_time) + ' ' + \
        ' '.join([df_row['category']] * w_category) + ' ' + \
        ' '.join([df_row['difficulty']] * w_difficulty) + ' ' + \
        ' '.join([df_row['recipe_title']] * w_title) + ' ' + \
        ' '.join([df_row['tags']] * w_tags)


def _return_values(value):
    values = []
    if value is not None:
        values.append(value.lower().replace(" ", ""))

    return ' '.join(values)


def _return_list_values(value):
    values = []
    if value is not None:
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except ValueError:
                value = value.split()

        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    words = item.split()
                    for word in words:
                        values.append(word.lower().replace(" ", ""))

    return ' '.join(values)


def _convert_values(df):
    df = df.copy()
    df['record_health'] = df.apply(lambda x: _return_values(x.record_health), axis=1)
    df['recipe_title'] = df.apply(lambda x: _return_values(x.recipe_title), axis=1)
    df['cuisine'] = df.apply(lambda x: _return_values(x.cuisine), axis=1)
    df['course'] = df.apply(lambda x: _return_values(x.course), axis=1)
    df['diet'] = df.apply(lambda x: _return_values(x.diet), axis=1)
    df['category'] = df.apply(lambda x: _return_values(x.category), axis=1)
    df['difficulty'] = df.apply(lambda x: _return_values(x.difficulty), axis=1)
    df['tags'] = df.apply(lambda x: _return_list_values(x.tags), axis=1)
    df['ingredients'] = df.apply(lambda x: _return_list_values(x.ingredients), axis=1)
    df['instructions'] = df.apply(lambda x: _return_list_values(x.instructions), axis=1)

    return df


def _process_text(text):
    text = ' '.join(text.split())
    text = text.lower()

    return text


def _load_model():
    return joblib.load(COUNT_VECTORIZER_FILE_LOCATION)
