import os
import random
from time import time

dirname = os.path.dirname(__file__)

def readfile(directory):
    # !file directory is relative to utility.py!
    filename = os.path.join(dirname, directory)
    with open(filename, 'rb') as file:
        bytelist = file.readlines()
        bytes = b''
        for line in bytelist:
            bytes += line
        return bytes

def writefile(directory, content):
    # !file directory is relative to utility.py!
    filename = os.path.join(dirname, directory)
    with open(filename, 'wb') as file:
        file.write(content)


class PrimeGenerator():
    '''
        Generate n-bit prime number by doing:
        1. Generate n-bit random odd number (at least 2**(n-1))
        2. Sieve of Eratosthenes: check if the number is not prime by dividing it by small prime numbers
        3. Rabin-Miller Primality test: check with high probability if the number is prime
        PrimeGenerator is initialized with number of bits that is used to generate the prime number
    '''
    def __init__(self, n_bits=64):
        self.n_bits = n_bits
        self.timestamp = time()
        self.small_primes = self.generate_small_primes(limit=1000)

    def generate_small_primes(self, limit):
        isprime = [True for i in range(limit)]

        for i in range(2, limit):
            if not isprime[i]:
                continue
            for j in range(i+1, limit):
                if j % i == 0:
                    isprime[j] = False
        
        return [i for (i, _) in filter(lambda x: x[1], enumerate(isprime))][2:]
    
    def sieve_of_erathosthenes_test(self, number: int):
        '''
            Check if number is not prime by dividing it with small primes
            Return True if number pass this test (is not divisible by any small prime numbers)
            return False otherwise
        '''
        for prime in self.small_primes:
            if number % prime == 0:
                return False
        return True
    
    def random_n_bits(self, n: int=64):
        '''
        Generate n bits odd number in range(2**(n-1)+1, 2**n, 2)
        '''
        return random.randrange((1<<(n-1)) + 1, 1<<(n), 2)
    
    
    # [ DELETE LATER ]
    # From wikipedia: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    # Input #1: n > 3, an odd integer to be tested for primality
    # Input #2: k, the number of rounds of testing to perform
    # Output: “composite” if n is found to be composite, “probably prime” otherwise

    # write n as 2**r·d + 1 with d odd (by factoring out powers of 2 from n − 1)
    # WitnessLoop: repeat k times:
    #     pick a random integer a in the range [2, n − 2]
    #     x ← a**d mod n
    #     if x = 1 or x = n − 1 then
    #         continue WitnessLoop
    #     repeat r − 1 times:
    #         x ← x**2 mod n
    #         if x = n − 1 then
    #             continue WitnessLoop
    #     return “composite”
    # return “probably prime”
    def miller_rabin_test(self, n, k: int = 20):
        '''
            [DESC]
                Perform Miller-Rabin test to determine with high probability if n is prime
            [PARAMS]
                n: int { number to be tested }
                k: int { number of iteration, default=20 }
            [RETURN]
                True if n passes Miller-Rabin test in k iteration.
                False otherwise
        '''
        # Write n as 2**r . d + 1, where d is odd, by factorizing powers of 2 from n-1
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        # d is odd, n-1 = 2**r . d
        # print(f'{n = } = 2**r . d + 1, {d = }, {r = }')

        for _ in range(k):
            a = random.randrange(2, n-1)
            # x ← a**d mod n
            x = pow(a, d, n)
            # print(f'{a = } = rand[2, n-2], {x = } = (a**d) % n')
            if x == 1 or x == n-1:
                continue
            
            for _ in range(r-1):
                # x ← x**2 mod n
                x = pow(x, 2, n)
                if x == n-1:
                    continue
            
            return False
        return True

    def generate_prime(self):
        print('start: ', time()-self.timestamp)
        self.timestamp = time()
        while True:
            number = self.random_n_bits(self.n_bits)

            if not self.sieve_of_erathosthenes_test(number):
                # The number does not pass this test
                continue

            if not self.miller_rabin_test(number):
                # The number does not pass this test
                continue

            print('end: ', time() - self.timestamp)
            return number
                

if __name__ == "__main__":
    # Test generate prime, insert number of bits
    p = PrimeGenerator(1024)
    print(p.generate_prime())