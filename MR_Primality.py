#################################################
#          Simple, reliable algorithm           #
# Find primes less than or equal to some number #
#################################################
def kprimes(limit):
    primes = [2,3]
    n = 5
    follower = 3
    followerSquare = 9
    while (n <= limit):
        while followerSquare < n:
            follower += 1
            followerSquare += (2 * follower - 1)
        comp = 0
        for p in primes:
            if p > follower:
                break
            elif n%p == 0:
                comp = 1
                break
        if comp == 0:
            primes.append(n)
        n += 2
    return primes

#####################################
# Another, more efficient algorithm #
#####################################
import random
import sys

def sieve(suspect, pList, abovePlaces = 0, below = 0): #Sieve a single suspect, as last resort
    if below == 0:
        below = pList[-1]
    stop = len(pList)
    comp = 0
    for i in range(abovePlaces, stop):
        if pList[i] > below:
            break
        elif suspect % pList[i] == 0:
            comp = 1
            break
    return comp

def dragnet(lower, upper, flist): # Sections set of possible witnesses into cordons, along factorial numbers
    i = lower
    cordons = []
    while flist[i + 1] < upper:
        cordons.append([flist[i], flist[i + 1]])
        i += 1
    cordons.append([flist[i], upper])
    return cordons

def callWitness(n, d, cordon): # Select a random witness from a given cordon
    i = 1
    a = random.randint(cordon[0], cordon[1])
    while ((((a ** d) % n) == 1) or (((a ** d) % n) == (n - 1))): # Select new witness, if a^d eq. +/-1 (mod n).
        a = random.randint(cordon[0], cordon[1])
        i+=1
        if i >= (cordon[1]-cordon[0])/10:
            i = 0
            break
    if i == 0: #If random selection keeps failing, try each witness for selection
        for i in range(cordon[0]+2, cordon[1] + 1):
            if ((((i ** d) % n) != 1) and (((i ** d) % n) != (n - 1))):
                a = i
                i = 0 ###Move outside loop?
                break
    if i == 0:
        return 0
    return a

def interrogate(suspect): #determine d, where n = 2^sd + 1
    s = 0
    suspect -= 1
    while (suspect % 2) == 0:
        s += 1
        suspect = int(suspect/2)
    return(suspect, s)

def testify(n, d, s, a): #Check if a is witness for compositeness of n
    comp = 1
    for r in range(s):
        if ((a ** ((2 ** r) * d)) % n) == (n - 1):
            comp = 0
            break
    return comp

#Menu options
printprimes = -1
checkagainstsieve = -1
findamount = -1
mersennes = -1

#Menu
print('Primality testing! We can test for primes up through any integer larger than 10.')
limit = input('Please enter the biggest integer you\'d like to check, or type \"options\" to see more options:\n')
while limit in ['options', 'print', 'check', 'amount', 'mers']:
    if limit == 'print':
        printprimes = printprimes * (-1)
    elif limit == 'check':
        checkagainstsieve = checkagainstsieve * (-1)
    elif limit == 'amount':
        findamount = findamount * (-1)
    elif limit == 'mers':
        mersennes = mersennes * (-1)
    if printprimes == 1:
        print('You selected to print the list of primes at the end of the search.')
        print('Type \"print\" to toggle this option off.')
    else:
        print('Type \"print\" to print the list of primes found at the end.')
    if checkagainstsieve == 1:
        print('You selected to check the algorithm\'s results against the sieve algorithm at the end.')
        print('Type \"check\" to toggle this option off.')
    else:
        print('Type \"check\" to check the algorithm\'s results against the sieve algorithm at the end.')
    if findamount == 1:
        print('You selected to find an inputted number of prime numbers.')
        print('Type \"amount\" to toggle this option off.')
    else:
        print('Type \"amount\" to instead find a certain number of prime numbers.')
    if mersennes == 1:
        print('You selected to gather mersenne numbers, and to check them at the end.')
        print('Type \"mers\" to toggle this option off.')
    else:
        print('Type \"mers\" to also catalog mersenne primes and pseudoprimes.')
    print('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-')
    limit = input('Enter a keyword for an option, or a positive integer to run the algorithm!:\n')

