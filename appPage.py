import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import sys

class AppPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings
		self.current_stock = self.settings.stocks[0]
		self.last_current_stock_index = 0
		self.append_new = []
		self.update_mode = False
		self.stocks_index = []


		super().__init__(parent) # window.conteiner
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_left_right_frame()


	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg="pink")
		self.left_frame.grid(row=0, column=0, sticky="nsew")
		self.create_left_header()
		self.create_left_content()

	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg="white", width=2*self.settings.width//3)
		self.right_frame.grid(row=0, column=1, sticky="nsew")
		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()

	def config_left_right_frame(self):
		self.grid_columnconfigure(0, weight=1) # 1/3
		self.grid_columnconfigure(1, weight=2) # 2/3
		self.grid_rowconfigure(0, weight=1)

	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5
		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_header.pack()

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio),int(i_h/ratio)) #(x,y)
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.logo)
		self.label_logo.pack()

		self.searchbox_frame = tk.Frame(self.left_header, bg="white", width=frame_w, height=frame_h//4)
		self.searchbox_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.searchbox_frame, bg="white", fg="black", font=("Arial", 14), textvariable=self.entry_search_var)
		self.entry_search.grid(row=0, column=0)

		self.button_search = tk.Button(self.searchbox_frame, bg="white", fg="black", font=("Arial", 14), text="Find", command=self.clicked_search_btn)
		self.button_search.grid(row=0, column=1)

		self.searchbox_frame.grid_columnconfigure(0, weight=3) # 3/4
		self.searchbox_frame.grid_columnconfigure(1, weight=1) # 1/4

	def show_stocks_in_listBox(self):
		stocks = self.settings.stocks
		
		for index in self.stocks_index:
			stock = stocks[index]
			for key, value in stock.items():
				full_name = f"{value['nama']}"
				self.stock_listBox.insert("end", full_name)

	def show_all_stocks_in_listBox(self) :
		stocks = self.settings.stocks

		self.stocks_index = []
		counter_index=0
		for stock in stocks :
			self.stocks_index.append(counter_index)
			counter_index += 1
		
		self.show_stocks_in_listBox()

	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = 4*self.settings.height//5

		self.left_content = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_content.pack(fill="x")

		self.stock_listBox = tk.Listbox(self.left_content, bg="white", fg="black", font=("Arial", 12), height=frame_h)
		self.stock_listBox.pack(side="left", fill="both", expand=True)

		self.stocks_scroll = tk.Scrollbar(self.left_content)
		self.stocks_scroll.pack(side="right", fill="y")

		stocks = self.settings.stocks
		counter_index = 0
		for stock in stocks:
			self.stocks_index.append(counter_index)
			counter_index += 1

		self.show_stocks_in_listBox()

		self.stock_listBox.configure(yscrollcommand=self.stocks_scroll.set)
		self.stocks_scroll.configure(command=self.stock_listBox.yview)

		self.stock_listBox.bind("<<ListboxSelect>>", self.clicked_item_in_Listbox)


	def clicked_item_in_Listbox(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try:
				index_item = selection[0]
			except IndexError:
				index_item = self.last_current_stock_index
			index = self.stocks_index[index_item]
			self.last_current_stock_index = index
			print(index_item,"=>",index)
			self.current_stock = self.settings.stocks[index]
			for codeNumber, info in self.current_stock.items(): #codeNumber -> Key, info -> Value
				code = codeNumber
				full_name = info['nama']
				tanggal_produksi = info['tanggal_produksi']
				tanggal_exp = info['tanggal_exp']
				lisensi_produk = info['lisensi_produk']
				NET = info['berat_bersih/NET']
				stock_barang = info['stock_barang']
				harga_beli = info['harga_beli']
				harga_jual = info['harga_jual']
				lokasi = info['lokasi']
				tanggal_masuk = info['tanggal_masuk']
			#print(stock)
			self.full_name_label.configure(text=full_name)
			self.table_info[0][1].configure(text=code)
			self.table_info[1][1].configure(text=tanggal_produksi)
			self.table_info[2][1].configure(text=tanggal_exp)
			self.table_info[3][1].configure(text=lisensi_produk)
			self.table_info[4][1].configure(text=NET)
			self.table_info[5][1].configure(text=stock_barang)
			self.table_info[6][1].configure(text=harga_beli)
			self.table_info[7][1].configure(text=harga_jual)
			self.table_info[8][1].configure(text=lokasi)
			self.table_info[9][1].configure(text=tanggal_masuk)


	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_header.pack()
		self.create_detail_right_header()

	def create_detail_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="white")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		data = list(self.current_stock.values())[0]
		full_name = f"{data['nama']}"
		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.full_name_label = tk.Label(self.detail_header, text=full_name, font=("Arial", 30, "bold"), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg="white")
		self.full_name_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)

	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_content.pack(expand=True)
		self.create_detail_right_content()


	def create_detail_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		for codeNumber, info in self.current_stock.items():
			info = [
				['Code : ', codeNumber],
				['Tanggal Produksi : ', info['tanggal_produksi']],
				['Tanggal Exp : ', info['tanggal_exp']],
				['Lisensi Produk : ', info['lisensi_produk']],
				['Berat Bersih / NET : ', info['berat_bersih/NET']],
				['Stock Barang : ', info['stock_barang']],
				['Harga Beli : ', info['harga_beli']],
				['Harga Jual : ', info['harga_jual']],
				['Lokasi : ', info['lokasi']],
				['Tanggal Masuk : ', info['tanggal_masuk']]

			]

		self.table_info = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 12), bg="white")
				aRow.append(label)
				if column == 0:
					sticky = "e"
				else:
					sticky = "w"
				label.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)



		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)


	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_footer.pack()
		self.create_detail_right_footer()

	def create_detail_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update', 'Delete', 'Add New']
		commands = [self.clicked_update_btn, self.clicked_delete_btn, self.clicked_add_new_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def recreate_right_frame(self):
		self.detail_update_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()

	def clicked_update_btn(self):
		self.update_mode = True

		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="white")
		self.detail_update_header.grid(row=0, column=0, sticky="nsew")

		data = list(self.current_stock.values())[0]
		full_name = f"{data['nama']}"
		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.full_name_label = tk.Label(self.detail_update_header, text=full_name, font=("Arial", 30, "bold"), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg="white")
		self.full_name_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for codeNumber, info in self.current_stock.items():
			info = [
				['Nama :', info['nama']],
				['Code : ', codeNumber],
				['Tanggal Produksi : ', info['tanggal_produksi']],
				['Tanggal Exp : ', info['tanggal_exp']],
				['Lisensi Produk : ', info['lisensi_produk']],
				['Berat Bersih / NET : ', info['berat_bersih/NET']],
				['Stock Barang : ', info['stock_barang']],
				['Harga Beli : ', info['harga_beli']],
				['Harga Jual : ', info['harga_jual']],
				['Lokasi : ', info['lokasi']],
				['Tanggal Masuk : ', info['tanggal_masuk']]
			]

		self.table_info = []
		self.entry_update_stock_vars = []
		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					entry = tk.Entry(self.detail_update_content,font=("Arial", 12), bg="white", textvariable=entry_var)
					entry.insert(0, info[row][column])
					aRow.append(entry)
					self.entry_update_stock_vars.append(entry_var)
					entry.grid(row=row, column=column, sticky=sticky)
					sticky = "w"
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_stock_btn, self.clicked_cancel_stock_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", font=("Arial", 15, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)


	def clicked_delete_btn(self):
		stocks = self.settings.stocks
		index = self.last_current_stock_index

		respond = messagebox.askyesnocancel("Delete Item", "Are You sure to delete this item ?")
		if respond :
			del stocks[int(index)]
			self.settings.save_data_to_json()

		self.stock_listBox.delete(0, 'end')
		self.show_all_stocks_in_listBox()


	def clicked_add_new_btn(self):
		self.update_mode = True

		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="white")
		self.detail_update_header.grid(row=0, column=0, sticky="nsew")

		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.top_label = tk.Label(self.detail_update_header, text="New Item", font=("Arial", 20, "bold"), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg="white")
		self.top_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for codeNumber, info in self.current_stock.items():
			info = [
				['Nama :', info['nama']],
				['Code : ', codeNumber],
				['Tanggal Produksi : ', info['tanggal_produksi']],
				['Tanggal Exp : ', info['tanggal_exp']],
				['Lisensi Produk : ', info['lisensi_produk']],
				['Berat Bersih / NET : ', info['berat_bersih/NET']],
				['Stock Barang : ', info['stock_barang']],
				['Harga Beli : ', info['harga_beli']],
				['Harga Jual : ', info['harga_jual']],
				['Lokasi : ', info['lokasi']],
				['Tanggal Masuk : ', info['tanggal_masuk']]
			]

		self.table_info = []
		self.entry_addnew_stock_vars = []
		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					entry = tk.Entry(self.detail_update_content,font=("Arial", 12), bg="white", textvariable=entry_var)
					aRow.append(entry)
					self.entry_addnew_stock_vars.append(entry_var)
					entry.grid(row=row, column=column, sticky=sticky)
					sticky = "w"
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_new_stock_btn, self.clicked_cancel_stock_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", font=("Arial", 15, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def clicked_save_new_stock_btn(self) :
		self.update_mode = False

		confirmed = messagebox.askyesnocancel("stockapp Confirmation", "Are you sure to add this new stock?")

		nama = self.entry_addnew_stock_vars[0].get()
		code = self.entry_addnew_stock_vars[1].get()
		tanggal_produksi = self.entry_addnew_stock_vars[2].get()
		tanggal_exp = self.entry_addnew_stock_vars[3].get()
		lisensi_produk = self.entry_addnew_stock_vars[4].get()
		NET = self.entry_addnew_stock_vars[5].get()
		stock_barang= self.entry_addnew_stock_vars[6].get()
		harga_beli = self.entry_addnew_stock_vars[7].get()
		harga_jual = self.entry_addnew_stock_vars[8].get()
		lokasi = self.entry_addnew_stock_vars[9].get()
		tanggal_masuk = self.entry_addnew_stock_vars[10].get()

		if confirmed and code and nama :
			self.append_new = {
				code : {
					"nama" : nama,
					"tanggal_produksi" : tanggal_produksi,
					"tanggal_exp" : tanggal_exp,
					"lisensi_produk" : lisensi_produk,
					"berat_bersih/NET" : NET,
					"stock_barang" : stock_barang,
					"harga_beli" : harga_beli,
					"harga_jual" : harga_jual,
					"lokasi" : lokasi,
					"tanggal_masuk" : tanggal_masuk
					}
				}

			self.settings.stocks.append(self.append_new)
			self.settings.save_data_to_json()
			index = len(self.settings.stocks) - 1
			self.last_current_stock_index = index
			self.current_stock = self.settings.stocks[self.last_current_stock_index]
		else:
			info = messagebox.showinfo("StockApp Confirmation", "Nothing To Save.")

		self.recreate_right_frame()
		self.stock_listBox.delete(0, 'end')
		self.show_all_stocks_in_listBox()


	def clicked_save_stock_btn(self):
		self.update_mode = False

		confirmed = messagebox.askyesnocancel("stockapp Conrifmation", "Are you sure to update this stock?")

		if confirmed:
			nama = self.entry_update_stock_vars[0].get()
			code = self.entry_update_stock_vars[1].get()
			tanggal_produksi = self.entry_update_stock_vars[2].get()
			tanggal_exp = self.entry_update_stock_vars[3].get()
			lisensi_produk = self.entry_update_stock_vars[4].get()
			NET = self.entry_update_stock_vars[5].get()
			stock_barang= self.entry_update_stock_vars[6].get()
			harga_beli = self.entry_update_stock_vars[7].get()
			harga_jual = self.entry_update_stock_vars[8].get()
			lokasi = self.entry_update_stock_vars[9].get()
			tanggal_masuk = self.entry_update_stock_vars[10].get()

			self.settings.stocks[self.last_current_stock_index] = {
				code : {
					"nama" : nama,
					"tanggal_produksi" : tanggal_produksi,
					"tanggal_exp" : tanggal_exp,
					"lisensi_produk" : lisensi_produk,
					"berat_bersih/NET" : NET,
					"stock_barang" : stock_barang,
					"harga_beli" : harga_beli,
					"harga_jual" : harga_jual,
					"lokasi" : lokasi,
					"tanggal_masuk" : tanggal_masuk
					}
				}

			self.current_stock = self.settings.stocks[self.last_current_stock_index]

		self.settings.save_data_to_json()

		self.recreate_right_frame()
		self.stock_listBox.delete(0, 'end')
		self.show_all_stocks_in_listBox()

	def clicked_cancel_stock_btn(self):
		self.update_mode = False

		self.recreate_right_frame()

	def clicked_search_btn(self):
		item_search = self.entry_search_var.get()
		if item_search:
			stocks = self.settings.stocks
			self.stocks_index = []
			counter_index = 0
			for stock in stocks:
				for codeNumber, info in stock.items():
					if item_search in codeNumber:
						self.stocks_index.append(counter_index) #stocks.index(stock)
					for info_key, info_value in info.items():
						if item_search in info_value:
							self.stocks_index.append(counter_index) #stocks.index(stock)
				counter_index += 1
			self.stock_listBox.delete(0, 'end')
			self.show_stocks_in_listBox()

		else :
			self.stock_listBox.delete(0, 'end')
			self.show_all_stocks_in_listBox()