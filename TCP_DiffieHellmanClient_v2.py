import random
import math
from socket import *

def encriptar_cesar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar_cesar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost', 8080))

# 1. Diffie-Hellman
a_privado = random.randint(100, 500)
A_publico = pow(2, a_privado, 997)
clientSocket.send(str(A_publico).encode())
B_publico = int(clientSocket.recv(1024).decode())
K = pow(B_publico, a_privado, 997)
print(f"[DH] Chave estabelecida: {K}")

# 2. Receber RSA
data_rsa = clientSocket.recv(1024).decode()
N, e = map(int, data_rsa.split("|"))
print(f"[RSA] Chave Pública recebida: N={N}, e={e}")

# 3. Enviar Mensagem
msg = input("Digite a mensagem: ")

# LOG DA CIFRA DE CÉSAR
msg_cesar = encriptar_cesar(msg, K)
print(f"[CÉSAR] Mensagem após César: {msg_cesar}")

# LOG DA CIFRAGEM RSA
lista_rsa = []
print("--- INICIANDO CIFRAGEM RSA ---")
for char in msg_cesar:
    m = ord(char)
    c = pow(m, e, N) # C = M^e mod N
    print(f"Caractere '{char}' (ASCII {m}) -> Cifrado: {c}")
    lista_rsa.append(str(c))

msg_final_rsa = ",".join(lista_rsa)
clientSocket.send(msg_final_rsa.encode())

# 4. Receber Resposta
resp_raw = clientSocket.recv(8192).decode()
if resp_raw:
    # Decifrando resposta (usando d calculado localmente para o exemplo)
    d_local = pow(e, -1, (61-1)*(53-1))
    lista_resp = [int(x) for x in resp_raw.split(",")]
    
    # Desfaz RSA e César
    resp_cesar = "".join([chr(pow(c, d_local, N)) for c in lista_resp])
    resp_final = decriptar_cesar(resp_cesar, K)
    print(f"\n[RESPOSTA] Servidor retornou: {resp_final}")

clientSocket.close()