#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''rename files of a dir to prefix-n.ext which n is 1,2,3...'''

import os
import sys

arg_num = len(sys.argv)

if arg_num < 2:
    print('Usage: {} <path> [filename_prefix]'.format(sys.argv[0]))
    sys.exit(0)


path = sys.argv[1]
if not os.path.exists(path):
    print('path {} not exist, please check.'.format(path))
    sys.exit(1)

# prefix of rename files
prefix = os.path.basename(os.path.realpath(path))
if arg_num == 3:
    prefix = sys.argv[2]

files = os.listdir(path)
print('--------------------------------------')
print('Old files from path ' + path)
print(files)
print('--------------------------------------')

num = 0
for file in files:
    num += 1
    newfile = '{}-{}{}'.format(prefix, num, os.path.splitext(file)[-1])
    os.rename(os.path.join(path, file), os.path.join(path, newfile))

print('New files from path ' + path)
print(os.listdir(path))
print('--------------------------------------')