limit = int(limit)

#Search through first k, or for k-many?
if findamount == 1:
    goal = limit
    limit = float('inf')

n = 9
primes = [2, 3, 5, 7] #initial primes set
usualSuspects = [2, 3, 5, 7] #designated set of small primes, for quick mod testing before MR test

# Following variables, to keep witnesses below 2Ln(2)^2

squarefollow = 2
squareNComp = 4

expfollow = 2
expAComp = 8
expNComp = 4

factPComp = 2

flist = [2, 6, 24, 120] #initial factorial numbers

while n < limit:
    sys.stdout.write("\rCurrently trialling: %i" % n)
    sys.stdout.flush()
    comp = 0

    comp = sieve(n, usualSuspects, 1) #Quick mod check against small primes
    over = len(usualSuspects) #Set lover limit

    if comp == 0:
        while expNComp * 2 < n: #Adjust following variables for upper limit
            expfollow += 1
            expAComp += (4 * expfollow - 2)
            expNComp = expNComp * 2
            if (flist[-1] < expAComp):
                flist.append(flist[-1] * (len(flist) + 2))
                usualSuspects.append(primes[len(usualSuspects)])
                while flist[factPComp] < usualSuspects[-1]:
                    factPComp += 1

        [d, s] = interrogate(n)
        for p in usualSuspects: #MR check against small primes
            if ((((p ** d) % n) != 1) and (((p ** d) % n) != (n - 1))):
                comp = testify(n, d, s, p)
                if comp == 1:
                    break

    if comp == 0 and flist[-1] < expAComp: #MR check against random witnesses
        cordons = dragnet(factPComp, expAComp, flist)
        for i in range(len(cordons)):
            a = callWitness(n, d, cordons[i])
            if a != 0:
                comp = testify(n, d, s, a)
            if comp == 1:
                break

    if comp == 0: # Still think it's prime? Submit it to the sieve
        while squareNComp < n: #Update square following variable
            squareNComp += (2 * squarefollow + 1)
            squarefollow += 1
        comp = sieve(n, primes, over - 1, squarefollow)

    if comp == 0:
        primes.append(n)

    if findamount == 1: # End search, if number of primes is set and fulfilled
        if len(primes) == goal:
            n += 2
            break

    n += 2

#Print results
print()
print('We found',len(primes), 'prime numbers.')
print('The more, the merrier!')

if printprimes == 1:
    print('Here they all are:')
    print(primes)

if mersennes == 1: #Gather mersennes suspects, sort by prime/composite
    maxp = max(primes)
    msusps = []
    mprimes = []
    mcomps = []
    for p in primes:
        m = 2 ** p - 1
        if m > maxp:
            break
        msusps.append(m)
    for m in msusps:
        if m in primes:
            mprimes.append(m)
        else:
            mcomps.append(m)
    print('Any mersenne primes that we stumbled upon are shown below:')
    print(mprimes)
    print('These mersenne numbers were set aside, but found to be composite. Don\'t ask me to factor them!')
    print(mcomps)

if checkagainstsieve == 1: #Optional check against sieve
    print('Comparing to sieve:')
    primescheck = kprimes(n - 2)
    if primes == primescheck:
        print('Yay! It matches the sieve!')
    else:
        falsepos = []
        falseneg = []
        for p in primes:
            if not(p in primescheck):
                falsepos.append(p)
        for p in primescheck:
            if not(p in primes):
                falseneg.append(p)
        print('Whoops! something went wrong.')
        print('We had', len(falsepos), 'false positive results.')
        print('We had', len(falseneg), 'false negative results.')
        print('False positives:')
        print(falsepos)
        print('False negatives:')
        print(falseneg)
