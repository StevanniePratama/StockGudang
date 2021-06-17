from json import load, dump

class Settings :

	def __init__(self) :

		#App Conf
		self.title = "Stock"

		#Window Conf
		base = 50
		ratio = (16, 9)
		self.width = base*ratio[0]
		self.height = base*ratio[1]

		self.screen = f"{self.width}x{self.height}"

		#Img Logo
		self.logo = "img/logo.jpeg"
		
		self.login = None
		self.load_dataLogin_from_json()

		self.stocks = None
		self.load_data_from_json()

		self.admins = ["Sallini", "Stevannie"]

	def login_username(self, username) :
		users = self.admins
		if username in users :
			return True
		else :
			return False

	def login_password(self, username, password) :
		if username == "Sallini" :
			if password == "23456" :
				return True
			else :
				return False
		if username == "Stevannie" :
			if password == "113333" :
				return True
			else :
				return False
		else :
			return False

	def load_dataLogin_from_json(self) :
		with open("data/login.json", "r") as json_file :
			self.login = load(json_file)

	def save_dataLogin_to_json(self) :
		with open("data/login.json", "w") as json_file :
			dump(self.login, json_file)

	def load_data_from_json(self) :
		with open("data/stocks.json", "r") as json_file :
			self.stocks = load(json_file)

	def save_data_to_json(self) :
		with open("data/stocks.json", "w") as json_file :
			dump(self.stocks, json_file)

			