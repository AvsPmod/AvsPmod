# AvsP - an AviSynth editor
# Copyright 2007 Peter Jang <http://www.avisynth.org/qwerpoi>
#           2010-2012 the AvsPmod authors <http://forum.doom9.org/showthread.php?t=153248>
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

# pyavs - AVI functions via Avisynth in Python [platform-independent, wxPython only]
# Dependencies:
#     Python (tested with v2.4.2)
# Scripts:
#     avisynth.py (python Avisynth wrapper)

import sys
import os
import ctypes
import wx

import avisynth

try: _
except NameError:
    def _(s): return s
        
avsfile=None

def InitRoutines():
    pass
    
def ExitRoutines():
    pass

class AvsClip:
    def __init__(self, script, filename='', env=None, fitHeight=None, fitWidth=None, oldFramecount=240, keepRaw=False, matrix=['auto', 'tv'], interlaced=False, swapuv=False):
        # Internal variables
        self.initialized = False
        self.error_message = None
        self.current_frame = -1
        self.pBits = None
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
            except OSError:
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
            
        # Initialize display-related variables.  RGB24 allows simpler memory copy operations.
        if not self.vi.IsRGB24():
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
            if isinstance(matrix, basestring):
                arg1 = avisynth.AVS_Value(matrix)
            else:
                matrix = matrix[:]
                if matrix[0] == 'auto':
                    matrix[0] = '709' if self.HeightActual > 576 else '601'
                matrix[1] = 'Rec' if matrix[1] == 'tv' else 'PC.'
                arg1 = avisynth.AVS_Value(matrix[1] + matrix[0])
            if not self.IsYV12:
                interlaced = False
            arg2 = avisynth.AVS_Value(interlaced)
            args = avisynth.AVS_Value([arg, arg1, arg2])
            try:
                # Avisynth uses BGR ordering but we need RGB
                rgb = self.env.Invoke("converttorgb24", args, 0)
                r = self.env.Invoke("showred", rgb, 0)
                b = self.env.Invoke("showblue", rgb, 0)
                merge_args = avisynth.AVS_Value([b, rgb, r, avisynth.AVS_Value("rgb24")])
                avsfile = self.env.Invoke("mergergb", merge_args, 0)
                # Release intermediate clips
                rgb.Release()
                r.Release()
                b.Release()
                arg.Release()
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
            #~ except OSError:
                #~ return False
            # DrawPitch is the pitch of the RGB24 image for drawing.
            # pitch is the pitch of the actual raw image from clipRaw.
            self.DrawPitch=src.GetPitch()
            if self.clipRaw is not None:
                frame=self.clipRaw.GetFrame(frame)
                self.pitch = frame.GetPitch()
                self.ptrY = frame.GetReadPtr(plane=avisynth.PLANAR_Y)
                self.ptrU = frame.GetReadPtr(plane=avisynth.PLANAR_U)
                self.ptrV = frame.GetReadPtr(plane=avisynth.PLANAR_V)
            return True
        else:
            return False
            
    def DrawFrame(self, frame, dc=None, offset=(0,0), size=None):
        if not self._GetFrame(frame):
            return
        self.current_frame
        if dc:
            if size is None:
                w = self.Width
                h = self.Height
            else:
                w, h = size
            buf = ctypes.create_string_buffer(h * self.DrawPitch)
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
    AVI._GetFrame(100)
    AVI = None
    env.Release()
    env = None
    
    print "Exit program."

