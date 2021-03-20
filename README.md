# GGH13-matrix obfuscation

Repository contains implementation of cryptographic program obfuscation using GGH13-matrix scheme.

-----------------------------------------------------------------------------------------

To test execution of encrypted basic group programs with decryption run command:

`./main.py --test -p 5 -q 7`

To test execution of group program in S5 for specified circuit run command:

`./main.py --file circuits/gp1.circ`

Arguments used in commands:
- p - prime number defining quotient ring (x^p-x-1) (default p=761)
- q - prime number defining finite field (default q=4591)

For help run:

`./main.py -h`

-----------------------------------------------------------------------------------------
