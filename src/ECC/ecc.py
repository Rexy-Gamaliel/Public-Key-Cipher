import sys
sys.path.append("../../../public-key-cipher")
import math
import src.utility.utility as util
from random import randrange
from collections import defaultdict

class ECC():
    def __init__(self):
        self.debug = True
        pass
    
    def generate_keys(self):
        n = 3
        self._a = randrange(-1 * (1<<n), 1<<n)
        self._b = randrange(-1 * (1<<n), 1<<n)
        generator = util.PrimeGenerator(16)
        self._p = generator.generate_prime()

        if self.debug:
            print(f"y^2 = x^4 + {self._a}x + {self._b}\np:{self._p}")
    
    def store_keys(self):
        util.writefile("key/ecc-config.txt", f"{self._a} {self._b} {self._p}".encode("utf-8"))
        # util.writefile("key/ecc-private.pri", f"{self._a} {self._n}".encode("utf-8"))
        # util.writefile("key/ecc-public.pri", f"{self._b} {self._n}".encode("utf-8"))

    def read_keys(self):
        self._a, self._b, self._p = [int(i) for i in util.readfile("key/ecc-config.txt").decode("utf-8").split(' ')]
        # self._d, self._n = [int(i) for i in util.readfile("key/ecc-private.pri").decode("utf-8").split(' ')]
        # self._e, self._n = [int(i) for i in util.readfile("key/ecc-public.pri").decode("utf-8").split(' ')]
        # self._n = self._p * self._q
        # self._totient_n = self._n - self._p - self._q + 1
        # self._e = self._generate_e()
        # self._d = pow(self._e, -1, self._totient_n)

        if self.debug:
            print(f"y^2 = x^3 + {self._a}x + {self._b}\n{self._p=}")
    
    def _y_square(self, x: int):
        return x**3 + self._a * x + self._b

    def _generate_square_map(self):
        # Set up map
        # <key, value> where key and value in {0, 1, ..., p-1} and key is i^2 mod p for every p in [0, p)
        self._map = defaultdict(list)
        for n in range(self._p):
            n_squared = pow(n, 2, self._p)
            self._map[n_squared].append(n)
        print(self._map)
    
    def generate_points(self):
        self._generate_square_map()
        
        self._points = []
        for x in range(self._p):
            rhs = self._y_square(x)
            # print(x, rhs, rhs%self._p)
            # if rhs >= 0:
            # print(rhs, end='#')
            # y = math.sqrt(rhs)
            y_squared = rhs % self._p
            for y_valid in self._map[y_squared]:
                # print(y, end='#')
                self._points.append((x, y_valid))
                # self._points.append((x, y%self._p))
        
        #
        if self.debug:
            print(self._points)




if __name__ == "__main__":
    ecc = ECC()
    # ecc.generate_keys()
    # ecc.store_keys()
    ecc.read_keys()
    ecc.generate_points()
    pass