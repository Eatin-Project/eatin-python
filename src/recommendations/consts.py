from enum import Enum
import json
import os

import pandas as pd

RECIPE_AMOUNT = 3
COLD_START_RATING_AMOUNT = 3

COUNT_USER_RATINGS_QUERY = "select count(*) from ratings where user_id = '{}'"
ALL_RECIPES_QUERY = "select * from recipes"
ALL_RATINGS_QUERY = "select * from ratings;"
USER_RATINGS_COLUMNS = ['user_id', 'recipe_index', 'rating', 'rating_timestamp']
GET_USER_TOP_RATED_RECIPES_QUERY = "select recipes.recipe_title from ratings, recipes \
                                        where ratings.user_id = '{}' \
                                        and ratings.recipe_index = recipes.index \
                                        order by ratings.rating desc \
                                        limit {}"

MOST_POPULAR_QUERY = "select * from recipes order by vote_count desc, rating desc limit 20;"

POPULARITY = "(0.4 * SUM(vote_count) + 0.4 * AVG(rating) + 0.2 * COUNT(*))"

TOP_CATEGORIES_QUERY = "SELECT \
  category, \
  COUNT(*) AS recipe_count, \
  SUM(vote_count) AS total_votes, \
  AVG(rating) AS average_rating, \
  {0} AS popularity_score, \
  ROW_NUMBER () OVER (ORDER BY {0} desc) as row_num \
FROM recipes \
GROUP BY category \
ORDER BY popularity_score DESC \
LIMIT 10;".format(POPULARITY)


TOP_RECIPES_FOR_CATEGORY_QUERY = "select * from recipes \
where category = '{}' \
order by (vote_count * rating) desc \
limit 20;"

USER_RECIPES_CONNECTION_QUERY = "select user_id, is_saved, is_uploaded, given_comment from userrecipes \
where recipe_index = '{}' "


RECIPES_BY_IS_SAVED_QUERY = "select is_saved, is_uploaded, given_comment, index, recipe_title, url, \
                                     record_health, vote_count, rating, description, cuisine, course, diet, prep_time, \
                                     cook_time, ingredients, instructions, author, tags, category, image, difficulty, \
                                     total_time  \
                                     from userrecipes \
                                     where user_id = '{}' where is_saved = '{}'\
                                     inner join recipes on index = recipe_index"

RECIPES_BY_IS_UPLOADED_QUERY = "select is_saved, is_uploaded, given_comment, index, recipe_title, url, \
                                     record_health, vote_count, rating, description, cuisine, course, diet, prep_time, \
                                     cook_time, ingredients, instructions, author, tags, category, image, difficulty, \
                                     total_time  \
                                     from userrecipes \
                                     where user_id = '{}' where is_uploaded = '{}' \
                                     inner join recipes on index = recipe_index"

RECIPES_BY_COMMENT_EXISTS_QUERY = "select is_saved, is_uploaded, given_comment, index, recipe_title, url, \
                                     record_health, vote_count, rating, description, cuisine, course, diet, prep_time, \
                                     cook_time, ingredients, instructions, author, tags, category, image, difficulty, \
                                     total_time  \
                                     from userrecipes \
                                     where user_id = '{}' where len(given_comment) '{}' \
                                     inner join recipes on index = recipe_index"


TOP_CATEGORIES_COLUMNS = ['category', 'recipe_count', 'total_votes', 'average_rating', 'popularity_score', 'row_num']

RECIPE_COLUMNS = ['index',
                  'recipe_title',
                  'url',
                  'record_health',
                  'vote_count',
                  'rating',
                  'description',
                  'cuisine',
                  'course',
                  'diet',
                  'prep_time',
                  'cook_time',
                  'ingredients',
                  'instructions',
                  'author',
                  'tags',
                  'category',
                  'image',
                  'difficulty',
                  'total_time']

USER_RECIPE_CONNECTION_COLUMNS = [
    'user_id',
    'is_saved',
    'is_uploaded',
    'given_comment'
]

USER_RECIPE_WITH_FULL_RECIPE_COLUMNS = [
    'index',
     'recipe_title',
     'url',
     'record_health',
     'vote_count',
     'rating',
    'description',
     'cuisine',
     'course',
     'diet',
     'prep_time',
     'cook_time',
    'ingredients',
    'instructions',
    'author',
    'tags',
    'category',
    'image',
    'difficulty',
    'total_time',
    'is_saved',
    'is_uploaded',
    'given_comment'
]


TF_IDF_FILE_LOCATION = os.path.join('models', 'tf_idf.joblib')
COUNT_VECTORIZER_FILE_LOCATION = os.path.join('models', 'count-vectorizer.joblib')
RECIPES_PARQUET_LOCATION = os.path.join('dataset', 'recipes.parquet.gzip')
SVD_FILE_LOCATION = os.path.join('models', 'svd.joblib')
RATINGS_PARQUET_LOCATION = os.path.join('dataset', 'ratings.parquet.gzip')


def get_recipes():
    all_recipes = pd.read_parquet(RECIPES_PARQUET_LOCATION).reset_index()
    all_recipes['ingredients'] = [json.dumps(ingredient.tolist()) for ingredient in all_recipes['ingredients']]
    all_recipes['instructions'] = [json.dumps(instruction.tolist()) for instruction in all_recipes['instructions']]
    all_recipes['tags'] = [json.dumps(tag.tolist()) for tag in all_recipes['tags']]

    return all_recipes


