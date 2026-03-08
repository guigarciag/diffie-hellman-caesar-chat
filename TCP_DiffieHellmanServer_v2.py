import random
import math
from socket import *

def encriptar_cesar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar_cesar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)

# --- CONFIGURAÇÃO RSA COM LOGS ---
p, q = 61, 53
N = p * q
fi_N = (p - 1) * (q - 1)
e = 17
d = pow(e, -1, fi_N)

print("=== LOGS DE CONFIGURAÇÃO RSA ===")
print(f"Primos escolhidos: p={p}, q={q}")
print(f"Módulo N (p*q): {N}")
print(f"Phi de N ((p-1)*(q-1)): {fi_N}")
print(f"Expoente Público (e): {e}")
print(f"Chave Privada Decifradora (d = e^-1 mod fi_N): {d}")
print("================================\n")

# Parâmetros DH
f_dh, g_dh = 997, 2
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", 8080))
serverSocket.listen(1)

print("Servidor aguardando conexão...")

while True:
    conn, addr = serverSocket.accept()
    print(f"\n[INFO] Conectado a {addr}")

    # 1. Diffie-Hellman
    b_privado = random.randint(100, 500)
    B_publico = pow(g_dh, b_privado, f_dh)
    A_publico = int(conn.recv(1024).decode())
    conn.send(str(B_publico).encode())
    K = pow(A_publico, b_privado, f_dh)
    print(f"[DH] Chave Simétrica K estabelecida: {K}")

    # 2. Enviar Chave Pública RSA
    conn.send(f"{N}|{e}".encode())

    # 3. Receber e Decifrar
    dados = conn.recv(8192).decode()
    if dados:
        print(f"[RSA] Ciphertext recebido (lista de inteiros): {dados[:50]}...")
        lista_rsa = [int(x) for x in dados.split(",")]
        
        # LOG DA DECIFRAGEM RSA
        msg_cesar = ""
        for c in lista_rsa:
            m_dec = pow(c, d, N) # M = C^d mod N
            msg_cesar += chr(m_dec)
        
        print(f"[RSA] Mensagem após RSA (ainda com César): {msg_cesar}")
        
        # LOG DA CIFRA DE CÉSAR
        msg_final = decriptar_cesar(msg_cesar, K)
        print(f"[CÉSAR] Mensagem final decifrada: {msg_final}")

        # 4. Resposta em Maiúsculo
        resposta = msg_final.upper()
        print(f"[PROC] Convertendo para: {resposta}")
        
        # Cifrar de volta (César -> RSA)
        resp_cesar = encriptar_cesar(resposta, K)
        resp_rsa = ",".join([str(pow(ord(c), e, N)) for c in resp_cesar])
        conn.send(resp_rsa.encode())
        print("[INFO] Resposta enviada ao cliente.")

    conn.close()