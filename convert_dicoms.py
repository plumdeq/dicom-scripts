#! /usr/bin/env python3
# coding:utf8
"""
copyright Asan Agibetov <asan.agibetov@gmail.com>

Converts all dicom files to images and saves to disk. Dicom files are assumed
to have only one image

"""
# Standard-library imports
import os
import itertools as it
import random
import math
import glob
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Third-party imports
import click
import numpy as np
import skimage 
import skimage.io as img_io
import dicom
from tqdm import tqdm


def collect_dicoms(path_to_walk, dcm_regexp):
    """Collects all dicom files in the given path"""
    # all_files = [os.path.join(dir_name, f) 
    #              for dir_name, _ , files in os.walk(path_to_walk)
    #              for f in files]
    #              # if ".dcm" in f.lower()]

    logger.info("globbing {} with {}".format(path_to_walk, dcm_regexp))
    all_files = list(glob.glob(path_to_walk + dcm_regexp, recursive=True))

    return all_files


def convert_dicoms(dicoms, dest, export_name):
    """
    Convert all DICOM sequences to images, and store
    them in the `dest` directory
    
    """
    n_total = len(dicoms)
    n_problems = 0

    if n_total == 0:
        logger.info("No dicoms to convert")
        return None

    for i, f in enumerate(tqdm(dicoms, desc="exporting image from DICOM")):
        try:
            convert_dicom(f, dest, export_name, i, n_total)
        except Exception as e:
           click.echo(e)
           n_problems += 1

    click.echo("converted {0}/{1} (uncoverted {2:0.2f}%) files".format(
        n_total-n_problems, n_total, n_problems/n_total))

    return None

    # for dir_name, subdir_list, file_list in os.walk(path_to_walk):
    #     dicoms = [filename
    #               for filename in file_list 
    #               if ".dcm" in filename.lower()]

    #     [convert_dicom(dir_name, dcm, dest) for dcm in dicoms]
    #     
    #     # recursively call in all subdirectories
    #     [walk_dirs(subdir, dest) for subdir in subdir_list]

    # return None


def convert_dicom(dcm_file, dest, export_name, counter, n_total):
    """Convert dicom file at `dcm_file` to an image (jpg with the same name) in
    the `dest` folder"""
    # name = dcm_file.replace(".dcm", ".jpg")
    # give it a name with counter, e.g., exported-00001.jpg
    name = '-'.join([export_name, str(counter).zfill(len(str(n_total)))])
    name = '.'.join([name, 'jpg'])
    name = os.path.join(dest, name)

    # dcm_file = os.path.join(dir_name, dcm_file)
    dcm = dicom.read_file(dcm_file)

    I = dcm.pixel_array

    if is_2d_array(I):
        I8 = ((I - I.min())/(I.max() - I.min()) * 255).astype(np.uint8)
        # click.echo("saving in grayscale to {}".format(name))
        img_io.imsave(name, I8)
    else:
        raise Exception("WARNING: {} is not 2D image".format(name))

    return name


def is_2d_array(array):
    """Check if the given array is a 2d"""
    return len(array.shape) == 2


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True))
@click.option("--export-name", default="exported", help="default name of exported images + id (usually simple count)")
@click.option("--dest", default="./converted-images")
def main(paths, export_name, dest):
    dicoms = list(it.chain(*[collect_dicoms(path) for path in paths]))
    convert_dicoms(dicoms, os.path.abspath(dest), export_name)

if __name__ == "__main__":
    main()
