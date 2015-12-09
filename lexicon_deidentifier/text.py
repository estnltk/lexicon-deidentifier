# -*- coding: utf-8 -*-
import os
import codecs
import logging

from six import string_types
from cached_property import cached_property
from estnltk import Text as EstnltkText
from estnltk.names import START, END, TEXT
from suffix_lemmatizer import SuffixLemmatizer

from . import util

log = logging.getLogger(__name__)

PII = 'pii'
default_dictionary = None


def get_default_dictionary():
    global default_dictionary
    if default_dictionary is None:
        default_dictionary = Dictionary.load_from_environment()
    return default_dictionary
    

class Text(EstnltkText):
    
    
    def __init__(self, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self.pii_dictionary = kwargs.get('pii_dictionary') or get_default_dictionary()
        
    
    @cached_property
    def layer_tagger_mapping(self):
        mapping = super(Text, self).layer_tagger_mapping
        mapping[PII] = self.tokenize_pii
        return mapping
    
    
    @cached_property
    def pii(self):
        """ A list of personally identifiable information in `pii` layer """
        if not self.is_tagged(PII):
            self.tokenize_pii()
        return self[PII]
    
    
    @cached_property
    def pii_texts(self):
        """The list of words representing ``pii`` layer elements."""
        if not self.is_tagged(PII):
            self.tokenize_pii()
        return [pii[TEXT] for pii in self[PII]]
    
    @cached_property
    def pii_spans(self):
        """The list of spans representing ``pii`` layer elements."""
        if not self.is_tagged(PII):
            self.tokenize_pii()
        return self.spans(PII)
    
    
    @cached_property
    def pii_starts(self):
        """The list of start positions representing ``pii`` layer elements."""
        if not self.is_tagged(PII):
            self.tokenize_pii()
        return self.starts(PII)
    
    
    @cached_property
    def pii_ends(self):
        """The list of end positions representing ``pii`` layer elements."""
        if not self.is_tagged(PII):
            self.tokenize_pii()
        return self.ends(PII)
    
    
    def tokenize_pii(self):
        """ Lookup entries in dictionary and add ``pii``-layer annontations."""
        self.pii_dictionary.process(self)
        


class Dictionary(object):
    
    
    def __init__(self, vocabulary, look_ahead, lower, use_suffix_lemmatizer):
        '''
        Loads vocabulary.
        
        Parameters
        ----------
        vocabulary: set or str
            
        look_ahead: int
            A number of tokens to check to compose phrases.
        lower: bool
            Convert text to lower-case for dictionary lookup
        use_suffix_lemmatizer: bool
            Use suffix lemmatizer to match a dictionary
        '''
        self.look_ahead = look_ahead
        self.lower = lower
        self.use_suffix_lemmatizer = use_suffix_lemmatizer
        
        if use_suffix_lemmatizer:
            self.suffix_lemmatizer = SuffixLemmatizer()
        
        if isinstance(vocabulary, set):
            self.vocabulary = vocabulary
        elif isinstance(vocabulary, string_types):
            self.vocabulary = Dictionary.load_transform_vocabulary(vocabulary)
        else:
            raise ValueError('Invalid vocabulary type: "{}"'.format(type(vocabulary)))
    
    
    @classmethod
    def load_from_environment(cls):
        c = util.read_configuraton()
        return cls(vocabulary=c.FILE, 
                   look_ahead=c.LOOK_AHEAD, 
                   lower=c.LOWER_CASE,
                   use_suffix_lemmatizer=c.USE_SUFFIX_LEMMATIZER)
    
    
    @classmethod
    def load_transform_vocabulary(cls, fnm):
        if not fnm.endswith('.voc'):
            fnm = fnm + '.voc'
        if not os.path.exists(fnm):
            log.debug('File {} not found. Running transformation ...'.format(fnm))
            util.transform_vocabulary()
        with codecs.open(fnm, encoding='utf8') as f:
            vocabulary = set(ln.rstrip() for ln in f)
        log.debug('Loaded vocabulary from file "{}"'.format(fnm))
        return vocabulary
    
    
    def process(self, text):
        ''' Process estnltk text. '''
        look_ahead = self.look_ahead
        words = text.words
        lemmas = text.lemmas
        if self.lower:
            lemmas = [lemma.lower() for lemma in lemmas]
        
        if self.use_suffix_lemmatizer:
            suf_lemmas = [self.suffix_lemmatizer(w.lower()) for w in text.word_texts]
        
        dicts = []
        for i in range(len(lemmas)):
            for j in range(min(i + look_ahead, len(lemmas)), i, -1):
                phrase = " ".join(lemmas[i:j])
                if phrase in self.vocabulary:
                    dicts.append({START: words[i][START], 
                                  END: words[j-1][END],
                                  TEXT:phrase})
                    break
                else:
                    if self.use_suffix_lemmatizer:
                        suf_phrase = " ".join(suf_lemmas[i:j])
                        if suf_phrase != phrase and suf_phrase in self.vocabulary:
                            dicts.append({START: words[i][START], 
                                          END: words[j-1][END],
                                          TEXT:phrase})
                            break
        text[PII] = dicts
