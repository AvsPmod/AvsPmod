# AvsP - an AviSynth editor
# 
# Copyright 2007 Peter Jang <http://www.avisynth.org/qwerpoi>
#           2010-2012 the AvsPmod authors <https://github.com/avspmod/avspmod>
#
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

# pyavs - AVI functions via AviSynth in Python
# Drawing uses VFW on Windows and generical wxPython support on other platforms
# 
# Dependencies:
#     Python (tested on v2.6 and v2.7)
#     wxPython (for *nix, tested on v2.8 and v2.9)
# Scripts:
#     avisynth.py (Python AviSynth/AvxSynth wrapper)

import sys
import os
import ctypes
import re

import avisynth

try: _
except NameError:
    def _(s): return s

class AvsClipBase:
    
    def __init__(self, script, filename='', workdir='', env=None, fitHeight=None, 
                 fitWidth=None, oldFramecount=240, keepRaw=False, onlyRaw=False, 
                 reorder_rgb=False, matrix=['auto', 'tv'], interlaced=False, swapuv=False):
        # Internal variables
        self.workdir = ''
        self.initialized = False
        self.error_message = None
        self.current_frame = -1
        self.pBits = None
        self.clipRaw = None
        self.onlyRaw = onlyRaw
        self.ptrY = self.ptrU = self.ptrV = None
        # Avisynth script properties
        self.Width = -1
        self.Height = -1
        self.WidthSubsampling = -1
        self.HeightSubsampling = -1
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
        self.IsYUV = None
        self.IsYUY2 = None
        self.IsYV24 = None
        self.IsYV16 = None
        self.IsYV12 = None
        self.IsYV411 = None
        self.IsY8 = None
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
        if env is not None:
            if isinstance(env,avisynth.PIScriptEnvironment):
                self.env = env
            else:
                raise TypeError("env must be a PIScriptEnvironment or None")
        else:
            if isinstance(script,avisynth.PClip):
                raise ValueError("env must be defined when providing a clip") 
            try:
                self.env=avisynth.avs_create_script_environment(3)
            except OSError:
                return
            if hasattr(self.env, 'GetError'):
                self.error_message = self.env.GetError()
                if self.error_message: return
        if isinstance(script,avisynth.PClip):
            self.clip=script
        else:
            if type(script) != unicode:
                f=unicode(script)
            else:
                f = script
            arg=avisynth.AVS_Value(f)           #assign to AVSValue
            scriptdirname, scriptbasename = os.path.split(filename)
            curdir = os.getcwdu()
            workdir = os.path.isdir(workdir) and workdir or scriptdirname
            if os.path.isdir(workdir):
                self.env.SetWorkingDir(workdir)
                self.workdir = workdir
            self.file = avisynth.AVS_Value(filename)
            self.name = avisynth.AVS_Value(scriptbasename)
            self.dir = avisynth.AVS_Value(scriptdirname)
            self.env.SetGlobalVar("$ScriptFile$", self.file)
            self.env.SetGlobalVar("$ScriptName$", self.name)
            self.env.SetGlobalVar("$ScriptDir$", self.dir)
            arg2=avisynth.AVS_Value(filename)
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
            finally:
                os.chdir(curdir)
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
        if self.vi.IsYUV() and not self.vi.IsY8():
            self.WidthSubsampling = self.vi.GetPlaneWidthSubsampling(avisynth.PLANAR_U)
            self.HeightSubsampling = self.vi.GetPlaneHeightSubsampling(avisynth.PLANAR_U)
        self.WidthActual, self.HeightActual = self.Width, self.Height # not used anymore
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
        self.IsYUV = self.vi.IsYUV()
        self.IsYUY2 = self.vi.IsYUY2()
        self.IsYV24 = self.vi.IsYV24()
        self.IsYV16 = self.vi.IsYV16()
        self.IsYV12 = self.vi.IsYV12()
        self.IsYV411 = self.vi.IsYV411()
        self.IsY8 = self.vi.IsY8()
        self.Colorspace = ('RGB24'*self.IsRGB24 + 'RGB32'*self.IsRGB32 + 'YUY2'*self.IsYUY2 + 'YV12'*self.IsYV12 + 
                           'YV24'*self.IsYV24 + 'YV16'*self.IsYV16 + 'YV411'*self.IsYV411 + 'Y8'*self.IsY8)
        self.IsPlanar = self.vi.IsPlanar()
        self.IsInterleaved = self.vi.IsInterleaved()
        self.IsFieldBased = self.vi.IsFieldBased()
        self.IsFrameBased = not self.IsFieldBased
        self.GetParity = avisynth.avs_get_parity(self.clip,0)#self.vi.image_type
        self.HasAudio = self.vi.HasAudio()
        if keepRaw or onlyRaw:
            self.clipRaw = self.clip
            if onlyRaw and self.IsRGB and reorder_rgb:
                self.clipRaw = self.BGR2RGB(self.clipRaw)
        
        # Initialize display-related variables
        if not self.IsRGB and not onlyRaw:
            if swapuv and self.IsYUV and not self.IsY8:
                try:
                    arg = avisynth.AVS_Value(self.clip)
                    avsfile = self.env.Invoke("swapuv", arg, 0)
                    arg.Release()
                    self.clip = avsfile.AsClip(self.env)
                except avisynth.AvisynthError, err:
                    return
        if isinstance(matrix, basestring):
            self.matrix = matrix
        else:
            matrix = matrix[:]
            if matrix[0] == 'auto':
                if self.Width > 1024 or self.Height > 576:
                    matrix[0] = '709'
                else:
                    matrix[0] = '601'
            matrix[1] = 'Rec' if matrix[1] == 'tv' else 'PC.'
            self.matrix = matrix[1] + matrix[0]
        self.interlaced = interlaced if self.IsYV12 else False
        if not onlyRaw and not self._ConvertToRGB():
            return
        
        # Add a resize...
        # Update: Not used anymore, resizing is done nowadays on avsp.LayoutVideoWindows
        #         Width == WidthActual, Height == HeightActual
        if 0 and fitHeight is not None and self.Height != 0:
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
        return True
    
    def __del__(self):
        if self.initialized:
            self.clip = None
            self.clipRaw = None
            if __debug__:
                print "Deleting allocated video memory for '{0}'".format(self.name)
    
    def _ConvertToRGB(self):
        '''Convert to RGB for display. Return True if successful'''
        pass
    
    def _GetFrame(self, frame):
        if self.initialized:
            if self.current_frame == frame:
                return True
            if frame < 0:
                frame = 0
            if frame >= self.Framecount:
                frame = self.Framecount - 1
            self.current_frame = frame
            src = self.clip.GetFrame(frame)
            self.pBits = src.GetReadPtr()
            # DrawPitch is the pitch of the RGB24 image for drawing.
            # pitch is the pitch of the actual raw image from clipRaw.
            self.DrawPitch = src.GetPitch()
            if self.clipRaw is not None:
                frame = self.clipRaw.GetFrame(frame)
                self.pitch = frame.GetPitch()
                self.pitchUV = frame.GetPitch(avisynth.PLANAR_U)
                self.ptrY = frame.GetReadPtr(plane=avisynth.PLANAR_Y)
                if not self.IsY8:
                    self.ptrU = frame.GetReadPtr(plane=avisynth.PLANAR_U)
                    self.ptrV = frame.GetReadPtr(plane=avisynth.PLANAR_V)
            return True
        return False
    
    def GetPixelYUV(self, x, y):
        if self.clipRaw is not None:
            if self.IsPlanar:
                indexY = x + y * self.pitch
                if self.IsY8:
                    return (self.ptrY[indexY], -1, -1)
                x = x >> self.WidthSubsampling
                y = y >> self.HeightSubsampling
                indexU = indexV = x + y * (self.pitchUV)
            elif self.IsYUY2:
                indexY = (x*2) + y * self.pitch
                indexU = 4*(x/2) + 1 + y * self.pitch
                indexV = 4*(x/2) + 3 + y * self.pitch
            else:
                return (-1,-1,-1)
            return (self.ptrY[indexY], self.ptrU[indexU], self.ptrV[indexV])
        else:
            return (-1,-1,-1)
    
    def GetPixelRGB(self, x, y, BGR=True):
        if self.clipRaw is not None and self.IsRGB:
            bytes = self.vi.BytesFromPixels(1)
            if BGR:
                indexB = (x * bytes) + (self.HeightActual - 1 - y) * self.pitch
                indexG = indexB + 1
                indexR = indexB + 2
            else:
                indexR = (x * bytes) + y * self.pitch
                indexG = indexR + 1
                indexB = indexR + 2
            return (self.ptrY[indexR], self.ptrY[indexG], self.ptrY[indexB])
        else:
            return (-1,-1,-1)
    
    def GetPixelRGBA(self, x, y, BGR=True):
        if self.clipRaw is not None and self.IsRGB32:
            bytes = self.vi.BytesFromPixels(1)
            if BGR:
                indexB = (x * bytes) + (self.HeightActual - 1 - y) * self.pitch
                indexG = indexB + 1
                indexR = indexB + 2
                indexA = indexB + 3
            else:
                indexR = (x * bytes) + y * self.pitch
                indexG = indexR + 1
                indexB = indexR + 2
                indexA = indexB + 3
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
    
    def BGR2RGB(self, clip):
        '''Reorder AviSynth's RGB (BGR) to RGB
        
        BGR -> RGB
        BGRA -> RGBA
        '''
        if self.IsRGB:
            clip = avisynth.AVS_Value(clip)
            clip = self.env.Invoke("FlipVertical", clip, 0)
            r = self.env.Invoke("ShowRed", clip, 0)
            b = self.env.Invoke("ShowBlue", clip, 0)
            if self.IsRGB24:
                merge_args = avisynth.AVS_Value([b, clip, r, avisynth.AVS_Value("RGB24")])
                return self.env.Invoke("MergeRGB", merge_args, 0).AsClip(self.env)
            else:
                merge_args = avisynth.AVS_Value([clip, b, clip, r])
                return self.env.Invoke("MergeARGB", merge_args, 0).AsClip(self.env)
    
    def Y4MHeader(self, colorspace=None, depth=None, width=None, height=None, sar='0:0', X=None): 
        '''Return a header for a yuv4mpeg2 stream'''
        re_res = re.compile(r'([x*/])(\d+)')
        if width is None:
            width = self.Width
        elif isinstance(width, basestring):
            match = re_res.match(width)
            if match:
                if match.group(1) == '/':
                    width = self.Width / int(match.group(2))
                else:
                    width = self.Width * int(match.group(2))
            else:
                raise Exception(_('Invalid string: ') + width)
        if height is None:
            height = self.Height
        elif isinstance(height, basestring):
            match = re_res.match(height)
            if match:
                if match.group(1) == '/':
                    height = self.Height / int(match.group(2))
                else:
                    height = self.Height * int(match.group(2))
            else:
                raise Exception(_('Invalid string: ') + height)
        if self.interlaced:
            interlaced = 'b' if self.vi.IsBFF() else 't'
        else:
            interlaced = 'p'
        colorspace_dict = {'YV24': '444', 
                           'YV16': '422', 
                           'YV12': '420', 
                           'YV411': '411', 
                           'Y8': 'mono'}
        if colorspace is None:
            if self.Colorspace not in colorspace_dict:
                raise Exception(_("{colorspace} can't be used with a yuv4mpeg2 "
                    "header.\nSpecify the right colorspace if piping fake video data.\n"
                    .format(colorspace=self.Colorspace)))
            colorspace = colorspace_dict[self.Colorspace]
        if depth:
            colorspace = 'p'.join((colorspace, str(depth)))
        X = ' X' + X if X is not None else ''
        return 'YUV4MPEG2 W{0} H{1} I{2} F{3}:{4} A{5} C{6}{7}\n'.format(width, 
            height, interlaced, self.FramerateNumerator, self.FramerateDenominator, 
            sar, colorspace, X)
    
    def RawFrame(self, frame, y4m_header=False):
        '''Get a buffer of raw video data'''
        if self.initialized and self.clipRaw is not None:
            if frame < 0:
                frame = 0
            if frame >= self.Framecount:
                frame = self.Framecount - 1
            frame = self.clipRaw.GetFrame(frame)
            total_bytes = self.Width * self.Height * self.vi.BitsPerPixel() >> 3
            if y4m_header is not False:
                X = ' X' + y4m_header if isinstance(y4m_header, basestring) else ''
                y4m_header = 'FRAME{0}\n'.format(X)
            else:
                y4m_header = ''
            y4m_header_len = len(y4m_header)
            buf = ctypes.create_string_buffer(total_bytes + y4m_header_len)
            buf[:y4m_header_len] = y4m_header
            write_addr = ctypes.addressof(buf) + y4m_header_len
            P_UBYTE = ctypes.POINTER(ctypes.c_ubyte)
            if self.IsPlanar and not self.IsY8:
                for plane in (avisynth.PLANAR_Y, avisynth.PLANAR_U, avisynth.PLANAR_V):
                    write_ptr = ctypes.cast(write_addr, P_UBYTE)
                    # using GetRowSize(plane) and GetHeight(plane) breaks v2.5.8
                    width = frame.GetRowSize() >> self.vi.GetPlaneWidthSubsampling(plane)
                    height = frame.GetHeight() >> self.vi.GetPlaneHeightSubsampling(plane)
                    self.env.BitBlt(write_ptr, width, frame.GetReadPtr(plane), 
                                    frame.GetPitch(plane), width, height)
                    write_addr += width * height
            else:
                # Note that AviSynth uses BGR
                write_ptr = ctypes.cast(write_addr, P_UBYTE)
                self.env.BitBlt(write_ptr, frame.GetRowSize(), frame.GetReadPtr(), 
                            frame.GetPitch(), frame.GetRowSize(), frame.GetHeight())
            return buf
    
    def AutocropFrame(self, frame, tol=70):
        '''Return crop values for a specific frame'''
        width, height = self.Width, self.Height
        if self.clipRaw is not None: # Get pixel color from the original clip
            self._GetFrame(frame)
            GetPixelColor = self.GetPixelRGB if self.IsRGB else self.GetPixelYUV
        else: # Get pixel color from the video preview (slower)
            bmp = wx.EmptyBitmap(width, height)
            mdc = wx.MemoryDC()
            mdc.SelectObject(bmp)
            self.DrawFrame(frame, mdc)
            img = bmp.ConvertToImage()
            GetPixelColor = lambda x, y : (img.GetRed(x, y), img.GetGreen(x, y), img.GetBlue(x, y))
        w, h = width - 1, height - 1
        top_left0, top_left1, top_left2 = GetPixelColor(0, 0)
        bottom_right0, bottom_right1, bottom_right2 = GetPixelColor(w, h)
        top = bottom = left = right = 0
        
        # top & bottom
        top_done = bottom_done = False
        for i in range(height):
            for j in range(width):
                if not top_done:
                    color0, color1, color2 = GetPixelColor(j, i)
                    if (abs(color0 - top_left0) > tol or 
                        abs(color1 - top_left1) > tol or 
                        abs(color2 - top_left2) > tol):
                            top = i
                            top_done = True
                if not bottom_done:
                    color0, color1, color2 = GetPixelColor(j, h - i)
                    if (abs(color0 - bottom_right0) > tol or 
                        abs(color1 - bottom_right1) > tol or 
                        abs(color2 - bottom_right2) > tol):
                            bottom = i
                            bottom_done = True
                if top_done and bottom_done: break
            else: continue
            break
        
        # left & right
        left_done = right_done = False
        for j in range(width):
            for i in range(height):
                if not left_done:
                    color0, color1, color2 = GetPixelColor(j, i)
                    if (abs(color0 - top_left0) > tol or 
                        abs(color1 - top_left1) > tol or 
                        abs(color2 - top_left2) > tol):
                            left = j
                            left_done = True
                if not right_done:
                    color0, color1, color2 = GetPixelColor(w - j, i)
                    if (abs(color0 - bottom_right0) > tol or 
                        abs(color1 - bottom_right1) > tol or 
                        abs(color2 - bottom_right2) > tol):
                            right = j
                            right_done = True
                if left_done and right_done: break
            else: continue
            break
        
        return left, top, right, bottom
    
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


