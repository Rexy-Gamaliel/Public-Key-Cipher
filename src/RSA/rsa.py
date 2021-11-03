# from .. utility import utility
import sys
sys.path.append("../../../public-key-cipher")
import os
# import src.utility.utility as util
# from src.ElGamal.elgamal import Encoder
import utility.utility as util
from random import randrange
# from src.utility.utility import readfile

CHARSIZE = 8

class RSA():
    def __init__(self, n_bit: int = 1024):
        self.debug = True
        self._input = None
        self._output = None

        self._n_bit = n_bit
    
    def generate_keys(self):
        generator = util.PrimeGenerator(self._n_bit)
        self._p = generator.generate_prime()
        self._q = generator.generate_prime()
        self._n = self._p * self._q
        self._totient_n = self._n - self._p - self._q + 1
        self._e = self._generate_e()
        self._d = pow(self._e, -1, self._totient_n)
        self.store_keys()

        if self.debug:
            print(f"p:{self._p}\nq:{self._q}\nn:{self._n}\ntotient(n):{self._totient_n}\ne:{self._e}\nd:{self._d}")

    def store_keys(self):
        util.writefile("key/rsa-private.pri", f"{self._d} {self._n}".encode("utf-8"))
        util.writefile("key/rsa-public.pri", f"{self._e} {self._n}".encode("utf-8"))

    def read_keys(self):
        self._d, self._n = [int(i) for i in util.readfile("key/rsa-private.pri").decode("utf-8").split(' ')]
        self._e, self._n = [int(i) for i in util.readfile("key/rsa-public.pri").decode("utf-8").split(' ')]
        # self._n = self._p * self._q
        # self._totient_n = self._n - self._p - self._q + 1
        # self._e = self._generate_e()
        # self._d = pow(self._e, -1, self._totient_n)

        if self.debug:
            print(f"n:{self._n}\ne:{self._e}\nd:{self._d}")


    def _generate_e(self):
        # Generate e, where e is relatively prime to totient n
        temp = randrange(1<<(self._n_bit-1), 1<<(self._n_bit))
        if self.debug:
            print(temp)
        while util.gcd(temp, self._totient_n) != 1:
            temp = randrange(1<<(self._n_bit-1), 1<<(self._n_bit))
            if self.debug:
                print(temp)
        return temp

    def encode(self, message: str, block_size:int=64):
        '''
            [DESC]
                str --> bytes (utf-8 encoding)
                Encode message by dividing it into blocks of <block_size> bits of chars.
                If the last block consist of less than <block_size> chars, add b'00000000' as padding for every needed char.
                Each block is then converted to int which value coresponds to the binary representation of the chars
            [PARAMS]
                message: str        { message to be encoded }
                block_size: int           { size of each block (bits) }
            [RETURN]
                array of number, where each number represents the int value of each block
        '''
        print("===== ENCODING =====")
        message_length = len(message)
        message_size = message_length * CHARSIZE    # message_size in bits
        num_blocks = message_size // block_size     # number of *full* blocks
        
        idx_step = block_size // CHARSIZE           # how many chars are in each block
        idx_limit = idx_step * num_blocks
        print(f"{message_length=}")
        print(f"{idx_limit=}")

        # Encode full blocks
        result = []
        i = 0
        while i <= idx_limit:
            block_char = message[i : i+idx_step]
            print(f"{i}-th block: {block_char}")
            int_val = 0
            for c in block_char:
                int_val <<= CHARSIZE    # 1 char = 8 bits
                int_val += ord(c)
                # int_val += c
            result.append(int_val)
            i += idx_step
        
        # # idx_limit < i <= idx_limit + idx_step
        # i -= idx_step
        # # idx_limit - idx_step < i <= idx_limit
        # # Encode last block (if any)
        # if  i < message_length:
        #     print("residu")
        #     block_char = message[i : message_length]
        #     print(block_char)
        #     int_val = 0
        #     for c in block_char:
        #         int_val <<= CHARSIZE    # 1 char = 8 bits
        #         int_val += ord(c)
        #         # int_val += c
        #     print(int_val)
        #     int_val <<= CHARSIZE * (block_size-len(block_char))    # append zeros as padding
        #     result.append(int_val)
        print("===== /ENCODING/ =====")
        return result
    
    def decode(self, encoded_message: list, block_size:int=64):
        '''
            [DESC]
                Decode message by interpreting the value coresponding to each block
                and combining it into blocks of <block_size> bits of chars.
                The last block may consist b'00000000' as padding.
            [PARAMS]
                encoded_message: list[int]  { message to be decoded }
                block_size: int           { size of each block (bits) }
            [RETURN]
                the string representation of the int value on each block
        '''
        print("===== DECODING =====")
        result = ''
        
        if len(encoded_message) > 1:
            # Decode full blocks
            for val in encoded_message[:-1]:    # encoded_message is not empty
                # print(format(val, '01024b'))
                block_char = ""
                while val > 0:
                    char_val = val % (1 << CHARSIZE)
                    val >>= CHARSIZE
                    block_char += chr(char_val)
                result += block_char[::-1]
        
        # Decode last block
        val = encoded_message[-1]
        # print(format(val, '01024b'))
        # # Remove padding
        # while val % (1 << CHARSIZE) == 0:
        #     val >>= CHARSIZE

        block_char = ""
        while val > 0:
            char_val = val % (1 << CHARSIZE)
            val >>= CHARSIZE
            block_char += chr(char_val)
        result += block_char[::-1]
        # print(f"Decoded: {result}")
        print(f"{len(result)=}")
        print("===== /DECODING/ =====")
        return result

    def encrypt_txt(self, input_dir, output_dir):
        message = util.readfile(input_dir)
        # message: bytes

        message = message.decode("utf-8")
        # message: str

        # e = Encoder()
        encoded_message = self.encode(message, self._n_bit)
        # encoded_message = e.encode(message, self._n_bit)
        print(f"{encoded_message=}")
        encrypted = encoded_message
        encrypted = []
        for val in encoded_message:
            encrypted.append(pow(val, self._e, self._n))
        
        print(f"{encrypted=}")
        
        # decoded_message = e.decode(encrypted, self._n_bit)

        # decoded_message = self.decode(encrypted, self._n_bit)
        # b = decoded_message.encode("utf-8")
        # print(f"{b=}")
        # util.writefile(output_dir, b)
        
        # util.writefile(output_dir, b''.join([str(i) for i in encrypted]))
        dirname = os.path.dirname(__file__)
        dirname = os.path.dirname(os.path.dirname(dirname))
        filename = os.path.join(dirname, output_dir)
        with open(filename, 'w') as file:
            file.write(' '.join([str(i) for i in encrypted]))
        return message
    
    def decrypt_txt(self, input_dir, output_dir):
        dirname = os.path.dirname(__file__)
        dirname = os.path.dirname(os.path.dirname(dirname))
        filename = os.path.join(dirname, input_dir)
        with open(filename, 'r') as file:
            message = [int(i) for i in file.readline().split(' ')]
            # print(message)
            # file.write(decoded_message)
        # message = util.readfile(input_dir)
        print(f"{message=}")
        # message: bytes

        # message = message.decode("utf-8")
        # print(f"(Decoded) {message=}")
        # encoded_message = self.encode(message, self._n_bit)
        encoded_message = message
        # print(f"{encoded_message=}")
        decrypted = []
        for val in encoded_message:
            decrypted.append(pow(val, self._d, self._n))
        
        print(f"{decrypted=}")
        
        decoded_message = self.decode(decrypted, self._n_bit)

        b = decoded_message.encode("utf-8")
        # print(f"{b=}")
        util.writefile(output_dir, b)

        # util.writefile(output_dir, ''.join(str(i) for i in decrypted))
        return message

    def printKey(self):
        print("n:{}\ne:{}\nd:{}".format(self._n, self._e, self._d))

if __name__ == "__main__":
    # print(readfile('../input.txt'))
    rsa = RSA(16)
    # rsa.generate_keys()
    rsa.read_keys()
    # message = rsa.encrypt_txt("test/rsa-input-test.txt", "test/rsa-output-test.txt")
    message = rsa.decrypt_txt("test/rsa-output-test.txt", "test/rsa-result-test.txt")
    # print(rsa.encode(message))
    pass
