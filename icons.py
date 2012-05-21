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

#----------------------------------------------------------------------
checked_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAWElEQVR42s2RQQoAIAgE82c+"
    "3Z8ZHYwsgxUh2kOHckbYqBVD4xARzYLMTE5gF0jW+acCjeZRgXUECeamDU4J7O2AM4IWwWgH"
    "eoMzJWoEV77xdwEKW5ygkg43FHEROvSJLgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
unchecked_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAMUlEQVR42mNkoBAwgogDBw78"
    "J1Wjg4MDI4oBMAFiALL6UQNGDRhuBhCrGQZQDKAEAABsPGgR8pSNpgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
smile_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAwNJ"
    "REFUOI1lk11Mm3UUxn//f8sKLLQbhQrd+ArQroOaZWMGGMwLlyyZgPFKXUx2Iy6LF7pdeqHR"
    "zOiWmPkRRW8k3rgY9YJ4sRiMqN0cc+qW0c6NlQJV6Nv3pYwBsgFve7xo3eb2JM/NyTnP8+Tk"
    "HKW0gweRTpkynTjP1MQvrK7mqNraRiDURV39FvVgr7pfwDQs+WPkRVwqga/CS1mZl7V1zV+p"
    "ea7EZjFuejn8ymnqG+4J3RVIJsYkHT3EtlAdG+trQBcDCmwNt4W1BZvfLk/zzbe/c7D/C3a3"
    "tysAZ97ZkEysh117w1BWw+3VHCWuyryFEyhzIFmLzifClJZ6GBx4nsmJpDQ01iqUdnBpuE/E"
    "elZEXpd3T/UKIPv37xCR0yLypfT1PSaAnHyzV2T5hAx9/py8/EKnKO1Ap2eT4q9YBK8X8BD5"
    "aQaAkZE4sAEo5scfbuRro3/Dxk0EGrbiLl1n4saEOG/NXaBmswdUEZDl668O8cmn2zlwYDfg"
    "AhTR2NsMDY1y+EgHkGWTuxi/v5prYxHUheFj0taSQldvAXwFevILJAvoQhIHsAxYzMVMhiMJ"
    "zFvFOO2sk9U7WUrQJBImtv0PgUCQexsUYAUoIhq7jtdl43I4yOZyOIs2oN2+TtJGBrCZSc3R"
    "2zNYcMwB6wUCaPqeGiAzs8Tyis18ZoFgqAtdWd3B+OQca1PzdO9poqPLR3//h4XIJQUqnjn4"
    "Dk/va6a1rY7r8QyWZRJs2ZM/pMH398n2xjV27dyGfsTP0WNnOHsuTVd3M5KDyM/j9Oxt5I3j"
    "T3L5/AyR0TjWzRWOn/peKaUdpI2MfPZeK93trbQEa/EE/CxOLxI5l0KJpqOtjs2Vbn69aHDp"
    "yixj0RivnTxLlb9C3T3l+HhcPjrRzo5wLcGmJnwVbtzuUtZtTcq4w2RyibFrSaanZnn1rTM0"
    "BwPqoWeyzEUZ+OAIU+PfUeUrp7zch21rUsY8hrlAKPw4Lx39mEqf5+Fnuh+WuSRXo6P8efUi"
    "IkL40U6CoZ3/G/wP/wJ3xTm0DZwlTwAAAABJRU5ErkJggg==")
    
