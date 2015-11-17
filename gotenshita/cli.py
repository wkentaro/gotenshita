#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import re
import datetime

import tabulate
import requests
from bs4 import BeautifulSoup


__version__ = '1.0.2'


def get_open_info_monthly(datetime_):

    yearmonth = datetime_.strftime('%Y%m')

    url = 'http://www.undoukai-reserve.com/facility/reserve/goten/calendar.php?place=gymnasium&yearmonth={0}'
    url = url.format(yearmonth)
    res = requests.get(url)
# res.encoding = res.apparent_encoding
    res.encoding = 'EUC-JP'
# print(res.apparent_encoding)
    soup = BeautifulSoup(res.text, 'lxml')

    close_color = ['#ffaa00', '#ffdd66']

    month_table = soup.find('table', {'cellpadding': '3', 'bgcolor': 'black', 'width': '765'})

# time header from 10:00 to 20:20
    time_header = month_table.find('td', {'bgcolor': 'black'})
    time_header = [tuple(tr.text.strip().split(u'\u301c')) for tr in time_header.find_all('tr')]

    month_info = {}
    for date_sec in month_table.find_all('td', {'bgcolor': 'eeaa00'}):
        if not (date_sec.a and u'日' in date_sec.a.text):
            continue  # this is not date section
        date_table = date_sec.table
        time_sections = []  # is open? each time tables
        rows = date_table.find_all('tr')
        rows.pop(0)  # remove A-F header
        assert len(time_header) == len(rows)
        for tr in rows:
            time_sec = [td.attrs.get('bgcolor') not in close_color for td in tr.find_all('td')]
            time_sec = dict(zip('abcdef', time_sec))
            time_sections.append(time_sec)
        date = int(re.sub(u'日\(.*\)$', '', date_sec.a.text))
        month_info[date] = dict(zip(time_header, time_sections))
    return month_info


def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('court', nargs='?', default='a', type=str,
                        help='A to F (default: A)')
    args = parser.parse_args()

    court = args.court.lower()
    if court not in 'abcdef':
        sys.stderr.write('Invalid court, we support A,B,C,..F.\n')

    now = datetime.datetime.now()
    print('=' * 28)
    print('Date: {}, Court: {}'.format(now.strftime('%Y-%m-%d'), court.upper()))
    print('=' * 28)
    table = []
    month_info = get_open_info_monthly(now)
    for time, is_open in sorted(month_info[int(now.strftime('%d'))].items()):
        open_or_close = 'open' if is_open[court] else 'close'
        table.append(['{}-{}'.format(*time), open_or_close])
    print(tabulate.tabulate(table, headers=['time', 'open or close'], stralign='center'))


if __name__ == '__main__':
    main()
