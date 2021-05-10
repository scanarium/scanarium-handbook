#!/usr/bin/env python3

import argparse
import os
import shutil
import sys


DOCUMENT_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))
IMAGE_DIR = os.path.join(DOCUMENT_ROOT, 'images')


def copy_image(source, target_name=None):
    if target_name is None:
        target_name = os.path.basename(source)
    target = os.path.join(IMAGE_DIR, target_name)
    shutil.copy2(source, target)


def process_scanarium_support_dir(dir):
    name = os.path.join(
        dir, 'avatar',
        'avatar-ohne-hintergrund-ohne-schwarzem-rand-mit-schatten.png')
    copy_image(name, 'logo-big.png')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Updates static content sourced from other repos',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--scanarium-support-dir', default=None,
        help='The directory where `scanarium-support` can be found')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    exit_code = 0

    scanarium_support_dir = args.scanarium_support_dir
    if args.scanarium_support_dir:
        process_scanarium_support_dir(args.scanarium_support_dir)
        print('scanarium-support done.')
    else:
        exit_code = 1
        print('No scanarium-support dir given. Skipping corresponding updates')

    sys.exit(exit_code)