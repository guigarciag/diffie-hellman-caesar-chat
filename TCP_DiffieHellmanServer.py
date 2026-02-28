import random
from socket import *

# Funções da Cifra de César (Etapa 2)
def encriptar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)

# Validação de Primo (Etapa 3 - Baseada no "Primo Fast")
def e_primo(n):
    if n < 2: return False
    i = 2
    while i * i <= n: # Otimização: testar até a raiz quadrada
        if n % i == 0: return False
        i += 1
    return True

# Parâmetros Públicos
p = 997  
g = 2    

serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

print(f"Servidor aguardando Diffie-Hellman na porta {serverPort}...")

while True:
    connectionSocket, addr = serverSocket.accept()
    
    # --- PROCESSO DIFFIE-HELLMAN ---
    # 1. Gerar segredo privado do servidor (b)
    b = random.randint(100, 500)
    # 2. Calcular chave pública do servidor (B = g^b mod p)
    B = pow(g, b, p)
    
    # 3. Receber chave pública do cliente (A)
    A = int(connectionSocket.recv(1024).decode())
    
    # 4. Enviar chave pública do servidor (B)
    connectionSocket.send(str(B).encode())
    
    # 5. Calcular Chave Secreta Final (K = A^b mod p)
    K = pow(A, b, p)
    print(f"Chave Simétrica estabelecida: {K}")

    # --- CHAT CRIPTOGRAFADO ---
    dados_recebidos = connectionSocket.recv(65000).decode("utf-8")
    if dados_recebidos:
        msg_real = decriptar(dados_recebidos, K)
        print(f"Cliente disse: {msg_real}")
        
        resposta_crip = encriptar(msg_real.upper(), K)
        connectionSocket.send(resposta_crip.encode("utf-8"))

    connectionSocket.close()