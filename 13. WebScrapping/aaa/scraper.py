import requests
import sys
import shutil
import re
import threading
from bs4 import BeautifulSoup as soup

THREAD_COUNTER = 0
THREAD_MAX     = 5

def get_source( link ):
    r = requests.get( link )
    if r.status_code == 200:
        return soup( r.text )
    else:
        sys.exit( "[~] Invalid Response Received." )

def filter( html ):
    imgs = html.findAll( "img" )
    if imgs:
        return imgs
    else:
        sys.exit("[~] No images detected on the page.")

def requesthandle( link, name ):
    global THREAD_COUNTER
    THREAD_COUNTER += 1
    try:
        r = requests.get( link, stream=True )
        if r.status_code == 200:
            r.raw.decode_content = True
            f = open( name, "wb" )
            shutil.copyfileobj(r.raw, f)
            f.close()
            print ("[*] Downloaded Image: %s" % name)
    except Exception as error:
        print ("[~] Error Occured with %s : %s" % (name, error))
    THREAD_COUNTER -= 1

def main():
    path1 = "https://drive.google.com/drive/folders/1tsNzkpVvfbEQDVOFTuverce1CqBUWSYC/"
    path2 = "https://www.drivespark.com/wallpapers/"
    html = get_source(path1)
    tags = filter( html )
    for tag in tags:
        src = tag.get( "src" )
        if src:
            src = re.match( r"((?:https?:\/\/.*)?\/(.*\.(?:png|jpg)))", src )
            if src:
                (link, name) = src.groups()
                if not link.startswith("http"):
                    link = "https://www.drivespark.com" + link
                _t = threading.Thread( target=requesthandle, args=(link, name.split("/")[-1]) )
                _t.daemon = True
                _t.start()

                while THREAD_COUNTER >= THREAD_MAX:
                    pass

    while THREAD_COUNTER > 0:
        pass

main()