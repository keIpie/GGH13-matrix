from sage.all import *
from functools import partial
import multiprocessing as mp
import sys, os

class GroupProgram:
    def __init__(self,group=SymmetricGroup(5),el=SymmetricGroup(5).one(),num=0):
        self.group = group
        self.zeros = [group.one()]
        self.ones = [el]
        self.nonid = el
        self.vars = [num]
    def printGP(self):
        print "-------------------------------------------"
        print "GROUP: ", self.group
        print "ZEROS:", self.zeros
        print "ONES: ", self.ones
        print "VARIABLES: ", self.vars
        print "PRODUCT: ", self.nonid
        print "-------------------------------------------"
    def notGP(self,n=5):
        length = len(self.zeros)
        assert length != 0, "List is empty."
        #p = random_element_GP(self.group,n)
        #print "random:", p
        self.zeros[0] = self.nonid**(-1) * self.zeros[0]
        self.ones[0]  = self.nonid**(-1) * self.ones[0]
        self.zeros[length-1] = self.zeros[length-1]
        self.ones[length-1]  = self.ones[length-1]
        self.nonid = self.nonid**(-1)
    def andGP(self,GP2,n=5):
        if(self.group == SymmetricGroup(5)):
            while (self.nonid == GP2.nonid or self.nonid == GP2.nonid**(-1) or (self.nonid*GP2.nonid*self.nonid**(-1)*GP2.nonid**(-1)).cycle_type()[0]!= 5):
                self.changeGP(n)
        else:
            while (self.nonid == GP2.nonid or self.nonid == GP2.nonid**(-1)):
                self.changeGP(n)
        lengthGP2 = len(GP2.zeros)
        lengthGP1 = len(self.zeros)
        assert lengthGP1 != 0, "List is empty GP1."
        assert lengthGP2 != 0, "List is empty GP2."
        invZerosGP1 = []
        invOnesGP1  = []
        invVarsGP1 = []
        for i in xrange(lengthGP1):
            invZerosGP1.append(self.zeros[lengthGP1-1-i]**(-1))
            invOnesGP1.append(self.ones[lengthGP1-1-i]**(-1))
            invVarsGP1.append(self.vars[lengthGP1-1-i])
        invZerosGP2 = []
        invOnesGP2  = []
        invVarsGP2 = []
        for i in xrange(lengthGP2):
            invZerosGP2.append(GP2.zeros[lengthGP2-1-i]**(-1))
            invOnesGP2.append(GP2.ones[lengthGP2-1-i]**(-1))
            invVarsGP2.append(GP2.vars[lengthGP2-1-i])
        self.zeros = self.zeros + GP2.zeros + invZerosGP1 + invZerosGP2
        self.ones = self.ones + GP2.ones + invOnesGP1 + invOnesGP2
        #problem: komutator dwoch 5cykli nie musi byc 5 cyklem... a nonid musi byc!!! - zmienic tylko na alfa, beta, ich komutator??
        self.nonid = self.nonid * GP2.nonid * self.nonid**(-1) * GP2.nonid**(-1)
        self.vars = self.vars + GP2.vars + invVarsGP1 + invVarsGP2
    def orGP(self,GP2,n=5):
        self.notGP(n)
        GPnew = GroupProgram()
        GPnew = deepcopy(GP2)
        GPnew.notGP(n)
        self.andGP(GPnew,n)
        self.notGP(n)
    def xorGP(self,GP2,n=5):
        GPnew = GroupProgram()
        GPnew = deepcopy(GP2)
        GPnew.notGP(n)
        GPnew.andGP(self,n)
        self.notGP(n)
        self.andGP(GP2, n)
        self.orGP(GPnew, n)
    def changeGP(self,n=5):
        assert self.group==SymmetricGroup(5), "Group not known"
        ro  = SymmetricGroup(4).random_element()
        while(ro == self.nonid or ro == self.nonid.inverse()):
            ro  = SymmetricGroup(4).random_element()
        ro = SymmetricGroup(5)(ro)
        print "changeGP:", ro
        self.zeros[0] = ro * self.zeros[0]
        self.ones[0] = ro * self.ones[0]
        leng = len(self.zeros)
        self.zeros[leng-1] = self.zeros[leng-1] * ro.inverse()
        self.ones[leng-1] = self.ones[leng-1] * ro.inverse()
        self.nonid = ro * self.nonid * ro.inverse()
    def evaluate(self,indicies,n=5,verbose=True):
        assert len(self.zeros) == len(indicies), "List is empty GP1."
        result = self.group.one()
        for i in xrange(len(indicies)):
            assert indicies[i] == 0 or indicies[i] == 1, "Not binary index!"
            if (indicies[i] == 0):
                result = result * self.zeros[i]
            else:
                result = result * self.ones[i]
        if(verbose):
            print "indicies:", indicies
            if (self.group != BraidGroup(n)):
                print "result:", result
            else:
                print "result:", result.permutation()
        return result
    def evaluateShort(self,indicies):
        result = self.group.one()
        for i in xrange(len(self.zeros)):
            j = self.vars[i]
            assert indicies[j] == 0 or indicies[j] == 1, "Not binary index!"
            if (indicies[j] == 0):
                result = result * self.zeros[i]
            else:
                result = result * self.ones[i]
        print "indicies:", indicies
        return result
    def encrypt(self,a,n):
        length = len(self.zeros)
        assert length != 0, "Program is empty."
        print "Inverting scret parameter a..."
        inv_a = a**(-1)
        pool = mp.Pool(mp.cpu_count())
        pool.map(partial(self.enc_func, A=[inv_a, a, length]), [i for i in range(0,length,1)])
        #for i in xrange(length):
        #    print "Encrypting element ", i+1, "/", length
        #    self.zeros[i] = inv_a * self.zeros[i] * a
        #    self.zeros[i].left_normal_form()
        #    self.ones[i] = inv_a * self.ones[i] * a
        #    self.ones[i].left_normal_form()
    def enc_func(self, i, A):
        sys.stdout.write("\rEncrypting element %s/%s" %(i+1, A[2]))
        sys.stdout.flush()
        self.zeros[i] = A[0] * self.zeros[i] * A[1]
        self.zeros[i].left_normal_form()
        self.ones[i] = A[0] * self.ones[i] * A[1]
        self.ones[i].left_normal_form()

