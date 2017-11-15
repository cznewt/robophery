# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'RoboPhery'
copyright = u'2017, Aleš Komárek'
version = '0.5'
release = '0.5.0'
exclude_patterns = []
pygments_style = 'sphinx'

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    'collapse_navigation': False,
    'display_version': False,
}

latex_elements = {}
latex_documents = [
    ('index', 'robophery.tex', u'RoboPhery Documentation',
     u'RoboPhery Team', 'manual'),
]
