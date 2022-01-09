# Python program to create a simple GUI
# Simple Quiz using Tkinter

#import everything from tkinter
from tkinter import *

# and import messagebox as mb from tkinter
from tkinter import messagebox as mb

#import json to use json file for data
import json
import threading
from client import Client

class Quiz:
	# This is the first method which is called when a
	# new object of the class is initialized. This method
	# sets the question count to 0. and initialize all the
	# other methoods to display the content and make all the
	# functionalities available
	def __init__(self, name):
		
		# set question number to 0
		self.q_no=0

		self.client = Client(name, self)
		#x = threading.Thread(target=self.client.recieve_from_server, args=())
		#x.start()
		#self.client.send_msg(1,'test')

		# assigns ques to the display_question function to update later.
		self.display_title()
		self.display_menu()

		self.right_btn = Button()
		self.left_btn = Button()
		self.text = Label()
		self.text_another = Label()
		self.text_input = Entry()
				

	def show_q(self, question, answers):
		self.right_btn.config(width=0, text='')
		self.right_btn.place(x=-100, y=-100)
		self.display_question(question)
		
		# opt_selected holds an integer value which is used for
		# selected option in a question.
		self.opt_selected=IntVar()
		
		# displaying radio button for the current question and used to
		# display options for the current question
		self.opts=self.radio_buttons()
		
		# display options for the current question
		self.display_options(answers)
		
		# displays the button for next and exit.
		self.buttons()
		
		# no of questions
		self.data_size=len(question)

	def send_answer_btn(self):
		self.client.send_quiz_answer(self.opt_selected.get())

	def start_btn(self):
		self.client.request_id_player()

	# This method shows the two buttons on the screen.
	# The first one is the next_button which moves to next question
	# It has properties like what text it shows the functionality,
	# size, color, and property of text displayed on button. Then it
	# mentions where to place the button on the screen. The second
	# button is the exit button which is used to close the GUI without
	# completing the quiz.
	def buttons(self):
		
		# The first button is the Next button to move to the
		# next Question
		self.right_btn.config(text="Uložit odpověď",command=self.send_answer_btn, width=10,bg="blue",fg="white",font=("ariel",16,"bold"))
		
		# palcing the button on the screen
		self.right_btn.place(x=350,y=380)
		
		# This is the second button which is used to Quit the GUI
		quit_button = Button(gui, text="Quit", command=gui.destroy,
		width=5,bg="black", fg="white",font=("ariel",16," bold"))
		
		# placing the Quit button on the screen
		quit_button.place(x=700,y=50)

	# This method deselect the radio button on the screen
	# Then it is used to display the options available for the current
	# question which we obtain through the question number and Updates
	# each of the options for the current question of the radio button.
	def display_options(self, answers):
		print(f"odpovedi: {answers}")
		val=0
		answers = answers.split('-')
		# deselecting the options
		self.opt_selected.set(0)
		
		# looping over the options to be displayed for the
		# text of the radio buttons.
		for option in answers:
			self.opts[val]['text']=option
			val+=1


	def display_question(self, question):
		self.text.config(text=question, width=60,font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
	
	def display_answer(self, answer):
		self.text.config(text=f"Správná odpověď: {answer}.", width=60,font=( 'ariel' ,16, 'bold' ), anchor= 'w' )

	def display_menu(self):
		self.client.connect()
		thread = threading.Thread(target=self.client.recieve_from_server)
		thread.start()

		self.text = Label(gui, text="Menu", width=60, font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		self.text.place(x=350, y=100)
		
		self.right_btn = Button(gui, text="Připojit se na server",command=self.client.request_id_player, width=20,bg="red",fg="white",font=("ariel",16,"bold"))
		self.right_btn.place(x=400,y=380)

	def display_room(self, num_players, admin, id = ''):
		if admin:
			self.text.config(text=f"Room ID - {id}\nPlayers: {num_players}/3", width=60, font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		else:
			self.text.config(text=f"Room\nPlayers: {num_players}/3", width=60, font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		
		self.text.place(x=350, y=100)

		self.left_btn.config(width=0, text='')
		self.left_btn.place(x=-100, y=-100)

		self.text_input.place(x=-100, y=-100)
		self.right_btn.place(x=-100, y=-100)

		if admin:
			self.right_btn.config(text="Start game",command=self.client.start_game, width=45,bg="red",fg="white",font=("ariel",16,"bold"))
			self.right_btn.place(x=50,y=380)
		else:
			self.text_another.config(text="A teď počkej na zahájení hry adminem.", width=60, font=( 'ariel' ,22, 'bold' ), anchor= 'w' )
			self.text_another.place(x=50,y=380)

	def hide_menu(self):
		pass

	def connect_input(self):
		self.text_input = Entry(gui)
		self.text_input.place(x=350,y=250)

		self.right_btn.configure(height=0, width=0)

		self.right_btn.config(text="Připojit se do místnosti",command= lambda: self.client.connect_to_game(self.text_input.get()), width=20,bg="purple",fg="white",font=("ariel",16,"bold"))
		self.left_btn.config(text="Vytvořit místnost",command= lambda: self.client.create_new_room(), width=20,bg="purple",fg="white",font=("ariel",16,"bold"))
		self.right_btn.place(x=400,y=380)
		self.left_btn.place(x=50,y=380)

	# This method is used to Display Title
	def display_title(self):
		
		# The title to be shown
		title = Label(gui, text="Kvíz", width=50, bg="pink",fg="white", font=("ariel", 20, "bold"))
		
		# place of the title
		title.place(x=0, y=2)


	# This method shows the radio buttons to select the Question
	# on the screen at the specified position. It also returns a
	# lsit of radio button which are later used to add the options to
	# them.
	def radio_buttons(self):
		
		# initialize the list with an empty list of options
		q_list = []
		
		# position of the first option
		y_pos = 150
		
		# adding the options to the list
		while len(q_list) < 4:
			
			# setting the radio button properties
			radio_btn = Radiobutton(gui,text=" ",variable=self.opt_selected,
			value = len(q_list)+1,font = ("ariel",14))
			
			# adding the button to the list
			q_list.append(radio_btn)
			
			# placing the button
			radio_btn.place(x = 100, y = y_pos)
			
			# incrementing the y-axis position by 40
			y_pos += 40
		
		# return the radio buttons
		return q_list

# Create a GUI Window
gui = Tk()

# set the size of the GUI Window
gui.geometry("800x450")

# set the title of the Window
gui.title("Kvízeček pro pindíkový královny")


# get the data from the json file
#with open('/home/jan/UPS/UPSSP/SP/data.json') as f:
#	data = json.load(f)

with open('/home/jan/Desktop/UPSSP-master/SP/data.json') as f:
	data = json.load(f)

# set the question, options, and answer
question = (data['question'])
options = (data['options'])
answer = (data['answer'])

# create an object of the Quiz Class.
quiz = Quiz("Pepa")

# Start the GUI
gui.mainloop()

# END OF THE PROGRAM
