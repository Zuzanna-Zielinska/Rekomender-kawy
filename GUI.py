# TODO: Main window
# wybór w nim będzie po prostu przyciskami create_user i login, po kliknięciu login 
# wybierać się będzie usera jeszcze jeden przycisk można dodać delete_user i po kliknięciu 
# się będzie wybierać usera to też bym jako pop_up zrobił?
#Zuzia: tutaj też bym dała pole wyboru użytkownika, tzn jest na to miejsce

# TODO: create_user window
#   zrobić pole na podanie imienia i nazwiska
#   rozwijane menu z wyborem ostrości i tego czy jest się vege, wegan, czy nie wegan osobno te 2 rozwijane menu
# implementacja funkcji zapisujących to wszystko do df w user.py tu tylko wywołania
# zapis danych do pliku csv, który wstępnie definiuje w user.py
#   po zatwierdzeniu wracamy do main window

# TODO: Recommendation window
# okno w którym będziemy wyświetlać rekomendację oraz możliwość likowania diet i dislikowania
# okno będzie otwierane po wyborze użytkownika z pop_upu po kliknięciu przycisku login
# przycisk powrotu do main window
# można jeszcze coś dodać ale na razie tyle
# będziemy wyświetlać 3 dania i możliwe, że przekąski to początkowo 3 pola opisane śniadanie, obiad, kolacja
# obiaad składa się z zupy i drugiego dania

from tkinter import *
from tkinter import ttk
from typing import NewType
import pandas as pd
from GUI_templates import I_Window, I_Page, Page, window, Drop_Down_Menu
import user
import recommender as re

    
tag_meat_or_not = ["Vegan", "Wegetariański", "mięsny"]
tag_spiciness = ["ostry", "średni", "łagodny"]


"""
Główne okno programu. Inicjuje stronę startową.

Przyjmuje:
    width - szerokość okna
    height - wysokość okna
"""
class Main_Window(I_Window):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs) #załadowanie initu z rodzica

        Start_Page(self.window)   
     
"""
Strona wyboru użytkownika

Przyjmuje:
    window - okno programu
"""
class Start_Page(I_Page):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #załadowanie initu z rodzica
        self.logo_png = PhotoImage(file=r"png/logo.png")
        self.add_user_png = PhotoImage(file=r"png/add_user.png")
        self.pick_user_png = PhotoImage(file=r"png/pick_user.png")
        self.layout()
        
    
    def layout(self):
        '''
        Ułożenie i wyswietlenie wszystkiego na stronie
        '''
        
        self.make_frames(2)
        #tło

        # ---------------tytuł----------------
        title = Label(master=self.frames[0],
                      image = self.logo_png, bg='#c1c7b6')
        title.pack()
        # ------------------------------------
        # ------------przyciski------------
        self.button_login = Button( master = self.frames[1], width = self.like_button_size[0],
            height = self.button_size[1],image = self.pick_user_png, text="Wybierz użytkownika",bg='#c1c7b6', font = self.button_font,
            command=(lambda: self.change_page(Recommendation_Page, self.choose_user.get(), True)))
        self.button_login.pack(pady=(5,5))
        
        self.choose_user = Drop_Down_Menu(self.window, self.frames[1], user.get_all_user_names())
        
        self.button_create_user = Button( master = self.frames[1], width = self.like_button_size[0],
            height = self.button_size[1],image = self.add_user_png, text="Dodaj użytkownika",bg='#c1c7b6', font = self.button_font,
            command=(lambda: self.change_page(Create_User_Page)))
        self.button_create_user.pack(pady=(5,5))
        # ----------------------------------
        
    def change_page(self, New_Page, chosen_user = None, activate_if = False):
        
        if self.choose_user.get() != "Brak użytkowników" and activate_if == True:
            super().change_page(New_Page, chosen_user)
        elif activate_if == False:
            super().change_page(New_Page, chosen_user)
        
        

