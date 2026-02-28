from socket import *

# --- FUNÇÕES AUTORAIS DE CRIPTOGRAFIA ---
def encriptar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)

def decriptar(texto_crip, chave):
    return "".join(chr((ord(char) - chave) % 256) for char in texto_crip)
# ----------------------------------------

serverName = "54.233.35.215" # <--- MUDE ISSO!
serverPort = 8080
CHAVE_FIXA = 5

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input("Digite uma frase para enviar ao servidor: ")

# 1. Encripta antes de enviar
frase_encriptada = encriptar(sentence, CHAVE_FIXA)
print(f"Enviando dados cifrados: {frase_encriptada}")

# 2. Envia
clientSocket.send(frase_encriptada.encode("utf-8"))

# 3. Recebe a resposta cifrada
resposta_cifrada = clientSocket.recv(65000).decode("utf-8")

# 4. Decripta a resposta
resposta_real = decriptar(resposta_cifrada, CHAVE_FIXA)

print(f"Resposta do Servidor (Cifrada): {resposta_cifrada}")
print(f"Resposta Final (Decifrada): {resposta_real}")

clientSocket.close()