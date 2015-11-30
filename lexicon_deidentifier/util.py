# -*- coding: utf-8 -*-
import os
import sys
import codecs
import logging

import unicodecsv
from six.moves import configparser

log = logging.getLogger(__name__)


def read_configuraton():
    """Reads configuration file defined by an environment variable CONFIG"""
    try:
        config_file_name = os.environ['DI_CONFIG']
    except KeyError as e:
        print('Environment variable "DI_CONFIG" not defined.')
        sys.exit(0)
    
    if not os.path.exists(config_file_name):
        print('Environment variable "DI_CONFIG" points to a non-existent file "{}".'.format(config_file_name))
        sys.exit(0)
    
    log.debug('Configuration file: "{}"'.format(config_file_name))
    log.debug('Settings:\n{}'.format(open(config_file_name).read()))
    
    config = configparser.ConfigParser()
    config.read(config_file_name)
    return config


def transform_vocabulary():
    """Transforms user-provided vocabulary using configuration settings."""
    config = read_configuraton()
    LOWER_CASE = config.getboolean('DICTIONARY', 'LOWER_CASE')
    FILE = config.get('DICTIONARY', 'FILE')
    FLIP_WORDS = config.getboolean('DICTIONARY','FLIP_WORDS')
    WORD_SEPARATORS = list(config.get('DICTIONARY', 'WORD_SEPARATORS')[1:-1])
    
    def generate_transformations(first_name, last_name):
        first_name = first_name.lower() if LOWER_CASE else first_name
        last_name = last_name.lower() if LOWER_CASE else last_name
        for ws in WORD_SEPARATORS:
            variant = first_name + ws + last_name
            yield variant
            if FLIP_WORDS:
                variant = last_name + ws + first_name
                yield variant
    
    outf = codecs.open(FILE + '.voc', 'w', encoding='utf8')
    
    log.debug('Converting dictionary file "{}" to "{}"'.format(FILE, outf.name))
    
    reader = unicodecsv.reader(open(FILE, 'rb'), delimiter=' ', encoding='utf-8')
    reader.next()
    for row in reader:
        first_name = row[0] 
        last_name = row[1]
        if first_name == u'*':
            outf.write(last_name.lower() if LOWER_CASE else last_name)
            outf.write('\n')
        elif last_name == u'*':
            outf.write(first_name.lower() if LOWER_CASE else first_name)
            outf.write('\n')
        else:
            for variant in generate_transformations(first_name, last_name):
                outf.write(variant)
                outf.write('\n')
    outf.close()
