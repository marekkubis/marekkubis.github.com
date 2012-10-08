# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader
from pybtex.database.input import bibtex

def nameformat(names):
    return names.replace(' and ', ', ')

parser = bibtex.Parser()
publications = parser.parse_file('publications.bib').entries.values()

env = Environment(loader=FileSystemLoader(['templates', 'content']))
env.filters['nameformat'] = nameformat

for path, dirnames, filenames in os.walk('content'):
    for filename in filenames:
        if filename.endswith('html'):
            with open(filename, 'w') as file:
                template = env.get_template(filename)
                file.write(template.render(name = filename, publications = publications).encode('utf-8'))

