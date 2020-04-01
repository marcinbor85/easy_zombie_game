import os
import sys
from setuptools import setup, find_packages

from ezg import __version__, __appname__, __description__

def read(fname):
    content = ''
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        content = f.read()
    return content

setup(
    name = __appname__,
    version = __version__,
    author = "Marcin Borowicz",
    author_email = "marcinbor85@gmail.com",
    description = (__description__),
    license = "MIT",
    keywords = "zombie python pygame sdl framework game",
    url = "https://github.com/marcinbor85/easy_zombie_game",
    packages = find_packages(exclude=['tests', 'tests.*']),
    include_package_data = True,
    long_description = read('DESCRIPTION'),
    install_requires = [
        "pygame==2.0.0.dev6",
    ],
    entry_points = {
        'console_scripts': [
            'ezg = ezg.main:run',
        ]
    },
)
