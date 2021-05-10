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


def process_scanarium_dir(dir):
    pass

def process_scanarium_support_dir(dir):
    name = os.path.join(
        dir, 'avatar',
        'avatar-ohne-hintergrund-ohne-schwarzem-rand-mit-schatten.png')
    copy_image(name, 'logo-big.png')


def process_scanarium_homepage_dir(dir):
    for image in [
        'facebook',
        'instagram',
        'scanarium',
        'twitter',
        'youtube',
            ]:
        copy_image(os.path.join(dir, f'dynamisch/images/{image}.png'))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Updates static content sourced from other repos',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--scanarium-dir', default=None,
        help='The directory where the `scanarium` repo can be found')
    parser.add_argument(
        '--scanarium-homepage-dir', default=None,
        help='The directory where the `Homepages/scanarium.com` repo can '
        'be found')
    parser.add_argument(
        '--scanarium-support-dir', default=None,
        help='The directory where the `scanarium-support` repo can be found')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    exit_code = 0

    for repo_conf in [
        {'name': 'scanarium',
         'directory': args.scanarium_dir,
         'processor': process_scanarium_dir},
        {'name': 'scanarium-support',
         'directory': args.scanarium_support_dir,
         'processor': process_scanarium_support_dir},
        {'name': 'scanarium-homepage',
         'directory': args.scanarium_homepage_dir,
         'processor': process_scanarium_homepage_dir},
            ]:
        dir = repo_conf['directory']
        if dir:
            repo_conf['processor'](dir)
            print(f'`{repo_conf["name"]}` repo done.')
        else:
            exit_code = 1
            print(f'No {repo_conf["name"]} dir given. Skipping corresponding '
                  'updates')

    sys.exit(exit_code)
