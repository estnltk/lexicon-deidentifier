#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name = 'lexicon-deidentifier',
    description = "A wrapper over the Estnltk's Text class, which extracts personally identifiable information (PII) from text.",
    version = '1.0.0',
    dependency_links = [
        'https://github.com/estnltk/suffix-lemmatizer/tarball/master#egg=suffix_lemmatizer-1.0.0'
    ],
    install_requires = [
        'estnltk==1.3', 
        'unicodecsv==0.14.1',
        'six==1.9.0',
        'suffix-lemmatizer==1.0'],
    author = 'Alexander Tkachenko',
    author_email='alex.tk.fb@gmail.com',
    packages = find_packages(),
    license='GNU GPL version 2',
    entry_points = {
        'console_scripts': [
          'transform_vocabulary=lexicon_deidentifier.scripts.transform_vocabulary:main',
         ]
    }
)
