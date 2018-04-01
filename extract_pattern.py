#!/usr/bin/env python
#
# extract_pattern.py
#
# If you calcule atomic forces in displacement patterns which the cutoff
# radius is in the range of r1(file1) and r2(file2), this script can
# generate the pattern file (extract.pattern) for such calculation.
#
# Copyright (c) 2018 Yuto Tanaka
#

"""
--- How to use ---

$ python extract_pattern.py --file1=file1.pattern --file2=file2.pattern


"""

import argparse

usage = "usage: %prog [options]"
parser = argparse.ArgumentParser(usage=usage)
parser.add_argument('--file1', help="alamode pattern file (*.pattern*)")
parser.add_argument('--file2', help="alamode pattern file (*.pattern*)")

def extract_pair(file_in):

    f_in = open(file_in, 'r')
    line = f_in.readline().split()
    pair = []
    pair_list = []
    count = 0

    for line in f_in:
        data = line.strip().split()
        column = len(data)
        if column == 2:
            natom = int(data[1])
            count = 0
            pair = []

        else:
            pair.append(int(data[0]))
            count += 1

        if count == natom:
            if pair not in pair_list:
                pair_list.append(pair)

    return pair_list


def compare_pattern(file1_in, file2_in):
    pair1 = extract_pair(file1_in)
    pair2 = extract_pair(file2_in)
    num_pair1 = len(pair1)
    num_pair2 = len(pair2)
    pattern_file = file2_in   # assume that number of pattern in file2 is more than that in file1.

    if num_pair1 < num_pair2:
        pairs = [pair for pair in pair2 if pair not in pair1]

    elif num_pair1 > num_pair2:
        pairs = [pair for pair in pair1 if pair not in pair2]
        pattern_file = file1_in

    else:
        pairs = []

    return pairs, pattern_file


def create_newfile(pairs, file_in):

    f_in = open(file_in, 'r')
    f_out = open('extract.pattern', 'w')
    basis = f_in.readline().split()
    f_out.write("  ".join(map(str, basis)) + "\n")

    num_pattern = 0

    for line in f_in:
        data = line.strip().split()
        column = len(data)
        if column == 2:
            natom = int(data[1])
            count = 0
            pair = []
            pattern_data = []

        else:
            pair.append(int(data[0]))
            pattern_data.append(data)
            count += 1

        if count == natom and pair in pairs:
            num_pattern += 1
            f_out.write("   %3d: %d\n" % (num_pattern, natom))
            for i in range(natom):
                f_out.write("     %3d    %2d    %2d    %2d\n" \
                        %(int(pattern_data[i][0]), int(pattern_data[i][1]),\
                          int(pattern_data[i][2]), int(pattern_data[i][3])))

    f_out.close()


def main():

    options = parser.parse_args()

    if options.file1:
        file1_in = options.file1
    else:
        print("Input file1 is not selected.")

    if options.file2:
        file2_in = options.file2
    else:
        print("Input file2 is not selected.")

    pairs, pattern_file = compare_pattern(file1_in, file2_in)

    if pairs == []:
        print("can not extract any patterns.")
    else:
        create_newfile(pairs, pattern_file)
        print("some patterns were extracted.")
        print("extract.pattern was generated.")

if __name__ == "__main__":
    main()
