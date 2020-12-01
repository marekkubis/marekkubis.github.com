# -*- coding: utf-8 -*-
import os
import re
import yaml

from jinja2 import Environment, FileSystemLoader
from pybtex.database.input import bibtex

key_pattern = re.compile('([a-z])[a-z]*([0-9]+.*)')
entry_start_pattern = re.compile('@[A-Za-z]+{(.*),')


def key2bibfile(key):
    matcher = key_pattern.match(key)
    return matcher.group(1).lower() + matcher.group(2) + '.bib'


def nameformat(persons):
    return ', '.join(str(person) for person in persons)


curr_file = None

with open('publications.bib') as pubfile:
    for line in pubfile:
        matcher = entry_start_pattern.search(line)

        if matcher is not None:
            bibfilename = key2bibfile(matcher.group(1))

            if curr_file is not None:
                curr_file.close()

            curr_file = open(bibfilename, 'w')

        if not line.lstrip().startswith('note'):
            curr_file.write(line)

if curr_file is not None:
    curr_file.close()

parser = bibtex.Parser()
publications = parser.parse_file('publications.bib').entries.values()

with open('data.yaml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)


def plword(word):
    for key, value in data['en2pl'].items():
        word = word.replace(key, value)
    return word


env = Environment(loader=FileSystemLoader(['_templates', '_content']))
env.filters['nameformat'] = nameformat
env.filters['key2bibfile'] = key2bibfile
env.filters['pl'] = plword

for path, dirnames, filenames in os.walk('_content'):
    for filename in filenames:
        if filename.endswith('html'):
            with open(filename, 'w') as file:
                template = env.get_template(filename)
                file.write(template.render(name=filename, data=data, publications=publications))
