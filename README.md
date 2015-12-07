# lexicon-deidentifier
Lexicon-deidentifier provides a wrapper over the Estnltk's Text class, 
which extracts personally identifiable information (PII) from text based on
user-provided lexicon.

## Installation
```
git clone https://github.com/estnltk/lexicon-deidentifier.git
cd lexicon-deidentifier
pip install -r requirements.txt
```

##Usage
Create a catalog containing files names.txt and settings.conf

`names.txt` file format:
```
first_name,last_name
tõnu,tamm
tõnu,*
```

`settings.conf` file format:
```
[DICTIONARY]
LOOK_AHEAD=3
LOWER_CASE=True
FLIP_WORDS=False
WORD_SEPARATORS=' '
USE_SUFFIX_LEMMATIZER=True
```

Setup an environment variable `LD_CONFIG` to point to the configuration catalog:
```
export LD_CONFIG=<full path to the configuration catalog>
```

Extract PII entities using estnltk-like interface:
```python
> from lexicon_deidentifier import Text
> text = Text(u'Tõnu Tamm lause alguses ja lõpus Tõnu')
> text.pii
[{u'end': 4, u'start': 0, u'text': u'tõnu'},
 {u'end': 9, u'start': 0, u'text': u'tõnu tamm'},
 {u'end': 37, u'start': 33, u'text': u'tõnu'}]
```
