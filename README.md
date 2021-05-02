# FART
Foggy Album Rename Tool

Version 0.7a

python3 FART.py --help

# PURPOSE
FART can help to automate downloading music and renaming files. These are some of the currently working features:

- Integration with youtube-dl. Currently only outputs mp3
- Automatically query MusicBrainz for album info
- Automatic fuzzy matching of song title to file name
- Automatic renaming of matched files

This is intended only to make it easier to archive music you've paid for. FART is not intended to aid in music piracy and should not be used for such purposes.

# REQUIREMENTS

- python-Levenshtein - Levenshtein algorithm for fuzzy matching
- fuzzywuzzy - builds on Levenshtein
- musicbrainzngs - Python library for interacting with MusicBrainz Web API