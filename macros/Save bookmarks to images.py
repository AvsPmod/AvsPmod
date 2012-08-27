# Save bookmarks to images.py - an AvsP macro
import os
import sys
import re
import wx
import pyavs

# run in thread
if avsp.IsScriptSaved():
    filename = avsp.GetSaveFilename(_('Select the output directory and basename'))
    if filename:        
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)
        name, ext = os.path.splitext(basename)
        # force filename pattern
        if not re.search(r'%0\d+[di]', name):    
            name = re.split(r'\W*\d', name)[0] + '%06d'
        extDict = {
            '.bmp': wx.BITMAP_TYPE_BMP,
            '.gif': wx.BITMAP_TYPE_GIF,
            '.jpg': wx.BITMAP_TYPE_JPEG,
            '.pcx': wx.BITMAP_TYPE_PCX,
            '.png': wx.BITMAP_TYPE_PNG,
            '.pnm': wx.BITMAP_TYPE_PNM,
            '.tif': wx.BITMAP_TYPE_TIF,
            '.xpm': wx.BITMAP_TYPE_XPM,
            '.ico': wx.BITMAP_TYPE_ICO,
        }
        if ext not in extDict:
            ext = '.png'
        filename = os.path.join(dirname, name + ext)
    
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
        if bookmarks:               
            f = open(avsp.GetScriptFilename())
            script = f.read()
            f.close()
            quality = -1
            if ext == '.jpg':
                quality = avsp.SafeCall(wx.GetNumberFromUser, _('JPEG Quality (0-100):'), 
                                        '', _('JPEG Quality'), 70, 0, 100)
            AVS = pyavs.AvsClip(script)
            if AVS.IsErrorClip():
                avsp.MsgBox(AVS.error_message, _('Error'))
            else:
                bmp = wx.EmptyBitmap(AVS.Width, AVS.Height)
                mdc = wx.MemoryDC()
                mdc.SelectObject(bmp)
                count = 0
                for bookmark in bookmarks:
                    if bookmark > avsp.GetVideoFramecount():
                        break
                    AVS.DrawFrame(bookmark, mdc)
                    if quality == -1:
                        bmp.SaveFile(filename % bookmark, extDict[ext])
                    else:
                        img = bmp.ConvertToImage()
                        img.SetOptionInt(wx.IMAGE_OPTION_QUALITY, quality)
                        img.SaveFile(filename % bookmark, extDict[ext])
                    count += 1            
                avsp.MsgBox(_('%d image files created.') % count, _('Information'))
else:
    avsp.MsgBox(_('Please save the current script first!'), _('Error'))
