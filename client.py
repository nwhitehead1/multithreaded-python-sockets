#!/usr/bin/python3

import socket
import sys
import crypto

BUFFER_SIZE = 1024

# File Not Found -> Throw this to end execution on empty server send.
class FileNotFoundException(Exception):
    pass

def main():
    # ping6 -I lowpan0 fe80::ec0b:fb0f:76b9:f393 <- Other rasp pi device
    HOST = sys.argv[1]      # Server IP address
    PORT = int(sys.argv[2]) # Port used by the server

    print('[CLIENT] Creating socket...')
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    s.connect((HOST, PORT, 0, 0))
    print('[CLIENT] Connecting to server:', HOST, ' (', PORT, ')')
    clientPrivateKey, clientPublicKey = crypto.keyGen()
    # Receive public key from server
    try:
        serverPublicKeyString = s.recv(BUFFER_SIZE).decode('utf-8')
        serverPublicKey = crypto.stringToKey(serverPublicKeyString)
    except ValueError as ve:
        print('[CLIENT] Invalid public key from server:', ve)
        s.close()
    # Send public key to server
    print('[CLIENT] Sending Public Key:\n', crypto.keyToBytes(clientPublicKey))
    s.sendall(crypto.keyToBytes(clientPublicKey))
    try:
        # Request String
        byteRequestString = input('[CLIENT] File Name Request: ').encode()
        encryptedByteRequestString = crypto.encrypt(byteRequestString, serverPublicKey)
        print('[CLIENT] Sending encrypted request:', encryptedByteRequestString)
        s.sendall(encryptedByteRequestString)

        # Response File
        encryptedResponseFile = s.recv(BUFFER_SIZE)
        if not encryptedResponseFile:
           raise FileNotFoundException()
        else:
            print('[CLIENT] Receiving encrypted server response:', encryptedResponseFile)
            print('[CLIENT] Response received. Writing data to local file...')
            try:
                decryptedResponseFile = crypto.decrypt(encryptedResponseFile, clientPrivateKey)
                f = open('responses/response_file.txt', 'wb')
                f.write(decryptedResponseFile)
                if f:
                    f.close()
            except:
                print('[CLIENT] Unable to write response to file!')
    except KeyboardInterrupt:
        print('[CLIENT] Closing client socket...')
    except FileNotFoundException:
        print('[CLIENT] Response not received: The file could not be found.')
    finally:
        s.close()

if __name__ == '__main__':
    main()
