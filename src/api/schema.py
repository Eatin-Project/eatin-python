import typing

import strawberry

from src.api.models.model import Section
from src.recommendations.recommender import Recommender


def get_sections():
    return Recommender.get_sections(Recommender(), 1)


@strawberry.type
class Query:
    sections: list[Section] = strawberry.field(resolver=get_sections)
# Recipe(index=1, recipe_title="bla", url="bla", record_health="bla", vote_count=1, rating=1, description="bla", cuisine="bla", course="bla", diet="bla", prep_time=1, cook_time=1, ingredients="bla", instructions="bla", author="bla", tags="bla", category="bla", image="bla", difficulty="bla", total_time=1)
