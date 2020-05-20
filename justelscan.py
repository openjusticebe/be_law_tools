#!/usr/bin/env python3
import click
import requests
import json
import time
import logging
import re
from bs4 import BeautifulSoup as bs


logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('DEBUG'))
logger.addHandler(logging.StreamHandler())

BASE_URL = "http://www.ejustice.just.fgov.be/eli/loi/{year}/"


def content_get(year):
    content_url = BASE_URL.format(year=year)
    logger.info('Scanning URL %s', content_url)
    while True:
        r = requests.get(content_url, allow_redirects=False)
        if r.status_code == 200:
            break
        time.sleep(2)
    return bs(r.text, 'html5lib')


def links_get(soup):
    links = []
    for link in soup.find_all('a', text=re.compile('\W*Justel\W*')):
    #for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links


@click.command()
@click.option('--year', 'year', default=1804)
@click.option(
    '-d',
    '--doc-type',
    'doctype',
    type=click.Choice(
        ['constitution', 'loi', 'decret', 'ordonnance', 'arrete', 'grondwet', 'wet', 'decreet', 'ordonnantie', 'besluit'],
        case_sensitive=False),
    default='loi')
@click.option(
    '-o',
    '--output',
    'output',
    type=click.Choice(['stdout', 'json']),
    default='stdout')
def main(year, doctype, output):
    """
    Scan Justel for links to documents

    Doctype values:
        constitution / loi / decret / ordonnance / arrete
        grondwet / wet / decreet / ordonnantie / besluit

    Output values:
        stdout
        json

    """
    content = content_get(year)
    links = links_get(content)
    print(json.dumps(links, indent=2))


if __name__ == "__main__":
    main()
