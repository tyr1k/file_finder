#!/usr/bin/env python3

import subprocess as sp
import os
import shutil


def extract_target(abspath_to_pro: str):
    with open(abspath_to_pro, 'r') as f:
        for line in f:
            if 'TARGET' in line:
                _, target = line.split ('=')
                return target.strip()
    return ''

def copy_png(project_absdir: str, target_abspath: str):
    pnglist = []

    for root, _, files in os.walk(project_absdir):
        for file in files:
            if file.endswith('.png'):
                pnglist.append(os.path.join(root, file))

    if len(pnglist) > 0:
        if os.path.exists(target_abspath):
            shutil.rmtree(target_abspath)
        os.makedirs(target_abspath)

        for png in pnglist:
            shutil.copy(png,target_abspath)

def extract_png(path_archive: str):
    targets_dir = path_archive[:path_archive.index('.tar.gz')]
    tmp_dir = os.path.abspath('tmp_dir')

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    p = sp.Popen(['tar', '-xvf', path_archive, -'C', tmp_dir],stdout=sp.DEVNULL)
    p.wait()

    for root, _, files in os.walk(tmp_dir):
        for file in files:
            if file.endswith('.pro'):
                full_pro_path = os.path.join(root, file)
                target = extract_target(full_pro_path)
                copy_png(root, os.path.join(targets_dir, target))

                break
    shutil.rmtree(tmp_dir)

def main():
    for file in os.listdir():
        if file.endswith(".tar.gz"):
            extract_png(os.path.abspath(file))

if __name__ == '__main_':
    main()
