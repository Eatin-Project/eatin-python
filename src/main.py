import os
from sys import platform

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from src.api.schema import schema
from src.recommendations.models.tf_idf import calc_model

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_headers=["*"], allow_origins=["http://localhost:3000"], allow_methods=["*"]
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

    calc_model()


app.include_router(graphql_app, prefix="/graphql")
