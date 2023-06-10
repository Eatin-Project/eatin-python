from src.infra.postgres_connector import connect, get_df_from, execute_select
from src.recommendations.consts import ALL_RATINGS_QUERY, USER_RATINGS_COLUMNS, RATINGS_PARQUET_LOCATION, \
    ALL_RECIPES_QUERY, RECIPE_COLUMNS, RECIPES_PARQUET_LOCATION
from src.recommendations.models.count_vectorizer import calc_count_vectorizer_model
from src.recommendations.models.svd import calc_svd_model
from src.recommendations.models.tf_idf import calc_tf_idf_model


def calculate_recommendation_models():
    conn = connect()
    ratings = get_df_from(ALL_RATINGS_QUERY, USER_RATINGS_COLUMNS, conn)
    ratings.to_parquet(RATINGS_PARQUET_LOCATION, compression='gzip')
    recipes = execute_select(conn, ALL_RECIPES_QUERY, RECIPE_COLUMNS)
    recipes.to_parquet(RECIPES_PARQUET_LOCATION, compression='gzip')
    conn.close()

    all_recipes = recipes.reset_index()
    calc_count_vectorizer_model(all_recipes)
    calc_svd_model()
    calc_tf_idf_model(all_recipes)

