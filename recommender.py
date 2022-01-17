import pandas as pd
import numpy as np
import random as rd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

'''
Funkcja tworząca tagi oddzielone spacją od siebie, wymagają tego funkcje używane w programie

Przyjmuje:
    x - df z potrawami
'''
def create_tags(x):
    tags = x['tags'].lower().split(', ')
    tags.extend(x['food_title'].lower().split())
    return " ".join(sorted(set(tags), key=tags.index))

'''
Funkcja tworząca cosin similarity matrix od dań. Innymi słowy macierz podobieństw dań na podstawie tagów z nazw dań i smaku

Przyjmuje:
    df - df z potrawami
'''
def create_coin_sim(df):
    count = CountVectorizer(stop_words=['english', 'z', 'ze', 'w', 'i', 'na', 'zupa'])
    count_matrix = count.fit_transform(df['tager'])
    return cosine_similarity(count_matrix, count_matrix)

'''
Funkcja oceniająca potrawy na podstawie ocen i wpisująca je do df

Przyjmuje:
    df - df z potrawami
'''
def score_rec(df):
    m = df['num_rating'].quantile(0.6)
    C = df['avg_rating'].mean()

    def weighted_rating(x, m=m, C=C):
        v = x['num_rating']
        R = x['avg_rating']
        return (v / (v + m) * R) + (m / (m + v) * C)

    df['score'] = df.apply(weighted_rating, axis=1)
    return df

'''
Funkcja wyliczająca ilość tagów zgodnych z tagami usera i wpisująca je do df

Przyjmuje:
    df - df z potrawami
    user - aktualny użytkownik, wiersz z user.csv
'''
def pref_rec(df, user):
    user_pref = user['preferences']
    df['tager'] = df.apply(create_tags, axis=1)

    def bonus_pref(x, user_pref=user_pref):
        counter = 0
        for pref in str(user_pref.values[0]).split(' '):
            if pref in x['tager'].split(' '):
                counter += 1
        return counter

    df['pref_count'] = df.apply(bonus_pref, axis=1)

'''
Funkcja wyliczająca podobieństwo potrawy na podstawie wcześniej polubionych diet

Przyjmuje:
    df - df z potrawami
    user - aktywny użytkownik wiersz z user.csv
    diets_df - df z pliku liked_diets.csv
    category - aktualna kategoria dania
'''
def sim_scoring(df, user, diets_df, category):
    if not user.liked_diets.isnull().any():
        cos_sim = create_coin_sim(df)
        indices_from_food_id = pd.Series(df.index, index=df['food_id'])

        diet_ids = str(user['liked_diets'].values[0]).split()
        for i in diet_ids:
            diet_ids.append(int(float(diet_ids.pop(0))))
        diet = diets_df.loc[diets_df['diet_id'].isin(diet_ids).any() and diets_df['user_id'] == user['user_id'][0]]

        for cat in category:
            food_ids = diet[cat].values
            food_indices = []
            for i in food_ids:
                food_indices.append(indices_from_food_id[i])

            sim_scores = []
            for i in food_indices:
                sim_scores.append(list(cos_sim[i]))
            sim_scores = np.array(sim_scores)
            sim_scores = sim_scores.sum(axis=0)/len(food_indices)
            df[f'liked_sim_{cat}'] = sim_scores

'''
Funkcja  wylicza ocenę na podstawie wcześniej wyliczonych wartości

Przyjmuje:
    df - df z potrawami
    category - kategoria dań
    user - aktywny użytkownik wiersz z pliku user.csv
'''
def hybri_calculate(df, category, user):
    user_diets = user['liked_diets']
    cat = np.NAN

    def hybrid_scoring(x, user_diets=user_diets, category=cat):
        score = x['score']
        tags = x['pref_count']
        if not user_diets.isnull().any():
            sim_score = x[f'liked_sim_{cat}']
            weight = 1.07 ** len(str(user_diets.values).split()) - 0.5
        else:
            sim_score = 0
            weight = 0
        hybrid_score = (score / 10 * 3 + tags / 2 + sim_score * weight) / (4 + weight)
        return hybrid_score

    for cat in category:
        df[f'hybrid_score_{cat}'] = df.apply(hybrid_scoring, axis=1)

