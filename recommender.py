import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tag_transformer(df, path):
    for i, row in df.iterrows():
        df.loc[i, 'tags'] = f'{row.tag_1}, {row.tag_2}'
    df.pop('Unnamed: 0')
    df.pop('tag_1')
    df.pop('tag_2')
    df.to_csv(path)


def create_tags(x):
    tags = x['tags'].lower().split(', ')
    tags.extend(x['food_title'].lower().split())
    #tags.extend(x['category'].lower().split())
    return " ".join(sorted(set(tags), key=tags.index))


def create_coin_sim(df):
    count = CountVectorizer(stop_words=['english', 'z', 'ze', 'w', 'i', 'na', 'zupa'])
    count_matrix = count.fit_transform(df['tager'])
    return cosine_similarity(count_matrix, count_matrix)


def get_recommendations(cosine_sim, idx=-1):
    # Get the pairwsie similarity scores of all dishes with that dish
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the dishes based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar dishes
    sim_scores = sim_scores[1:3]

    # Get the food indices
    food_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar dishes
    return food_indices


df1 = pd.read_csv('db/dania_glowne_database.csv')
df1['tager'] = df1.apply(create_tags, axis=1)
indices_from_food_id = pd.Series(df1.index, index=df1['food_id'])
