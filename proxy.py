# coding: utf-8

import socketserver
import re
import random
import requests

from bs4 import BeautifulSoup

import signal
import sys


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(4096).strip()
        print('\r\n{} request:'.format(self.client_address))
        print(self.data.decode('UTF-8'))

        if not self.data:
           return

        params = self.data.decode('UTF-8').splitlines()
        method = params[0].split()[0]
        url = params[0].split()[1]
        if ':443' in url:
            method = 'GET' if method == 'CONNECT' else method
            url = 'https://{}/'.format(url[:-4])

        # get raw headers and post query of request
        headers = {}
        post_query = ''
        isPOST = False
        for param in params[1:]:
            if param.strip() == '':
                isPOST = True
                continue
            if isPOST:
                post_query += param
            else:
                headers[param.split(':')[0]] = param.split(':')[1].strip()

        # show some infomations
        print('*****replaced request parameters*****')
        print(method, url)
        print(headers)
        print(post_query)
        print('*****sending request*****')

        """send request and get response
        cntlm proxy: http://127.0.0.1:3128
        SOCKS proxy: http://127.0.0.1:1080
        """
        proxies = {'socks': {'socks5':'http://127.0.0.1:1080'},
            'cntlm': {'http':'http://127.0.0.1:3128', 'https':'http://127.0.0.1:3128'}}
        response = requests.request(method, url, headers=headers,
            data=post_query,
            # proxies=proxies['socks']
            )
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())

        # get response headers
        response_headers = 'HTTP/1.0 {} {}\r\n'.format(response.status_code,
            response.reason)
        for key, value in response.headers.items():
            if key == 'Content-Encoding':
                value = 'ASCII'
            response_headers += '{}: {}\r\n'.format(key, value)
        response_headers += '\r\n'

        # modify response data
        response_content = response.content
        if 'basicStatus.cgi' in url:
            response_content = response_content.replace(b'ERROR', b'GOOD')\
                .replace(b'0', bytes(str(random.randint(0,10)), 'utf-8'))
            response_headers = re.sub('Content-length: *\d+ *\r\n',
                'Content-length: {}\r\n'.format(len(response_content)),
                response_headers)

        # forward packets
        self.request.send(response_headers.encode('UTF-8') + response_content)


def exit(signalnum, frame):
    server.server_close()
    print('Exit ...')
    sys.exit(1)

if __name__ == "__main__":
    HOST, PORT = 'localhost', 4444

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        signal.signal(signal.SIGINT, exit)
        print('server listening on Port:{}'.format(PORT))
        server.serve_forever()

