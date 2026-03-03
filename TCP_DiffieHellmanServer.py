import random
import math
from socket import *

# Funções da Cifra de César (Etapa 2)
def encriptar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)

def gen4096():
    n = random.getrandbits(4096)

    # garante que o bit mais alto esteja ligado (pra não vir menor)
    n |= (1 << 4095)

    return n

# Validação de Primo (Etapa 3 - Baseada no "Primo Fast")
def e_primo(n):
    if n < 2: return False
    i = 2
    while i * i <= n: # Otimização: testar até a raiz quadrada
        if n % i == 0: return False
        i += 1
    return True

def find_mod_inv(a,m):

    """
        a = e
        m = fi_N
    
    """
    for x in range(1,m):
        if (a % m) * (x % m) % m == 1:
            return x
    raise Exception("Não existe o modulo inverso")


# p = gen4096()
# q = gen4096()

p = 3 
q = 5

N = p * q

fi_N = (p-1) * (q-1)

print(f"fi_N: {fi_N}")

e = 7
print(math.gcd(fi_N))


# print(math.gcd(fi_N,e))

y = pow(e,-1,fi_N)

while math.gcd(fi_N,e) > 1:
    e = e + 2

print(f"e: {e}")
print(f"y: {y}")

d = find_mod_inv(e,fi_N)



# # Parâmetros Públicos
# f = 997  
# g = 2    

# serverPort = 1300
# serverSocket = socket(AF_INET, SOCK_STREAM)
# serverSocket.bind(("", serverPort))
# serverSocket.listen(1)

# print(f"Servidor aguardando Diffie-Hellman na porta {serverPort}...")

# while True:
#     connectionSocket, addr = serverSocket.accept()
    
#     # --- PROCESSO DIFFIE-HELLMAN ---
#     # 1. Gerar segredo privado do servidor (b)
#     b = random.randint(100, 500)
#     # 2. Calcular chave pública do servidor (B = g^b mod p)
#     B = pow(g, b, f)
    
#     # 3. Receber chave pública do cliente (A)
#     A = int(connectionSocket.recv(1024).decode())
    
#     # 4. Enviar chave pública do servidor (B)
#     connectionSocket.send(str(B).encode())
    
#     # 5. Calcular Chave Secreta Final (K = A^b mod p)
#     K = pow(A, b, f)
#     print(f"Chave Simétrica estabelecida: {K}")

#     # --- CHAT CRIPTOGRAFADO ---
#     dados_recebidos = connectionSocket.recv(65000).decode("utf-8")
#     if dados_recebidos:
#         msg_real = decriptar(dados_recebidos, K)
#         print(f"Cliente disse: {msg_real}")
        
#         resposta_crip = encriptar(msg_real.upper(), K)
#         connectionSocket.send(resposta_crip.encode("utf-8"))

#     connectionSocket.close()