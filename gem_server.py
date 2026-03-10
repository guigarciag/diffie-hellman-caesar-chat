import random
from socket import *

# --- FUNÇÕES AUXILIARES ---
def encriptar_cesar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar_cesar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)

def is_prime(n, k=5):
    """Teste de primalidade Miller-Rabin para gerar primos grandes"""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def generate_large_prime(bits):
    print(f"Gerando primo de {bits} bits... (pode levar alguns segundos)")
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1
        if is_prime(p):
            return p

# --- 1. CONFIGURAÇÃO RSA DO SERVIDOR (4096 BITS) ---
print("=== INICIANDO GERAÇÃO DE CHAVES RSA DO SERVIDOR ===")
# Dois primos de 2048 bits geram um N de 4096 bits
p = generate_large_prime(2048)
q = generate_large_prime(2048)
N = p * q
fi_N = (p - 1) * (q - 1)
e = 65537 # Expoente público padrão e eficiente
d = pow(e, -1, fi_N)
print("=== CHAVES RSA DO SERVIDOR GERADAS COM SUCESSO ===\n")

# --- 2. CONFIGURAÇÃO DIFFIE-HELLMAN ---
P_dh = 997 # Primo público DH (pode ser maior, se o professor exigir)
G_dh = 2   # Base pública DH

# --- INICIANDO O SERVIDOR ---
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", 8080))
serverSocket.listen(1)

print("Servidor aguardando conexão na porta 8080...")

while True:
    conn, addr = serverSocket.accept()
    print(f"\n[INFO] Conectado a {addr}")

    # TROCA DE CHAVES RSA (Para podermos criptografar R1 e R2)
    # Envia chave pública RSA do Servidor para o Cliente
    conn.send(f"{N}|{e}".encode())
    
    # Recebe chave pública RSA do Cliente
    data_rsa_client = conn.recv(8192).decode()
    N_client, e_client = map(int, data_rsa_client.split("|"))

    # --- 3. TROCA DIFFIE-HELLMAN PROTEGIDA POR RSA ---
    # Recebe R1 (A_publico) do cliente, que está criptografado com o RSA do Servidor!
    R1_cifrado = int(conn.recv(8192).decode())
    # Descriptografa R1 usando a chave privada (d) do Servidor
    R1 = pow(R1_cifrado, d, N)
    print(f"[DH-RSA] R1 (A_publico) recebido e descriptografado: {R1}")

    # Gera o b_privado do Servidor e calcula R2 (B_publico)
    b_privado = random.randint(100, 500)
    R2 = pow(G_dh, b_privado, P_dh)
    
    # Criptografa R2 com a chave pública RSA do Cliente e envia
    R2_cifrado = pow(R2, e_client, N_client)
    conn.send(str(R2_cifrado).encode())

    # Calcula a chave simétrica K
    K = pow(R1, b_privado, P_dh)
    print(f"[DH] Chave Simétrica (K) estabelecida: {K}")

    # --- 4. FLUXO DE MENSAGENS (CIFRA DE CÉSAR) ---
    msg_cifrada = conn.recv(8192).decode()
    if msg_cifrada:
        print(f"[CÉSAR] Mensagem criptografada recebida: {msg_cifrada}")
        
        # Descriptografa com César usando K
        msg_original = decriptar_cesar(msg_cifrada, K)
        print(f"[CÉSAR] Mensagem decifrada: {msg_original}")

        # Processamento: Transforma em maiúsculo
        resposta = msg_original.upper()
        print(f"[PROC] Resposta a ser enviada: {resposta}")
        
        # Criptografa a resposta com César e envia
        resp_cifrada = encriptar_cesar(resposta, K)
        conn.send(resp_cifrada.encode())

    conn.close()