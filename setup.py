# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

def main() -> None:
    extra_files = package_files('./PyDFannots/templates')
    config_files = package_files('./default_cfg.json')
    setup(
        name='PyDFannots',
        version='0.1.1',
        description='PDF annotations extract using PyMuPDF',
        long_description=readme,
        author='Pedro Souza',
        author_email='pho.souza.mail@gmail.com',
        url='https://github.com/pho-souza/PyDFannots',
        license=license,
        packages=['PyDFannots'],
        package_dir={'PyDFannots': 'PyDFannots'},
        entry_points = {
            'console_scripts': [
                'pydfannots=PyDFannots.cli:main'
                ],
            },
        package_data={'PyDFannots': extra_files,
                      '': config_files},
        # data_files=[('PyDFannots/templates',['template_html.html'])],
        install_requires=['PyMuPDF','jinja2']
    )

if __name__ == '__main__':
    main()