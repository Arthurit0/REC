import json
import glob
import matplotlib.pyplot as plt


def main():

    type = ''

    while type not in ['1', '2']:
        type = input(
            "Deseja gerar o gráfico para (1) Servidores ou (2) Clientes? ")
        if int(type) not in ['1', '2']:
            print("Escolha um dos tipos digitando '1' ou '2'!", end=" ")

    files = []

    if type == '1':
        type = 'client'
    else:
        type = 'server'


if __name__ == "__main__":
    main()
