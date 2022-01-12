import socket
from msg_codes import *

class Client:
    def __init__(self, name, gui) -> None:
        self.HOST = '127.0.0.1'  # The server's hostname or IP address
        self.PORT = 10000        # The port used by the server
        self.name = name
        self.id = -1
        self.gui = gui
        # socket který se připojí na server

    def connect(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.connect((self.HOST, self.PORT))
            return True
        except:
            self.receive_wrong("server nefrčí, zkus hru zapnout déle")
            return False

    def send_test(self):
        self.soc.sendall(b'Hello, world')

    def send_msg(self, msg_code, msg_param='x'):
        msg = f'{self.id},{msg_code},{msg_param}'
        print(f'Na server odesilam: {msg}')
        self.soc.sendall(msg.encode())

    def recieve_from_server(self):
        """Přijímání zpráv ze serveru
        """
        while(True):
            data = ''
            data = self.soc.recv(512)
            data = data.decode()
            print(f'Ze serveru dostavam: {data}')
            data = data.split(',')
            data = [s.rstrip('\x00') for s in data]
            msg_code = int(data[0])
            if msg_code == REQ_ID:
                self.set_player_id(int(data[1]))
            elif msg_code == CONNECT_TO_GAME:
                self.can_connect_to_game(data[1])
            elif msg_code == CREATE_NEW_ROOM:
                self.receive_create_new_room(data[1])
            elif msg_code == START_GAME:
                self.receive_start_game(data[1])
            elif msg_code == NEXT_QUESTION:
                self.receive_next_question(data[1])
            elif msg_code == SEND_QUIZ_ANSWER:
                self.receive_quiz_answer(data[1])
            elif msg_code == ERR:
                self.receive_wrong(data[1])
            elif msg_code == BACK_TO_MENU:
                self.receive_back_to_menu()
            elif msg_code == SHOW_TABLE:
                self.show_table(data[1])
            else:
                print('chybný kód')
        
    # metody, které přijímaj

    def can_connect_to_game(self, msg):
        """ Získá ze serveru odpověď, zda se hráč může či nemůže připojit
        """
        if int(msg) > 1:
            self.gui.display_room(int(msg), False)
        else:
            print('Moc lidí')

    def set_player_id(self, id):
        if id == None or id == -1:
            return
        print(f'Nastavuji id hráče na {id}')
        self.id = id
        self.gui.connect_input()

    # metody, které odesílaj
    def request_id_player(self):
        """Žádá server o přiřazení id hráče
            Returns: id_hráče
        """
        self.send_msg(str(REQ_ID))
        #self.set_player_id(2)

    def connect_to_game(self, id_game):
        """žádá o připojení do hry
        """
        self.send_msg(str(CONNECT_TO_GAME), str(id_game))

    def reconnect_to_game(self, id_game):
        """Znovu připojení do hry
            return: True/False
        """
        self.send_msg(str(RECONNECT_TO_GAME), str(id_game))

    def create_new_room(self):
        """Vytvoří novou hru
        """
        self.send_msg(str(CREATE_NEW_ROOM))

    def start_game(self):
        self.send_msg(str(START_GAME))

    def send_quiz_answer(self, answer):
        """Odešle na server odpověď na otázku

        Args:
            answer a,b,c,d = co odpověděl
        return: true/false = zda bylo odpověď přijatá serverem
        """
        self.send_msg(str(SEND_QUIZ_ANSWER), answer)

    def leave_game(self):
        """Opuštění hry
        """
        self.send_msg(str(LEAVE_GAME))

    def receive_create_new_room(self, msg):
        msg = msg.split(';')
        print(msg)
        if int(msg[0]) > -1:
            self.gui.display_room(msg[1], True, int(msg[0]))
        else:
            #TODO klidne udělat nejakou hlasku chybovou
            pass

    def receive_start_game(self, msg:str):
        msg = msg.split(';')
        self.gui.show_q(msg[0], msg[1])

    def receive_next_question(self, msg:str):
        msg = msg.split(';')
        self.gui.display_question(msg[0])
        self.gui.display_options(msg[1])

    def receive_quiz_answer(self, msg:str):
        msg = msg.split(';')
        self.gui.display_answer(msg[1], msg[0])

    def receive_wrong(self, msg:str):
        self.gui.show_wrong_label(msg)

    def receive_back_to_menu(self):
        self.gui.back_to_menu()

    def show_table(self, msg:str):
        self.gui.show_score(msg)

