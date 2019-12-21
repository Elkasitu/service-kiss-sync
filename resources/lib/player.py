import hashlib
import kiss
import xbmc


class Player(xbmc.Player):

    def onPlayBackStarted(self):
        f = self.getPlayingFile()
        # TODO: hash the file contents and not the name
        hashed = hashlib.sha1(f.encode('utf-8')).hexdigest()
        seek_t = kiss.fetch(hashed)['time']

        if seek_t and seek_t > self.getTime():
            self.seekTime(seek_t)
