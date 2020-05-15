#!/usr/bin/env python3
import click
import requests
import time
import re
from bs4 import BeautifulSoup as bs

# TEST_URL = "http://www.ejustice.just.fgov.be/cgi_loi/loi_a1.pl?detail=1804032130%2ff&caller=list&cn=1804032130&table_name=loi&nm=1804032150&language=fr&fromtab=loi_all"
TEST_URL = "http://www.ejustice.just.fgov.be/eli/loi/1804/03/21/1804032150/justel"
# http://www.ejustice.just.fgov.be/eli/wet/1804/03/21/1804032150/justel


RE_FORMATS = [
    (r"\s*Texte\s*Table des matières\s*Début\s*", ""),
    (r"Art\.  (?P<artnum>[\d/a-z\-]{1,20})\.", "**Art. \g<artnum>.**"),
    (r"^.*----------\s*$", ""),
    (r"^\u00A0{2}\((?P<refnum>\d{1,3})\)<(?P<ref>.*)>\s*$", "> \g<refnum>: \g<ref>\n\n"),
    (r"^(?P<titre>TITRE .*)$", "# \g<titre>"),
    (r"^\u00A0{2}(?P<titre>TITRE .*)$", "# \g<titre>"),
    (r"^\u00A0{2}LIVRE (?P<num>[\dIVL]{1,5})\.( - )?(?P<txt>.*)$", "# Livre \g<num> \g<txt>"),
    (r"^\u00A0{2}TITRE (?P<num>[\dIVL]{1,5})\.( - )?(?P<txt>.*)$", "## Titre \g<num> \g<txt>"),
    (r"^\u00A0{2}CHAPITRE (?P<num>[\dIVL]{1,5})(er)?\.( - )?(?P<txt>.*)$", "### Chapitre \g<num> \g<txt>"),
    (r"^\u00A0{2}SECTION (?P<num>[\dIVL]{1,3})(re)?\.(?P<txt>.*)$", "#### Section \g<num> \g<txt>"),
    (r"^\u00A0{2}Section (?P<num>[\dIVL]{1,3})(re)?\.(?P<txt>.*)$", "#### Section \g<num> \g<txt>"),
    (r"^\u00A0{2}\s*-\s*", " * "),
    (r"^\u00A0{2}\s*(?P<num>\d+)°?\s*", " \g<num>. "),
    (r"^\u00A0{2}\s*§\s*(?P<num>\d+)\.?", "\n\n§\g<num>. "),
]

RE_CLEANUP = [
    (r"^\u00A0{2}\s*", "\n"),
]


@click.command()
@click.option('-c', '--clean', 'clean', is_flag=True)
def main(clean):
    click.echo("Testing justel2md")
    while True:
        r = requests.get(TEST_URL, allow_redirects=False)
        if r.status_code == 200:
            break
        time.sleep(2)
    # soup = bs(r.text, 'html.parser')
    # soup = bs(r.text, 'lxml')
    soup = bs(r.text, 'html5lib')
    table = soup.find('body').findChildren('table')[3]
    for br in soup.find_all('br'):
        br.replace_with("\n")
    # textTable = el.findNext('table').findAll('tr')
    text = table.getText()
    for mod in RE_FORMATS:
        (reg, rep) = mod
        text = re.sub(reg, rep, text, flags=re.M)
    if clean:
        for mod in RE_CLEANUP:
            (reg, rep) = mod
            text = re.sub(reg, rep, text, flags=re.M)
    print(text)


if __name__ == "__main__":
    main()
