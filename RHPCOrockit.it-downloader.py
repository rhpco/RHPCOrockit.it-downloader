'''
RHPCOrockit.it-downloader
rakkapriccio@gmail.com
'''
import argparse
import os
import httplib2
import http
import sys
import hashlib
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import textwrap

def connect(url):
    try:
        conn=http.client.HTTPConnection("www.rockit.it")
        conn.request("GET",url)
    except:
       print ("Error - Connection"+conn)
       exit(1)
    r1=conn.getresponse()
    return r1
def getPlaylist(soup):
    playlists = soup.findAll(attrs={'itemprop': 'track'})
    return playlists
def downloader(playlist,repositoryUrl,seed,directory):
    for play in playlist:
        songname = play.find(attrs={'class': 'titolo'}).string
        id= play['id'].split("_")
        albumid = id[2]
        songid = id[1]
        if directory==None: directory=albumid
        downloadurl = repositoryUrl+albumid+"/"+songid+".mp3"
        downloadTrack(downloadurl,
                      createHash(downloadurl,seed),
                      directory,
                      songid,
                      songname)
def downloadTrack_viewer(url,hash,directory,song,songname):
    print ("Downloading... %s/%s - %s" %(directory,songname,hash))
def downloadTrack(url,hash,directory,song,songname):
    downloadTrack_viewer(url,hash,directory,song,songname)
    post_params = {
              'rockitID' : hash,
              }
    params = urllib.parse.urlencode(post_params).encode('ascii')
    req = urllib.request.Request(url,params)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Referer', 'http://www.rockit.it/')
    res = urllib.request.urlopen(req)
    if not os.path.exists(directory):
        os.makedirs(directory)
    output = open(directory+"/"+songname+".mp3",'wb')
    output.write(res.read())
    output.close()
def createHash(url,seed):
    return hashlib.md5(url.encode('utf-8')+seed.encode('utf-8')).hexdigest()
def customArgParse():

    parser = argparse.ArgumentParser(
        prog='RHPCOrockit-listener',
        usage='%(prog)s /album/path/singer  ~/mp3/albumname/ --seed -newseed ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
______ _   _ ______  _____ _____
| ___ \ | | || ___ \/  __ \  _  |
| |_/ / |_| || |_/ /| /  \/ | | |
|    /|  _  ||  __/ | |   | | | |
| |\ \| | | || |    | \__/\ \_/ /
\_| \_\_| |_/\_|     \____/\___/ rockit.it-downloader

            Download mp3 from the most hipster italian
            music website.

                ''')
    )

    parser.add_argument('album',  nargs='?', help='rockit.it album page url')
    parser.add_argument('directory',  nargs='?', help='destination directory')
    parser.add_argument('--seed', '-s',  nargs='?', default='-pirla', help='seed for hash creation')
    if len(sys.argv) < 2:
        parser.print_help()
        exit()
    args = parser.parse_args()
    return args

args = customArgParse()
repositoryUrl = "http://ww2.rockit.it/7mp3/"
r1 = connect(args.album)
soup = BeautifulSoup(r1.read())
playlist = getPlaylist(soup)
downloader(playlist,repositoryUrl,args.seed,args.directory)

