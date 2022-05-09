import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5005))

num_codes = 0

while True:
    sock.sendto(bytes([0xfe]), ('127.0.0.1', 2082))
    num_codes += 1
    sys.stdout.write("\rSent %i requests" % num_codes)
    sys.stdout.flush()