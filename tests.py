#!/usr/bin/env sage

from sage.all import *
from encrypt import *
from gp import *

#p=761
# found q = 1000001773
# found q = 1000000000000000000030103
# found q = 1000000000000000000000000152973
def find_q(p,lower_bound_on_q):
    q = next_prime(lower_bound_on_q)
    print(q)
    end = False
    counter = 1
    while(not end):
        print(str(counter)+". starting")
        R = PolynomialRing(GF(q),'x')
        x = R.gens()[0]
        f = x**p-x-1
        print("polynomial: ", f)
        if f.is_irreducible():  # too complex... need to check irreduciblity more effectively
            end = True
            print("GOOD: ",q)
        else:
            q = next_prime(q+1)
            counter = counter + 1
            print("WRONG: ",q)

#p=761
# found q = 1000001773
def find_p(lower_bound_on_p,q):
    q = 1000000000000000000023643
    p = next_prime(lower_bound_on_p)
    print(p)
    end = False
    counter = 1
    while(not end):
        print(str(counter)+". starting")
        R = PolynomialRing(GF(q),'x')
        x = R.gens()[0]
        f = x**p-x-1
        print("polynomial: ", f)
        if f.is_irreducible():  # too complex... need to check irreduciblity more effectively
            end = True
            print("GOOD: ",p)
        else:
            p = next_prime(p+1)
            counter = counter + 1
            print("WRONG: ",p)

def encGPand(verbose=True,p=761,q=4591):
    print "-------------------------------------------------------------------"
    print "Evaluating Enc group program for gate AND with decryption"
    print "-------------------------------------------------------------------"
    S5 = SymmetricGroup(5)
    el1 = S5([2,3,4,5,1])
    el2 = S5([3,1,5,2,4])
    g1 = GroupProgram(S5,el1,1)
    #if(verbose):
    #    g1.printGP()
    g2 = GroupProgram(S5,el2,2)
    #if(verbose):
    #    g2.printGP()
    g1.andGP(g2)
    if(verbose):
        g1.printGP()
    egp = encrypt_trivial(g1,p,q,verbose)
    if(verbose):
        #egp.printGP()
        print(count_norm(egp.get_mat_zeros(0), q))
        print(count_norm(egp.get_mat_zeros(1), q))
        print(count_norm(egp.get_mat_zeros(2), q))
        print(count_norm(egp.get_mat_zeros(3), q))
        print(count_norm(egp.get_mat_ones(0), q))
        print(count_norm(egp.get_mat_ones(1), q))
        print(count_norm(egp.get_mat_ones(2), q))
        print(count_norm(egp.get_mat_ones(3), q))
    pub = egp.get_pzt()
    w = egp.evaluate([0,0,0,0],verbose)
    w_dummy = egp.evaluate_dummy([0,0,0,0],verbose)
    print "AND(0,0)=", decrypt(w,w_dummy,pub,p,q)
    w = egp.evaluate([0,1,0,1],verbose)
    w_dummy = egp.evaluate_dummy([0,1,0,1],verbose)
    print "AND(0,1)=", decrypt(w,w_dummy,pub,p,q)
    w = egp.evaluate([1,0,1,0],verbose)
    w_dummy = egp.evaluate_dummy([1,0,1,0],verbose)
    print "AND(1,0)=", decrypt(w,w_dummy,pub,p,q)
    w = egp.evaluate([1,1,1,1],verbose)
    w_dummy = egp.evaluate_dummy([1,1,1,1],verbose)
    print "AND(1,1)=", decrypt(w,w_dummy,pub,p,q)

def encGPor(verbose=True,p=761,q=4591):
    print "-------------------------------------------------------------------"
    print "Evaluating Enc group program for gate OR with decryption"
    print "-------------------------------------------------------------------"
    S5 = SymmetricGroup(5)
    el1 = S5([2,3,4,5,1])
    el2 = S5([3,1,5,2,4])
    g1 = GroupProgram(S5,el1,1)
    if(verbose):
        g1.printGP()
    g2 = GroupProgram(S5,el2,2)
    if(verbose):
        g2.printGP()
    g1.orGP(g2)
    egp = encrypt(g1,p,q,verbose)
    pub = egp.get_pzt()
    w = egp.evaluate([0,0,0,0],verbose)
    w_dummy = egp.evaluate_dummy([0,0,0,0],verbose)
    print "OR(0,0)=", decrypt(w,w_dummy,pub,p,q)
    w = egp.evaluate([0,1,0,1],verbose)
    w_dummy = egp.evaluate_dummy([0,1,0,1],verbose)
    print "OR(0,1)=", decrypt(w,w_dummy,pub,p,q)
    w = egp.evaluate([1,0,1,0],verbose)
    w_dummy = egp.evaluate_dummy([1,0,1,0],verbose)
    print "OR(1,0)=", decrypt(w,w_dummy,pub,p,q)
    w = egp.evaluate([1,1,1,1],verbose)
    w_dummy = egp.evaluate_dummy([1,1,1,1],verbose)
    print "OR(1,1)=", decrypt(w,w_dummy,pub,p,q)
