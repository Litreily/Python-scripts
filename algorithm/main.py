#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import time
import random
import imageio
from quick_sort import QuickSort
import os
from os.path import join


def save_gif(path, gif_name):
    if not os.path.exists(path) or len(os.listdir(path))==0:
        return

    images = []
    for file_name in range(len(os.listdir(path))):
        file_path = join(path, '{}.png'.format(file_name))
        images.append(imageio.imread(file_path))
    imageio.mimsave(join(path, gif_name), images, 'GIF', duration=0.2)


def main():
    data = []
    random.seed(time.time())
    data = [_ for _ in range(0,20)]
    random.shuffle(data)
    # data = [40] * 40
    # data = [_ for _ in reversed(range(40))]

    print('source: {0}'.format(data))
    start = time.time()
    qs = QuickSort(debug=True, save_fig=True)
    swap_times, fig_path = qs.sort(data)
    save_gif(fig_path, 'quick_sort.gif')
    stop = time.time()
    print('result: {0}\n'.format(data))

    print('----------------------------------')
    print('swap times: {0}'.format(swap_times))
    print('spend time: {0}s'.format(stop - start))
    print('image path: {0}'.format(fig_path))
    print('----------------------------------')


if __name__ == '__main__':
    main()
