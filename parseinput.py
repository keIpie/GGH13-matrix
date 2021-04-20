#!/usr/bin/env sage

""" parser from https://github.com/amaloz/obfuscation modified a bit """


from __future__ import print_function
from copy import deepcopy
import functools, sys
from sage.all import *
from gp import *

def clr_error(s):
    return '\x1b[31m%s\x1b[0m' % s
def clr_warn(s):
    return '\x1b[33m%s\x1b[0m' % s
def clr_ok(s):
    return '\x1b[32m%s\x1b[0m' % s

# __all__ = ['parse', 'ParseException']

class ParseException(Exception):
    pass

def test_file(path, args):
    testcases = {}
    print("-------------------------------------------------------------------")
    print("Testing %s" % path)
    print("-------------------------------------------------------------------")
    with open(path) as f:
        for line in f:
            if line.startswith('#'):
                if 'TEST' in line:
                    _, _, inp, outp = line.split()
                    testcases[inp] = int(outp)
            else:
                continue
    if len(testcases) == 0:
        print("no test cases")
        return True
    else:
        print("testcases: ", testcases)
        if(args.obf):
            success = testObf(path, testcases, args)
        else:
            success = testGP(path, testcases, args)
    if success:
        print(clr_ok('Pass'))
    else:
        print(clr_error('Fail'))
    return True

def testObf(path, testcases, args):
    # stworz program grupowy parsujac path
    gp = parse(path)
    # gp.printGP()
    # zaobfuskuj program grupowy
    egp = encrypt(gp,args.p,args.q,args.verbose)
    # egp.printGP()
    # przetestuj na testcases
    for t in testcases:
        tints = [int(i) for i in list(t)]
        print("testcase: ", t)
        print(checkID(decrypt(egp.evaluate(tints,args.verbose),egp.evaluate_dummy(tints,args.verbose),egp.get_pzt(),args.p,args.q)))
    return True

def testGP(path, testcases, args):
    # parse input file
    group = SymmetricGroup(5)
    gp = parse(path)
    for t in testcases:
        tints = [int(i) for i in list(t)]
        result = checkID(gp.evaluateShort(tints))
        print(result)
        if (result != testcases[t]):
            return False
    return True

def _parse_param(line):
    try:
        _, param, value = line.split()
    except ValueError:
        raise ParseException("Invalid line '%s'" % line)
    param = param.lower()
    if param in ('nins', 'depth'):
        try:
            value = int(value)
        except ValueError:
            raise ParseException("Invalid value '%s'" % value)
        return {param: value}
    else:
        raise ParseException("Invalid parameter '%s'" % param)

def parse(fname, f_inp_gate=False, f_gate=False):
    G = SymmetricGroup(5)
    alpha = G([2,3,4,5,1])
    beta  = G([3,1,5,2,4])
    info = {'nlayers': 0}
    output = False
    num = 0
    GPs = {}
    with open(fname) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            elif line.startswith(':'):
                info.update(_parse_param(line))
                continue
            print(line)
            num, rest = line.split(None, 1)
            try:
                num = int(num)
            except ValueError:
                raise ParseException(
                    'Line %d: gate index not a number' % lineno)
            #if rest.startswith('input'):
                # f_inp_gate(bp, num)
                #info['nlayers'] += 1
            #elif ...
            if rest.startswith('gate') or rest.startswith('output'):
                if rest.startswith('output'):
                    if output:
                        raise ParseException(
                            'Line %d: only one output gate supported' % lineno)
                    else:
                        output = True
                _, gate, rest = rest.split(None, 2)
                inputs = [int(i) for i in rest.split()]
                if len(inputs) == 2:
                    bp0I = inputs[0]
                    g1 = GroupProgram(G,alpha,1)
                    g2 = GroupProgram(G,beta,1)
                    if (bp0I <info['nins']):
                        g1 = GroupProgram(G,alpha,bp0I)
                    else:
                        g1 = GPs[bp0I]
                    bp1I = inputs[1]
                    if (bp1I <info['nins']):
                        g2 = GroupProgram(G,beta,bp1I)
                    else:
                        g2 = GPs[bp1I]
                    if gate=="AND":
                        print("gate AND")
                        gnew = GroupProgram()
                        gnew = deepcopy(g1)
                        gnew.andGP(g2,n)
                        # gnew.printGP()
                        GPs.update({num: gnew})
                    elif gate=="OR":
                        print("gate OR")
                        gnew = GroupProgram()
                        gnew = deepcopy(g1)
                        gnew.orGP(g2,n)
                        # gnew.printGP()
                        GPs.update({num : gnew})
                    elif gate=="XOR":
                        print("gate XOR")
                        gnew = GroupProgram()
                        gnew = deepcopy(g1)
                        gnew.xorGP(g2,n)
                        # gnew.printGP()
                        GPs.update({num : gnew})
                    else:
                        print("no such gate defined")
                elif (len(inputs) == 1 and gate=="NOT"):
                    print("gate NOT")
                    bp0I = inputs[0]
                    g1 = GroupProgram(G,alpha,1)
                    if (bp0I <info['nins']):
                        g1 = GroupProgram(G,alpha,bp0I)
                    else:
                        g1 = GPs[bp0I]
                    gnew = GroupProgram()
                    gnew = deepcopy(g1)
                    gnew.notGP(n)
                    # g1.printGP()
                    GPs.update({num: gnew})
                else:
                    print("something wrong...")
#                 try:
#                     f_gate(bp, num, lineno, gate.upper(), inputs)
#                 except KeyError:
#                     raise ParseException(
#                         'Line %d: unsupported gate %s' % (lineno, gate))
#                 except TypeError:
#                     raise ParseException(
#                         'Line %d: incorrect number of arguments given' % lineno)
            else:
                raise ParseException('Line %d: unknown gate type' % lineno)
    if not output:
        raise ParseException('no output gate found')
    print("info: ", info)
    # for i in xrange(4,4+len(GPs)):
    #     print("GP", i)
    #     GPs[i].printGP()
    return GPs[num]
    # return bp[-1], info
