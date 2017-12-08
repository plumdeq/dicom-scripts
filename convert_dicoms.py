#! /usr/bin/env python3
# coding:utf8
"""
copyright Asan Agibetov <asan.agibetov@gmail.com>

Converts all dicom files to images and saves to disk. Dicom files are assumed
to have only one image

"""
# Standard-library imports
import os


# Third-party imports
import click
import numpy as np
import skimage 
import skimage.io as img_io
import dicom


def walk_dirs(path_to_walk, dest):
    """
    Convert all DICOM sequences found in `path_to_walk` to images, and store
    them in the `dest` directory
    
    """
    for dir_name, subdir_list, file_list in os.walk(path_to_walk):
        dicoms = [filename
                  for filename in file_list 
                  if ".dcm" in filename.lower()]

        [convert_dicom(dir_name, dcm, dest) for dcm in dicoms]
        
        # recursively call in all subdirectories
        [walk_dirs(subdir, dest) for subdir in subdir_list]

    return None


def convert_dicom(dir_name, dcm_file, dest):
    """Convert dicom file at `dcm_file` to an image (jpg with the same name) in
    the `dest` folder"""
    name = dcm_file.replace(".dcm", ".jpg")
    name = os.path.join(dest, name)

    dcm_file = os.path.join(dir_name, dcm_file)
    dcm = dicom.read_file(dcm_file)
    I = dcm.pixel_array
    I8 = ((I - I.min())/(I.max() - I.min()) * 255).astype(np.uint8)

    click.echo("saving in grayscale to {}".format(name))
    img_io.imsave(name, I8)

    return name


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True))
@click.option("--dest", default="./converted-images")
def main(paths, dest):
    for path in paths:
        walk_dirs(path, os.path.abspath(dest))


if __name__ == "__main__":
    main()
