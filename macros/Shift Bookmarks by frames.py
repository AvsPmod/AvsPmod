# Written by wOxxOm
try:
    shift=int(avsp.GetTextEntry('Introduce the number of frames:', '', 
                                'Shift bookmarks by # frames', 'spin', 200))
    try:
        bookmarks=[(b+shift, t) for b,t in avsp.GetBookmarkList( title=True )]
    except TypeError:
        bookmarks=[(b+shift) for b in avsp.GetBookmarkList()]
    avsp.GetWindow().DeleteAllFrameBookmarks()
    avsp.SetBookmark( bookmarks )
except:
    pass