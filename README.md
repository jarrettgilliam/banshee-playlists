banshee-playlists.py
====================

A simple utility written in python for extracting playlists from the popular Banshee music player database and writing utf-8 encoded m3u playlists.

### Example Usage

The most basic usage is just simply calling the script.
```
./banshee-playlists.py
```
This will output all your playlists to the current directory using relative path names in the playlist.


More commonly I use something like this:
```
./banshee-playlists.py -aro ~/my/playlist/directory
```
This is similar to the previous example except it remove all the old (*.m3u) playlist files from the target playlist directory, uses absolute path names in the playlist, and specifies the target playlist directory.


If you just want your user playlist or smart playlists your can add the `-u` or `-s` option respectively.


If you only want a few of your playlists you can specify them with the `-p` option and pipe delimiters.
```
./banshee-playlists.py -aro ~/my/playlist/directory -p "MyPlaylist|MyOtherPlaylist"
```

Be aware however that the playlist names are case sensitive. I recommend using the `-l` option to output the playlist names to the console first for reference.
```
./banshee-playlists.py -l
```
As before you can use the `-u` or `-s` options to only output user or smart playlists.


also if the script doesn't automatically find your database you can specify it manually with the `-d` option 
```
./banshee-playlists.py -d /path/to/banshee/database.db
```

Lastly if you get stuck or forget how to use it you can use the `-h` option for help. I use it all the time :)

Enjoy!
