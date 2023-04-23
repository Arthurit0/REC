import socket
import os


def connectToServer():

    HOST = '127.0.0.1'  # Endereço IP do servidor
    PORT = 12000  # Porta do servidor

    # conexão comunicação IPv4 avisa q é protocolo TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # estabelecendo conexão com as variaveis
    client_socket.connect((HOST, PORT))  # conexão estabelecida
    print("Herói foi conectado ao servidor com sucesso!\n")


def startGame(client):
    playerAct = ''

    while playerAct.lower() != 'quit':
        os.system('clear')
        data = client.recv(1024).decode()
        gameAction = data.split(';')

        if gameAction[0] in ['WIN', 'GAME_OVER']:
            return handleEnd(gameAction)

        if len(gameAction) == 4:
            print(
                f'Status do Herói:\n\tVida: {gameAction[2]}\n\tPontuação: {gameAction[3]}\n')
        else:
            print(
                f'Status do Herói:\n\tVida: {gameAction[1]}\n\tPontuação: {gameAction[2]}\n')

        playerAct = handleAction(gameAction)

        client.send(playerAct.upper().encode())


def handleAction(game):
    event = game[0]

    if event == "NOTHING_HAPPENED":
        playerAct = input(
            'Nada aconteceu. Adentrando mais nas masmorras...\n\nPressione Enter para continuar... ')
    elif event == 'MONSTER_ATTACK':
        playerAct = input(
            f'Um monstro apareceu atrás das portas! Escolha uma porta entre 0 a {game[1]} para atacar o monstro: ')

        while playerAct > game[1] and playerAct < 0:
            playerAct = input(
                f'Ação Inválida! Envie um número de 0 a {game[1]}: ')
    elif event == 'MONSTER_KILLED':
        playerAct = input(
            'Você acertou a porta e atacou o monstro! Sua pontuação aumentou!\n\nPressione Enter para continuar...')

    elif event == 'MONSTER_ATTACKED':
        playerAct = input(
            'Você errou a porta e o monstro atacou! Sua vida diminuiu!\n\nPressione Enter para continuar...')

    elif event == 'TAKE_CHEST':
        playerAct = input(
            'Você encontrou um baú. Envie "YES" para abrí-lo ou "NO" para ignorá-lo: ')

        while playerAct.lower() not in ['yes', 'no']:
            playerAct = input(
                f'Ação Inválida! Envie "YES" ou "NO": ')

    elif event == 'CHEST_VALUE':
        playerAct = input(
            f'O baú proporcionou {game[1]} pontos a seu herói!\n\nPressione Enter para continuar...')

    elif event == 'SKIPPING_CHEST':
        playerAct = input(
            'O herói ignorou o baú e continuou em sua jornada...\n\nPressione Enter para continuar...')

    elif event == 'BOSS_EVENT':
        playerAct = input(
            f'Você encontrou um chefão! Para lutar, envie "FIGHT", mas se quiser fugir, envie "RUN": ')

        while playerAct.lower() not in ['fight', 'run']:
            playerAct = input(
                f'Ação Inválida! Envie "FIGHT" ou "RUN": ')

    elif event == 'BOSS_DEFEATED':
        playerAct = playerAct = input(
            f'Você lutou corrajosamente e derrotou o chefão!\n\nPressione Enter para continuar...')

    elif event == 'FAILED_BOSS_FIGHT':
        playerAct = input(
            f'O chefão ganhou a luta e te machucou gravemente!\n\nPressione Enter para continuar...')

    elif event == 'ESCAPED':
        playerAct = input(
            f'Com dificuldades você escapou... Mas perdeu um pouco de vida!\n\nPressione Enter para continuar...')

    if playerAct == '':
        playerAct = 'Continue'

    return playerAct


def handleEnd(game):
    event = game[0]

    if event == 'WIN':
        print('Parabéns, você venceu o jogo!\n')
        input(
            f'Você venceu {game[1]} salas e conquistou {game[3]} pontos, com {game[2]} de vida restante.')
    else:
        print("Game Over! Você morreu e perdeu o jogo!\n")
        input(f'Você venceu {game[1]} salas e conquistou {game[3]} pontos.')


if __name__ == '__main__':
    client = connectToServer()
    start = input('Pressione "Enter" para iniciar o jogo...')
    while start != '':
        start = input()
    client.send('start'.upper().encode())
    startGame(client)
    client.close()