'''
W tej funkcji wywoływane są wszystkie funkcje rekomendujące oraz oceniane są potrawy i sortowane

Przyjmuje:
    df - df z potrawami
    user_df - df z user.csv
    user_id - id użytkownika aktywnego
    diets_df - df z liked_diets.csv
    category - kategoria dania
'''
def recommendation_engine(df, user_df, user_id, diets_df, category):
    user = user_df.loc[user_df['user_id'] == user_id]
    score_rec(df)
    pref_rec(df, user)
    sim_scoring(df, user, diets_df, category)
    hybri_calculate(df, category, user)
    if len(category) > 1:
        return df[['food_id', 'food_title', 'kcal', f'hybrid_score_{category[0]}', f'hybrid_score_{category[1]}']]
    else:
        return df[['food_id', 'food_title', 'kcal', f'hybrid_score_{category[0]}']]

'''
Funkcja, która napodstawie limitu kalorii oraz DataFramów posiłków losuje taki zestaw potraw, który spełnia limit.
W przypadku, kiedy nie może znaleźć kombinacji spełniającej limit zwraca flagę oraz zwiększa limit kalorii.

Przyjmuje:
    recommendations - lista df zawierających posortowane posiłki
    kcal_limit - limit kalorii
'''
def food_chooser(recomendations, kcal_limit):
    random_items = []
    flag = 0
    while True:
        recom_foods = []
        kcal_sum = 0
        for i, value in enumerate(recomendations):
            loc_idx = random_items.count(i)
            if i in [0, 1] and loc_idx > 49:
                loc_idx = 49
            elif i in [2, 3] and loc_idx > 99:
                loc_idx = 99
            recom_foods.append(value.loc[loc_idx])
            loc_idx -= loc_idx

        for i in recom_foods:
            kcal_sum += i['kcal']

        if kcal_limit - 500 < kcal_sum < kcal_limit:
            break

        if len(random_items) > 500:
            random_items = []
            kcal_limit += 100
            flag = 1
        random_items.append(rd.randint(0, 4))
    return recom_foods, kcal_sum, flag

'''
Funkcja zwracać będzie listę z rekomendacjami, albo słownik zależy co wolicie,
przyjmuje listę DataFramów w postaci [df_śniadanie, df_obiad, df_zupy]
wywoływana przy przejściu na ekran rekomendacji. Zwraca listę z Serii, które są 1 rzędem z DataFrame, która zawiera
food_id, food_title, kcal oraz hybrid_score_{category_name}. Lista ma układ [śniadanie, kolacja, obiad, zupa]
Zwraca  również sumę kalori posiłku oraz flagę, że limit kalorii ulagł zwiększeniu.

Przyjmuje:
    df_list - lista df w postaci [df_śniadanie, df_obiad, df_zupy]
    user_df - df od user.csv
    user_id - id użytkownika obecnie aktywnego
    diets_df - df od liked_diets.csv
    kcal_limit - limit kalorii
'''
def get_recommendation(df_list, user_df, user_id, diets_df, kcal_limit):
    recomendations = []
    category_dict = {0: ['śniadanie', 'kolacja'], 1: ['obiad'], 2: ['zupa'], 3: np.NAN}
    cat_id = 0

    for df in df_list:
        category = category_dict[cat_id]
        rec = recommendation_engine(df, user_df, user_id, diets_df, category)
        cat_id += 1

        for cat in category:
            rec = rec.sort_values(f'hybrid_score_{cat}', ascending=False)
            recomendations.append(rec)

    i = 1
    for table in recomendations[:2]:
        table.pop(f'hybrid_score_{category_dict[0][i]}')
        i -= 1

    return food_chooser(recomendations, kcal_limit)
