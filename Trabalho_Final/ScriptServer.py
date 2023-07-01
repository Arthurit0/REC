import subprocess
import socket
import json
import sys


def my_ip():
    return socket.gethostbyname(socket.gethostname())


def start_iperf_server(port, num, json):
    # Replace "iperf3" with the full path to the executable.
    command = ["/usr/bin/iperf3", "-s", "-p", str(port), "m"]

    format = "txt"

    if json == "S":
        format = "json"
        command.append("-J")

    try:
        with open(f"port_{port}_server.{format}", "w") as f:
            process = subprocess.Popen(command, stdout=f)

            print(
                f"Iniciado servidor iperf3 Nº {num} com IP {my_ip()}:{port} [PID: {process.pid}]"
            )
    except Exception as e:
        print(f"Um erro ocorreu: {e}", file=sys.stderr)

    return process


def main():
    port = 5201
    server_num = input(
        "Nº de servidores iperf3 que você deseja iniciar (Enter para 2): "
    )

    if server_num == "":
        server_num = 2
    else:
        server_num = int(server_num)

    json = False

    while json not in ["", "S", "N"]:
        json = input(
            "Formato de exportação dos arquivos em JSON? (Enter ou 'S' para JSON, 'N' para TXT): "
        )

        if json not in ["", "S", "N"]:
            print("\nResposta inválida! Escolha entre 'S' ou 'N'")

    if json == "":
        json = "S"

    print()

    iperf_servers = []

    for i in range(server_num):
        iperf_servers.append(start_iperf_server(port + i, i + 1, json))

    try:
        for server in iperf_servers:
            server.wait()
    except KeyboardInterrupt:
        for server in iperf_servers:
            server.kill()
    print("Servidores encerrados pelo usuário!")


if __name__ == "__main__":
    main()
