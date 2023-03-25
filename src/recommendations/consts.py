RECIPE_AMOUNT = 3
COLD_START_RATING_AMOUNT = 3

COUNT_USER_RATINGS_QUERY = "select count(*) from ratings where user_id = '{}'"
ALL_RECIPES_QUERY = "select * from recipes"
USER_RATINGS_COLUMNS = ['user_id', 'recipe_id', 'rating']
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
