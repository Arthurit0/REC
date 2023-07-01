import subprocess
import threading
import time
import sys


def run_iperf_tcp_client(ip, port, duration, bitrate, cong_alg, json):
    command = [
        "iperf3",
        "-c",
        ip,
        "-p",
        str(port),
        "-t",
        str(duration),
        "-C",
        cong_alg,
    ]

    if bitrate != "":
        command = command + ["-b", f"{bitrate}Mb"]

    format = "txt"

    if json == "S":
        format = "json"
        command.append("-J")

    try:
        with open(f"./tcp_client_port_{port}.{format}", "w") as outfile:
            process = subprocess.Popen(command, stdout=subprocess.PIPE)

            for line in process.stdout:
                print(line.decode().strip(), file=outfile)
    except Exception as e:
        print(f"Um erro ocorreu: {e}", file=sys.stderr)


def run_iperf_udp_client(ip, port, duration, bitrate, json):
    command = [
        "iperf3",
        "-c",
        ip,
        "-p",
        str(port),
        "-u",
        "-b",
        f"{bitrate}Mb",
        "-t",
        str(duration),
    ]

    format = "txt"

    if json == "S":
        format = "json"
        command.append("-J")

    try:
        with open(f"./udp_client_port_{port}.{format}", "w") as outfile:
            process = subprocess.Popen(command, stdout=subprocess.PIPE)

            for line in process.stdout:
                print(line.decode().strip(), file=outfile)

    except Exception as e:
        print(f"Um erro ocorreu: {e}", file=sys.stderr)


def main():
    print("Para ambos os servidores:\n")

    server_ip = input("Digite o IP alvo: ")
    tcp_port = input(
        "Digite a porta para o TCP (Pressione Enter para a porta padrão 5201): "
    )

    udp_port = input(
        "Digite a porta para o UDP (Pressione Enter para a porta padrão 5202): "
    )

    if tcp_port == "":
        tcp_port = 5201
    if udp_port == "":
        udp_port = 5202

    duration = input(
        "\nDigite a duração dos envios (Em segundos, Enter para 10 segundos, haverá um atraso de 10 segundos entre o início da conexão TCP e UDP): "
    )

    if duration == "":
        duration = 10
    else:
        duration = int(duration)

    json = False

    while json not in ["", "S", "N"]:
        json = input(
            "Formato de exportação dos arquivos em JSON? (Enter ou 'S' para JSON, 'N' para TXT): "
        )

        if json not in ["", "S", "N"]:
            print("Resposta inválida!", end=" ")

    if json == "":
        json = "S"

    print("\nPara o TCP:\n")

    cong_alg = False

    while cong_alg not in ["", "cubic", "reno"]:
        cong_alg = input(
            'Qual algoritmo de congestionamento você quer para o TCP ("cubic" ou "reno", Enter para "cubic"): '
        ).lower()

        if cong_alg not in ["", "cubic", "reno"]:
            print('\nResposta inválida! Escolha entre "cubic" ou "reno"! \n')

    if cong_alg == "":
        cong_alg = "cubic"

    tcp_bitrate = input(
        "Qual a vazão (ou bitrate) você quer para o TCP (em Mb, enter para Ilimitado): "
    )

    print("\nPara o UDP:\n")

    udp_bitrate = ""

    while udp_bitrate == "":
        udp_bitrate = input("Qual a vazão (ou bitrate) você quer para o UDP (em Mb): ")
        if udp_bitrate == "":
            print("UDP precisa de um valor de bitrate!", end=" ")

    # Cria Threads para cada cliente
    tcp_thread = threading.Thread(
        target=run_iperf_tcp_client,
        args=(server_ip, tcp_port, str(duration + 10), tcp_bitrate, cong_alg, json),
    )

    udp_thread = threading.Thread(
        target=run_iperf_udp_client,
        args=(server_ip, udp_port, duration, udp_bitrate, json),
    )

    # Inicia as threads
    tcp_thread.start()
    print(
        f"\nIniciada conexão TCP para servidor {server_ip}:{tcp_port}{f' com {tcp_bitrate} Mb' if tcp_bitrate != '' else '' } e algoritmo de cong. {cong_alg.capitalize()}"
    )
    time.sleep(10)

    udp_thread.start()
    print(
        f"Iniciada conexão UDP para servidor {server_ip}:{udp_port} com bitrate de {udp_bitrate} Mb"
    )

    # Espera elas terminarem
    tcp_thread.join()
    udp_thread.join()
    print("Fim das conexões!")


if __name__ == "__main__":
    main()
