#!/usr/bin/python3

import socket
import sys

BUFFER_SIZE = 1024

def main():
    HOST = sys.argv[1]      # Server IP address
    PORT = int(sys.argv[2]) # Port used by the server
    FILE = sys.argv[3]      # File Name (full server path)
    
    print('[CLIENT] Creating socket...')
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((HOST, PORT, 0, 0))
    print('[CLIENT] Connecting to server:', HOST, ' (', PORT, ')')
    try:
        # Request String
        byteRequestString = FILE.encode('utf-8')
        s.sendall(byteRequestString)

        # Response File
        responseData = s.recv(BUFFER_SIZE)
        if not responseData:
            print('[CLIENT] Response not received: Socket shutdown by server -> The file could not be found.')
        else:
            print('[CLIENT] Response received. Writing data to local file...')
            try:
                f = open('response_file.txt', 'wb')
                f.write(responseData)
            except:
                print('[CLIENT] Unable to write response to file!')
                if f:
                    f.close()
    finally:
        print('[CLIENT] Closing client socket...')
        s.close()

if __name__ == '__main__':
    main()
