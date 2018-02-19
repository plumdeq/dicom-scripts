#/usr/bin/env python3
# coding:utf8
"""
copyright Asan AGIBETOV <asan.agibetov@gmail.com>

Split imagefolder 

* folder1


into 

* train
    * folder1
* test
    * folder1

"""
# Standard-library imports
import os
import random
import math

# Third-party imports
import click


def collect_files(path):
    """Collects all files in the directory (1 level of depth)"""
    root, _, files = next(os.walk(path))

    return os.path.basename(path), [os.path.join(root, f) for f in files]


def move_files(folder, files, indices, dest, dataset_type):
    """Given indices move all files to the given destination for the given
    dataset type"""
    path = os.path.join(dest, dataset_type)
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(dest, dataset_type, folder)
    if not os.path.exists(path):
        os.mkdir(path)
    for i in indices:
        f = files[i]
        fname = os.path.basename(f)
        os.rename(f, os.path.join(path, fname))


def split_train_test(folder, files, dest, tr_ratio=0.8):
    idx = list(range(len(files)))
    random.shuffle(idx)
    n_total = len(files)
    n_tr = math.ceil(n_total*tr_ratio)

    tr_idx = idx[:n_tr]
    te_idx = idx[n_tr:]

    print("moving {} files into train folder".format(len(tr_idx)))
    move_files(folder, files, tr_idx, dest, "train")
    print("moving {} files into test folder".format(len(te_idx)))
    move_files(folder, files, te_idx, dest, "test")


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.argument("dest", type=click.Path(exists=True))
@click.option("--tr_ratio", default=0.8)
def main(path, dest, tr_ratio):
    folder, files = collect_files(path)
    split_train_test(folder, files, dest, tr_ratio)


if __name__ == "__main__":
    main()
