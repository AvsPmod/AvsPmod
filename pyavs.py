# AvsP - an AviSynth editor
# Copyright 2007 Peter Jang
#  http://www.avisynth.org/qwerpoi

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

# pyavs - AVI functions via Avisynth in Python
# Dependencies:
#     Python (tested with v2.4.2)
#     ctypes (tested with v1.0.1) - note that ctypes is included with Python 2.5+
# Scripts:
#     avisynth.py (python Avisynth wrapper)

import ctypes
import sys
import os

import avisynth

# Define C types and constants
DWORD = ctypes.c_ulong
UINT = ctypes.c_uint
WORD = ctypes.c_ushort
LONG = ctypes.c_long
BYTE = ctypes.c_byte
CHAR = ctypes.c_char
HANDLE = ctypes.c_ulong
NULL = 0
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



class BITMAPFILEHEADER(ctypes.Structure):
    _fields_ = [
        ("bfType",    WORD),
        ("bfSize",   DWORD),
        ("bfReserved1",    WORD),
        ("bfReserved2",    WORD),
        ("bfOffBits",   DWORD)]

                
# Define C functions

CreateFile = ctypes.windll.kernel32.CreateFileA
WriteFile = ctypes.windll.kernel32.WriteFile
CloseHandle = ctypes.windll.kernel32.CloseHandle

DrawDibOpen = ctypes.windll.msvfw32.DrawDibOpen
DrawDibClose = ctypes.windll.msvfw32.DrawDibClose
DrawDibDraw = ctypes.windll.msvfw32.DrawDibDraw
handleDib = [None]

avsfile=None

def InitRoutines():
    handleDib[0] = DrawDibOpen()
    
def ExitRoutines():
    DrawDibClose(handleDib[0])

