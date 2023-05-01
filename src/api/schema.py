import operator
import typing

import strawberry
from strawberry.schema.config import StrawberryConfig

from src.api.models.recipe import Section, FullSingleRecipeOfUser
from src.recommendations.recommender import get_recipes_sections,\
    get_similar_recipes,\
    get_recipes_with_connection_by_is_saved,\
    get_recipes_with_connection_by_given_comment,\
    get_recipes_with_connection_by_is_uploaded


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


def recipes_with_connection_by_is_saved_resolver(user_id: str, is_saved: bool) ->\
        typing.List[FullSingleRecipeOfUser]:
    return get_recipes_with_connection_by_is_saved(user_id, is_saved)


def recipes_with_connection_by_is_uploaded_resolver(user_id: str, is_uploaded: bool) ->\
        typing.List[FullSingleRecipeOfUser]:
    return get_recipes_with_connection_by_is_uploaded(user_id, is_uploaded)


def recipes_with_connection_by_comment_resolver(user_id: str, does_comment_exist: bool) ->\
        typing.List[FullSingleRecipeOfUser]:
    return get_recipes_with_connection_by_given_comment(user_id, does_comment_exist)


def similar_recipes_resolver(recipe_index: int) -> typing.List[Section]:
    return get_similar_recipes(recipe_index)


@strawberry.type
class Query:
    sections: typing.List[Section] = strawberry.field(resolver=sections_resolver)
    similar_recipes: typing.List[Section] = strawberry.field(resolver=similar_recipes_resolver)
    recipes_connection_is_saved = strawberry.field(resolver=recipes_with_connection_by_is_saved_resolver)
    recipes_connection_is_uploaded = strawberry.field(resolver=recipes_with_connection_by_is_uploaded_resolver)
    recipes_connection_comment = strawberry.field(resolver=recipes_with_connection_by_comment_resolver)


schema = strawberry.Schema(query=Query, config=config)
