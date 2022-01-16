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
        self.small_button_size = [0, 0]
        
    def clear_window(self):
        """
        Funkcja czysci okno z wszelkich elementow.
        """   
        
        for child in self.window.winfo_children():
            child.destroy()
            
    def change_page(self, New_Page: Page, chosen_user = None):
        '''
        Przełączenie do innej strony
        '''
        
        if chosen_user == None:
            self.clear_window()
            New_Page(self.window)
        else:
            self.clear_window()
            New_Page(self.window, chosen_user)
        
    def make_frames(self, n: int, col = 0):
        
        self.frames = []
        self.number_of_frames = n
        
        # ----elementy w oknie dopasowują się do jego rozmiaru----
        self.window.columnconfigure(col, weight=1)
        for i in range(2):
            self.window.rowconfigure(i, weight=1)
        # --------------------------------------------------------
        
        for i in range(n):
            
            self.frames.append(Frame(master = self.window))
            self.frames[i].grid(row=i, column=col, sticky="n")
            
    # def add_frame(self):
        
    #     self.window.rowconfigure(self.number_of_frames, weight=1)
    #     self.frames.append(Frame(master = self.window))
    #     self.frames[self.number_of_frames].grid(row=self.number_of_frames, column=0, sticky="n")
        
    #     self.number_of_frames = self.number_of_frames + 1
        
class Drop_Down_Menu():
    def __init__(self, window, frame, tag_table, start_value = -1):
        self.value = StringVar(window)
        self.value.set(tag_table[start_value])
        self.menu = OptionMenu(frame, self.value, *tag_table)
        self.menu.pack()
        
    def get(self):
        return self.value.get()
    
        