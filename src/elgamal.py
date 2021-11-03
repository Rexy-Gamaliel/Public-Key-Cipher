from os import truncate
from Crypto.Util.number import getPrime
from io import FileIO
import random
from constant import *


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
        for c in text:
            c_bin = "{0:b}".format(ord(c))
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

    # def decode_r(self, arr_ab, p:int):
    #     bits = len("{0:b}".format(p))-1
    #     ab_bin = ''
    #     for a, b in arr_ab:
    #         a_bin = "{0:b}".format(a)
    #         a_bin = bits-len(a_bin)*'0' + a_bin
    #         b_bin = "{0:b}".format(b) 
    #         b_bin = bits-len(b_bin)*'0' + b_bin
    #         ab_bin += a_bin + b_bin

    #     t_bin = []
    #     while ab_bin != '':
            

class ElGamal():
    def __init__(self):
        self.key = KeyGen();
        self.key.generate()

    def printkey(self):
        print(self.key.public())
        print(self.key.private())

    def dumpKey(self, pubfile=KEY_DIR+"elgamal.pub", prifile=KEY_DIR+"elgamal.pri"):
        with open(pubfile, "w") as f:
            self.key.dumpPub(f)
        with open(prifile, "w") as f:
            self.key.dumpPri(f)

    def importPubKey(self, filename):
        file = open(filename, "r")
        buffer = file.read()
        file.close()

        lines = buffer.split("\n")
        if lines[0].split(" ")[0] != "ELGAMAL":
            print("Import failed")
            return

        self.key.setKey(y=int(lines[1]),\
                        g=int(lines[2]),\
                        p=int(lines[3]))

    def importPriKey(self, filename):
        file = open(filename, "r")
        buffer = file.read()
        file.close()

        lines = buffer.split("\n")
        if lines[0].split(" ")[0] != "ELGAMAL":
            print("Import failed")
            return

        self.key.setKey(x=int(lines[1]),\
                        p=int(lines[2]))

    def encrypt(self, plain, key=None):
        y, g, p = self.key.public()
        cipher = []
        for m in plain:
            k = random.randint(1, p-2)
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
        return plain

    def setKey(self, p=None, g=None, x=None, y=None):
        self.key = KeyGen(p, g, x, y)

    def encrypt_text(self, text):
        y, g, p = self.key.public()
        plain = Encoder().encode(text, p)
        cipher = []
        for m in plain:
            k = random.randint(1, p-2)
            a = pow(g, k, p)
            ykp = pow(y, k, p)
            mp = pow(m, 1, p)
            b = ykp * mp % p 
            cipher.append((a,b))
        return cipher

    def encrypt_file(self, infile, outfile=TEST_DIR+"output"):
        # filename is in TEST_DIR
        file = open(infile, "r")
        plain = file.read()
        file.close()
        _, _, p = self.key.public()
        plain = Encoder().encode(plain, p)
        cipher = self.encrypt(plain)
        with open(outfile, "w") as f:
            for a,b in cipher:
                f.write(str(a)+" "+str(b)+"\n")

    def decrypt_file(self, infile, outfile=TEST_DIR+"output"):
        file = open(infile, 'r')
        buffer = file.read()
        file.close()
        lines = buffer.split('\n')
        cipher = []
        for line in lines:
            ab = line.split(" ")
            try:
                a = int(ab[0])
                b = int(ab[1])
                cipher.append((a,b))
            except:
                pass
        with open(outfile, 'w') as f:
            plain = self.decrypt(cipher)
            plaintext = Encoder().decode(plain, self.key.p)
            f.write(plaintext)

    def textbox_to_file(self, text:str, filename:str):
        data = text.split(" ")
        i = 0
        buffer = ""
        while i < len(data):
            try:
                buffer += data[i] + " " + data[i+1] + "\n"
            except:
                pass
            i += 2
        with open(filename, 'w') as f:
            f.write(buffer)

    def encrypt_any_file(self, infile:str, outfile:str):
        file = open(infile, "rb")
        byte = file.read()
        file.close()
        byte2 = []
        byte2.extend(byte[:10])
        plaintext = "".join(chr(b) for b in byte)
        self.test1 = plaintext
        _, _, p = self.key.public()
        plain = Encoder().encode(plaintext, p)
        cipher = self.encrypt(plain)
        with open(outfile, "w") as f:
            for a,b in cipher:
                f.write(str(a)+" "+str(b)+"\n")
    
    def decrypt_any_file(self, infile:str, outfile:str):
        file = open(infile, 'r')
        buffer = file.read()
        file.close
        lines = buffer.split('\n')
        cipher = []
        for line in lines:
            ab = line.split(" ")
            try:
                a = int(ab[0])
                b = int(ab[1])
                cipher.append((a,b))
            except:
                pass
        with open(outfile, 'wb') as f:
            plain = self.decrypt(cipher)
            plaintext = Encoder().decode(plain, self.key.p)
            self.test2 = plaintext
            plain = []
            for p in plaintext:
                plain.append(ord(p))
            f.write(bytes(plain))

def main():
    elgamal = ElGamal()
    # elgamal.dumpKey()

    elgamal.importPubKey(KEY_DIR+"key.pub")
    elgamal.importPriKey(KEY_DIR+"key.pri")

    # elgamal.encrypt_file("test/input.txt", "test/output.txt")
    # elgamal.decrypt_file("test/output.txt", "test/output2.txt")

    elgamal.encrypt_any_file("test/input", "test/output")
    elgamal.decrypt_any_file("test/output", "test/output2")

    # print(elgamal.test1)
    # print(elgamal.test2)

    # print(elgamal.test1[:20])
    # enc = Encoder().encode(elgamal.test1, elgamal.key.p, True)

    # dec = Encoder().decode(enc, elgamal.key.p, True)
    # print(dec[:20])

if __name__ == "__main__":
    main()