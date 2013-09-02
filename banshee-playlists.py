#!/usr/bin/python
# Export playlists from the banshee database

import os
import urllib
import sqlite3
import codecs
import argparse

# Variables
m3uHeader = '#EXTM3U'
metaHeader = '#EXTINF:'
playlistsOut = []

# Parse arguments
parser = argparse.ArgumentParser(description='Extract playlists from the banshee music database')
parser.add_argument('-l','--list-playlists', action="store_true", default=False,
                    help='List playlists and exit')
parser.add_argument('-a','--absolute', action="store_true", default=False,
                    help='Use absolute paths (relative by default)')
parser.add_argument('-u','--user-playlists', action="store_true", default=False,
                    help='Extract user playlists (default)')
parser.add_argument('-s','--smart-playlists', action="store_true", default=False,
                    help='Extract smart playlists')
parser.add_argument('-r','--remove-old', action="store_true", default=False,
                    help='Remove existing *.m3u files in --output-dir')
parser.add_argument('-p','--playlists', action="store", default="",
                    help='Specify which playlists to export by name. Delimit using "|"')
parser.add_argument('-o','--output-dir', action="store", default=os.getcwd(),
                    help='Specify where to put the playlist files')
parser.add_argument('-d','--database', action="store", 
                    default=os.path.join(os.path.expanduser('~'), '.config/banshee-1/banshee.db'),
                    help='Specify where the database is')
args = parser.parse_args()

# Format paths
args.output_dir = os.path.realpath(args.output_dir)
args.database = os.path.realpath(args.database)

# Connect to the banshee database
connection = sqlite3.connect(args.database)
c = connection.cursor()

# Gather CorePlaylist names if required
if args.user_playlists == True or args.smart_playlists == False:
    playlistsSQL = 'Select Name from CorePlaylists Where PrimarySourceID = 1'
    for x in c.execute(playlistsSQL):
        playlistsOut.append([x, 'Playlist'])

# Gather CoreSmartPlaylist names if required
if args.smart_playlists == True:
    smartplaylistsSQL = 'Select Name from CoreSmartPlaylists Where PrimarySourceID = 1'
    for x in c.execute(smartplaylistsSQL):
        playlistsOut.append([x, 'SmartPlaylist'])

# Remove playlists not present in args.playlists if args.playlists != ""
if args.playlists != "":
    playlistsIn = args.playlists.split("|")
    i = 0
    n = len(playlistsOut)
    while i < n:
        if playlistsOut[i][0][0] not in playlistsIn:
            playlistsOut.pop(i)
            n -= 1
        else:
            i += 1

# List playlists and exit if required
if args.list_playlists == True:
    for x in playlistsOut:
        print x[0][0]
    exit()

# Remove old playlists if required
if args.remove_old:
    for x in sorted(os.listdir(args.output_dir)):
        if os.path.splitext(x)[1] == '.m3u':
            print 'Removing "' + x + '"...',
            os.remove(os.path.join(args.output_dir,x))
            print 'Done'

# Loop through CorePlaylists
for x in sorted(playlistsOut):
    playlistName = x[0][0]
    playlistType = x[1]
    playlistInfoSQL = 'Select round(t.Duration/1000.0,0), a.Name, t.Title, t.Uri '+\
                      'From Core'+ playlistType +'s p, Core'+ playlistType +'Entries e, '+\
                           'CoreTracks t, CoreArtists a '+\
                      'Where p.'+ playlistType +'ID = e.'+ playlistType +'ID and '+\
                            'e.TrackID = t.TrackID and '+\
                            't.ArtistID = a.ArtistID and '+\
                            't.PrimarySourceID = 1 and '+\
                            'p.Name = "' + playlistName +\
                      '" Group By p.Name, a.Name, t.Title, t.Uri'
    
    print 'Writing "' + playlistName + '.m3u"...',
    # Open current playlist file for writing
    playOut = codecs.open(os.path.join(args.output_dir, playlistName + '.m3u'), 'w', "utf-8-sig")
    playOut.write(m3uHeader + '\n')
    # Loop through CorePlaylistEntries for the current CorePlaylist
    for y in c.execute(playlistInfoSQL):
        duration = int(y[0])
        artist = y[1] if y[1] != None else ""
        title = y[2] if y[2] != None else ""
        path = unicode(urllib.unquote(y[3][7:].encode('ascii')), "utf-8")
        # Make playlist paths relative
        if args.absolute == False:
            path = os.path.relpath(path, args.output_dir)
        else:
            path = os.path.realpath(path)

        # Write playlist detail line
        playOut.write(metaHeader + str(duration) + ',' + artist + ' - ' + title + '\n')
        playOut.write(path + '\n')
    playOut.close()
    print 'Done'
