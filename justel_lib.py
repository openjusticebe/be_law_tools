import re
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from reg_lib import (
    RE_CLEANUP,
    RE_FORMATS,
    RE_KEY_MASKS,
)

logger = logging.getLogger(__name__)


def format_text(text, clean=False):
    for mod in RE_FORMATS:
        (reg, rep) = mod
        text = re.sub(reg, rep, text, flags=re.M)
    if clean:
        for mod in RE_CLEANUP:
            (reg, rep) = mod
            text = re.sub(reg, rep, text, flags=re.M)
    return text


def meta2md(data):
    print('---')
    for k, v in data.items():
        if type(v) is list:
            print(f'{k}: {", ".join(v)}')
        else:
            print(f'{k}: {v}')
    print('\n---\n')


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


def soup2meta(soup, meta_in={}):
    meta_table = soup.find('body').findChildren('table')[1]
    content = meta_table.findAll('th')[1]
    for br in content.find_all('br'):
        br.replace_with("\n")
    raw_text = content.getText()
    return meta_get(raw_text, content, meta_in)


def soup2md(soup, clean=False, meta_in={}):
    # Get meta
    text_meta = meta2md(soup2meta(soup), meta_in)

    # Get text
    table = soup.find('body').findChildren('table')[3]
    for br in soup.find_all('br'):
        br.replace_with("\n")
    raw_text = table.getText()
    text = format_text(raw_text, clean)

    return f"{text_meta}{text}"


def justel_urls(startDate, endDate=False, interval='month'):
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

    MASK_BASE = "http://www.ejustice.just.fgov.be/eli/loi/{year}"
    MASK_MONTH = "/{month:02d}"
    MASK_DAY = "/{day:02d}"
    while cur <= edt:
        url = MASK_BASE.format(year=cur.year)
        if not isY:
            url += MASK_MONTH.format(month=cur.month)
            if isD:
                url += MASK_DAY.format(day=cur.day)
        yield url
        cur += delta
