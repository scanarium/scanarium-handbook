#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import sys


DOCUMENT_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))
IMAGE_DIR = os.path.join(DOCUMENT_ROOT, 'images')
PYTHON_SOURCE_DIR = os.path.join(DOCUMENT_ROOT, 'functions')
CONFIG_FILE = os.path.join(DOCUMENT_ROOT, 'config.json')
CONVERT = '/usr/bin/convert'
WIDTH_SMALL = 200

with open(CONFIG_FILE) as f:
    CONFIG = json.loads(f.read())

LANGUAGES = [CONFIG['default_l10n']] + CONFIG['additional_l10ns']


def run_command(command):
    subprocess.run(command, check=True, timeout=10)


def generate_resized_image(source, target, width):
    command = [
        CONVERT,
        source,
        '-resize', f'{width}x{int(width*1.33333)}',
        '-background', 'white',
        '-flatten',
        target,
        ]
    return run_command(command)


def generate_small_image(source, target):
    return generate_resized_image(source, target, WIDTH_SMALL)


def copy_file(source, target_dir=DOCUMENT_ROOT, target_name=None):
    if target_name is None:
        target_name = os.path.basename(source)
    target = os.path.join(target_dir, target_name)
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy2(source, target)
    return (target, target_dir, target_name)


def copy_image(source, target_dir=IMAGE_DIR, target_name=None,
               small=False):
    (_, _, target_name) = copy_file(
        source, target_dir=target_dir, target_name=target_name)

    if small:
        resized_name = target_name.rsplit('.', 1)[0] + '-small.jpg'
        generate_small_image(source,
                             os.path.join(target_dir, resized_name))


def process_scanarium_dir(dir):
    scenes_dir = os.path.join(dir, 'scenes')
    for scene in os.listdir(scenes_dir):
        scene_dir = os.path.join(scenes_dir, scene)
        if os.path.isdir(scene_dir):
            scene_file = os.path.join(scene_dir, 'scene-bait.png')
            target_dir = os.path.join(IMAGE_DIR, 'scenes', scene)
            copy_image(scene_file, target_dir=target_dir, small=True)

    groups = []
    for (name, group) in [
        ('LocalizerFactory.py', 'translate'),
        ('Localizer.py', 'translate'),
        ('MessageFormatter.py', 'translate'),
            ]:
        copy_file(os.path.join(dir, 'scanarium', name),
                  target_dir=os.path.join(PYTHON_SOURCE_DIR, group))
        if group not in groups:
            init_file = os.path.join(PYTHON_SOURCE_DIR, group, '__init__.py')
            open(init_file, 'w').close()
            groups.append(group)

    for language in LANGUAGES:
        copy_file(os.path.join(dir, 'localization', f'{language}.json'),
                  target_dir=os.path.join(PYTHON_SOURCE_DIR, 'translate',
                                          'localizations'))


def process_scanarium_support_dir(dir):
    name = os.path.join(
        dir, 'avatar',
        'avatar-ohne-hintergrund-ohne-schwarzem-rand-mit-schatten.png')
    copy_image(name, target_name='logo-big.png')

    dir_handbook = os.path.join(dir, 'handbook', 'images')
    for file in os.listdir(dir_handbook):
        copy_image(os.path.join(dir_handbook, file), small=True)


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
