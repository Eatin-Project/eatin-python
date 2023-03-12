import strawberry
@strawberry.federation.type(keys=["index"])
class Recipes:
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


schema = strawberry.federation.Schema(
    enable_federation_2=True,
    types=[Recipes],
)