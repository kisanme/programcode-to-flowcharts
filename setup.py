
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Project to transpile a set of source code into flowcharts',
    'author': 'Nasik Shafeek <nasik2ms@gmail.com>',
    'url': 'nasik2ms@gmail.com',
    'download_url': 'Where to download it.',
    'author_email': 'nasik2ms@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['toflowcompiler'],
    'scripts': [],
    'name': 'toflowcompiler'
}

setup(**config)
