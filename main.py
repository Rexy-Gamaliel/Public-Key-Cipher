from src.utility import *

if __name__ == "__main__":
    message = readfile('./input.txt')
    print(message)
    writefile('./output.txt', message)
    print(readfile('./output.txt'))