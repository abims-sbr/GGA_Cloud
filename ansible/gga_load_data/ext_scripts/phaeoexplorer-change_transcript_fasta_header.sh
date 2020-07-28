#!/usr/bin/env bash
INFILE=$1
OUTFILE=tmpfile
./common-stringSubsitute.py -i $INFILE -o $OUTFILE -p '^>\d+ mRNA' -r '>mRNA' || mv $OUTFILE $INFILE || echo "'>[0-9]+ mRNA' replaced by '>mRNA' in $1"