# on Windows is faster to use DrawDib (VFW)
if os.name == 'nt':
    
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
    
    def InitRoutines():
        handleDib[0] = DrawDibOpen()
    
    def ExitRoutines():
        DrawDibClose(handleDib[0])
    
    
    class AvsClip(AvsClipBase):
        
        def __init__(self, *args, **kwargs):
            
            if not AvsClipBase.__init__(self, *args, **kwargs):
                return
            
            if not self.onlyRaw:
                # Prepare info header for displaying
                self.bmih = BITMAPINFOHEADER()
                avisynth.CreateBitmapInfoHeader(self.clip, self.bmih)
                self.pInfo = ctypes.pointer(self.bmih)
                #~ self.BUF=ctypes.c_ubyte*self.bmih.biSizeImage
                #~ self.pBits=self.BUF()
            
            self.initialized = True
            if __debug__:
                print "AviSynth clip created successfully: '{0}'".format(self.name)
        
        def _ConvertToRGB(self):
            if not self.IsRGB:
                arg = avisynth.AVS_Value(self.clip)
                arg1 = avisynth.AVS_Value(self.matrix)
                arg2 = avisynth.AVS_Value(self.interlaced)
                args = avisynth.AVS_Value([arg, arg1, arg2])
                try:
                    avsfile = self.env.Invoke("ConvertToRGB24", args, 0)
                    arg.Release()
                    self.clip = avsfile.AsClip(self.env)
                except avisynth.AvisynthError, err:
                    return False
            return True
        
        def _GetFrame(self, frame):
            if AvsClipBase._GetFrame(self, frame):
                self.bmih.biWidth = self.DrawPitch * 8 / self.bmih.biBitCount
                #~ row_size=src.GetRowSize()
                #~ height=self.bmih.biHeight
                #~ dst_pitch=self.bmih.biWidth*self.bmih.biBitCount/8
                #~ self.env.BitBlt(self.pBits,dst_pitch,src.GetReadPtr(),src_pitch,row_size,height)
                return True
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
                DrawDibDraw(handleDib[0], hdc, offset[0], offset[1], w, h, 
                            self.pInfo, self.pBits, 0, 0, w, h, 0)


