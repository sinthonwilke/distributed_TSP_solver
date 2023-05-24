import socket
import threading

PORT = 8000
ADDR = ('172.16.238.10', '172.16.238.11', '172.16.238.12',
        '172.16.238.13')  # node0, node1, node2, node3
ADDR_INDEX = 0
HOSTNAME = socket.gethostname()
HOST_ADDR = socket.gethostbyname(HOSTNAME)


def handle_client(client_socket, client_addr):
    message = "received node" + str(ADDR.index(HOST_ADDR)) + \
        " from " + HOST_ADDR
    client_socket.send(message.encode())
    client_socket.close()


def server(addr):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((addr, PORT))
    server_socket.listen()
    clientList = []
    while True:
        client_socket, client_addr = server_socket.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_addr))
        client_thread.start()
        clientList.append(client_addr)
        if (len(clientList) == len(ADDR) - 1):
            break
    server_socket.close()


def client(addr):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((addr, PORT))
            message = client_socket.recv(1024).decode()
            print(message)
            client_socket.close()
            break
        except Exception as e:
            continue


def main():
    global ADDR_INDEX
    if HOST_ADDR == ADDR[ADDR_INDEX]:
        server(ADDR[ADDR_INDEX])
    else:
        client(ADDR[ADDR_INDEX])

    ADDR_INDEX += 1

    if (ADDR_INDEX != len(ADDR)):
        main()


main()
