from io import FileIO
from Crypto.Util.number import GCD, getPrime
import random
from app import TEMP_DIR
from constant import *

from elgamal import Encoder

def LCM(a, b):
    return a * b // GCD(a,b)

class KeyGen():
    def __init__(self, g=None, n=None, h=None, u=None):
        self.g = g
        self.n = n
        self.h = h
        self.u = u

    def gen_pq(self):
        p = getPrime(SIZE_T)
        q = getPrime(SIZE_T)
        while GCD(p*q, (p-1)*(q-1)) != 1:
            p = getPrime(SIZE_T)
            q = getPrime(SIZE_T)
        return p, q

    def L(self, x):
        return (x-1) // self.n

    def generate(self, size=SIZE_T):
        p, q = self.gen_pq()
        self.n = p * q
        self.g = random.randint(1, (self.n**2)-1)
        self.h = LCM(p-1, q-1)
        self.u = pow(self.L(pow(self.g, self.h, self.n**2)),\
                        -1,\
                        self.n)

    def public(self):
        return self.g, self.n

    def private(self):
        return self.h, self.u

    def dumpPub(self, f:FileIO):
        f.write("PAILLIER PUBLIC KEY\n")
        f.write(str(self.g)+"\n")
        f.write(str(self.n)+"\n")
    
    def dumpPri(self, f:FileIO):
        f.write("PAILLIER PRIVATE KEY\n")
        f.write(str(self.h)+"\n")
        f.write(str(self.u)+"\n")

    def setKey(self, g=None, n=None, h=None, u=None):
        if g:
            self.g = g
        if n:
            self.n = n
        if h:
            self.h = h
        if u:
            self.u = u


class Paillier():
    def __init__(self):
        self.key = KeyGen()
        self.key.generate()

    def dumpKey(self, pubfile:str, prifile:str):
        with open(pubfile, 'w') as f:
            self.key.dumpPub(f)
        with open(prifile, 'w') as f:
            self.key.dumpPri(f)
    
    def printKey(self):
        g, n = self.key.public()
        h, u = self.key.private()
        print('''g : {}\nn : {}\nh : {}\nu : {}'''
                .format(g, n, h, u))

    def gen_r(self) :
        n = self.key.n
        r = random.randint(0, n)
        while GCD(r, n) != 1:
            r = random.randint(0, n)
        return r

    def encrypt(self, plain):
        g, n = self.key.public()
        r = self.gen_r()
        cipher = []
        for m in plain:
            gm = pow(g, m, n**2)
            rn = pow(r, n, n**2)
            c = gm * rn % n**2
            cipher.append(c)
        return cipher

    def decrypt(self, cipher):
        h, u = self.key.private()
        g, n = self.key.public()
        plain = []
        for c in cipher:
            ch = pow(c, h, n**2)
            m = self.key.L(ch) * u % n
            plain.append(m)
        return plain

    def encrypt_file(self, infile:str, outfile:str):
        file = open(infile, 'r')
        text = file.read()
        file.close()
        plain = Encoder().encode(text, self.key.n)
        print(plain)
        cipher = self.encrypt(plain)
        with open(outfile, 'w') as f:
            for c in cipher:
                f.write(str(c)+" ")
    
    def decrypt_file(self, infile:str, outfile:str):
        file = open(infile, 'r')
        buff = file.read().split(" ")
        file.close()
        cipher = []
        for c in buff:
            try:
                cipher.append(int(c))
            except:
                pass
        plain = self.decrypt(cipher)
        print(plain)
        plaintext = Encoder().decode(plain, self.key.n)
        with open(outfile, 'w') as f:
            f.write(plaintext)


def main():
    print("hello palier")
    pail = Paillier()
    pail.printKey()
    pail.dumpKey(KEY_DIR+"paillier.pub",\
                KEY_DIR+"paillier.pri")

    pail.encrypt_file(TEST_DIR+"input.txt", \
                        TEST_DIR+"output.txt")

    pail.decrypt_file(TEST_DIR+"output.txt", \
                        TEST_DIR+"output2.txt")

if __name__ == "__main__":
    main()