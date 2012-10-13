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
                            _('Timecode format v1 files') + ' (*.txt)|*.txt|' + 
                            _('All files') + ' (*.*)|*.*')
if not filename:
    return

lines = avsp.GetWindow().GetTextFromFile(filename)[0]

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

# parsing Timecode format v1: place a bookmark on every starting frame
if not bookmarkDict:
    if lines.startswith('# timecode format v1'):
        match = re.search(r'^\s*assume\s*(\d*\.*\d+\.*\d*)', lines, re.M|re.I)
        base_fps = (match.group(1) if match else 'unknown') + ' fps'
        bookmarkDict[0] = base_fps
        for line in lines.splitlines():
            if line and line[0].isdigit():
                start, end, fps = line.split(',')
                bookmarkDict[int(start)] = fps + ' fps'
                bookmarkDict[int(end)+1] = base_fps

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
            stats = lines.split('#   FORMAT:')
            if len(stats)==5:
                sectionslice = (0,(2,-2),(2,-4),(2,-4),(2,-1))
                section = lambda sectionidx: stats[sectionidx].strip().split('\n')[sectionslice[sectionidx][0]:sectionslice[sectionidx][1]]
                sectionisempty = lambda sectionidx: 'none detected' in stats[sectionidx]

                frameindent = 4
                frametitle = lambda line: line[line.find(' ',frameindent+1)+1:]
                framenum = lambda line: int(line[1:line.find(' ',frameindent)])

                dCombed = dict( (framenum(L), frametitle(L)) for L in section(1) ) if not sectionisempty(1) else {}
                dGrouped = dict( (int(F), frametitle(L)) for L in section(2) for F in re.split('[\s,]',L[frameindent:])[:-2] ) if not sectionisempty(2) else {}
                dPossible = dict( (framenum(L), frametitle(L)) for L in section(3) ) if not sectionisempty(3) else {}
                dUBmatch = dict( (int(F),L[-1]) for L in section(4) for F in re.split('[\s,]',L[frameindent:-2]) ) if not sectionisempty(4) else {}
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