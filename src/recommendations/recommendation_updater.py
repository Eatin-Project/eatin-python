import json

from src.infra.postgres_connector import execute_insert, connect
from src.recommendations.recommender import get_recipes_sections

QUERY = """
        INSERT INTO userrecommendations(user_id, recommendations)
        VALUES (%s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET recommendations = excluded.recommendations
    """


def update_recommendations(user_id):
    conn = connect()
    recommendations = get_recipes_sections(conn, user_id)
    execute_insert(conn, QUERY, (user_id, json.dumps(recommendations)))
    conn.close()
    
    return user_id


