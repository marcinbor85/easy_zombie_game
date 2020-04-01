import os
import logging

from ezg.engine import config

config['ASSETS_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
