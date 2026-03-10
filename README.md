# RSA, Diffie-Hellman & Caesar Cipher Chat 🛡️

Este repositório contém a implementação de um sistema de comunicação cliente-servidor via TCP, focado no aprendizado de conceitos fundamentais de criptografia e redes. O projeto evolui de uma cifra estática para uma arquitetura robusta de **Múltiplas Camadas de Criptografia**, utilizando Diffie-Hellman protegido por RSA de 4096 bits, sem o uso de bibliotecas criptográficas prontas.

## 🚀 Sobre o Projeto

O objetivo deste projeto é demonstrar como garantir a confidencialidade em uma rede combinando criptografia simétrica e assimétrica. Ele foi desenvolvido em três etapas principais:

1. **Criptografia de César:** Implementação de cifra de substituição em fluxo contínuo.
2. **Protocolo Diffie-Hellman:** Implementação de um aperto de mão (*handshake*) para estabelecer uma chave secreta compartilhada de forma dinâmica entre cliente e servidor.
3. **Criptografia RSA (4096 bits):** Proteção das chaves trocadas no Diffie-Hellman utilizando chaves assimétricas gigantes. Para garantir a viabilidade da geração dessas chaves em tempo real, foi implementado o algoritmo **PrimoHyper** (baseado no teste de primalidade de Miller-Rabin).

---

## 🛠️ Tecnologias e Conceitos Utilizados

* **Linguagem:** Python 3.x
* **Redes:** Protocolo de Transporte TCP (Sockets)
* **Criptografia Simétrica:** Cifra de César (com chave dinâmica)
* **Troca de Chaves:** Diffie-Hellman
* **Criptografia Assimétrica:** RSA (Geração de chaves, encriptação e decriptação)
* **Matemática Computacional:** Algoritmo PrimoHyper (Miller-Rabin) para geração eficiente de números primos de 2048 bits.

---

## 📂 Estrutura de Arquivos

O projeto principal é executado através de dois scripts que concentram toda a lógica de sockets e criptografia:

* `TCP_DiffieHellmanClient_v2.py`: Cliente TCP que gera suas chaves RSA, realiza o handshake Diffie-Hellman e inicia o chat cifrado.
* `TCP_DiffieHellmanServer_v2.py`: Servidor TCP que gera suas chaves RSA, responde ao handshake, recebe mensagens em fluxo contínuo, processa (converte para maiúsculas) e devolve a resposta cifrada.

*(Nota: Os nomes dos arquivos podem variar conforme a sua organização local, como `Simple_tcpClient.py` e `Simple_tcpServer.py`)*

---

## 🔐 Como Funciona a Implementação (O Handshake)

O fluxo de segurança do nosso projeto ocorre em três camadas sequenciais:

### 1. A Camada Assimétrica (RSA 4096 bits & PrimoHyper)
Ao iniciar, tanto o Cliente quanto o Servidor geram um par de chaves RSA de 4096 bits. Para isso, o algoritmo **PrimoHyper** gera dois números primos gigantes (2048 bits cada) em questão de segundos. As chaves públicas ($e, N$) são trocadas em texto plano logo no início da conexão.

### 2. A Camada de Troca de Chaves (Diffie-Hellman Protegido)
Para evitar que a chave de comunicação seja interceptada, utilizamos o algoritmo DH protegido pelo RSA:
1. Ambos concordam com um primo ($P = 997$) e uma base ($G = 2$).
2. Cada lado gera um número aleatório privado ($a$ e $b$).
3. O Cliente calcula $R1$ (Valor Público A) e o Servidor calcula $R2$ (Valor Público B).
4. **O pulo do gato:** O $R1$ é encriptado com a chave RSA do Servidor antes de ser enviado na rede. O $R2$ é encriptado com a chave RSA do Cliente. 
5. Ambos decriptam os valores recebidos e calculam a mesma **Chave Simétrica Final (K)**.

### 3. A Camada de Cifragem de Mensagens (Cifra de César)
Com a chave simétrica $K$ estabelecida secretamente, a função de chat entra em loop. A comunicação utiliza o deslocamento de caracteres baseado na tabela ASCII (módulo 256):

## 🎥 Vídeo Explicativo

Acesse o vídeo abaixo no YouTube com a explicação de funcionamento do projeto: https://www.youtube.com/watch?v=1_6uaGNSKyQ

---

Desenvolvido por:
- Guilherme Garcia  [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/guigarciag)
- Lohan Batista  [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Lohan1303)
- Rodrigo Puertas [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RodrigoPuertas)
- Paulo Henrique [![GitHub Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PauloTristao)
