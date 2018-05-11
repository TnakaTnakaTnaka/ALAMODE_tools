#!/usr/bin/env python
#
# extract_pattern.py
#
#
# Copyright (c) 2018 Yuto Tanaka
#

"""
--- How to use ---

$ python extract_pattern.py --file1=file1.pattern --file2=file2.pattern

If you calcule atomic forces in displacement patterns which the cutoff
radius is in the range of r1(file1) and r2(file2), this script can
generate the pattern file (extract.pattern) for such calculation.
"""

import argparse

usage = "usage: %prog [options]"
parser = argparse.ArgumentParser(usage=usage)
parser.add_argument('--file1', help="alamode pattern file (*.pattern*)")
parser.add_argument('--file2', help="alamode pattern file (*.pattern*)")

def extract_pair(file_in):

    f_in = open(file_in, 'r')
    line = f_in.readline().split()
    pair_list = []
    patterns = {}
    count = 0

    for line in f_in:
        data = line.strip().split()
        column = len(data)
        if column == 2:
            natom = int(data[1])
            count = 0
            pair = []
            pattern = []

        else:
            pair.append(int(data[0]))
            pattern.append([int(data[1]), int(data[2]), int(data[3])])
            count += 1

        if count == natom:
            if pair not in pair_list:
                pair_list.append(pair)
                patterns[str(pair)] = [pattern]

            else:
                patterns[str(pair)].append(pattern)

    return pair_list, patterns


def generate_patterns(pair1, pair2, pattern1, pattern2):
    patterns = {}
    pairs = [pair for pair in pair2 if pair not in pair1]
    for pair in pairs:
        patterns[str(pair)] = pattern2[str(pair)]

    for pair in pair1:
        key = str(pair)
        num_pat1 = len(pattern1[key])
        num_pat2 = len(pattern2[key])
        if num_pat1 != num_pat2:
            pairs.append(pair)
            patterns[key] = pattern2[key]
            rm_pat = [p for p in pattern1[key] if p in patterns[key]]
            for p in rm_pat:
                patterns[key].remove(p)


    return pairs, patterns


def compare_pattern(file1_in, file2_in):
    pair1, pattern1 = extract_pair(file1_in)
    pair2, pattern2 = extract_pair(file2_in)
    num_pair1 = len(pair1)
    num_pair2 = len(pair2)

    if num_pair1 < num_pair2:
        pairs, patterns = generate_patterns(pair1, pair2, pattern1, pattern2)

    elif num_pair1 > num_pair2:
        pairs, patterns = generate_patterns(pair2, pair1, pattern2, pattern1)

    else:
        pairs = []

    return pairs, patterns


def generate_extractfile(pairs, patterns):

    f_out = open('extract.pattern', 'w')
    f_out.write("Basis : C\n")

    num_pattern = 0
    for pair in pairs:
        nat = len(pair)
        key = str(pair)
        for pattern in patterns[key]:
            num_pattern += 1
            atom = 0
            f_out.write("   %d:     %d\n" %(num_pattern, nat))
            for p in pattern:
                atom += 1
                f_out.write("   %3d         %2d      %2d     %2d\n" %(atom, p[0], p[1], p[2]))

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

    pairs, patterns = compare_pattern(file1_in, file2_in)

    if pairs == []:
        print("can not extract any patterns.")
    else:
        generate_extractfile(pairs, patterns)
        print("some patterns were extracted.")
        print("extract.pattern was generated.")

if __name__ == "__main__":
    main()
