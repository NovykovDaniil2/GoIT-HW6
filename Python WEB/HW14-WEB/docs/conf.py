import sys
import os

from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath('..'))
project = 'GoIT-RestAPI'
copyright = '2023, Daniil Novykov'
author = 'Daniil Novykov'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']