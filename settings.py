import os

from kivy.lang.builder import Builder

# Get project directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')

# List of paths for .kv files
TEMPLATE_PATHS = [
    os.path.join(ROOT_DIR, 'templates\\film_view.kv'),
    os.path.join(ROOT_DIR, 'templates\\update_data_screen.kv'),
    os.path.join(ROOT_DIR, 'templates\\navigation_drawer.kv'),
    os.path.join(ROOT_DIR, 'templates\\volume_view.kv')
]

# Main template built with by app.build() method
MAIN_TEMPLATE_PATH = os.path.join(ROOT_DIR, 'templates\\main.kv')

# Database Settings
DATABASE = 'db.sqlite3'

DEVELOPEMENT_KV = os.path.join(ROOT_DIR, 'templates\\test.kv')

# Types of Solutions
SOLUTION_TYPES = [
    '% Wt/Wt',
    '% Wt/Vol',
]
