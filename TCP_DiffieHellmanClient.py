import random
from socket import *

def encriptar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)

def gen4096():
    n = random.getrandbits(4096)

    # garante que o bit mais alto esteja ligado (pra não vir menor)
    n |= (1 << 4095)

    return n

# Configurações
serverName = "localhost"
serverPort = 1300
f = 997 
g = 2

# DH - Segredo privado do cliente (a)
a = random.randint(100, 500)
# DH - Chave pública do cliente (A = g^a mod p)
A = pow(g, a, f)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# --- TROCA DIFFIE-HELLMAN ---
# 1. Enviar A
clientSocket.send(str(A).encode())
# 2. Receber B
B = int(clientSocket.recv(1024).decode())
# 3. Calcular Chave Secreta Final (K = B^a mod p)
K = pow(B, a, f)
print(f"Chave estabelecida via DH: {K}")

# --- ENVIO DE MENSAGEM ---
msg = input("Digite a mensagem: ")
msg_crip = encriptar(msg, K)
clientSocket.send(msg_crip.encode())

resp_crip = clientSocket.recv(65000).decode()
print(f"Servidor (Criptografado): {resp_crip}")
print(f"Servidor (Decifrado): {decriptar(resp_crip, K)}")

clientSocket.close()