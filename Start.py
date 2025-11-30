import tkinter as tk
from tkinter import ttk, messagebox
import requests
import hashlib
from PIL import Image, ImageTk

# Server IP, register, and login connection for VM server
PI_SERVER_URL = "http://192.168.1.153:5000"
REGISTER_ENDPOINT = f"{PI_SERVER_URL}/register"
LOGIN_ENDPOINT = f"{PI_SERVER_URL}/login"

# Path to the background image
BG_IMAGE_PATH = "C:/Users/natha/Downloads/DoubleJump-main (1)/DoubleJump-main/sprites/cyber dice.jpg"

class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checkers Login")
        self.geometry("800x600")
        self.resizable(False, False)
        self.configure(bg='black')
        self.current_view = "login"
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        # Load background
        self.setup_background()

        # Main GUI
        self.container = tk.Frame(self, bg="#1a1a1a", bd=2, relief="ridge")  # Dark gray for visibility
        self.container.place(relx=0.5, rely=0.5, anchor='center')
        self.container.config(width=320, height=380)

        # Build views
        self.build_login_view()
        self.build_register_view()

        # Start with login screen
        self.show_login()
        self.focus_set()

    # Creates initial background
    def setup_background(self):
        try:
            pil_image = Image.open(BG_IMAGE_PATH)
            pil_image = pil_image.resize((800, 600), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(pil_image)
            bg_label = tk.Label(self, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
            bg_label.image = self.bg_image  # Ref to prevent GC
        except Exception as e:
            print(f"BG load error: {e}")

    def build_login_view(self):
        self.login_frame = tk.Frame(self.container, bg="#1a1a1a")
        self.login_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title coloring Cyan
        title = tk.Label(self.login_frame, text="LOGIN", font=("Arial", 24, "bold"), fg="#00FFFF", bg="#1a1a1a")
        title.pack(pady=10)

        # Username label & entry
        user_label = tk.Label(self.login_frame, text="Username:", font=("Arial", 12), fg="white", bg="#1a1a1a")
        user_label.pack(pady=5)
        user_entry = tk.Entry(self.login_frame, textvariable=self.username_var, width=25, bg="white", fg="black", font=("Arial", 10))
        user_entry.pack(pady=5)

        # Password label & entry
        pass_label = tk.Label(self.login_frame, text="Password:", font=("Arial", 12), fg="white", bg="#1a1a1a")
        pass_label.pack(pady=5)
        pass_entry = tk.Entry(self.login_frame, textvariable=self.password_var, width=25, show="*", bg="white", fg="black", font=("Arial", 10))
        pass_entry.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.login_frame, bg="#1a1a1a")
        button_frame.pack(pady=20)
        login_btn = tk.Button(button_frame, text="Login", command=self.handle_login, bg="#333333", fg="white", font=("Arial", 10, "bold"), activebackground="#00FFFF", activeforeground="black", width=10)
        login_btn.pack(side=tk.LEFT, padx=5)
        register_btn = tk.Button(button_frame, text="Create Account", command=self.switch_to_register, bg="#333333", fg="white", font=("Arial", 10, "bold"), activebackground="#FF0000", activeforeground="white", width=12)
        register_btn.pack(side=tk.LEFT, padx=5)

        # Enter button binding
        self.login_frame.bind('<Return>', lambda e: self.handle_login())

    # registration input screen
    def build_register_view(self):
        self.register_frame = tk.Frame(self.container, bg="#1a1a1a")
        self.register_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title colored neon red
        title = tk.Label(self.register_frame, text="CREATE ACCOUNT", font=("Arial", 20, "bold"), fg="#FF0000", bg="#1a1a1a")
        title.pack(pady=10)

        # Username label & entry
        user_label = tk.Label(self.register_frame, text="Username:", font=("Arial", 12), fg="white", bg="#1a1a1a")
        user_label.pack(pady=5)
        user_entry = tk.Entry(self.register_frame, textvariable=self.username_var, width=25, bg="white", fg="black", font=("Arial", 10))
        user_entry.pack(pady=5)

        # Password label & entry
        pass_label = tk.Label(self.register_frame, text="Password:", font=("Arial", 12), fg="white", bg="#1a1a1a")
        pass_label.pack(pady=5)
        pass_entry = tk.Entry(self.register_frame, textvariable=self.password_var, width=25, show="*", bg="white", fg="black", font=("Arial", 10))
        pass_entry.pack(pady=5)

        # Confirm label & entry
        confirm_label = tk.Label(self.register_frame, text="Confirm Password:", font=("Arial", 12), fg="white", bg="#1a1a1a")
        confirm_label.pack(pady=5)
        confirm_entry = tk.Entry(self.register_frame, textvariable=self.confirm_password_var, width=25, show="*", bg="white", fg="black", font=("Arial", 10))
        confirm_entry.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.register_frame, bg="#1a1a1a")
        button_frame.pack(pady=20)
        reg_btn = tk.Button(button_frame, text="Register", command=self.handle_register, bg="#333333", fg="white", font=("Arial", 10, "bold"), activebackground="#00FFFF", activeforeground="black", width=10)
        reg_btn.pack(side=tk.LEFT, padx=5)
        back_btn = tk.Button(button_frame, text="Back to Login", command=self.switch_to_login, bg="#333333", fg="white", font=("Arial", 10, "bold"), activebackground="#FF0000", activeforeground="white", width=12)
        back_btn.pack(side=tk.LEFT, padx=5)

        # Bind Enter
        self.register_frame.bind('<Return>', lambda e: self.handle_register())

    def show_login(self):
        if hasattr(self, 'register_frame'):
            self.register_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def switch_to_register(self):
        print("Switching to register...")  # Debug
        self.current_view = "register"
        self.login_frame.pack_forget()
        self.register_frame.pack(fill="both", expand=True)
        self.username_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("")

    def switch_to_login(self):
        print("Switching to login...")  # Debug
        self.current_view = "login"
        self.register_frame.pack_forget()
        self.show_login()
        self.username_var.set("")
        self.password_var.set("")
    # Encrypts password to SHA256 for database storage
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    #
    def handle_login(self):
        print("Login clicked!")  # Debug
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return
        hashed_password = self.hash_password(password)
        try:
            response = requests.post(LOGIN_ENDPOINT, json={"username": username, "password": hashed_password}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    messagebox.showinfo("Success", "Login successful! Starting game...")
                    self.start_game()
                else:
                    messagebox.showerror("Error", data.get("message", "Invalid credentials."))
            else:
                messagebox.showerror("Error", f"Server error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")

    def handle_register(self):
        print("Register clicked!")  # Debug
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters.")
            return
        hashed_password = self.hash_password(password)
        try:
            response = requests.post(REGISTER_ENDPOINT, json={"username": username, "password": hashed_password}, timeout=5)
            if response.status_code == 201:
                data = response.json()
                if data.get("success"):
                    messagebox.showinfo("Success", "Account created! Please login.")
                    self.switch_to_login()
                else:
                    messagebox.showerror("Error", data.get("message", "Registration failed."))
            elif response.status_code == 409:
                messagebox.showerror("Error", "Username already exists.")
            else:
                messagebox.showerror("Error", f"Server error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")

    def start_game(self):
        print("Starting game...")  # Debug
        self.destroy()
        try:
            from game_initializer import GameInitializer
            game_init = GameInitializer()
            result = game_init.run()
            if result == "quit":
                self.quit()
        except ImportError as e:
            print(f"Game import error: {e}")
            messagebox.showerror("Error", "Game initializer not found. Check imports.")
            self.quit()
# Run login screen
if __name__ == "__main__":
    app = LoginScreen()
    app.mainloop()