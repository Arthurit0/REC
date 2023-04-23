from socket import *



serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input('O que você vai fazer? ').encode()
clientSocket.send(sentence)

modifiedSentence = clientSocket.recv(1024)
print('From server: ', modifiedSentence.decode())


clientSocket.close()
