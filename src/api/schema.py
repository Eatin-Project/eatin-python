import operator
import typing

import strawberry
from strawberry.schema.config import StrawberryConfig

from src.api.models.recipe import Section
from src.recommendations.recommender import get_recipes_sections, get_similar_recipes


def default_resolver(root, field):
    try:
        return operator.getitem(root, field)
    except KeyError:
        return getattr(root, field)


config = StrawberryConfig(
    default_resolver=default_resolver,
    auto_camel_case=False
)


def sections_resolver(user_id: str) -> typing.List[Section]:
    return get_recipes_sections(user_id)


def similar_recipes_resolver(recipe_index: int) -> typing.List[Section]:
    return get_similar_recipes(recipe_index)


@strawberry.type
class Query:
    sections: typing.List[Section] = strawberry.field(resolver=sections_resolver)
    similar_recipes: typing.List[Section] = strawberry.field(resolver=similar_recipes_resolver)


schema = strawberry.Schema(query=Query, config=config)