# Use generical wxPython drawing support on other platforms
else:
    
    import wx
    
    def InitRoutines():
        pass
    
    def ExitRoutines():
        pass
    
    
    class AvsClip(AvsClipBase):
        
        def __init__(self, *args, **kwargs):
            
            if not AvsClipBase.__init__(self, *args, **kwargs):
                return
            
            self.initialized = True
            if __debug__:
                print "AviSynth clip created successfully: '{0}'".format(self.name)
        
        def _ConvertToRGB(self):
            # There's issues with RGB32, we convert to RGB24 
            # Avisynth uses BGR ordering but we need RGB
            try:
                clip = avisynth.AVS_Value(self.clip)
                if not self.IsRGB24:
                    arg1 = avisynth.AVS_Value(self.matrix)
                    arg2 = avisynth.AVS_Value(self.interlaced)
                    args = avisynth.AVS_Value([clip, arg1, arg2])
                    clip(self.env.Invoke("ConvertToRGB24", args, 0))
                r = self.env.Invoke("ShowRed", clip, 0)
                b = self.env.Invoke("ShowBlue", clip, 0)
                merge_args = avisynth.AVS_Value([b, clip, r, avisynth.AVS_Value("RGB24")])
                avsfile = self.env.Invoke("MergeRGB", merge_args, 0)
                r.Release()
                b.Release()
                clip.Release()
                self.clip = avsfile.AsClip(self.env)
                return True
            except avisynth.AvisynthError, err:
                return False
        
        def DrawFrame(self, frame, dc=None, offset=(0,0), size=None):
            if not self._GetFrame(frame):
                return
            if dc:
                if size is None:
                    w = self.Width
                    h = self.Height
                else:
                    w, h = size
                buf = ctypes.create_string_buffer(h * w * 3)
                # Use ctypes.memmove to blit the Avisynth VFB line-by-line
                read_addr = ctypes.addressof(self.pBits.contents) + (h - 1) * self.DrawPitch
                write_addr = ctypes.addressof(buf)
                P_UBYTE = ctypes.POINTER(ctypes.c_ubyte)
                for i in range(h):
                    read_ptr = ctypes.cast(read_addr, P_UBYTE)
                    write_ptr = ctypes.cast(write_addr, P_UBYTE)
                    ctypes.memmove(write_ptr, read_ptr, w * 3)
                    read_addr -= self.DrawPitch
                    write_addr += w * 3
                bmp = wx.BitmapFromBuffer(w, h, buf)
                dc.DrawBitmap(bmp, 0, 0)


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
        print 'IsYUV =', AVI.IsYUV
        print 'IsYUY2 =', AVI.IsYUY2
        print 'IsYV24 =', AVI.IsYV24
        print 'IsYV16 =', AVI.IsYV16
        print 'IsYV12 =', AVI.IsYV12
        print 'IsYV411 =', AVI.IsYV411
        print 'IsY8 =', AVI.IsY8
        print 'IsPlanar =', AVI.IsPlanar
        print 'IsInterleaved =', AVI.IsInterleaved
        print 'IsFieldBased =', AVI.IsFieldBased
        print 'IsFrameBased =', AVI.IsFrameBased
        print 'GetParity =', AVI.GetParity 
        print 'HasAudio =', AVI.HasAudio
        print 'HasVideo =', AVI.HasVideo
        #AVI._x_SaveFrame("C:\\workspace\\test_file.bmp", 100)
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
    #AVI._x_SaveFrame("C:\\workspace\\test_file2.bmp", 100)
    AVI._GetFrame(100)
    AVI = None
    env.Release()
    env = None
    
    print "Exit program."

