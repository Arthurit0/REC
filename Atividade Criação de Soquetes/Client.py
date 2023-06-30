import socket

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12000  # Porta do servidor

#conexão        comunicação       IPv4      avisa q é protocolo TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# estabelecendo conexão com as variaveis
client_socket.connect((HOST, PORT))
#---------conexão estabelecida--------------



message = 'Bora pro game:\n'
#envia dados para servidor\ codifica para bytes a mensagem
client_socket.send(message.encode())

# Recebe as mensagens do servidor e as imprime na tela
while True:

#          especifica tamanho dos bytes e decodifica
    data = client_socket.recv(1024).decode()
    print(data)
    
    #ação do Cliente
    action = input('Digite a sua ação: ')
    
    # envia ação para o server e codifica a mes
    client_socket.send(action.encode())

