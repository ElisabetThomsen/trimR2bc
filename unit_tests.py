#!/usr/bin/env python3

"""
Author: Elisabet Thomsen
Date: 05-05-2020
Description:
Unit tests for testing trimR2bc.py
Tests:
    - There are equal amount of lines in R2 file before and after trim.
    - The trimmed reads are of equal or shorter length than the untrimmed reads.
    - The quality line is the same length as the read line.
    - The trimmed file is keeping the rules of fastq format.

Usage: ./unit_tests.py <rawR2file> <trimmedR2file>
"""

import sys, gzip

# Function: Open file giziped or not
def open_file(filename):
    try:
        if filename.lower().endswith('.gz'):
            return gzip.open(filename,"rb")
        else:
            return open(filename,"rb")
    except IOError as err:
        print("Cant open file:", str(err));
        print('Usage: ./unit_tests.py <rawR2file> <trimmedR2file>');
        sys.exit(1)


# Test: Equal amount of lines before and after trim
def equal_lines(rawfile, trimfile):

    rawcount = 0
    for line in rawfile:
        rawcount += 1

    trimcount = 0
    for line in trimfile:
        trimcount += 1

    assert rawcount == trimcount, "Files have unequal length!"

# Test: Trimmed reads are not shorter
def trimmed_read_length(rawfile, trimfile):

    linecount = 0
    for rawline, trimline in zip(rawfile, trimfile):
        if linecount == 2:
            assert len(rawline) >= len(trimline), "Trimmed read is longer than untrimmed read!"
        if linecount == 4:
            linecount = 0

# Test: Trimmed quality score line is same length as trimmed read
def trimmed_QSline_length(trimfile):

    linecount = 0
    for line in trimfile:
        if linecount == 2:
            readlen = len(line)
        if linecount == 4:
            assert len(line) == readlen, "Read line and QS line have unequal length in trimmed file!"
            linecount = 0

# Main program
if __name__ == '__main__':

    # Check commandline
    if len(sys.argv) != 3:
        print('Usage: ./unit_tests.py <rawR2file> <trimmedR2file>');
        sys.exit(1)

    # Get filenames from commandline
    rawfilename = sys.argv[1]
    trimfilename = sys.argv[2]

    # Open files
    rawfile = open_file(rawfilename)
    trimfile = open_file(trimfilename)

    # Check if equal amont of lines
    equal_lines(rawfile, trimfile)

    # Check that trimmed read is not longer than untrimmed read
    trimmed_read_length(rawfile, trimfile)

    # Check that trimmed quality score line is same length as trimmed read line
    trimmed_QSline_length(trimfile)
