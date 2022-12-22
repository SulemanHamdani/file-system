import socket, threading
from _thread import *
from FileManager import FileManager

print_lock = threading.Lock()

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

file_manager = FileManager()
thread_pool = []

def main(conn):
    print("Threaded")
    # command = conn.recv(1024).decode('utf-8')
    # response = execute.execute_command(command, file_manager)
    response = 'hello'
    conn.sendall(bytes(response, 'utf-8'))
    print_lock.release()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            start_new_thread(main, (conn,))
    