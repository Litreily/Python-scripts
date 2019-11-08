#!/usr/bin/env python
# -*- conding: utf-8 -*-
# Description: auto download and remove a file base on url

import requests
import time
import logging
import os
import sys
import argparse

def download(url, filename):
    res = requests.get(url, stream=True)
    total_length = res.headers.get('content-length')

    if res.status_code == 404:
        logging.error("NOT FOUND FILE " + filename)
        sys.exit(1)

    with open(filename, 'wb') as f:
        if not total_length:
            f.write(res.content)
        else:
            chunk_count = 0
            for data in res.iter_content(chunk_size=1024):
                f.write(data)
                f.flush()

                chunk_count += len(data)
                dl_percent = chunk_count / (int)(total_length)
                if dl_percent > 1:
                    dl_percent = 1
                done = int(80 * dl_percent)

                # show processing bar
                print("\r[{}{}]{}%".format('#' * done, ' ' * (80 - done),
                    (int)(100 * dl_percent)), end='', flush=True)
            print()
    logging.info('Download success!')
    return True

def parse():
    parser = argparse.ArgumentParser(description='Download url files.')
    parser.add_argument('-u', '--url', help='url, will escaped --path and --host')
    parser.add_argument('--host', help='host name or ip')
    parser.add_argument('-p','--path', help='file path, base on --host')
    parser.add_argument('-n','--num', help='download n times')
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO,
            format='[%(asctime)s][%(levelname)s] %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S')

    args = parse()
    if args.url:
        url = args.url
    elif args.host and args.path:
        url = 'http://{}/{}'.format(args.host, args.path)
    else:
        default_url = 'http://www.baidu.com'
        logging.warn('Argument error or missing, '
                'use default url: {}'.format(default_url))
        url = default_url

    dl_times = -1 if not args.num else (int)(args.num)

    count = 0

    filename = url.rstrip('/ ').split('/')[-1]
    if os.path.isfile(filename):
        os.remove(filename)

    logging.info("=============================")
    logging.info("Starting Test...")
    logging.info("=============================")

    try:
        while True:
            logging.info("downloading {0} {1} times".format(url, count))
            download(url, filename)

            count += 1
            if dl_times > 0 and count >= dl_times:
                break;

            time.sleep(5)
            os.remove(filename)

    except KeyboardInterrupt:
        logging.info('Exit by CTRL-C')
        sys.exit(1)


if __name__  == '__main__':
    main()
