# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

#import evolved5g

# -- Project information

project = 'EVOLVED-5G SDK'
copyright = '2021, EVOLVED-5G'
author = 'EVOLVED-5G'

# The short X.Y version.
#version = evolved5g.__version__
# The full version, including alpha/beta/rc tags.
#release = evolved5g.__version__

version = "0.1.4"
release = "0.0.1"


# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

