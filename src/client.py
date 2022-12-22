import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:     
        s.connect((HOST, PORT))
        command = input("Command: ")
        s.sendall(bytes(command, 'utf-8'))
        data = s.recv(1024)
        # convert bytes to string
        data = data.decode("utf-8")
        if (data == '$_exit_$'):
            print('Exiting...')
            break
        print(f"Received {data!r}")


