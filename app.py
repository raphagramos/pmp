import sys
import os

# Adiciona o caminho da pasta principal ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Pages.LoginScreen import LoginScreen
from tkinter import PhotoImage, Tk

class Application:
    def __init__(self):
        self.root = Tk()
        self.login_screen = LoginScreen(self.root)
        self.root.title("PMP - Pesagens Matéria Prima")
        self.root.geometry("350x250") 
        icon = PhotoImage(file="C:/Users/Rapha - PC/Documents/Git Projects/PMP/Icon.png")  # Caminho corrigido
        self.root.iconphoto(True, icon)
        self.root.mainloop()       
      
if __name__ == "__main__":
    try:
        app = Application()
    except Exception as e:
        import traceback
        print("An unexpected error occurred:")
        traceback.print_exc()
        input("\nPress Enter to exit...")
