import os

from kivy.lang.builder import Builder

# Get project directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')

# List of paths for .kv files
TEMPLATE_PATHS = [
    os.path.join(ROOT_DIR, 'templates\\film_thickness_screen.kv'),
    os.path.join(ROOT_DIR, 'templates\\update_data_screen.kv'),
    os.path.join(ROOT_DIR, 'templates\\volume_needed_screen.kv'),
    os.path.join(ROOT_DIR, 'templates\\navigation_drawer.kv'),
]

MAIN_TEMPLATE_PATH = os.path.join(ROOT_DIR, 'templates\\main.kv')