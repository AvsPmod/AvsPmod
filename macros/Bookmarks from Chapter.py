import re
import cPickle

fps = avsp.GetVideoFramerate()
oldBookmarks = avsp.GetBookmarkList()
filename = avsp.GetFilename(_('Open a bookmark file'), filefilter=
                            _('Supported files') + '|*.txt;*.xml;*.ses|' + 
                            _('Chapters Text files') + ' (*.txt)|*.txt|' + 
                            _('Matroska XML files') + ' (*.xml)|*.xml|' + 
                            _('Celltimes files') + ' (*.txt)|*.txt|' + 
                            _('AvsP Session files') + ' (*.ses)|*.ses|' + 
                            _('All files') + ' (*.*)|*.*')
if filename:
    f = open(filename)
    lines = f.read()
    f.close()
    bookmarkList = []
    bookmarkDict = {}
    titleDict = {}
    # pasering chapters text files
    timeList = re.findall(r'(\d+)=(\d+):(\d+):(\d+\.\d+)', lines)
    if timeList:
        for index, title in re.findall(r'(\d+)NAME=(.*)', lines, re.I):
            titleDict[index] = title
        for index, hr, min, sec in timeList:
            sec = int(hr)*3600 + int(min)*60 + float(sec)
            bookmark = int(round(sec*fps))
            bookmarkDict[bookmark] = titleDict.get(index, '')
    # pasering matroska xml files            
    if not bookmarkDict:
        sections = re.findall(r'<ChapterAtom>(.*?)</ChapterAtom>', lines, re.I|re.S)
        for text in sections:
            timecode = re.search(r'<ChapterTimeStart>(\d+):(\d+):(\d+\.\d+)</ChapterTimeStart>', text)
            if not timecode:
                continue
            title = re.search(r'<ChapterString>(.*?)</ChapterString>', text)
            hr, min, sec = timecode.groups()
            sec = int(hr)*3600 + int(min)*60 + float(sec)
            bookmark = int(round(sec*fps))
            bookmarkDict[bookmark] = title.group(1) if title else ''
    # pasering celltime format - frame count content        
    if not bookmarkDict:
        try:
            for index in lines.strip().split():
                bookmarkDict[int(index)] = ''
        except:
            bookmarkDict = {}
    # pasering AvsP ssesion files
    if not bookmarkDict:
        try:
            f = open(filename, 'rb')
            session = cPickle.load(f)
        except:
            pass
        f.close()
        if 'bookmarks' in session:
            if 'bookMarkDict' in session:
                for bookmark, btype in session['bookmarks']:
                    bookmarkDict[bookmark] = session['bookMarkDict'].get(bookmark, '')
            else:
                for bookmark, btype in session['bookmarks']:
                    bookmarkDict[bookmark] = ''
            
    if bookmarkDict:
        bookmarkList = bookmarkDict.items()
        for bookmark in bookmarkDict:
            if bookmark in oldBookmarks:
                if bookmarkDict[bookmark]:
                    bookmarkList.append((bookmark, bookmarkDict[bookmark]))
                else:
                    bookmarkList.remove((bookmark, bookmarkDict[bookmark]))
        ret = avsp.SetBookmark(bookmarkList)
        if not ret and bookmarkList: # back-compitable with v2.0.5 or before
            bookmarkList = [ bookmark for bookmark, title in bookmarkList]
            avsp.SetBookmark(bookmarkList)
    else:
        avsp.MsgBox(_('Bookmark file unrecognized!'), _('Error'))