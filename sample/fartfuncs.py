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

def organize_releases(releases):
    '''
    Take dict of release data and return an ordered list of data for use in printing
    a summary.

    releases: dict of release data

    rreturns: list of lists
    '''
    organized = [
        ['ID', 'Artist', 'Title', 'Country', 'Date', 'Tracks(Media)'],
        ['--', '------', '-----', '-------', '----', '-------------']
    ]
    i = 0
    for release in releases:
        this_result = [
            str("[" + str(i) + "]"),
            str(release['artist-credit-phrase'] if 'artist-credit-phrase' in release else ''),
            str(release['title'] if 'title' in release else ''),
            str(release['release-event-list'][0]['area']['name'] if 'release-event-list' in release else ''),
            str(release['date'] if 'date' in release else ''),
            str(str((release['medium-track-count'] if 'medium-track-count' in release else 0)) + "(" + 
                str((release['medium-count'] if 'medium-count' in release else 0)) + ")")
        ]
        organized.append(this_result)
        i += 1
    return(organized)

def get_col_width_list(my_list, row_len):
    '''
    Return the given list of lists with an additional list of max lengths per index
    inserted at index 0.

    my_list: Given list of lists. All internal lists must be the same length
    row_len: Length of an internal list

    Returns: List of lists
    '''
    col_width = []
    for i in range(row_len):
        col_width.append(max(len(item[i]) for item in my_list) + 2)
    my_list.insert(0, col_width)
    return(my_list)

def print_cols(my_list):
    '''
    Prints the given list in a table with each sublist starting at index 1 as a row.
    Assumes index 0 contains the maximum length of the respective index in the other lists.

    my_list: The given list

    Returns: None
    '''
    for row in my_list[1:]:
        for col in row:
            print("".join(col.ljust(my_list[0][row.index(col)])), end='')
        print()

def print_releases(releases):
    '''
    Print individual release info

    releases: List of releases

    Return: None
    '''
    sorted_list = organize_releases(releases)
    sorted_list = get_col_width_list(sorted_list, len(sorted_list[0]))
    print_cols(sorted_list)
    return(len(sorted_list))

def main():
    # Define a useragent
    new_useragent()

    # Get artist/album
    artist = "Wardruna"
    album = "Runaljod Ragnarok"

    my_release = select_album(artist, album)
    print(my_release)

if __name__ == "__main__":
    main()