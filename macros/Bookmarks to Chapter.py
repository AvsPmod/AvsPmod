import codecs
import os.path

# run in thread
try:
    bookmarks = avsp.GetBookmarkList(title=True)
except TypeError:
    bookmarks = avsp.GetBookmarkList()
bookmarks.sort()
filename = avsp.GetSaveFilename(
                title=_('Save chapter file as...'), 
                default=os.path.splitext(
                    avsp.GetScriptFilename(propose='general', only='base'))[0],
                filefilter = '|'.join((_('Text files') + ' (*.txt)|*.txt', 
                                       _('All files') + ' (*.*)|*.*')))
if not filename:
    return
fps = avsp.GetVideoFramerate()
text = []
chapter = 1
for item in bookmarks:
    if type(item) is int:
        bookmark = item
        title = ''
    else:
        bookmark, title = item
    m, s = divmod(bookmark/fps, 60)
    h, m = divmod(m, 60)
    timecode = 'CHAPTER%02d=%02d:%02d:%06.3f\n' % (chapter, h ,m, s)
    if not title:
        title = 'Chapter %02d' % chapter
    title = 'CHAPTER%02dNAME=%s\n' % (chapter, title)
    text += [timecode, title]
    chapter +=1
    f = codecs.open(filename, 'w', 'utf-8')
    f.writelines(text)
    f.close()