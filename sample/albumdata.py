from trackdata import TrackData

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