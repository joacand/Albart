# Albart - Simple album cover downloader

Albart is a simple Python 3 script that automatically fetches music album art covers from Google images for your album directories.

### Requirements
The script requires the following libraries from pip:
* mutagen
* bs4 (BeautifulSoup)

### How to run
  - Run the Python 3 script with the starting directory flag:
  py -3 AlbumCoverDownloader.py -d "E:\Directory\To\Music\Artists"

The script will recursively go through all the directories.

### Thanks
Thanks to http://stackoverflow.com/a/28487500/4695853 for some of the Google image search code.

License
----
MIT
