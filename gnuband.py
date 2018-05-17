#!/usr/bin/env python
#
# gnuband.py
#
# Script to generate band data file and gnuplot script file for gnuplot  .
#
# Copyright (c) 2018 Yuto Tanaka
#

"""
--- How to use ---
$ python bandgnu.py --file=file.bands (--unit=meV)

default unit is cm^(-1).
"""

import argparse

usage = "usage: %prog [options]"
parser = argparse.ArgumentParser(usage=usage)
parser.add_argument('--file', help="bands file")
parser.add_argument("-u", "--unit", action="store", type=str, \
        dest="unitname", default="kayser", help="print the band dispersion \
        in units of UNIT. Available options are kayser, meV, and THz", \
        metavar="Unit")

def generate_gnuband(prefix, file_band, k_path, k_point, ylabel, factor):

    num_path = len(k_path)
    xtics = ""
    for i in range(1, num_path):
        if k_path[i] == 'G':
            k_path[i] = "{/Symbol G}"
        xtics += " '" + k_path[i] + "' " + k_point[i]
        if i < num_path - 1:
            xtics += ','

    file_gnu = prefix + ".gnuband"
    f_gnu = open(file_gnu, 'w')

    f_gnu.write("# gnuplot\n")
    f_gnu.write("unset key\n")
    f_gnu.write("set ylabel '%s'\n" %(ylabel))
    f_gnu.write("set yrange [0:]\n")
    f_gnu.write("set xtics (%s)\n" % (xtics))
    f_gnu.write("set grid xtics\n")
    f_gnu.write("\n")
    f_gnu.write("factor = %f\n" % (factor))
    f_gnu.write("plot '%s' u 1:($2 * factor) w l\n" %(file_band))
    f_gnu.write("\n")
    f_gnu.write("pause -1\n")

    f_gnu.close()


def generate_banddata(prefix, file_in, ylabel, factor):

    f_in = open(file_in, 'r')
    file_band = prefix + ".banddata"
    f_band = open(file_band, 'w')

    k_path = f_in.readline().split()
    k_point = f_in.readline().split()
    unit = f_in.readline().split()
    k_max = float(k_point[-1])
    k_grid = []

    # read bands data
    band = []
    for line in f_in:
        data = line.strip().split()
        band.append(data)

    num_eigen = len(band[0]) # number of eigen value
    num_kgrid = len(band)    # number of k grid

    # normalize k point
    for i in range(1, len(k_point)):
        k_point[i] = str(float(k_point[i]) / k_max)

    for i in range(num_kgrid):
        k_grid.append(float(band[i][0]) / k_max)

    # output
    for i in range(1, num_eigen):
        for j in range(num_kgrid):
            f_band.write("%f %f \n" % (k_grid[j], float(band[j][i])))
        f_band.write("\n")

    f_band.close()

    generate_gnuband(prefix, file_band, k_path, k_point, ylabel, factor)


def main():
    options = parser.parse_args()

    if options.file:
        file_in = options.file
    else:
        print("input file is not selected.")

    prefix = file_in.split('.')[0]

    if options.unitname.lower() == "mev":
        ylabel = "Frequency (meV)"
        factor = 0.0299792458 * 1.0e+12 * 6.62606896e-34 \
                    / 1.602176565e-19 * 1000
    elif options.unitname.lower() == "thz":
        ylabel = "Frequency (THz)"
        factor = 0.0299792458
    else:
        ylabel = "Frequency (cm^{-1})"
        factor = 1.0

    generate_banddata(prefix, file_in, ylabel, factor)

    print("%s.gnuband and %s.banddata are generated." %(prefix, prefix))

if __name__ == "__main__":
    main()
