#!/usr/bin/env python
# coding: utf-8

""" Run rawtran on all images in a directory. """

from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys
import glob
from argparse import ArgumentParser

def main(path, overwrite):
    if os.path.isabs(path):
        full_path = path
    else:
        full_path = os.path.expanduser(path)
    
    os.chdir(full_path)
    
    for filename in glob.glob("*.CR2"):
        for filter in ["Ri", "Gi", "Bi"]:
            base,ext = os.path.splitext(filename)
            fits_filename = "{0}_{1}{2}".format(base, filter, ".fits")
            
            if os.path.exists(fits_filename):
                if overwrite:
                    os.remove(fits_filename)
                else:
                    print("Skipping {0} because the file exists..."\
                            .format(fits_filename))
                    continue
            
            cmd = "rawtran -o {0} -c {1} -b 16 {2}"\
                    .format(fits_filename, filter, filename)
            ret_code = os.system(cmd)
            
            if ret_code != 0:
                raise IOError("Failed to create file {0}".format(fits_filename))
    
if __name__ == "__main__":
    parser = ArgumentParser("Run rawtran on all images in a directory.")
    parser.add_argument("-p", "--path", dest="path", required=True,
                        default=None, help="The directory to run in.")
    parser.add_argument("-o", "--overwrite", dest="overwrite", action="store_true",
                        default=None, help="overwrite files if they exist")
       
    args = parser.parse_args()
    
    main(args.path, args.overwrite)