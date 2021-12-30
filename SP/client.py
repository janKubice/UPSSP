import socket
from msg_codes import *

class Client:
    def __init__(self, name) -> None:
        self.HOST = '127.0.0.1'  # The server's hostname or IP address
        self.PORT = 10000        # The port used by the server
        self.name = name
        self.id = -1
        #socket který se připojí na server
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect((self.HOST, self.PORT))


    def send_test(self):
        self.soc.sendall(b'Hello, world')

    def send_msg(self, msg_code, msg_param = ''):
        self.soc.sendall(f'{self.id}|{msg_code}|{msg_param}'.encode())

    def recieve_from_server(self):
        """Přijímání zpráv ze serveru
        """
        while(True):
            try:
                data = self.soc.recv(1024)
            except:
                print('Chyba')

            if len(data) == 0:
                continue

	    #data = data.decode('UTF-8')
	    
            data = data.split('|')
            msg_code = int(data[0])
            if msg_code == REQ_ID:
                self.set_player_id(int(data[1]))
            elif msg_code == CONNECT_TO_GAME:
                pass
            elif msg_code == RECONNECT_TO_GAME:
                pass
            elif msg_code == CREATE_NEW_GAME:
                pass
            elif msg_code == START_NEW_GAME:
                pass
            elif msg_code == SEND_QUIZ_ANSWER:
                pass
            elif msg_code == PAUSE_GAME:
                pass
            elif msg_code == LEAVE_GAME:
                pass
            else:
                print('chybný kód')

    def request_id_player(self):
        """Žádá server o přiřazení id hráče
            Returns: id_hráče
        """
        self.send_msg(str(REQ_ID))

    def set_player_id(self, id):
        if id == None or id == -1:
            return

        self.id = id

    def connect_to_game(self, id_game):
        """připojení do hry, vrací True/False
            returns: True/False
        """
        self.send_msg(str(REQ_ID), str(id_game))

    

    def reconnect_to_game(self, id_game):
        """Znovu připojení do hry
            return: True/False
        """
        self.send_msg(str(RECONNECT_TO_GAME), str(id_game))

    def create_new_game(self):
        """Vytvoří novou hru
            return: Id_hry
        """
        self.send_msg(str(CREATE_NEW_GAME))

    def start_new_game(self):
        """Startne novou hru = vygenerování otázek
            return: True/False
        """
        self.send_msg(str(CREATE_NEW_GAME))

    def send_quiz_answer(self, answer):
        """Odešle na server odpověď na otázku

        Args:
            answer a,b,c,d = co odpověděl
        return: true/false = zda bylo odpověď přijatá serverem
        """
        self.send_msg(str(SEND_QUIZ_ANSWER), answer)

    def pause_game(self):
        """Pauznutí hry
            Return: True/False
        """
        self.send_msg(str(PAUSE_GAME))

    def leave_game(self):
        """Opuštění hry
        """
        self.send_msg(str(LEAVE_GAME))

    
 