#----------------------------------------------------------------------
question_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACI0lEQVQ4jYWTwUsbQRTGfzOx"
    "SWZN06R4CcKeikQLpUJdmlrwppfmouip4KVQaKEI/SN66lGhIF57K7156m1FTSCUSkrQRLAQ"
    "4mVziDXo7Ganh26KyGo/eAwPvvfm+96bEcTjMfAamIryn8An4Pt1oogpfm5Z1seZmZkHhUIh"
    "C9DpdHrVarXZ7/ffA+5VciKmwYfZ2dlnY2NjOUCGYSiVUiqfz989OTm5B3y5SpbXip8AxVwu"
    "l9Vao7XG93183yefz2eBYsS5EQeO45wvLCyYbrf7L1zXNfPz88ZxnHPg4DYLT8fHx6dGR0fv"
    "NBoNXNdlMBgwPT1NvV6n3W777Xb7G/D1JgurlUplTwgRHB8f02q16PV6nJ6e4nleUKlU9oDV"
    "22YAsH54eNgFKBaLzM3NsbW1xf7+fhdYv83/VbRWVlZMs9k029vbZnl52QCtOOJITP5mqGxt"
    "bQ0hBEqpodp3wAYQxDVzgM/A0dLSkimXy6bT6ZidnR1TLpfN4uKiAY4ijjMsGm7hpWVZG7Zt"
    "PyqVSoUgCJBSMjk5ied51Go1tNZMTEzcD8PQvry8fOH7vgf8GD7leqlUKkopZTKZRClFMpnk"
    "7OwMgEwmg9aai4sLfN9nMBiEu7u7DeDhCGABdjqdllJKUqkUSilSqRTZbBZjDEEQkEgkEEIg"
    "pcQYIwEbsAR/f95b4BXQB35H0Qd0pDAdXZSJTgvYBNZFNHk7ZiP/QwD8+gOTQ9W5+jdpxQAA"
    "AABJRU5ErkJggg==")
    
#----------------------------------------------------------------------
ok_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9i"
    "ZSBJbWFnZVJlYWR5ccllPAAAAWVJREFUeNpi/P//PwNdgVsnw38QJkuzYxvD/3c/JoIxiE2y"
    "5idfmv/P2sQAxk+/NoJdwkKs5sV5zQzbj9QyMLAyMDACxb7/f4eqyB1omjsWvzkBNd/+XPR/"
    "1h6G/zOBePZehv+XPsX/d4J4wRiu6MqnOCCGS0DEW4GKPyb8n30Q6OwDQM2HQJoTUDWDbD37"
    "we//7GNABUcZ/p967//foZkBjEFskPgsoPgcIH36gz+qZiBggfuHmYHhH1Dqwq2NDLVpNmBJ"
    "EJuBCehnIFZTsWOomLaRYV8VgwlQ6izMAJB+Y5c2hjOlqboMj59cZvj3j4EBlrYYgbJMQM2y"
    "MroMXbMvM+xF0wwCQHsZnt/by7DlheCrNAd7WYYfPz4x/AfZCpRhBsaRiIQsw4Q5t7FqRgcg"
    "l/xf+Zz7/9wbDGAMYrug+ZkQMHYFalj9khuMXUnUDDfEExgznp3kaYYbQqxmRkqzM0CAAQBW"
    "bMG1YQFlxwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
rectangle_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABXElEQVR42sXSv0vDQBQH8O9d"
    "ErUVp/ojCAoiiDjU/hAHlzq5WXBRu1pBEAc3J/EPcHIRWpFODv4Bzro4CEXQWRBc1FYpUps0"
    "lzTnpeqU10UFH2S6y4f3fe8YflnsT4F6sybfnCdwppGXfekjFh1FxIiyECA8IU9ut1CxbqDz"
    "HhIQXgOT/YtYmtoLA5ZoyEJ5GU2/Co0ZJOC2bJi9SeTTxxRgyWI5B0c+K6CL7qBlwYymsZYu"
    "EIATdJCDi4qaQWdgKJJCfqYYBhoBcJWDp1XBuYogw+N2PQsD3Smsz3YADi9VB7wKXTPAuDr8"
    "OpUK81sMwrUwGEliY65IRzg4X1VDfGnPoP1z8MlP4DvCcF8Cm5kjogPxLvfPVmCLGjROb8FR"
    "EUZicWwvEFtourbcPc2i8voAQ6ffgS3qiI9nsJMthYGgru8v5N2jekg6sQUVw/MFEmPzmDCn"
    "aeAn9f/AByV0jxHGo4HSAAAAAElFTkSuQmCC")