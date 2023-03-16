import json

from src.infra.postgres_connector import connect, execute_select

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


def get_recipes_sections(user_id):
    if _needs_cold_start(user_id):
        return _get_cold_start_recipes(user_id)

    return _recommend_recipes(user_id)


def _needs_cold_start(user_id):
    # TODO: write cold start entering logic (e.g. if the user has less than X ratings)
    return True

    # TODO: 1. get the overall most popular (vote count + rating)
    #       2. sort the categories by popularity
    #           2.1 for each category -> get the most popular (vote count + rating)
    #       3. if there are other users in the DB
    #           3.1 do Count Vectorizer for the user metadata to find similar users
    #           3.2 get the other user's top rated recipes
    #       4. recommend recipes by the time of the day (0800 -> breakfast)


def _get_cold_start_recipes(user_id):
    query = "select * from recipes order by vote_count desc, rating desc limit 100;"
    conn = connect()
    df = execute_select(conn, query, RECIPE_COLUMNS)
    recipes_json = json.loads(df.to_json(orient='records'))
    recipes = [{'name': 'for_you', 'recipes': recipes_json[:13]},
               {'name': 'other', 'recipes': recipes_json[14:99]}]
    conn.close()

    return recipes


def _recommend_recipes(user_id):
    print('kaki')
