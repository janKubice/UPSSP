import socket

class Client:
    def __init__(self, name) -> None:
        self.HOST = '127.0.0.1'  # The server's hostname or IP address
        self.PORT = 10000        # The port used by the server
        self.name = name
        self.id = self.get_id()


    def send_test(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b'Hello, world')
            data = s.recv(1024)

        print('Received', repr(data))

    def recieve_from_server(self):
        """Přijímání zpráv ze serveru
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            data = s.recv(1024)
    
    def request_id_player(self):
        """Žádá server o přiřazení id hráče
            Returns: id_hráče
        """
        pass

    def connect_to_game(self, id_game):
        """připojení do hry, vrací True/False
            returns: True/False
        """
        pass

    def reconnect_to_game(self, id_game):
        """Znovu připojení do hry
            return: True/False
        """
        pass

    def create_new_game(self):
        """Vytvoří novou hru
            return: Id_hry
        """
        pass

    def start_new_game(self):
        """Startne novou hru = vygenerování otázek
            return: True/False
        """
        pass

    def send_quiz_answer(self, answer):
        """Odešle na server odpověď na otázku

        Args:
            answer a,b,c,d = co odpověděl
        return: true/false = zda bylo odpověď přijatá serverem
        """
        pass

    def pause_game(self):
        """Pauznutí hry
            Return: True/False
        """
        pass

    def leave_game(self):
        """Opuštění hry
        """
        pass

    
 