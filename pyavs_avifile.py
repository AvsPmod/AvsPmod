# AvsP - an AviSynth editor
# Copyright 2007 Peter Jang
#  http://avisynth.nl/users/qwerpoi

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA, or visit
#  http://www.gnu.org/copyleft/gpl.html .

# pyavi - AVI functions in Python
# Dependencies:
# Python (tested with v2.4.2)
# ctypes (tested with v0.9.6) - note that ctypes is included with Python 2.5+

import ctypes
import sys
import os
import codecs

encoding = sys.getfilesystemencoding()

# Define C types and constants
DWORD = ctypes.c_ulong
UINT = ctypes.c_uint
WORD = ctypes.c_ushort
LONG = ctypes.c_long
BYTE = ctypes.c_byte
CHAR = ctypes.c_char
HANDLE = ctypes.c_ulong
NULL = 0
streamtypeVIDEO = DWORD(1935960438)
OF_READ = UINT(0)
BI_RGB = 0
GENERIC_WRITE = 0x40000000L
CREATE_ALWAYS = 2
FILE_ATTRIBUTE_NORMAL  = 0x00000080

try: _
except NameError:
    def _(s): return s
        
# Define C structures
class RECT(ctypes.Structure):
    _fields_ = [("left", LONG),
                ("top", LONG),
                ("right", LONG),
                ("bottom", LONG)]
                
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize",  DWORD),
                ("biWidth",   LONG),
                ("biHeight",   LONG),
                ("biPlanes",   WORD),
                ("biBitCount",   WORD),
                ("biCompression",  DWORD),
                ("biSizeImage",  DWORD),
                ("biXPelsPerMeter",   LONG),
                ("biYPelsPerMeter",   LONG),
                ("biClrUsed",  DWORD),
                ("biClrImportant",  DWORD)]

class RGBQUAD(ctypes.Structure):
  _fields_ = [("rgbBlue",    BYTE),
              ("rgbGreen",    BYTE),
              ("rgbRed",    BYTE),
              ("rgbReserved",    BYTE)]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER),
                ("bmiColors", RGBQUAD)]

class BITMAPFILEHEADER(ctypes.Structure):
    _fields_ = [
        ("bfType",    WORD),
        ("bfSize",   DWORD),
        ("bfReserved1",    WORD),
        ("bfReserved2",    WORD),
        ("bfOffBits",   DWORD)]

class AVISTREAMINFO(ctypes.Structure):
    _fields_ = [("fccType", DWORD),
                ("fccHandler", DWORD),
                ("dwFlags", DWORD),
                ("dwCaps", DWORD),
                ("wPriority", WORD),
                ("wLanguage", WORD),
                ("dwScale", DWORD),
                ("dwRate", DWORD),
                ("dwStart", DWORD),
                ("dwLength", DWORD),
                ("dwInitialFrames", DWORD),
                ("dwSuggestedBufferSize", DWORD),
                ("dwQuality", DWORD),
                ("dwSampleSize", DWORD),
                ("rcFrame", RECT),
                ("dwEditCount", DWORD),
                ("dwFormatChangeCount", DWORD),
                ("szName", CHAR * 64)]
                
# Define C functions
AVIFileInit = ctypes.windll.avifil32.AVIFileInit
try:
    AVIStreamOpenFromFileA = ctypes.windll.avifil32.AVIStreamOpenFromFileA
    AVIStreamOpenFromFileW = ctypes.windll.avifil32.AVIStreamOpenFromFileW
except AttributeError:
    AVIStreamOpenFromFileA = ctypes.windll.avifil32.AVIStreamOpenFromFile
AVIStreamInfo = ctypes.windll.avifil32.AVIStreamInfo
AVIStreamReadFormat = ctypes.windll.avifil32.AVIStreamReadFormat
AVIStreamGetFrameOpen = ctypes.windll.avifil32.AVIStreamGetFrameOpen
AVIStreamGetFrameClose = ctypes.windll.avifil32.AVIStreamGetFrameClose
AVIStreamRelease = ctypes.windll.avifil32.AVIStreamRelease
AVIFileRelease = ctypes.windll.avifil32.AVIFileRelease
AVIFileExit = ctypes.windll.avifil32.AVIFileExit
AVIStreamGetFrame = ctypes.windll.avifil32.AVIStreamGetFrame
SetDIBitsToDevice = ctypes.windll.gdi32.SetDIBitsToDevice
CreateFile = ctypes.windll.kernel32.CreateFileA
WriteFile = ctypes.windll.kernel32.WriteFile
CloseHandle = ctypes.windll.kernel32.CloseHandle

DrawDibOpen = ctypes.windll.msvfw32.DrawDibOpen
DrawDibClose = ctypes.windll.msvfw32.DrawDibClose
DrawDibDraw = ctypes.windll.msvfw32.DrawDibDraw
handleDib = [None]

def InitRoutines():
    AVIFileInit()
    handleDib[0] = DrawDibOpen()
    
def ExitRoutines():
    AVIFileExit()
    DrawDibClose(handleDib[0])


