#! /usr/bin/env python3
# coding:utf8
"""
copyright Asan Agibetov <asan.agibetov@gmail.com>

display given image

"""
import click
import dicom
from matplotlib import pyplot as plt

@click.command()
@click.argument("path_to_dicom")
def main(path_to_dicom):
    dcm = dicom.read_file(path_to_dicom)
    plt.set_cmap(plt.get_cmap("gray"))
    # plt.pcolormesh(dcm.pixel_array, vmin=-1., vmax=1.)
    plt.imshow(dcm.pixel_array)
    plt.show()


if __name__ == "__main__":
    main()
