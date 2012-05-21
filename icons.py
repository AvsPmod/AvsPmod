#----------------------------------------------------------------------
# Name:        wx.lib.embeddedimage
# Purpose:     Defines a class used for embedding PNG images in Python
#              code. The primary method of using this module is via
#              the code generator in wx.tools.img2py.
#
# Author:      Anthony Tuininga
#
# Created:     26-Nov-2007
# RCS-ID:      $Id: embeddedimage.py 65197 2010-08-04 20:22:24Z RD $
# Copyright:   (c) 2007 by Anthony Tuininga
# Licence:     wxWindows license
#----------------------------------------------------------------------

import base64
import cStringIO
import wx

try:
    b64decode = base64.b64decode
except AttributeError:
    b64decode = base64.decodestring
    

class PyEmbeddedImage(object):
    """
    PyEmbeddedImage is primarily intended to be used by code generated
    by img2py as a means of embedding image data in a python module so
    the image can be used at runtime without needing to access the
    image from an image file.  This makes distributing icons and such
    that an application uses simpler since tools like py2exe will
    automatically bundle modules that are imported, and the
    application doesn't have to worry about how to locate the image
    files on the user's filesystem.

    The class can also be used for image data that may be acquired
    from some other source at runtime, such as over the network or
    from a database.  In this case pass False for isBase64 (unless the
    data actually is base64 encoded.)  Any image type that
    wx.ImageFromStream can handle should be okay.
    """

    def __init__(self, data, isBase64=True):
        self.data = data
        self.isBase64 = isBase64

    def GetBitmap(self):
        return wx.BitmapFromImage(self.GetImage())

    def GetData(self):
        data = self.data
        if self.isBase64:
            data = b64decode(self.data)
        return data

    def GetIcon(self):
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(self.GetBitmap())
        return icon

    def GetImage(self):
        stream = cStringIO.StringIO(self.GetData())
        return wx.ImageFromStream(stream)

    # added for backwards compatibility
    getBitmap = GetBitmap
    getData = GetData
    getIcon = GetIcon
    getImage = GetImage

    # define properties, for convenience
    Bitmap = property(GetBitmap)
    Icon = property(GetIcon)
    Image = property(GetImage)

AvsP_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAgZJ"
    "REFUWIXtl6FywjAch38pmN2RoXbH3bgZqlD0AYKo6gwvgmMPALzAHK+A2QPAISqK2dwUCgy3"
    "qblRu2WiJLTQJG2BMbG/IrmQ39fv0iQlxCrhkmVdNP0vAJTTOvn3Fy86IbFK5CgA/v3FgyBA"
    "pVLR/jEMQ/i+j+dNHwAwXQMIV+ATm+cBIfFFKMJrtRrCMMwcHi8BgomdCUICiHDbtg/C421d"
    "eBEIQqySDG+1WgeB++3xeKwNzwuRWAOUUu2ky+XSGCzKuwOmC/O41LdABeL7Pj6qfTSqUXv1"
    "Zpi90gDul+ATm6sslIFoxbbbbc55+tsXBxrd7vq7BogsFhIb0Xw+Vw7cbDZwXReDxTAKr0cw"
    "jbo+QFpQ7C0SYGtBOQ+lFIyxRN9j0wzh3en5DrZinQUA6HQ6GCyGGL0BjeudCW1pLCQATBYA"
    "wHEc+Xu2hQCKW0g9jH7TwgFAUQvdejELyuM4j4XVZ9RXxEIqgLCgg3AcB67rAq8zjLZ7QREL"
    "SgMCghCiBGGMIfCupAkgvwXtjYhYJWICYYyh1+tJCJOF/cp0JTOBUEolBJDBQl6ALCAC4mY2"
    "VFqYro8EMIGIQ2tkOiVjdwRyiu8CsaCCIAAQHduDZh/ey26MfPonkrignORaHjciNrHuuzkc"
    "OJGB/RJGvAe+A0gJPxvAPgigvqafFSBLXfzT7B/gBzi2CON/wMBrAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
play_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAH5J"
    "REFUWIXt1EESwCAIQ1GQ3v/GHbvqXiBpuoAD+N+MivsKU86S1gcwgN8DwnyH+ZYBvoCkroAB"
    "Kb0BJKT1CBEQyC/oQKDfsAKh7IEMhLqITiDyTXgxD79tuwRwEqYAMmEooBKGADrhFgARLgGQ"
    "4RSAET4CMMPvyDfhAAYgBzzIPiRzQVyedwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
next_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAHZJ"
    "REFUWIXt10sKACEMA9BU739k0RsM/aQoTLrtIg9sC5qNiZs1rqYLIIAAHsCE7Uq/DOhGuJ+g"
    "CxGagQ5EeAjZiNQWMBHpNWQhSneAgXj/EH3VwrZKvwRghKcBrPAUgBkeBrDDQ4COcDegKxwA"
    "TP8CAQT4PeAAzMIsUQFAh3wAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
skip_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAH1J"
    "REFUWIXt10sKwDAIBNAxuf+RU7PqrhQ/IylUtwbmEaIQkTFxssbR9AY0oAEWwIRopn+XXuvx"
    "nOkGWIgwoBLhegMVCPcjZCNCU8BEhMeQhUjtAQbi+4vorRZUMv0UgBEeBrDCQwBmuBvADncB"
    "KsLNgKpwAJD+FzSgAb8HbDPFMErXwWvCAAAAAElFTkSuQmCC")