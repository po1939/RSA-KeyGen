#import gmpy2
from gmpy2 import mpz, powmod, mul,gcd
import random
import sys


# returns False when composite,
def witness(d,n,r):

    # random int in [2,n-1)
    a = random.randrange(2, n-1)

   # x = a**d % n
    x = powmod(a,d,n)

    if (x == 1 or x == n-1):
        return True

    for i in range(r):
        x = (x**2) % n
        if x == 1:
            return False
        if x == n-1:
            return True
    return False


# uses Miller-Rabin Test to check if n is prime
# return True if the number is prime and false if it is not
def isPrime(n):
    # check 20 times. higher the number, more accurate it is
    s = 20
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 ==0:
        return False

    r = 0
    d = n-1
    while d % 2 != 1:
        d = d / 2
        r+= 1


    for i in range(s):
        if witness(d,n,r)== False:
            return False
    return True

#def modInverse(a,b):
 #   if b ==0:
  #      return(a,1,0)
   # (d1,x1,y1) = modInverse(b,a%b)
#
 #   (d,x,y) = (d1,y1,x1-a/b * y1)
  #  return (d,x,y)


# calculate modular invserse using Extended-Euclidean Algorithm
def modInverse(a,n):
    if n == 1:
        return 0
    x= 0
    y =1

    while (a >1):
        quotient = a/n

        temp = n
        n = a % n
        a = temp

        temp = x
        x = y - quotient * x
        y = temp

    return y

# create RSA key pairs with p and q
# p, q are prime numbers
# returns (public pair, private pair)
def keygen(p,q):

    n = mul(p,q)

    phiN = mul((p-1),(q-1))

    while True:
        e = random.randrange(2,phiN)
        e= mpz(e)
        if gcd(e,phiN) == 1:
            break

    d = modInverse(e,phiN)

    #print "mod inv of ",e, phiN,"is: ", d
    if d<0:
        d += phiN


    return ((e,n),(d,n))


def main():

    size = input("Enter modulus size: ")
    print

    # generating random numbers
    while True:
        myRand = random.getrandbits(size - 1) + (1 << size - 1)
        p = mpz(myRand)
        if isPrime(p):
            break

    while True:
        myRand = random.getrandbits(size - 1) + (1 << size - 1)
        q = mpz(myRand)
        if isPrime(q) and p!=q:
            break

    public, private = keygen(p,q)

    print ("Public Key: ",public)
    print
    print ("Private Key: ",private)

    # Change message to padded binary integer
    M = "I deserve an A"
    x = 0
    for c in M:
        x = x << 8

        x = x^ ord(c)


    # Digital Signature
    ciphertext = powmod(x,private[0],private[1])
    print
    print ("Signed Message: ",ciphertext)

    # Decrypt
    decrypted = powmod(ciphertext, public[0],public[1])

    # converting from padded integer to original message
    for i in reversed(range((decrypted.bit_length()+7) // 8)):
        sys.stdout.write(chr(decrypted[i*8:(i+1)*8]))
	
    print

main()
