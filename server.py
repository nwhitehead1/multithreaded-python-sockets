#!/usr/bin/python3

import socket
from threading import Thread
from crypto import encrypt, decrypt

HOST = 'localhost'
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
        textRequest = self.requestFileName
        decryptedTextRequest = decrypt(textRequest).decode('utf-8')
        print('[SERVER] Attempting to open file:', decryptedTextRequest)
        try:
            f = open('files/' + decryptedTextRequest, 'rb')
            print('[SERVER] Successfully opened file:', decryptedTextRequest)
            l = f.read(BUFFER_SIZE)
            encryptedResponse = encrypt(l)
            print('[SERVER] Sending encrypted response:', encryptedResponse)
            self.sock.sendall(encryptedResponse)
            if f:
                f.close() 
        except:
            print('[SERVER] File not found:', decryptedTextRequest)
            self.sock.shutdown(socket.SHUT_WR)
        
def main():
    print('[SERVER] Creating socket...')
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
        serverAddress = (HOST, PORT, 0, 0)
        print('[SERVER] Binding host and port...')
        s.bind(serverAddress)
        threads = []
        print('[SERVER] Listening for incoming connections...')
        while True:
            s.listen(2)
            conn, addr = s.accept()
            print('[SERVER] Connection accepted from:', addr)
            while True:
                data = conn.recv(BUFFER_SIZE)
                print('[SERVER] Receiving encrypted client request:', data)
                if not data:
                    break
                thread = ClientThread(addr[0], addr[1], conn, data)
                thread.start()
                threads.append(thread)

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

