#!/usr/bin/env sage

""" preparing circuits to be obfuscated """
""" similiar format to galois 5gen, try to make it the same later """

import functools, os, sys, time
from sage.all import *

def checkkey(key):
    l = len(key)
    k = ceil(log(l,2))
    assert l!=0, "no key bits given"
    with open('circuits/checkkey-'+key+'.circ', 'w') as fw:
        fw.write(": nins "+str(l)+"\n")
        fw.write(": depth "+str(k)+"\n")
        fw.write("# TEST "+key+" 1\n")
        for i in xrange(3):
            fw.write("# TEST "+randnotkey(key)+" 0\n")
        num = l
        key2 = []
        for i in xrange(l):
            if (key[i]=="0"):
                fw.write(str(num)+" gate NOT "+str(i)+"\n")
                #print str(num)+" gate NOT "+str(i)+"\n"
                key2.append(num)
                num = num + 1
            else:
                key2.append(i)
        numB = num
        tmp = 0
        cnt = 0
        for i in xrange(floor(l/2)):
            fw.write(str(num)+" gate AND "+str(key2[2*i])+" "+str(key2[2*i+1])+"\n")
            #print str(num)+" gate AND "+str(key2[2*i])+" "+str(key2[2*i+1])+"\n"
            num = num + 1
        if (l%2!=0):
            tmp = key2[l-1]
            cnt = 1
        numA = num
        for i in range(2,floor(log(l,2))+1):
            for j in xrange(floor(l/2**i)):
                if (i!=floor(log(l,2)) or j!=floor(l/2**i)-1):
                    fw.write(str(num)+" gate AND "+str(numB+2*j)+" "+str(numB+2*j+1)+"\n")
                    #print str(num)+" gate AND "+str(numB+2*j)+" "+str(numB+2*j+1)+"\n"
                    num = num + 1
                else:
                    if(cnt==0):
                        fw.write(str(num)+" output AND "+str(numB+2*j)+" "+str(numB+2*j+1)+"\n")
                        #print str(num)+" output AND "+str(numB+2*j)+" "+str(numB+2*j+1)+"\n"
                    else:
                        fw.write(str(num)+" gate AND "+str(numB+2*j)+" "+str(numB+2*j+1)+"\n")
                        #print str(num)+" gate AND "+str(numB+2*j)+" "+str(numB+2*j+1)+"\n"
                        num = num + 1
            if ((l-cnt)%(2**(i+1))!=0):
                if(cnt==1):
                    if(i==(k-1)):
                        fw.write(str(num)+" output AND "+str(num-1)+" "+str(tmp)+"\n")
                    else:
                        fw.write(str(num)+" gate AND "+str(numA-1)+" "+str(tmp)+"\n")
                        cnt = 0
                        num = num + 1
                else:
                    tmp = numA-1
                    cnt = 1
            numB = numA
            numA = num
            if((numA-numB)%2!=0):
                tmp = numA-1
                cnt = 1
            #print "numB", numB
            #print "numA", numA

def randnotkey(key):
    l = len(key)
    result = key
    while(result == key):
        result = ""
        for i in xrange(l):
            result = result + str(randint(0,1))
    return result