class EncryptedGroupProgram:
    def __init__(self, struct, zeros, ones, el, num, public, dummy_zeros, dummy_ones):
        self.struct = struct
        self.zeros = zeros
        self.ones = ones
        self.nonid = el
        self.vars = num
        self.public = public
        self.dummy_zeros = dummy_zeros
        self.dummy_ones = dummy_ones
    def printGP(self):
        print "-------------------------------------------"
        print "STRUCTURE: ", self.struct
        print "ZEROS:", self.zeros
        print "ONES: ", self.ones
        print "VARIABLES: ", self.vars
        print "PRODUCT: ", self.nonid
        print "PUBLIC PARAMETER: ", self.public
        print "DUMMY_ZEROS: ", self.dummy_zeros
        print "DUMMY_ONES: ", self.dummy_ones
        print "-------------------------------------------"
    def evaluate(self,indicies,verbose=False):
        assert len(self.zeros) == len(indicies), "List is empty GP1."
        result = self.struct(1)
        for i in xrange(len(indicies)):
            assert indicies[i] == 0 or indicies[i] == 1, "Not binary index!"
            if (indicies[i] == 0):
                result = result * self.zeros[i]
            else:
                result = result * self.ones[i]
        if (verbose):
            print "indicies:", indicies
        return result
    def evaluate_dummy(self,indicies,verbose=False):
        assert len(self.dummy_zeros) == len(indicies), "List is empty GP1."
        result = self.struct(1)
        for i in xrange(len(indicies)):
            assert indicies[i] == 0 or indicies[i] == 1, "Not binary index!"
            if (indicies[i] == 0):
                result = result * self.dummy_zeros[i]
            else:
                result = result * self.dummy_ones[i]
        if (verbose):
            print "indicies:", indicies
        return result
    def get_pzt(self):
        return self.public
    def get_mat_zeros(self,i):
        assert i<len(self.zeros) and i>=0, "wrong index"
        return self.zeros[i]
    def get_mat_ones(self,i):
        assert i<len(self.ones) and i>=0, "wrong index"
        return self.ones[i]

def random_element_GP(group,n=5):
    assert (group == Permutations(5) or group == SymmetricGroup(5) or group == BraidGroup(n)), "Group is not known"
    if (group == Permutations(5)):
        rand = group.random_element()
        el = group.element_in_conjugacy_classes([5])
        return rand**(-1) * el * rand
    elif (group == SymmetricGroup(5)):
        rand = group.random_element()
        el = group([2,3,4,5,1])
        return rand**(-1) * el * rand
    else:
        return randomLittleBraid(n,5)

def randomBraid(n):
    print "Generating braid of length ", n
    B = BraidGroup(n)
    d = B.Delta()
    u = randrange(n)
    table = []
    if (n%2 == 1): n = n-1
    for i in xrange(n/2):
        table.append(randrange(n-1)+1)
    print table
    b = B(table)
    return d**u*b

def randomLittleBraid(n,l):
    print "Generating braid of length ", l, "/", n
    B = BraidGroup(n)
    table = []
    for i in xrange(l):
        table.append(randrange(l-1)+1)
    b = B(table)
    return b
