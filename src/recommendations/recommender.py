import json

from src.infra.postgres_connector import connect, execute_select

MOST_POPULAR_QUERY = "select * from recipes order by vote_count desc, rating desc limit 100;"

TOP_CATEGORIES_QUERY = "SELECT \
  category, \
  COUNT(*) AS recipe_count, \
  SUM(vote_count) AS total_votes, \
  AVG(rating) AS average_rating, \
  (0.4 * SUM(vote_count) + 0.4 * AVG(rating) + 0.2 * COUNT(*)) AS popularity_score \
FROM recipes \
GROUP BY category \
ORDER BY popularity_score DESC \
LIMIT 10;"

TOP_RECIPES_FOR_CATEGORY_QUERY = "select * from recipes \
where category = '{}' \
order by (vote_count * rating) desc \
limit 20;"


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
    conn = connect()
    most_popular_df = execute_select(conn, MOST_POPULAR_QUERY, RECIPE_COLUMNS)
    top_categories_df = execute_select(conn, TOP_CATEGORIES_QUERY,
                                       ['category', 'recipe_count', 'total_votes', 'average_rating', 'popularity_score'])
    category_sections = [create_sections_of(category, conn) for category in top_categories_df['category']]
    recipes_json = json.loads(most_popular_df.to_json(orient='records'))
    popular_section = [{'name': 'Popular On Eatin', 'recipes': recipes_json}]
    conn.close()

    return popular_section + category_sections


def create_sections_of(category, conn):
    df = execute_select(conn, TOP_RECIPES_FOR_CATEGORY_QUERY.format(category), RECIPE_COLUMNS)
    recipes_json = json.loads(df.to_json(orient='records'))
    section = {'name': category, 'recipes': recipes_json}
    return section


def _recommend_recipes(user_id):
    print('kaki')
