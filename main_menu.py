import tkinter as tk
from tkinter import ttk

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()

        #Basic window
        self.title("Checkers Main Menu")
        self.geometry("900x600")
        self.minsize(720, 480)

        #Style
        self.style = ttk.Style(self)

        #Trying "calm" style
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        #App-level states
        self.display_name = tk.StringVar(value="")
        self.volume = tk.DoubleVar(value=0.7)
        self.muted = tk.BooleanVar(value=False)

        #Container frame
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        #Screens dictionary
        self.screens = {}
        for ScreenClass in (MainMenu, PlaceholderCPU, PlaceholderLocal, PlaceholderOnline):
            screen = ScreenClass(self.container, self)
            name = screen.name
            self.screens[name] = screen
            #Places all screens in same location, raise active screen
            screen.grid(row=0, column=0, sticky="nsew")

        #Allow container size change
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        #NEW For the choice of gamemode. Used in handoff to pygame.
        self.choice = None

        #Starts on menu. Either change to login page or (...?)
        self.show("menu")

    #Switch screens
    def show(self, name: str):
        self.screens[name].tkraise()

    #Volume muting
    def effective_volume(self) -> float:
        return 0.0 if self.muted.get() else float(self.volume.get())
    
    # NEW currently called when the user chooses Local (2P). Closes the Tk window so we can start pygame cleanly
    def start_local(self):
        self.choice = "PVP"
        self.destroy()

    # Start game vs CPU
    def start_cpu(self):
        self.choice = "PVC"
        self.destroy()


#-------------------------
#BASE SCREEN
class Screen(ttk.Frame):
    # Other screens inherit
    name = "base"

    def __init__(self, parent, app: Menu):
        super().__init__(parent)
        self.app = app

        # Grid to keep content centered
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


#-------------------------
#MAIN MENU
class MainMenu(Screen):
    name = "menu"

    def __init__(self, parent, app: Menu):
        super().__init__(parent, app)

        #Wrapper to center content
        wrap = ttk.Frame(self)
        wrap.grid(row=0, column=0, sticky="n", pady=40)
        for i in range(1):
            wrap.columnconfigure(i, weight=1)

        ttk.Label(wrap, text="Checkers", style="Title.TLabel").grid(row=0, column=0, pady=(0, 6))
        ttk.Label(wrap, text="Main Menu", style="Subtitle.TLabel").grid(row=1, column=0, pady=(0, 20))

        #Buttons
        #NEW Local (2P) button for handing off to the pygame window
        ttk.Button(
            wrap,
            text="Play: Local (2P)",
            command=app.start_local  # <— handoff
        ).grid(row=2, column=0, pady=6, ipadx=20)

        ttk.Button(wrap, text="Play: vs CPU", command=app.start_cpu).grid(row=3, column=0, pady=6, ipadx=20)
        ttk.Button(wrap, text="Play: Online", command=lambda: app.show("online")).grid(row=4, column=0, pady=6,
                                                                                       ipadx=20)

        ttk.Separator(wrap).grid(row=6, column=0, sticky="ew", pady=12)

        ttk.Button(wrap, text="Quit", command=app.destroy).grid(row=7, column=0, pady=6, ipadx=20)

#-------------------------
#CONNECT TO GAME LATER
class PlaceholderBase(Screen):
    _title = "Placeholder"

    def __init__(self, parent, app: Menu):
        super().__init__(parent, app)

        #Center content vertically
        box = ttk.Frame(self, padding=20)
        box.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(box, text=self._title, style="Title.TLabel").pack(pady=(30, 10))
        ttk.Label(box, text=(
            "This is a placeholder screen"
        ), style="Subtitle.TLabel", justify="center").pack(pady=(0, 20))

        ttk.Button(box, text="Back to Menu", command=lambda: app.show("menu")).pack(pady=10)

class PlaceholderLocal(PlaceholderBase):
    name = "local"
    _title = "Local 2P"

class PlaceholderCPU(PlaceholderBase):
    name = "cpu"
    _title = "vs CPU"

class PlaceholderOnline(PlaceholderBase):
    name = "online"
    _title = "Online"

#Entry point
if __name__ == "__main__":
    Menu().mainloop()
