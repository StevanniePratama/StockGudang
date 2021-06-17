import tkinter as tk
from PIL import Image, ImageTk

class Page01(tk.Frame) :

	def __init__(self, parent, App) :

		self.app = App
		self.settings = App.settings

		super().__init__(parent)
		self.configure(bg="black")
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.main_frame = tk.Frame(self, height=self.settings.width, width=self.settings.width, bg="black")
		self.main_frame.pack(expand=True)

		self.top_label = tk.Label(self.main_frame, text="Verifikasi Lanjutan", font=("Comic Sans Ms", 30, "bold"), bg="Black", fg="Brown")
		self.top_label.pack(pady=2) 

		frame_w = self.settings.width

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio/3),int(i_h/ratio/3))
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.logo = ImageTk.PhotoImage(image)
		self.label_logo = tk.Label(self.main_frame, image=self.logo)
		self.label_logo.pack(pady=5)

		self.welcome_label = tk.Label(self.main_frame, text="Hello!!! Welcome Back Admin", font=("Arial", 20, "bold"), bg="black", fg="orange")
		self.welcome_label.pack(pady=0)

		self.password_label = tk.Label(self.main_frame, text="Please... input your password", font=("Arial", 16, "bold"), bg="black", fg="orange")
		self.password_label.pack(pady=2)

		self.var_password = tk.StringVar()
		self.input_password = tk.Entry(self.main_frame, font=("Comic Sans MS", 15),  textvariable=self.var_password, show="*")
		self.input_password.pack(pady=10)

		self.btn_login = tk.Button(self.main_frame, text="LOGIN", font=("Arial", 18, "bold"), command=lambda:self.app.window.auth_login_password(), bd=2)
		self.btn_login.pack(pady=7)


	def setToEmptyEntry(self) :
		self.var_password.set("")
		self.input_password.configure(textvariable = self.var_password)