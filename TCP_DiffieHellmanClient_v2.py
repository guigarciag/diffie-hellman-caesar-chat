from socket import *
import time
import random

def encriptar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)

def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if n in small:
        return True
    for p in small:
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def witness(a: int) -> bool:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return True
        return False

    if n < (1 << 64):
        bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
    else:
        k = 12
        bases = [random.randrange(2, n - 2) for _ in range(k)]

    for a in bases:
        a %= n
        if a == 0:
            continue
        if not witness(a):
            return False
    return True

def generate_large_prime(bits: int) -> int:
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1
        if is_probable_prime(p):
            return p

def generate_keypair(bits: int):
    if bits != 4096:
        raise ValueError("Somente 4096 bits é suportado nesta implementação.")
    e = 65537
    while True:
        p = generate_large_prime(bits // 2)
        q = generate_large_prime(bits // 2)
        if p == q:
            continue
        n = p * q
        phi = (p - 1) * (q - 1)
        try:
            d = pow(e, -1, phi)
        except ValueError:
            continue
        return (e, n), (d, n)

def encrypt_rsa(public_key_rsa, plaintext: str) -> str:
    e, n = public_key_rsa
    return ",".join(str(pow(ord(ch), e, n)) for ch in plaintext)

def decrypt_rsa(private_key_rsa, ciphertext: str) -> str:
    d, n = private_key_rsa
    if not ciphertext:
        return ""
    return "".join(chr(pow(int(c), d, n)) for c in ciphertext.split(",") if c)

def generate_private_key(p: int) -> int:
    return random.randrange(2, p - 1)

def public_key(g: int, private: int, p: int) -> int:
    return pow(g, private, p)

def shared_secret(other_public: int, private: int, p: int) -> int:
    return pow(other_public, private, p)

def derive_shift(secret: int) -> int:
    return secret % 256

serverName = "localhost"
serverPort = 1300
clientSocket = socket(AF_INET, SOCK_STREAM)

print("Gerando chaves RSA do Cliente...")
public_rsa_client, private_rsa_client = generate_keypair(4096)

print(f"Conectando-se ao servidor {serverName}:{serverPort}...")
clientSocket.connect((serverName,serverPort))

#===============TROCA DE CHAVES RSA================
print("Realizando troca de chaves RSA...")
# Recebe a chave pública RSA do servidor
server_rsa_bytes = clientSocket.recv(65000)
s_e_str, s_n_str = server_rsa_bytes.decode("utf-8").split("|")
public_rsa_server = (int(s_e_str), int(s_n_str))
print("Chave pública RSA do servidor recebida.")

# Envia a chave pública RSA para o servidor
e_c, n_c = public_rsa_client
clientSocket.send(f"{e_c}|{n_c}".encode("utf-8"))
#==================================================

#===============DIFFIE HELLMAN=====================
# Recebe parâmetros DH (p, g) e B do servidor encriptados
encrypted_initial = clientSocket.recv(65000)
decrypted_initial = decrypt_rsa(private_rsa_client, encrypted_initial.decode("utf-8"))
p_str, g_str, B_str = decrypted_initial.split("|")
p = int(p_str)
g = int(g_str)
B = int(B_str)
print("Mensagem DH (p|g|B) recebida e decriptada com RSA.")

# Gera segredo do cliente e valor público A
priv_a = generate_private_key(p)
A = public_key(g, priv_a, p)
# Envia A para o servidor, encriptado com a chave RSA do servidor
encrypted_A = encrypt_rsa(public_rsa_server, str(A))
clientSocket.send(encrypted_A.encode("utf-8"))
print("Valor DH 'A' encriptado via RSA enviado ao servidor.")

# Calcula segredo compartilhado e deslocamento para cifra de César
secret = shared_secret(B, priv_a, p)
shift = derive_shift(secret)
print('===========================')
print("CHAVEAMENTO DIFFIE-HELLMAN/nDH handshake concluído")
print(f"p={p}\ng={g}\nB={B}\nA={A}\nsecret={secret}\nshift={shift}")
#==================================================

sentence = ''
while sentence != 'exit':
    sentence = input("Input lowercase sentence: ")
    encrypted = encriptar(sentence, shift)
    print('===========================')
    print ("Encrypted: ", encrypted)
    clientSocket.send(bytes(encrypted, "utf-8"))

    modifiedSentence = clientSocket.recv(65000)
    text = decriptar(str(modifiedSentence,"utf-8"), shift)
    print ("Decrypted from Server: ", text)
    print('===========================')

clientSocket.send(bytes("exit", "utf-8"))
clientSocket.close()
