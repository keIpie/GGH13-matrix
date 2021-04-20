#!/usr/bin/env sage

from sage.all import *
from gp import *

def lift_matrix_elements(mat,M):
    lifted = []
    for i in range(len(mat.rows())):
        row = []
        for j in range (len(mat[0])):
            row.append(mat[i][j].lift())
        lifted.append(row)
    return M(lifted)


def encode(num,maxnum,groupElement1,groupElement2,G,Fq,Fq_tiny):
    print("Encoding matrix: ",num, "/",maxnum)
    M5  = MatrixSpace(Fq,5,5)
    M10 = MatrixSpace(Fq,10,10)
    M5_tiny  = MatrixSpace(Fq_tiny,5,5)
    M1 = M5(groupElement1.matrix())
    M2 = M5(groupElement2.matrix())
    if (num==0):
        el1 = M10(block_matrix([
                [M5.zero_matrix(), lift_matrix_elements(M5_tiny.random_element(),M5)*G],
                [M1, lift_matrix_elements(M5_tiny.random_element(),M5)*G]]))
        el2 = M10(block_matrix([
                [M5.zero_matrix(),lift_matrix_elements(M5_tiny.random_element(),M5)*G],
                [M2,lift_matrix_elements(M5_tiny.random_element(),M5)*G]]))
    elif (num==maxnum):
        el1 = M10(block_matrix([
                [lift_matrix_elements(M5_tiny.random_element(),M5),lift_matrix_elements(M5_tiny.random_element(),M5)*G + M1],
                [lift_matrix_elements(M5_tiny.random_element(),M5),lift_matrix_elements(M5_tiny.random_element(),M5)*G]]))
        el2 = M10(block_matrix([
                [lift_matrix_elements(M5_tiny.random_element(),M5),lift_matrix_elements(M5_tiny.random_element(),M5)*G + M2],
                [lift_matrix_elements(M5_tiny.random_element(),M5),lift_matrix_elements(M5_tiny.random_element(),M5)*G]]))
    else:
        el1 = M10(block_matrix([
                [M1,lift_matrix_elements(M5_tiny.random_element(),M5)*G],
                [M5.zero_matrix(),lift_matrix_elements(M5_tiny.random_element(),M5)*G]]))
        el2 = M10(block_matrix([
                [M2,lift_matrix_elements(M5_tiny.random_element(),M5)*G],
                [M5.zero_matrix(),lift_matrix_elements(M5_tiny.random_element(),M5)*G]]))
    return (el1, el2)

def encrypt_trivial(g1,p,q,verbose=True):
    print("Encrypting group program with:",p,q)

    S5 = SymmetricGroup(5)

    R = PolynomialRing(GF(q),'x')
    x = R.gens()[0]
    f = x**p-x-1
    Fq = QuotientRing(R,f)
    M5 = MatrixSpace(Fq,5,5)
    MQ = MatrixSpace(Fq,10,10)
    SQ = SL(10,Fq).matrix_space()

    #q_small = next_prime(int(sqrt(q)))
    q_small = 7
    R_small = PolynomialRing(GF(q_small),'y')
    y = R_small.gens()[0]
    f_small = y**p-y-1
    Fq_small = QuotientRing(R_small,f_small)
    SQ_small = SL(10,Fq_small).matrix_space()

    #q_tiny = next_prime(int(sqrt(sqrt(q))))
    q_tiny = 3
    R_tiny = PolynomialRing(GF(q_tiny),'z')
    z = R_small.gens()[0]
    f_tiny = z**p-z-1
    Fq_tiny = QuotientRing(R_tiny,f_tiny)

    g = x**7+3*x**4+1
    G = g * M5.identity_matrix()
    Ginv = MQ(block_matrix([[M5.zero_matrix(),M5.zero_matrix()],[M5.zero_matrix(),G.inverse()]]))

    encZeros = []
    encOnes = []
    dummyZeros = []
    dummyOnes = []

    public = MQ.zero_matrix()

    Zi = lift_matrix_elements(SQ_small.random_element(),SQ)
    Zo = SQ.random_element()
    H  = lift_matrix_elements(SQ_small.random_element(),SQ)

    for i in xrange(len(g1.zeros)):
        if(i != len(g1.zeros) - 1):
            Zi2 =  SQ.random_element()
            Zi2o = Zi2.inverse()
            (g1m, g2m) = encode(i,len(g1.zeros)-1,g1.zeros[i],g1.ones[i],G,Fq,Fq_tiny)
            (d1m, d2m) = encode(i,len(g1.zeros)-1,S5.identity(),S5.identity(),G,Fq,Fq_tiny)
            enc = Zi * g1m * Zi2o
            encZeros.append(enc)
            denc = Zi * d1m * Zi2o
            dummyZeros.append(denc)
            enc = Zi * g2m * Zi2o
            encOnes.append(enc)
            denc = Zi * d2m * Zi2o
            dummyOnes.append(denc)
            Zi  = Zi2
            Zio = Zi2o
        else:
            (g1m, g2m) = encode(i,len(g1.zeros)-1,g1.zeros[i],g1.ones[i],G,Fq,Fq_tiny)
            (d1m, d2m) = encode(i,len(g1.zeros)-1,S5.identity(),S5.identity(),G,Fq,Fq_tiny)
            enc = Zi * g1m * Zo
            encZeros.append(enc)
            denc = Zi * d1m * Zo
            dummyZeros.append(denc)
            enc = Zi * g2m * Zo
            encOnes.append(enc)
            denc = Zi * d2m * Zo
            dummyOnes.append(denc)
    public = Zo.inverse() * Ginv * H
    eg = EncryptedGroupProgram(MQ, encZeros, encOnes, g1.nonid, g1.vars, public, dummyZeros, dummyOnes)
    #if(verbose):
    #    eg.printGP()
    return eg

