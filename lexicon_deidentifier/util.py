# -*- coding: utf-8 -*-
import os
import sys
import codecs
import logging
from collections import namedtuple

import unicodecsv
from six.moves import configparser

log = logging.getLogger(__name__)
Config = namedtuple('Config', ['FILE', 'LOOK_AHEAD', 'LOWER_CASE', 
                               'FLIP_WORDS', 'WORD_SEPARATORS', 
                               'USE_SUFFIX_LEMMATIZER'])

def read_configuraton():
    """Reads configuration file defined by an environment variable CONFIG"""
    try:
        config_dir = os.environ['LD_CONFIG']
    except KeyError as e:
        print('Environment variable "LD_CONFIG" not defined.')
        sys.exit(0)
    
    if not os.path.exists(config_dir):
        print('Environment variable "LD_CONFIG" points to a non-existent directory "{}".'.format(config_dir))
        sys.exit(0)
    
    config_file = os.path.join(config_dir, 'settings.conf')
    
    log.debug('Lexicon-Deidentifier:\nConfiguration:"{}"\nSettings:\n{}'.format(config_dir,
                                                                          open(config_file).read()))
    config = configparser.ConfigParser()
    config.read(config_file)
    
    return Config(FILE=os.path.join(config_dir, 'names.txt'),
                  LOOK_AHEAD=config.getint('DICTIONARY', 'LOOK_AHEAD'),
                  LOWER_CASE=config.getboolean('DICTIONARY', 'LOWER_CASE'),
                  FLIP_WORDS=config.getboolean('DICTIONARY','FLIP_WORDS'),
                  WORD_SEPARATORS=list(config.get('DICTIONARY', 'WORD_SEPARATORS')[1:-1]),
                  USE_SUFFIX_LEMMATIZER=config.getboolean('DICTIONARY','USE_SUFFIX_LEMMATIZER')
                  )


def transform_vocabulary():
    """Transforms user-provided vocabulary using configuration settings."""
    c = read_configuraton()
    
    def generate_transformations(first_name, last_name):
        first_name = first_name.lower() if c.LOWER_CASE else first_name
        last_name = last_name.lower() if c.LOWER_CASE else last_name
        for ws in c.WORD_SEPARATORS:
            variant = first_name + ws + last_name
            yield variant
            if c.FLIP_WORDS:
                variant = last_name + ws + first_name
                yield variant
    
    outf = codecs.open(c.FILE + '.voc', 'w', encoding='utf8')
    
    log.debug('Converting dictionary file "{}" to "{}"'.format(c.FILE, outf.name))
    
    reader = unicodecsv.reader(open(c.FILE, 'rb'), delimiter=',', encoding='utf-8')
    reader.next()
    for row in reader:
        first_name = row[0] 
        last_name = row[1]
        if first_name == u'*':
            outf.write(last_name.lower() if c.LOWER_CASE else last_name)
            outf.write('\n')
        elif last_name == u'*':
            outf.write(first_name.lower() if c.LOWER_CASE else first_name)
            outf.write('\n')
        else:
            for variant in generate_transformations(first_name, last_name):
                outf.write(variant)
                outf.write('\n')
    outf.close()
