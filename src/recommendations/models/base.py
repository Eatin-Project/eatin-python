def recommendations(df, cosine_similarity_matrix, number_of_recommendations, recipe_title=None, recipe_index=None):
    index = recipe_index if recipe_index is not None else _index_from_title(df, recipe_title)
    similarity_scores = list(enumerate(cosine_similarity_matrix[index]))
    similarity_scores_sorted = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommendations_indices = [t[0] for t in similarity_scores_sorted[1:(number_of_recommendations + 1)]]

    return df.iloc[recommendations_indices]


def _index_from_title(df, title):
    return df[df['recipe_title'] == title].index.values[0]


def title_from_index(df, index):
    return df[df['index'] == index].recipe_title.values[0]
