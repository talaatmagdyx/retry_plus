# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = 'retry_plus'
copyright = '2024, talaatmagdyx'
author = 'talaatmagdyx'
release = '1.0.4'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
    'myst_parser',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.extlinks',
]

# Configuration for the MyST parser to enable Markdown support
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "substitution",
    "tasklist",
]

# Enable todo items
todo_include_todos = True

# Intersphinx configuration to link to other project's documentation
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# Paths for templates and static files
templates_path = ['_templates']
html_static_path = ['_static']

# Patterns to exclude
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'

# -- Options for Autodoc -----------------------------------------------------
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'show-inheritance': True,
}

# -- Options for Autosummary -------------------------------------------------
autosummary_generate = True

# -- Options for Extlinks ----------------------------------------------------
extlinks = {
    'issue': ('https://github.com/talaatmagdyx/retry_plus/issues/%s', 'issue %s'),
    'pr': ('https://github.com/talaatmagdyx/retry_plus/pull/%s', 'PR %s'),
}

# -- Options for Sphinx-GitHub Pages -----------------------------------------
html_baseurl = 'https://talaatmagdyx.github.io/retry_plus/'

# -- Options for Napoleon ----------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Source file suffixes
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}
