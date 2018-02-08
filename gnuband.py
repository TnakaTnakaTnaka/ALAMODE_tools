#!/usr/bin/env python
#
# gnuband.py
#
# Script to generate band data for gnuplot and gnuplot script file.
#
# Copyright (c) 2018 Yuto Tanaka
#

""" 
--- How to use ---
$ python bandgnu.py --file=file.dat (--unit=meV)

default unit is cm^(-1).
"""

import numpy as np
import optparse

usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage=usage)
parser.add_option('--file', help="OpenMX input file (*.dat)")
parser.add_option("-u", "--unit", action="store", type="string", dest="unitname", default="kayser", help="print the band dispersion in units of UNIT. Available options are kayser, meV, and THz", metavar="UNIT")


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

    band = []
    for line in f_in:
        data = line.strip().split()
        band.append(data)
         
    num_eigen = len(band[0])
    num_kgrid = len(band)

    for i in range(1, num_eigen):
        for j in range(num_kgrid):
            f_band.write("%f %f \n" % (float(band[j][0]), float(band[j][i])))
        f_band.write("\n")

    f_band.close()

    generate_gnuband(prefix, file_band, k_path, k_point, ylabel, factor)


def main():
    options, args = parser.parse_args()
    
    if options.file:
        file_in = options.file
    else:
        print("input file is not selected.")
   
    prefix = file_in.split('.')[0]

    if options.unitname.lower() == "mev":
        ylabel = "Frequency (meV)"
        factor = 0.0299792458 * 1.0e+12 * 6.62606896e-34 / 1.602176565e-19 * 1000
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
