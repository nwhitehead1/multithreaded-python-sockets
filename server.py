#!/usr/bin/python3

import socket
from threading import Thread
import sys

BUFFER_SIZE = 1024

class ClientThread(Thread):
    
    def __init__(self, ip, port, sock, requestFileName):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("[SERVER] New thread started:", ip, ":"+str(port))
        self.requestFileName = requestFileName

    def run(self):
        print('[SERVER] Attempting to open file:', self.requestFileName.decode('utf-8'))
        f = open(self.requestFileName.decode('utf-8'), 'rb')
        print('[SERVER] Successfully opened file:', self.requestFileName.decode('utf-8'))
        l = f.read(BUFFER_SIZE)
        self.sock.send(l)
            
        
def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    print('[SERVER] Creating socket...')
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0) as s:
        serverAddress = (HOST, PORT, 0, 0)
        s.bind(serverAddress)
        threads = []
        print('[SERVER] Binding host and port successful.')
        print("[SERVER] Listening for incoming connections...")
        s.listen()
        while True:
            conn, addr = s.accept()
            print('[SERVER] Connection accepted from:', addr)
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                thread = ClientThread(addr[0], addr[1], conn, data)
                thread.start()
                threads.append(thread)

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()