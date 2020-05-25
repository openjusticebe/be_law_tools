#!/usr/bin/env python3
import logging
import click
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup as bs
from justel_lib import (
    soup2md
)

TEST_URL = "http://www.ejustice.just.fgov.be/eli/loi/1804/03/21/1804032150/justel"
# http://www.ejustice.just.fgov.be/eli/wet/1804/03/21/1804032150/justel
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('INFO'))
logger.addHandler(logging.StreamHandler())


@click.group()
@click.option('--debug/--no-debug', default=False)
def main(debug):
    # FIXME: set debug
    if debug:
        logger.setLevel(logging.getLevelName('DEBUG'))
        logger.debug('Debug enabled')


@main.command()
@click.option('-c', '--clean', 'clean', is_flag=True)
def test(clean):
    url = TEST_URL
    while True:
        r = requests.get(TEST_URL, allow_redirects=False)
        if r.status_code == 200:
            break
        time.sleep(2)
    soup = bs(r.text, 'html5lib')
    md = soup2md(soup, clean, {'url': url})

    # Output
    print(md)


@main.command()
@click.option('--start-date', '-s', 'sdate', default='1800-01-01')
@click.option('--end-date', '-e', 'edate', default=None)
@click.option(
    '--interval',
    '-i',
    type=click.Choice(['year', 'month', 'day']),
    default='year')
@click.option(
    '--doc-type',
    '-t',
    'dtype',
    type=click.Choice(
        ['constitution', 'loi', 'decret', 'ordonnance', 'arrete', 'grondwet', 'wet', 'decreet', 'ordonnantie', 'besluit'],
        case_sensitive=False),
    default='loi')
@click.option(
    '--output-dir',
    '-o',
    default='./out'
)
def scan(sdate, edate, interval, dtype, output_dir):
    start_dt = datetime.strptime(sdate, '%Y-%m-%d')
    end_dt = datetime.strptime(edate, '%Y-%m-%d') if end_date else datetime.now()
    # XXX: Make generator to obtain next URL to test, add unittests




if __name__ == "__main__":
    main()
