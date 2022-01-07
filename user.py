import pandas as pd
# user_id od  0 do 1
# liked_diets i disliked_diets id diety z tabeli diet, które będziemy w df zapisywać już w recommender window do implementacji
# preferences dane podane przy zakładaniu konta w gui ten df będzie tworzony w create_user window
users = pd.DataFrame(columns=['user_id', 'imie',  'nazwisko', 'liked_diets', 'dislike_diets', 'preferences'])
