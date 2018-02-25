#! /usr/bin/env python3
# coding:utf8
"""
copyright Asan Agibetov <asan.agibetov@gmail.com>

Convert dicom files in the given folders to tensors, each subfolder will
correspond to one tensor

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


def convert_dicoms_to_tensor(dicoms, channels=1):
    """Convert all the given dicoms to one tensor, if channels==3, then
    duplicate the image (grayscale) 3 times"""
    tensors = [convert_dicom_to_tensor(dicom) for dicom in dicoms]
    # we might have had empty tensors
    tensors = [tensor for tensor in tensors if tensor is not None]

    T = np.zeros([len(tensors)] + list(tensors[0].shape))
    for i, tensor in enumerate(tensors):
        T[i] = tensor
    
    return T


def convert_dicom_to_tensor(dcm_file, channels=1):
    """Convert one dicom to a tensor (if channels=3 duplicate three times)"""
    dcm = dicom.read_file(dcm_file)

    try:
        I = dcm.pixel_array

        if cdcm.is_2d_array(I):
            I8 = ((I - I.min())/(I.max() - I.min()) * 255).astype(np.uint8)

            if channels == 1:
                # return np.expand_dims(I8, 0)
                return I8
            else:
                return np.broadcast_to(I8, [channels] + list(I8.shape))
        else:
            print("not a 2D image. Cannot convert")
            return None
    except Exception as e:
        print(e)
        return None
