# lexicon-deidentifier
Lexicon-deidentifier provides a wrapper over the Estnltk's Text class, 
which extracts personally identifiable information (PII) from text. 

## Installation
```
git clone https://github.com/estnltk/lexicon-deidentifier.git
cd lexicon-deidentifier
python setup.py install
```

##Usage
Create a file listing PII entities, e.g.
```
first_name last_name
tõnu tamm
tõnu *
```

Edit a configuration file settings.conf:
```
[DICTIONARY]
FILE=<full path to the PII file>
LOOK_AHEAD=3
LOWER_CASE=True
FLIP_WORDS=False
WORD_SEPARATORS=' '
USE_SUFFIX_LEMMATIZER=True
```

Setup an environment variable DI_CONFIG to point to the configuration file:
```
export DI_CONFIG=<full path to the configuration file>
```

Extract PII entities:
```python
> from lexicon_deidentifier import Text
> text = Text(u'Tõnu Tamm lause alguses ja lõpus Tõnu')
> text.pii
[{u'end': 4, u'start': 0, u'text': u'tõnu'},
 {u'end': 9, u'start': 0, u'text': u'tõnu tamm'},
 {u'end': 37, u'start': 33, u'text': u'tõnu'}]
```
