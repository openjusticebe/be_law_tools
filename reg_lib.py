# Formating text
RE_FORMATS = [
    (r"\s*(Texte|Tekst)\s*(Table des matières|Inhoudstafel)\s*(Début|Begin)\s*", ""),
    (r"Art(icle|ikel)?\.*\s*(?P<artnum>[\d/a-z\-:\.]{1,20})\.", "**Art. \g<artnum>.**"),
    (r"^.*----------\s*$", ""),
    (r"^\u00A0{2}\((?P<refnum>\d{1,3})\)<(?P<ref>.*)>\s*$", "> \g<refnum>: \g<ref>\n\n"),
    (r"^(?P<titre>(TITRE|TITEL) .*)$", "# \g<titre>"),
    (r"^\u00A0{2}(?P<titre>(TITRE|TITEL) [^\dIVL]*)$", "# \g<titre>"),
    (r"^\u00A0{2}(LIVRE|BOEK) (?P<num>[\dIVLX]{1,5}(er|re)?)\.( - )?(?P<txt>.*)$", "# Livre \g<num> \g<txt>"),
    (r"^\u00A0{2}BOEK (?P<num>[\dIVLX]{1,5})\.( - )?(?P<txt>.*)$", "# Boek \g<num> \g<txt>"),
    (r"^\u00A0{2}TITRE (?P<num>[\dIVLX]{1,5}(er|re|ère)?(bis|ter|quater)?)\.( - )?(?P<txt>.*)$", "## Titre \g<num> \g<txt>"),
    (r"^\u00A0{2}TITEL (?P<num>[\dIVLX]{1,5}(bis|ter|quater)?)\.( - )?(?P<txt>.*)$", "## Titel \g<num> \g<txt>"),
    (r"^\u00A0{2}(CHAPITRE|Chapitre) (?P<num>[\dIVLX]{1,5}(er|re|ère)?)\.( - )?(?P<txt>.*)$", "### Chapitre \g<num> \g<txt>"),
    (r"^\u00A0{2}(HOOFDSTUK|Hoofdstuk) (?P<num>[\dIVLX]{1,5})\.( - )?(?P<txt>.*)$", "### Hoofdstuk \g<num> \g<txt>"),
    (r"^\u00A0{2}(SECTION|Section) (?P<num>[\dIVLX]{1,3}(er|re|ère)?)\.(?P<txt>.*)$", "#### Section \g<num> \g<txt>"),
    (r"^\u00A0{2}(SOUS-SECTION|Sous-section) (?P<num>[\dIVLX]{1,3}(er|re|ère)?)\.(?P<txt>.*)$", "#### Sous-section \g<num> \g<txt>"),
    (r"^\u00A0{2}(AFDELING|Afdeling) (?P<num>[\dIVLX]{1,3})\.(?P<txt>.*)$", "#### Afdeling \g<num> \g<txt>"),
    (r"^\u00A0{2}(ONDERAFDELING|Onderafdeling) (?P<num>[\dIVLX]{1,3})\.(?P<txt>.*)$", "#### Onderafdeling \g<num> \g<txt>"),
    (r"^\u00A0{2}\s*-\s*", " * "),
    (r"^\u00A0{2}\s*(?P<num>\d+)°?\s*", " \g<num>. "),
    (r"^\u00A0{2}\s*§\s*(?P<num>\d+)\.?", "\n\n§\g<num>. "),
    (r"<(?P<note>[^>]*)>", "`\g<note>`"),
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
    ('pubDate', ".*Publi(cation|katie|catie)\s*:\s*(?P<value>[\d\-]+)"),
    ('startDate', ".*(vigueur|Inwerkingtreding)\s*:\s*(?P<value>[\d\-]+)"),
    ('number', ".*(numéro|nummer)\s*:\s*(?P<value>[0-9AB]{10})"),
    ('source', ".*(Source|Bron)\s*:\s*(?P<value>.*)$"),
]
