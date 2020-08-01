#!/usr/bin/env python3
import sys
import logging
import re
import json

from justel_lib import (
    extract_data,
    JUSTEL_LEVEL_HIERARCHY,
)

logger = logging.getLogger(__name__)

def main(argv):
    url = argv[0]
    output = None
    if(len(argv)>1): output = argv[1]

    """Extract the content of a justel url and convert it into a json as a tree structure."""
    raw_text,meta = extract_data(url)

    array = text2dict_arr(raw_text, meta["language"])
    tree = dict_arr2tree(array)

    if output :
        serialize_tree(tree, output)
    else :
        print(tree)


#-----------------------
# Extracting metadata
RE_MASKS = { "FR" : [
    ('part',   "^\u00A0{0,2}PARTIE (?P<num>[\dIVXL]{1,5})(er|re)?\.( - )?(?P<txt>.*)$"),
    ('book',    "^\u00A0{0,2}LIVRE (?P<num>[\dIVXL]{1,5})(er|re)?\.( - )?(?P<txt>.*)$"),
    ('title',    "^\u00A0{0,2}TITRE (?P<num>[\dIVXL]{1,5})(er|re)?\.( - )?(?P<txt>.*)$"),
    ('chapter', "^\u00A0{0,2}CHAPITRE (?P<num>[\dIVXL]{1,5})(er|re)?\.( - )?(?P<txt>.*)$"),
    ('chapter', "^\u00A0{0,2}Chapitre (?P<num>[\dIVXL]{1,5})(er|re)?\.( - )?(?P<txt>.*)$"),
    ('section',  "^\u00A0{0,2}Section (?P<num>[\dIVXL]{1,5})(er|re)?\.( - )?(?P<txt>.*)$"),
    ('subsection',  "^\u00A0{0,2}Sous-section (?P<num>[\dIVXL]{1,5})(er|re)?\.( - )?(?P<txt>.*)$"),
    ('article',  "^\u00A0*Art(icle)?\.*\s*(?P<num>[\d/a-z\-:]{1,20})\s?(?P<suffix>[^.,§]*)\.(?P<txt>.*)")

], "NL" : [
    ('part',   "^\u00A0{0,2}DEEL (?P<num>[\dIVXL]{1,5})\.( - )?(?P<txt>.*)$"),
    ('book',    "^\u00A0{0,2}BOEK (?P<num>[\dIVXL]{1,5})\.( - )?(?P<txt>.*)$"),
    ('title',    "^\u00A0{0,2}TITEL (?P<num>[\dIVXL]{1,5})\.( - )?(?P<txt>.*)$"),
    ('chapter', "^\u00A0{0,2}HOOFDSTUK (?P<num>[\dIVXL]{1,5})\.( - )?(?P<txt>.*)$"),
    ('chapter', "^\u00A0{0,2}Hoofdstuk (?P<num>[\dIVXL]{1,5})\.( - )?(?P<txt>.*)$"),
    ('section',  "^\u00A0{0,2}Afdeling (?P<num>[\dIVXL]{1,5})\.( - )?(?P<txt>.*)$"),
    ('subsection',  "^\u00A0{0,2}Onderafdeling (?P<num>[\dIVXL]{1,5})\.( - )?(?P<txt>.*)$"),
    ('article',  "^\u00A0*Art(ikel)?\.*\s*(?P<num>[\d/a-z\-:]{1,20})\s?(?P<suffix>[^.,§(overeenkomstige)]*)\.(?P<txt>.*)")
]
}

#-------------------------

def identify_line(text, language):
    for element_type in RE_MASKS[language]:
        (element, reg) = element_type
        matches = re.match(reg, text)

        if matches :
            return { "type" : element, "ref" : matches['num'], "text" : matches['txt'].strip() }
    return None
#-------------------------

#post operations made after the instanciation of an element
def element_analyzing(element):
    if not element: return
    matches = re.match("(.|\n)*----------\n(?P<modifications>(.|\n)*)", element["text"])
    if matches:
        element["modifications"] = []
        for line in matches["modifications"].splitlines():
            matchesLine = re.match(".*(?P<num>[\d]{1,2})\)<Inséré par L\s(?P<reference>.*);.*:(?P<applicationDate>.*)>", line)
            if matchesLine:
                law_ref = matchesLine['reference'].strip()[:13]
                element["modifications"].append({ "type": "add", "index" : matchesLine['num'], "law_reference" : law_ref, "complete_reference" : matchesLine['reference'].strip(), "applicationDate" : matchesLine['applicationDate'].strip() })

            matchesLine = re.match(".*(?P<num>[\d]{1,2})\)<L\s(?P<reference>.*);.*:(?P<applicationDate>.*)>", line)
            if matchesLine:
                law_ref = matchesLine['reference'].strip()[:13]
                element["modifications"].append({ "type": "update", "index" : matchesLine['num'], "law_reference" : law_ref, "complete_reference" : matchesLine['reference'].strip(), "applicationDate" : matchesLine['applicationDate'].strip() })

        element["text"] = element["text"].split("\n----------")[0]
        element["text"] = element["text"].split("----------")[0]
            
    return element

def text2dict_arr(raw_text, language):
    data = []
    currentElement = None
    previousElement = None
    for line in raw_text.splitlines():
        text = line
        currentElement = identify_line(text, language)
        if currentElement :
            data.append(currentElement)
            if previousElement: element_analyzing(previousElement)
            previousElement = currentElement
        else :
            text = text.strip()
            if text and previousElement:
                previousElement["text"] = previousElement["text"] + "\n" + text

    element_analyzing(previousElement)

    return data
#-------------------------


def dict_arr2tree(array):
    element_hierarchy = JUSTEL_LEVEL_HIERARCHY

    actual_hierarchy = []
    # determine the hierarchy of elements in the parsed text.
    for level in element_hierarchy:
        element = next((dict for dict in array if dict["type"] == level), None)
        if element:
            actual_hierarchy.append(level)

    tree = {"level":-1, "children":[], "type":"root"}
    current_node = tree
    for dict in array:
        dict["level"] = actual_hierarchy.index(dict["type"])
        dict["children"] = []
        current_node = insert_in_tree(dict, current_node)

    return tree


#insert an element related to the tree_node argument.
# if the element has a higher level than the tree_node, it will be append in the tree_node children array. 
# else, we call this fonction recursively for element and tree_node parent.
#Result will be a tree with each children having a level higher than their parent.
def insert_in_tree(element, tree_node):
    if element["level"] > tree_node["level"]:
        tree_node["children"].append(element)
        element["parent"] = tree_node
    else:
        return insert_in_tree(element, tree_node["parent"])
    return element


#util function to delete parent attribute to avoid circular reference during serialization
def clean_node(node):
    node["parent"] = None
    node["children"] = list(map(lambda child: clean_node(child), node["children"]))
    return node


def serialize_tree(tree, output):
    tree = clean_node(tree)
    with open(output, "w") as f:
        f.write(json.dumps(tree))
    logger.info("json saved into file %s", output)
 
#-------------------------


if __name__ == "__main__":
    main(sys.argv[1:])
