import socket

PORT = 95  # The port used by the server
host = input("Host IP: ")
username = input("Username: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, PORT))
    s.send(bytes(f"username {username}", "utf-8"))

    while True:
        data = s.recv(1048576)
        data = data.decode("utf-8").replace("\\n", "\n")

        if data == "$$_exit_$$":
            break

        print(data, end="")
        command = input()
        s.send(bytes(command, "utf-8"))

    s.close()
