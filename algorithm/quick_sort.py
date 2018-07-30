#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @date: 2018.06.20

import matplotlib.pyplot as plt
import time
import os

class QuickSort(object):
    '''Quick sort algorithm'''
    def __init__(self, debug=False, save_fig=False):
        self.debug = debug
        self.save_fig = save_fig
        self.fig, self.ax = plt.subplots()
        plt.ion()

        if self.save_fig:
            self.path = './images/{0}'.format(time.strftime('%Y%m%d_%H%M%S'))
            os.makedirs(self.path)
        else:
            self.path = None

    def sort(self, data):
        self.swap_times = 0
        self.__plot_figure(data)
        # set the largest element to the end
        # self.__swap(data, data.index(max(data)), len(data) - 1)
        self.__sort(data, 0, len(data) - 1)
        return self.swap_times, self.path

    def __swap(self, data, lo, hi):
        data[lo], data[hi] = data[hi], data[lo]
        self.swap_times += 1

        if self.debug:
            print('\t{0} swap({1}, {2})'.format(data, lo, hi))

        self.__plot_figure(data, lo, hi, show_swap=True)

    def __plot_figure(self, data, lo=0, hi=0, show_swap=False):
        '''plot and save figure'''
        self.ax.clear()
        self.ax.set_title('data quicksort')
        self.ax.bar(range(len(data)), data, label='data')
        if show_swap:
            self.ax.bar([lo, hi], [data[lo], data[hi]], color='red', label='swap')
        plt.legend()
        plt.pause(0.001)

        if self.save_fig:
            plt.savefig('{0}/{1}.png'.format(self.path, self.swap_times))

    def __sort(self, data, lo, hi):
        if lo >= hi:
            return
        key = self.__partition(data, lo, hi)
        self.__sort(data, lo, key - 1)
        self.__sort(data, key + 1, hi)

    def __partition(self, data, lo, hi):
        '''partition array'''
        i = lo
        j = hi
        v = data[lo] # slicing element
        while True:
            # find one element that larger than v scan from left to right(→)
            i += 1
            while data[i] < v:
                # below judge can dropped if the end element is the largest
                if i == hi:
                    break
                i += 1

            # find one element that smaller than v scan from right to left(←)
            while v < data[j]:
                j -= 1

            if i >= j:
                break
            self.__swap(data, i, j)
        self.__swap(data, lo, j)
        return j
