# TODO: Main window
# wybór w nim będzie po prostu przyciskami create_user i login, po kliknięciu login 
# wybierać się będzie usera jeszcze jeden przycisk można dodać delete_user i po kliknięciu 
# się będzie wybierać usera to też bym jako pop_up zrobił?
#Zuzia: tutaj też bym dała pole wyboru użytkownika, tzn jest na to miejsce

# TODO: create_user window
# zrobić pole na podanie imienia i nazwiska
# rozwijane menu z wyborem ostrości i tego czy jest się vege, wegan, czy nie wegan osobno te 2 rozwijane menu
# implementacja funkcji zapisujących to wszystko do df w user.py tu tylko wywołania
# zapis danych do pliku csv, który wstępnie definiuje w user.py
# po zatwierdzeniu wracamy do main window

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

Page = NewType('Page', object)  # pomocnicza podpowiedź typu
window = NewType('window', object)

"""
Interfejs wyświetlania okna.
Tak, próbowałam stowować zasady SOLID XD.

Przyjmuje:
    width - szerokość okna
    height - wysokość okna
"""
class I_Window():
    def __init__(self, width, height):
        self.window = Tk()  # tworzenie okna
        self.window.geometry('{0}x{1}'.format(width, height))
        
    
    def mainloop(self):
        self.window.mainloop()
        
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
Interfejs wyświetlania strony.

Przyjmuje:
    window - okno programu
"""
class I_Page():
    def __init__(self, window: window):
        self.window = window
        self.number_of_frames = 0
        self.style_table()
        
    def style_table(self):
        """
        Lista czcionek, ich wysokości, wymiarów przycisków.
        """
        self.title_font = ["lucida", 40]
        self.minor_title_font = ["lucida", 30] 
        self.button_font = ["lucida", 20]
        self.normal_text_font = ["lucida", 12]
        
        self.button_size = [20, 0]
        
    def clear_window(self):
        """
        Funkcja czysci okno z wszelkich elementow.
        """   
        
        for child in self.window.winfo_children():
            child.destroy()
            
    def change_page(self, New_Page: Page):
        '''
        Przełączenie do innej strony
        '''
        
        self.clear_window()
        New_Page(self.window)
        
    def make_frames(self, n: int):
        
        self.frames = []
        self.number_of_frames = n
        
        # ----elementy w oknie dopasowują się do jego rozmiaru----
        self.window.columnconfigure(0, weight=1)
        for i in range(2):
            self.window.rowconfigure(i, weight=1)
        # --------------------------------------------------------
        
        for i in range(n):
            
            self.frames.append(Frame(master = self.window))
            self.frames[i].grid(row=i, column=0, sticky="n")
            
    def add_frame(self):
        
        self.window.rowconfigure(self.number_of_frames, weight=1)
        self.frames.append(Frame(master = self.window))
        self.frames[self.number_of_frames].grid(row=self.number_of_frames, column=0, sticky="n")
        
        self.number_of_frames = self.number_of_frames + 1
    
        
"""
Strona wyboru użytkownika

Przyjmuje:
    window - okno programu
"""
class Start_Page(I_Page):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #załadowanie initu z rodzica
        self.layout()
        
    
    def layout(self):
        '''
        Ułożenie i wyswietlenie wszystkiego na stronie
        '''
        
        self.make_frames(2)

        # ---------------tytuł----------------

        title = Label(master=self.frames[0],
                      text="Rekomender", font=self.title_font)
        title.pack()
        # ------------------------------------
        # ------------przyciski------------
        
        self.button_login = Button( master = self.frames[1], width = self.button_size[0],
            height = self.button_size[1], text="Wybierz użytkownika", font = self.button_font, 
            command=(lambda: self.change_page(Recommendation_Page)))
        self.button_login.pack()
        
        self.button_create_user = Button( master = self.frames[1], width = self.button_size[0],
            height = self.button_size[1], text="Dodaj użytkownika", font = self.button_font, 
            command=(lambda: self.change_page(Create_User_Page)))
        self.button_create_user.pack()
        # ----------------------------------


"""
Strona tworzenia urzytkownika

Przyjmuje:
    window - okno programu
"""        
class Create_User_Page(I_Page):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #załadowanie initu z rodzica
        self.layout()
        
    def layout(self):
        '''
        Ułożenie i wyswietlenie wszystkiego na stronie
        '''
        
        self.make_frames(3)
        
        # ---------------tytuł----------------

        title = Label(master=self.frames[0],
                      text="Kreacja użytkownika", font=self.minor_title_font)
        title.pack()
        # ------------------------------------
        
        # ---------------pola do wpisywania danych----------------

        self.name_label = Label(master=self.frames[1],
                      text="Podaj imię", font=self.normal_text_font)
        self.name_label.pack()
        self.name = ttk.Entry(master = self.frames[1])
        self.name.pack()
        # --------------------------------------------------------
        
        # ------------przyciski------------
        self.button_go_back = Button( master = self.frames[2], width = self.button_size[0],
            height = self.button_size[1], text="Zatwierdź wybór", font = self.button_font, 
            command=(lambda: self.change_page(Start_Page)))
        self.button_go_back.pack()
        # ----------------------------------

"""
Strona z rekomendacjami

Przyjmuje:
    window - okno programu
"""      
class Recommendation_Page(I_Page):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #załadowanie initu z rodzica
        self.layout()
        
    def layout(self):
        '''
        Ułożenie i wyswietlenie wszystkiego na stronie
        '''
        
        self.make_frames(2)
        
        # ---------------tytuł----------------
        title = Label(master=self.frames[0],
                      text="Dieta dla ciebie!", font=self.minor_title_font)
        title.pack()
        # ------------------------------------
        
        # ------------przyciski------------
        self.button_go_back = Button( master = self.frames[1], width = self.button_size[0],
            height = self.button_size[1], text="Powrót do strony startowej", font = self.button_font, 
            command=(lambda: self.change_page(Start_Page)))
        self.button_go_back.pack()
        # ----------------------------------
        
        
open_window = Main_Window(500, 580)
open_window.mainloop()