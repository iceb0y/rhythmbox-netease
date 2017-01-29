from gi.repository import GObject, RB, Peas
from rhythmbox_netease.api import playlist_detail, song_enhance_player_url

class NeteasePlugin(GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(NeteasePlugin, self).__init__()
        self.sources = list()

    def do_activate(self):
        shell = self.object
        page_group = RB.DisplayPageGroup.get_by_id('netease-playlist')
        if not page_group:
            page_group = RB.DisplayPageGroup.new(
                shell=shell, id='netease-playlist', name='Netease Playlist',
                category=RB.DisplayPageGroupCategory.TRANSIENT)
        shell.append_display_page(page_group, None)
        source = GObject.new(NeteasePlaylistSource, shell=shell,
                             entry_type=NeteaseEntryType(), name='Playlist')
        source.id = 108891640
        self.sources.append(source)
        shell.append_display_page(source, page_group)

    def do_deactivate(self):
        for source in reversed(self.sources):
            source.delete_thyself()
        del self.sources[:]

class NeteasePlaylistSource(RB.BrowserSource):
    def __init__(self):
        RB.BrowserSource.__init__(self)
        self.loaded = False

    def do_selected(self):
        if not self.loaded:
            db = self.props.shell.props.db
            result = playlist_detail(self.id, 1000)
            assert result['code'] == 200
            self.props.name = result['playlist']['name']
            for index, track in enumerate(result['playlist']['tracks']):
                entry = RB.RhythmDBEntry.new(db, NeteaseEntryType(), str(track['id']))
                db.entry_set(entry, RB.RhythmDBPropType.TRACK_NUMBER, index)
                db.entry_set(entry, RB.RhythmDBPropType.TITLE, track['name'])
                db.entry_set(entry, RB.RhythmDBPropType.ARTIST, track['ar'][0]['name'])
                db.entry_set(entry, RB.RhythmDBPropType.ALBUM, track['al']['name'])
                db.entry_set(entry, RB.RhythmDBPropType.DURATION, track['dt'] / 1000)
            db.commit()
            self.loaded = True

class NeteaseEntryType(RB.RhythmDBEntryType):
    def __init__(self):
        RB.RhythmDBEntryType.__init__(self, name='netease')
        globals()[self.__class__.__name__] = lambda: self  # singleton

    def do_get_playback_uri(self, entry):
        id = entry.dup_string(RB.RhythmDBPropType.LOCATION)
        result = song_enhance_player_url(320000, [id])
        assert result['code'] == 200
        assert result['data'][0]['code'] == 200
        return result['data'][0]['url']
