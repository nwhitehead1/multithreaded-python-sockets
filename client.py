#!/usr/bin/python3

import socket
import sys

BUFFER_SIZE = 1024

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    FILE = sys.argv[3]

    print('[CLIENT] Creating socket...')
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0) as s:
        print('[CLIENT] Connecting to server:', HOST, ' (', PORT, ')')
        s.connect((HOST, PORT, 0, 0))

        # Request String
        try:
            byteRequestString = FILE.encode('utf-8')
            s.send(byteRequestString)
        except socket.error:
            print('[CLIENT] Request failed!')
    
        # Response File
        try:
            fileData = s.recv(BUFFER_SIZE)
            try:
                f = open('response_file.txt', 'wb')
                print('[CLIENT] Response received.')
                f.write(fileData)
            finally:
                f.close()
        finally:
            print('[CLIENT] Closing client socket...')
            s.close()

if __name__ == '__main__':
    main()
