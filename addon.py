import hashlib
import json
import requests
import time
import xbmc
import xbmcaddon


__addon__ = xbmcaddon.Addon('service.kiss-sync')
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__ = __addon__.getAddonInfo('id')


def main():
    # XXX: Check onPlayBackStarted()
    if not xbmc.Player().isPlayingVideo():
        return
    current_file= xbmc.Player().getPlayingFile()
    # FIXME: hash the __contents__ of the file...
    hashed_file = hashlib.sha1(current_file.encode('utf-8')).hexdigest()
    r = requests.get('http://localhost:5000/fetch/%s' % hashed_file)
    assert r.ok, "Something went wrong when contacting the server"
    cur_time = xbmc.Player().getTime()

    # TODO: abstractify this and/or send JSON objects and decode them
    val = json.loads(r.text)['time']
    if val and val > cur_time:
        # FIXME: Seek should be done separately, only when the video is launched
        # XXX: Figure out how to either disable the native kodi feature to seek or how to make
        # the service query the internal kodi database and modify its value
        xbmc.Player().seekTime(val)
        return
    elif val is None:
        data = {'name': hashed_file}
        # TODO: this is gonna get annoying, move this into a generic function in utilities
        r = requests.post('http://localhost:5000/add', json=data)
        assert r.ok, "Something went wrong when contacting the server"
        return
    else:
        # update the centralized DB
        data = {'name': hashed_file, 'time': cur_time}
        r = requests.post('http://localhost:5000/update', json=data)
        assert r.ok, "Something went wrong when contacting the server"


if __name__ == '__main__':
    mon = xbmc.Monitor()

    while not mon.abortRequested():
        main()

        # sleep for 10s
        if mon.waitForAbort(10):
            break
