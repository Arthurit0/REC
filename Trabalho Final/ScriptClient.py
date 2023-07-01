import subprocess
import threading
import time


def run_iperf_tcp_client(ip, port, duration, cong_alg):
    command = ["iperf3", "-c", ip, "-p", str(port), "-t", str(duration), "-C", cong_alg]

    with open("tcp_client_output.txt", "w") as outfile:
        tempo = time.strftime("%H:%M:%S")
        print(f"Começou em {tempo}: \n", file=outfile)

        process = subprocess.Popen(command, stdout=subprocess.PIPE)

        for line in process.stdout:
            print(line.decode().strip(), file=outfile)


def run_iperf_udp_client(ip, port, duration, bitrate):
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

    with open("udp_client_output.txt", "w") as outfile:
        tempo = time.strftime("%H:%M:%S")
        print(f"Começou em {tempo}: \n", file=outfile)

        process = subprocess.Popen(command, stdout=subprocess.PIPE)

        for line in process.stdout:
            print(line.decode().strip(), file=outfile)


def main():
    print("Para ambos os servidores:\n")
    server_ip = input("Digite o IP alvo: ")
    duration = input("Digite a duração dos envios (segundos): ")

    print("\nPara o TCP:\n")

    cong_alg = ""

    while cong_alg not in ["cubic", "reno"]:
        cong_alg = input(
            'Qual algoritmo de congestionamento você quer para o TCP ("cubic" ou "reno"): '
        )

        if cong_alg not in ["cubic", "reno"]:
            print('\nResposta inválida! Escolha entre "cubic" ou "reno"! \n')

    print("\nPara o UDP:\n")

    bitrate = input("Qual a vazão (ou bitrate) você quer para o UDP (em Mb): ")

    tcp_port = 5201
    udp_port = 5202

    # Cria Threads para cada cliente
    tcp_thread = threading.Thread(
        target=run_iperf_tcp_client, args=(server_ip, tcp_port, duration, cong_alg)
    )

    udp_thread = threading.Thread(
        target=run_iperf_udp_client, args=(server_ip, udp_port, duration, bitrate)
    )

    # Inicia as threads
    tcp_thread.start()
    udp_thread.start()

    # Espera elas terminarem
    tcp_thread.join()
    udp_thread.join()


if __name__ == "__main__":
    main()
