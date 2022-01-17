import pandas as pd
import numpy as np

# liked_diets i disliked_diets id diety z tabeli diet, które będziemy w df zapisywać już w recommender window do implementacji
# preferences dane podane przy zakładaniu konta w gui ten df będzie tworzony w create_user window

'''
Funkcja tworząca użytkownika przyjmująca 3 stringi. Jest możliwość przyjmowania listy preferencji
'''
def create_user(imie, nazwisko, preferencje):
    df = pd.read_csv('db/users.csv')
    idx = df['user_id'].values
    for count, idx in enumerate(set(sorted(idx))):
        if count+1 != idx:
            new_idx = count + 1
            break
        else:
            new_idx = count + 2
    if df['user_id'].values.size == 0:
        new_idx = 1
    new_user = {'user_id': new_idx, 'imie': imie, 'nazwisko': nazwisko, 'liked_diets': np.NAN, 'dislike_diets': np.NAN, 'preferences': preferencje}
    df = df.append(new_user, ignore_index=True)
    df.to_csv('db/users.csv', index=False)

'''
Funkcja usuwająca użytkownika przyjmująca imię, nazwisko  or user_id,  preferable user_id
'''
def delete_user(user_id):
    df = pd.read_csv('db/users.csv')
    df = df.loc[df['user_id'] != user_id]
    df.to_csv('db/users.csv', index=False)

def get_all_user_names():
    df = pd.read_csv('db/users.csv')
    list_of_names = []
    
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

# delete_user(1)
# create_user('adam', 'wojniak', 'angi cos ans')