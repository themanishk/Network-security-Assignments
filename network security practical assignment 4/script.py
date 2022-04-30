# PRNG 1 -> Linear Congruential Generator
import time
import os


class LCG_Class:
  def __init__(self):
    custom_seed = os.name+os.getcwd()+str(time.time_ns()) 
    
    self.s = 1
    for i in range(len(custom_seed)):
        ch = custom_seed[i]
        in1 = ord(ch) 
        self.s = self.s * in1
    self.s = int(str(self.s)[:10]) + time.time_ns()
    self.a = 1664525
    self.c = 1013904223
    #self.m = 2**32
    self.m= 270

  def seed(self,seed):
    self.s = seed

  def randnumbers(self,n):
    numbers = []
    for i in range(n):
      self.s = (self.a * self.s + self.c) % self.m
      numbers.append(int(self.s))
      
    return numbers

  def randnumber(self):
    self.s = (self.a * self.s + self.c) % self.m
      
    return int(self.s)

  def randrange(self,start,end):
    return self.choice(range(start,end))

  def randint(self,start, end):
    return self.choice(range(start,(end+1)))

  def choice(self, the_list):
    count = 0
    number = len(the_list)
 
    while (number > 0):
     number = number//10
     count = count + 1
    while True:
     sequance = int(str(self.randnumber())[-count:])
     if not (len(the_list)-1) < sequance:
       return the_list[sequance]

  def shuffle(self,the_list):
    copy_of_list = the_list.copy()
    for i in reversed(range(len(the_list))):
      selection = self.choice(copy_of_list)
      the_list[i] = selection
      copy_of_list.remove(the_list[i])

  def sample(self, the_list, k):
    copy_of_list = the_list.copy()
    self.shuffle(copy_of_list)
    return copy_of_list[-k:]

  def random(self):
    return (self.randint(0, 10**5)/ 10**5)

  def uniform(self,start,end):
    return self.randint(start, end) + self.random()


LCG = LCG_Class()
random_nums_LCG=LCG.randnumbers(200)
print("generated random numbers: ")
print(random_nums_LCG)

# PRNG 2 -> BLUM BLUM SHUB
from random import randint, getrandbits
from math import gcd as bltin_gcd


def coprime(a, b):
    return bltin_gcd(a, b) == 1

def findX(p, q):
    if(isPrime(p) and isCongruentNumber(p) and isPrime(q) and isCongruentNumber(q)):
        n = p * q
        x = 1
        while (coprime(n, x)):
            x = randint(0, n)
        return x
def isCongruentNumber(number):
    # a - b = k * n
    # b = 3
    # k = 4
    # number - 3 = 4 * n
    if((number - 3) % 4 == 0):
        return True
    else:
        return False
def isPrime(number):
    if number == 1 or number == 2 or number == 3:
        return True
    if number == 4:
        return False

    index = 3
    while number > index:
        if number % index == 0:
            return False
        else:
            index += 1

    if(index == number):
        return True
    
def isPrime(number):
    if number == 1 or number == 2 or number == 3:
        return True
    if number == 4:
        return False

    index = 3
    while number > index:
        if number % index == 0:
            return False
        else:
            index += 1

    if(index == number):
        return True
    
    

class BBS:
    p = 0
    q = 0
    n = 0
    seed = 0
    generatedValues = []

    def __init__(self, p, q):
        self.setP(p)
        self.setQ(q)
        if(self.p > 0 and self.q > 0):
            self.__setN()
            self.__setSeed()

    def setP(self, p):
        if(not self.__checkParams(p)):
            self.p = p

    def setQ(self, q):
        if(not self.__checkParams(q)):
            self.q = q

    def __checkParams(self, number):
        isError = False
        if(not isPrime(number)):
            print(number, 'is not prime')
            isError = True

        return isError

    def __setN(self):
        self.n = self.p * self.q

    def __setSeed(self):
        while(not coprime(self.n, self.seed) and self.seed < 1):
            self.seed = randint(0, self.n - 1)

    def __generateValue(self):
        if(self.p > 0 and self.q > 0):
            x = 0
            while (not coprime(self.n, x)):
                x = randint(0, self.n)
            return pow(x, 2) % self.n

    def generateBits(self, amount):
        if(self.p == self.q):
            print('p should be diffrent than q')
            return False

        if (self.n == 0):
            print('N is equal 0')
            return False

        else:
            bitsArray = []
            generated=[]
            amount += 1

            for i in range(amount):
                generatedValue = self.__generateValue()
                self.generatedValues.append(generatedValue)
                generated.append(generatedValue)

                if(generatedValue % 2 == 0):
                    bitsArray.append(0)
                else:
                    bitsArray.append(1)

            return bitsArray,generated
        

        


bits = BBS(7, 47)
bits = bits.generateBits(2000)
random_nums_BBS=bits[1]
print("generated random numbers: ")
print(bits[1])



#Randomness test 1 -> Monte Carlo Test for Randomness
import sys
import math

print("................Randomness test 1 -> Monte Carlo Test for Randomness.........\n")





def runtest1(values):
    max=350.0
    inval=0.0
    outval=0.0
    ptr=0
    for i in range(0,len(values)//2):
        x = (values[ptr]-max/2)/(max/2)
        y = (values[ptr+1]-max/2)/(max/2)

        z = math.sqrt(x*x+y*y)
        
        if (z<1):
            inval=inval+1
        else:
            outval=outval+1
        ptr=ptr+2
    return 4.0*inval/(inval+outval)

print("....... result of Monte Carlo Test for Randomness for Linear Congruential Generator  :  ", runtest1(random_nums_LCG))
print( "\n \n")

print("....... result of Monte Carlo Test for Randomness BLUM BLUM SHUB :  ", runtest1(random_nums_BBS))





# #Randomness test 2 -> Runs test for Randomness

import random
import math
import statistics

print("................Randomness test 2 -> Runs test for Randomness.........\n")
def runsTest(l, l_median):

	runs, n1, n2 = 0, 0, 0
	
	# Checking for start of new run
	for i in range(len(l)):
		
		# no. of runs
		if (l[i] >= l_median and l[i-1] < l_median) or \
				(l[i] < l_median and l[i-1] >= l_median):
			runs += 1
		
		# no. of positive values
		if(l[i]) >= l_median:
			n1 += 1
		
		# no. of negative values
		else:
			n2 += 1

	runs_exp = ((2*n1*n2)/(n1+n2))+1
	stan_dev = math.sqrt((2*n1*n2*(2*n1*n2-n1-n2))/ \
					(((n1+n2)**2)*(n1+n2-1)))

	z = (runs-runs_exp)/stan_dev

	return z
	
# Making a list of 100 random numbers


lcg_median= statistics.median(random_nums_LCG)
bbs_median= statistics.median(random_nums_BBS)

Z_LCG = abs(runsTest(random_nums_LCG, lcg_median))
Z_BBS = abs(runsTest(random_nums_BBS, bbs_median))

print('Z-statistic for linear congruent generator:  ', Z_LCG)
print("\n")
if(Z_LCG<1.96):
    print("Z-statistic is less Z_critical(1.96) so the numbers can be declared as random")

print("\n\n")

print('Z-statistic for BLUM BLUM SHUP:  ', Z_BBS)

print("\n")

if(Z_LCG<1.96):
    print("Z-statistic is less than Z_critical(1.96) so the numbers can be declared as random")