def encrypt(g1,p,q,verbose=True):
    print("Encrypting group program with:",p,q)

    S5 = SymmetricGroup(5)

    R = PolynomialRing(GF(q),'x')
    x = R.gens()[0]
    f = x**p-x-1
    Fq = QuotientRing(R,f)
    M5 = MatrixSpace(Fq,5,5)
    MQ = MatrixSpace(Fq,10,10)
    SQ = SL(10,Fq).matrix_space()

    #q_small = next_prime(int(sqrt(q)))
    q_small = 7
    R_small = PolynomialRing(GF(q_small),'y')
    y = R_small.gens()[0]
    f_small = y**p-y-1
    Fq_small = QuotientRing(R_small,f_small)
    SQ_small = SL(10,Fq_small).matrix_space()

    #q_tiny = next_prime(int(sqrt(sqrt(q))))
    q_tiny = 3
    R_tiny = PolynomialRing(GF(q_tiny),'z')
    z = R_small.gens()[0]
    f_tiny = z**p-z-1
    Fq_tiny = QuotientRing(R_tiny,f_tiny)

    g = x**7+3*x**4+1
    G = g * M5.identity_matrix()

    encZeros = []
    encOnes = []
    dummyZeros = []
    dummyOnes = []

    public = MQ.zero_matrix()

    Zi = lift_matrix_elements(SQ_small.random_element(),SQ)
    Zo = SQ.random_element()
    H  = lift_matrix_elements(SQ_small.random_element(),SQ)

    for i in xrange(len(g1.zeros)):
        if(i != len(g1.zeros) - 1):
            Zi2 =  SQ.random_element()
            Zi2o = Zi2.inverse()
            (g1m, g2m) = encode(i,len(g1.zeros)-1,g1.zeros[i],g1.ones[i],G,Fq,Fq_tiny)
            (d1m, d2m) = encode(i,len(g1.zeros)-1,S5.identity(),S5.identity(),G,Fq,Fq_tiny)
            enc = Zi * g1m * Zi2o
            encZeros.append(enc)
            denc = Zi * d1m * Zi2o
            dummyZeros.append(denc)
            enc = Zi * g2m * Zi2o
            encOnes.append(enc)
            denc = Zi * d2m * Zi2o
            dummyOnes.append(denc)
            Zi  = Zi2
            Zio = Zi2o
        else:
            (g1m, g2m) = encode(i,len(g1.zeros)-1,g1.zeros[i],g1.ones[i],G,Fq,Fq_tiny)
            (d1m, d2m) = encode(i,len(g1.zeros)-1,S5.identity(),S5.identity(),G,Fq,Fq_tiny)
            enc = Zi * g1m * Zo
            encZeros.append(enc)
            denc = Zi * d1m * Zo
            dummyZeros.append(denc)
            enc = Zi * g2m * Zo
            encOnes.append(enc)
            denc = Zi * d2m * Zo
            dummyOnes.append(denc)
    public = Zo.inverse() * MQ(block_matrix([[M5.zero_matrix(),M5.zero_matrix()],[M5.zero_matrix(),G.inverse()]])) * H
    eg = EncryptedGroupProgram(MQ, encZeros, encOnes, g1.nonid, g1.vars, public, dummyZeros, dummyOnes)
    #if(verbose):
    #    eg.printGP()
    return eg

def decrypt(enc, enc_dummy, pub, p, q):
    print("Decrypting the result")
    #print("enc norm:", count_norm(enc,q))
    #print("enc_dummy norm:", count_norm(enc_dummy,q))
    #print("diff norm:", count_norm((enc - enc_dummy),q))
    res = (enc - enc_dummy) * pub
    res_enc = enc * pub
    res_dum = enc * enc_dummy * pub
    #print("res enc norm:", count_norm(res_enc,q))
    #print("res dum norm:", count_norm(res_dum,q))
    #print("res norm:", count_norm(res,q))
    #print("result matrix:", res)
    norm = count_norm(res,q)
    compare_q = float(sqrt(sqrt(q)))**3
    print (norm, compare_q)
    print (float(norm) < compare_q)
    if float(norm) < compare_q:
        return 0
    else:
        return 1

def count_norm(mat,q):
    #print("Counting maximum norm of a matrix")
    norm = 0
    for i in range(len(mat.rows())):
        for j in range(len(mat[0])):
            poly_coeffs = []
            for c in mat[i,j].list():
                mid = int(q/2)
                if c < mid:
                    poly_coeffs.append(c)
                else:
                    poly_coeffs.append(q-c)
            poly_max = max(poly_coeffs)
            if (poly_max > norm):
                norm = poly_max
    return norm
