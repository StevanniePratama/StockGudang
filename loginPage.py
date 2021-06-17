import tkinter as tk
from PIL import Image, ImageTk

class LoginPage(tk.Frame) :

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

		self.stockapp_label = tk.Label(self.main_frame, text="Stock Gudang", font=("Comic Sans", 30), bg="Black", fg="Brown")
		self.stockapp_label.pack()

		self.version_label = tk.Label(self.main_frame, text="Admin Version", font=("Comic Sans", 20), bg="Black", fg="Brown")
		self.version_label.pack()

		frame_w = self.settings.width

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio/3),int(i_h/ratio/3))
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.logo = ImageTk.PhotoImage(image)
		self.label_logo = tk.Label(self.main_frame, image=self.logo)
		self.label_logo.pack(pady=15)

		self.username_label = tk.Label(self.main_frame, text="Admin Username : ", font=("Arial", 18, "bold"), bg="black", fg="orange")
		self.username_label.pack(pady=2)

		self.var_username = tk.StringVar()
		self.input_username = tk.Entry(self.main_frame, font=("Comic Sans MS", 16),  textvariable=self.var_username)
		self.input_username.pack(pady=10)

		self.btn_continue = tk.Button(self.main_frame, text="CONTINUE", font=("Arial", 18, "bold"), command=lambda:self.app.window.auth_login_username(), bd=2)
		self.btn_continue.pack(pady=10)

	def setToEmptyEntry(self) :
		self.var_username.set("")
		self.input_username.configure(textvariable = self.var_username)
