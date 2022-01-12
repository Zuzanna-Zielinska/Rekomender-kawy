import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

'''
Funkcja robocza do usunięcia do koniec projektu
'''
def tag_transformer(df, path):
    for i, row in df.iterrows():
        df.loc[i, 'tags'] = f'{row.tag_1}, {row.tag_2}'
    df.pop('Unnamed: 0')
    df.pop('tag_1')
    df.pop('tag_2')
    df.to_csv(path)

'''
Funkcja tworząca tagi oddzielone spacją od siebie, wymagają tego funkcje używane w programie
'''
def create_tags(x):
    tags = x['tags'].lower().split(', ')
    tags.extend(x['food_title'].lower().split())
    return " ".join(sorted(set(tags), key=tags.index))


def create_coin_sim(df):
    count = CountVectorizer(stop_words=['english', 'z', 'ze', 'w', 'i', 'na', 'zupa'])
    count_matrix = count.fit_transform(df['tager'])
    return cosine_similarity(count_matrix, count_matrix)

'''
Funkcja oceniająca potrawy na podstawie ocen i wpisująca je do df
'''
def score_rec(df):
    m = df['num_rating'].quantile(0.6)
    C = df['avg_rating'].mean()

    def weighted_rating(x, m=m, C=C):
        v = x['num_rating']
        R = x['avg_rating']
        return (v / (v + m) * R) + (m / (m + v) * C)

    df['tager'] = df.apply(create_tags, axis=1)
    df['score'] = df.apply(weighted_rating, axis=1)
    return df

'''
Funkcja wyliczająca ilość tagów zgodnych z tagami usera i wpisująca je do df
'''
def pref_rec(df, user):
    user_pref = user['preferences']

    def bonus_pref(x, user_pref=user_pref):
        counter = 0
        for pref in user_pref[0].split(' '):
            if pref in x['tager'].split(' '):
                counter += 1
        return counter

    df['pref_count'] = df.apply(bonus_pref, axis=1)

'''
W tej funkcji wywoływane są wszystkie funkcje rekomendujące oraz oceniane są potrawy i sortowane
'''
def recommendation_engine(df, user_df, user_id, diets_df):
    user = user_df.loc[user_df['user_id'] == user_id]
    score_rec(df)
    pref_rec(df, user)

    if user.liked_diets[0] != np.NAN:
        cos_sim = create_coin_sim(df)
        indices_from_food_id = pd.Series(df.index, index=df['food_id'])
        for diet_id in user['liked_diets']:
            diet = diets_df.loc[diets_df['diet_id'] == diet_id]
            sniadanie = diet['śniadanie']
            zupa = diet['zupa']
            obiad = diet['obiad']
            kolacja = diet['kolacja']
    else:
        return df


'''
Funkcja zwracać będzie listę z rekomendacjami, albo słownik zależy co wolicie,
wywoływana przy przejściu na ekran rekomendacji
'''
def get_recommendation(df_list, user_df, user_id, diets_df):
    for df in df_list:
        rec = recommendation_engine(df, user_df, user_id, diets_df)

    pass


df1 = pd.read_csv('db/sniadania_database.csv')
df2 = pd.read_csv('db/dania_glowne_database.csv')
df3 = pd.read_csv('db/zupy_database.csv')

users_df = pd.read_csv('db/users.csv')
liked_diet_df = pd.read_csv('db/liked_diets.csv')
df_ls = [df1, df2, df3]
get_recommendation(df_ls, users_df, 1, liked_diet_df)
q_it = recommendation_engine(df1, users_df, 1, liked_diet_df)
