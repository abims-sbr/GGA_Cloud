#!/usr/bin/env bash

INFILE=$1
OUTFILE=tmpfile

FILE_HEADER_START=$(grep ">" $INFILE | cut -c 1-6 | sort | uniq)
HEADER_START_STRING=">mRNA."

if [[ "$FILE_HEADER_START" == "$HEADER_START_STRING" ]]
then
    /usr/local/genome2/mmo/scripts/common/common-stringSubstitute.py -i $INFILE -o $OUTFILE -p '^>mRNA' -r '>protein'
    mv $OUTFILE $INFILE
    echo "'>mRNA' replaced by '>protein'"
else 
    echo "Abort. Not all headers start with '>mRNA.':"
    echo "$FILE_HEADER_START"
fi