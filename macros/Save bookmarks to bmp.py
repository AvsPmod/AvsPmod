# Save bookmarks to bmp.py - an AvsP macro
import os
import re
import pyavs
import threading

def worker():
    name, ext = os.path.splitext(basename)
    # force filename pattern
    if not re.search(r'%0\d+[di]', name):    
        name = re.split(r'\W*\d', name)[0] + '%06d'
    filename = os.path.join(dirname, name + '.bmp')
    
    # merge trim selections and bookmrks
    selections = avsp.GetSelectionList()
    if selections:
        selections = [i for lo, hi in selections for i in range(lo, hi+1)]
    else:
        selections = []
    bookmarks = avsp.GetBookmarkList()
    if bookmarks:
        bookmarks += selections
    else:
        bookmarks = selections
        
    # deduplicate and sort frame no  
    bookmarks = list(set(bookmarks))
    bookmarks.sort()
    
    AVS = pyavs.AvsClip(avsp.GetText())
    for bookmark in bookmarks:
        AVS._x_SaveFrame(filename % bookmark, bookmark)
        
    avsp.MsgBox('%d image files created.' % len(bookmarks))
    

filename = avsp.GetSaveFilename()
dirname = os.path.dirname(filename)
basename = os.path.basename(filename)    
if filename:
    thread = threading.Thread(target=worker)
    thread.start()
    