import json
import math

from src.infra.postgres_connector import connect, execute_select, get_df_from
from src.recommendations.consts import MOST_POPULAR_QUERY, RECIPE_COLUMNS, TOP_CATEGORIES_QUERY, TOP_CATEGORIES_COLUMNS, \
    TOP_RECIPES_FOR_CATEGORY_QUERY, COUNT_USER_RATINGS_QUERY, COLD_START_RATING_AMOUNT
from src.recommendations.models.tf_idf import generate_tf_idf_recommendations


def get_recipes_sections(user_id):
    if _needs_cold_start(user_id):
        return _get_cold_start_recipes(user_id)

    recipes = _recommend_recipes(user_id) + _get_cold_start_recipes(user_id)
    recipes.sort(key=get_rank)

    return recipes


def get_rank(element):
    return element['rank']


def _needs_cold_start(user_id):
    df = get_df_from(COUNT_USER_RATINGS_QUERY.format(user_id), ['count'])

    return df[df['count'] >= COLD_START_RATING_AMOUNT].empty

    # TODO: 1. get the overall most popular (vote count + rating)
    #       2. sort the categories by popularity
    #           2.1 for each category -> get the most popular (vote count + rating)
    #       3. if there are other users in the DB
    #           3.1 do Count Vectorizer for the user metadata to find similar users
    #           3.2 get the other user's top rated recipes
    #       4. recommend recipes by the time of the day (0800 -> breakfast)


def _get_cold_start_recipes(user_id):
    conn = connect()
    most_popular_df = execute_select(conn, MOST_POPULAR_QUERY, RECIPE_COLUMNS)
    top_categories_df = execute_select(conn, TOP_CATEGORIES_QUERY,
                                       TOP_CATEGORIES_COLUMNS)
    category_sections = [_create_sections_of(category.category, _get_rank(len(top_categories_df), category.row_num)
                                             , conn) for category in top_categories_df.itertuples()]
    recipes_json = json.loads(most_popular_df.to_json(orient='records'))
    popular_section = [{'name': 'Popular On Eatin', 'recipes': recipes_json, 'rank': 0}]
    conn.close()

    return popular_section + category_sections


def _get_rank(length, row):
    chunk = math.ceil(length / 2.99)
    return (row / chunk) // 1 + 1


def _create_sections_of(category, rank, conn):
    df = execute_select(conn, TOP_RECIPES_FOR_CATEGORY_QUERY.format(category), RECIPE_COLUMNS)
    recipes_json = json.loads(df.to_json(orient='records'))
    return {'name': category, 'recipes': recipes_json, 'rank': int(rank)}


def _recommend_recipes(user_id):
    return generate_tf_idf_recommendations(user_id)
