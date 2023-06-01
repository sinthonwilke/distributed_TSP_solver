import socket
import threading
from typing import List, Tuple
from collections import deque
import sys
import time

PORT = 8000
ADDR = ('172.16.238.10', '172.16.238.11', '172.16.238.12', '172.16.238.13')  # node0, node1, node2, node3
ADDR_INDEX = 0
HOSTNAME = socket.gethostname()
HOST_ADDR = socket.gethostbyname(HOSTNAME)

cities = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]


def tsp_bfs(start_city: int) -> Tuple[List[int], int]:
    n = len(cities)
    min_distance = sys.maxsize
    optimal_path = []

    queue = deque([(start_city, [start_city], 0)])

    while queue:
        current_city, path, total_distance = queue.popleft()

        # Check if all cities have been visited
        if len(path) == n:
            # Add distance from last city back to the starting city
            total_distance += cities[current_city][start_city]
            if total_distance < min_distance:
                min_distance = total_distance
                optimal_path = path + [start_city]

        # Explore neighboring cities
        for neighbor in range(n):
            if neighbor not in path:
                new_path = path + [neighbor]
                new_distance = total_distance + cities[current_city][neighbor]
                queue.append((neighbor, new_path, new_distance)) # type: ignore

    return optimal_path, min_distance


def handle_client(client_socket, client_addr):
    start_city = int(client_socket.recv(1024).decode())
    path, total_distance = tsp_bfs(start_city)

    if path:
        message = f"Optimal path: {' -> '.join(map(str, path))}\nTotal distance: {total_distance + cities[path[-1]][start_city]}"
    else:
        message = "No solution found"

    client_socket.send(message.encode())
    client_socket.close()


def server(addr):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((addr, PORT))
    server_socket.listen()
    clientList = []
    while True:
        client_socket, client_addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        client_thread.start()
        clientList.append(client_addr)
        if len(clientList) == len(ADDR) - 1:
            break
    server_socket.close()


def client(addr):
    time.sleep(5)  # Add a delay of 5 seconds before connecting
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((addr, PORT))
        start_city = ADDR.index(HOST_ADDR)  # Use the index of the current address as the start city
        client_socket.send(str(start_city).encode())
        message = client_socket.recv(1024).decode()
        print(message)
        client_socket.close()
    except Exception as e:
        print(f"Error connecting to {addr}: {e}")


def main():
    global ADDR_INDEX
    if HOST_ADDR == socket.gethostbyname(ADDR[ADDR_INDEX]):
        server(socket.gethostbyname(ADDR[ADDR_INDEX]))
    else:
        client(socket.gethostbyname(ADDR[ADDR_INDEX]))

    ADDR_INDEX += 1

    if ADDR_INDEX != len(ADDR):
        main()


if __name__ == '__main__':
    main()