"""
Strona tworzenia urzytkownika

Przyjmuje:
    window - okno programu
"""        
class Create_User_Page(I_Page):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #załadowanie initu z rodzica
        self.logo_png = PhotoImage(file=r"png/logo.png")
        self.accept_png = PhotoImage(file=r"png/accept.png")
        self.layout()
        
    def layout(self):
        '''
        Ułożenie i wyswietlenie wszystkiego na stronie
        '''
        
        self.make_frames(3)

        # ---------------tytuł----------------
        title = Label(master=self.frames[0],
                      image = self.logo_png)
        title.pack()
        # ------------------------------------
        
        # ---------------pola do wpisywania danych----------------
        self.name_label = Label(master=self.frames[1],
                      text="Podaj imię", bg='#c1c7b6',font=self.normal_text_font)
        self.name_label.pack()
        self.name = ttk.Entry(master = self.frames[1])
        self.name.pack()
        
        self.surname_label = Label(master=self.frames[1],
                      text="Podaj nazwisko",bg='#c1c7b6', font=self.normal_text_font)
        self.surname_label.pack()
        self.surname = ttk.Entry(master = self.frames[1])
        self.surname.pack()
        # --------------------------------------------------------
        
        # ---------------preferencje----------------
        self.label = Label(master=self.frames[1],
                      text="Czy jesz dania mięsne?",bg='#c1c7b6', font=self.normal_text_font)
        self.label.pack()

        self.meat_or_not = Drop_Down_Menu(self.window, self.frames[1], tag_meat_or_not)
        
        self.label = Label(master=self.frames[1],
                      text="Wolisz dania łagodne, czy ostre?", bg='#c1c7b6',font=self.normal_text_font)
        self.label.pack()

        self.spiciness = Drop_Down_Menu(self.window, self.frames[1], tag_spiciness)
        # -------------------------------------------
        
        # ------------przyciski------------
        self.button_go_back = Button( master = self.frames[self.number_of_frames-1], width = self.like_button_size[0],
            height = self.button_size[1],image = self.accept_png, bg='#c1c7b6',text="Zatwierdź wybór", font = self.button_font,
            command=(lambda: self.change_page(Start_Page)))
        self.button_go_back.pack(pady=(5,5))
        # ----------------------------------
        
    def add_user(self):
        '''
        Zapisywanie wartosci podanych przez użytkownika
        '''
        self.preferences = self.spiciness.get() + " " + self.meat_or_not.get()
        user.create_user(self.name.get(), self.surname.get(), self.preferences)
        
    def change_page(self, New_Page):
        self.add_user()
        super().change_page(New_Page)

"""
Strona z profilem użytkownika

Przyjmuje:
    window - okno programu
"""      
class Recommendation_Page(I_Page):
    
    def __init__(self,window: window, choosen_user):
        self.window = window
        self.number_of_frames = 0
        self.style_table()
        self.diet_png = PhotoImage(file=r"png/diet.png")
        self.back_start_png = PhotoImage(file=r"png/back_start.png")
        self.logo_png = PhotoImage(file=r"png/logo.png")
        self.edit_png = PhotoImage(file=r"png/edit.png")


        if type(choosen_user) == str:
            self.user_id = user.search_for_user_name(choosen_user)
        else:
            self.user_id = choosen_user
        self.user_data = pd.read_csv('db/users.csv') 
        self.layout()
        
    def layout(self):
        '''
        Ułożenie i wyswietlenie wszystkiego na stronie
        '''
        
        self.make_frames(4)

        
        # ---------------tytuł----------------
        title = Label(master=self.frames[0],
                      image = self.logo_png,bg='#c1c7b6')
        title.pack()
        # ------------------------------------
        
        # ---------------info użytkownika----------------
        self.inner_frame_right = Frame(master=self.frames[1],bg='#c1c7b6')
        self.inner_frame_right.grid(row=0, column=0, sticky="w")
        
        self.label = Label(master=self.inner_frame_right,
                      text="Imię:",bg='#c1c7b6', font=self.normal_text_font)
        self.label.pack()
        self.label = Label(master=self.inner_frame_right,
                      text=self.user_data.imie[self.user_id - 1], bg='#c1c7b6',font=self.normal_text_font)
        self.label.pack()
        
        self.label = Label(master=self.inner_frame_right,
                      text="Nazwisko:", bg='#c1c7b6',font=self.normal_text_font)
        self.label.pack()
        self.label = Label(master=self.inner_frame_right,
                      text=self.user_data.nazwisko[self.user_id - 1],bg='#c1c7b6', font=self.normal_text_font)
        self.label.pack()
        
        self.label = Label(master=self.inner_frame_right,
                      text="Preferencje:",bg='#c1c7b6', font=self.normal_text_font)
        self.label.pack()
        self.label = Label(master=self.inner_frame_right,
                      text=self.user_data.preferences[self.user_id - 1], bg='#c1c7b6',font=self.normal_text_font)
        self.label.pack()
        
        self.label = Label(master=self.inner_frame_right,
                      text="Dzienny limit kalorii:",bg='#c1c7b6', font=self.normal_text_font)
        self.label.pack()
        self.kcal = ttk.Entry(master = self.inner_frame_right)
        self.kcal.insert(0, 2000)
        self.kcal.pack()
        # -----------------------------------------------
        
        # ---------------przycisk edycji użytkownika----------------
        self.inner_frame_right = Frame(master=self.frames[1])
        self.inner_frame_right.grid(row=0, column=1, sticky="e")
        
        self.button_go_back = Button( master = self.inner_frame_right, width = self.small_button_size[0],
            height = self.small_button_size[1], image = self.edit_png, bg='#c1c7b6',text="Edytuj", font = self.button_font,
            command=(lambda: self.change_page(Edit_User_Page, self.user_id)))
        self.button_go_back.pack()
        # ----------------------------------------------------------
        
        # ------------przyciski------------
        self.button_go_back = Button( master = self.frames[2], width = self.like_button_size[0],
            height = self.button_size[1],image = self.diet_png,bg='#c1c7b6', text="Sprawdź dietę!", font = self.button_font,
            command=(lambda: self.change_page(Diet_Page, [self.user_id, self.kcal.get()])))
        self.button_go_back.pack(pady=(5,5))
        
        self.button_go_back = Button( master = self.frames[self.number_of_frames-1], width = self.like_button_size[0],
            height = self.button_size[1],image = self.back_start_png, bg='#c1c7b6',text="Powrót do strony startowej", font = self.button_font,
            command=(lambda: self.change_page(Start_Page)))
        self.button_go_back.pack(pady=(5,5))
        # ----------------------------------
        
        
