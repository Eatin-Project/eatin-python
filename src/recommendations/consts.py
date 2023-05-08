import json
import os

import pandas as pd

RECIPE_AMOUNT = 13
COLD_START_RATING_AMOUNT = 3
RATING_LOWER_BOUND = 3.5

COUNT_USER_RATINGS_QUERY = "select count(*) from ratings where user_id = '{}'"
ALL_RECIPES_QUERY = "select * from recipes"
ALL_RATINGS_QUERY = "select * from ratings;"
USER_RATINGS_COLUMNS = ['user_id', 'recipe_index', 'rating', 'rating_timestamp']
GET_USER_TOP_RATED_RECIPES_QUERY = "select recipes.recipe_title from ratings, recipes \
                                        where ratings.user_id = '{}' \
                                        and ratings.recipe_index = recipes.index \
                                        and ratings.rating >= {} \
                                        order by ratings.rating_timestamp desc, ratings.rating desc \
                                        limit {}"

MOST_POPULAR_QUERY = "select index, recipe_title, url, record_health, vote_count, rating, description, cuisine, course,\
                  diet, prep_time, cook_time, ingredients, instructions, author, tags, category, image, difficulty, \
                  total_time, \
  case when userrecipes.is_saved is NULL then false else userrecipes.is_saved end as is_saved,\
 case when userrecipes.is_uploaded is NULL then false else userrecipes.is_uploaded end as is_uploaded,\
 case when userrecipes.given_comment is NULL then '' else userrecipes.given_comment end as given_comment \
                  from recipes \
                    left outer join userrecipes on recipes.index = userrecipes.recipe_index and userrecipes.user_id = '{}' \
                    order by vote_count desc, rating desc limit 20;"

TOP_RECIPES_FOR_CATEGORY_QUERY = "select index, recipe_title, url, record_health, vote_count, rating, description, cuisine,\
                                 course, diet, prep_time, cook_time, ingredients, instructions,\
                                  author, tags, category, image, difficulty, total_time, \
  case when userrecipes.is_saved is NULL then false else userrecipes.is_saved end as is_saved,\
 case when userrecipes.is_uploaded is NULL then false else userrecipes.is_uploaded end as is_uploaded,\
 case when userrecipes.given_comment is NULL then '' else  userrecipes.given_comment end as given_comment \
                                 from recipes \
left outer join userrecipes on recipes.index = userrecipes.recipe_index and userrecipes.user_id = '{}'\
where category = '{}'\
order by (vote_count * rating) desc \
limit 20;"

RECIPES_BY_INDEXES_QUERY = "select index, recipe_title, url, record_health, vote_count, rating, description, cuisine,\
                                 course, diet, prep_time, cook_time, ingredients, instructions,\
                                  author, tags, category, image, difficulty, total_time, \
  case when userrecipes.is_saved is NULL then false else userrecipes.is_saved end as is_saved,\
 case when userrecipes.is_uploaded is NULL then false else userrecipes.is_uploaded end as is_uploaded,\
 case when userrecipes.given_comment is NULL then '' else  userrecipes.given_comment end as given_comment \
                                 from recipes \
left outer join userrecipes on recipes.index = userrecipes.recipe_index and userrecipes.user_id = '{}'\
where recipes.index in {}"

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

SAVED_RECIPES_QUERY = "select  index, recipe_title, url, record_health, vote_count, rating, description, cuisine,\
                                 course, diet, prep_time, cook_time, ingredients, instructions,\
                                  author, tags, category, image, difficulty, total_time\
                                     from userrecipes \
                                     left outer join recipes on index = recipe_index\
                            where userrecipes.user_id = '{}' and userrecipes.is_saved = '{}'"

UPLOADED_RECIPES_QUERY = "select  index, recipe_title, url, record_health, vote_count, rating, description, cuisine,\
                                 course, diet, prep_time, cook_time, ingredients, instructions,\
                                  author, tags, category, image, difficulty, total_time\
                                     from userrecipes \
                                     left outer join recipes on index = recipe_index\
                            where userrecipes.user_id = '{}' and userrecipes.is_uploaded = '{}'"

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

UPDATED_RECIPE_COLUMNS = ['index',
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
                          'given_comment']

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
