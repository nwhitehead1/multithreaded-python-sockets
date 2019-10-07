#!/usr/bin/python3

import socket
import sys
from crypto import encrypt, decrypt

BUFFER_SIZE = 1024

def main():
    HOST = sys.argv[1]      # Server IP address
    PORT = int(sys.argv[2]) # Port used by the server
    
    print('[CLIENT] Creating socket...')
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((HOST, PORT, 0, 0))
    print('[CLIENT] Connecting to server:', HOST, ' (', PORT, ')')
    while True:
        try:
            # Request String
            byteRequestString = input('[CLIENT] File Name Request: ').encode('utf-8')
            encryptedByteRequestString = encrypt(byteRequestString)
            s.sendall(encryptedByteRequestString)

            # Response File
            responseData = s.recv(BUFFER_SIZE)
            responseDataDecrypted = decrypt(responseData)
            if not responseDataDecrypted:
                print('[CLIENT] Response not received: The file could not be found.')
            else:
                print('[CLIENT] Response received. Writing data to local file...')
                try:
                    f = open('response_file.txt', 'wb')
                    f.write(responseDataDecrypted)
                except:
                    print('[CLIENT] Unable to write response to file!')
                    if f:
                        f.close()
        except KeyboardInterrupt:
            print('[CLIENT] Closing client socket...')
            break
    s.close()

if __name__ == '__main__':
    main()
