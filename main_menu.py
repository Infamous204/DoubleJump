import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from pathlib import Path

class Menu(tk.Tk):
    def __init__(self):
        super().__init__()

        #Basic window
        self.title("Checkers Main Menu")
        self.geometry("1024x1536")
        self.minsize(980, 980)
        self.maxsize(980, 980)
        self.resizable(False, False)

        self.configure(bg="#000000")

        #Style
        self.style = ttk.Style(self)

        #Trying "calm" style
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure("Background.TFrame", background="#000000")

        title_font = tkfont.Font(family="Terminal", size=40, weight="bold")
        subtitle_font = tkfont.Font(family="Terminal", size=18)
        button_font = tkfont.Font(family="Terminal", size=12)

        neon_green = "#00ff66"
        neon_red = "#ff0033"
        dark_bg = "#000000"

        self.style.configure("Title.TLabel", font=title_font, foreground=neon_green, background=dark_bg)
        self.style.configure("Subtitle.TLabel", font=subtitle_font, foreground=neon_red, background=dark_bg)
        self.style.configure("Neon.TButton", font=button_font, foreground=neon_green, background="#111111", borderwith=1, focusthickness=0, relief="flat")
        self.style.map("Neon.TButton", background=[("active", "#222222"), ("pressed", "#000000")])

        #App-level states
        self.display_name = tk.StringVar(value="")
        self.volume = tk.DoubleVar(value=0.7)
        self.muted = tk.BooleanVar(value=False)

        #Container frame
        self.container = ttk.Frame(self, style="Background.TFrame")
        self.container.pack(fill="both", expand=True)

        #Screens dictionary
        self.screens = {}
        for ScreenClass in (MainMenu, PlaceholderCPU, PlaceholderLocal): #PlaceholderOnline removed
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
        super().__init__(parent, style="Background.TFrame")
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

        #Background
        base_dir = Path(__file__).resolve().parent
        img_path = base_dir / "sprites" / "MMBackground.png"

        self.bg_image = tk.PhotoImage(file=str(img_path))

        #Fill canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg="#000000")
        self.canvas.pack(fill="both", expand=True)

        def center_bg(event=None):
            self.canvas.delete("bg")
            self.canvas.create_image(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, anchor="center", image=self.bg_image, tags="bg")

            self.canvas.tag_lower("bg")

        self.after(10, center_bg)

        self.canvas.bind("<Configure>", center_bg)

        width, height = 980, 980
        center_x = width // 2

        title_y = int(height * 0.15)
        subtitle_y = title_y + 40
        button_start_y = int(height * 0.29)
        spacing = 55

        neon_green = "#00ff66"
        neon_pink = "#FF69B4"
        neon_red = "#ff0033"
        neon_white = "#ffffff"
        neon_hover = "#00FFFF"
        neon_press = "#00cc55"

        #Fonts again :(
        title_font = ("Terminal", 40, "bold")
        subtitle_font = ("Terminal", 20, "bold")
        button_font = ("Terminal", 18, "bold")

        #Title
        self.canvas.create_text(center_x, title_y, text="Checkers", font=title_font, fill=neon_green)

        self.canvas.create_text(center_x, subtitle_y, text="Main Menu", font=subtitle_font, fill=neon_red)

        #Attempt at transparent buttons
        def neon_button(y, text, command):
            item = self.canvas.create_text(center_x, y, text=text, font=button_font, fill=neon_white)

            #Button reaction
            def on_enter(event, i=item):
                self.canvas.itemconfig(i, fill=neon_hover)

            def on_leave(event, i=item):
                self.canvas.itemconfig(i, fill=neon_white)

            def on_click(event, i=item, cmd=command):
                self.canvas.itemconfig(i, fill=neon_press)
                self.after(1,cmd)

            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)
            self.canvas.tag_bind(item, "<Button-1>", on_click)

            return item

        neon_button(button_start_y, "Play: Local (2P)", app.start_local)
        neon_button(button_start_y + spacing, "Play: vs CPU", app.start_cpu)
        neon_button(button_start_y + spacing*3 + 55, "Quit", app.destroy)


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

#class PlaceholderOnline(PlaceholderBase):
#    name = "online"
#    _title = "Online"

#Entry point
if __name__ == "__main__":
    Menu().mainloop()
