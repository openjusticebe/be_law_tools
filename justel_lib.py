import re
import os
import time
import logging
import requests
from slugify import slugify
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup as bs
from reg_lib import (
    RE_CLEANUP,
    RE_FORMATS,
    RE_KEY_MASKS,
)

logger = logging.getLogger(__name__)

def clean_text(text):
    for mod in RE_CLEANUP:
        (reg, rep) = mod
        text = re.sub(reg, rep, text, flags=re.M)
    return text


def format_text(text, clean=False):
    for mod in RE_FORMATS:
        (reg, rep) = mod
        text = re.sub(reg, rep, text, flags=re.M)
    if clean:
        text = clean_text(text)
    return text


def meta2md(data, dump=False):
    out = ['---']
    for k, v in data.items():
        if type(v) is list:
            out.append(f'{k}: {", ".join(v)}')
        else:
            out.append(f'{k}: {v}')
    out.append('\n---\n')
    if dump:
        print("\n".join(out))
    return "\n".join(out)


def meta_get(raw_text, html_text, data={}):
    for key, mask in RE_KEY_MASKS:
        for line in raw_text.splitlines():
            matches = re.match(mask, line)
            if matches:
                data[key] = matches['value'].replace(':', '').strip()
                break
    data['updated'] = [
        x.group() for x in re.finditer(r'([0-9AB]{10})', raw_text)
        if x.group() != data.setdefault('number', None)
    ]
    return data


def soup2meta(soup, meta_input={}):
    meta_table = soup.find('body').findChildren('table', recursive=False)[1]
    content = meta_table.findAll('th')[1]

    header = soup.find('body').findChildren('table', recursive=False)[0]
    archived_version = header.findAll('tr')[2].findAll('td')[4].find('a')
    if archived_version: archived_version = archived_version.getText()

    if "wetgeving" in header.getText():
        meta_input["language"] = "NL"
    elif "Législation" in header.getText():
        meta_input["language"] = "FR"

    for br in content.find_all('br'):
        br.replace_with("\n")

    raw_text = content.getText()
    if archived_version:
        raw_text += "\n" + archived_version

    return meta_get(raw_text, content, meta_input)

def soup2md(soup, clean=False, meta_input={}, do_return_meta=False):
    # Get meta
    meta = soup2meta(soup, meta_input)
    text_meta = meta2md(meta)

    # Get text
    table = soup.find('body').findChildren('table', recursive=False)[3]
    for br in soup.find_all('br'):
        br.replace_with("\n")
    raw_text = table.getText()
    text = format_text(raw_text, clean)

    if do_return_meta:
        return f"{text_meta}{text}", meta
    else:
        return f"{text_meta}{text}"


def justel_urls(startDate, endDate=False, interval='month', dtype='loi'):
    sdt = datetime.strptime(startDate, '%Y-%m-%d')
    edt = datetime.strptime(endDate, '%Y-%m-%d') if endDate else datetime.now()
    cur = sdt

    delta = relativedelta(months=1)
    isY, isD = False, False
    if interval == 'day':
        delta = relativedelta(days=1)
        isD = True
    elif interval == 'year':
        delta = relativedelta(years=1)
        isY = True
    elif interval != 'month':
        logger.warning("Date interval %s is not in supported list (day, year or month), applying default value (month)", interval)

    MASK_BASE = "http://www.ejustice.just.fgov.be/eli/{dtype}/{year}"
    MASK_MONTH = "/{month:02d}"
    MASK_DAY = "/{day:02d}"
    while cur <= edt:
        url = MASK_BASE.format(year=cur.year, dtype=dtype)
        if not isY:
            url += MASK_MONTH.format(month=cur.month)
            if isD:
                url += MASK_DAY.format(day=cur.day)
        yield url
        cur += delta


def justel_eli_scan(url):
    cur = 0
    links = []
    while cur < 4:
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 200:
            break
        time.sleep(2)
        cur += 1

    if r.status_code != 200:
        logger.warning("Bad response code: %s", r.status_code)
        return False, links
    if 'error select' in r.text:
        logger.warning('SQL Error on server')
        return False, links
    if '<center><FONT SIZE=6>Aide ELI ' in r.text:
        logger.warning('Page does not exist')
        return False, links
    try:
        soup = bs(r.text, 'html5lib')
        for link in soup.find_all('a', text=re.compile('\W*Justel\W*')):
            links.append(link.get('href'))
    except Exception as exc:
        logger.exception(exc)
        return False, links

    return True, links


def justel_doc_scan(url):
    cur = 0
    while cur < 4:
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 200:
            break
        time.sleep(2)
        cur += 1

    if r.status_code != 200:
        logger.warning("Bad response code: %s", r.status_code)
        return False, ""
    if '<center><FONT SIZE=6>Aide ELI ' in r.text:
        logger.warning('Page does not exist')
        return False, ""
    if '(NOTE : pas de texte disponible)' in r.text:
        logger.warning('Text not available')
        return False, ""
    if '(NOTA : geen tekst beschikbaar)' in r.text:
        logger.warning('Text not available')
        return False, ""
    if 'La version int&eacute;grale et consolid&eacute;e de ce texte n\'est pas disponible.' in r.text:
        logger.warning('Consolidated version not available')
        return False, ""
    if 'De geconsolideerde versie van deze tekst is niet beschikbaar.' in r.text:
        logger.warning('Consolidated version not available')
        return False, ""
    return True, r.text


def store_md(output_dir, md, meta):
    basepath = os.path.abspath(output_dir)
    slug_type = slugify(meta['dtype'], max_length=12, word_boundary=True)
    pub_date = datetime.strptime(meta['pubDate'], '%d-%m-%Y').strftime('%Y-%m-%d')
    if 'subTitle' in meta and meta['subTitle']:
        slug_title = slugify(meta['title'] + '-' + meta['subTitle'], max_length=60, word_boundary=True)
    else:
        slug_title = slugify(meta['title'], max_length=25, word_boundary=True)
    filename = f"{slug_type}_{pub_date}_{meta['lang']}_{slug_title}_{meta['number']}.md"
    filepath = os.path.join(basepath, meta['number'][:4], filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(md)
    return filepath

#this function extract metadata and main text (unformatted) of a justel page
def extract_data(url, clean = True):
    #download
    while True:
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 200:
            break
        time.sleep(2)
    soup = bs(r.text, 'html5lib')
    #get metadata
    meta = soup2meta(soup)
    #get text
    text_index = 0
    table = soup.find('body').findChildren('table', recursive=False)[text_index]
    while ((not table.find('tr').find('th')) or not (("Texte" in table.find('tr').find('th').getText()) or ("Tekst" in table.find('tr').find('th').getText()) )):
        text_index = text_index + 1
        table = soup.find('body').findChildren('table', recursive=False)[text_index]

    for br in soup.find_all('br'):
        br.replace_with("\n")
    raw_text = table.getText()
    if clean :
        raw_text = clean_text(raw_text)
    return raw_text, meta
