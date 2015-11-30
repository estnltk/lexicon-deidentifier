# -*- coding: utf-8 -*-
import unittest
from text import Text, Dictionary


class TestText(unittest.TestCase):
    
    def test(self):
        vocabulary=set([u'tõnu tamm', u'tõnu'])
        pii_dictionary = Dictionary(vocabulary=vocabulary, look_ahead=2, lower=True, use_suffix_lemmatizer=True)
        t = Text(u'Tõnu Tamm alguses ja lõpus Tõnu', 
                 pii_dictionary=pii_dictionary)
        self.assertTrue(u'tõnu tamm' in t.pii_texts)
        self.assertTrue(u'tõnu' in t.pii_texts)
        self.assertEquals(t.pii_starts, [0, 0, 27])
        self.assertEquals(t.pii_ends, [4, 9, 31])
        self.assertEquals(t.pii_spans, zip(t.pii_starts, t.pii_ends))
