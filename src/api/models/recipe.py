import typing
import strawberry


@strawberry.type
class Recipe:
    index: int
    recipe_title: str
    url: str
    record_health: str
    vote_count: int
    rating: float
    description: str
    cuisine: str
    course: str
    diet: str
    prep_time: int
    cook_time: int
    ingredients: str
    instructions: str
    author: str
    tags: str
    category: str
    image: str
    difficulty: str
    total_time: int


@strawberry.type
class UpdatedRecipe(Recipe):
    is_saved: bool
    is_uploaded: bool
    given_comment: str


@strawberry.type
class Section:
    name: str
    recipes: typing.List[UpdatedRecipe]
