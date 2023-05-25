import os
from sys import platform

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from src.api.schema import schema
from src.infra.postgres_connector import connect, get_df_from
from src.recommendations.consts import get_recipes, RATINGS_PARQUET_LOCATION, ALL_RATINGS_QUERY, USER_RATINGS_COLUMNS
from src.recommendations.models.count_vectorizer import calc_count_vectorizer_model
from src.recommendations.models.svd import calc_svd_model
from src.recommendations.models.tf_idf import calc_tf_idf_model

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_headers=["*"], allow_origins=["http://localhost:3000", "http://eatin.cs.colman.ac.il:3000/"], allow_methods=["*"]
)


# TODO: I am not sure why this is not working
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "public,max-age=3600"
    return response


# TODO: remove this when we deploy on a server
@app.on_event("startup")
async def startup_event():
    if platform == "win32":
        os.chdir('../')

    conn = connect()
    ratings = get_df_from(ALL_RATINGS_QUERY, USER_RATINGS_COLUMNS, conn)
    ratings.to_parquet(RATINGS_PARQUET_LOCATION, compression='gzip')
    conn.close()

    all_recipes = get_recipes()
    calc_count_vectorizer_model(all_recipes)
    calc_svd_model()
    calc_tf_idf_model(all_recipes)


app.include_router(graphql_app, prefix="/graphql")
