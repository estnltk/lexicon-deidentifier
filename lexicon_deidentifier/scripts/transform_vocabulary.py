#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from .. import util


def main():
    logging.basicConfig(level=logging.DEBUG)
    util.transform_vocabulary()

    
if __name__ == '__main__':
    main()
