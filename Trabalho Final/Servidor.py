import socket


def udp_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    print("Servidor rodando!")

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(f"received message: {len(data)} bytes from: {addr}")


udp_server("127.0.0.1", 5005)
