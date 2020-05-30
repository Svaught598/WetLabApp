import os

from kivy.lang.builder import Builder

# Get project directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')

# List of paths for .kv files
TEMPLATE_PATHS = [
    os.path.join(ROOT_DIR, 'templates/navigation_drawer.kv'),

    os.path.join(ROOT_DIR, 'templates/film_view.kv'),
    os.path.join(ROOT_DIR, 'templates/update_view.kv'),
    os.path.join(ROOT_DIR, 'templates/volume_view.kv'),
    os.path.join(ROOT_DIR, 'templates/dilution_view.kv'),

    os.path.join(ROOT_DIR, 'templates/about_view.kv'),
]

# Main template built with by app.build() method
MAIN_TEMPLATE_PATH = os.path.join(ROOT_DIR, 'templates/main.kv')

# Path to license to be displayed in a popup
LICENSE_PATH = os.path.join(ROOT_DIR, 'LICENSE')

# Database Settings
DATABASE = 'db.sqlite3'

DEVELOPEMENT_KV = os.path.join(ROOT_DIR, 'templates/test.kv')

# Types of Solutions
SOLUTION_TYPES = [
    'w/w %', 'mg/mL', 'g/mL', 'M', 'mM', '\u03BCM', 'nM'
]

MASS_UNITS = [
    'kg', 'g', 'mg', '\u03BCg', 'ng'
]
