import pandas as pd
import numpy as np
# liked_diets i disliked_diets id diety z tabeli diet, które będziemy w df zapisywać już w recommender window do implementacji
# preferences dane podane przy zakładaniu konta w gui ten df będzie tworzony w create_user window

'''
Funkcja znajduje pierwszy wolny index w bazie danych
Przyjmuje:
    df - dla którego  szukamy idx
    id_str - nazwa kolumny z indexami
'''
def idx_finder(df, id_str):
    idx = df[id_str].values
    for count, idx in enumerate(set(sorted(idx))):
        if count + 1 != idx:
            new_idx = count + 1
            break
        else:
            new_idx = count + 2
    if df[id_str].values.size == 0:
        new_idx = 1
    return new_idx

'''
Funkcja tworząca użytkownika przyjmująca 3 stringi. Jest możliwość przyjmowania listy preferencji
Przyjmuje
    imie - imie uzytkownika
    nazwisko - nazwisko użytkownika
    preferencje - preferencje użytkownika
'''
def create_user(imie, nazwisko, preferencje):
    df = pd.read_csv('db/users.csv')
    new_idx = idx_finder(df, 'user_id')
    new_user = {'user_id': new_idx, 'imie': imie, 'nazwisko': nazwisko, 'liked_diets': np.NAN, 'dislike_diets': np.NAN, 'preferences': preferencje}
    df = df.append(new_user, ignore_index=True)
    df.sort_values('user_id')
    df.to_csv('db/users.csv', index=False)

'''
Funkcja usuwająca użytkownika
Przyjmuje
    user_id - id użytkownika
'''
def delete_user(user_id):
    df = pd.read_csv('db/users.csv')
    df = df.loc[df['user_id'] != user_id]
    df.to_csv('db/users.csv', index=False)

'''
Funkcja zmieniająca dane użytkownika
Przyjmuje:
    user_id - id użytkownika
    name - imie zmienione
    surname - nazwisko zmienione
    preferences - zmienione preferencje
'''
def change_user(user_id, **kwargs):
    df = pd.read_csv('db/users.csv')
    for key, value in kwargs.items():
        if key == 'name':
            df.loc[df['user_id'] == user_id, ['imie']] = value
        if key == 'surname':
            df.loc[df['user_id'] == user_id, ['nazwisko']] = value
        if key == 'preferences':
            df.loc[df['user_id'] == user_id, ['preferences']] = value
    df.to_csv('db/users.csv', index=False)


def get_all_user_names():
    df = pd.read_csv('db/users.csv')
    list_of_names = []
    if df.size == 0:
        return ["Brak użytkowników"]
    else:
        for i in df.user_id:
            if type(df.imie[i-1]) == str and type(df.nazwisko[i-1]) == str:
                name = df.imie[i-1]
                name = name + " " + df.nazwisko[i-1]
                list_of_names.append(name)
            
    return list_of_names


def search_for_user_name(name_to_compare):

    df = pd.read_csv('db/users.csv')    

    for i in df.user_id:
        if type(df.imie[i-1]) == str and type(df.nazwisko[i-1]) == str:
            name = df.imie[i-1]
            name = name + " " + df.nazwisko[i-1]
            
            if name_to_compare == name:
                return i
            
    return 0 #jeśli id == 0, to jest błąd

'''
Funkcja zapisuje do pliku csv polubione diety użytkownika
Przyjmuje:
    column_name - nazwę kolumny do której zapisać polubione diety
    diet_id - id diety do zapisania
    user_id - id użytkownika
'''
def save_liked_to_user(column_name, diet_id, user_id):
    user_df = pd.read_csv('db/users.csv')
    if user_df.loc[user_df['user_id'] == user_id, [column_name]].isnull().any()[column_name]:
        user_df.loc[user_df['user_id'] == user_id, [column_name]] = str(diet_id)
    else:
        new_liked = str(user_df.loc[user_df['user_id'] == user_id, [column_name]][column_name].values[0])
        user_df.loc[user_df['user_id'] == user_id, [column_name]] = new_liked + f" {diet_id}"
    user_df.to_csv('db/users.csv', index=False)

'''
Funkcja zapisująca polubione diety
    Przyjmuje:
    like_type - Wartość logiczna  True lub False zależnie czy jest to polubienie czy niepolubienie
    user_id - id aktywnego użytkownika
    food_list - lista potraw zarekomendowanych
'''
def like_dislike_diet(like_type, user_id, food_list):
    if like_type:
        df = pd.read_csv('db/liked_diets.csv')
    elif not like_type:
        df = pd.read_csv('db/unliked_diets.csv')

    diet_id = idx_finder(df, 'diet_id')
    df = df.append({'diet_id': diet_id, 'user_id': user_id,
                    'śniadanie': food_list[0]['food_id'],
                    'zupa': food_list[2]['food_id'],
                    'obiad': food_list[3]['food_id'],
                    'kolacja': food_list[1]['food_id']}, ignore_index=True)

    if like_type:
        save_liked_to_user('liked_diets', diet_id, user_id)
        df.to_csv('db/liked_diets.csv', index=False)
    elif not like_type:
        save_liked_to_user('dislike_diets', diet_id, user_id)
        df.to_csv('db/unliked_diets.csv', index=False)
