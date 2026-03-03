import random

def gen4096():
    n = random.getrandbits(4096)

    # garante que o bit mais alto esteja ligado (pra não vir menor)
    n |= (1 << 4095)

    return n

print(gen4096())