def MakePreviewScriptFile(script, filename):
    # Construct the filename of the temporary avisynth script
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname) or not os.access(dirname, os.W_OK):
        dirname = os.getcwd()
    previewname = os.path.join(dirname, 'preview.avs')
    i = 1
    while os.path.exists(previewname):
        previewname = os.path.join(dirname, 'preview%i.avs' % i)
        i = i+1
    # Write the file
    try:
        f = open(previewname,'w')
        f.write(script)
        f.close()
    except UnicodeEncodeError:
        f = codecs.open(previewname, 'w', encoding)
        f.write(script)
        f.close()
    return previewname

class AvsClip:
    def __init__(self, script, filename='', fitHeight=None, fitWidth=None, oldFramecount=None, keepRaw=False):
        self.initialized = False
        self.error_message = None
        self.current_frame = -1
        self.pvidstream = LONG() # = PAVISTREAM()
        self.bmih = BITMAPINFOHEADER()
        self.pgf = LONG()
        self.pBits = None
        self.pInfo = None
        psi = AVISTREAMINFO()
        # Avisynth script properties
        self.Width = -1
        self.Height = -1
        self.Framecount = -1
        self.Framerate = -1.0
        self.FramerateNumerator = -1
        self.FramerateDenominator = -1
        self.Audiorate = -1.0
        self.Audiolength = -1
        #~ self.AudiolengthF = None
        self.Audiochannels = -1
        self.Audiobits = -1
        self.IsAudioFloat = None
        self.IsAudioInt = None
        self.IsRGB = None
        self.IsRGB24 = None
        self.IsRGB32 = None
        self.IsYUY2 = None
        self.IsYV12 = None
        self.IsYUV = None
        self.IsPlanar = None
        self.IsInterleaved = None
        self.IsFieldBased = None
        self.IsFrameBased = None
        self.GetParity  = None
        self.HasAudio = None
        self.HasVideo = None
        self.Colorspace = 'RGB32'
        
        # Open the avi file
        previewname = MakePreviewScriptFile(script, filename)
        AVIStreamOpenFromFile = AVIStreamOpenFromFileA
        if type(previewname) == type(u''):
            try:
                AVIStreamOpenFromFile = AVIStreamOpenFromFileW
            except NameError:
                pass
        if (AVIStreamOpenFromFile(ctypes.byref(self.pvidstream), previewname, streamtypeVIDEO, 0, OF_READ, NULL)!=0):
            if __debug__:
                print>>sys.stderr, _("Failed to open the AVI file")
                #~ print>>sys.stderr, filename
            #~ AVIFileExit()
            return
        else:
            if __debug__:
                print "AVI file opened successfully"
            pass
        
        # Read basic data from the avi file
        AVIStreamInfo(self.pvidstream, ctypes.byref(psi), ctypes.sizeof(psi))
        self.Framecount = psi.dwLength
        self.Width = psi.rcFrame.right-psi.rcFrame.left
        self.Height = psi.rcFrame.bottom-psi.rcFrame.top
        self.WidthActual, self.HeightActual = self.Width, self.Height
        self.Framerate = psi.dwRate/(psi.dwScale+0.0)
        
        if fitHeight is not None:
            fitWidthTemp = int(round(fitHeight *  (self.Width/float(self.Height))))
            if fitWidth is None:
                fitWidth = fitWidthTemp
            elif fitWidthTemp > fitWidth:
                fitHeight = int(round(fitWidth *  (self.Height/float(self.Width))))
            else:
                fitWidth = fitWidthTemp
            if fitHeight >= 4 and fitWidth >= 4:
                resizeScript = 'Import("%s").ConvertToRGB().BicubicResize(%i,%i)' % (previewname, fitWidth, fitHeight)
                previewname2 = MakePreviewScriptFile(resizeScript, filename)
                AVIStreamRelease(self.pvidstream)
                if (AVIStreamOpenFromFile(ctypes.byref(self.pvidstream), previewname2, streamtypeVIDEO, 0, OF_READ, NULL)!=0):
                    if __debug__:
                        print>>sys.stderr, _("Failed to open the AVI file")
                    return
                else:
                    if __debug__:
                        print "AVI file opened successfully"
                    pass
                # Set internal width and height variables appropriately
                self.Width, self.Height = fitWidth, fitHeight
                os.remove(previewname2)
            
        # Define the desired image format
        self.bmih.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        self.bmih.biPlanes = 1
        self.bmih.biBitCount = 24
        self.bmih.biWidth = self.Width
        self.bmih.biHeight = self.Height
        self.bmih.biCompression = BI_RGB
        self.bmih.biSizeImage = 0
        self.bmih.biClrUsed = 0
        self.bmih.biClrImportant = 0
        # Change desired format to 32 bit (RGBA) if necessary
        bmihtemp = BITMAPINFOHEADER()
        bmihtemp_size = LONG(ctypes.sizeof(bmihtemp))
        AVIStreamReadFormat(self.pvidstream,0,ctypes.byref(bmihtemp),ctypes.byref(bmihtemp_size))
        if(bmihtemp.biBitCount==32):
            self.bmih.biBitCount = 32
        
        # Open the video stream
        self.pgf = AVIStreamGetFrameOpen(self.pvidstream,ctypes.byref(self.bmih))
        if self.pgf==-1:
            AVIStreamRelease(self.pvidstream)
            if __debug__:
                print>>sys.stderr, _("Failed to open the AVI frame")
            #~ AVIFileExit()
            return
        else:
            if __debug__:
                print "AVI frame opened successfully"
            pass
            
        self.AVIStreamGetFrameClose = AVIStreamGetFrameClose
        self.AVIStreamRelease = AVIStreamRelease
        self.AVIFileRelease = AVIFileRelease
        #~ self.AVIFileExit = AVIFileExit
        self.initialized = True
        os.remove(previewname)
        
    def __del__(self):
        if self.initialized:
            if __debug__:
                print "Deleting allocated video memory..."
            self.AVIStreamGetFrameClose(self.pgf)
            self.AVIStreamRelease(self.pvidstream)
            
    def _GetFrame(self, frame):
        if self.initialized:
            if(frame<0):
                frame = 0
            if(frame>=self.Framecount):
                frame = self.Framecount-1
            try:
                self.lpbi = AVIStreamGetFrame(self.pgf, frame) #Grab Data From The AVI Stream
            except WindowsError:
                print>>sys.stderr, _("Failed to retrieve AVI frame")
                return False
            self.pInfo = LONG(self.lpbi)
            self.pBits = LONG(self.lpbi + self.bmih.biSize + self.bmih.biClrUsed * ctypes.sizeof(RGBQUAD))
            return True
        else:
            return False
            
    def DrawFrame(self, frame, dc=None, offset=(0,0), size=None):
        if not self._GetFrame(frame):
            return
        if dc:
            hdc = dc.GetHDC()
            if size is None:
                w = self.Width
                h = self.Height
            else:
                w, h = size
            #~ SetDIBitsToDevice(hdc, offset[0], offset[1], w, h, 0, 0, 0, h, self.pBits, self.pInfo, 0)
            DrawDibDraw(handleDib[0], dc, offset[0], offset[1], w, h, self.pInfo, self.pBits, 0, 0, -1, -1, 0)
        
    def GetPixelYUV(self, x, y):
        return (-1,-1,-1)
            
    def GetPixelRGB(self, x, y):
        return (-1,-1,-1)
            
    def GetPixelRGBA(self, x, y):
        return (-1,-1,-1,-1)
                
    def GetVarType(self, strVar):
        return 'unknown'
    
    def IsErrorClip(self):
        return self.error_message is not None
        
    def _x_SaveFrame(self, filename, frame=None):
        # Get the frame to display
        if frame == None:
            if self.pInfo == None or self.pBits == None:
                self._GetFrame(0)
        else:
            self._GetFrame(frame)
        # Create the file for writing
        buffer = ctypes.create_string_buffer(filename)
        hFile = CreateFile(
                ctypes.byref(buffer),
                GENERIC_WRITE,
                0,
                NULL,
                CREATE_ALWAYS,
                FILE_ATTRIBUTE_NORMAL,
                NULL
                )
        # Write the bitmap file header
        fileheadersize = 14
        bmpheadersize = 40
        extrabytes = (4 - self.bmih.biWidth % 4) % 4
        widthPadded = self.bmih.biWidth + extrabytes
        bitmapsize = (widthPadded * self.bmih.biHeight * self.bmih.biBitCount) / 8
        bfType = WORD(0x4d42)
        bfSize = DWORD(fileheadersize + bmpheadersize + bitmapsize)
        bfReserved1 = WORD(0)
        bfReserved2 = WORD(0)
        bfOffBits = DWORD(fileheadersize + bmpheadersize)
        dwBytesWritten = DWORD()
        WriteFile(
                hFile,
                ctypes.byref(bfType),
                2,
                ctypes.byref(dwBytesWritten),
                NULL
                )
        WriteFile(
                hFile,
                ctypes.byref(bfSize),
                4,
                ctypes.byref(dwBytesWritten),
                NULL
                )
        WriteFile(
                hFile,
                ctypes.byref(bfReserved1),
                2,
                ctypes.byref(dwBytesWritten),
                NULL
                )
        WriteFile(
                hFile,
                ctypes.byref(bfReserved2),
                2,
                ctypes.byref(dwBytesWritten),
                NULL
                )
        WriteFile(
                hFile,
                ctypes.byref(bfOffBits),
                4,
                ctypes.byref(dwBytesWritten),
                NULL
                )
        # Write the bitmap info header and (unused) color table
        WriteFile(
                hFile,
                self.pInfo,
                bmpheadersize, #(self.bmih.biSize + self.bmih.biClrUsed * ctypes.sizeof(RGBQUAD)), # + bitmapsize),
                ctypes.byref(dwBytesWritten),
                NULL
                )
        # Write the bitmap bits
        WriteFile(
                hFile,
                self.pBits,
                bitmapsize,
                ctypes.byref(dwBytesWritten),
                NULL
                )
        CloseHandle(hFile)
        
if __name__ == '__main__':
    AVI = PyAVIFile("D:\\test.avs")
    AVI.SaveFrame("D:\\test_save_frame.bmp", 100)
    print "Exit program."
