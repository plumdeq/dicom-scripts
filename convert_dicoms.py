#! /usr/bin/env python3
# coding:utf8
"""
copyright Asan Agibetov <asan.agibetov@gmail.com>

Converts all dicom files to images and saves to disk. Dicom files are assumed
to have only one image

"""
import click
import numpy as np
import skimage 
import skimage.io as img_io
import dicom


@click.command()
@click.argument("path_to_dicom_folder", type=click.Path(exists=True))
@click.option("--output", default="./dicom-image.jpg")
def main(path_to_dicom_folder, output):
    dcm = dicom.read_file(path_to_dicom_folder)
    I = dcm.pixel_array
    I8 = ((I - I.min())/(I.max() - I.min()) * 255).astype(np.uint8)

    click.echo("saving in grayscale")
    img_io.imsave(output, I8)


if __name__ == "__main__":
    main()
