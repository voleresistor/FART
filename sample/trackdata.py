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