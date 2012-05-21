import re

fps = avsp.GetVideoFramerate()
oldBookmarks = avsp.GetBookmarkList()
filename = avsp.GetFilename('Open a bookmark file', filefilter=
                            'Supported files|*.txt;*.xml|'
                            'Chapters Text files (*.txt)|*.txt|'
                            'Matroska XML files (*.xml)|*.xml|'
                            'All files (*.*)|*.*')
if filename:
    f = open(filename)
    lines = f.read()
    f.close()
    bookmarkList = []
    titleDict = {}
    # pasering chapters text files
    timeList = re.findall(r'(\d+)=(\d+):(\d+):(\d+\.\d+)', lines)
    if timeList:
        for index, title in re.findall(r'(\d+)NAME=(.*)', lines, re.I):
            titleDict[index] = title
        for index, hr, min, sec in timeList:
            sec = int(hr)*3600 + int(min)*60 + float(sec)
            bookmark = int(round(sec*fps))
            title = titleDict.get(index, '')
            bookmarkList.append((bookmark, title))
            if bookmark in oldBookmarks:
                bookmarkList.append((bookmark, title))
    # pasering matroska xml files            
    if not bookmarkList:
        sections = re.findall(r'<ChapterAtom>(.*?)</ChapterAtom>', lines, re.I|re.S)
        for text in sections:
            timecode = re.search(r'<ChapterTimeStart>(\d+):(\d+):(\d+\.\d+)</ChapterTimeStart>', text)
            if not timecode:
                continue
            title = re.search(r'<ChapterString>(.*?)</ChapterString>', text)
            hr, min, sec = timecode.groups()
            sec = int(hr)*3600 + int(min)*60 + float(sec)
            bookmark = int(round(sec*fps))
            title = title.group(1) if title else ''
            bookmarkList.append((bookmark, title))
            if bookmark in oldBookmarks:
                bookmarkList.append((bookmark, title))
    # pasering celltime format - frame count content        
    if not bookmarkList:
        try:
            for index in lines.strip().split():
                index = int(index)
                bookmarkList.append(index)
                if index in oldBookmarks:
                    bookmarkList.append(index)
        except:
            bookmarkList = []
    
    if bookmarkList:        
        ret = avsp.SetBookmark(bookmarkList)
        if not ret and bookmarkList and type(bookmarkList[0]) is tuple:
            for index in range(len(bookmarkList)):
                bookmarkList[index] = bookmarkList[index][0]
            avsp.SetBookmark(bookmarkList)
    else:
        avsp.MsgBox('bookmark file unrecognized!', 'Error')