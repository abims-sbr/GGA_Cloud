#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import re
import sys

# Return the file obtained by replacing the occurrences of pattern by the replacement string.
# Use of python method re.sub()
# python common-stringSubsitute.py -f file -p pattern -r replacement_string
# ex : python common-stringSubsitute.py -f file -p '(tRNA)(\w{3})(\w{3})' -r '\g<1>-\g<2>(\g<3>)'

if __name__ == '__main__':

    #Get arguments
    parser = argparse.ArgumentParser(description="Return the file obtained by replacing the occurrences of pattern by the replacement string. Use of python method re.sub(). Example: python common-stringSubsitute.py -f file -p '(tRNA)(\w{3})(\w{3})' -r '\g<1>-\g<2>(\g<3>)'")
    parser.add_argument('-i','--infile', help='Input file', required=True)
    parser.add_argument('-o','--outfile', help='Output file', default='outfile')
    parser.add_argument('-p','--pattern', help='Pattern string to be replaced', required=True)
    parser.add_argument('-r','--repl', help='Replacement string', required=True)
    args = parser.parse_args()

    infilename=args.infile
    outfilename=args.outfile
    pattern=args.pattern
    repl=args.repl

    infile=open(infilename,'r')
    outfile=open(outfilename,'w')

    lines=infile.readlines()

    for line in lines :
        line_out=re.sub(pattern,repl,line)
        outfile.write(line_out)

    outfile.close()