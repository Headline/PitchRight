from enum import IntEnum
import ipaddress

class PacketType(IntEnum):
    ACK = 0xFF
    CREATE = 0xFE
    JOIN = 0xFD
    CONNECT = 0xFC
    P2P_START = 0xFB
    P2P_DATA = 0xFA
    CREATE_RESPONSE = 0xF9
    INVALID_LOBBY = 0xF8


class PacketFactory:
    @staticmethod
    def create_join_packet(lobby_code):
        return bytearray([PacketType.JOIN, lobby_code.encode()])
    @staticmethod
    def create_new_lobby_packet(lobby_code):
        return bytearray([PacketType.CREATE_RESPONSE, lobby_code.encode])
    @staticmethod
    def create_invalid_lobby_packet():
        return bytearray([PacketType.INVALID_LOBBY])
    @staticmethod
    def create_lobby():
        return bytearray([PacketType.CREATE])
    @staticmethod
    def create_p2p_start_packet(ip, port, knownport):
        ip = int(ipaddress.ip_address(ip))
        return bytearray([PacketType.P2P_START, ip, port, knownport])


class Packet:
    def __init__(self, bytes, address):
        self.bytes = bytes
        self.address = address

    def get_type(self):
        return self.bytes[0]

    def is_ack(self):
        return self.bytes[0] == PacketType.ACK

    def is_create(self):
        return self.bytes[0] == PacketType.CREATE

    def is_join(self):
        return self.bytes[0] == PacketType.JOIN

    def is_connect(self):
        return self.bytes[0] == PacketType.CONNECT

    def is_create_response(self):
        return self.bytes[0] == PacketType.CREATE_RESPONSE

    def get_lobby_code(self):
        assert self.is_join() or self.is_create_response()
        return self.bytes[2:8]