class AvsClip:
    def __init__(self, script, filename='', env=None, fitHeight=None, fitWidth=None, oldFramecount=240, keepRaw=False, matrix='Rec601', interlaced=False, swapuv=False):
        # Internal variables
        self.initialized = False
        self.error_message = None
        self.current_frame = -1
        self.bmih = BITMAPINFOHEADER()
        self.pgf = LONG()
        self.pBits = None
        self.pInfo = None
        self.clipRaw = None
        self.ptrY = self.ptrU = self.ptrV = None
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
        self.Colorspace = None
        self.ffms_info_cache = {}
        # Create the Avisynth script clip
        if (env is not None) and not isinstance(env,avisynth.PIScriptEnvironment):
            raise TypeError("env must be a PIScriptEnvironment or None")
        if env is None:
            if isinstance(script,avisynth.PClip):
                raise ValueError("env must be defined when providing a clip") 
            try:
                self.env=avisynth.avs_create_script_environment(3)
            except WindowsError:
                return
        if isinstance(script,avisynth.PClip):
            self.clip=script
            self.env=env
        else:
            if type(script) != unicode:
                f=unicode(script)
            else:
                f = script
            arg=avisynth.AVS_Value(f)           #assign to AVSValue
            scriptdirname, scriptbasename = os.path.split(filename)
            if os.path.isdir(scriptdirname):
                self.env.SetWorkingDir(scriptdirname)
            arg2=avisynth.AVS_Value(scriptbasename)
            args=avisynth.AVS_Value([arg,arg2])
            try:
                avsfile=self.env.Invoke("eval",args,0) #use eval to load it
                self.clip=avsfile.AsClip(self.env)
            except avisynth.AvisynthError, err:
                fontSize=24
                self.error_message = str(err)
                lineList = []
                yLine = 0
                nChars = 0
                for errLine in str(err).split('\n'):
                    lineList.append('Subtitle("""%s""",y=%i,size=%i,text_color=$FF0000,align=8)' % (errLine, yLine, fontSize))
                    yLine += fontSize
                    nChars = max(nChars, len(errLine))
                eLength = oldFramecount
                eWidth = nChars * fontSize / 2
                eHeight = yLine + fontSize/4
                firstLine = 'BlankClip(length=%(eLength)i,width=%(eWidth)i,height=%(eHeight)i)' % locals()
                errText = firstLine + '.'.join(lineList)
                arg = avisynth.AVS_Value(errText)
                try:
                    avsfile=self.env.Invoke("eval",arg,0) #use eval to load it
                    self.clip=avsfile.AsClip(self.env)
                except avisynth.AvisynthError, err:
                    return
            if not self.env.GetVar("last").IsClip():#.AsClip(self.env)
                self.env.SetVar("last",avisynth.AVS_Value(self.clip))
        # Set the video properties
        self.vi=self.clip.GetVideoInfo()
        self.HasVideo = self.vi.HasVideo()
        if not self.HasVideo:
            self.clip = None
            errText = 'MessageClip("No video")'
            arg = avisynth.AVS_Value(errText)
            try:
                avsfile = self.env.Invoke("eval", arg, 0)
                self.clip = avsfile.AsClip(self.env)
            except avisynth.AvisynthError, err:
                return
            if not self.env.GetVar("last").IsClip():#.AsClip(self.env)
                self.env.SetVar("last",avisynth.AVS_Value(self.clip))
            self.vi=self.clip.GetVideoInfo()
            self.HasVideo = self.vi.HasVideo()
        self.Framecount = self.vi.num_frames
        self.Width = self.vi.width
        self.Height = self.vi.height
        self.WidthActual, self.HeightActual = self.Width, self.Height
        self.FramerateNumerator = self.vi.fps_numerator 
        self.FramerateDenominator = self.vi.fps_denominator
        try:
            self.Framerate = self.vi.fps_numerator / float(self.vi.fps_denominator)
        except ZeroDivisionError:
            pass
        self.sample_type_dict = {
            avisynth.SAMPLE_INT8: 8,
            avisynth.SAMPLE_INT16: 16,
            avisynth.SAMPLE_INT24: 24,
            avisynth.SAMPLE_INT32: 32,
            avisynth.SAMPLE_FLOAT: 32,
        }
        self.Audiorate = self.vi.audio_samples_per_second
        self.Audiolength = self.vi.num_audio_samples
        #~ self.AudiolengthF = None
        self.Audiochannels = self.vi.nchannels
        self.Audiobits = self.sample_type_dict.get(self.vi.sample_type, 0)
        self.IsAudioFloat = self.vi.sample_type == avisynth.SAMPLE_FLOAT
        self.IsAudioInt = not self.IsAudioFloat
        self.IsRGB = self.vi.IsRGB()
        self.IsRGB24 = self.vi.IsRGB24()
        self.IsRGB32 = self.vi.IsRGB32()
        self.IsYUY2 = self.vi.IsYUY2()
        self.IsYV12 = self.vi.IsYV12()
        self.IsYUV = self.vi.IsYUV()
        self.Colorspace = 'RGB24'*self.IsRGB24 + 'RGB32'*self.IsRGB32 + 'YUY2'*self.IsYUY2 + 'YV12'*self.IsYV12
        self.IsPlanar = self.vi.IsPlanar()
        self.IsInterleaved = not self.IsPlanar
        self.IsFieldBased = self.vi.IsFieldBased()
        self.IsFrameBased = not self.IsFieldBased
        self.GetParity = avisynth.avs_get_parity(self.clip,0)#self.vi.image_type
        self.HasAudio = self.vi.HasAudio()
        if keepRaw:
            self.clipRaw = self.clip
            
        # Initialize display-related variables
        if not self.vi.IsRGB32():
            try:
                arg(self.clip)
            except NameError:
                arg = avisynth.AVS_Value(self.clip)
            if self.IsYUV and swapuv:
                try:
                    avsfile = self.env.Invoke("swapuv", arg, 0)
                    arg.Release()
                    self.clip = avsfile.AsClip(self.env)
                except avisynth.AvisynthError, err:
                    return
            arg = avisynth.AVS_Value(self.clip)
            arg1 = avisynth.AVS_Value(matrix)
            if not self.IsYV12:
                interlaced = False
            arg2 = avisynth.AVS_Value(interlaced)
            args = avisynth.AVS_Value([arg, arg1, arg2])
            try:
                avsfile = self.env.Invoke("converttorgb32", args, 0)
                arg.Release()  #release the clip
                self.clip = avsfile.AsClip(self.env)
            except avisynth.AvisynthError, err:
                return
        # Add a resize...
        if fitHeight is not None and self.Height != 0:
            fitWidthTemp = int(round(fitHeight *  (self.Width/float(self.Height))))
            if fitWidth is None:
                fitWidth = fitWidthTemp
            elif fitWidthTemp > fitWidth:
                fitHeight = int(round(fitWidth *  (self.Height/float(self.Width))))
            else:
                fitWidth = fitWidthTemp
            if fitHeight >= 4 and fitWidth >= 4:
                arg0 = avisynth.AVS_Value(self.clip)
                arg1 = avisynth.AVS_Value(fitWidth)
                arg2 = avisynth.AVS_Value(fitHeight)
                args = avisynth.AVS_Value([arg0, arg1, arg2])
                try:
                    avsfile = self.env.Invoke("bicubicresize", args, 0)
                    arg0.Release()
                    self.clip = avsfile.AsClip(self.env)
                except avisynth.AvisynthError, err:
                    return
                # Set internal width and height variables appropriately
                self.Width, self.Height = fitWidth, fitHeight
        avisynth.CreateBitmapInfoHeader(self.clip,self.bmih)
        self.pInfo=ctypes.pointer(self.bmih)
        #~ self.BUF=ctypes.c_ubyte*self.bmih.biSizeImage
        #~ self.pBits=self.BUF()
        # Initialization complete.
        self.initialized = True
        if __debug__:
            print 'Avisynth clip created successfully'
        
    def __del__(self):
        if self.initialized:
            self.clip = None
            self.clipRaw = None
            if __debug__:
                print "Deleting allocated video memory..."
            
    def _GetFrame(self, frame):
        if self.initialized:
            if self.current_frame == frame:
                return True
            if frame < 0:
                frame = 0
            if frame >= self.Framecount:
                frame = self.Framecount-1
            self.current_frame = frame
            src=self.clip.GetFrame(frame)
            self.pBits = src.GetReadPtr()
            #~ try:
                #~ src=self.clip.GetFrame(frame)
            #~ except WindowsError:
                #~ return False
            src_pitch=src.GetPitch()
            self.bmih.biWidth = src_pitch*8/self.bmih.biBitCount
            #~ row_size=src.GetRowSize()
            #~ height=self.bmih.biHeight
            #~ dst_pitch=self.bmih.biWidth*self.bmih.biBitCount/8
            #~ self.env.BitBlt(self.pBits,dst_pitch,src.GetReadPtr(),src_pitch,row_size,height)
            if self.clipRaw is not None:
                frame=self.clipRaw.GetFrame(frame)
                self.pitch = frame.GetPitch()
                self.ptrY = frame.GetReadPtr(plane=avisynth.PLANAR_Y)
                self.ptrU = frame.GetReadPtr(plane=avisynth.PLANAR_U)
                self.ptrV = frame.GetReadPtr(plane=avisynth.PLANAR_V)
            return True
        else:
            return False
            
    def DrawFrame(self, frame, hdc=None, offset=(0,0), size=None):
        if not self._GetFrame(frame):
            return
        self.current_frame
        if hdc:
            if size is None:
                w = self.Width
                h = self.Height
            else:
                w, h = size 
            DrawDibDraw(handleDib[0], hdc, offset[0], offset[1], w, h, self.pInfo, self.pBits, 0, 0, w, h, 0)
        
    def GetPixelYUV(self, x, y):
        if self.clipRaw is not None:
            if self.IsYV12:
                indexY = x + y * self.pitch
                indexU = indexV = (x/2) + (y/2) * (self.pitch/2)
            elif self.IsYUY2:
                indexY = (x*2) + y * self.pitch
                indexU = 4*(x/2) + 1 + y * self.pitch
                indexV = 4*(x/2) + 3 + y * self.pitch
            else:
                return (-1,-1,-1)
            return (self.ptrY[indexY], self.ptrU[indexU], self.ptrV[indexV])
        else:
            return (-1,-1,-1)
            
    def GetPixelRGB(self, x, y):
        if self.clipRaw is not None:
            if self.IsRGB32:
                indexB = (x*4) + (self.HeightActual - 1 - y) * self.pitch
                indexG = indexB + 1
                indexR = indexB + 2
            if self.IsRGB24:
                indexB = (x*3) + (self.HeightActual - 1 - y) * self.pitch
                indexG = indexB + 1
                indexR = indexB + 2
            else:
                return (-1,-1,-1)
            return (self.ptrY[indexR], self.ptrY[indexG], self.ptrY[indexB])
        else:
            return (-1,-1,-1)
            
    def GetPixelRGBA(self, x, y):
        if self.clipRaw is not None:
            if self.IsRGB32:
                indexB = (x*4) + (self.HeightActual - 1 - y) * self.pitch
                indexG = indexB + 1
                indexR = indexB + 2
                indexA = indexB + 3
            else:
                return (-1,-1,-1,-1)
            return (self.ptrY[indexR], self.ptrY[indexG], self.ptrY[indexB], self.ptrY[indexA])
        else:
            return (-1,-1,-1,-1)
                
    def GetVarType(self, strVar):
        try:
            arg = self.env.GetVar(strVar)
        except avisynth.AvisynthError:
            return 'unknown'
        #~ print strVar, arg
        argtype = 'unknown'
        if arg.IsInt():
            argtype = 'int'
        elif arg.IsString():
            argtype = 'string'
        elif arg.IsBool():
            argtype = 'bool'
        elif arg.IsClip():
            argtype = 'clip'
        elif arg.IsFloat():
            argtype = 'float'
        elif arg.IsArray():
            argtype = 'array'
        elif arg.IsError():
            argtype = 'error'
        arg.Release()
        return argtype
        
    def IsErrorClip(self):
        return self.error_message is not None
        
    def _x_SaveFrame(self, filename, frame=None):
        # Get the frame to display
        if frame == None:
            if self.pInfo == None or self.pBits == None:
                self._GetFrame(0)
        else:
            self._GetFrame(frame)
        if isinstance(filename, unicode):
            filename = filename.encode(sys.getfilesystemencoding())
        buffer = ctypes.create_string_buffer(filename)
        hFile = CreateFile(
                ctypes.byref(buffer),
                #filename,
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
        #~ extrabytes = (4 - self.bmih.biWidth % 4) % 4
        #~ widthPadded = self.bmih.biWidth + extrabytes
        #~ bitmapsize = (widthPadded * self.bmih.biHeight * self.bmih.biBitCount) / 8
        widthPadded = self.bmih.biWidth
        self.bmih.biWidth = self.Width
        src_pitch = widthPadded * self.bmih.biBitCount / 8
        dst_pitch = self.bmih.biWidth * self.bmih.biBitCount / 8
        bfType = WORD(0x4d42)
        bfSize = DWORD(fileheadersize + bmpheadersize + self.bmih.biSizeImage)
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
        for i in range(self.bmih.biHeight):
            WriteFile(
                    hFile,
                    avisynth.ByRefAt(self.pBits, src_pitch*i),
                    dst_pitch,
                    ctypes.byref(dwBytesWritten),
                    NULL
                    )
        CloseHandle(hFile)
        self.bmih.biWidth = widthPadded
        
if __name__ == '__main__':
    AVI = AvsClip('Version().ConvertToYV12()', 'example.avs')
    if AVI.initialized:
        print 'Width =', AVI.Width
        print 'Height =', AVI.Height
        print 'Framecount =', AVI.Framecount
        print 'Framerate =', AVI.Framerate
        print 'FramerateNumerator =', AVI.FramerateNumerator
        print 'FramerateDenominator =', AVI.FramerateDenominator
        print 'Audiorate =', AVI.Audiorate
        print 'Audiolength =', AVI.Audiolength
        #~ print 'AudiolengthF =', AVI.AudiolengthF
        print 'Audiochannels =', AVI.Audiochannels
        print 'Audiobits =', AVI.Audiobits
        print 'IsAudioFloat =', AVI.IsAudioFloat
        print 'IsAudioInt =', AVI.IsAudioInt
        print 'Colorspace =', AVI.Colorspace
        print 'IsRGB =', AVI.IsRGB
        print 'IsRGB24 =', AVI.IsRGB24
        print 'IsRGB32 =', AVI.IsRGB32
        print 'IsYUY2 =', AVI.IsYUY2
        print 'IsYV12 =', AVI.IsYV12
        print 'IsYUV =', AVI.IsYUV
        print 'IsPlanar =', AVI.IsPlanar
        print 'IsInterleaved =', AVI.IsInterleaved
        print 'IsFieldBased =', AVI.IsFieldBased
        print 'IsFrameBased =', AVI.IsFrameBased
        print 'GetParity =', AVI.GetParity 
        print 'HasAudio =', AVI.HasAudio
        print 'HasVideo =', AVI.HasVideo
        AVI._x_SaveFrame("C:\\workspace\\test_file.bmp", 100)
    else:
        print AVI.error_message
    AVI = None
    
    AVI = AvsClip('Blackness()', 'test.avs')
    if AVI.initialized:
        print AVI.Width
    else:
        print AVI.error_message
    AVI = None
    
    s="""    Version().ConvertToYV12()
    Sharpen(1.0)
    FlipVertical()
    """
    env = avisynth.avs_create_script_environment(3)
    r=env.Invoke("eval",avisynth.AVS_Value(s),0)
    AVI = AvsClip(r.AsClip(env),env=env)
    AVI._x_SaveFrame("C:\\workspace\\test_file2.bmp", 100)
    AVI._GetFrame(100)
    AVI = None
    env.Release()
    env = None
    
    print "Exit program."

