#!/usr/bin/env python3

"""
Author: Elisabet Thomsen
Date: 05-05-2020
Description:
Unit tests for testing trimR2bc.py
Tests:
    - There are equal amount of lines in R2 file before and after trim.
    - The trimmed reads are of equal or shorter length than the untrimmed reads.
    - The trimmed file is keeping the rules of fastq format:
        * Line 1 has to start with '@'
        * Line 2 has the sequence letters which can be: AGCTYRWSKMDVHBXN-
        * Line 3 has to start with '+'
        * The quality line (line 4) is the same length as the read line (line 2).

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
        elif linecount == 4:
            linecount = 0

# Test: Trimmed file is not violating fastq-format
def fastq_format(trimfile):
    linecount = 0
    for line in trimfile:
        if linecount == 1:
            assert line[0] == b'@', "Fastq-format violated: Line 1 has to start with '@'"
        elif linecount == 2:
            readlen = len(line)
            assert line[5] in 'AGCTYRWSKMDVHBXN-', "Fastq-format violation: Line 2 can only contain AGCTYRWSKMDVHBXN-"
        elif linecount == 3:
            assert line[0] == b'+', "Fastq-format violated: Line 3 has to start with '+'"
        elif linecount == 4:
            assert len(line) == readlen, "Fastq-format violated: Read line and QS line have unequal length in trimmed file!"
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
    rawfile.seek(0)
    trimfile.seek(0)
    trimmed_read_length(rawfile, trimfile)

    # Check that trimmed file is not violating fastq-format
    trimfile.seek(0)
    fastq_format(trimfile)

    # Close files
    rawfile.close()
    trimfile.close()
