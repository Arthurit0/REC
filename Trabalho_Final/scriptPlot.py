import json
import glob
import matplotlib.pyplot as plt


def main():

    type = ''

    while type not in ['1', '2']:
        type = input(
            "Deseja gerar o gráfico para (1) Servidores ou (2) Clientes? ")
        if type not in ['1', '2']:
            print("Escolha um dos tipos digitando '1' ou '2'!")

    offset = input("Quantos segundos de atraso do UDP? ")

    if offset == '':
        offset = 0  # se nenhum offset for fornecido, definimos como 0
    else:
        offset = int(offset)

    if type == '1':
        type = 'server'
    else:
        type = 'client'

    json_files = glob.glob(f'{type}*.json')

    metrics_data = {}

    for file in json_files:
        print(f'Lendo e processando arquivo: {file}')

        with open(file) as json_file:
            data = json.load(json_file)

        # Verifica se o protocolo é UDP
        is_udp = data['start']['test_start']['protocol'].lower() == 'udp'

        if file not in metrics_data:
            metrics_data[file] = {'indice': [], 'bps': []}

        for i, interval in enumerate(data['intervals']):
            for stream in interval['streams']:
                metrics_data[file]['indice'].append(
                    i + (offset if is_udp else 0))
                metrics_data[file]['bps'].append(stream['bits_per_second'])

    for filename, data in metrics_data.items():
        port = filename.replace(f'{type}_port_', '').replace('.json', '')

        with open(filename) as json_file:
            protocol = json.load(json_file)[
                'start']['test_start']['protocol'].upper()

        legend_label = f'{type} - porta - {port} ({protocol})'

        x_axis = data['indice']
        y_axis = data['bps']

        plt.plot(x_axis, y_axis, label=f'{legend_label}')
    plt.title("Comparação de bytes por segundo")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
