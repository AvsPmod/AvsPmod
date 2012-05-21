# GOCR.py - an AvsP macro invoking GOCR engine
# dependencies: gocr.exe - http://jocr.sourceforge.net/

import os
import wx
from subprocess import Popen, PIPE

# convert bmp to pnm
avsp.SaveImage('temp.bmp')
img = wx.Image('temp.bmp')
img.SaveFile('temp.pnm', wx.BITMAP_TYPE_PNM)

# launch and redirect the executable
cmd = 'macros/gocr.exe temp.pnm'
proc = Popen(cmd, stdout=PIPE, stderr=PIPE,
             creationflags=0x08000000) # no cmd window
stdout, stderr = proc.communicate()

# copy ocr text to the scrap window and clipboard
if proc.returncode == 0:
    avsp.WriteToScrap(stdout)
    if not wx.TheClipboard.IsOpened():
        wx.TheClipboard.Open()
        data = wx.TextDataObject(stdout)
        wx.TheClipboard.SetData(data)
        wx.TheClipboard.Close()
else:    
    avsp.MsgBox(stderr, 'Error')

# delete temporary files
os.remove('temp.pnm')
os.remove('temp.bmp')