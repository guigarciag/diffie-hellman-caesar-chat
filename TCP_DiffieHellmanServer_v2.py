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

def checa_primo(n: int) -> bool:
    return is_probable_prime(n)

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

serverPort = 1300
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(5)
print ("TCP Server\n")
print("Gerando chaves RSA do Servidor...")
public_rsa_server, private_rsa_server = generate_keypair(4096)
print("Aguardando conexão do cliente...")
connectionSocket, addr = serverSocket.accept()


#===============TROCA DE CHAVES RSA================
print("Realizando troca de chaves RSA...")
# Envia a chave pública RSA para o cliente
e_s, n_s = public_rsa_server
connectionSocket.send(f"{e_s}|{n_s}".encode("utf-8"))

# Recebe a chave pública RSA do cliente
client_rsa_bytes = connectionSocket.recv(65000)
c_e_str, c_n_str = client_rsa_bytes.decode("utf-8").split("|")
public_rsa_client = (int(c_e_str), int(c_n_str))
print("Chave pública RSA do cliente recebida.")
#==================================================

#===============DIFFIE HELLMAN=====================
p = 2147483647  # primo (2^31 - 1)
g = 5
# Segredo do servidor e valor público B
priv_b = generate_private_key(p)
B = public_key(g, priv_b, p)
# Envia parâmetros e B para o cliente (Encriptados com RSA)
handshake_msg = f"{p}|{g}|{B}"
encrypted_handshake = encrypt_rsa(public_rsa_client, handshake_msg)
connectionSocket.send(encrypted_handshake.encode("utf-8"))
print("Mensagem DH (p|g|B) encriptada via RSA enviada ao cliente.")

# Recebe A do cliente e decripta com RSA
encrypted_A_bytes = connectionSocket.recv(65000)
decrypted_A_str = decrypt_rsa(private_rsa_server, encrypted_A_bytes.decode("utf-8"))
A = int(decrypted_A_str)
print("Valor DH 'A' recebido e decriptado com RSA.")

# Calcula segredo compartilhado e deriva deslocamento
secret = shared_secret(A, priv_b, p)
shift = derive_shift(secret)
print('===========================')
print("CHAVEAMENTO DIFFIE-HELLMAN/nDH handshake concluído")
print(f"p={p}\ng={g}\nA={A}\nB={B}\nsecret={secret}\nshift={shift}")
#==================================================


# Loop de eco com cifra de César usando o deslocamento derivado
sentence = ""
while sentence != "exit":
    sentence = connectionSocket.recv(65000)
    if sentence == b"exit":
        break
    decrypted = decriptar(str(sentence, "utf-8"), shift)
    print('===========================')
    print("Encrypted From Client: ", sentence)
    print("Decrypted From Client: ", decrypted)
    capitalizedSentence = decrypted.upper()

    encrypted = encriptar(capitalizedSentence, shift)
    print("Capitalized Sentence: ", capitalizedSentence)
    print("Encrypted To Client: ", encrypted)
    print('===========================')
    connectionSocket.send(encrypted.encode("utf-8"))

connectionSocket.close()
