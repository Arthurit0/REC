import socket
import time


def send_udp_data(ip, port, start_size, end_size, step):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    total_size = 0
    start_time = time.time()

    for size in range(start_size, end_size, step):
        data = b"x" * size
        sock.sendto(data, (ip, port))
        total_size += size

    end_time = time.time()

    sock.close()

    time_elapsed = end_time - start_time
    throughput = total_size / time_elapsed

    print(f"Tempo passado: {time_elapsed} segundos")
    print(f"Vazão: {throughput} bytes/seg")


def send_tcp_data(ip, port, start_size, end_size, step):
    # Diferença no TCP é o socket.SOCK_STREAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    total_size = 0
    start_time = time.time()

    for size in range(start_size, end_size, step):
        data = b"x" * size
        sock.send(data)
        total_size += size

    end_time = time.time()

    sock.close()

    time_elapsed = end_time - start_time
    throughput = total_size / time_elapsed

    print(f"Tempo passado: {time_elapsed} segundos")
    print(f"Vazão: {throughput} bytes/seg")


# send_tcp_data("192.168.1.1", 5005)

send_udp_data(ip="127.0.0.1", port=5001, start_size=1, end_size=50, step=1)
# send_tcp_data(ip="127.0.0.1", port=5201, start_size=1, end_size=50, step=1)
