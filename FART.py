#!/usr/bin/python
# FART.py: Read in data from a JSON file and rename audio files using fuzzy matching
#
# REQUIREMENTS (Can be installed via pip)
#	python-Levenshtein - Levenshtein algorithm for fuzzy matching
#	fuzzywuzzy - builds on Levenshtein
#	musicbrainzngs - Python library for interacting with MusicBrainz Web API
#
#	pip install python-Levenshtein fuzzywuzzy musicbrainzngs
#
# TODO: GUI front end using PyGObject?
# TODO: Option to allow automatic rename of entire collection? YIKES
# TODO: Debug and test options?
# TODO: Load an external config file that maintains defaults like music folder root?
# TODO: Allow editing of matches?
# TODO: Major code review. Simplify and deobfuscate - ongoing
# TODO: Pretty up output with spacing and maybe colors
#
# BUG: Script fails when accessing non-existent keys in source dicts
# BUG: -y switch not universal

import json, sys, getopt, subprocess, FARTmbngs
from os import listdir, rename, path, makedirs
from os.path import isfile, join
from fuzzywuzzy import process
from FARTClasses import AlbumData, TrackData		# Custom classes

# ======== Functions ========
# get_help
def get_help(_help_type):
    '''
    Simple help file with syntax and usage notes

    _help_type: [short|full] determines how much help to display
    '''
    print('FART.py: v0.6a\r\n')
    print('Usage: FART.py -a <artist> -l <album> [ -r  <root path> | -h | -t | -i ]\r\n')

    if _help_type == 'full':
        print('Options:')
        print('   -a --artist\t\tThe name of the artist.')
        print('   -l --album\t\tThe name of the album.')
        #print('   -j --json_file\tAlternate file path to JSON data.')
        print('   -r --music_root\tPath to the directory in which the artist directory resides.')
        print('   -t --report_only\tDo not perform renames.')
        print('   -i --ignore_warn\tIgnore warnings and attempt to process album anyway.')
        print('   -u --youtube-dl\tURL to Youtube Music album to download using youtube-dl.')
        print('   --min_match\t\tMinimum match percentage for fuzzy matching. Must be between 0-100.')
        print('   -y\t\t\tDo not request change confirmation prior to rename.')
        print('   -h --help\t\tPrint this help file.')
    else:
        print('For full help, run FART.py [-h | --help]\r\n')

# get_options
def get_options(_args):
    '''
    '''
    _options = {
        'music_root': '.',
        'album': None,
        'artist': None,
        'json_file': None,
        'response': False,
        'report_only': False,
        'ignore_warn': False,
        'min_match_pct': 75,
        'youtube-dl': None
    }

    _opts, _argv = getopt.getopt(_args, 'a:l:j:r:u:htiy', \
    ['artist=', 'album=', 'json_file=', 'music_root=', 'min_match=', 'youtube-dl=', 'help', 'report_only','ignore_warn'])
    for _opt, _arg in _opts:
        if _opt in ['-h', '--help']:
            get_help('full')
            exit()
        elif _opt in ['-l', '--album']:
            _options['album'] = _arg
        elif _opt in ['-a', '--artist']:
            _options['artist'] = _arg
        elif _opt in ['-j', '--json_file']:
            #_options['json_file'] = _arg
            continue
        elif _opt in ['-r', '--music_root']:
            _options['root'] = _arg
        elif _opt in ['-t', '--report_only']:
            print('Running in report only mode. No changes will be made.')
            _options['report_only'] = True
        elif _opt in ['-i', '--ignore_warn']:
            _options['ignore_warn'] = True
        elif _opt in ['-u', '--youtube-dl']:
            _options['youtube-dl'] = _arg
        elif _opt in ['-y']:
            _options['response'] = True
        elif _opt in ['--min_match']:
            if int(_arg) in range(100):
                _options['min_match_pct'] = int(_arg)
            else:
                print('Min match percent must be between 0-100.')
                exit(1)
        else:
            get_help('short')
            exit()
    
    return _options

# load_json
def load_json(__album_data, _music_root, _artist_name, _album_name):
    '''
    Load album data JSON file. If no file is given, assume a
    standard path like "Artist Name/artistname-albumname.json"	
    _album_data: path and file name of JSON file
    _music_root: Root directory that albums are stored in
    _artist_name: Directory name of artist
    _album_name: Directory name of album
    '''
    if _album_data == None:
        _album_data = _music_root + '/' + _artist_name + '/' +	_artist_name.lower().replace(' ', '') + '-' + \
            _album_name.lower().replace(' ', '') + '.json'
        
    if not path.exists(_album_data):
        print('ERROR: JSON file not present or not readable: {}'.format(_album_data))
        exit(1)

    with open(_album_data, 'r') as jd:
        return json.load(jd)

# confirm_response
def confirm_response(_message):
    '''
    '''
    # Confirm low confidence match with user
    _response = input(_message)
    print() # Spacing for readability in console
    if _response.lower() in ['y', 'yes']:
        return True
    return False

