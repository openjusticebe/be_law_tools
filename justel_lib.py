import re
from reg_lib import (
    RE_CLEANUP,
    RE_FORMATS,
    RE_KEY_MASKS,
)

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
        print(f'{k}: {v}')
    print('---')


def meta_get(raw_text, html_text):
    data = {}
    for key, mask in RE_KEY_MASKS:
        for line in raw_text.splitlines():
            matches = re.match(mask, line)
            if matches:
                data[key] = matches['value']
                break
    data['updated'] = [
        x.group() for x in re.finditer(r'([0-9AB]{10})', raw_text)
        if x.group() != data.setdefault('number', None)
    ]
    return data
