import random
from socket import *

def encriptar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)

# Configurações
serverName = "54.233.35.215"
serverPort = 8080
p = 997 
g = 2

# DH - Segredo privado do cliente (a)
a = random.randint(100, 500)
# DH - Chave pública do cliente (A = g^a mod p)
A = pow(g, a, p)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# --- TROCA DIFFIE-HELLMAN ---
# 1. Enviar A
clientSocket.send(str(A).encode())
# 2. Receber B
B = int(clientSocket.recv(1024).decode())
# 3. Calcular Chave Secreta Final (K = B^a mod p)
K = pow(B, a, p)
print(f"Chave estabelecida via DH: {K}")

# --- ENVIO DE MENSAGEM ---
msg = input("Digite a mensagem: ")
msg_crip = encriptar(msg, K)
clientSocket.send(msg_crip.encode())

resp_crip = clientSocket.recv(65000).decode()
print(f"Servidor (Criptografado): {resp_crip}")
print(f"Servidor (Decifrado): {decriptar(resp_crip, K)}")

clientSocket.close()