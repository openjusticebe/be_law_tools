#!/usr/bin/env python3
import logging
import click
import requests
import time
from bs4 import BeautifulSoup as bs
from justel_lib import (
    soup2md,
    justel_urls,
    justel_eli_scan,
    justel_doc_scan,
    store_md,
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
    default='./output'
)
def scan(sdate, edate, interval, dtype, output_dir):
    """
    Generate a url for each date within given interval,
    and scan for useable documents.
    """
    cnt_page = 0
    cnt_doc = 0
    for jurl in justel_urls(sdate, edate, interval, dtype):
        page_check, links = justel_eli_scan(jurl)
        cnt_page += 1

        if not page_check:
            logger.debug("Url %s invalid, continueing", jurl)
            continue

        for link in links:
            cnt_doc += 1
            doc_check, text = justel_doc_scan(link)
            if not doc_check:
                logger.debug("Document %s invalid, continueing", link)
                continue
            soup = bs(text, 'html5lib')
            md, meta = soup2md(soup, True, {'url': link}, True)

            filepath = store_md(output_dir, md, meta)
            logger.debug("Wrote file %s", filepath)

        click.secho(f"Scanned {cnt_page} pages, {cnt_doc} documents", bg='green', fg='black', bold=True)

    # XXX: Make generator to obtain next URL to test, add unittests




if __name__ == "__main__":
    main()
