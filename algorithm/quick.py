#!/bin/env python
# -*- coding:utf-8 -*-
# This script only contains the implement of quicksort

import random

def sort(data):
    __sort(data, 0, len(data) - 1)

def __swap(data, lo, hi):
    data[lo], data[hi] = data[hi], data[lo]

def __sort(data, lo, hi):
    if lo >= hi:
        return
    key = __partition(data, lo, hi)
    __sort(data, lo, key - 1)
    __sort(data, key + 1, hi)

def __partition(data, lo, hi):
    '''partition array'''
    i = lo
    j = hi
    v = data[lo] # slicing element
    while True:
        # find one element that larger than v scan from left to right(→)
        i += 1
        while data[i] < v:
            if i == hi:
                break
            i += 1

        # find one element that smaller than v scan from right to left(←)
        while v < data[j]:
            if j == lo:
                break
            j -= 1

        if i >= j:
            break
        __swap(data, i, j)
    __swap(data, lo, j)
    return j


def main():
    data = [_ for _ in range(20)]
    random.shuffle(data)
    print(data)
    sort(data)
    print(data)


if __name__ == '__main__':
    main()
