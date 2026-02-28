# Diffie-Hellman & Caesar Cipher Chat 🛡️

Este repositório contém a implementação de um sistema de comunicação cliente-servidor via TCP, focado no aprendizado de conceitos fundamentais de criptografia e redes. O projeto evolui de uma cifra estática para uma troca de chaves dinâmica e segura utilizando o algoritmo Diffie-Hellman

## 🚀 Sobre o Projeto

O objetivo deste projeto é demonstrar como garantir a confidencialidade em uma rede. Ele está dividido em duas etapas principais:

1. **Criptografia de César:** Implementação básica de cifra de substituição com chave fixa.
2. **Protocolo Diffie-Hellman:** Implementação de um aperto de mão (*handshake*) para estabelecer uma chave secreta compartilhada de forma dinâmica entre cliente e servidor.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Protocolo de Transporte:** TCP (Sockets)
* **Conceitos de Criptografia:** Cifra de César, Aritmética Modular, Troca de Chaves Diffie-Hellman.

---

## 📂 Estrutura de Arquivos

O projeto é composto por quatro scripts principais:

### 1. Comunicação com Chave Fixa

* `Simple_tcpClient.py`: Cliente que utiliza uma `CHAVE_FIXA = 5` para cifrar mensagens antes de enviar ao servidor.
* `Simple_tcpServer.py`: Servidor que recebe a mensagem, processa (converte para maiúsculas) e devolve a resposta.

### 2. Comunicação com Diffie-Hellman

* `TCP_DiffieHellmanClient.py`: Implementa a lógica de geração de chaves públicas ($A = g^a \pmod p$) e cálculo do segredo compartilhado.
* `TCP_DiffieHellmanServer.py`: Realiza o cálculo simétrico ($B = g^b \pmod p$) e utiliza a chave resultante para decifrar as mensagens do cliente.

---

## 🔐 Como Funciona a Implementação

### A Cifra de César (Camada de Cifragem)

A função `encriptar` utiliza o deslocamento de caracteres baseado na tabela ASCII (módulo 256) para garantir que qualquer caractere possa ser enviado com segurança básica:

```python
def encriptar(texto, chave):
    return "".join(chr((ord(char) + chave) % 256) for char in texto)
```

### O Protocolo Diffie-Hellman (Camada de Chave)

Para evitar que a chave seja "hardcoded" (fixa), utilizamos o algoritmo DH:

1. **Parâmetros Públicos:** Cliente e servidor concordam com um número primo ($p = 997$) e uma base ($g = 2$).
2. **Segredos Privados:** Cada lado gera um número aleatório secreto ($a$ e $b$).
3. **Troca Pública:** Eles trocam os resultados de $g^{segredo} \pmod p$.
4. **Chave Final:** Ambos calculam o mesmo segredo $K$ de forma independente, sem que $K$ tenha transitado pela rede.

---

## 🚦 Como Executar

1. **Clone o repositório:**
```bash
git clone https://github.com/guigarciag/diffie-hellman-caesar-chat.git
cd diffie-hellman-caesar-chat

```


2. **Inicie o Servidor:**
```bash
python TCP_DiffieHellmanServer.py
```


3. **Inicie o Cliente (em outro terminal):**
```bash
python TCP_DiffieHellmanClient.py
```



> **Nota:** Certifique-se de ajustar o endereço IP (`serverName`) nos arquivos do cliente para o IP onde o servidor está rodando (use `localhost` para testes locais).

---

## 🛡️ Segurança e Fins Didáticos

Este projeto possui **fins puramente educacionais**. A Cifra de César é vulnerável a ataques de força bruta e análise de frequência. O protocolo Diffie-Hellman aqui implementado utiliza números primos pequenos para facilitar a visualização dos cálculos, não sendo recomendado para aplicações em produção.

---

## 🎥 Vídeo Explicativo

Acesse o vídeo abaixo no YouTube com a explicação de funcionamento do projeto: https://www.youtube.com/watch?v=1_6uaGNSKyQ

---

Desenvolvido por:
- Guilherme Garcia  [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/guigarciag)
- Lohan Batista  [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Lohan1303)
- Rodrigo Puertas [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RodrigoPuertas)
- Paulo Henrique [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PauloTristao)
