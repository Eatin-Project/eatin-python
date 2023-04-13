def recommendations(df, cosine_similarity_matrix, number_of_recommendations, recipe_title=None, recipe_index=None):
    index = _df_index_from_recipe_index(df, recipe_index) \
        if recipe_index is not None else _index_from_title(df, recipe_title)

    similarity_scores = list(enumerate(cosine_similarity_matrix[index]))
    similarity_scores_sorted = [score for score in sorted(similarity_scores, key=lambda x: x[1], reverse=True) if score[0] != index]
    recommendations_indices = [score[0] for score in similarity_scores_sorted[1:(number_of_recommendations + 1)]]

    return df.iloc[recommendations_indices]


def _index_from_title(df, title):
    return df[df['recipe_title'] == title].index.values[0]


def _df_index_from_recipe_index(df, recipe_index):
    return df[df['index'] == recipe_index].index.values[0]


def title_from_index(df, index):
    return df[df['index'] == index].recipe_title.values[0]
