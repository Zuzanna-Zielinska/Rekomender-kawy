# TODO: Main window
# wybór w nim będzie po prostu przyciskami create_user i login, po kliknięciu login 
# wybierać się będzie usera jeszcze jeden przycisk można dodać delete_user i po kliknięciu 
# się będzie wybierać usera to też bym jako pop_up zrobił?

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

from tkinter import *

"""
Interfejs wyświetlania okna.
Próbowałam stowować zasady SOLID.

Przyjmuje:
    width - szerokość okna
    height - wysokość okna

"""
class IWindow():
    def __init__(self, width, height):
        self.style_table()
        
        self.window = Tk()  # tworzenie okna
        self.window.geometry('{0}x{1}'.format(width, height))
        
    def style_table(self):
        """
        Lista czcionek, ich wysokości, wymiarów przycisków.
        """
        self.title_font = ["lucida", 40]
        self.button_font = ["lucida", 20]
        self.normal_text_font = ["lucida", 12]
        
        self.button_size = [20, 0]
    
    def mainloop(self):
        self.window.mainloop()

        
"""
Okno wyboru użytkownika
"""
class Start_window(IWindow):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs) #załadowanie initu z rodzica
        self.layout()
        
    
    def layout(self):
        '''
        Ułożenie i wyswietlenie przycisków na stronie
        '''
        
        # ----elementy w oknie dopasowują się do jego rozmiaru----
        self.window.columnconfigure(0, weight=1)
        for i in range(2):
            self.window.rowconfigure(i, weight=1)
        # --------------------------------------------------------
        
        # ---------------tytuł----------------
        self.title_frame = Frame(master = self.window)
        self.title_frame.grid(row=0, column=0, sticky="n")

        title = Label(master=self.title_frame,
                      text="Rekomender", font=self.title_font)
        title.pack()
        # ------------------------------------
        # --------przycisk wczytywania--------
        self.buttons_frame = Frame(master = self.window)
        self.buttons_frame.grid(row=1, column=0, sticky="n")
        
        self.button_login = Button( master = self.buttons_frame, width = self.button_size[0],
            height = self.button_size[1], text="Wybierz użytkownika", font = self.button_font)
        self.button_login.pack()
        
        self.button_create_user = Button( master = self.buttons_frame, width = self.button_size[0],
            height = self.button_size[1], text="Dodaj użytkownika", font = self.button_font)
        self.button_create_user.pack()
        # ------------------------------------
        
open_window = Start_window(500, 580)
open_window.mainloop()