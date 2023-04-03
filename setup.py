# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pdfannot',
    version='0.1.0',
    description='PDF annotations extractor using PyMuPDF',
    long_description=readme,
    author='Pedro Souza',
    author_email='pho.souza.mail@gmail.com',
    url='https://github.com/pho-souza/PyDFNotesExtractor',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

