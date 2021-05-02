#!/usr/bin/python

class AlbumData:
    def __init__(self, artist, album, release_data=None):
        self.Album = album
        self.Artist = artist
        self.TrackCount = 0
        self.Date = None
        self.Media = []
        self.MediaCount = 0

        if release_data:
            self.Date = release_data['date']
            for medium in release_data['medium-list']:
                self.new_media()
                for track in medium['track-list']:
                    new_track = TrackData(
                        track['recording']['title'],
                        artist,
                        track['number'],
                        medium['position'])
                    self.add_track(new_track)

    def print_album(self):
        print(u"Album: {}\r\nArtist: {}\r\nMedia Count: {}\r\nTrack Count: {}\r\nRelease Date: {}".format(
            self.Album, self.Artist, self.MediaCount, self.TrackCount, self.Date
        ))

    def get_artist(self):
        return self.Artist
    
    def get_album(self):
        return self.Album

    def get_media_count(self):
        return self.MediaCount

    def get_track_count(self):
        return self.TrackCount

    def get_date(self):
        return self.Date

    def new_media(self):
        self.MediaCount += 1
        self.Media.append({
            'MediaNumber': self.MediaCount,
            'TrackCount': 0,
            'TrackList': []
        })

    def add_track(self, track):
        media_idx = int(track.DiscNumber) - 1
        if media_idx not in range(self.MediaCount):
            print("Warning: Media doesn't exist!")
            return None
        self.Media[media_idx]['TrackList'].append(track)
        self.Media[media_idx]['TrackCount'] += 1
        self.TrackCount += 1
    
    def print_media_tracks(self, media_num):
        media_idx = media_num - 1
        if media_idx not in range(self.MediaCount):
            print("Can't find requested media")
            return None
        print(u"Media Number: {}".format(self.Media[media_idx]['MediaNumber']))
        for track in self.Media[media_idx]['TrackList']:
            track.print_track()

    def print_all_tracks(self):
        for media in self.Media:
            self.print_media_tracks(media['MediaNumber'])

    def get_report(self):
        '''
        Get report on tracks and matching files

        return: list
        '''
        match_report = [
            ['TrackNumber', 'Title', 'File', 'MatchPercent'],
            ['-----------', '-----', '----', '------------']
        ]
        for _media in self.Media:
            for _track in _media['TrackList']:
                this_match = [
                    str(_track.get_track_number()),
                    str(_track.get_track_title()),
                    str(_track.get_file_name()),
                    str(_track.get_match_pct())
                ]
                match_report.append(this_match)
        return(match_report)


class TrackData:
    def __init__(self, title=None, artist=None, number=0, disc=0, match_data=[]):
        self.Title = title
        self.Artist = artist
        self.TrackNumber = number
        self.DiscNumber = disc
        self.MatchData = match_data
        self.NewName = None
        self.FileName = None
        self.MatchPct = None

    def add_match(self, _file_name, _match_pct):
        '''
        Add match data, including new name to this object

        _file_name: Matching file name to be renamed
        _match_pct: Percentage of confidence in the match

        return: None
        '''
        self.FileName = _file_name
        self.MatchPct = _match_pct
        self.NewName = self.clean_str(self.new_name())

    def new_name(self):
        '''
        Generate a new file name based on track data and the existing file

        returns: string
        '''
        _disc_number = str(self.get_track_disc()).zfill(2).rstrip()
        _track_number = str(self.get_track_number()).zfill(2).rstrip()
        _track_title = self.get_track_title().rstrip()
        _extension = self.get_file_name().split('.')[-1]
        return (_disc_number + '_' + _track_number + '_' + _track_title + '.' + _extension).rstrip()

    def clean_str(self, _strin):
        '''
        Clean up Windows and Linux reserved characters to make filenames compatible
        with either.

        return: string
        '''
        # These chars should cover the Windows and Linux reserved characters
        _illegal_chars = ['/', '<', '>', ':', '"', '\\', '|', '?', '*', '!']
        _clean = False
        while not _clean:
            for c in _strin:
                if c in _illegal_chars:
                    #print("Stripping {}".format(c))
                    _strin = _strin.replace(c, '')
                    continue
            _clean = True
        return _strin

    def print_track(self):
        print(u"\t{} - {} - {}".format(
                str(self.DiscNumber).zfill(2), str(self.TrackNumber).zfill(2), self.Title
            ))

    def get_track_title(self):
        return self.Title
    
    def get_track_artist(self):
        return self.Artist

    def get_track_number(self):
        return self.TrackNumber

    def get_track_disc(self):
        return self.DiscNumber

    def get_file_name(self):
        return self.FileName

    def get_new_name(self):
        return self.NewName

    def get_match_pct(self):
        return self.MatchPct
