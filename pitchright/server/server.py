import random
import socket
import string
import threading

from packet import Packet, PacketFactory


class Lobby:
    def __init__(self, code, initial_client):
        self.code = code
        self.initial_client = initial_client
        self.other = None

    def dispatch(self, sock):
        c1_ip, c1_port = self.initial_client
        c2_ip, c2_port = self.other

        sock.sendto(PacketFactory.create_p2p_start_packet(c1_ip, c1_port, 5002), self.other)
        sock.sendto(PacketFactory.create_p2p_start_packet(c2_ip, c2_port, 5002), self.initial_client)


class Server:
    def __init__(self, p):
        self.port = p
        self.lobbies = {}
        self.sock = None

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.port))

        while True:
            data, address = self.sock.recvfrom(128)

            packet = Packet(data, address)
            t = threading.Thread(target=self.process_packet, args=(packet,))
            t.start()

    def create_lobby_code(self):
        lobby_code = ''
        while True: # O(inf) for the win
            lobby_code = ''.join(random.choice(string.ascii_uppercase) for i in range(5))
            if self.lobbies.get(lobby_code) is None:
                break
        return lobby_code

    def process_packet(self, packet):
        if packet.is_create():
            code = self.create_lobby_code()
            lobby = Lobby(code, packet.address)
            print("Creating lobby with code: " + code)
            self.lobbies[code] = lobby
            self.sock.sendto(PacketFactory.create_new_lobby_packet(code), packet.address)
        elif packet.is_ack():
            # handle ack
            pass
        elif packet.is_join():
            code = packet.get_lobby_code()
            if self.lobbies.get(code) is None:
                self.sock.sendto(PacketFactory.create_invalid_lobby_packet(), packet.address)
                return
            print("Joining lobby with code: " + code)
            self.lobbies[code].other = packet.address
            self.lobbies[code].dispatch()


s = Server(2082)
s.run()