"""
Strona z edycją użytkownika

Przyjmuje:
    window - okno programu
    user_id - id użytkownika do zmiany (ten zaczynający się od 1)
"""  
class Edit_User_Page(Create_User_Page):
    
    def __init__(self,window: window, user_id):
        self.window = window
        self.number_of_frames = 0
        self.style_table()
        self.logo_png = PhotoImage(file=r"png/logo.png")
        self.accept_png = PhotoImage(file=r"png/accept.png")
        
        self.user_id = user_id
        self.user_data = pd.read_csv('db/users.csv') 
        self.layout()
        
    def layout(self):
        super().layout()
        self.name.insert(0, self.user_data.imie[self.user_id-1])
        self.surname.insert(0, self.user_data.nazwisko[self.user_id-1])
        
    def add_user(self):
        self.preferences = self.spiciness.get() + " " + self.meat_or_not.get()
        
        user.create_user(self.name.get(), self.surname.get(), self.preferences)
        
    def change_page(self, New_Page):
        user.delete_user(self.user_id)
        super().change_page(New_Page)

"""
Strona z rekomendacją diety

Przyjmuje:
    window - okno programu
    user_id - [id użytkownika do zmiany (ten zaczynający się od 1), limit kalorii]
"""  
class Diet_Page(I_Page):
    
    def __init__(self,window: window, user_id):
        self.window = window
        self.number_of_frames = 0
        self.style_table()
        
        self.kcal_limit = int(user_id[1])
        self.data_base(user_id[0])
        self.is_liked = 2 #like - 1, dislike - 0, brak interakcji - 2
        self.like_png = PhotoImage(file = r"png/like.png")
        self.dislike_png = PhotoImage(file=r"png/dislike.png")
        self.back_png = PhotoImage(file=r"png/back.png")
        self.logo_png = PhotoImage(file=r"png/logo.png")

        self.layout()
        
    def data_base(self, user_id):
        self.user_id = user_id
        self.user_data = pd.read_csv('db/users.csv')
        

        self.breakfast_data = pd.read_csv('db/sniadania_database.csv')
        self.dinner_data = pd.read_csv('db/dania_glowne_database.csv') 
        self.soup_data = pd.read_csv('db/zupy_database.csv') 
        self.liked_data = pd.read_csv('db/liked_diets.csv')
        
        self.recommend = re.get_recommendation([self.breakfast_data, self.dinner_data, self.soup_data], 
                                               self.user_data, self.user_id, self.liked_data, self.kcal_limit)
        self.recommend = self.recommend[0]
    
    def layout(self):
        '''
        Ułożenie i wyswietlenie wszystkiego na stronie
        '''
        
        self.make_frames(11)


        
        # ---------------tytuł----------------
        title = Label(master=self.frames[0],
                      image = self.logo_png,bg='#c1c7b6')
        title.pack()
        # ------------------------------------
        
        # ---------------sniadanie----------------
        self.label = Label(master=self.frames[1],
                      text="Śniadanie: " + self.recommend[0]['food_title'], bg='#c1c7b6',font=self.dish_title_text_font)
        self.label.pack()
        
        self.label = Label(master=self.frames[2],
                      text= "{0} kcal, ".format(self.recommend[0]['kcal']), 
                      font=self.normal_text_font,bg='#c1c7b6')
        self.label.grid(row=0, column=0)
        
        self.label = Label(master=self.frames[2],
                      text= "{0:.3f} trafności".format(self.recommend[0]['hybrid_score_śniadanie']), 
                      font=self.normal_text_font,bg='#c1c7b6')
        self.label.grid(row=0, column=1)
        # ----------------------------------------
        
        # ---------------zupa------------------
        self.label = Label(master=self.frames[3],
                      text="Zupa: " + self.recommend[3]['food_title'],bg='#c1c7b6', font=self.dish_title_text_font)
        self.label.pack()
        
        self.label = Label(master=self.frames[4],
                      text= "{0} kcal, ".format(self.recommend[3]['kcal']), bg='#c1c7b6',
                      font=self.normal_text_font)
        self.label.grid(row=0, column=0)
        
        self.label = Label(master=self.frames[4],
                      text= "{0:.3f} trafności".format(self.recommend[3]['hybrid_score_zupa']), bg='#c1c7b6',
                      font=self.normal_text_font)
        self.label.grid(row=0, column=1)
        # --------------------------------------
        
        # ---------------drugie danie------------------
        self.label = Label(master=self.frames[5],
                      text="Drugie danie: " + self.recommend[2]['food_title'],bg='#c1c7b6', font=self.dish_title_text_font)
        self.label.pack()
        
        self.label = Label(master=self.frames[6],
                      text= "{0} kcal, ".format(self.recommend[2]['kcal']), bg='#c1c7b6',
                      font=self.normal_text_font)
        self.label.grid(row=0, column=0)
        
        self.label = Label(master=self.frames[6],
                      text= "{0:.3f} trafności".format(self.recommend[2]['hybrid_score_obiad']), bg='#c1c7b6',
                      font=self.normal_text_font)
        self.label.grid(row=0, column=1)
        # ---------------------------------------------
        
        # ---------------kolacja------------------
        self.label = Label(master=self.frames[7],bg='#c1c7b6',
                      text="Kolacja: " + self.recommend[1]['food_title'], font=self.dish_title_text_font)
        self.label.pack()
        
        self.label = Label(master=self.frames[8],
                      text= "{0} kcal, ".format(self.recommend[1]['kcal']), bg='#c1c7b6',
                      font=self.normal_text_font)
        self.label.grid(row=0, column=0)
        
        self.label = Label(master=self.frames[8],
                      text= "{0:.3f} trafności".format(self.recommend[1]['hybrid_score_kolacja']), bg='#c1c7b6',
                      font=self.normal_text_font)
        self.label.grid(row=0, column=1)
        # ----------------------------------------
        
        # ------------przyciski------------
        #polubienie
        self.button_dislike1 = Button( master = self.frames[self.number_of_frames-2], width = self.like_button_size[0],
            height = self.like_button_size[1],image= self.dislike_png, text="dislike", font = self.like_button_font,bg='#c1c7b6',
            command = lambda: self.set_like(0))

        self.button_dislike1.grid(row=0, column=0)
        
        self.button_like1 = Button( master = self.frames[self.number_of_frames-2], width = self.like_button_size[0],
            height = self.like_button_size[1], image= self.like_png, text="like", font = self.like_button_font,bg='#c1c7b6',
            command = lambda: self.set_like(1))

        self.button_like1.grid(row=0, column=1)
        
        #przycisk powrotu
        self.button_go_back = Button( master = self.frames[self.number_of_frames-1], width = self.like_button_size[0],
            height = self.button_size[1], image= self.back_png, text="Powrót do profilu", font = self.button_font,bg='#c1c7b6',
            command = lambda: self.change_page(Recommendation_Page, self.user_id))
        self.button_go_back.pack(pady=(5,5))
        # ----------------------------------

    def set_like(self, a):
        if a == 2:
            self.is_liked = 2
        elif a == 0:
            self.is_liked = 0
        elif a == 1:
            self.is_liked = 1

    def do_like(self):
        if self.is_liked == 2:
            return None
        elif self.is_liked == 0:
            return False
        elif self.is_liked == 1:
            return True
    
    def change_page(self, New_Page, chosen_user = None):
        
        is_liked = self.do_like()
        if is_liked != None:
            user.like_dislike_diet(is_liked, self.user_id, self.recommend)
        
        super().change_page(New_Page, chosen_user)
        
        
open_window = Main_Window(800,600)
open_window.mainloop()
