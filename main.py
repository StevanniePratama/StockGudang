import tkinter as tk 
from tkinter import messagebox

import time
import sys
from datetime import datetime

from settings import Settings 
from loginPage import LoginPage
from page01 import Page01
from appPage import AppPage

class Window(tk.Tk) :

	def __init__(self, App) :
		self.app = App
		self.settings = App.settings

		self.username = None
		self.password = None

		super().__init__()
		self.title(self.settings.title)
		self.geometry(self.settings.screen)
		self.resizable = (0,0)

		self.create_menu()
		self.create_container()
		self.pages = {}
		
		waktu = datetime.now()
			
		menit = waktu.minute*60
		detik = waktu.second*1

		login_time = menit + detik
		logout_time = self.settings.login[0]
		durasi = login_time - logout_time

		if durasi >= 300 :
			self.create_appPage()
			self.create_page01()
			self.create_loginPage()
		
		else :
			self.create_appPage()


	def create_menu(self) :
		self.menuBar = tk.Menu(self)
		self.configure(menu=self.menuBar)

		self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
		self.fileMenu.add_command(label="Exit", command = self.clicked_exit_menu)

		self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
		self.helpMenu.add_command(label="About", command=self.clicked_about_menu)

		self.menuBar.add_cascade(label="Quit", menu=self.fileMenu)
		self.menuBar.add_cascade(label="Help", menu=self.helpMenu)


	def change_page(self, page) :
		page = self.pages[page]
		page.tkraise()

	def auth_login_username(self) :
		self.username = self.pages['loginPage'].var_username.get()

		granted = self.settings.login_username(self.username)
		
		if granted :
			self.change_page('page01')
		else :
			messagebox.showerror("Invalid Username", "Username not found")
			self.pages["loginPage"].setToEmptyEntry()

	def auth_login_password(self) :
		self.password = self.pages['page01'].var_password.get()

		print(f"password: {self.password}")

		granted = self.settings.login_password(self.username, self.password)
		
		if granted :
			self.change_page('appPage')
		else :
			messagebox.showwarning("WRONG PASSWORD", "Please.... CHECK your PASSWORD again!!")
			self.pages["page01"].setToEmptyEntry()

	def create_container(self):
		self.container = tk.Frame(self)
		self.container.pack(fill="both", expand=True)

	def create_appPage(self) :
		self.pages["appPage"] = AppPage(self.container, self.app)

	def create_loginPage(self) :
		self.pages['loginPage'] = LoginPage(self.container, self.app)

	def create_page01(self) :
		self.pages['page01'] = Page01(self.container, self.app)

	def clicked_about_menu(self) :
		messagebox.showinfo("About stockApp", "This App created by SALLINI & STEVANNIE")

	def clicked_exit_menu(self) :
		respond = messagebox.askyesnocancel("Exit Program", "Are You sure to close the program ?")
		
		if respond and self.username == None and self.password == None :
			sys.exit()
		else:
			waktu = datetime.now()
			
			menit = waktu.minute*60
			detik = waktu.second*1

			time = menit + detik

			self.settings.login.clear()
			self.settings.login.append(time)
			self.settings.save_dataLogin_to_json()

			sys.exit()


class StockBarang :

	def __init__ (self) :
		self.settings = Settings()
		self.window = Window(self)

	def run(self) :
		self.window.mainloop()

if __name__ == '__main__' :
	myApp = StockBarang()
	myApp.run()