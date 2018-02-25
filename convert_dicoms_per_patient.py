# coding:utf8
#/usr/bin/env python3
"""
copyright Asan AGIBETOV <asan.agibetov@gmail.com>

We assume that the path in which we start contains subdirectories that
correspond to patients. For each subdirectory, we collect all dicoms, and
export all of them as jpg images. Therefore, the extracted images will have at
most one level of depth, corresponding to the hierarchical structure divided
into patients.

"""
# Standard-library imports
import os
import itertools as it
import random
import math


# Third-party imports
import click
import numpy as np
import skimage 
import skimage.io as img_io
import dicom
from tqdm import tqdm

# Cross-library imports
import convert_dicoms as cdcm


def collect_subdirs(path_to_walk):
    """Collect 1-level subdirectories, which should delimit patients or any
    other collection of dicoms (the latter could still have a hierarchical
    structure"""
    root, subdirs, _ = next(os.walk(path_to_walk))

    return [os.path.join(root, d) for d in subdirs]


def convert_subdir(subdir, dest):
    """Convert all dicoms (at any depth) collected in this subdirectory, and
    save them as images in the dest file"""
    dicoms = cdcm.collect_dicoms(subdir)
    base_name = os.path.basename(subdir)
    dest = os.path.join(dest, base_name)

    # create sub folder in the dest if does not exist
    if not os.path.exists(dest):
        os.makedirs(dest)

    cdcm.convert_dicoms(dicoms, dest, base_name)


def convert_subdirs(path_to_walk, dest):
    """Convert all subdirs by maintaining the same hierarchical structure"""
    subdirs = collect_subdirs(path_to_walk)
    for subdir in subdirs:
        convert_subdir(subdir, dest)



@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--dest", default="./converted-images")
def main(path, dest):
    convert_subdirs(path, dest) 


if __name__ == "__main__":
    main()
