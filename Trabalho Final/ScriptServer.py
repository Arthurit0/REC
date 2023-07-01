import subprocess
import socket


def my_ip():
    return socket.gethostbyname(socket.gethostname())


def start_iperf_server(protocol, port):
    # Replace "iperf3" with the full path to the executable.
    command = ["/usr/bin/iperf3", "-s", "-p", str(port)]
    with open(f"{protocol}_server_output.txt", "w") as f:
        process = subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT)

        print(
            f"Started iperf3 {protocol.upper()} server on IP {my_ip()} on port {port} [PID: {process.pid}]"
        )
    return process


def main():
    tcp_server = start_iperf_server("tcp", port=5201)
    udp_server = start_iperf_server("udp", port=5202)

    try:
        tcp_server.wait()
        udp_server.wait()
    except KeyboardInterrupt:
        tcp_server.kill()
        udp_server.kill()
        print("Servers stopped by user")


if __name__ == "__main__":
    main()
