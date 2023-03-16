import operator
import typing

import strawberry
from strawberry.schema.config import StrawberryConfig

from src.api.models.model import Section
from src.recommendations.recommender import get_recipes_sections


def default_resolver(root, field):
    try:
        return operator.getitem(root, field)
    except KeyError:
        return getattr(root, field)


config = StrawberryConfig(
    default_resolver=default_resolver
)


def sections_resolver(user_id: str) -> typing.List[Section]:
    print(user_id)
    return get_recipes_sections(user_id)


@strawberry.type
class Query:
    sections: typing.List[Section] = strawberry.field(resolver=sections_resolver)


schema = strawberry.Schema(query=Query, config=config)
