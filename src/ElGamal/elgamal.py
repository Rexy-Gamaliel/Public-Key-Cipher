from Crypto.Util.number import getPrime
from io import FileIO
import random
import math

KEY_DIR = "./key/"
TEST_DIR = "./test/"
SIZE_T = 32

class KeyGen():
    def __init__(self, p=None, g=None, x=None, y=None):
        self.p = p
        self.g = g
        self.x = x
        self.y = y

    def generate(self, size=SIZE_T):
        self.p = getPrime(size)
        self.g = random.randint(1,self.p-1)
        self.x = random.randint(1,self.p-2)
        self.y = pow(self.g, self.x, self.p)

    def public(self):
        return self.y, self.g, self.p

    def private(self):
        return (self.x, self.p)

    def dumpPub(self, f:FileIO):
        f.write("ELGAMAL PUBLIC KEY\n")
        f.write(str(self.y)+"\n")
        f.write(str(self.g)+"\n")
        f.write(str(self.p)+"\n")
    
    def dumpPri(self, f:FileIO):
        f.write("ELGAMAL PRIVATE KEY\n")
        f.write(str(self.x)+"\n")
        f.write(str(self.p)+"\n")

    def setKey(self, p=None, g=None, x=None, y=None):
        if p:
            self.p = p
        if g:
            self.g = g
        if x:
            self.x = x
        if y:
            self.y = y

class Encoder():
    def __init__(self):
        pass

    def encode(self, text, p:int):
        p_bin = "{0:b}".format(p)
        bits = len(p_bin)-1
        t_bin = ""
        for c in bytearray(text, "utf-8"):
            c_bin = format(c, 'b')
            padding = 8-len(c_bin)
            c_bin = padding*'0' + c_bin
            t_bin += c_bin
        
        padding = 0
        encoded = []
        while t_bin != '':
            encoded.append(int(t_bin[:bits],2))
            padding = bits - len(t_bin[:bits])
            t_bin = t_bin[bits:]

        encoded.append(padding)
        return encoded

    def decode(self, arrint, p:int):
        p_bin = "{0:b}".format(p)
        bits = len(p_bin)-1;
        padding = 0
        t_bin = []
        for a in arrint:
            a_bin = "{0:b}".format(a)
            a_bin = (bits-len(a_bin)) * '0' + a_bin
            t_bin.append(a_bin)
            padding = a

        t_bin[len(t_bin)-2] = t_bin[len(t_bin)-2][padding:]
        t_bin = t_bin[:len(t_bin)-1]
        t_bin = "".join(t_bin)

        text = ''
        while t_bin != '':
            text += chr(int(t_bin[:8], 2))
            t_bin = t_bin[8:]

        return text

class ElGamal():
    def __init__(self):
        self.key = KeyGen();
        self.key.generate()

    def printkey(self):
        print(self.key.public())
        print(self.key.private())

    def dumpKey(self):
        with open(KEY_DIR+"key.pub", "w") as f:
            self.key.dumpPub(f)
        with open(KEY_DIR+"key.pri", "w") as f:
            self.key.dumpPri(f)

    def encrypt(self, text, key=None):
        y, g, p = self.key.public()
        plain = Encoder().encode(text, p)
        k = random.randint(1, p-2)
        cipher = []
        for m in plain:
            a = pow(g, k, p)
            ykp = pow(y, k, p)
            mp = pow(m, 1, p)
            b = ykp * mp % p 
            cipher.append((a,b))
        return cipher

    def decrypt(self, cipher, key=None):
        x, p = self.key.private()
        plain = []
        for a, b in cipher:
            m = b * (pow(a, p-1-x, p)) % p
            plain.append(m)
        return Encoder().decode(plain, p)

def main():
    cipher = ElGamal()
    cipher.printkey()
    cipher.dumpKey()

    ciphertext = cipher.encrypt("lalalalhokoko")
    print(ciphertext)
    print(cipher.decrypt(ciphertext))

if __name__ == "__main__":
    main()