import math
import random

import math
import random

# return d = gcd(a, b)
def gcd(a, b):
    if (b==0):
        return a
    else:
        return gcd(b, a%b)

# return (x,y,d) such that a*x+b*y = d = gcd(a,b)
def exGcd(a, b):
    if (b==0):
        return (1,0,a);
    else:
        (y,x,d) = exGcd(b, a%b)   # which means y*b + x*(a%b) = d, i.e. y*b + x*(a-a/b*b) = d <=> a*x + b*(y-a/b*x) = d
        return (x, y-a/b*x, d)

# return inva in {1, 2, ..., p-1} such that inva*a = 1(mod p)
# This is a wrapper function for exGcd(a, p)
def inverse(a, p):
    (inva, tmp1, tmp2) = exGcd(a, p)
    return inva % p;

# return a list whose element x satiefies a*x = b (mod m) and in the range of {0, 1, ..., m-1}
# return [] if not feasible
# This is a wrapper function for exGcd(a, p)
def solvemod(a, b, m):
    (x, y, d) = exGcd(a, m);
    if b%d==0:
        print( "have ", d, " answers")
        x0, delta = b/d*x%m, m/d
        return [(x0+delta*i)%m for i in xrange(d)]
    else:
        print( a, b, d, m, " Not feasible!")
        return []

# return a**b%p. If p=0, no modulo is taken.
def powermod(a, b, p=0):
    res, tmp = 1, a
    if p!=0:
        while b>0:
            if (b&1)==1:
                res = res * tmp % p
            tmp = tmp * tmp % p
            b >>= 1
            #print("result,tmp = ", res,tmp)
    else:
        while b>0:
            if (b&1)==1:
                res = res * tmp
            tmp = tmp * tmp
            b >>= 1
            
    return res








# returns a list which contains all its prime factors
# assume n is larger than 100(if n is too small, Pollard-Rho may get into an endless loop)
def factorList(n):

    # using Pollard-Rho Algorithm to factor n
    if millerRabin(n)==True:
        return [n]
    else:
        factor1 = pollardrhoNT(n)
        print(factor1, n/factor1)
        return factorList(factor1) + factorList(n/factor1)


# returns a dictionary which contains all its prime factors
# this is a wrapper function for factorList(n)
# assume n>1
def factorDict(n):

    factors = []

    # try to figure out all prime factors < 100
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 
            53, 59, 61, 61, 67, 71, 73, 79, 83, 89, 91, 97]
    for i in small:
        while (n%i==0):
            factors.append(i)
            n /= i
    if n>1:
        factors = factors + factorList(n)
    s = set(factors)
    ans = {}
    for i in s:
        ans[i] = factors.count(i)
    return ans







class ElGamalKey:
    
    SMOOTH = 10**15     # bound for smooth numbers

    def __init__(self, p_, alpha_, a_, beta_):
        self.p, self.alpha, self.a, self.beta = p_, alpha_, a_, beta_

    def publicKey(self):
        return (self.p, self.alpha, self.beta)

    def privateKey(self):
        return self.a

    # generate a random key whose p in [rangep, ~2*rangep]
    # difficulty: 0 for random, 1 for easy, 2 for normal, 3 for difficult, 4 for crazy
    def randomKey(self, difficulty = 2, rangep = 0):
        if rangep==0:
            if difficulty==0:
                rangep = random.randint(10**10, 10**25)
            elif difficulty==1:
                rangep = 10**10
            elif difficulty==2:
                rangep = 10**15
            elif difficulty==3:
                rangep = 10**20
            else:
                rangep = 10**30
                
        # randomly choose a prime number as p
        
        
        self.p = random.randint(rangep, 2*rangep)
        if self.p%2==0:         # try odd numbers only
            self.p += 1
        cnt = 0
        while (True):
            self.p += 2
            cnt += 1
            if cnt>29 and cnt%30==0:
                print("Try to choose", self.p, ". Please be patient...")

            if millerRabin(self.p)==True:
                mydct = {}
                if (difficulty!=4):    # Just use smooth number for non-crazy case
                    mydct = factorDict(self.p-1)
                    if max(mydct.keys())>self.SMOOTH:
                        continue;
                self.alpha = findPrimitiveRoot(self.p, mydct)
                if (difficulty==1 or difficulty==2):
                    self.a = random.randint(1, self.p - 2)
                else:                                       # self.a is of the same order with self.p
                    self.a = random.randint(self.p/10, self.p*9/10)
                self.beta = powermod(self.alpha, self.a, self.p)
                return (self.p, self.alpha, self.a, self.beta)

        return (2579, 2, 765, 949) # this part should never be visited(though this is a valid key)


    # ElGamal Encryption
    def encrypt(self, x):
        print("..............Encrypting..........")
        r = random.randint(1, self.p - 2)
        y1 = powermod(self.alpha, r, self.p)
        cipher=[]
        for i in x:
            y2 = ord(i) * powermod(self.beta, r, self.p) % self.p
            cipher.append([y1,y2])
        #y2 = ord(x) * powermod(self.beta, r, self.p) % self.p
        return (cipher)
    
    # ElGamal Decryption
    def decrypt(self, y):
        print("...............Decrypting..........")
        s=""
        for y1 in y:
            s=s+chr(y1[1] * powermod(inverse(y1[0], self.p), self.a) % self.p) # y[1] * y[0]^(-a) (mod p)
        return s

    # used for debug
    def show(self):
        print("p, alpha, a, beta = ", self.p, self.alpha, self.a, self.beta)








print("...............Generating Key............")

key = ElGamalKey(2579, 2, 765, 949) 
print("key generated")

print("\n \n")
plain = "hello world"

print("...............Plain text............")
print(plain)
print("\n \n")
cipher = key.encrypt(plain)
print("\n")
print(" ciphertext in form of (c1,c2):")
print(cipher)
print("\n ")

deciphered = key.decrypt(cipher)
print("\n ")
print("decrypted text:")


print(deciphered)