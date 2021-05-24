import socket

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 11000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        enter_string = s.recv(1024)
        print(enter_string.decode('utf-8'))
        data = s.send(input(': ').encode('utf-8'))
        if not data:
            break

        response = s.recv(1024)
        print(response.decode('utf-8'))
