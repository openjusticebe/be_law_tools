#!/usr/bin/env python3
import click
import requests
import time
from bs4 import BeautifulSoup as bs
from justel_lib import (
    format_text,
    meta2md,
    meta_get,
)

TEST_URL = "http://www.ejustice.just.fgov.be/eli/loi/1804/03/21/1804032150/justel"
# http://www.ejustice.just.fgov.be/eli/wet/1804/03/21/1804032150/justel


@click.command()
@click.option('-c', '--clean', 'clean', is_flag=True)
def main(clean):
    url = TEST_URL
    while True:
        r = requests.get(TEST_URL, allow_redirects=False)
        if r.status_code == 200:
            break
        time.sleep(2)
    soup = bs(r.text, 'html5lib')

    # Get meta
    meta_table = soup.find('body').findChildren('table')[1]
    content = meta_table.findAll('th')[1]
    for br in content.find_all('br'):
        br.replace_with("\n")
    raw_text = content.getText()
    meta = meta_get(raw_text, content)
    meta['url'] = url

    # Get text
    table = soup.find('body').findChildren('table')[3]
    for br in soup.find_all('br'):
        br.replace_with("\n")
    raw_text = table.getText()
    text_meta = meta2md(meta)
    text = format_text(raw_text)

    # Output
    print(text_meta)
    print(text)


if __name__ == "__main__":
    main()
