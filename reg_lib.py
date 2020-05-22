# Formating text
RE_FORMATS = [
    (r"\s*Texte\s*Table des matières\s*Début\s*", ""),
    (r"Art(icle)?\.  (?P<artnum>[\d/a-z\-]{1,20})\.", "**Art. \g<artnum>.**"),
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

# Removing unbreakable spaces
RE_CLEANUP = [
    (r"^\u00A0{2}\s*", "\n"),
]

# Extracting metadata
RE_KEY_MASKS = [
    ('dateString', "^(?P<value>\d{1,2} [A-Z]{3,9} \d{4})"),
    ('title', "^\d{1,2} [A-Z]{3,9} \d{4}\. - (?P<value>[^\.]*)"),
    ('subTitle', "^\d{1,2} [A-Z]{3,9} \d{4}\. - [^\.]*\. - (?P<value>.*)$" ),
    ('pubDate', ".*Publication\s*:\s*(?P<value>[\d\-]+)"),
    ('startDate', ".*vigueur\s*:\s*(?P<value>[\d\-]+)"),
    ('number', ".*numéro\s*:\s*(?P<value>[0-9AB]{10})"),
]
