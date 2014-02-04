# -*- coding: utf-8 -*-
import os
import re

from jinja2 import Environment, FileSystemLoader
from pybtex.database.input import bibtex

key_pattern = re.compile('([A-Z])[a-z]*([0-9]+.*)')
entry_start_pattern = re.compile('@[A-Za-z]+{(.*),')

def key2bibfile(key):
    matcher = key_pattern.match(key)
    return matcher.group(1).lower() + matcher.group(2) + '.bib'

def nameformat(names):
    return names.replace(' and ', ', ')

curr_file = None

with open('publications.bib') as pubfile:
    for line in pubfile:
        matcher = entry_start_pattern.search(line)

        if matcher != None:
            bibfilename = key2bibfile(matcher.group(1))

            if curr_file != None:
                curr_file.close()

            curr_file = open(bibfilename, 'w')

        curr_file.write(line)
 
if curr_file != None:
    curr_file.close()

parser = bibtex.Parser()
publications = parser.parse_file('publications.bib').entries.values()

env = Environment(loader=FileSystemLoader(['_templates', '_content']))
env.filters['nameformat'] = nameformat
env.filters['key2bibfile'] = key2bibfile

for path, dirnames, filenames in os.walk('_content'):
    for filename in filenames:
        if filename.endswith('html'):
            with open(filename, 'w') as file:
                template = env.get_template(filename)
                file.write(template.render(name = filename, publications = publications).encode('utf-8'))

