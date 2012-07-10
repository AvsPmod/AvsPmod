import re
import cPickle

filename = avsp.GetFilename(_('Select a file'), filefilter=
                            _('All supported files') + '|*.txt;*.xml;*.ses;*.log;*.qp|' +
                            _('Chapters Text files') + ' (*.txt)|*.txt|'+
                            _('Matroska XML files') + ' (*.xml)|*.xml|' + 
                            _('Celltimes files') + ' (*.txt)|*.txt|' +
                            _('AvsP Session files') + ' (*.ses)|*.ses|' +
                            _('TFM log files') + ' (*.log)|*.log|' + 
                            _('XviD log files') + ' (*.log)|*.log|' + 
                            _('QP files') + ' (*.qp)|*.qp|' + 
                            _('All files') + ' (*.*)|*.*')
if not filename:
    return

f = open(filename)
lines = f.read()
f.close()

bookmarkDict = {}

# parsing QP-file
if not bookmarkDict:
    try:
        for index in lines.strip().split('\n'):
            s=index.strip()
            if s!='':
                bookmarkDict[int(s.split(' ')[0])] = ''
    except:
        bookmarkDict = {}

# parsing SCXviD log
if not bookmarkDict:
    try:
        if lines.startswith('# XviD 2pass stat file'):
            bookmarkDict=dict((i-3,'') for i,v in enumerate(lines.split('\n')) if v.startswith('i'))
    except:
        bookmarkDict = {}

# parsing TFM output
if not bookmarkDict:
    if lines.startswith('#TFM '):
        try:
            stats=re.split('\[Individual Frames|\[Grouped Ranges|\[POSSIBLE|\[u, b|'.replace('|',r'.+?FORMAT.+?\n|'),re.sub(r'#\s+\n?','',lines),0,re.DOTALL)
            if len(stats)==5:
                dCombed=dict( (int(L.split(' ')[0]), L.split(' ')[1]) for L in stats[1].strip().split('\n') if not L.startswith('none'))
                dPossible=dict( (int(L.split(' ')[0]), '') for L in re.sub('\(\d+\)',' ',stats[3].strip()).split('\n') if not L.startswith('none'))
                dUBmatch=dict( (int(L.split(' ')[0]), L.split(' ')[1]) for L in stats[4].strip().split('\n') if not L.startswith('none'))
                maxframe = max([max(d.keys()) if d.keys() else -1 for d in (dCombed, dPossible, dUBmatch)])
                if maxframe == -1:
                    avsp.MsgBox(_('Not combed or out of order frames'), _('Bookmarks from TFM file'))
                    return
                s=avsp.GetTextEntry( \
                        [_('Combed') + ' (%d)' % len(dCombed),\
                         _('Possible') + ' (%d)' % len(dPossible),\
                         _('u,b,out-of-order') + ' (%d)' % len(dUBmatch),\
                         '',\
                         _('Min frame:'),\
                         _('Max frame:')],\
                        [True,True,True,'','0',str(maxframe)],\
                        _('TFM log parser'),\
                        ['check','check','check','sep','text','text'],\
                        250 )
                if not s: return

                if s[0]: bookmarkDict.update(dCombed)
                if s[1]: bookmarkDict.update(dPossible)
                if s[2]: bookmarkDict.update(dUBmatch)

                try:
                    f1,f2=int(s[3]),int(s[4])
                    if f1!=0 or f2!=maxframe:
                        bookmarkDict=dict( (f,t) for (f,t) in bookmarkDict.items() if f1<=f<=f2 )
                except:
                    pass

                avsp.GetWindow().GetStatusBar().SetStatusText( _('%d frames imported') % len(bookmarkDict) )
        except:
            raise
            avsp.MsgBox(_('[COMBED FRAMES] section could not be parsed'))
            return

# parsing chapters text files
if not bookmarkDict:
    timeList = re.findall(r'(\d+)=(\d+):(\d+):(\d+\.\d+)', lines)
    if timeList:
        fps = avsp.GetVideoFramerate()
        titleDict = {}
        for index, title in re.findall(r'(\d+)NAME=(.*)', lines, re.I):
            titleDict[index] = title
        for index, hr, min, sec in timeList:
            sec = int(hr)*3600 + int(min)*60 + float(sec)
            bookmark = int(round(sec*fps))
            bookmarkDict[bookmark] = titleDict.get(index, '')

# parsing matroska xml files
if not bookmarkDict:
    sections = re.findall(r'<ChapterAtom>(.*?)</ChapterAtom>', lines, re.I|re.S)
    fps = avsp.GetVideoFramerate()
    for text in sections:
        timecode = re.search(r'<ChapterTimeStart>(\d+):(\d+):(\d+\.\d+)</ChapterTimeStart>', text)
        if not timecode:
            continue
        title = re.search(r'<ChapterString>(.*?)</ChapterString>', text)
        hr, min, sec = timecode.groups()
        sec = int(hr)*3600 + int(min)*60 + float(sec)
        bookmark = int(round(sec*fps))
        bookmarkDict[bookmark] = title.group(1) if title else ''

# parsing celltime format - frame count content
if not bookmarkDict:
    try:
        for index in lines.strip().split():
            bookmarkDict[int(index)] = ''
    except:
        bookmarkDict = {}

# parsing AvsP ssesion files
if not bookmarkDict:
    try:
        f = open(filename, 'rb')
        session = cPickle.load(f)
    except:
        pass
    f.close()
    try:
        if 'bookmarks' in session:
            if 'bookMarkDict' in session:
                for bookmark, btype in session['bookmarks']:
                    bookmarkDict[bookmark] = session['bookMarkDict'].get(bookmark, '')
            else:
                for bookmark, btype in session['bookmarks']:
                    bookmarkDict[bookmark] = ''
    except:
        pass

if bookmarkDict:
    bookmarkList = bookmarkDict.items()
    # Don't delete current bookmarks, update its title if supplied
    oldBookmarks = avsp.GetBookmarkList()
    for bookmark, title in bookmarkDict.items():
        if bookmark in oldBookmarks:
            if title:
                bookmarkList.append((bookmark, title))
            else:
                bookmarkList.remove((bookmark, title))
    avsp.SetBookmark(bookmarkList)
else:
    avsp.MsgBox(_('Bookmark file unrecognized!'), _('Error'))