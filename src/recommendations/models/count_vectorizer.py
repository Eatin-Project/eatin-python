import json

import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.recommendations.consts import COUNT_VECTORIZER_FILE_LOCATION
from src.recommendations.models.base import recommendations, title_from_index

w_ingredients = 10
w_record_health = 2
w_course = 1
w_cuisine = 10
w_diet = 3
w_prep_time = 7
w_cook_time = 7
w_category = 13
w_difficulty = 4
w_tags = 15


def concatenate_features(df_row):
    return ' '.join([df_row['record_health']] * w_record_health) + ' ' + \
        ' '.join([df_row['cuisine']] * w_cuisine) + ' ' + \
        ' '.join([df_row['course']] * w_course) + ' ' + \
        ' '.join([df_row['diet']] * w_diet) + ' ' + \
        ' '.join([df_row['ingredients']] * w_ingredients) + ' ' + \
        ' '.join(str([df_row['prep_time']]) * w_prep_time) + ' ' + \
        ' '.join(str([df_row['cook_time']]) * w_cook_time) + ' ' + \
        ' '.join([df_row['category']] * w_category) + ' ' + \
        ' '.join([df_row['difficulty']] * w_difficulty) + ' ' + \
        ' '.join([df_row['tags']] * w_tags)


def return_values(value):
    values = []
    if value is not None:
        values.append(value.lower().replace(" ", ""))

    return ' '.join(values)


def return_list_values(value):
    values = []
    if value is not None:
        for item in value:
            values.append(item.lower().replace(" ", ""))

    return ' '.join(values)


def convert_values(df):
    df['record_health'] = df.apply(lambda x: return_values(x.record_health), axis=1)
    df['cuisine'] = df.apply(lambda x: return_values(x.cuisine), axis=1)
    df['course'] = df.apply(lambda x: return_values(x.course), axis=1)
    df['diet'] = df.apply(lambda x: return_values(x.diet), axis=1)
    df['category'] = df.apply(lambda x: return_values(x.category), axis=1)
    df['difficulty'] = df.apply(lambda x: return_values(x.difficulty), axis=1)
    df['tags'] = df.apply(lambda x: return_list_values(x.tags), axis=1)
    df['ingredients'] = df.apply(lambda x: return_list_values(x.ingredients), axis=1)


def process_text(text):
    text = ' '.join(text.split())
    text = text.lower()

    return text


def calc_count_vectorizer_model(all_recipes):
    print('calculating count vectorizer')
    df = all_recipes
    convert_values(df)
    df['features'] = df.apply(concatenate_features, axis=1)
    df['features'] = df.apply(lambda x: process_text(x.features), axis=1)

    vect = CountVectorizer(stop_words='english')
    vect_matrix = vect.fit_transform(df['features'])
    cosine_similarity_matrix = cosine_similarity(vect_matrix, vect_matrix)

    joblib.dump(cosine_similarity_matrix, COUNT_VECTORIZER_FILE_LOCATION)
    print('finished calculating count vectorizer')


def _load_model():
    return joblib.load(COUNT_VECTORIZER_FILE_LOCATION)


def generate_count_vectorizer_recommendations(recipe_index, all_recipes):
    cosine_similarity_matrix = _load_model()

    df = recommendations(title_from_index(all_recipes, recipe_index), all_recipes, cosine_similarity_matrix, 12)
    recipes_json = json.loads(df.to_json(orient='records'))

    return [{'name': 'Similar Recipes', 'recipes': recipes_json, 'rank': 0}]
