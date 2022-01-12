# Třída pro tvorbu GUI.
# @author Michaela Benešová
# @verze 1.0
# datum 12.01.2022

from tkinter import *
from client import Client
import threading
import sys

class Quiz:
	def __init__(self):
		""" Metoda, která se zavolá při inicializaci nového objektu.
		"""

		#klient
		self.client = Client(self)

		# vytvoření jednotlivých labelů a tlačítek
		self.right_btn = Button()
		self.left_btn = Button()
		self.text = Label()
		self.text_points = Label()
		self.text_another = Label()
		self.text_input = Entry()
		self.text_wrong = Label()
		self.opt_selected = IntVar()

		self.radio_buttons_array = []
		for i in range(4):
			radio_btn = Radiobutton(gui,text=" ",variable="", value = i+1,font = ("ariel",14))
			self.radio_buttons_array.append(radio_btn)


		self.display_title()
		self.display_menu()		

	def show_q(self, question, answers):
		""" Zavolá potřebné metody pro zobrazení otázky a možných odpovědí a nadefinuje vzhled obrazovky.
		@param question = otázka
		@param answers = odpovědi
		"""

		self.right_btn.config(width=0, text='')
		self.right_btn.place(x=-100, y=-100)
		self.text_another.config(text='')
		self.text.config(text='')
		self.display_question(question)
		self.opt_selected=IntVar()
		self.radio_buttons()
		self.display_options(answers)
		self.buttons()


	def send_answer_btn(self):
		""" Odešlě odpověď na server.
		"""
		self.client.send_quiz_answer(self.opt_selected.get())

	def start_btn(self):
		""" Při spuštění hry vyžadá id pro hráče na serveru.
		"""
		self.client.request_id_player()

	def show_wrong_label(self, txt):
		""" Ukáže chybovou hlášku.
		@param txt = chybová hláška
		"""
		self.text_wrong.config(text=txt, width=60,font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		self.text_wrong.place(x=200, y=200)

	def buttons(self):
		""" Tlačítka pro uložení odpovědi a ukončení hry.
		"""
		self.right_btn.config(text="Ulozit odpoved",command=self.send_answer_btn, width=22, bg="red",fg="white",font=("ariel",16,"bold"))
		self.right_btn.place(x=350,y=300)

		quit_button = Button(gui, text="Quit", command=self.quit_game, width=5,bg="black", fg="white",font=("ariel",16," bold"))

		quit_button.place(x=700,y=50)

	def quit_game(self):
		""" Ukončení hry.
		"""
		self.client.leave_game()
		
		gui.destroy()
		sys.exit(0)

	def display_options(self, answers):
		""" Ukáže možné odpovědi.
		"""
		print(f"odpovedi: {answers}")
		val=0
		answers = answers.split('-')
		self.opt_selected.set(0)

		for idx, option in enumerate(answers):
			self.radio_buttons_array[idx]['text']=option
			val+=1

	def display_question(self, question):
		""" Zobrazí otázku.
		"""
		self.text.config(text=question, width=60,font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
	
	def display_answer(self, answer, points):
		""" Zobrazí správnou odpověď a body.
		"""
		self.text.config(text=f"Správná odpověď: {answer}.", width=60,font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		self.text_points.config(text=f"Body: {points}.", width=60,font=( 'ariel' ,16, 'bold' ), anchor= 'w' )


	def display_menu(self):
		""" Zobrazí menu.
		"""
		if self.client.connect():
			thread = threading.Thread(target=self.client.recieve_from_server)
			thread.start()

		self.text = Label(gui, text="Menu", width=60, font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		self.text.place(x=350, y=100)

		self.text_points.config(text="", width=60,font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		
		self.right_btn.config(text="Připojit se na server", command= lambda: self.client.request_id_player(), width=20, height=1,bg="red",fg="white",font=("ariel",16,"bold"))
		self.right_btn.place(x=400,y=380)

	def display_room(self, num_players, admin, id = ''):
		""" Zobrazí lobby.
		@param num_players = počet hráčů
		@param admin (boolean) = zda je nebo není admin
		@param id = id lobby, zobrazuje se jen adminovi
		"""

		if admin:
			self.text.config(text=f"Room ID - {id}\nPlayers: {num_players}/3", width=60, font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		else:
			self.text.config(text=f"Room\nPlayers: {num_players}/3", width=60, font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		
		self.text.place(x=350, y=100)

		self.left_btn.config(width=0, text='')
		self.left_btn.place(x=-100, y=-100)

		self.text_points.config(text="Body: 0", width=60,font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		self.text_points.place(x=200,y=200)

		self.text_input.place(x=-100, y=-100)
		self.right_btn.place(x=-100, y=-100)

		if admin:
			self.right_btn.config(text="Start game",command=self.client.start_game, width=45,bg="red",fg="white",font=("ariel",16,"bold"))
			self.right_btn.place(x=50,y=380)
		else:
			self.text_another.config(text="A teď počkej na zahájení hry adminem.", width=60, font=( 'ariel' ,22, 'bold' ), anchor= 'w' )
			self.text_another.place(x=50,y=380)

	def show_score(self, msg:str):
		""" Zobrazí větu zda vyhrál či nevyhrál uživatel.
		"""
		self.text.config(text=msg, width=60, font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		self.right_btn.config(text="Vrátit se do menu",command=self.back_to_menu, width=45,bg="red",fg="white",font=("ariel",16,"bold"))

	def back_to_menu(self):
		""" Vrátí do menu.
		"""
		for idx, btn in enumerate(self.radio_buttons_array):
			btn.config(text=" ",variable=self.opt_selected, value = idx+1,font = ("ariel",14))
			btn.place(x = 10000, y = 1000)
		self.display_menu()
		self.connect_input()

	def connect_input(self):
		""" Připojení do místnosti či vytvoření místnosti.
		"""
		self.text_input.place(x=350,y=250)

		self.text_another.config(text='')
		self.text.config(text='Menu\n                   ')

		self.right_btn.config(text="Připojit se do místnosti",command= lambda: self.client.connect_to_game(self.text_input.get()), width=20, height=1,bg="purple",fg="white",font=("ariel",16,"bold"))
		self.left_btn.config(text="Vytvořit místnost",command= lambda: self.client.create_new_room(), width=20, height=1,bg="purple",fg="white",font=("ariel",16,"bold"))
		self.right_btn.place(x=400,y=420)
		self.left_btn.place(x=50,y=420)


	def display_title(self):
		""" Zobrazení nadpisu kvízu.
		"""
		title = Label(gui, text="Kvíz", width=50, bg="pink",fg="white", font=("ariel", 20, "bold"))
		title.place(x=0, y=2)



	def radio_buttons(self):
		""" Tlačítka ve stylu radio pro odpovědi.
		"""
		y_pos = 150
		
		for idx, btn in enumerate(self.radio_buttons_array):
			btn.config(text=" ",variable=self.opt_selected, value = idx+1,font = ("ariel",14))
			btn.place(x = 100, y = y_pos)
			y_pos += 40
		
	def close_window(self):
		self.quit_game()
		


#vytvoří gui
gui = Tk()

#nastaví velikost
gui.geometry("820x460")

#zobrazí název
gui.title("Kvízeček")

#vytvoří objekt
quiz = Quiz()
gui.protocol("WM_DELETE_WINDOW", quiz.close_window)

#zapne gui
gui.mainloop()


