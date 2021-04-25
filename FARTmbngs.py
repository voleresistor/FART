#!/usr/bin/python

import musicbrainzngs

def new_useragent():
    '''
    Define a useragent for use with MusicBrainzNGS queries

    return: None
    '''
    appName = 'FoggyAlbumRenameTool(FART)'
    appVersion = '0.6a'
    appContact = 'FoggyAlbumRename@trvm.xyz'
    musicbrainzngs.set_useragent(appName, appVersion, appContact)

def select_album(_artist, _album):
    '''
    Guides user through querying and selecting the correct release to match against

    _artist: The artist to search for
    _album: The album to search for

    return: dict
    '''
    # Select release ID from release groups
    _releases = get_releases(_artist, _album)
    _selection = get_user_selection(print_releases(_releases['release-list']))
    _rid = _releases['release-list'][_selection]['id']

    _release_data = get_release_data(_rid)
    return(_release_data)

def get_user_selection(_count):
    '''
    Get index selection from user in response to a list of options

    _count: The number of items to choose from

    return: int
    '''
    if _count == 1:
        return(0)

    while True:
        _selection = input("\r\nSelect a release [0-{} | q to quit]: ".format(_count - 1))
        if _selection.lower() in ['q', 'quit']:
            print("Exiting...")
            exit(0)
        elif int(_selection) in range (_count):
            return(int(_selection))
        else:
            print("Invalid selection. Please try again.")
    return(0)

def get_releases(_artist, _album, _limit=0):
    '''
    Query MusicBrainz a second time for all releases in the selected release group

    _artist: Artist to search for
    _album: Album to search for
    _limit: Limit the number of returned items

    return: str
    '''
    _result = musicbrainzngs.search_releases(artist=_artist, release=_album, limit=_limit)
    return(_result)

def get_release_data(_rid):
    '''
    Get data on a specific release

    _rid: ID of selected release

    return: dict
    '''
    _includes = [
        'labels',
        'discids',
        'recordings',
        'media'
    ]
    _result = musicbrainzngs.get_release_by_id(_rid, includes=_includes)
    return(_result)

def organize_releases(_releases):
    '''
    '''
    _organized = []
    _i = 0
    for _release in _releases:
        _this_result = {
            'id': "[" + str(_i) + "]",
            'artists': (_release['artist-credit-phrase'] if 'artist-credit-phrase' in _release else '-'),
            'title': (_release['title'] if 'title' in _release else '-'),
            'country': (_release['release-event-list'][0]['area']['name'] if 'release-event-list' in _release else '-'),
            'date': (_release['date'] if 'date' in _release else '-'),
            'counts': str((_release['medium-track-count'] if 'medium-track-count' in _release else 0)) + "(" + 
                str((_release['medium-count'] if 'medium-count' in _release else 0)) + ")"
        }
        _organized.append(_this_result)
        _i += 1
    return(_organized)

def get_col_widths(_sorted_list):
    '''
    '''
    _col_widths = []
    for _key in _sorted_list[0]:
        _col_widths.append(max(len(_release[_key]) for _release in _sorted_list) + 2)
    return(_col_widths)

def print_releases(_releases):
    '''
    Print individual release info

    _releases: List of releases
    '''
    _sorted_list = organize_releases(_releases)
    _result_count = len(_sorted_list)
    _col_widths = get_col_widths(_sorted_list)

    for _row in _sorted_list:
        print("{}{}{}{}{}{}".format(
            "".join(_row['id'].ljust(_col_widths[0])),
            "".join(_row['artists'].ljust(_col_widths[1])),
            "".join(_row['title'].ljust(_col_widths[2])),
            "".join(_row['country'].ljust(_col_widths[3])),
            "".join(_row['date'].ljust(_col_widths[4])),
            "".join(_row['counts'].ljust(_col_widths[5]))
        ))
    return(_result_count)

#if __name__ == "__main__":
#    # Define a useragent
#    new_useragent()
#
#    # Get artist/album
#    artist = "Wardruna"
#    album = "Runaljod Ragnarok"
#
#    # Get releases
#    #release_id_list = get_release_groups(artist, album)
#    #for release_id in release_id_list:
#    #    print(u"Selected ID: {}".format(release_id))
#    #album_data = select_album(artist, album)
#    #print(album_data)
#
#    my_release = select_album(artist, album)
#    print(my_release)