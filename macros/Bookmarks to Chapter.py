fps = avsp.GetVideoFramerate(index=None)
bookmarks = avsp.GetBookmarkList()
bookmarks.sort()
filename = avsp.GetSaveFilename(title='Save as')
if filename!='':
    file=open(filename,'w')
    chapter = 1
    for bookmark in bookmarks:
       	m, s = divmod(bookmark/fps, 60)
        s2 = s
        h, m = divmod(m, 60)
        ms = (s2-int(s))*1000
        time = '%02i:%02i:%02i.%03i' % (h ,m, s, ms)
        file.write('CHAPTER%02i=' % chapter)
        file.write(time + '\n')
        file.write('CHAPTER%02iNAME=Chapter %02i\n' % (chapter, chapter))
        chapter+=1
    file.close()