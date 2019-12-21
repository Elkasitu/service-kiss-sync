import hashlib
import json
import os
import requests
import sys
import time
import xbmc
import xbmcaddon


__addon__ = xbmcaddon.Addon('service.kiss-sync')
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__ = __addon__.getAddonInfo('id')

addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
sys.path.append(os.path.join(addon_dir, 'resources', 'lib'))


import kiss
import player


def main(p):
    if not p.isPlayingVideo():
        return

    current_file = p.getPlayingFile()
    hashed_file = hashlib.sha1(current_file.encode('utf-8')).hexdigest()
    val = kiss.fetch(hashed_file)['time']


    if val is None:
        return kiss.add({'name': hashed_file})
    else:
        # update the centralized DB
        return kiss.update({'name': hashed_file, 'time': p.getTime()})


if __name__ == '__main__':
    mon = xbmc.Monitor()
    p = player.Player()

    while not mon.abortRequested():
        main(p)

        # sleep for 1s
        if mon.waitForAbort(10):
            break
