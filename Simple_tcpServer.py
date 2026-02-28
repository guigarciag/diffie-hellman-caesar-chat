from socket import *

serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)

print("TCP Server rodando e escutando na porta", serverPort, "...\n")

# Loop infinito adicionado para o servidor não desligar após 1 mensagem
while True:
    connectionSocket, addr = serverSocket.accept()
    print("Conexão estabelecida com o cliente:", addr)
    
    sentence = connectionSocket.recv(65000)
    
    # Previne que o servidor quebre se receber dados vazios
    if not sentence:
        connectionSocket.close()
        continue

    received = str(sentence, "utf-8")
    print("Received From Client:", received)

    capitalizedSentence = sentence.upper() # processamento original do professor

    connectionSocket.send(capitalizedSentence)

    sent = str(capitalizedSentence, "utf-8")
    print("Sent back to Client:", sent)
    
    connectionSocket.close()