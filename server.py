#!/usr/bin/python3

import socket
import crypto
from threading import Thread

HOST = ''
PORT = 12000

BUFFER_SIZE = 1024

class ClientThread(Thread):
    
    def __init__(self, ip, port, sock, requestFileName, pubKey):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print('[SERVER] New thread started:', ip, '(', str(port), ')')
        self.requestFileName = requestFileName
        self.pubKey = pubKey

    def run(self):
        print('[SERVER] Attempting to open file:', self.requestFileName)
        try:
            f = open('files/' + self.requestFileName, 'rb')
            print('[SERVER] Successfully opened file:', self.requestFileName)
            l = f.read(BUFFER_SIZE)
            encryptedResponseFileBytes = crypto.encrypt(l, self.pubKey)
            print('[SERVER] Sending encrypted response:', encryptedResponseFileBytes)
            self.sock.sendall(encryptedResponseFileBytes)
            if f:
                f.close() 
        except Exception as e:
            print('[SERVER] Exception Occurred:', e)
            self.sock.shutdown(socket.SHUT_RDWR)
        
def main():
    print('[SERVER] Starting up server...')
    serverPrivateKey, serverPublicKey = crypto.keyGen()
    print('[SERVER] Creating socket...')
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0) as s:
        serverAddress = (HOST, PORT, 0, 0)
        print('[SERVER] Binding host and port...')
        s.bind(serverAddress)
        threads = []
        print('[SERVER] Listening for incoming connections...')
        s.listen(2)
        while True:
            conn, addr = s.accept()
            print('[SERVER] Connection accepted from:', addr)
            # Send public key to client
            print('[SERVER] Sending Public Key:\n', crypto.keyToBytes(serverPublicKey))
            conn.sendall(crypto.keyToBytes(serverPublicKey))
            # Receive public key from client
            try:
                clientPublicKeyString = conn.recv(BUFFER_SIZE).decode('utf-8')
                clientPublicKey = crypto.stringToKey(clientPublicKeyString)
            except ValueError as ve:
                print('[SERVER] Invalid public key from client:', ve)
                conn.close()
            while True:
                # Receive encrypted fileName string -> decrypt it
                encryptedData = conn.recv(BUFFER_SIZE)
                if not encryptedData:
                    conn.close()
                    break
                print('[SERVER] Receiving encrypted client request:', encryptedData)
                decryptedData = crypto.decrypt(encryptedData, serverPrivateKey).decode()
                thread = ClientThread(addr[0], addr[1], conn, decryptedData, clientPublicKey)
                thread.start()
                threads.append(thread)

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
