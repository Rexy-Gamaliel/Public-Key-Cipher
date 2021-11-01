from array import array
from ctypes import Array
from io import FileIO
from os import POSIX_FADV_DONTNEED
from Crypto.Util.number import getPrime
import random

KEY_DIR = "./key/"
SIZE_T = 64

class KeyGen():
    def __init__(self):
        self.p = None
        self.g = None
        self.x = None
        self.y = None

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


class Encoder():
    def __init__(self):
        pass

    def encode(self, text, p:int):
        p_bin = "{0:b}".format(p)
        # t_bin = "".join(format(c, 'b') for c in bytearray(text, 'utf-8'))
        bits = len(p_bin)-1
        t_bin = ""
        for c in bytearray(text, "utf-8"):
            c_bin = format(c, 'b')
            padding = 8-len(c_bin)
            c_bin = padding*'0' + c_bin
            t_bin += c_bin
            print(c_bin)

        print("p bin :", p_bin)
        print("t bin :", t_bin)
        
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

        print("t_bin :", t_bin)
        text = ''
        while t_bin != '':
            text += chr(int(t_bin[:8], 2))
            print(t_bin[:8])
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

    # def encrypt(text, key):
    #     encoded = Encoder().encode(text)
    #     for 

def main():
    cipher = ElGamal()
    cipher.printkey()
    cipher.dumpKey()

    p = 1279000131313

    encoder = Encoder()
    result = encoder.encode("kzaak kzaak", p)
    # result = [1200000]
    print(result)

    print(encoder.decode(result, p))

if __name__ == "__main__":
    main()