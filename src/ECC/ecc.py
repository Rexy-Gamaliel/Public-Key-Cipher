import sys
sys.path.append("../../../public-key-cipher")
import math
import src.utility.utility as util
from random import randrange
from collections import defaultdict
from time import time

INFPOINT = (None, None)

class ECC():

    def __init__(self):
        self.debug = False
        pass
    
    def udpate_config(self):
        self.generate_keys(prime_bit=128, coef_bit=16)
        self.store_keys()

    def initiate(self):
        self.read_keys()
        self.point = self.determine_start_point()
        # self.generate_points()

    def generate_keys(self, prime_bit:int=128, coef_bit:int=16):
        self._a = randrange(-1 * (1<<coef_bit), 1<<coef_bit)
        self._b = randrange(-1 * (1<<coef_bit), 1<<coef_bit)
        generator = util.PrimeGenerator(prime_bit)
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
            print(f"y^2 = x^3 + {self._a}x + {self._b}\np = {self._p}")
    
    def show_info(self):
        print(f"y^2 = x^3 + {self._a}x + {self._b}\np = {self._p}")
        print(f"Starting point: {self.point}")
    
    def _y_square(self, x: int):
        return x**3 + self._a * x + self._b

    def _generate_square_map(self):
        # Set up map
        # <key, value> where key and value in {0, 1, ..., p-1} and key is i^2 mod p for every p in [0, p)
        self._map = defaultdict(list)
        i = 0
        for n in range(self._p):
            if i % (1<<32) == 0: print(i, end=' ')
            n_squared = pow(n, 2, self._p)
            self._map[n_squared].append(n)
            i += 1
        print(self._map)
    
    def generate_points(self):
        self._generate_square_map()

        self._points = []
        for x in range(self._p):
            rhs = self._y_square(x)
            # print(x, rhs, rhs%self._p)
            # if rhs >= 0:
            # print(rhs, end='#')
            # y = math.isqrt(rhs)
            y_squared = rhs % self._p
            for y_valid in self._map[y_squared]:
                # print(y, end='#')
                self._points.append((x, y_valid))
                # self._points.append((x, y%self._p))
        
        if self.debug:
            print(self._points)
    
    def determine_start_point(self):
        while True:
            # x = randrange(self._p)
            x = 178353325960679233252873817867044506126
            print("failed?", x)
            y_squared = self._y_square(x) % self._p
            result = util.modular_sqrt(y_squared, self._p)
            if result != 0:
                return (x, result)

    def add_points(self, P, Q):
        if P == INFPOINT: return Q
        if Q == INFPOINT: return P

        if P[0] == Q[0]:
            if P[1] == Q[1]: return self.double_point(P)
            if P[1] != Q[1]: return INFPOINT

        # m = ((P[1] - Q[1]) / (P[0] - Q[0])) % self._p
        m = (P[1]-Q[1]) * pow(P[0]-Q[0], -1, self._p) % self._p
        x = (m*m - P[0] - Q[0]) % self._p
        y = (m*(P[0] - x) - P[1]) % self._p

        return (x, y)
    
    def double_point(self, P):
        assert(P != INFPOINT)

        # m = ((3 * P[0]**2 + self._a) / (2*P[1])) % self._p
        m = (3*P[0]*P[0] + self._a) * pow(2*P[1], -1, self._p) % self._p
        x = (m*m - 2*P[0]) % self._p
        y = (m * (P[0] - x) - P[1]) % self._p

        return (x, y)
    
    def multiply_point(self, P, k:int):
        assert(k > 1)
        result = P
        # print(result)
        k -= 1
        while k > 0:
            result = self.add_points(result, P)
            # print(result)
            k -= 1
        return result

if __name__ == "__main__":
    start = time()
    ecc = ECC()
    # ecc.udpate_config()
    ecc.initiate()
    ecc.show_info()
    starting_point = ecc.point
    k = 1 << 20
    print(f"{k = }")
    result = ecc.multiply_point(starting_point, k)
    print(result)
    print("Compute time:", time()-start)