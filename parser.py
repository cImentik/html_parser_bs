#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os
import textwrap

from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import urlopen, Request
from urllib.parse import urlparse

import config


class ArgvParser():
    """Arguments parser"""
    def __init__(self):
        self.__arg = None
        self.create_argv_parser()

    def create_argv_parser(self):
        argv = argparse.ArgumentParser()
        argv.add_argument('url')
        self.arg = argv.parse_args().url

    def make_url_scheme(self, url):
        if ('http://' in url) or ('https://'):
            return url
        else:
            return 'http://'+url

    def get_arg(self):
        return self.make_url_scheme(self.arg)


class FsHelper():
    """File system helper class"""
    @staticmethod
    def get_path_to_file(url):
        o = urlparse(url)
        path = o.path.strip('/').split('/')
        if '.' in path[-1]:
            end_path_list = path[-1].split('.')
            end_path_list[-1] = 'txt'
            path[-1] = '.'.join(end_path_list)
        else:
            path[-1] = path[-1]+'.txt'
        return os.path.join(os.getcwd(), o.netloc, '/'.join(path))

    @staticmethod
    def write_file(filename, text):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            file.write(text)


class MyHTMLParser(object):
    """Main class of parsing"""
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.content = None
        soup = BeautifulSoup(self.get_page(), "html.parser")
        self.content = self.get_header(soup)
        c_list = soup.find(config.C_TAG, config.C_ATR)
        self.content += self.get_text(soup)

    def get_content(self):
        return self.content

    def get_page(self):
        content = None
        req = Request(
            self.url,
            data=None,
            headers=config.headers
        )
        try:
            resource = urlopen(req)
        except URLError as e:
            print(e.msg)
        else:
            if resource.code == 200:
                html = resource.read().decode(
                    resource.headers.get_content_charset()
                )
            else:
                raise URLError('Connection status bad')
        return html

    def get_header(self, cont):
        return cont.find(config.H_TAG, config.H_ATR).text+"\n\n"

    def get_text(self, cont):
        text = ''
        for nf_text in cont.find_all(config.T_TAG):
            t = nf_text.text+"\n\n"
            for a in nf_text.find_all('a', href=True):
                t = t.replace(a.text, '['+a['href']+'] '+a.text)
            text += t
        return text

    def get_fill_text(self):
        text = self.get_content()
        textLines = text.split('\n')
        wrapedLines = []
        indentRe = re.compile('^(\W+)')
        for line in textLines:
            preservedIndent = ''
            existIndent = re.search(indentRe, line)
            if (existIndent):
                preservedIndent = existIndent.groups()[0]
            wrapedLines.append(textwrap.fill(
                line,
                width=config.MAX_TEXT,
                subsequent_indent=preservedIndent
            ))
        text = '\n'.join(wrapedLines)
        return text


def main():
    argv_parser = ArgvParser()
    p = MyHTMLParser(argv_parser.get_arg())
    FsHelper.write_file(
        FsHelper.get_path_to_file(argv_parser.get_arg()), p.get_fill_text()
        )
    # print(p.get_fill_text())

if __name__ == '__main__':
    main()

# url = "http://www.gazeta.ru/army/news/8611511.shtml"
# url = "http://www.gazeta.ru/army/news/8612927.shtml"
# url = "https://lenta.ru/news/2016/05/08/canadabridge/"
# url = "https://lenta.ru/news/2016/05/10/stopsalary/"
