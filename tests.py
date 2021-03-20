#!/usr/bin/env sage

from sage.all import *
from encrypt import *
from gp import *
from groupring import *


def encGPand(verbose=True,p=761,q=4591):
    print "-------------------------------------------------------------------"
    print "Evaluating Enc group program for gate AND over RG with decryption"
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
    g1.andGP(g2)
    egp = encrypt(g1,p,q,verbose)
    pub = egp.get_pzt()
    w = egp.evaluate([0,0,0,0],verbose)
    w_dummy = egp.evaluate_dummy([0,0,0,0],verbose)
    print "AND(0,0)=", checkID(decrypt(w,w_dummy,pub,p,q))
    w = egp.evaluate([0,1,0,1],verbose)
    w_dummy = egp.evaluate_dummy([0,1,0,1],verbose)
    print "AND(0,1)=", checkID(decrypt(w,w_dummy,pub,p,q))
    w = egp.evaluate([1,0,1,0],verbose)
    w_dummy = egp.evaluate_dummy([1,0,1,0],verbose)
    print "AND(1,0)=", checkID(decrypt(w,w_dummy,pub,p,q))
    w = egp.evaluate([1,1,1,1],verbose)
    w_dummy = egp.evaluate_dummy([1,1,1,1],verbose)
    print "AND(1,1)=", checkID(decrypt(w,w_dummy,pub,p,q))

def encGPor(verbose=True,p=761,q=4591):
    print "-------------------------------------------------------------------"
    print "Evaluating Enc group program for gate OR over RG with decryption"
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
    print "OR(0,0)=", checkID(decrypt(w,w_dummy,pub,p,q))
    w = egp.evaluate([0,1,0,1],verbose)
    w_dummy = egp.evaluate_dummy([0,1,0,1],verbose)
    print "OR(0,1)=", checkID(decrypt(w,w_dummy,pub,p,q))
    w = egp.evaluate([1,0,1,0],verbose)
    w_dummy = egp.evaluate_dummy([1,0,1,0],verbose)
    print "OR(1,0)=", checkID(decrypt(w,w_dummy,pub,p,q))
    w = egp.evaluate([1,1,1,1],verbose)
    w_dummy = egp.evaluate_dummy([1,1,1,1],verbose)
    print "OR(1,1)=", checkID(decrypt(w,w_dummy,pub,p,q))

def checkID(s):
    S5 = SymmetricGroup(5)
    id = S5.identity()
    if(s==id):
        return 0
    else:
        return 1
