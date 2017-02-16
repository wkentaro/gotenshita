# -*- coding: utf-8 -*-

import argparse
import datetime
import pkg_resources
import re
import sys
import time

from bs4 import BeautifulSoup
import requests
import tabulate
import termcolor
import yaml


__version__ = pkg_resources.get_distribution('gotenshita').version


def _is_holiday(dt):
    yaml_file = 'https://raw.githubusercontent.com/k1LoW/holiday_jp/master/holidays.yml'  # NOQA
    res = requests.get(yaml_file)
    data = yaml.load(res.text)
    info = data.get(dt)
    if info:
        return info['en']
    return False


def _is_sunday(dt):
    if dt.weekday() == 6:
        return 'Sunday'
    return False


def is_gotenshita_open(dt, verbose=True):
    stamp = dt.strftime('%Y-%m-%d')
    holiday = _is_sunday(dt) or _is_holiday(dt) or None
    if holiday:
        if verbose:
            print('{} is {}, and Gotenshita is closed.'
                  .format(stamp, termcolor.colored(holiday, color='red')))
        return False
    return True


def get_open_info_monthly(datetime_):
    yearmonth = datetime_.strftime('%Y%m')

    url = 'http://www.undoukai-reserve.com/facility/reserve/goten/calendar.php?place=gymnasium&yearmonth={}'  # NOQA
    url = url.format(yearmonth)
    res = requests.get(url)
    res.encoding = 'EUC-JP'
    soup = BeautifulSoup(res.text, 'lxml')

    close_color = ['#ffaa00', '#ffdd66']

    month_table = soup.find(
        'table', {'cellpadding': '3', 'bgcolor': 'black', 'width': '765'})

    # time header from 10:00 to 20:20
    time_header = month_table.find('td', {'bgcolor': 'black'})
    time_header = [tuple(tr.text.strip().split(u'\u301c'))
                   for tr in time_header.find_all('tr')]

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
            time_sec = [td.attrs.get('bgcolor') not in close_color
                        for td in tr.find_all('td')]
            time_sec = dict(zip('abcdef', time_sec))
            time_sections.append(time_sec)
        date = int(re.sub(u'日\(.*\)$', '', date_sec.a.text))
        month_info[date] = dict(zip(time_header, time_sections))
    return month_info


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'court', nargs='?', default=None, type=str,
        help="A to F (default is all), supports multiple select like 'a,f'")
    parser.add_argument('-p', '--show-past', help='show even if past time',
                        action='store_true')
    parser.add_argument('-t', '--tomorrow', help="show tomorrow's data",
                        action='store_true')
    args = parser.parse_args()

    show_past = args.show_past
    tomorrow = args.tomorrow

    # decide the date when the info is shown about
    when = datetime.datetime.now()
    if tomorrow:
        when = datetime.datetime(when.year, when.month, when.day)
        when += datetime.timedelta(days=1)

    # check if gotenshita is open/close
    if not is_gotenshita_open(when):
        sys.exit(0)

    # validate args.court
    if args.court is None:
        courts = list('abcdef')
    else:
        courts = args.court.lower().split(',')
        for c in courts:
            if c not in 'abcdef':
                sys.stderr.write('Invalid court, we support A,B,C,..F.\n')
                sys.exit(1)

    # compose the result table
    table = []
    month_info = get_open_info_monthly(when)
    when_time = time.strptime(when.strftime('%H:%M:%S'), '%H:%M:%S')
    for t, is_open in sorted(month_info[int(when.strftime('%d'))].items()):
        end_time = time.strptime(t[1], '%H:%M')
        if not show_past and end_time < when_time:
            continue
        period = '{}-{}'.format(*t)
        row = [period]
        for c in courts:
            open_or_close = 'close'
            if is_open[c]:
                if len(courts) == 1:
                    row[0] = termcolor.colored(period, 'green')
                open_or_close = termcolor.colored('open', 'green')
            row.append(open_or_close)
        table.append(row)
    headers = [when.strftime('%Y-%m-%d %a')] + courts
    print(tabulate.tabulate(table, headers=headers, stralign='center'))
