from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from api.schema import Query

schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
