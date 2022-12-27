import socket
import threading

from _thread import start_new_thread
from FileManager import FileManager
from execute import execute_command

HOST = ""
PORT = 65431
host_name = socket.gethostname()
file_manager = FileManager()
# thread function
def threaded(conn):
    username = ""
    response = ""

    while True:
        command = conn.recv(1024)
        command = command.decode("utf-8")

        if command.startswith("username"):
            username = command.split(" ")[1]
        elif command == "exit":
            conn.send(bytes("$$_exit_$$", "utf-8"))
            break
        else:
            response = execute_command(command, file_manager)

        conn.send(bytes(response, "utf-8"))
        conn.send(bytes(f"\n{username}@{host_name}:", "utf-8"))

    print(f"{username} disconnected.")
    conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    # put the socket into listening mode
    s.listen(5)
    print(f"Listening for connections on port {PORT}...")
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        conn, addr = s.accept()
        print("Connected to :", addr[0], ":", addr[1])
        start_new_thread(threaded, (conn,))

    s.close()


main()
