#!/usr/bin/env sage

import argparse, os, sys, time
from obf import *
from tests import *
from parseinput import *
from preparecirc import *

def is_circ(fname):
    ext = os.path.splitext(fname)[1]
    if ext in ('.circ'):
        return True
    else:
        print("%s unknown extension '%s'" % ("Error:", ext))
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Program obfuscation using Braid Groups.')
    parser.add_argument("-p", type=int, help="specify the dimension of a generating polynomial", default=761)
    parser.add_argument("-q", type=int, help="specify the size of a finite field", default=4591)
    parser.add_argument("--test", help="evaluating encrypted basic group programs with decryption", action="store_true")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument('--file', metavar='FILE', type=str, help='test circuit or branching program from FILE',  action='store')
    args = parser.parse_args()
    if args.test:
         encGPand(args.verbose, args.p, args.q)
         encGPor(args.verbose, args.p, args.q)
    if args.file:
        if is_circ(args.file):
            test_file(args.file, args)

if __name__ == "__main__":
    main()