# rename_track
def rename_track(_track, _root):
    '''
    Rename a given track using data queried from the object

    _track: The TrackData object
    _root: The folder root of tthe files being renamed

    return: None
    '''
    print('Renaming:\r\n\t{}\r\n\t{}\r\n'.format(_track.get_file_name(), _track.get_new_name()))
    rename(_root + '/' + _track.get_file_name(), _root + '/' + _track.get_new_name())

# get_local_files
def get_local_files(_album_path):
    '''
    '''
    return [_t for _t in listdir(_album_path) if isfile(join(_album_path, _t))]

# match_track
def match_track(_min_match_pct, _track_title, _file_list):
    '''
    Use fuzzy logic to match track names from the given _file_list to the given _track_title
    from the data dict.

    _min_match_pct: Minimum confidence percentage to consider a match
    _track_title: Title of the track from dict
    _file_list: List of files gathered from the local repository
    '''
    _new_match = None
    _song_matches = process.extract(_track_title, _file_list)
    for _match in _song_matches:
        if _match[1] > _min_match_pct:
            _new_match = {
                'FileName': _match[0],
                'MatchPct': _match[1]
            }
        else:
            print('\tNo definitive match for: {}'.format(_track_title))
            print('\tFirst match: {}: {}'.format(_match[0], _match[1]))
            _response = input("Confirm this match? [y/N/q]: ").lower()

            if _response in ['q', 'quit']:
                print("Exiting...")
                exit(1)
            elif _response in ['y', 'yes']:
                _new_match = {
                    'FileName': _match[0],
                    'MatchPct': _match[1]
                }
        if _new_match != None:
            return(_new_match)

    # No matches. Warn and exit cleanly
    print("No matches found for {}. Exiting...".format(_track_title))
    exit(1)

# get_album_path
def get_album_path(_music_root, _artist_name, _album_name):
    '''
    Build and verify an album path using provided parameters

    _music_root: Root directory that albums are stored in
    _artist_name: Directory name of artist
    _album_name: Directory name of album
    '''
    _new_path = _music_root + '/' + _artist_name + '/' + _album_name
    if not path.isdir(_new_path):
        create_album_path(_new_path)
        #print('ERROR: album path not found: {}'.format(_new_path))
        #exit(1)

    return _new_path

# create_album_path
def create_album_path(_path):
    '''
    Create album path.

    _path: Path to create recursively

    return: None
    '''
    print("Creating new directory: {}".format(_path))
    try:
        makedirs(_path, exist_ok=True)
        print("Created non-existant directory: {}".format(_path))
    except OSError as error:
        print("ERROR: Couldn't create directory: {}".format(_path))
        exit(1)

# Hide main vars from global scope by defining a separate main() function
def main():
    # Process command line arguments
    opts = get_options(sys.argv[1:])
    if opts['album'] == None or opts['artist'] == None:
        print('ERROR: Please specify both artist and album.\r\n')
        get_help('short')
        exit(1)

    # Test album path and create if necessary
    opts['album_path'] = get_album_path(opts['music_root'], opts['artist'], opts['album'])

    # Download the files using youtube-dl
    if opts['youtube-dl']:
        # Download
        ytdl_opts = "-x -f 251 " + opts['youtube-dl']
        ytdl = subprocess.run(['youtube-dl', "-x", "--audio-format", "mp3", opts['youtube-dl']], cwd=opts['album_path'])
        if ytdl.check_returncode():
            print("ERROR: There was a problem with the download.")
            exit(1)

    # Get local file listing
    files = get_local_files(opts['album_path'])

    # If a JSON file wasn't given then get data from MusicBrainz
    # BUG: JSON isn't supported anymore but will be again
    if not opts['json_file']:
        # Set up our user agent string and query MusicBrainz
        FARTmbngs.new_useragent()
        album_info = FARTmbngs.select_album(opts['artist'], opts['album'])
        my_album = AlbumData(opts['artist'], opts['album'], album_info['release'])
    else:
        # Load JSON file
        album_info = load_json(opts['json_file'], opts['root'], opts['artist'], opts['album'])
        print("JSON not currently supported in this version.")
        exit(1)

    # Verify that folder contains same number of songs as album info
    if my_album.get_track_count() != len(files):
        print("WARNING: album data and file count mismatch.\r\n")
        if not opts['ignore_warn']:
            exit(1)


    # Loop through CDs and tracks to build a database
    for medium in my_album.Media:
        for track in medium['TrackList']:
            this_match = match_track(
                opts['min_match_pct'],
                track.get_track_title(),
                files
            )
            track.add_match(this_match['FileName'], this_match['MatchPct'])

    # Always print a report
    my_album.print_report()
    if opts['report_only']:
        exit(0)

    # Only carry on if we're in full destroy files mode
    if opts['response'] or confirm_response('Continue renaming? [y/N]: '):
        for media in my_album.Media:
            for track in media['TrackList']:
                rename_track(track, opts['album_path'])
    else:
        print('Canceling changes...\r\n')

# main process
if __name__ == "__main__":
    main()
    exit(0)