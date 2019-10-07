#!/usr/bin/python3

import socket
from threading import Thread

HOST = ''
PORT = 12000

BUFFER_SIZE = 1024

class ClientThread(Thread):
    
    def __init__(self, ip, port, sock, requestFileName):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print('[SERVER] New thread started:', ip, '(', str(port), ')')
        self.requestFileName = requestFileName

    def run(self):
        textRequest = self.requestFileName.decode('utf-8')
        print('[SERVER] Attempting to open file:', textRequest)
        try:
            f = open(self.requestFileName.decode('utf-8'), 'rb')
            print('[SERVER] Successfully opened file:', textRequest)
            l = f.read(BUFFER_SIZE)
            self.sock.sendall(l)
            if f:
                f.close() 
        except:
            print('[SERVER] File not found:', textRequest)
            self.sock.shutdown(socket.SHUT_WR)
        
def main():
    print('[SERVER] Creating socket...')
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
        serverAddress = (HOST, PORT, 0, 0)
        print('[SERVER] Binding host and port...')
        s.bind(serverAddress)
        threads = []
        print('[SERVER] Listening for incoming connections...')
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