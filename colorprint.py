#!/usr/bin/python

import FARTmbngs

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
        _col_widths.append(max(len(_release[_key]) for _release in _sorted_list)) + 2
    return(_col_widths)

def print_releases(_releases):
    '''
    Print individual release info

    _release_ids: List of 
    '''
    _sorted_list = organize_releases(_releases)
    _result_count = len(_sorted_list)
    _col_widths = get_col_widths(_sorted_list)
    
    for _row in _sorted_list:
        print("{}{}{}{}{}{}".format(
            join(_row['id'].ljust(_col_widths[0])),
            join(_row['artists'].ljust(_col_widths[1])),
            join(_row['title'].ljust(_col_widths[2])),
            join(_row['country'].ljust(_col_widths[3])),
            join(_row['date'].ljust(_col_widths[4])),
            join(_row['counts'].ljust(_col_widths[5]))
        ))
    return(_result_count)

FARTmbngs.new_useragent()

artist = 'Carbon Based Lifeforms'
album = 'Hydroponic Garden'

_releases = FARTmbngs.get_releases(artist, album)
print_releases(_releases['release-list'])