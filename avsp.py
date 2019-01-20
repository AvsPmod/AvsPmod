# AvsP - an AviSynth editor
# 
# Copyright 2007 Peter Jang <http://www.avisynth.org/qwerpoi>
#           2010-2015, 2019 the AvsPmod authors <https://github.com/avspmod/avspmod>
#
# Printing support based on stcprint.py from Peppy/Editra (wxWidgets license)
# Copyright 2007 Cody Precord <staff@editra.org>
#           2009 Rob McMullen <robm@users.sourceforge.net>
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

# Dependencies:
#     Python (tested on v2.6 and 2.7)
#     wxPython (tested on v2.8 Unicode and 2.9)
#     cffi and its dependencies (only for x86-64, tested on v0.9.2)
#         pycparser
#         Visual C++
#     avisynth_c.h (only for x86-64, interface 5, or at least 3 + colorspaces 
#                   from 5, tested with the header used by x264)
# Scripts:
#     wxp.py (general wxPython framework classes)
#     avisynth.py (Python AviSynth/AvxSynth wrapper, only for x86-32)
#     avisynth_cffi.py (Python AviSynth wrapper, only for x86-64)
#     pyavs.py (AvsP AviSynth support by loading AviSynth directly as a library)
#     pyavs_avifile.py (AvsP AviSynth support through Windows AVIFile routines)
#     icon.py (icons embedded in a Python script)
#     i18n.py (internationalization and localization)
#     global_vars.py (application info and other shared variables)

import os
import sys
import platform
import traceback
import cPickle
import shutil
import string
import array
import struct
import codecs
import re
import functools
import bisect
import random, math, copy
import subprocess, shlex
import socket
import thread
import threading
import time
import StringIO
import textwrap
import ctypes
import tempfile
import zlib
import glob
import urllib2
import cgi
if os.name == 'nt':
    import _winreg
from hashlib import md5
import __builtin__
import collections

if hasattr(sys,'frozen'):
    programdir = os.path.dirname(sys.executable)
    sys.path.insert(0, programdir)

import global_vars
import i18n
messages = None
def _(s):
    if messages:
        s2 = messages.get(s, s)
        if s2:
            return s2.replace(r'\n','\n')
    return s
__builtin__._ = _
encoding = sys.getfilesystemencoding()

import wx
from wx import stc
import wx.lib.buttons as wxButtons
import  wx.lib.colourselect as  colourselect
import wxp

from icons import AvsP_icon, next_icon, play_icon, pause_icon, external_icon, \
                  skip_icon, spin_icon, ok_icon, smile_icon, question_icon, \
                  rectangle_icon, dragdrop_cursor


# Filter database for each tab
class AvsFilterDict(collections.MutableMapping):
    
    def __init__(self, shared_dict=None, own_dict=None):
        self.shared_dict = shared_dict or {}
        self.own_dict = own_dict or {}
    
    def __getitem__(self, key):
        if key in self.own_dict:
            return self.own_dict[key]
        return self.shared_dict[key]
    
    def __setitem__(self, key, value):
        return self.own_dict.__setitem__(key, value)
    
    def __delitem__(self, key):
        return self.own_dict.__delitem__(key)
        
    def __len__(self, key):
        return len(self.shared_dict) + len(self.own_dict)
    
    def __iter__(self):
        for item in self.own_dict:
            yield item
        for item in self.shared_dict:
            yield item


# Custom styled text control for avisynth language
class AvsStyledTextCtrl(stc.StyledTextCtrl):
    (
    STC_AVS_DEFAULT, STC_AVS_COMMENT, STC_AVS_ENDCOMMENT, 
    STC_AVS_BLOCKCOMMENT, STC_AVS_NUMBER, STC_AVS_NUMBERBAD,
    STC_AVS_OPERATOR, STC_AVS_STRING, STC_AVS_STRINGEOL, 
    STC_AVS_TRIPLE, STC_AVS_COREFILTER, STC_AVS_PLUGIN,
    STC_AVS_CLIPPROPERTY, STC_AVS_USERFUNCTION, STC_AVS_UNKNOWNFUNCTION, 
    STC_AVS_USERSLIDER, STC_AVS_SCRIPTFUNCTION, STC_AVS_PARAMETER, 
    STC_AVS_ASSIGN, STC_AVS_KEYWORD, STC_AVS_MISCWORD, 
    STC_AVS_DATATYPE, STC_AVS_IDENTIFIER) = range(23)
    def __init__(self, parent, app, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.SIMPLE_BORDER,
            #~ filterDict=None,
            #~ filterPresetDict=None,
            #~ keywordLists=None,
            #~ autocomplete=True,
            #~ autoparentheses=1,
            #~ usestringeol=False,
            #~ calltips=True,
            #~ frequentcalltips=True,
            #~ usetabs=False,
            #~ tabwidth=4,
            #~ highlightline=False,
            #~ highlightlinecolor=(232,232,255),
            #~ wrap=False,
            #~ numlinechars=0,
            #~ usemonospacedfont=False,
            #~ textstyles=None,
            ):
        stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style)
        self.app = app
        self.styleInfo = {
            self.STC_AVS_DEFAULT: ('default', ''),
            self.STC_AVS_COMMENT: ('comment', ',eol'),
            self.STC_AVS_ENDCOMMENT: ('endcomment', ''),
            self.STC_AVS_BLOCKCOMMENT: ('blockcomment', ''),
            self.STC_AVS_NUMBER: ('number', ''),
            self.STC_AVS_STRING: ('string', ''),
            self.STC_AVS_TRIPLE: ('stringtriple', ''),
            self.STC_AVS_COREFILTER: ('internalfilter', ''),
            self.STC_AVS_PLUGIN: ('externalfilter', ''),
            self.STC_AVS_CLIPPROPERTY: ('clipproperty', ''),
            self.STC_AVS_USERFUNCTION: ('userdefined', ''),
            self.STC_AVS_UNKNOWNFUNCTION: ('unknownfunction', ''),
            self.STC_AVS_PARAMETER: ('parameter', ''),
            self.STC_AVS_ASSIGN: ('assignment', ''),
            self.STC_AVS_OPERATOR: ('operator', ''),
            self.STC_AVS_STRINGEOL: ('stringeol', ',eol'),
            self.STC_AVS_USERSLIDER: ('userslider', ''),

            self.STC_AVS_SCRIPTFUNCTION: ('internalfunction', ''),
            self.STC_AVS_KEYWORD: ('keyword', ''),
            self.STC_AVS_MISCWORD: ('miscword', ''),

            stc.STC_STYLE_LINENUMBER: ('linenumber', ''),
            stc.STC_STYLE_BRACELIGHT: ('bracelight', ''),
            stc.STC_STYLE_BRACEBAD: ('badbrace', ''),
            self.STC_AVS_NUMBERBAD: ('badnumber', ''),

            self.STC_AVS_DATATYPE: ('datatype', ''),
        }
        self.avsfilterdict = AvsFilterDict(self.app.avsfilterdict)
        self.avsazdict = collections.defaultdict(list)
        self.styling_refresh_needed = False
        self.SetUserOptions()
        if wx.VERSION > (2, 9):
            self.SetScrollWidth(1)
            self.SetScrollWidthTracking(True)
        self.SetEOLMode(stc.STC_EOL_LF)
        #~ self.CmdKeyClear(stc.STC_KEY_TAB,0)
        self.UsePopUp(0)
        self.showLinenumbers = 1
        #~ self.enableFolding = 1
        self.calltipFilter = None
        self.calltiptext = None
        self.calltipOpenpos = None
        self.flagTextChanged = self.flagCodeFolding = False
        self.keywordStyleList = (
            self.STC_AVS_COREFILTER,
            #~ self.STC_AVS_CLIPPROPERTY,
            self.STC_AVS_PLUGIN,
            self.STC_AVS_USERFUNCTION,
            #~ self.STC_AVS_SCRIPTFUNCTION,
        )
        self.highlightwordStyleList = (
            self.STC_AVS_COREFILTER,
            self.STC_AVS_CLIPPROPERTY,
            self.STC_AVS_PLUGIN,
            self.STC_AVS_USERFUNCTION,
            self.STC_AVS_SCRIPTFUNCTION,
        )
        self.commentStyle = [self.STC_AVS_COMMENT, self.STC_AVS_BLOCKCOMMENT, self.STC_AVS_ENDCOMMENT]
        self.nonBraceStyles = [
            self.STC_AVS_COMMENT,
            self.STC_AVS_ENDCOMMENT,
            self.STC_AVS_BLOCKCOMMENT,
            self.STC_AVS_STRING,
            self.STC_AVS_TRIPLE,
            self.STC_AVS_STRINGEOL,
            self.STC_AVS_USERSLIDER,
        ]
        self.stc_attr = ( # 'eol' not supported in html export
            ('bold', 'italic', 'underline'),
            ('fore', 'back', 'face', 'size'))
        self.css_properties = {
            'bold':      'font-weight',
            'italic':    'font-style',
            'fore':      'color',
            'back':      'background-color',
            'face':      'font-family',
            'size':      'font-size',
            'underline': 'text-decoration',
        }
        # Auto-completion options
        self.AutoCompSetIgnoreCase(1)
        self.AutoCompSetDropRestOfWord(1)
        self.AutoCompSetAutoHide(1)
        self.AutoCompSetChooseSingle(0)
        self.AutoCompSetCancelAtStart(1)
        self.AutoCompSetSeparator(ord('\n'))
        self.AutoCompStops_chars = ''' `~!@#$%^&*()+=[]{};:'",<.>/?\|'''
        # Margin options
        #~ self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, self.initialMarginWidth)
        self.SetMarginWidth(1, 0)
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)        
        self.SetMarginWidth(2, 13)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY)
        self.SetSavePoint()
        # Event handling
        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(stc.EVT_STC_CHANGE, self.OnTextChange)
        self.Bind(stc.EVT_STC_CHARADDED, self.OnTextCharAdded)
        self.Bind(stc.EVT_STC_NEEDSHOWN, self.OnNeedShown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftMouseDown)
        self.Bind(stc.EVT_STC_AUTOCOMP_SELECTION, self.OnAutocompleteSelection)
        self.Bind(stc.EVT_STC_USERLISTSELECTION, self.OnUserListSelection)
        self.Bind(stc.EVT_STC_CALLTIP_CLICK, self.OnCalltipClick)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(stc.EVT_STC_ZOOM, lambda event: self.fitNumberMarginWidth())
        try:
            self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, lambda event: self.ReleaseMouse())
        except AttributeError:
            pass
        if self.GetLexer() == stc.STC_LEX_CONTAINER:
            self.Bind(stc.EVT_STC_STYLENEEDED, self.OnStyleNeeded)

    def SetUserOptions(self):
        # AviSynth filter information
        #~ if not filterDict:
            #~ filterDict = self.defineFilterDict()
            #~ filterDict = dict([(name.lower(), (name,args,ftype)) for name, (args,ftype) in filterDict.items()])
        #~ if not keywordLists:
            #~ keywords = ['default', 'end', 'return', 'global', 'function', 'last', 'true', 'false', 'try', 'catch',]
            #~ datatypes = ['clip', 'int', 'float', 'string', 'bool', 'val']
            #~ operators = ('-', '*', ',', '.', '/', ':', '?', '\\', '+', '<', '>', '=', '(', ')', '[', ']', '{', '}', '!', '%', '&', '|')
            #~ miscwords = []
            #~ keywordLists = (keywords, datatypes, operators, miscwords)
        self.SetTextStyles(self.app.options['textstyles'], self.app.options['usemonospacedfont'])
        if self.styling_refresh_needed:
            self.styling_refresh_needed = False
            self.Colourise(0, 0) # set self.GetEndStyled() to 0
        if self.app.options['autocompleteicons']:            
            self.RegisterImage(1, ok_icon.GetBitmap())
            self.RegisterImage(2, smile_icon.GetBitmap())
            self.RegisterImage(3, question_icon.GetBitmap())            
            self.RegisterImage(4, rectangle_icon.GetBitmap())
            self.RegisterImage(5, wx.ArtProvider.GetBitmap(wx.ART_FOLDER))
            self.RegisterImage(6, wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE))
        else:
            self.ClearRegisteredImages()
        # General options
        self.SetUseTabs(self.app.options['usetabs'])
        self.SetTabWidth(self.app.options['tabwidth'])
        self.SetCaretLineBack(self.app.options['textstyles']['highlightline'].split(':')[1])
        self.SetCaretLineVisible(self.app.options['highlightline'])
        if self.app.options['wrap']:
            self.SetWrapMode(stc.STC_WRAP_WORD)
        else:
            self.SetWrapMode(stc.STC_WRAP_NONE)
        self.SetFoldFlags(self.app.options['foldflag']<<4)
        if self.app.options['numlinechars']:
            self.initialMarginWidth = self.numlinechars2pixels(self.app.options['numlinechars'])
            self.fitNumberMarginWidth()
        else:
            self.initialMarginWidth = 0
            self.SetMarginWidth(0, 0)

    def defineFilterDict(self): # not used anymore, filter info is stored in MainFrame.filterdbfilename
        return {
            'AddBorders': ('(clip, int left, int top, int right, int bottom, int color)', 0),
            'Amplify': ('(clip, float amount1 [, ...])', 0),
            'AmplifydB': ('(clip, float amount1 [, ...])', 0),
            'Animate': ('(clip, int start_frame, int end_frame, string filtername, start_args, end_args)', 0),
            'ApplyRange': ('(clip, int start_frame, int end_frame, string filtername, args)', 0),
            'AssumeFrameBased': ('(clip)', 0),
            'AssumeFieldBased': ('(clip)', 0),
            'AssumeBFF': ('(clip)', 0),
            'AssumeTFF': ('(clip)', 0),
            'AssumeSampleRate': ('(clip, int samplerate)', 0),
            'AudioDub': ('(video_clip, audio_clip)', 0),
            'AVISource': ('(string filename [, ...], bool "audio", string "pixel_type")', 0),
            'OpenDMLSource': ('(string filename [, ...], bool "audio", string "pixel_type")', 0),
            'AVIFileSource': ('(string filename [, ...], bool "audio", string "pixel_type")', 0),
            'WAVSource': ('(string filename [, ...])', 0),
            'BlankClip': ('(clip clip, int "length", int "width", int "height", string "pixel_type",\nfloat "fps", int "fps_denominator", int "audio_rate", bool "stereo",\nbool "sixteen_bit", int "color")', 0),
            'Blackness': ('(clip clip, int "length", int "width", int "height", string "pixel_type",\nfloat "fps", int "fps_denominator", int "audio_rate", bool "stereo",\nbool "sixteen_bit", int "color")', 0),
            'Blur': ('(clip, float amount)', 0),
            'Sharpen': ('(clip, float amount)', 0),
            'Bob': ('(clip, float "b", float "c", float "height")', 0),
            'ColorBars': ('(int width, int height)', 0),
            'ColorYUV': ('(clip, float "gain_y", float "off_y", float "gamma_y", float "cont_y",\nfloat "gain_u", float "off_u", float "gamma_u", float "cont_u", float "gain_v",\nfloat "off_v", float "gamma_v", float "cont_v", string "levels", string "opt",\nbool "showyuv", bool "analyze", bool "autowhite", bool "autogain")', 0),
            'ComplementParity': ('(clip)', 0),
            'Compare': ('(clip_filtered, clip_original, string "channels", string "logfile", bool "show_graph")', 0),
            'ConditionalFilter': ('(clip testclip, clip source1, clip source2, string filter,\nstring operator, string value, bool ''show'')', 0),
            'FrameEvaluate': ('(clip clip, script function, bool "after_frame")', 0),
            'ScriptClip': ('(clip clip, string function, bool ''show'')', 0),
            'ConditionalReader': ('(clip clip, string filename, string variablename, bool "show")', 0),
            'ConvertBackToYUY2': ('(clip, bool "interlaced")', 0),
            'ConvertToRGB': ('(clip, bool "interlaced")', 0),
            'ConvertToRGB24': ('(clip, bool "interlaced")', 0),
            'ConvertToRGB32': ('(clip, bool "interlaced")', 0),
            'ConvertToYUY2': ('(clip, bool "interlaced")', 0),
            'ConvertToYV12': ('(clip, bool "interlaced")', 0),
            'ConvertAudioTo8bit': ('(clip)', 0),
            'ConvertAudioTo16bit': ('(clip)', 0),
            'ConvertAudioTo24bit': ('(clip)', 0),
            'ConvertAudioTo32bit': ('(clip)', 0),
            'ConvertAudioToFloat': ('(clip)', 0),
            'ConvertToMono': ('(clip)', 0),
            'Crop': ('(clip, int left, int top, int -right, int -bottom, bool "align")', 0),
            'CropBottom': ('(clip, int count, bool "align")', 0),
            'DelayAudio': ('(clip, float seconds)', 0),
            'DeleteFrame': ('(clip, int frame)', 0),
            'DirectShowSource': ('(string filename, int "fps", bool "seek", bool "audio", bool "video")', 0),
            'Dissolve': ('(clip1, clip2 [, ...], int overlap)', 0),
            'DoubleWeave': ('(clip)', 0),
            'DuplicateFrame': ('(clip, int frame)', 0),
            'EnsureVBRMP3Sync': ('(clip)', 0),
            'FadeOut': ('(clip, int frames, int "color")', 0),
            'FadeOut2': ('(clip, int frames, int "color")', 0),
            'FadeIn': ('(clip, int frames, int "color")', 0),
            'FadeIn2': ('(clip, int frames, int "color")', 0),
            'FadeIO': ('(clip, int frames, int "color")', 0),
            'FadeIO2': ('(clip, int frames, int "color")', 0),
            'FixBrokenChromaUpsampling': ('(clip)', 0),
            'FixLuminance': ('(clip, int intercept, int slope)', 0),
            'FlipHorizontal': ('(clip)', 0),
            'FlipVertical': ('(clip)', 0),
            'AssumeFPS': ('(clip, float fps, bool "sync_audio")', 0),
            'ChangeFPS': ('(clip, float fps, bool "linear")', 0),
            'ConvertFPS': ('(clip, int new_rate, int "zone", int "vbi")', 0),
            'FreezeFrame': ('(clip, int first_frame, int last_frame, int source_frame)', 0),
            'GeneralConvolution': ('(clip, int "bias", string matrix)', 0),
            'GetChannel': ('(clip, int ch1 [, int ch2, ...])', 0),
            'Greyscale': ('(clip)', 0),
            'Histogram': ('(clip, string ''mode'')', 0),
            'ImageReader': ('(string path, int begin, int end, int fps, bool "use_DevIL")', 0),
            'ImageWriter': ('(clip, string "path", int "begin", int "end", string format)', 0),
            'Info': ('(clip)', 0),
            'Interleave': ('(clip1, clip2 [, ...])', 0),
            'Invert': ('(clip, string "channels")', 0),
            'KillAudio': ('(clip)', 0),
            'Layer': ('(clip, layer_clip, string "op", int "level", int "x", int "y", int "threshold",\nbool "use_chroma")', 0),
            'Mask': ('(clip, mask_clip)', 0),
            'ResetMask': ('(clip)', 0),
            'ColorKeyMask': ('(clip, int color, int tolerance)', 0),
            'Letterbox': ('(clip, int top, int bottom, [int left, int right])', 0),
            'Levels': ('(clip, int input_low, float gamma, int input_high, int output_low, int\noutput_high, bool "coring")', 0),
            'Limiter': ('(clip, int ''min_luma'', int ''max_luma'', int ''min_chroma'', int ''max_chroma'')', 0),
            'LoadPlugin': ('(string filename)', 0),
            'Loop': ('(clip, int "times", int "start", int "end")', 0),
            'MergeChannels': ('(clip1, clip2 [, ...])', 0),
            'MergeChroma': ('(clip1, clip2, float weight)', 0),
            'MergeLuma': ('(clip1, clip2, float weight)', 0),
            'MessageClip': ('(string message, int "width", int "height", bool "shrink", int "text_color",\nint "halo_color", int "bg_color")', 0),
            'MixAudio': ('(clip1, clip 2, clip1_factor, "clip2_factor")', 0),
            'Normalize': ('(clip, float "volume", bool "show")', 0),
            'Overlay': ('(clip, clip overlay, int ''x'', int ''y'', clip ''mask'', float ''opacity'',\nstring ''mode'', bool ''greymask'', string ''output'', bool ''ignore_conditional'',\nbool ''pc_range'')', 0),
            'PeculiarBlend': ('(clip, int cutoff)', 0),
            'Pulldown': ('(clip, int a , int b)', 0),
            'RGBAdjust': ('(clip, float red, float green, float blue, float alpha)', 0),
            'HorizontalReduceBy2': ('(clip)', 0),
            'VerticalReduceBy2': ('(clip)', 0),
            'ReduceBy2': ('(clip)', 0),
            'ResampleAudio': ('(clip, int new_sample_rate)', 0),
            'BilinearResize': ('(clip, int target_width, int target_height)', 0),
            'BicubicResize': ('(clip, int target_width, int target_height, float "b", float "c")', 0),
            'LanczosResize': ('(clip, int target_width, int target_height)', 0),
            'PointResize': ('(clip, int target_width, int target_height)', 0),
            'Reverse': ('(clip)', 0),
            'SegmentedAVISource': ('(string base_filename [, ...], bool "audio")', 0),
            'SegmentedDirectShowSource': ('(string base_filename [, ...] [, fps])', 0),
            'SelectEven': ('(clip)', 0),
            'SelectOdd': ('(clip)', 0),
            'SelectEvery': ('(clip, int step_size, int offset1 [, int offset2 [, ...]])', 0),
            'SelectRangeEvery': ('(clip, int period, int range)', 0),
            'SeparateFields': ('(clip)', 0),
            'ShowAlpha': ('(clip, string pixel_type)', 0),
            'ShowFiveVersions': ('(clip1, clip2, clip3, clip4, clip5)', 0),
            'ShowFrameNumber': ('(clip, bool "scroll")', 0),
            'ShowSMPTE': ('(clip, float fps)', 0),
            'SpatialSoften': ('(clip, int radius, int luma_threshold, int chroma_threshold)', 0),
            'TemporalSoften': ('(clip, int radius, int luma_threshold, int chroma_threshold, int "scenechange",\nint "mode")', 0),
            'AlignedSplice': ('(clip1, clip2 [, ...])', 0),
            'UnAlignedSplice': ('(clip1, clip2 [, ...])', 0),
            'SSRC': ('(int samplerate, bool "fast")', 0),
            'StackHorizontal': ('(clip1, clip2 [, ...])', 0),
            'StackVertical': ('(clip1, clip2 [, ...])', 0),
            'Subtitle': ('(clip, string text, int "x", int "y", int "first_frame", int "last_frame",\nstring "font", int "size", int "text_color", int "halo_color")', 0),
            'Subtract': ('(clip1, clip2)', 0),
            'SuperEQ': ('(string filename)', 0),
            'SwapUV': ('(clip)', 0),
            'UToY': ('(clip)', 0),
            'VToY': ('(clip)', 0),
            'YToUV': ('(clip)', 0),
            'SwapFields': ('(clip)', 0),
            'Tone': ('(float "length", float "frequency", int "samplerate", int "channels", string "type")', 0),
            'Trim': ('(clip, int first_frame, int last_frame)', 0),
            'TurnLeft': ('(clip)', 0),
            'TurnRight': ('(clip)', 0),
            'Tweak': ('(clip, float "hue", float "sat", float "bright", float "cont", bool "coring")', 0),
            'Version': ('()', 0),
            'Weave': ('(clip)', 0),
        }

        #~ # Currently FunctionNames, ClipProperties, and KeyWords are unused
        #~ self.FunctionNames = ['floor', 'ceil', 'round', 'int', 'float', 'frac', 'abs', 'sign',
                                       #~ 'hexvalue', 'sin', 'cos', 'pi', 'log', 'exp', 'pow', 'sqrt', 'rand', 'spline',
                                       #~ 'ucase', 'lcase', 'revstr', 'strlen', 'findstr', 'leftstr', 'midstr',
                                       #~ 'versionnumber', 'versionstring', 'chr', 'time', 'value', 'string',
                                       #~ 'isbool', 'isint', 'isfloat', 'isstring', 'isclip',
                                       #~ 'select', 'defined', 'default', 'exist', 'eval', 'apply', 'import', 'try', 'catch',
                                       #~ 'setmemorymax', 'setworkingdir']
        #~ self.ClipProperties = ['width', 'height', 'framecount', 'framerate',
                                     #~ 'audiorate', 'audiolength', 'audiochannels', 'audiobits',
                                     #~ 'isrgb', 'isrgb24', 'isrgb32', 'isyuy2', 'isyuv',
                                     #~ 'isplanar', 'isinterleaved', 'isfieldbased', 'isframebased', 'getparity']
        #~ self.KeyWords = tuple(' '.join(self.FilterNames).lower().split(' '))
    
    def ParseFunctions(self, text=None, refresh_highlighting=False):
        if text is None:
            text = self.GetText()
        filterInfo = self.app.ParseAvisynthScript(script_text=text, quiet=True) or []
        self.avsfilterdict.clear()
        self.avsfilterdict.update(dict(
            [
            (filtername.lower(), (filterargs, self.STC_AVS_USERFUNCTION, filtername, None))
            for filename, filtername, filterargs, ftype in filterInfo
            ]
        ))
        self.avsazdict = self.app.GetAutocompleteDict(self.avsfilterdict.own_dict)
        if refresh_highlighting:
            self.Colourise(0, 0)
    
    def SetTextStyles(self, textstyles, monospaced=False):
        self.SetLexer(stc.STC_LEX_CONTAINER)
        #~ self.commentStyle = [self.STC_AVS_COMMENT, self.STC_AVS_BLOCKCOMMENT, self.STC_AVS_ENDCOMMENT]
        #~ self.nonBraceStyles = [
            #~ self.STC_AVS_COMMENT,
            #~ self.STC_AVS_ENDCOMMENT,
            #~ self.STC_AVS_BLOCKCOMMENT,
            #~ self.STC_AVS_STRING,
            #~ self.STC_AVS_TRIPLE,
            #~ self.STC_AVS_STRINGEOL,
            #~ self.STC_AVS_USERSLIDER,
        #~ ]
        default = 'font:Arial, size:10, fore:#000000, back:#FFFFFF'

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, textstyles.get('default', default))
        #~ if textstyles.get('default', default).endswith('bold'):
            #~ self.StyleSetBold(stc.STC_STYLE_DEFAULT, 1)
        #~ else:
            #~ self.StyleSetBold(stc.STC_STYLE_DEFAULT, 0)
        if monospaced:
            face = ''
            size = ''
            for item in textstyles['monospaced'].split(','):
                if item.lower().startswith('face:'):
                    face = item.split(':')[1]
                if item.lower().startswith('size:'):
                    size = int(item.split(':')[1])
            self.StyleSetFaceName(stc.STC_STYLE_DEFAULT, face)
            self.StyleSetSize(stc.STC_STYLE_DEFAULT, size)
        self.StyleClearAll()  # Reset all to be like the default

        for style, (key, extra) in self.styleInfo.iteritems():
            self.StyleSetSpec(style, textstyles.get(key, default) + extra)
            if monospaced:
                self.StyleSetFaceName(style, face)
                self.StyleSetSize(style, size)
        # Set miscellaneous non-style colors
        for key in ('calltip', 'calltiphighlight'):
            value = textstyles[key]
            for elem in value.split(','):
                if elem.startswith('fore:'):
                    if key == 'calltip':
                        self.CallTipSetForeground(elem.split(':')[1].strip())
                    else:
                        self.CallTipSetForegroundHighlight(elem.split(':')[1].strip())
                if elem.startswith('back:'):
                    self.CallTipSetBackground(elem.split(':')[1].strip())
        self.SetCaretForeground(textstyles['cursor'].split(':')[1])
        for elem in textstyles['highlight'].split(','):
            if elem.startswith('fore:'):
                if self.app.options['highlight_fore']:
                    self.SetSelForeground(True, elem.split(':')[1].strip())
                else:
                    self.SetSelForeground(False, wx.WHITE)
            elif elem.startswith('back:'):
                self.SetSelBackground(True, elem.split(':')[1].strip())
        fore = back = None
        for elem in textstyles['foldmargin'].split(','):
            if elem.startswith('fore:'):
                fore = elem.split(':')[1].strip()
            elif elem.startswith('back:'):
                back = elem.split(':')[1].strip()
                self.SetFoldMarginColour(True, back)
                self.SetFoldMarginHiColour(True, back)
        fore = fore or 'white'
        back = back or 'black'
        self.MarkerSetForeground(stc.STC_MARKNUM_FOLDEROPEN, fore)
        self.MarkerSetBackground(stc.STC_MARKNUM_FOLDEROPEN, back)
        self.MarkerSetForeground(stc.STC_MARKNUM_FOLDER, fore)
        self.MarkerSetBackground(stc.STC_MARKNUM_FOLDER, back)
        self.MarkerSetForeground(stc.STC_MARKNUM_FOLDERSUB, fore)
        self.MarkerSetBackground(stc.STC_MARKNUM_FOLDERSUB, back)
        self.MarkerSetForeground(stc.STC_MARKNUM_FOLDERTAIL, fore)
        self.MarkerSetBackground(stc.STC_MARKNUM_FOLDERTAIL, back)
        self.MarkerSetForeground(stc.STC_MARKNUM_FOLDEREND, fore)
        self.MarkerSetBackground(stc.STC_MARKNUM_FOLDEREND, back)
        self.MarkerSetForeground(stc.STC_MARKNUM_FOLDEROPENMID, fore)
        self.MarkerSetBackground(stc.STC_MARKNUM_FOLDEROPENMID, back)
        self.MarkerSetForeground(stc.STC_MARKNUM_FOLDERMIDTAIL, fore)
        self.MarkerSetBackground(stc.STC_MARKNUM_FOLDERMIDTAIL, back)
    
    def numlinechars2pixels(self, numlinechars):
        return self.TextWidth(stc.STC_STYLE_LINENUMBER, '%s' % ('0'*numlinechars)) + 12

    def fitNumberMarginWidth(self):
        # Update line number margin width
        w = self.TextWidth(stc.STC_STYLE_LINENUMBER, '%s' % str(self.GetLineCount())) + 12
        w = max(w, self.initialMarginWidth)
        if w != self.GetMarginWidth(0):
            self.SetMarginWidth(0, w)

    # New utility functions
    def ShowQuickFindDialog(self):
        if self.app.findDialog.IsShown():
            self.app.findDialog.SetFocus()
        else:
            x0, y0 = self.app.currentScript.GetScreenPosition()
            w0, h0 = self.app.currentScript.GetSize()
            w, h = self.app.findDialog.GetSize()
            self.app.findDialog.SetPosition((x0 + w0 - w - 5, y0 + 5))
            self.app.findDialog.Show()
            self.app.findDialog.SetFocus()
        text = self.GetSelectedText()
        if text:
            self.app.findDialog.UpdateText(text)
    
    def ShowFindReplaceDialog(self, find=False):
        self.app.findDialog.Hide()
        text = self.GetSelectedText()
        if self.app.replaceDialog.IsShown():
            self.app.replaceDialog.SetFocus()
            if text:
                if '\n' in text.strip():
                    self.app.replaceDialog.only_selection.SetValue(True)
                else:
                    ctrl = 'find' if find else 'replace'
                    self.app.replaceDialog.UpdateText(text, ctrl)
        else:
            self.app.replaceDialog.Show()
            if text:
                if '\n' in text.strip():
                    self.app.replaceDialog.only_selection.SetValue(True)
                else:
                    self.app.replaceDialog.UpdateText(text, 'find')
    
    def FindNext(self):
        if self.AutoCompActive():
            self.AutoCompCancel()
        if self.app.replaceDialog.GetFindText():
            self.app.replaceDialog.OnFindNext()
        elif self.app.replaceDialog.IsShown():
            self.ShowFindReplaceDialog()
        else:
            text = self.GetSelectedText()
            if text:
                self.app.findDialog.UpdateText(text)
                self.app.replaceDialog.OnFindNext()
            else:
                self.ShowQuickFindDialog()
    
    def FindPrevious(self):
        if self.AutoCompActive():
            self.AutoCompCancel()
        if self.app.replaceDialog.GetFindText():
            self.app.replaceDialog.OnFindPrevious()
        elif self.app.replaceDialog.IsShown():
            self.ShowFindReplaceDialog()
        else:
            text = self.GetSelectedText()
            if text:
                self.app.findDialog.UpdateText(text)
                self.app.replaceDialog.OnFindPrevious()
            else:
                self.ShowQuickFindDialog()
    
    def ReplaceNext(self):
        if self.AutoCompActive():
            self.AutoCompCancel()
        if self.app.replaceDialog.GetReplaceText():
            if self.app.replaceDialog.GetFindText():
                self.app.replaceDialog.OnReplace()
            else:
                text = self.GetSelectedText()
                if text:
                    self.app.replaceDialog.UpdateText(text, 'find')
                    self.app.replaceDialog.OnReplace()
                else:
                    self.ShowFindReplaceDialog()
        else:
            self.ShowFindReplaceDialog()
    
    def IndentSelection(self):
        self.CmdKeyExecute(stc.STC_CMD_TAB)

    def UnIndentSelection(self):
        self.CmdKeyExecute(stc.STC_CMD_BACKTAB)

    def BlockComment(self):
        line1 = self.LineFromPosition(self.GetSelectionStart())
        line2 = self.LineFromPosition(self.GetSelectionEnd())
        self.BeginUndoAction()
        for line in xrange(line1, line2+1):
            txt = self.GetLine(line)
            if txt.strip():
                pos = self.PositionFromLine(line) + len(txt) - len(txt.lstrip())
                if txt.strip().startswith('#~ '):
                    self.SetTargetStart(pos)
                    self.SetTargetEnd(pos+3)
                    self.ReplaceTarget('')
                else:
                    self.SetTargetStart(pos)
                    self.SetTargetEnd(pos)
                    self.ReplaceTarget('#~ ')
        self.EndUndoAction()
        
    def StyleComment(self):
        pos = self.GetCurrentPos()
        start = self.PositionFromLine(self.LineFromPosition(pos))
        style = self.GetStyleAt(pos)
        if style == self.STC_AVS_COMMENT:
            while pos > start and self.GetStyleAt(pos-1) == self.STC_AVS_COMMENT:
                pos -= 1
            self.SetTargetStart(pos)
            if self.GetTextRange(pos, pos+3) == '#~ ':                
                self.SetTargetEnd(pos+3)
            else:
                self.SetTargetEnd(pos+1)
            self.ReplaceTarget('')
        else:
            if pos > start and unichr(self.GetCharAt(pos)) == '.' and self.GetStyleAt(pos-1) == self.STC_AVS_NUMBER:
                pos -= 1
                style = self.STC_AVS_NUMBER
            while pos > start and self.GetStyleAt(pos-1) == style:
                pos -= 1
            if pos > start and unichr(self.GetCharAt(pos-1)) == '.':
                pos -= 1
            if style == self.STC_AVS_NUMBER:
                while pos > start and self.GetStyleAt(pos-1) == style:
                    pos -= 1
                if pos > start and unichr(self.GetCharAt(pos-1)) in '+-':
                    pos -= 1
            self.InsertText(pos, '#~ ')                

    def MoveSelectionByOneLine(self, up=True):
        selA = self.GetSelectionStart()
        selB = self.GetSelectionEnd()
        line1 = self.LineFromPosition(selA)
        line2 = self.LineFromPosition(selB)
        numlines = self.GetLineCount()
        if line2 == numlines - 1:
            if selB != self.GetLength() or selB != self.PositionFromLine(line2):
                self.InsertText(self.GetLineEndPosition(line2), '\n')
        posA = self.PositionFromLine(line1)
        if self.GetSelectionEnd() == self.PositionFromLine(line2) and selA != selB:
            posB = self.PositionFromLine(line2)
        else:
            posB = self.PositionFromLine(line2 + 1)
        if up:
            newline = max(line1 - 1, 0)
        else:
            newline = min(line1 + 1, numlines-1 - (line2 - line1))
        if newline == line1:
            return
        if newline == self.GetLineCount() - 1 and self.GetLine(newline) != '':
                self.InsertText(self.GetLineEndPosition(newline), '\n')
        self.BeginUndoAction()
        self.SetSelection(posA, posB)
        txt = self.GetSelectedText()
        self.ReplaceSelection('')
        newpos = self.PositionFromLine(newline)
        self.GotoPos(newpos)
        self.ReplaceSelection(txt)
        self.SetSelection(newpos, newpos+len(txt))
        self.EndUndoAction()

    def ShowAutocomplete(self, all=False, auto=0):
        pos = self.GetCurrentPos()
        startwordpos = self.WordStartPosition(pos,1)
        if pos == startwordpos:
            return
        word = self.GetTextRange(startwordpos,pos)
        #~ if len(word) == 0:
            #~ return
        keywords = []
        wordlower = word.lower()
        avsazdict = self.app.avsazdict_all if all else self.app.avsazdict
        first_chr = word[0].lower()
        for keyword in set(avsazdict[first_chr] + self.avsazdict[first_chr]):
            if keyword.lower().startswith(wordlower):
                keywords.append(keyword)
        if self.app.options['autocompletevariables']:
            lineCount = self.LineFromPosition(pos)
            line = 0
            while line <= lineCount:
                if line == lineCount:
                    line += 1
                    lineCount = self.GetLineCount()
                    continue
                start = self.PositionFromLine(line)
                eol = self.GetLineEndPosition(line)
                #~ while unichr(self.GetCharAt(eol-1)) == '\\' or unichr(self.GetCharAt(eol+1)) == '\\':
                    #~ line += 1
                    #~ if line >= lineCount:
                        #~ break
                    #~ eol = self.GetLineEndPosition(line)
                while line < lineCount - 1 and (self.FindText(self.PositionFromLine(line), eol, r'\\[ ]*$', stc.STC_FIND_REGEXP) != -1 or \
                                                self.FindText(eol+1, self.GetLineEndPosition(line+1), r'^[ ]*\\', stc.STC_FIND_REGEXP) != -1):
                    line += 1
                    eol = self.GetLineEndPosition(line)
                start = self.FindText(start, eol, r'\<', stc.STC_FIND_REGEXP)
                while start != -1 and self.GetStyleAt(start) == self.STC_AVS_BLOCKCOMMENT:
                    end = self.WordEndPosition(start, 1)
                    start = self.FindText(end, eol, r'\<', stc.STC_FIND_REGEXP)
                if start == -1:
                    line += 1
                    continue
                end = self.WordEndPosition(start, 1)
                keyword = self.GetTextRange(start, end)
                #~ print keyword
                if self.GetStyleAt(start) == self.STC_AVS_ASSIGN and keyword.lower().startswith(wordlower) and keyword not in keywords:
                    keywords.append(keyword)
                elif keyword == 'global' or keyword == 'function':
                    start = self.FindText(end, self.GetLineEndPosition(line), r'\<', stc.STC_FIND_REGEXP)
                    if start == -1:
                        line += 1
                        continue
                    end = self.WordEndPosition(start, 1)
                    keyword = self.GetTextRange(start, end)
                    if keyword.lower().startswith(wordlower) and keyword not in keywords:
                        keywords.append(keyword)
                line += 1
            keywords.sort(key=lambda s: s.lower())
        if keywords:            
            if auto != 2 or (len(keywords) == 1 and len(keywords[0]) != len(word)):
                if self.app.options['autocompleteicons']:
                    for i in range(len(keywords)):
                        keyword = keywords[i].lower()
                        if keyword not in self.avsfilterdict:
                            keywords[i] += '?4'
                            continue
                        keyword = self.avsfilterdict[keyword][3] or keyword
                        preset = self.app.options['filterpresets'].get(keyword)
                        if preset is None:
                            preset = self.CreateDefaultPreset(keywords[i])
                        question = preset.count('?')
                        comma = preset.count(',')
                        if question == 0:
                            keywords[i] += '?1'
                        elif question == 1 or question*10 <= (comma+1)*3:
                            keywords[i] += '?2'                        
                        elif comma <= 1:
                            pass
                        elif question*10 >= (comma+1)*7:
                            keywords[i] += '?3'                
                self.autocomplete_case = 'function'
                self.AutoCompStops(self.AutoCompStops_chars)
                self.AutoCompShow(len(word), '\n'.join(keywords))
                if self.CallTipActive():
                    self.CallTipCancelCustom()
            #~ if len(keywords) == 1:
                #~ self.FinishAutocomplete()
        elif auto == 0 and pos - startwordpos > 0:
            self.CmdKeyExecute(stc.STC_CMD_CHARLEFT)
            wx.CallAfter(self.ShowAutocomplete)

    def FinishAutocomplete(self, key=None):
        self.AutoCompComplete()
        pos = self.GetCurrentPos()
        startwordpos = self.WordStartPosition(pos,1)
        filtername = self.GetTextRange(startwordpos,pos)
        if filtername.lower() not in self.avsfilterdict:
            return
        boolActivatePreset = (
            self.app.options['presetactivatekey'] == 'tab' and key == wx.WXK_TAB or
            self.app.options['presetactivatekey'] == 'return' and key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) or
            self.app.options['presetactivatekey'] == 'both')
        if boolActivatePreset:
            keyword = filtername.lower()
            keyword = self.avsfilterdict[keyword][3] or keyword
            preset = self.app.options['filterpresets'].get(keyword)
            boolHighlightQuestionMarks = True
            if preset is not None:
                self.SetSelection(startwordpos, pos)
                self.ReplaceSelection(preset)
                cursorTag = '[|]'
                nCursorTags = preset.count(cursorTag)
                if nCursorTags > 0:
                    minPos = startwordpos
                    maxPos = self.GetCurrentPos()
                    startSelectionPos = endSelectionPos = None
                    for i in xrange(nCursorTags):
                        findpos = self.FindText(minPos, maxPos, cursorTag, stc.STC_FIND_MATCHCASE)
                        if findpos != -1:
                            self.SetSelection(findpos, findpos + len(cursorTag))
                            self.ReplaceSelection('')
                            endSelectionPos = findpos
                            if startSelectionPos is None:
                                startSelectionPos = findpos
                            minPos = findpos
                            maxPos -= len(cursorTag)
                        else:
                            break
                    if startSelectionPos is not None and endSelectionPos is not None:
                        self.SetSelection(startSelectionPos, endSelectionPos)
                        boolHighlightQuestionMarks = False
            else:
                preset = self.CreateDefaultPreset(filtername)
                self.SetSelection(startwordpos, pos)
                self.ReplaceSelection(preset)
            if boolHighlightQuestionMarks:
                minPos = self.WordEndPosition(pos,1)
                maxPos = self.GetCurrentPos()
                findpos = self.FindText(minPos, maxPos, '?')#, stc.STC_FIND_MATCHCASE)
                if findpos != -1:
                    self.SetSelection(findpos, findpos+1)
            return
        args = self.avsfilterdict[filtername.lower()][0]
        if not args:
            return
        if args == '()':
            self.InsertText(pos,'()')
            self.GotoPos(pos+2)
            return
        level = self.app.options['autoparentheses']
        if unichr(self.GetCharAt(pos)) == '(':
            level = 0
        if level==0:
            pass
        elif level==1:
            self.InsertText(pos,'(')
            self.GotoPos(pos+1)
        elif level==2:
            self.InsertText(pos,'()')
            self.GotoPos(pos+1)
    
    def AutocompleteFilename(self):
        """Autocomplete a filename string, showing choices if necessary"""
        pos = self.GetCurrentPos()
        str_range = self.GetStringRange(pos)
        if not str_range:
            return
        start, end = str_range
        if self.GetStyleAt(start) == self.STC_AVS_TRIPLE: # only current line
            line = self.LineFromPosition(pos)
            start = max(start, self.PositionFromLine(line))
            end = min(end, self.GetLineEndPosition(line))
        ac_str = self.GetTextRange(start, pos)
        prefix = '' if os.path.isabs(ac_str) else self.workdir
        if os.path.isdir(os.path.join(prefix, ac_str)):
            dir = ac_str
            base = ''
        else:
            dir, base = os.path.split(ac_str)
        try:
            filenames = sorted([path for path in os.listdir(os.path.join(prefix, dir) or unicode(os.curdir)) 
                                if not base or os.path.normcase(path).startswith(os.path.normcase(base))], 
                               key=lambda s: s.upper())
        except OSError:
            return
        if filenames:
            if len(filenames) == 1:
                self.AutocompleteReplaceText(start, end, prefix, os.path.join(dir, filenames[0]))
            else:
                self.autocomplete_params = pos, start, end, prefix, dir
                if self.app.options['autocompleteicons']:
                    filenames = [u'{0}?{1}'.format(file, 5 if os.path.isdir(os.path.join(prefix, dir, file)) 
                                 else 6) for file in filenames]
                self.autocomplete_case = 'filename'
                self.AutoCompStops('')
                self.AutoCompShow(len(base), '\n'.join(filenames))
                if self.CallTipActive():
                    self.CallTipCancelCustom()
    
    def AutocompleteReplaceText(self, start, end, prefix, new_text):
        """Used on filename autocomplete, instead of the default handler"""
        if new_text != self.GetTextRange(start, end):
            self.SetTargetStart(start)
            self.SetTargetEnd(end)
            new_end = start + self.ReplaceTarget(new_text)
            self.GotoPos(new_end)
        else:
            self.GotoPos(end)
        if os.path.isdir(os.path.join(prefix, new_text)):
            def autocomplete_again():
                wx.GetApp().Yield(True)
                self.AutocompleteFilename()
            wx.CallAfter(autocomplete_again)
    
    def AutocompleteParameterName(self):
        """Autocomplete parameter name in a function call"""
        pos = self.GetCurrentPos()
        openpos = self.GetOpenParenthesesPos(pos - 1)
        if openpos is None:
            return
        wordstartpos = self.WordStartPosition(openpos, 1)
        if openpos == wordstartpos:
            wordstartpos = self.WordStartPosition(self.WordStartPosition(openpos, 0), 1)
        if wordstartpos != -1:
            matched_args = {}
            arg_start_pos = self.WordStartPosition(pos, 1)
            chrs = self.GetTextRange(arg_start_pos, pos).lower()
            function_name = self.GetTextRange(wordstartpos, openpos).strip()
            args_script = [arg[0].lower() for arg in self.GetFilterScriptArgInfo(openpos) or []]
            for arg_type, arg_name, arg_info in ((arg[1], arg[2].strip('"'), arg[5]) for arg in 
                             self.GetFilterCalltipArgInfo(function_name) or []
                             if arg[2].startswith('"') and arg[2].endswith('"')):
                arg_name_lower = arg_name.lower()
                if arg_name_lower.startswith(chrs) and arg_name_lower not in args_script:
                    matched_args[arg_name] = arg_type, arg_info
            if matched_args:
                if len(matched_args) == 1:
                    arg_name, (arg_type, arg_info) = matched_args.items()[0]
                    if unichr(self.GetCharAt(pos)) == '=':
                        new_text = arg_name
                    else:
                        new_text = arg_name + '='
                    self.SetTargetStart(arg_start_pos)
                    self.SetTargetEnd(self.WordEndPosition(pos, 1))
                    self.GotoPos(arg_start_pos + self.ReplaceTarget(new_text))
                    self.AutocompleteParameterValue(arg_type, arg_info)
                else:
                    args = matched_args.keys()
                    args.sort(key=lambda s: s.upper())
                    self.autocomplete_case = 'parameter name'
                    self.autocomplete_params = matched_args
                    self.AutoCompStops(self.AutoCompStops_chars)
                    self.AutoCompShow(len(chrs), '\n'.join(args))
                    if self.CallTipActive():
                        self.CallTipCancelCustom()
    
    def AutocompleteParameterValue(self, arg_type=None, arg_info=None):
        """Autocomplete parameter name in a function call"""
        if arg_type is None or arg_info is None:
            pos = self.GetCurrentPos()
            openpos = self.GetOpenParenthesesPos(pos - 1)
            if openpos is None:
                return
            wordstartpos = self.WordStartPosition(openpos, 1)
            if openpos == wordstartpos:
                wordstartpos = self.WordStartPosition(self.WordStartPosition(openpos, 0), 1)
            if wordstartpos != -1:
                matched_args = self.GetFilterMatchedArgs(wordstartpos)[self.cursorFilterScriptArgIndex][1]
                arg_info = self.GetFilterCalltipArgInfo(calltip=matched_args)[0]
                arg_type, arg_info = arg_info[1], arg_info[-1]
        if arg_type is not None and arg_info is not None:
            value_list = self.GetParameterValues(arg_type, arg_info)
            if value_list:
                self.autocomplete_case = 'parameter value'
                self.AutoCompStops('')
                self.AutoCompShow(0, '\n'.join(value_list))
                if self.CallTipActive():
                    self.CallTipCancelCustom()
    
    @staticmethod
    def GetParameterValues(arg_type, arg_info):
        if arg_type == 'bool':
            return ['true', 'false']
        elif arg_type in ('int', 'string'):
            if arg_type == 'string' and arg_info.startswith('"'):
                arg_info = arg_info[arg_info[1:].index('"') + 2:]
            start = arg_info.find('(')
            if start == -1:
                return
            arg_info = arg_info[start + 1:]
            value_list = [value.strip() for value in 
                          arg_info.strip(' )').split('/')]
            if len(value_list) > 1:
                return value_list
    
    def InsertSnippet(self):
        pos = self.GetCurrentPos()
        start = self.WordStartPosition(pos, 1)
        end = self.WordEndPosition(pos, 1)
        word = self.GetTextRange(start, end)
        if word in self.app.options['snippets']:
            text = self.app.options['snippets'][word]
            if text:
                self.SetTargetStart(start)
                self.SetTargetEnd(end)
                self.GotoPos(start + self.ReplaceTarget(text))
        else:
            if self.AutoCompActive():
                self.CmdKeyExecute(wx.stc.STC_CMD_CANCEL)
                if self.autocomplete_case == 'snippet':
                        return
            tag_list = [tag for tag, text in self.app.options['snippets'].iteritems() if text]
            if tag_list:
                self.autocomplete_case = 'snippet'
                self.autocomplete_params = pos
                self.UserListShow(1, '\n'.join(sorted(tag_list)))    
    
    def UpdateCalltip(self, force=False):
        caretPos = self.GetCurrentPos()
        # Cancel under certain conditions
        boolHasFocus = (self.app.FindFocus() == self)
        boolIsComment = (self.GetStyleAt(caretPos - 1) in self.commentStyle)
        if not self.app.options['calltips'] or not boolHasFocus or self.AutoCompActive() or boolIsComment:
            self.CallTipCancelCustom()
            return
        # Determine the positions of the filter within the script
        openpos = self.GetOpenParenthesesPos(caretPos-1)
        if openpos is None:
            if force:
                openpos = self.WordEndPosition(caretPos,1) #+ 1
            else:
                self.CallTipCancelCustom()
                return
        closepos = self.BraceMatch(openpos)
        if closepos == -1:
            closepos = self.GetLength()
        # Set the force flag to true if there's an appropriate highlight
        selA, selB = self.GetSelection()
        if selA != selB:
            if selA >= openpos and selB <= closepos+1:
                force = True
            else:
                self.CallTipCancelCustom()
                return
        startwordpos = self.WordStartPosition(self.WordStartPosition(openpos, 0), 1)
        endwordpos = self.WordEndPosition(startwordpos, 1)
        # Show the calltip
        self.calltipFilter = None
        word = self.GetTextRange(startwordpos, endwordpos)
        iArgPos = None
        #~ if word.lower() in self.filterDict:
        if self.GetStyleAt(startwordpos) in self.highlightwordStyleList:
            # Show the calltip
            wordWidth = self.TextWidth(stc.STC_STYLE_DEFAULT, '%s(' % word)
            spaceWidth = self.TextWidth(stc.STC_STYLE_DEFAULT, ' ')
            spaces = ' ' * int(round(wordWidth / float(spaceWidth)))
            #~ args = self.FilterNameArgs[word.lower()]
            args = self.avsfilterdict[word.lower()][0]
            if args  in ('', '()'):
                self.CallTipCancelCustom()
                self.calltipFilter = word
                return
            # Get the argument index based on the cursor position
            self.cursorFilterScriptArgIndex = None
            filterMatchedArgs = self.GetFilterMatchedArgs(startwordpos, args)
            try:
                iArgPos = filterMatchedArgs[self.cursorFilterScriptArgIndex][0]
            except IndexError:
                iArgPos = None
            boolOutOfOrder = False
            if iArgPos is not None:
                currentArgName = filterMatchedArgs[self.cursorFilterScriptArgIndex][2]
                if not currentArgName:
                    for item in filterMatchedArgs[:self.cursorFilterScriptArgIndex]:
                        if item[2]:
                            boolOutOfOrder = True
                            break
            # TODO: fix iArgPos to not be None if unfinished arg...?
            # Format the calltip
            splitargs = args.split('\n\n', 1)
            tempList = []
            for iTemp, tempInfo in enumerate(self.GetFilterCalltipArgInfo(calltip=splitargs[0])):
                cArgTotal, cArgType, cArgName, boolMulti, boolOptional, cArgInfo = tempInfo
                s = '%s %s' % (cArgType, cArgName)
                if iTemp == iArgPos and cArgInfo and not boolOutOfOrder:
                    s += '=%s' % cArgInfo
                if boolMulti:
                    s += ' [, ...]'
                tempList.append(s)
            args0 = '(%s)' % (','.join(tempList))
            args0 = self.app.wrapFilterCalltip(args0)
            args0 = args0.replace('\n', '\n'+spaces)
            if len(splitargs) == 2:
                args = '%s\n\n%s' % (args0, splitargs[1])
            else:
                args = args0
            text = '%s%s' % (word, args)
            if self.LineFromPosition(startwordpos) == self.GetCurrentLine():
                showpos = startwordpos
            else:
                showpos = self.PositionFromLine(self.LineFromPosition(caretPos))
            xpoint, ypoint = self.PointFromPosition(showpos)
            #~ if text != self.calltiptext:
                #~ self.CallTipCancelCustom()
                #~ return
            if openpos == self.calltipOpenpos or self.flagTextChanged:
                force = True
            if self.app.options['frequentcalltips'] or force:# or (charBefore and unichr(charBefore) == '('):
                if xpoint >= 0:
                    self.CallTipShow(showpos, text)
                else:
                    xpoint = self.GetMarginWidth(0) + self.GetMarginWidth(1) + self.GetMarginWidth(2)
                    newpos = self.PositionFromPoint(wx.Point(xpoint, ypoint))
                    self.CallTipShow(newpos, text)
            self.calltiptext = text
            self.calltipFilter = word
        if self.CallTipActive():
            self.calltipOpenpos = openpos
            # BOLD THE CURRENT ARGUMENT
            a, b = 1,1
            if iArgPos is not None and not boolOutOfOrder:
                # Get the calltip arguments text positions
                try:
                    calltiptext = text
                except UnboundLocalError:
                    return
                openpos = calltiptext.find('(')
                if openpos == -1:
                    return
                argPosList = []
                startpos = openpos+1
                stoppos = startpos
                nopenSquare = 0
                argString = calltiptext[stoppos:]
                imax = len(argString)-1
                for i, c in enumerate(argString):
                    if c == '[':
                        nopenSquare += 1
                    if c == ']':
                        nopenSquare -= 1
                    if nopenSquare > 0:
                        c = 'x'
                    if c == ',' or i == imax:
                        argPosList.append((startpos, stoppos))
                        startpos = stoppos + 1
                    stoppos += 1
                if len(argPosList) == 1 and iArgPos == 1:
                    pass
                else:
                    try:
                        a, b = argPosList[iArgPos]
                    except IndexError:
                        if __debug__:
                            print>>sys.stderr, 'Error in UpdateCalltip: invalid iArgPos'
            self.CallTipSetHighlight(a,b)
        else:
            self.calltipOpenpos = None

    def CallTipCancelCustom(self):
        self.CallTipCancel()
        self.calltipFilter = None
        self.calltiptext = None
        self.calltipOpenpos = None

    def GetOpenParenthesesPos(self, pos):
        boolInside = False
        nclose = 1
        stylesToSkip = (self.STC_AVS_STRING, self.STC_AVS_TRIPLE, self.STC_AVS_USERSLIDER)
        while pos >= 0:
            c = unichr(self.GetCharAt(pos))
            if self.GetStyleAt(pos) not in stylesToSkip:
                if c == ')':
                    nclose += 1
                if c == '(':
                    nclose -= 1
                if c == '\n':
                    current = self.GetLine(self.LineFromPosition(pos)).strip()
                    next = self.GetLine(self.LineFromPosition(pos+1)).strip()
                    if not current.endswith('\\') and not next.startswith('\\'):
                        # this is a not a multiline statement
                        # either an error or we weren't inside a function call to begin with
                        return None
            if nclose == 0:
                if self.GetStyleAt(pos) in self.commentStyle:
                    return None
                else:
                    return pos
            pos -= 1
        return None

    def GetFilterMatchedArgs(self, startwordpos, calltip=None):
        if calltip is None:
            filterName = self.GetTextRange(startwordpos, self.WordEndPosition(startwordpos, 1))
            calltip = self.avsfilterdict[filterName.lower()][0].split('\n\n')[0]
        # Get both argument lists
        filterCalltipArgInfo = self.GetFilterCalltipArgInfo(calltip=calltip)
        filterScriptArgInfo = self.GetFilterScriptArgInfo(startwordpos, calltip=calltip)
        # Determine if clip passed via "dot" operator
        isClipPrePassed = False
        try:
            firstType = filterCalltipArgInfo[0][1]
        except IndexError:
            return []
        if firstType == 'clip':
            preText = self.GetAviSynthLine(startwordpos, preSectionOnly=True)
            if preText.strip().endswith('.'):
                isClipPrePassed = True
            elif filterScriptArgInfo is not None and filterScriptArgInfo[0][1] == '?':
                isClipPrePassed = True
            else:
                lastClipIndex = 0
                for i, argInfo in enumerate(filterCalltipArgInfo):
                    if argInfo[1] != 'clip':
                        break
                    lastClipIndex = i
                try:
                    if filterScriptArgInfo is not None:
                        if filterScriptArgInfo[lastClipIndex][2] not in ('clip', 'var'):
                            isClipPrePassed = True
                    else:
                        isClipPrePassed = True
                except IndexError:
                    pass
        clipOffset = int(isClipPrePassed)
        if filterScriptArgInfo is None:
            return [(clipOffset, '', '', '')]
        # Match arguments
        calltipArgNames = [info[2].strip('"').lower() for info in filterCalltipArgInfo]
        maxCalltipIndex = len(filterCalltipArgInfo) - 1
        multiType = None
        multiIndex = None
        for index, calltipInfo in enumerate(filterCalltipArgInfo):
            cArgTotal, cArgType, cArgName, cBoolMulti, boolOptional, cArgInfo = calltipInfo
            if cBoolMulti:
                multiType = cArgType
                multiIndex = index
                postMultiIndex = index
                # TODO: handle multiple multiTypes...
                break
        filterArgInfo = []
        for scriptArgIndex, argInfo in enumerate(filterScriptArgInfo):
            argname, argvalue, argtype = argInfo
            if argname:
                # Check named arguments
                try:
                    calltipIndex = calltipArgNames.index(argname.lower())
                except ValueError:
                    calltipIndex = None
            else:
                calltipIndex = scriptArgIndex + clipOffset
                # Check for multi-arg possibility
                if multiIndex is not None and calltipIndex > multiIndex:
                    if argtype in (multiType, 'var'):
                        calltipIndex = multiIndex
                    else:
                        multiType = None
                        postMultiIndex += 1
                        calltipIndex = postMultiIndex
                if calltipIndex > maxCalltipIndex:
                    calltipIndex = None
                    continue
            if calltipIndex is not None:
                calltipFilterInfo = filterCalltipArgInfo[calltipIndex][0]
            else:
                calltipFilterInfo = ''
            filterArgInfo.append((calltipIndex, calltipFilterInfo, argname, argvalue))
        return filterArgInfo

    def GetFilterScriptArgInfo(self, startwordpos, calltip=None):
        openpos = self.FindText(startwordpos, self.GetTextLength(), '(')
        if openpos == -1:
            self.cursorFilterScriptArgIndex = 0
            return None
        # Grab the text line from the script
        line = self.LineFromPosition(openpos)
        posStart = openpos - self.PositionFromLine(line)
        iArg = 0
        pos1 = openpos
        posEnd = None
        while pos1 < self.GetLength():
            if unichr(self.GetCharAt(pos1)) == '(':
                posEnd = self.BraceMatch(pos1)
                if posEnd == -1:
                    posEnd = self.GetLineEndPosition(line) #self.GetLength()
                pos1 += 1
                break
            pos1 += 1
        if posEnd is None:
            self.cursorFilterScriptArgIndex = 0
            return None
        if pos1 == posEnd:
            self.cursorFilterScriptArgIndex = 0
            return None #[('','','')]
        currentPos = self.GetCurrentPos()
        currentIndex = None
        argsList = []
        counter = 0
        pos2 = self.GetNextValidCommaPos(pos1, allowparentheses=False)
        while pos2 is not None and pos2 <= posEnd:
            txt = self.GetTextRange(pos1,pos2).strip()
            argsList.append(txt)
            if pos2 >= currentPos and currentIndex is None:
                currentIndex = counter
            counter += 1
            pos1 = pos2 + 1
            pos2 = self.GetNextValidCommaPos(pos1, allowparentheses=False)
        if currentIndex is None:
            currentIndex = counter
        txt = self.GetTextRange(pos1,posEnd).strip()
        argsList.append(txt)
        argInfo = []
        for txt in argsList:
            try:
                argname, argvalue = [s.strip() for s in txt.split('=', 1)]
                argname = argname.strip(string.whitespace+'\\')
                argvalue = argvalue.strip(string.whitespace+'\\')
                argtype = 'named'
            except ValueError:
                argname = u''
                argvalue = txt
                argname = argname.strip(string.whitespace+'\\')
                argvalue = argvalue.strip(string.whitespace+'\\')
                argtype = self.GetAviSynthVarType(argvalue)
            #~ argname = argname.strip(string.whitespace+'\\')
            #~ argvalue = argvalue.strip(string.whitespace+'\\')
            argInfo.append((argname, argvalue, argtype))
        self.cursorFilterScriptArgIndex = currentIndex
        return argInfo

    def GetFilterCalltipArgInfo(self, word=None, calltip=None, ignore_opt_args=False):
        if calltip is None:
            # Get the user slider info from the filter's calltip
            try:
                calltip = self.avsfilterdict[word.lower()][0].split('\n\n')[0]
            except KeyError:
                return
        # Delete open and close parentheses
        if calltip.startswith('(') and calltip.endswith(')'):
            calltip = calltip[1:-1]
        elif calltip.startswith('('):
            calltip = calltip[1:]
        elif calltip.endswith(')'):
            calltip = calltip[:-1]
        
        # Delete/mark optional arguments
        new_calltip = []
        for arg in calltip.split(','):
            arg = arg.strip()
            if arg.startswith('[') and arg.endswith(']'):
                if not ignore_opt_args:
                    new_calltip.append(arg[1:-1] + 'OPT')
            else:
                new_calltip.append(arg)
        calltip = ', '.join(new_calltip)
        
        # Get rid of any commas in square brackets
        calltip = re.sub(r'\[.*\]', '[...]', calltip)
        
        # Split the arguments by commas
        argInfo = []
        for item in calltip.split(','):
            item = item.strip()
            if not item.strip():
                continue
            if item.count('[...]') > 0:
                boolMulti = True
                item = item.replace('[...]', '')
            else:
                boolMulti = False
            if item.endswith('OPT'):
                boolOptional = True
                item = item[:-3]
            else:
                boolOptional = False
            try:
                argtype, nameAndInfo = [s.strip() for s in item.split(' ', 1)]
                try:
                    name, info = [s.strip() for s in nameAndInfo.split('=', 1)]
                except ValueError:
                    name = nameAndInfo
                    info = u''
                argInfo.append((item, argtype.lower(), name, boolMulti, boolOptional, info))
            except ValueError:
                if item.lower() in ('clip', 'int', 'float', 'bool', 'string'):
                    argInfo.append((item, item.lower(), u'', boolMulti, boolOptional, u''))
                else:
                    # Assume it's a clip
                    argInfo.append((item, u'clip', item, boolMulti, boolOptional, u''))
        return argInfo

    def CreateDefaultPreset(self, filtername, calltip=None):
        if calltip is None:
            calltip = self.avsfilterdict[filtername.lower()][0].split('\n\n')[0]
        if calltip == '':
            return filtername
        argList = []
        for i, info in enumerate(self.GetFilterCalltipArgInfo(filtername, calltip, ignore_opt_args=True)):
            totalInfo, cArgType, cArgName, boolRepeatArg, boolOptionalArg, cArgInfo = info
            argtype, argname, guitype, defaultValue, other = self.app.ParseCalltipArgInfo(totalInfo)
            namedarg = ''
            if cArgName.startswith('"') and cArgName.endswith('"'):
                namedarg = cArgName.strip('"')+'='
            #~ if defaultValue is not None:
            if defaultValue or defaultValue == 0:
                if guitype == 'color':
                    argList.append('%s$%s' % (namedarg, defaultValue))
                elif argtype in ('float', 'int') and guitype == 'slider' and other is not None:
                    nDecimal = other[2]
                    strTemplate = '%.'+str(nDecimal)+'f'
                    try:
                        argList.append(namedarg+strTemplate % defaultValue)
                    except (TypeError, ValueError):
                        re_clip = re.compile(r'\bclip\b', re.I)
                        defaultValue = re_clip.sub('last', str(defaultValue))
                        argList.append(namedarg+defaultValue)
                else:
                    argList.append(namedarg+str(defaultValue))#.lower())
            elif argtype == 'clip' and i == 0:
                pass   # argList.append('last')
            else:
                argList.append(namedarg+'?')
        return '%s(%s)' % (filtername, ', '.join(argList))

    def GetAviSynthLine(self, pos, preSectionOnly=False, postSectionOnly=False):
        '''Returns the line of text at pos, accommodating for AviSynth line continuations'''
        linenumber = self.LineFromPosition(pos)
        if preSectionOnly:
            lines = [self.GetLine(linenumber)[:pos-self.PositionFromLine(linenumber)]]
        elif postSectionOnly:
            lines = [self.GetLine(linenumber)[pos-self.PositionFromLine(linenumber):]]
        else:
            lines = [self.GetLine(linenumber)]
        if not postSectionOnly:
            iLine = linenumber - 1
            while iLine >= 0:
                linetxt = self.GetLine(iLine)
                if lines[0].strip().startswith('\\') or linetxt.strip().endswith('\\'):
                    lines.insert(0, linetxt)
                else:
                    break
                iLine -= 1
        if not preSectionOnly:
            maxlinenumber = self.GetLineCount() - 1
            iLine = linenumber + 1
            while iLine <= maxlinenumber:
                linetxt = self.GetLine(iLine)
                if lines[-1].strip().endswith('\\') or linetxt.strip().startswith('\\'):
                    lines.append(linetxt)
                else:
                    break
                iLine += 1
        return ' '.join([s.strip().strip('\\') for s in lines])

    def GetAviSynthVarType(self, strVar):
        strVar = strVar.strip()
        if not strVar:
            return 'empty'
        # Check int
        if strVar.isdigit():
            return 'int'
        # Check float
        try:
            float(strVar)
            return 'float'
        except ValueError:
            pass
        # Check hex number
        if strVar.startswith('$'):
            return 'hex'
        # Check boolean
        if strVar.lower() in ('true', 'false'):
            return 'bool'
        # Check string
        if strVar.startswith('"') and strVar.endswith('"'):
            return 'string'
        if strVar.startswith('"'):
            # Incomplete string...
            return 'string'
        # Check if it's a named argument
        if strVar.count('=') > 0:
            return 'named'
        # Check if it's the Avisynth variable last
        if strVar.lower() == 'last':
            return 'clip'
        # Heuristic...
        if strVar.count('.') > 0:
            name = strVar.split('.')[-1].split('(')[0].lower()
            if name in ('width', 'height', 'framecount'):
                return 'int'
            elif name in ('framerate',):
                return 'float'
            elif name.startswith('is'):
                return 'bool'
        # If none of the above, it's a variable name
        if self.AVI is not None:
            vartype = self.AVI.GetVarType(strVar)
            if vartype in ('int', 'float', 'string', 'bool'):
                return vartype
        return 'var'

    def GetNextValidCommaPos(self, pos, checkChar=',', allowparentheses=False):
        #~ txt = self.GetTextRange(pos, self.GetLength())
        #~ newPos = pos
        #~ for c in txt:
            #~ if c == ',':
                #~ if self.GetStyleAt(newPos) not in (self.STC_AVS_STRING, self.STC_AVS_TRIPLE, self.STC_AVS_USERSLIDER):
                    #~ return newPos
            #~ newPos += 1
        nOpen = 0
        while pos <= self.GetLength():
            c = unichr(self.GetCharAt(pos))
            if c == '(' and not allowparentheses:
                pos = self.BraceMatch(pos)
                if pos == wx.NOT_FOUND:
                    return None
                continue
            if c == checkChar:
                if self.GetStyleAt(pos) not in (self.STC_AVS_STRING, self.STC_AVS_TRIPLE, self.STC_AVS_USERSLIDER, self.STC_AVS_COMMENT):
                    return pos
            pos += 1
        return None

    def ShowFilterDocumentation(self, name=None):
        if name is None:
            name = self.calltipFilter
        if not name:
            return
        docsearchpaths = []
        avisynthdir = self.app.ExpandVars(self.app.avisynthdir)
        docsearchpathstring = self.app.ExpandVars(self.app.options['docsearchpaths'])
        for path in docsearchpathstring.split(';'):
            path = path.strip()
            if os.path.isdir(path):
                docsearchpaths.append(path)
        extensions = ['.htm', '.html', '.txt', '.lnk', '']
        
        def get_names(name):
            name = name.lower()
            if name in self.avsfilterdict:
                display_name = self.avsfilterdict[name][2]
                if self.avsfilterdict[name][1] == AvsStyledTextCtrl.STC_AVS_PLUGIN:
                    is_short = self.avsfilterdict[name][3]
                    if is_short:
                        long_name = self.avsfilterdict[is_short][2]
                        short_name = display_name
                    else:
                        long_name = display_name
                        short_name = self.app.GetPluginFunctionShortName(long_name)
                    yield long_name[:-len(short_name) - 1]
                    yield short_name
                    yield long_name
                else:
                    yield display_name
        
        for find_name in get_names(name):
            for dir in docsearchpaths:
                filenames = []
                for filename in os.listdir(dir):
                    base, ext = os.path.splitext(filename)
                    if ext in extensions:
                        if re.findall(r'(\b|[_\W]|readme)%s(\b|[_\W]|readme)' % find_name, base, re.IGNORECASE):
                            filenames.append((extensions.index(ext), filename))
                if filenames:
                    filenames.sort()
                    filename = os.path.join(dir, filenames[0][1])
                    startfile(filename)
                    return True
        url = self.app.options['docsearchurl'].replace('%filtername%', name.replace('_', '+'))
        startfile(url)
        return False

    def GetFilterNameAtCursor(self, pos=None):
        if self.calltipFilter is not None:
            word = self.calltipFilter
        else:
            if pos is None:
                pos = self.GetCurrentPos()
            posA = self.WordStartPosition(pos, 1)
            posB = self.WordEndPosition(pos, 1)
            word = self.GetTextRange(posA, posB)
        return word
    
    def IsString(self, pos):
        if pos == self.GetTextLength():
            return self.IsString(pos - 1)
        return self.GetStyleAt(pos) in (self.STC_AVS_STRING, self.STC_AVS_TRIPLE, self.STC_AVS_STRINGEOL)
    
    def GetStringRange(self, pos):
        if not self.IsString(pos):
            return
        start = end = pos
        last_pos = self.GetTextLength()
        if pos == last_pos:
            start -= 1
        else:
            while end + 1 <= last_pos and self.IsString(end + 1):
                end += 1
        while start - 1 >= 0 and self.IsString(start - 1):
            start -= 1
        if self.GetStyleAt(start) == self.STC_AVS_TRIPLE:
            start += 3
            if self.GetStyleAt(end) != self.STC_AVS_STRINGEOL and end != last_pos:
                end -= 2
        else:
            start += 1
        return start, end
    
    def GenerateHTML(self, title=None, ext_css=None):
        """Return a HTML version of the text in the stc
        
        'ext_css' can be a filename for linking to an external style sheet.  
        In that case a tuple (html, css) is returned
        """
        
        # Override face and size with the monospace font if used
        if self.app.options['usemonospacedfont']:
            monospaced = self.GenerateCSSBlock('monospaced', join=False)
            face = monospaced[self.css_properties['face']]
            size = monospaced[self.css_properties['size']]
            monospaced = face, size
        else:
            monospaced = None
        
        # Generate the body of the html and the style sheet
        # a complete sheet if external, otherwise only the needed styles 
        # without inheritable declarations 
        body = list()
        if not ext_css:
            default_css = self.GenerateCSSBlock('default', join=False, 
                                                monospaced=monospaced)
            css = {'default': self.JoinCSSBlock('default', default_css)}
            default_css = default_css.items()
        last_style = self.GetStyleAt(0)
        style_start = 0
        length = self.GetLength()
        if not length:
            return
        for pos in xrange(0, length + 1):
            if pos != length:
                style = self.GetStyleAt(pos)
                if style == last_style:
                    continue
            style_name = self.styleInfo[last_style][0]
            if not ext_css and style_name not in css:
                css[style_name] = self.GenerateCSSBlock(style_name, default_css, 
                                                        monospaced=monospaced)
            text = cgi.escape(self.GetTextRange(style_start, pos), True)
            if style_name != 'default':
                text = u'<span class="{0}">{1}</span>'.format(style_name, text)
            body.append(text)
            last_style = style
            style_start = pos
        body = u'<body>\n<pre class="default">\n{0}\n</pre>\n</body>'.format(
                                                                  ''.join(body))
        css =  self.GenerateCSS(monospaced=monospaced) if ext_css else \
               '\n'.join(css.values())
        
        # Generate the head, inserting the css if required
        title = cgi.escape(title or _('AviSynth script'), True)
        generator = cgi.escape(u'{0} v{1}'.format(global_vars.name, 
                               global_vars.version), True)
        if ext_css:
            head_css = u'<link rel="stylesheet" type="text/css" '\
                        'href="{0}">'.format(ext_css)
        else:
            head_css = u'<style type="text/css">\n{0}\n</style>'.format(css)
        head = textwrap.dedent(u'''\
            <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
            "http://www.w3.org/TR/html4/strict.dtd">
            <html>
            <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <meta name="generator" content="{0}">
            <title>{1}</title>
            {2}
            </head>''').format(generator, title, head_css)
        
        # Return the html file, and optionally the style sheet
        html = u'{0}\n{1}\n</html>'.format(head, body)
        if ext_css:
            return html, css
        return html
    
    def GenerateCSS(self, monospaced=None):
        """Generate a style sheet from the styled text in the STC
        
        Override face and size with 'monospaced', if given
        """
        css = []
        for style, (key, extra) in self.styleInfo.iteritems():
            css.append(self.GenerateCSSBlock(key, monospaced=monospaced))
        return '\n'.join(css)
    
    def GenerateCSSBlock(self, style_name, default=None, monospaced=None, join=True):
        """Return a CSS block from a STC style
        
        Don't include in the block declarations in 'default', if given
        Override face and size with 'monospaced', if given
        """
        if not style_name in self.app.options['textstyles']:
            return ''
        if style_name == 'default' and default:
            default = None
        declarations = {}
        for attr in self.app.options['textstyles'][style_name].split(','):
            values = None
            splitted_attr = attr.split(':')
            if len(splitted_attr) == 1:
                if attr in self.stc_attr[0]:
                    values = self.css_properties[attr], attr
            elif len(splitted_attr) == 2:
                attr, value = splitted_attr
                if attr in self.stc_attr[1]:
                    if attr == 'face':
                        if monospaced:
                            value = monospaced[0]
                        else: # add fallback
                            if 'monospace' in style_name or 'string' in style_name:
                                fallback = 'monospace'
                            elif 'comment' in style_name:
                                fallback = 'serif'
                            else:
                                fallback = 'sans-serif'
                            value = u'"{0}", {1}'.format(value, fallback)
                    elif attr == 'size':
                        if monospaced:
                            value = monospaced[1]
                        else: # specify unit
                            value += 'pt'
                    values = self.css_properties[attr], value
            if values and (not default or values not in default):
                declarations[values[0]] = values[1]
        if join:
            return self.JoinCSSBlock(style_name, declarations)
        return declarations
    
    @staticmethod
    def JoinCSSBlock(css_class, css):
        """Generate a CSS block from a property: value dict"""
        declarations = []
        for property, value in css.iteritems():
            declarations.append(u"\n\t{0}: {1};".format(property, value))
        return u".{0} {{{1}\n}}".format(css_class, ''.join(declarations))
    
    # Event functions

    def OnUpdateUI(self, event):
        # Get the character before the caret
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
        # Highlight braces
        braceAtCaret = -1
        braceOpposite = -1
        # check before
        if charBefore and unichr(charBefore) in "[]{}()":# and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1
        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            #~ styleAfter = self.GetStyleAt(caretPos)
            if charAfter and unichr(charAfter) in "[]{}()":# and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos
        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)
        #~ if braceAtCaret != -1:
        if braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
        #~ if self.commentStyle in (self.GetStyleAt(braceAtCaret), self.GetStyleAt(braceAtCaret)):
        if self.GetStyleAt(braceAtCaret) in self.nonBraceStyles or self.GetStyleAt(braceOpposite) in self.nonBraceStyles:
            self.BraceHighlight(-1, -1)
        # Display call tips
        self.UpdateCalltip()
        self.flagTextChanged = False
    
    def x_CodeFolding(self):    # update folding level
        lineCount = self.GetLineCount()
        line = 0
        while line < lineCount:
            if self.GetFoldLevel(line) & stc.STC_FOLDLEVELHEADERFLAG:
                hasBrace = False
                hasBlock = False
                for pos in range(self.PositionFromLine(line), self.GetLineEndPosition(line)+1):
                    if unichr(self.GetCharAt(pos)) == '{' and self.GetStyleAt(pos) == self.STC_AVS_OPERATOR:
                        hasBrace = True
                        break
                if not hasBrace:
                    for pos in range(self.GetLineEndPosition(line), self.PositionFromLine(line)-1, -1):
                        if self.GetStyleAt(pos) == self.STC_AVS_BLOCKCOMMENT and self.GetStyleAt(pos-1) != self.STC_AVS_BLOCKCOMMENT:
                            hasBlock = True
                            break
                if hasBrace:
                    posMatch = self.BraceMatch(pos)
                    if posMatch != stc.STC_INVALID_POSITION:
                        lineEnd = self.LineFromPosition(posMatch) + 1
                        lastChild = self.GetLastChild(line, -1) + 1                        
                        if line+1 == lineEnd:
                            if not self.GetFoldExpanded(line):
                                self.SetFoldExpanded(line, True)
                                self.Expand(line, True)
                            self.SetFoldLevel(line, self.GetFoldLevel(line) & stc.STC_FOLDLEVELNUMBERMASK)
                    else:
                        lineEnd = lastChild = lineCount                        
                    level = (self.GetFoldLevel(line) & stc.STC_FOLDLEVELNUMBERMASK) + 1
                    for lineNum in range(line+1, lineEnd):
                        self.SetFoldLevel(lineNum, self.GetFoldLevel(lineNum) & 0xF000 | level)
                    for lineNum in range(lineEnd, lastChild):
                        self.SetFoldLevel(lineNum, self.GetFoldLevel(lineNum)-1)
                elif hasBlock:
                    end = pos
                    while self.GetStyleAt(end+1) == self.STC_AVS_BLOCKCOMMENT:
                        end += 1
                    lineEnd = self.LineFromPosition(end) + 1
                    lastChild = self.GetLastChild(line, -1) + 1 
                    if line+1 == lineEnd:
                        if not self.GetFoldExpanded(line):
                            self.SetFoldExpanded(line, True)
                            self.Expand(line, True)
                        self.SetFoldLevel(line, self.GetFoldLevel(line) & stc.STC_FOLDLEVELNUMBERMASK)
                    else:
                        for lineNum in range(line+1, self.LineFromPosition(end)+1):
                            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG and not self.GetFoldExpanded(lineNum):
                                self.SetFoldExpanded(lineNum, True)
                                self.Expand(lineNum, True)
                        level = (self.GetFoldLevel(line) & stc.STC_FOLDLEVELNUMBERMASK) + 1
                        for lineNum in range(line+1, lineEnd):
                            self.SetFoldLevel(lineNum, self.GetFoldLevel(lineNum) & 0xF000 | level)
                        for lineNum in range(lineEnd, lastChild):
                            self.SetFoldLevel(lineNum, self.GetFoldLevel(lineNum)-1)
                elif self.GetStyleAt(self.PositionFromLine(line)) != self.STC_AVS_ENDCOMMENT and self.GetStyleAt(self.PositionFromLine(line+1)) == self.STC_AVS_ENDCOMMENT:
                    for lineNum in range(line+1, lineCount):
                        if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG and not self.GetFoldExpanded(lineNum):
                            self.SetFoldExpanded(lineNum, True)
                            self.Expand(lineNum, True)                    
                        level = (self.GetFoldLevel(line) & stc.STC_FOLDLEVELNUMBERMASK) + 1
                    for lineNum in range(line+1, lineCount):                        
                        self.SetFoldLevel(lineNum, self.GetFoldLevel(lineNum) & 0xF000 | level)
                else:
                    if not self.GetFoldExpanded(line):
                        self.SetFoldExpanded(line, True)
                        self.Expand(line, True)
                    #~ else:
                        #~ lineNext = line + 1
                    for lineNum in range(line+1, self.GetLastChild(line, -1)+1):
                        self.SetFoldLevel(lineNum, self.GetFoldLevel(lineNum)-1)
                    self.SetFoldLevel(line, self.GetFoldLevel(line)&stc.STC_FOLDLEVELNUMBERMASK)
                    #~ line = lineNext - 1
            line += 1

    def OnTextChange(self, event):
        if self.app.options['numlinechars']:
            self.fitNumberMarginWidth()
        #~ self.UpdateCalltip(force=True)
        self.flagTextChanged = True
    
    def OnTextCharAdded(self, event):
        if unichr(event.GetKey()) == '\n':
            line = self.GetCurrentLine() - 1
            indentText = self.GetTextRange(self.PositionFromLine(line), self.GetLineIndentPosition(line))
            self.AddText(indentText)
            level = self.GetFoldLevel(line)
            if level & stc.STC_FOLDLEVELHEADERFLAG:
                self.SetFoldLevel(line + 1, level & stc.STC_FOLDLEVELNUMBERMASK)

    def OnNeedShown(self, event):
        line = self.LineFromPosition(event.GetPosition())
        lineEnd = self.LineFromPosition(event.GetPosition()+event.GetLength())
        while line < lineEnd:
            level = self.GetFoldLevel(line)
            if level & stc.STC_FOLDLEVELHEADERFLAG and not self.GetFoldExpanded(line):
                self.SetFoldExpanded(line, True)
                self.Expand(line, True)
            line += 1

    def OnKeyUp(self, event):
        pos = self.GetCurrentPos()
        #~ charCurrent = self.GetCharAt(pos-1)
        #~ charBefore = self.GetCharAt(pos-2)
        #~ charAfter= self.GetCharAt(pos)
        #~ isCurrentCap = unichr(charCurrent).isalpha() and unichr(charCurrent).isupper()#unichr(charCurrent).isalpha() and event.ShiftDown() #
        #~ isBeforeBlank = unichr(charBefore).isspace() or unichr(charBefore)=='.' or charBefore==0
        #~ isBeforeBlank = unichr(charBefore).isspace() or unichr(charBefore) in self.app.avsoperators or charBefore==0
        #~ isAfterBlank = unichr(charAfter).isspace() or unichr(charAfter)=='.' or charAfter==0
        #~ validChar = isCurrentCap and isBeforeBlank and isAfterBlank
        #~ isCommentStyle = self.commentStyle == self.GetStyleAt(pos - 1)
        #~ if self.app.options['autocomplete'] and validChar and not(self.AutoCompActive()) and not isCommentStyle:
            #~ keywords = self.app.avsazdict.get(unichr(charCurrent).lower(), [])[:]
            #~ for i in range(len(keywords)-1, -1, -1):
                #~ if keywords[i] in self.app.options['autocompleteexclusions']:
                    #~ del keywords[i]
            #~ if keywords:
                #~ self.AutoCompShow(1, '\n'.join(keywords))
        keys = (wx.WXK_ESCAPE, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, wx.WXK_TAB)
        if event.GetKeyCode() not in keys\
        and not self.AutoCompActive()\
        and not (self.CallTipActive() and self.app.options['calltipsoverautocomplete'])\
        and self.GetStyleAt(pos-1) not in self.nonBraceStyles:
            start = self.WordStartPosition(pos,1)
            end = self.WordEndPosition(pos,1)
            char = unichr(self.GetCharAt(start))
            if pos == end:
                if self.app.options['autocomplete']\
                and (char.isalpha() and char.isupper() or char == '_')\
                and pos - start == self.app.options['autocompletelength']:
                    wx.CallAfter(self.ShowAutocomplete, auto=1)
                elif self.app.options['autocompletesingle'] and char.isalpha():
                    wx.CallAfter(self.ShowAutocomplete, auto=2)
        event.Skip()

    def OnKeyDown(self,event):
        key = event.GetKeyCode()
        #~ flags = event.GetModifiers()
        if (self.AutoCompActive() and self.autocomplete_case == 'function' and 
            key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, wx.WXK_TAB) and 
            not (event.ControlDown() or event.AltDown() or event.ShiftDown())):
                self.FinishAutocomplete(key=key)
                #~ if key == wx.WXK_TAB:
                    #~ self.app.tab_processed = True
            #~ elif key == wx.WXK_TAB and mod == wx.MOD_NONE:
                #~ self.app.OnMenuEditIndentSelection()
            #~ elif key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) and not event.ControlDown():
                #~ pos = self.GetCurrentPos()
                #~ line = self.LineFromPosition(pos)
                #~ indentText = self.GetTextRange(self.PositionFromLine(line), self.GetLineIndentPosition(line))
                #~ self.ReplaceSelection('\n'+indentText)
                #~ level = self.GetFoldLevel(line)
                #~ if level & stc.STC_FOLDLEVELHEADERFLAG:
                    #~ self.SetFoldLevel(line+1, level & stc.STC_FOLDLEVELNUMBERMASK)
        else:
            event.Skip()
        
    def OnMiddleDown(self,event):
        xypos = event.GetPosition()
        self.GotoPos(self.PositionFromPoint(xypos))

    def OnMouseMotion(self,event):
        if event.MiddleIsDown():
            self.OnMiddleDown(event)
        elif event.LeftIsDown():
            xypos = event.GetPosition()
            self.SetCurrentPos(self.PositionFromPoint(xypos))
        #~ else:
            #~ pass

    def OnLeftMouseDown(self, event):
        #~ self.CallTipCancelCustom()
        event.Skip()
    
    def OnAutocompleteSelection(self, event):
        if self.autocomplete_case == 'function':
            event.Skip() # processing on EVT_KEY_DOWN, because we need event.GetKeyCode()
        elif self.autocomplete_case == 'parameter name':
            self.BeginUndoAction()
            event.Skip()
            def post_autocomplete(arg_name):
                # add an equals sign
                pos = self.GetCurrentPos()
                if unichr(self.GetCharAt(pos)) == '=':
                    self.GotoPos(pos + 1)
                else:
                    self.AddText('=')
                self.EndUndoAction()
                # autocomplete parameter value
                matched_args = self.autocomplete_params
                self.AutocompleteParameterValue(*matched_args[arg_name])
            wx.CallAfter(post_autocomplete, event.GetText())
        elif self.autocomplete_case == 'parameter value':
            # AutoCompSetDropRestOfWord doesn't include quotes
            pos = self.GetCurrentPos()
            self.SetTargetStart(pos)
            while unichr(self.GetCharAt(pos)) in (' ', '?') or self.IsString(pos):
                pos += 1
            self.SetTargetEnd(pos)
            self.BeginUndoAction()
            self.ReplaceTarget('')
            event.Skip()
            wx.CallAfter(self.EndUndoAction)
        elif self.autocomplete_case == 'filename':
            self.AutoCompCancel()
            pos0, start, end0, prefix, dir = self.autocomplete_params
            self.AutocompleteReplaceText(start, end0 + self.GetCurrentPos() - pos0, 
                                         prefix, os.path.join(dir, event.GetText()))
    
    def OnUserListSelection(self, event):
        if self.autocomplete_case == 'snippet':
            start, end = self.autocomplete_params, self.GetCurrentPos()
            self.SetTargetStart(start)
            self.SetTargetEnd(end)
            self.GotoPos(start + self.ReplaceTarget(self.app.options['snippets'][event.GetText()]))
    
    def OnCalltipClick(self, event):
        if wx.GetKeyState(wx.WXK_ALT) or wx.GetKeyState(wx.WXK_CONTROL) or wx.GetKeyState(wx.WXK_SHIFT):
            self.ShowFilterDocumentation()
        else:
            self.CallTipCancelCustom()

    def OnKillFocus(self, event):
        self.CallTipCancelCustom()
        self.AutoCompCancel()
        event.Skip()

    def OnSetFocus(self, event):
        self.UpdateCalltip()
        event.Skip()

    def OnStyleNeeded(self, event, forceAll=False):
        if forceAll:
            start = -1
            line = 0
            isCommentNest = 0
            end = self.GetLength()
        else:
            pos = self.GetEndStyled()
            line = self.LineFromPosition(pos)
            start = self.PositionFromLine(line) - 1
            if self.GetStyleAt(start) == self.STC_AVS_BLOCKCOMMENT:
                isCommentNest = self.GetLineState(line - 1) 
            else:
                isCommentNest = 0
            if self.app.options['wrap']: # workaround
                end = self.GetLineEndPosition(line + self.LinesOnScreen()) + 1
            else:
                end = event.GetPosition()
        if start < 1:
            start = 0
            state = self.STC_AVS_DEFAULT
        else:
            state = self.GetStyleAt(start)
            if state == self.STC_AVS_STRINGEOL:
                start += 1
                state = self.STC_AVS_DEFAULT
        isLoadPlugin = False
        flag = None # True -> start, False -> end
        if line and self.GetFoldLevel(line - 1) & stc.STC_FOLDLEVELHEADERFLAG:
            prev_flag = True
        else:
            prev_flag = None
        self.endstyled = pos = start
        fragment = []
        hexfragment = []
        triple_start = None
        # vpy hack, remove when VapourSynth is supported (with a custom Python lexer)
        string_delimiters = ['"', "'"] if self.filename.endswith('.vpy') else '"'
        self.StartStyling(pos, 31)
        while pos <= end:
            ch = unichr(self.GetCharAt(pos))
            isEOD = (ch == unichr(0))
            isEOL = (ch == '\n' or ch == '\r' or isEOD)
            if state == self.STC_AVS_DEFAULT:
                if ch == '#':
                    state = self.STC_AVS_COMMENT
                elif ch == '/' and unichr(self.GetCharAt(pos+1)) == '*':
                    pos += 1
                    flag = True
                    state = self.STC_AVS_BLOCKCOMMENT
                elif ch in string_delimiters:
                    self.ColourTo(pos-1, state)
                    if unichr(self.GetCharAt(pos+1)) in string_delimiters and unichr(self.GetCharAt(pos+2)) in string_delimiters:
                        pos += 2
                        if self.app.options['syntaxhighlight_styleinsidetriplequotes']:
                            self.ColourTo(pos, self.STC_AVS_TRIPLE)
                        else:
                            triple_start = pos
                            state = self.STC_AVS_TRIPLE                        
                    else:
                        state = self.STC_AVS_STRING
                    if isLoadPlugin:
                        isLoadPlugin = pos
                elif ch == '$':
                    hexfragment = []
                    state = self.STC_AVS_NUMBERBAD
                elif ch == '[' and unichr(self.GetCharAt(pos+1)) == '*':
                    pos += 1
                    isCommentNest += 1
                    self.SetLineState(self.LineFromPosition(pos), isCommentNest)
                    flag = True
                    state = self.STC_AVS_BLOCKCOMMENT
                elif ch == '[' and unichr(self.GetCharAt(pos+1)) == '<':
                    pos += 1
                    state = self.STC_AVS_USERSLIDER
                elif ch.isalpha() or ch == '_' or ch in self.app.avssingleletters:
                    fragment = [ch]
                    state = self.STC_AVS_IDENTIFIER
                elif ch.isdigit():
                    state = self.STC_AVS_NUMBER
                elif ch in self.app.avsoperators:
                    self.ColourTo(pos - 1, state)
                    self.ColourTo(pos, self.STC_AVS_OPERATOR)
                    if ch == '{':
                        flag = True
                    elif ch == '}':
                        flag = None if flag else False
                else:
                    if isEOD:
                        self.ColourTo(pos - 1, self.STC_AVS_DEFAULT)
                    else:
                        self.ColourTo(pos, self.STC_AVS_DEFAULT)
            elif state == self.STC_AVS_COMMENT:
                if isEOL:
                    if isEOD:
                        self.ColourTo(pos - 1, self.STC_AVS_COMMENT)
                    else:
                        self.ColourTo(pos, self.STC_AVS_COMMENT)
                    state = self.STC_AVS_DEFAULT
            elif state == self.STC_AVS_BLOCKCOMMENT:
                if isEOD or pos == end:
                    self.ColourTo(pos - 1, self.STC_AVS_BLOCKCOMMENT)
                elif isEOL:
                    self.SetLineState(self.LineFromPosition(pos), isCommentNest)
                elif isCommentNest:
                    if ch == '*' and unichr(self.GetCharAt(pos+1)) == ']':
                        pos += 1
                        isCommentNest -= 1
                        self.SetLineState(self.LineFromPosition(pos), isCommentNest)
                        flag = None if flag else False
                        if not isCommentNest:
                            self.ColourTo(pos, self.STC_AVS_BLOCKCOMMENT)
                            state = self.STC_AVS_DEFAULT
                    elif ch == '[' and unichr(self.GetCharAt(pos+1)) == '*':
                        pos += 1
                        isCommentNest += 1
                        self.SetLineState(self.LineFromPosition(pos), isCommentNest)
                        flag = True
                elif ch == '*' and unichr(self.GetCharAt(pos+1)) == '/':
                    pos += 1
                    self.ColourTo(pos, self.STC_AVS_BLOCKCOMMENT)
                    flag = None if flag else False
                    state = self.STC_AVS_DEFAULT
            elif state == self.STC_AVS_IDENTIFIER:
                if fragment[0] not in self.app.avssingleletters and (ch.isalnum() or ch == '_'):
                    fragment.append(ch)
                else:
                    pos2 = pos
                    pos -= 1
                    word =''.join(fragment).lower()
                    while unichr(self.GetCharAt(pos2)) in (u' ', u'\t'):
                        pos2 += 1
                    ch2 = unichr(self.GetCharAt(pos2))
                    if word in self.app.avsdatatypes and unichr(self.GetCharAt(pos+1)).isspace():
                        self.ColourTo(pos, self.STC_AVS_DATATYPE)
                    elif word in self.app.avskeywords:
                        self.ColourTo(pos, self.STC_AVS_KEYWORD)
                    elif word in self.app.avsmiscwords:
                        self.ColourTo(pos, self.STC_AVS_MISCWORD)
                        if word == '__end__':
                            line = self.LineFromPosition(pos)
                            self.UpdateFolding(line, True, prev_flag)
                            level = (self.GetFoldLevel(line) & stc.STC_FOLDLEVELNUMBERMASK) + 1
                            for line in range(line + 1, self.LineFromPosition(end) + 1):
                                self.SetFoldLevel(line, level)
                            self.ColourTo(end, self.STC_AVS_ENDCOMMENT)
                            break
                    elif ch2 == u'(':
                        if word in self.avsfilterdict:
                            #~ self.ColourTo(pos, self.keywordstyles[word])
                            self.ColourTo(pos, self.avsfilterdict[word][1])
                            if word == 'loadplugin':
                                isLoadPlugin = True
                        else:
                            self.ColourTo(pos, self.STC_AVS_UNKNOWNFUNCTION)
                    elif ch2 == u'=' and unichr(self.GetCharAt(pos2 + 1)) != '=':
                        if self.GetOpenParenthesesPos(pos - len(word)):
                            self.ColourTo(pos, self.STC_AVS_PARAMETER)
                        else:
                            self.ColourTo(pos, self.STC_AVS_ASSIGN)
                    else:
                        if self.app.options['syntaxhighlight_preferfunctions'] and \
                                word in self.avsfilterdict:
                            #~ self.ColourTo(pos, self.keywordstyles[word])
                            self.ColourTo(pos, self.avsfilterdict[word][1])
                        else:
                            self.ColourTo(pos, self.STC_AVS_DEFAULT)
                    fragment = []
                    state = self.STC_AVS_DEFAULT
            elif state == self.STC_AVS_STRING:
                if self.app.options['usestringeol']:
                    if unichr(self.GetCharAt(pos-1)) in string_delimiters and unichr(self.GetCharAt(pos)) in string_delimiters and unichr(self.GetCharAt(pos+1)) in string_delimiters:
                        state = self.STC_AVS_TRIPLE
                        pos += 1
                    elif ch in string_delimiters or isEOL:
                        if isEOL:
                            if isEOD:
                                self.ColourTo(pos - 1, self.STC_AVS_STRINGEOL)                                
                            else:
                                self.ColourTo(pos, self.STC_AVS_STRINGEOL)
                            isLoadPlugin = False
                        else:
                            self.ColourTo(pos, self.STC_AVS_STRING)
                            if isLoadPlugin:
                                self.parseDllname(isLoadPlugin, pos)
                                isLoadPlugin = False
                        state = self.STC_AVS_DEFAULT
                else:
                    if unichr(self.GetCharAt(pos-1)) in string_delimiters and unichr(self.GetCharAt(pos)) in string_delimiters and unichr(self.GetCharAt(pos+1)) in string_delimiters:
                        state = self.STC_AVS_TRIPLE
                        pos += 1
                    elif ch in string_delimiters:
                        self.ColourTo(pos, self.STC_AVS_STRING)                        
                        state = self.STC_AVS_DEFAULT
                        if isLoadPlugin:
                            self.parseDllname(isLoadPlugin, pos)
                            isLoadPlugin = False
                    elif isEOD:
                        self.ColourTo(pos - 1, self.STC_AVS_STRING)
                        state = self.STC_AVS_DEFAULT
                        isLoadPlugin = False
            elif state == self.STC_AVS_TRIPLE:
                if triple_start is None:
                    triple_start = self.GetStringRange(pos)[0]
                # AviSynth interprets """"""" as '"' etc.
                triple_quote_quirk = False
                if ch == '"' and pos - triple_start == 1:
                    last_quote_pos = pos
                    while unichr(self.GetCharAt(last_quote_pos)) == '"':
                        last_quote_pos += 1
                    quote_number = last_quote_pos - pos
                    if quote_number > 3:
                        pos += quote_number - 1 - 1
                        triple_quote_quirk = True
                if not triple_quote_quirk:
                    if isEOD or ((pos - triple_start > 2) and ch in string_delimiters and unichr(self.GetCharAt(pos-1)) in string_delimiters and unichr(self.GetCharAt(pos-2)) in string_delimiters):
                        self.ColourTo(pos, self.STC_AVS_TRIPLE)
                        state = self.STC_AVS_DEFAULT
                        triple_start = None
                        if isLoadPlugin:
                            if not isEOD:
                                self.parseDllname(isLoadPlugin, pos)
                            isLoadPlugin = False
                    elif isEOL:
                        self.ColourTo(pos, self.STC_AVS_TRIPLE)
            elif state == self.STC_AVS_NUMBER:
                if not ch.isdigit():
                    pos -= 1
                    self.ColourTo(pos, self.STC_AVS_NUMBER)
                    state = self.STC_AVS_DEFAULT
            elif state == self.STC_AVS_NUMBERBAD:
                if ch.isalnum() or ch == '_':
                    hexfragment.append(ch)
                else:
                    pos -= 1
                    #~ if len(hexfragment) == 6 and sum([c.isdigit() or c.lower() in ('a', 'b', 'c', 'd', 'e', 'f') for c in hexfragment]) == 6:
                        #~ self.ColourTo(pos, self.STC_AVS_NUMBER)
                    #~ else:
                        #~ self.ColourTo(pos, self.STC_AVS_NUMBERBAD)
                    try:
                        int(''.join(hexfragment), 16)
                        self.ColourTo(pos, self.STC_AVS_NUMBER)
                    except:
                        self.ColourTo(pos, self.STC_AVS_NUMBERBAD)
                    hexfragment = []
                    state = self.STC_AVS_DEFAULT
            elif state == self.STC_AVS_USERSLIDER:
                if isEOL or (ch == ']' and unichr(self.GetCharAt(pos-1)) == '>'):
                    if isEOL:
                        self.ColourTo(pos, self.STC_AVS_NUMBERBAD)
                    else:
                        self.ColourTo(pos, self.STC_AVS_USERSLIDER)
                    state = self.STC_AVS_DEFAULT
            elif state == self.STC_AVS_ENDCOMMENT:
                line = self.LineFromPosition(pos)
                if self.GetStyleAt(self.PositionFromLine(line)) != self.STC_AVS_ENDCOMMENT:
                    line += 1
                level = (self.GetFoldLevel(line) & stc.STC_FOLDLEVELNUMBERMASK)
                for line in range(line, self.LineFromPosition(end) + 1):
                    self.SetFoldLevel(line, level)
                self.ColourTo(end, self.STC_AVS_ENDCOMMENT)
                break
            ch = unichr(self.GetCharAt(pos))
            if pos != start and (ch == unichr(0) or ch == '\n' or ch == '\r'):
                self.UpdateFolding(self.LineFromPosition(pos), flag, prev_flag)
                prev_flag = flag
                flag = None
            pos += 1
        if wx.VERSION > (2, 9):
            self.app.IdleCall.append((self.Refresh, tuple(), dict()))
                    
    def ColourTo(self, pos, style):
        self.SetStyling(pos +1 - self.endstyled, style)
        self.endstyled = pos+1
        
    def parseDllname(self, start, end):
        path = self.GetTextRange(start, end).lower().strip('"')
        #~ print path
        ext = os.path.splitext(path)[1]
        if ext in ('.dll', '.so'):
            dllname = os.path.basename(path[:-len(ext)])
            if dllname.count('_') and dllname not in self.app.dllnameunderscored:
                self.app.dllnameunderscored.add(dllname)
                self.app.defineScriptFilterInfo()
    
    def UpdateFolding(self, line, flag, prev_flag):
        if line == 0:
            level = stc.STC_FOLDLEVELBASE
        else:
            level = self.GetFoldLevel(line - 1) & stc.STC_FOLDLEVELNUMBERMASK
            if prev_flag:
                level += 1
        if flag == True:
            level |= stc.STC_FOLDLEVELHEADERFLAG
        elif flag == False:
            level = max(stc.STC_FOLDLEVELBASE, level - 1)
        elif not self.GetLine(line).strip():
            level |=  stc.STC_FOLDLEVELWHITEFLAG 
        self.SetFoldLevel(line, level)
    
    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def FoldAll(self):
        if self.GetEndStyled() != self.GetLength():
            self.OnStyleNeeded(None, forceAll=True)
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1

        return line

# Dialog for choosing AviSynth specific fonts and colors
class AvsStyleDialog(wx.Dialog):
    # TODO: add export and import styles, macros to import...
    def __init__(self, parent, dlgInfo, options, defaults, colour_data=None, extra=None, title=_('AviSynth fonts and colors')):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title)
        self.dlgInfo = dlgInfo
        self.options = options.copy()
        self.defaults = defaults
        self.colour_data = colour_data
        # Create the font buttons
        self.controls = {}
        self.controls2 = {}
        self.notebook = wxp.Notebook(self, wx.ID_ANY, style=wx.NO_BORDER, 
                                     invert_scroll=self.GetParent().options['invertscrolling'])
        def OnNotebookPageChanged(event):
            event.GetEventObject().GetCurrentPage().SetFocus()
            event.Skip()
        for tabLabel, tabInfo in dlgInfo:
            tabPanel = wx.Panel(self.notebook, wx.ID_ANY)
            self.notebook.AddPage(tabPanel, tabLabel)
            sizer = wx.FlexGridSizer(cols=4, hgap=20, vgap=5)
            sizer.Add((0,0), 0)
            for label in ( _('Font'), _('Text color'), _('Background')):
                staticText = wx.StaticText(tabPanel, wx.ID_ANY, label)
                font = staticText.GetFont()
                font.SetUnderlined(True)
                font.SetWeight(wx.FONTWEIGHT_BOLD)
                staticText.SetFont(font)
                sizer.Add(staticText, flag=wx.ALIGN_CENTER)
            for label, key in tabInfo:
                (fontSize, fontStyle, fontWeight, fontUnderline,
                fontFace, fontFore, fontBack) = self.ParseStyleInfo(options[key].split(','))                
                if fontFace is not None:
                    font = wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, fontStyle, fontWeight, fontUnderline, faceName=fontFace)
                else:
                    font = None
                # Create the controls
                if type(label) is tuple:
                    label, optKey, tip = label
                    staticText = checkbox = wx.CheckBox(tabPanel, wx.ID_ANY, label)
                    checkbox.SetValue(parent.options[optKey])
                    checkbox.SetToolTipString(tip)
                    self.controls2[optKey] = checkbox
                else:
                    staticText = wx.StaticText(tabPanel, wx.ID_ANY, label)
                if font is not None:
                    fontLabel = '%s, %d' % (fontFace, fontSize)
                    fontButton = wxButtons.GenButton(tabPanel, wx.ID_ANY, label=fontLabel)
                    fontButton.SetUseFocusIndicator(False)
                    fontButton.SetFont(font)
                    self.Bind(wx.EVT_BUTTON, self.OnButtonFont, fontButton)
                else:
                    fontButton = None
                if fontFore is not None:
                    #~ foreButton = wx.StaticText(tabPanel, wx.ID_ANY, size=(50, 20))
                    #~ foreButton.SetBackgroundColour(wx.Colour(*fontFore))
                    #~ foreButton.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
                    #~ foreButton.Bind(wx.EVT_LEFT_UP, self.OnButtonColor)
                    foreButton = wxp.ColourSelect(tabPanel, wx.ID_ANY, colour=wx.Colour(*fontFore), size=(50,23), colour_data=self.colour_data)
                else:
                    foreButton = None
                if fontBack is not None:
                    #~ backButton = wx.StaticText(tabPanel, wx.ID_ANY, size=(50, 20))
                    #~ backButton.SetBackgroundColour(wx.Colour(*fontBack))
                    #~ backButton.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
                    #~ backButton.Bind(wx.EVT_LEFT_UP, self.OnButtonColor)
                    backButton = wxp.ColourSelect(tabPanel, wx.ID_ANY, colour=wx.Colour(*fontBack), size=(50,23), colour_data=self.colour_data)
                else:
                    backButton = None
                sizer.Add(staticText, flag=wx.ALIGN_CENTER)
                if fontButton is not None:
                    sizer.Add(fontButton, flag=wx.ALIGN_CENTER)
                else:
                    sizer.Add((0,0), flag=wx.ALIGN_CENTER)
                if foreButton is not None:
                    sizer.Add(foreButton, flag=wx.ALIGN_CENTER)
                else:
                    sizer.Add((0,0), flag=wx.ALIGN_CENTER)
                if backButton is not None:
                    sizer.Add(backButton, flag=wx.ALIGN_CENTER)
                else:
                    sizer.Add((0,0), flag=wx.ALIGN_CENTER)
                self.controls[key] = (fontButton, foreButton, backButton)
            tabSizer = wx.BoxSizer(wx.VERTICAL)
            tabSizer.Add(sizer, 0, wx.ALL, 10)
            tabPanel.SetSizerAndFit(tabSizer)
        self.notebook.SetSelection(0)
        # Standard (and not standard) buttons
        themes = [_('Select a predefined theme')] + parent.defaulttextstylesDict.keys()
        theme_choice = wx.Choice(self, choices=themes)
        theme_choice.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.OnSelectTheme, theme_choice)
        only_colors_checkbox = wx.CheckBox(self, wx.ID_ANY, _('Only change colours'))
        only_colors_checkbox.SetValue(parent.options['theme_set_only_colors'])
        only_colors_checkbox.SetToolTipString(_("When selecting a theme, don't change current fonts"))
        self.controls2['theme_set_only_colors'] = only_colors_checkbox
        okay  = wx.Button(self, wx.ID_OK, _('OK'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, okay)
        cancel = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        if extra: # single CheckBox
            label, optKey, tip = extra
            checkbox = wx.CheckBox(self, wx.ID_ANY, label)
            checkbox.SetValue(parent.options[optKey])
            checkbox.SetToolTipString(tip)
            self.controls2[optKey] = checkbox
            btns.Add(checkbox, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        btns.Add(theme_choice, 0, wx.LEFT | wx.RIGHT, 3)
        btns.Add(only_colors_checkbox, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Size the elements
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        #~ dlgSizer.Add(sizer, 0, wx.EXPAND|wx.ALL, 5)
        dlgSizer.Add(self.notebook, 0, wx.EXPAND|wx.ALL, 5)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(dlgSizer)
        dlgSizer.Fit(self)
        self.sizer = dlgSizer
        # Misc
        okay.SetDefault()
        self.Centre(wx.CENTRE_ON_SCREEN)
        
    @staticmethod
    def ParseStyleInfo(styleInfo):
        # Get the style info (face, size, bold/italic/underline, color, background)
        (fontSize, fontStyle, fontWeight, fontUnderline,
        fontFace, fontFore, fontBack) = (10, wx.FONTSTYLE_NORMAL,
        wx.FONTWEIGHT_NORMAL, False, None, None, None)
        for info in styleInfo:
            infolower = info.lower().strip()
            if infolower.startswith('face:'):
                fontFace = info[5:]
            elif infolower.startswith('size:'):
                fontSize = int(info[5:])
            elif infolower.startswith('fore:'):
                color = info.split(':')[1].strip().lstrip('#')
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4:6], 16)
                fontFore = (r, g, b)
            elif infolower.startswith('back:'):
                color = info.split(':')[1].strip().lstrip('#')
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4:6], 16)
                fontBack = (r, g, b)
            elif infolower =='bold':
                fontWeight = wx.FONTWEIGHT_BOLD
            elif infolower =='italic':
                fontStyle = wx.FONTSTYLE_ITALIC
            elif infolower =='underline':
                fontUnderline = True
        return (fontSize, fontStyle, fontWeight, fontUnderline,
                fontFace, fontFore, fontBack)
    
    def OnSelectTheme(self, event):
        theme = event.GetEventObject().GetStringSelection()
        if theme != _('Select a predefined theme'):
            return self.SetTheme(theme, only_colors=
                            self.controls2['theme_set_only_colors'].GetValue())
    
    def SetTheme(self, theme, only_colors=False):
        for tabLabel, tabInfo in self.dlgInfo:
            for label, key in tabInfo:
                fontButton, foreButton, backButton = self.controls[key]
                (fontSize, fontStyle, fontWeight, fontUnderline,
                fontFace, fontFore, fontBack) = self.ParseStyleInfo(self.defaults[theme][key].split(','))
                if not only_colors and fontButton is not None and fontFace is not None:
                    font = wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, fontStyle, 
                                   fontWeight, fontUnderline, faceName=fontFace)
                    fontButton.SetLabel('%s, %d' % (fontFace, fontSize))
                    fontButton.SetFont(font)
                    fontButton.SetBestSize()
                    fontButton.Refresh()
                if foreButton is not None and fontFore is not None:
                    foreButton.SetColour(wx.Colour(*fontFore))
                if backButton is not None and fontBack is not None:
                    backButton.SetColour(wx.Colour(*fontBack))
            self.sizer.Fit(self)
    
    def OnButtonOK(self, event):
        if self.UpdateDict():
            event.Skip()

    def OnButtonFont(self, event):
        button = event.GetEventObject()
        font = button.GetFont()
        # Show the font dialog
        data = wx.FontData()
        data.EnableEffects(False)
        data.SetInitialFont(font)
        dlg = wx.FontDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            fontFace = font.GetFaceName()
            fontSize = font.GetPointSize()
            fontLabel = '%s, %d' % (fontFace, fontSize)
            button.SetLabel(fontLabel)
        button.SetFont(font)
        button.SetBestSize()
        button.Refresh()
        self.sizer.Fit(self)
        dlg.Destroy()

    def GetDict(self):
        return self.options
        
    def GetDict2(self):
        for key in self.controls2:
            self.controls2[key] = self.controls2[key].GetValue()
        return self.controls2

    def UpdateDict(self):
        for key, value in self.controls.items():
            styleList = []
            fontButton, foreButton, backButton = value
            if fontButton is not None:
                font = fontButton.GetFont()
                styleList.append('face:%s' % font.GetFaceName())
                styleList.append('size:%i' % font.GetPointSize())
            if foreButton is not None:
                #~ styleList.append('fore:#%02x%02x%02x' % foreButton.GetBackgroundColour().Get())
                styleList.append('fore:#%02x%02x%02x' % foreButton.GetColour().Get())
            if backButton is not None:
                #~ styleList.append('back:#%02x%02x%02x' % backButton.GetBackgroundColour().Get())
                styleList.append('back:#%02x%02x%02x' % backButton.GetColour().Get())
            if fontButton is not None:
                if font.GetWeight() == wx.FONTWEIGHT_BOLD:
                    styleList.append('bold')
                if font.GetStyle() == wx.FONTSTYLE_ITALIC:
                    styleList.append('italic')
                if font.GetUnderlined():
                    styleList.append('underlined')
            stylestring = ','.join(styleList)
            self.options[key] = stylestring
        return True

# Printing
class STCPrintout(wx.Printout):
    """Specific printing support of the wx.StyledTextCtrl for the wxPython
    framework
    
    This class can be used for both printing to a printer and for print 
    preview functions.
    
    """
    debuglevel = 0
    
    def __init__(self, stc, page_setup_data, print_mode=None, header=True, 
                 title='', job_title='', border=False, zoom=False, 
                 wrap=None):
        """Constructor.
        
        stc: wx.StyledTextCtrl to print
        
        page_setup_data: wx.PageSetupDialogData instance that
        is used to determine the margins of the page.
        
        print_mode: optional; of the wx.stc.STC_PRINT_* flags indicating 
        how to render color text.  Defaults to 
        wx.stc.STC_PRINT_COLOURONWHITEDEFAULTBG
        
        header: optional flag indicating whether or not to include a header 
        on every page with the title and page number
        
        title: optional text string to use as the title, if header is True
        
        job_title: optional text string used to identify the job in the 
        printing list
        
        border: optional flag indicating whether or not to draw a black
        border around the text on each page
        
        zoom: optional flag indicating whether or not to apply stc's 
        current magnification to the output
        
        wrap: optional flag indicating whether or not to word-wrap long lines 
        
        """
        if not job_title:
            job_title = wx.PrintoutTitleStr
        wx.Printout.__init__(self, job_title)
        self.stc = stc
        self.page_setup_data = page_setup_data
        if print_mode:
            self.print_mode = print_mode
        else:
            self.print_mode = wx.stc.STC_PRINT_COLOURONWHITEDEFAULTBG
        self.header = header
        if self.header:
            self.setHeaderFont()
            self.title = title
        self.stc.SetPrintMagnification(self.stc.GetZoom() if zoom else 0)
        if wrap is not None:
            self.stc.SetPrintWrapMode(wx.stc.STC_WRAP_WORD if wrap else 
                                      wx.stc.STC_WRAP_NONE)
        self.border_around_text = border
    
    def OnPreparePrinting(self):
        """Called once before a print job is started to set up any defaults.
        
        """
        self.MapScreenSizeToPageMargins(self.page_setup_data)
        dc = self.GetDC()
        self._calculatePageStarts(dc)
    
    def _calculatePageStarts(self, dc):
        """Calculates offsets into the STC for each page
        
        This pre-calculates the page offsets for each page to support print
        preview being able to seek backwards and forwards.
        
        """
        if self.header:
            # Set font for title/page number rendering
            dc.SetFont(self.getHeaderFont())
            # Title
            self.header_height = dc.GetTextExtent(self.title)[1]
            # Page Number
            page_lbl = _("Page:")
            self.header_height = 1.5 * max(self.header_height, 
                                           dc.GetTextExtent(page_lbl)[1])
        else:
            self.header_height = 0
        
        self.stc.SetPrintColourMode(self.print_mode)
        edge_mode = self.stc.GetEdgeMode()
        self.stc.SetEdgeMode(wx.stc.STC_EDGE_NONE)
        stc_len = self.stc.GetLength()
        self.start_points = [0]
        rect = self.GetLogicalPageMarginsRect(self.page_setup_data)
        rect[2] -= self.stc.GetMarginWidth(0)
        rect[1] += self.header_height
        rect[3] -= self.header_height
        if self.debuglevel > 0:
            print  "prepare rect: ", rect
        while self.start_points[-1] < stc_len:
            self.start_points.append(self.stc.FormatRange(False, 
                                    self.start_points[-1], stc_len,
                                    dc, dc, rect, rect))
            if self.debuglevel > 0:
                if self.start_points[-1] == stc_len:
                    print "prepare printing - reached end of document: %d" % stc_len
                else:
                    print ("prepare printing - page %d first line: %d" % (
                           len(self.start_points), self.start_points[-1]))
        self.stc.SetEdgeMode(edge_mode)
    
    def GetPageInfo(self):
        """Return the valid page ranges.
        
        Note that pages are numbered starting from one.
        
        """
        return (1, len(self.start_points) - 1, 1, len(self.start_points) - 1)
    
    def HasPage(self, page):
        """Returns True if the specified page is within the page range
        
        """
        return page < len(self.start_points)
    
    def OnPrintPage(self, page):
        """Draws the specified page to the DC

        page: page number to render
        
        """
        self.MapScreenSizeToPageMargins(self.page_setup_data)
        dc = self.GetDC()
        self._drawPageContents(dc, page)
        if self.header:
            self._drawPageHeader(dc, page)
        if self.border_around_text:
            self._drawPageBorder(dc)
        return True
    
    def _drawPageContents(self, dc, page):
        """Render the STC window into a DC for printing.
        
        dc: the device context representing the page
        
        page: page number
        
        """
        self.stc.SetPrintColourMode(self.print_mode)
        edge_mode = self.stc.GetEdgeMode()
        self.stc.SetEdgeMode(wx.stc.STC_EDGE_NONE)
        stc_len = self.stc.GetLength()
        rect = self.GetLogicalPageMarginsRect(self.page_setup_data)
        rect[2] -= self.stc.GetMarginWidth(0)
        rect[1] += self.header_height
        rect[3] -= self.header_height
        next = self.stc.FormatRange(True, self.start_points[page-1], stc_len, 
                                    dc, dc, rect, rect)
        self.stc.SetEdgeMode(edge_mode)
        if self.debuglevel > 0:
            print  "print rect: ", rect
            if next == stc_len:
                print "printing - reached end of document: %d" % stc_len
            else:
                print "printing - page %d first line: %d" % (page + 1, next)
    
    def _drawPageHeader(self, dc, page):
        """Draw the page header into the DC for printing
        
        dc: the device context representing the page
        
        page: page number
        
        """
        rect = self.GetLogicalPageMarginsRect(self.page_setup_data)
        # Set font for title/page number rendering
        dc.SetFont(self.getHeaderFont())
        dc.SetTextForeground ("black")
        # Title
        if self.title:
            dc.DrawText(self.title, rect[0], rect[1])
        # Page Number
        page_lbl = _("Page: %d") % page
        pg_lbl_w, pg_lbl_h = dc.GetTextExtent(page_lbl)
        dc.DrawText(page_lbl, rect[2] - pg_lbl_w, rect[1])
    
    def setHeaderFont(self, point_size=10, family=wx.FONTFAMILY_SWISS,
                      style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL):
        """Set the font to be used as the header font
        
        point_size: point size of the font
        
        family: one of the wx.FONTFAMILY_* values, e.g.
        wx.FONTFAMILY_SWISS, wx.FONTFAMILY_ROMAN, etc.
        
        style: one of the wx.FONTSTYLE_* values, e.g.
        wxFONTSTYLE_NORMAL, wxFONTSTYLE_ITALIC, etc.
        
        weight: one of the wx.FONTWEIGHT_* values, e.g.
        wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_LIGHT, etc.
        
        """
        self.header_font_point_size = point_size
        self.header_font_family = family
        self.header_font_style = style
        self.header_font_weight = weight
    
    def getHeaderFont(self):
        """Returns the font to be used to draw the page header text
        
        returns: wx.Font instance
        
        """
        point_size = self.header_font_point_size
        font = wx.Font(point_size, self.header_font_family,
                       self.header_font_style, self.header_font_weight)
        return font
    
    def _drawPageBorder(self, dc):
        """Draw the page border into the DC for printing
        
        dc: the device context representing the page
        
        """
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangleRect(self.GetLogicalPageMarginsRect(self.page_setup_data))

# Dialog for scrap window
class ScrapWindow(wx.Dialog):
    def __init__(self, parent, title=_('Scrap Window'), pos=wx.DefaultPosition, size=(250,250)):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, pos, size, style=style)
        self.parent = parent
        # Create the stc control
        self.textCtrl = self.createTextCtrl()        
        self.Style()        
        self.textCtrl.nInserted = 0
        # Define keyboard shortcuts
        #~ self.BindShortcuts()
        # Add the text from the previous session
        txt, anchor, pos = self.parent.options['scraptext']
        self.textCtrl.SetText(txt)
        self.textCtrl.SetAnchor(anchor)
        self.textCtrl.SetCurrentPos(pos)
        self.textCtrl.EnsureCaretVisible()
        self.textCtrl.EmptyUndoBuffer()
        # Set the width for the horizontal scrollbar
        maxWidth = 50
        if wx.VERSION > (2, 9):
            self.textCtrl.SetScrollWidth(maxWidth)
            self.textCtrl.SetScrollWidthTracking(True)
        else:
            for line in txt.split('\n'):
                width = self.textCtrl.TextWidth(stc.STC_STYLE_DEFAULT, line)
                if width > maxWidth:
                    maxWidth = width
            self.textCtrl.SetScrollWidth(maxWidth)
        # Event binding
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        # Misc
        sizer = wx.BoxSizer()
        sizer.Add(self.textCtrl, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)
        self.neverShown = True

    def createTextCtrl(self):
        textCtrl = stc.StyledTextCtrl(self, wx.ID_ANY, size=(250,250), style=wx.SIMPLE_BORDER)
        # Define the context menu
        textCtrl.UsePopUp(0)
        self.idInsertFrame = wx.NewId()
        self.idGetStatusText = wx.NewId()
        self.idToggleScrapWindow = wx.NewId()
        menuInfo = (
            (_('Undo')+'\tCtrl+Z', lambda event: textCtrl.Undo(), wx.ID_ANY),
            (_('Redo')+'\tCtrl+Y', lambda event: textCtrl.Redo(), wx.ID_ANY),
            (''),
            (_('Cut')+'\tCtrl+X', lambda event: textCtrl.Cut(), wx.ID_ANY),
            (_('Copy')+'\tCtrl+C', lambda event: textCtrl.Copy(), wx.ID_ANY),
            (_('Paste')+'\tCtrl+V', lambda event: textCtrl.Paste(), wx.ID_ANY),
            (''),
            (_('Select all')+'\tCtrl+A', lambda event: textCtrl.SelectAll(), wx.ID_ANY),
            (''),
            (_('Refresh'), self.OnRefresh, wx.ID_ANY),
            (_('Insert frame #'), self.OnInsertFrameNumber, self.idInsertFrame),
            (_('Save to file...'), self.OnSave, wx.ID_SAVE),
            (_('Clear all'), self.OnClearAll, wx.ID_ANY),
            (_('Toggle scrap window'), self.OnToggleScrapWindow, self.idToggleScrapWindow),
        )
        self.contextMenu = menu = wx.Menu()
        for eachMenuInfo in menuInfo:
            # Define optional arguments
            if not eachMenuInfo:
                menu.AppendSeparator()
            else:
                label = eachMenuInfo[0]
                handler = eachMenuInfo[1]
                status = ''
                id = eachMenuInfo[2]
                menuItem = menu.Append(id, label, status)
                textCtrl.Bind(wx.EVT_MENU, handler, menuItem)
        textCtrl.contextMenu = menu
        textCtrl.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        # Misc properties
        textCtrl.SetMarginWidth(1, 0)
        textCtrl.SetEOLMode(stc.STC_EOL_LF)
        return textCtrl

    def Style(self):
        textstyles = self.parent.options['textstyles']
        # Define the default style
        self.textCtrl.StyleSetSpec(stc.STC_STYLE_DEFAULT, textstyles['scrapwindow'])
        self.textCtrl.StyleClearAll()
        # Set a style to use for text flashing upon insertion
        self.textCtrl.StyleSetSpec(stc.STC_P_WORD, "fore:#FF0000,bold")
        # Set a style for selected text
        self.textCtrl.SetCaretForeground(textstyles['cursor'].split(':')[1])
        for elem in textstyles['highlight'].split(','):
            if elem.startswith('fore:'):
                if self.parent.options['highlight_fore']:
                    self.textCtrl.SetSelForeground(True, elem.split(':')[1].strip())
                else:
                    self.textCtrl.SetSelForeground(False, wx.WHITE)
            elif elem.startswith('back:'):
                self.textCtrl.SetSelBackground(True, elem.split(':')[1].strip())
    
    def BindShortcuts(self):
        menuInfo = (
            (_('Insert frame #'), self.idInsertFrame),
            (_('Save script'), wx.ID_SAVE),
            (_('Toggle scrap window'), self.idToggleScrapWindow),
        )
        menu = self.contextMenu
        counter = 0
        accList = []
        for itemName, shortcut, id in self.parent.options['shortcuts']:
            for label, id in menuInfo:
                if itemName.endswith(label):
                    counter += 1
                    accel = wx.GetAccelFromString('\t'+shortcut)
                    if accel and accel.IsOk():
                        accList.append((accel.GetFlags(), accel.GetKeyCode(), id))
                    menuItem = menu.FindItemById(id)
                    label = '%s\t%s' % (menuItem.GetItemLabelText(), shortcut)
                    menuItem.SetItemLabel(label)
                    break
            if counter == len(menuInfo):
                break
        accTable = wx.AcceleratorTable(accList)
        self.textCtrl.SetAcceleratorTable(accTable)

    def OnClose(self, event):
        self.Hide()

    def OnContextMenu(self, event):
        win = event.GetEventObject()
        pos = win.ScreenToClient(event.GetPosition())
        try:
            win.PopupMenu(win.contextMenu, pos)
        except AttributeError:
            print>>sys.stderr, _('Error: no contextMenu variable defined for window')

    def OnRefresh(self, event):
        scrap = self.textCtrl
        scrap.StartStyling(0, 31)
        scrap.SetStyling(scrap.GetTextLength(), stc.STC_STYLE_DEFAULT)
        self.Refresh()

    def OnInsertFrameNumber(self, event):
        frame = self.parent.GetFrameNumber()
        self.textCtrl.ReplaceSelection(str(frame))

    def OnSave(self, event):
        filefilter = (_('Text document') + ' (*.txt)|*.txt|' + 
                      _('All files') + ' (*.*)|*.*')
        initialdir = self.parent.GetProposedPath(only='dir')
        dlg = wx.FileDialog(self,_('Save scrap text'),
            initialdir, '', filefilter, wx.SAVE | wx.OVERWRITE_PROMPT)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            filename = dlg.GetPath()
            self.textCtrl.SaveFile(filename)
            self.parent.options['recentdir'] = os.path.dirname(filename)
        dlg.Destroy()

    def OnClearAll(self, event):
        self.textCtrl.ClearAll()

    def OnToggleScrapWindow(self, event):
        self.Hide()

    def GetText(self):
        return self.textCtrl.GetText()

    def SetText(self, txt):
        return self.textCtrl.SetText(txt)

    def Show(self):
        if self.neverShown:
            xp, yp = self.parent.GetPositionTuple()
            wp, hp = self.parent.GetSizeTuple()
            wd, hd = wx.ScreenDC().GetSizeTuple()
            ws, hs = self.GetSizeTuple()
            self.SetPosition((min(xp+wp-50, wd-ws),-1))
        super(ScrapWindow, self).Show()
        if self.neverShown:
            self.Refresh()
            self.neverShown = False

    def write(self, msg):
        self.parent.MacroWriteToScrap(msg)

# Make safe calls to the main thread from other threads   
# Adapted from <http://thread.gmane.org/gmane.comp.python.wxpython/54892/focus=55223>
class AsyncCall:
    ''' Queues a func to run in thread of MainLoop.
    Code may wait() on self.complete for self.result to contain
    the result of func(*ar,**kwar).  It is set upon completion.
    Wait() does this.'''
    def __init__(self, func, *ar, **kwar):
        self.result = self.noresult = object()
        self.complete = threading.Event()
        self.func, self.ar, self.kwar = func, ar, kwar
        if threading.current_thread().name == 'MainThread':
            self.TimeToRun()
        else:
            wx.CallAfter(self.TimeToRun)
    def TimeToRun(self):
        try:
            self.result = self.func(*self.ar, **self.kwar)
        except:
            self.exception = sys.exc_info()
        else:
            self.exception = None
        self.complete.set()
    def Wait(self, timeout=None, failval=None):
        self.complete.wait(timeout)
        if self.exception:
            raise self.exception[0], self.exception[1], self.exception[2]
        if self.result is self.noresult:
            return failval
        return self.result

# Decorator for AsyncCall class
def AsyncCallWrapper(wrapped):
    '''Decorator for AsyncCall class'''
    def wrapper(*args, **kwargs):
        return AsyncCall(wrapped, *args, **kwargs).Wait()
    functools.update_wrapper(wrapper, wrapped)
    return wrapper

# Generate macros_readme.txt
def GenerateMacroReadme(file=None):
    ''' Return the macros_readme.txt content as a single string.  Additionally, if 'file' 
    is not None, write the string to 'file' if it's a string, 'macros/macros_readme.txt' 
    otherwise.
    
    '''
    doc = MainFrame.AvsP_functions(MainFrame).__doc__
    if file:
        if not isinstance(file, basestring):
            file = os.path.join('macros', 'macros_readme.txt')
        dir = os.path.dirname(file)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        file = open(file, 'w')
        file.write(doc)
        file.close()
    return doc

# Open a file or directory with its associate program
def startfile(path, prefer_dir=True):
    '''Open a file or directory with its associate program
    
    'prefer_dir': If True, ensure to open a dir and not an executable with 
    the same name on Windows (ignore PATHEXT)
    '''
    if os.name == 'nt':
        if prefer_dir and os.path.isdir(path):  path += os.sep
        os.startfile(path)
    else: 
        os.system('xdg-open "{0}"'.format(path))

# Dialog and validator for defining user slider
class UserSliderValidator(wx.PyValidator):
    def __init__(self, ctrlDict, labels):
        wx.PyValidator.__init__(self)
        self.ctrlDict = ctrlDict
        self.labels = labels

    def Clone(self):
        return UserSliderValidator(self.ctrlDict, self.labels)

    def Validate(self, parent):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
        if len(text) == 0:
            self.ShowWarning(textCtrl, _('This field must contain a value!'))
            return False
        elif textCtrl == self.ctrlDict['label']:
            try:
                temp  = str(text)
            except UnicodeEncodeError:
                temp = text
            if temp in self.labels:
                self.ShowWarning(textCtrl, _('This slider label already exists!'))
                return False
            if self.getModFromLabel(text) == -1:
                self.ShowWarning(textCtrl, _('Invalid slider label modulo syntax!'))
                return False
            return True
        else:
            try:
                float(text)
            except ValueError:
                self.ShowWarning(textCtrl, _('This field must contain a number!'))
                return False
            try:
                minValue = float(self.ctrlDict['min'].GetValue())
                maxValue = float(self.ctrlDict['max'].GetValue())
                value = float(self.ctrlDict['val'].GetValue())
                # Validate ranges
                if minValue >= maxValue and textCtrl == self.ctrlDict['min']:
                    self.ShowWarning(textCtrl, _('The min value must be less than the max!'))
                    return False
                if value < minValue or value > maxValue and textCtrl == self.ctrlDict['val']:
                    self.ShowWarning(textCtrl, _('The initial value must be between the min and the max!'))
                    return False
                # Validate modulo divisibility
                mod = self.getModFromLabel(self.ctrlDict['label'].GetValue())
                if mod == -1:
                    self.ShowWarning(textCtrl, _('Invalid slider label modulo syntax!'))
                    return False
                if mod is not None:
                    if int(minValue) % mod != 0 and textCtrl == self.ctrlDict['min']:
                        self.ShowWarning(textCtrl, _('The min value must be a multiple of %(mod)s!') % locals())
                        return False
                    if int(maxValue) % mod != 0 and textCtrl == self.ctrlDict['max']:
                        self.ShowWarning(textCtrl, _('The max value must be a multiple of %(mod)s!') % locals())
                        return False
                    if int(value) % mod != 0 and textCtrl == self.ctrlDict['val']:
                        self.ShowWarning(textCtrl, _('The initial value must be a multiple of %(mod)s!') % locals())
                        return False
                    if mod > (maxValue - minValue):
                        self.ShowWarning(self.ctrlDict['min'], _('The difference between the min and max must be greater than %(mod)s!') % locals())
                        return False
            except ValueError:
                pass
            return True

    def getModFromLabel(self, label):
        mod = None
        label = self.ctrlDict['label'].GetValue()
        splitlabel = label.split('%', 1)
        if len(splitlabel) == 2:
            try:
                mod = int(splitlabel[1])
                if mod <= 0:
                    mod = -1
            except ValueError:
                mod = -1
        return mod

    def ShowWarning(self, textCtrl, message):
        color = textCtrl.GetBackgroundColour()
        textCtrl.SetBackgroundColour('pink')
        textCtrl.Refresh()
        wx.MessageBox(message, _('Error'), style=wx.OK|wx.ICON_ERROR)
        textCtrl.SetBackgroundColour(color)
        textCtrl.SetSelection(-1,-1)
        textCtrl.SetFocus()
        textCtrl.Refresh()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

class UserSliderDialog(wx.Dialog):
    def __init__(self, parent, labels, initialValueText=''):
        wx.Dialog.__init__(self, None, wx.ID_ANY, _('Define user slider'))
        self.parent = parent
        # Entry fields
        gridSizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=5)
        gridSizer.AddGrowableCol(1)
        self.ctrlDict = {}
        for eachKey, eachLabel in self.fieldInfo():
            textCtrl = wx.TextCtrl(self, validator=UserSliderValidator(self.ctrlDict, labels))
            staticText = wx.StaticText(self, wx.ID_ANY, eachLabel)
            gridSizer.Add(staticText, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            gridSizer.Add(textCtrl, 0, wx.EXPAND)
            self.ctrlDict[eachKey] = textCtrl
        if initialValueText:
            self.ctrlDict['val'].SetValue(initialValueText)
        # Standard buttons
        okay  = wx.Button(self, wx.ID_OK, _('OK'))
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Set the sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(gridSizer, 0, wx.EXPAND|wx.ALL, 20)
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def fieldInfo(self):
        return (
            ('label', _('Slider label:')),
            ('min', _('Min value:')),
            ('max', _('Max value:')),
            ('val', _('Initial value:')),
        )

    def GetSliderText(self):
        textDict = dict([(k, v.GetValue()) for k,v in self.ctrlDict.items()])
        textDict['open'] = self.parent.sliderOpenString
        textDict['close'] = self.parent.sliderCloseString
        return '%(open)s"%(label)s", %(min)s, %(max)s, %(val)s%(close)s' % textDict

# Dialog for AviSynth filter information
class AvsFunctionDialog(wx.Dialog):
    def __init__(self, parent, filterDict, overrideDict, avsfilterdict, 
                       presetDict, removedSet, pluginDict, shortnamesDict, 
                       installed_plugins_filternames, 
                       installed_avsi_filternames, functionName=None, 
                       functionArgs=None, CreateDefaultPreset=None, 
                       ExportFilterData=None, nag=True):
        wx.Dialog.__init__(
            self, parent, wx.ID_ANY,
            _('Add or override AviSynth functions in the database'),
            size=(500, 300), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        )
        self.parent = parent
        self.filterDict = filterDict.copy()
        self.overrideDict = overrideDict.copy()
        self.avsfilterdict = avsfilterdict.copy()
        self.presetDict = presetDict.copy()
        self.removedSet = removedSet.copy()
        self.pluginDict = pluginDict.copy()
        self.shortnamesDict = shortnamesDict.copy()
        self.installed_plugins_filternames = installed_plugins_filternames
        self.installed_avsi_filternames = installed_avsi_filternames
        self.CreateDefaultPreset = CreateDefaultPreset
        self.ExportFilterData = ExportFilterData
        self.nag = nag
        self.CreateWindowElements()
        self.CreateFilterInfoDialog()
        if functionName is not None:
            wx.FutureCall(100, self.HighlightFunction, functionName, functionArgs)

    def HighlightFunction(self, functionName, functionArgs):
        lowername = functionName.lower()
        if lowername in self.avsfilterdict:
            lowername = self.avsfilterdict[lowername][3] or lowername
            for index in xrange(self.notebook.GetPageCount()):
                panel = self.notebook.GetPage(index)
                listbox = panel.listbox
                for i in xrange(listbox.GetCount()):
                    label = listbox.GetString(i)
                    if label.split()[0].lower() == lowername:
                        self.notebook.SetSelection(index)
                        listbox.SetSelection(i)
                        self.EditFunctionInfo(arg=functionArgs, prompt=True)
                        return
        else: # functionName was not found, show dialog to define new function
            self.AddNewFunction(functionName, arg=functionArgs, prompt=True)

    def CreateWindowElements(self):
        self.notebook = wxp.Notebook(self, wx.ID_ANY, style=wx.NO_BORDER, 
                                     invert_scroll=self.GetParent().options['invertscrolling'])
        
        class CheckListBox(wx.CheckListBox):
            def __init__(self, *args, **kwargs):
                wx.CheckListBox.__init__(self, *args, **kwargs)
                self.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckListBox)
                self.removedSet = self.GetTopLevelParent().removedSet
            
            def Check(self, item, check=True):
                wx.CheckListBox.Check(self, item, check)
                self.UpdateRemovedSet(item)
            
            def OnCheckListBox(self, event):
                self.UpdateRemovedSet(event.GetInt())
                event.Skip()
            
            def UpdateRemovedSet(self, item):
                name = self.GetString(item).split()[0].lower()
                if self.IsChecked(item):
                    if name in self.removedSet:
                        self.removedSet.remove(name)
                else:
                    self.removedSet.add(name)
        
        pageInfo = (
            (_('Core filters'), 0),
            (_('Plugins'), 2),
            (_('User functions'), 3),
            (_('Script functions'), 4),
            (_('Clip properties'), 1),
        )
        pageDict = collections.defaultdict(list)
        for key in set(self.filterDict.keys()+self.overrideDict.keys()):
            name, args, ftype = self.overrideDict.get(key, (None, None, None))
            extra = ' '
            if name is None:
                try:
                    name, args, ftype = self.filterDict[key]
                except:
                    continue
            else:
                extra += '*'
            if key in self.presetDict:
                extra += '~'
            pageDict[ftype].append(name + extra)
        for title, index in pageInfo:
            panel = wx.Panel(self.notebook, wx.ID_ANY, size=(700,-1))
            self.notebook.AddPage(panel, title)
            # List box

            #~ choices = [
                #~ self.overrideDict.get(key, value)[0]
                #~ for key, value in self.filterDict.items()
                #~ if value[2] == index
            #~ ]

            #~ d1 = dict([(lowername, name) for lowername, (name,args,ftype) in self.filterDict.items() if ftype==index])
            #~ d2 = dict([(lowername, name+' *') for lowername, (name,args,ftype) in self.overrideDict.items() if ftype==index])
            #~ d1.update(d2)
            #~ choices = [value for key, value in d1.items()]

            choices = pageDict[index]
            listbox = CheckListBox(panel, wx.ID_ANY, choices=choices, size=(-1,300), style=wx.LB_SORT)
            if choices:
                listbox.SetSelection(0)
            listbox.Bind(wx.EVT_LISTBOX_DCLICK, lambda event: self.EditFunctionInfo())
            for i in xrange(listbox.GetCount()):
                name = listbox.GetString(i).split()[0]
                if name.lower() not in self.removedSet:
                    listbox.Check(i)
            title = title.lower()
            # Buttons
            buttonadd = wx.Button(panel, wx.ID_ANY, _('New function'))#, size=(100, -1))
            buttonedit = wx.Button(panel, wx.ID_ANY, _('Edit selected'))
            buttondelete = wx.Button(panel, wx.ID_ANY, _('Delete selected'))
            buttoncheckall = wx.Button(panel, wx.ID_ANY, _('Select all'))
            buttonuncheckall = wx.Button(panel, wx.ID_ANY, _('Clear all'))
            panel.Bind(wx.EVT_BUTTON, lambda event: self.AddNewFunction(ftype=-1), buttonadd)
            panel.Bind(wx.EVT_BUTTON, lambda event: self.EditFunctionInfo(), buttonedit)
            panel.Bind(wx.EVT_BUTTON, lambda event: self.DeleteFunction(), buttondelete)
            panel.Bind(wx.EVT_BUTTON, lambda event: self.CheckAllFunctions(True), buttoncheckall)
            panel.Bind(wx.EVT_BUTTON, lambda event: self.CheckAllFunctions(False), buttonuncheckall)
            buttonSizer = wx.BoxSizer(wx.VERTICAL)
            buttonSizer.Add(buttonadd, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
            buttonSizer.Add(buttonedit, 0, wx.EXPAND|wx.BOTTOM, 5)
            buttonSizer.Add(buttondelete, 0, wx.EXPAND|wx.BOTTOM, 5)
            buttonSizer.Add(wx.StaticLine(panel, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
            buttonSizer.Add(buttonuncheckall, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
            buttonSizer.Add(buttoncheckall, 0, wx.EXPAND|wx.BOTTOM, 5)
            #~ if index == 2:
                #~ self.buttonclearlongnames = wx.Button(panel, wx.ID_ANY, _('Clear long names'))
                #~ panel.Bind(wx.EVT_BUTTON, lambda event: self.ClearLongNames(), self.buttonclearlongnames)
                #~ buttonSizer.Add(self.buttonclearlongnames, 0, wx.EXPAND|wx.BOTTOM, 5)
            if index in (2, 3):
                buttonselectinstalled = wx.Button(panel, wx.ID_ANY, _('Select installed'))
                panel.Bind(wx.EVT_BUTTON, lambda event: self.SelectInstalledFilters(), buttonselectinstalled)
                buttonSizer.Add(buttonselectinstalled, 0, wx.EXPAND|wx.BOTTOM, 5)
            # Size the elements in the panel
            listboxSizer = wx.BoxSizer(wx.HORIZONTAL)
            listboxSizer.Add(listbox, 1, wx.EXPAND|wx.RIGHT, 15)            
            listboxSizer.Add(buttonSizer, 0, wx.EXPAND|wx.RIGHT, 5)            
            panelSizer = wx.BoxSizer(wx.VERTICAL)
            panelSizer.Add(listboxSizer, 1, wx.EXPAND|wx.ALL, 5)            
            panel.SetSizer(panelSizer)
            panelSizer.Layout()
            # Bind items to the panel itself
            panel.listbox = listbox
            panel.functiontype = index
        self.CreatePluginsContextMenu()
        # Buttons
        button0 = wx.Button(self, wx.ID_ANY, _('Import'))
        menu0 = wx.Menu()
        menuItem = menu0.Append(wx.ID_ANY, _('Import from files'))
        self.Bind(wx.EVT_MENU, lambda event: self.ImportFromFiles(), menuItem)
        menuItem = menu0.Append(wx.ID_ANY, _('Import from wiki'))
        self.Bind(wx.EVT_MENU, lambda event: self.ImportFromFiles(wiki=True), menuItem)
        self.Bind(wx.EVT_BUTTON, lambda event: button0.PopupMenu(
                    menu0, (1, button0.GetSizeTuple()[1])), button0)
        button1 = wx.Button(self, wx.ID_ANY, _('Export customizations'))
        self.Bind(wx.EVT_BUTTON, lambda event: self.ExportCustomizations(), button1)
        button2 = wx.Button(self, wx.ID_ANY, _('Clear customizations'))
        self.Bind(wx.EVT_BUTTON, lambda event: self.ClearCustomizations(), button2)
        button3 = wx.Button(self, wx.ID_ANY, _('Clear manual presets'))
        self.Bind(wx.EVT_BUTTON, lambda event: self.ClearPresets(), button3)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(button0, 0, wx.RIGHT, 5)
        buttonSizer.Add(button1, 0, wx.RIGHT, 5)
        buttonSizer.Add(button2, 0, wx.RIGHT, 5)
        buttonSizer.Add(button3, 0, wx.RIGHT, 5)        
        self.checkBox = wx.CheckBox(self, wx.ID_ANY, _("When importing, don't show the choice dialog"))
        # Standard buttons
        okay  = wx.Button(self, wx.ID_OK, _('OK'))
        #~ self.Bind(wx.EVT_BUTTON, self.OnButtonOK, okay)
        cancel = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        sdtbtns = wx.StdDialogButtonSizer()
        sdtbtns.Add(self.checkBox)
        sdtbtns.AddButton(okay)
        sdtbtns.AddButton(cancel)
        sdtbtns.Realize()
        # Size the elements
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 5)
        dlgSizer.Add(buttonSizer, 0, wx.LEFT, 5)
        dlgSizer.Add(wx.StaticLine(self, style=wx.HORIZONTAL), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        dlgSizer.Add(sdtbtns, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(dlgSizer)
        dlgSizer.SetSizeHints(self)
        dlgSizer.Layout()
        # Misc
        def OnPageChanged(event):
            event.GetEventObject().GetCurrentPage().SetFocus()
            event.Skip()
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, OnPageChanged)
        self.notebook.GetCurrentPage().listbox.SetFocus()
        okay.SetDefault()

    def CreateFilterInfoDialog(self, resetargsbutton=True):
        dlg = wx.Dialog(self, wx.ID_ANY, _('Edit function information'))
        staticText0 = wx.StaticText(dlg, wx.ID_ANY, _('Name:'))
        textCtrl0 = wx.TextCtrl(dlg, wx.ID_ANY, size=(200,-1))
        staticText1 = wx.StaticText(dlg, wx.ID_ANY, _('Type:'))
        choices = [_('core filter'), _('clip property'), _('plugin'), _('user function'), _('script function')]
        choiceBox1 = wx.Choice(dlg, wx.ID_ANY, choices=choices)
        staticText2 = wx.StaticText(dlg, wx.ID_ANY, _('Arguments:'))
        staticText2_4 = wx.StaticText(dlg, wx.ID_ANY, _('define sliders'))
        staticText2_5 = wx.StaticText(dlg, wx.ID_ANY, _('reset to default'))
        for eachCtrl in (staticText2_4, staticText2_5):
            font = eachCtrl.GetFont()
            font.SetUnderlined(True)
            eachCtrl.SetFont(font)
            eachCtrl.SetForegroundColour(wx.Colour(0,0,255))
            eachCtrl.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        def OnArgsEditSliders(event):
            name = textCtrl0.GetValue()
            dlg2 = AvsFilterAutoSliderInfo(dlg, self.GetParent(), name, textCtrl2.GetValue(), title=_('Slider information'))
            ID = dlg2.ShowModal()
            if ID == wx.ID_OK:
                textCtrl2.SetValue(dlg2.GetNewFilterInfo())
            dlg2.Destroy()
        staticText2_4.Bind(wx.EVT_LEFT_DOWN, OnArgsEditSliders)
        def OnClickSetToDefault(event):
            textCtrl0.SetValue(dlg.defaultName)
            textCtrl2.SetValue(dlg.defaultArgs)
        staticText2_5.Bind(wx.EVT_LEFT_DOWN, OnClickSetToDefault)
        textCtrl2 = wxp.TextCtrl(dlg, wx.ID_ANY, size=(200,200), style=wx.TE_MULTILINE|wx.HSCROLL)
        def OnArgsChange(event):
            if checkBox3.IsChecked():
                name = textCtrl0.GetValue() #dlg.defaultName
                args= textCtrl2.GetValue()
                textCtrl3.SetValue(self.CreateDefaultPreset(name, args))
        textCtrl0.Bind(wx.EVT_TEXT, OnArgsChange)
        textCtrl2.Bind(wx.EVT_TEXT, OnArgsChange)
        #~ textCtrl2.Bind(wx.EVT_LEFT_DCLICK, OnArgsEditSliders)
        staticText3 = wx.StaticText(dlg, wx.ID_ANY, _('Preset:'))
        checkBox3 = wx.CheckBox(dlg, wx.ID_ANY, _('Auto-generate'))
        def OnCheck(event):
            if checkBox3.IsChecked():
                textCtrl3.SetEditable(False)
                colour = self.GetBackgroundColour()
                textCtrl3.SetBackgroundColour(colour)
                OnArgsChange(None)
            else:
                textCtrl3.SetEditable(True)
                textCtrl3.SetBackgroundColour(wx.WHITE)
        checkBox3.Bind(wx.EVT_CHECKBOX, OnCheck)
        textCtrl3 = wxp.TextCtrl(dlg, wx.ID_ANY, size=(-1,50), style=wx.TE_MULTILINE|wx.HSCROLL)
        # Standard buttons
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        def OnFilterInfoDialogButtonOK(event):
            newName = textCtrl0.GetValue()
            enteredName = dlg.enteredName
            if enteredName is None:
                lowername = newName.lower()
                if lowername in self.overrideDict or lowername in self.filterDict:
                    wx.MessageBox(_('Filter name already exists!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
                    textCtrl0.SetFocus()
                    return
                if not newName or newName[0].isdigit() or re.findall('\W', newName):
                    wx.MessageBox(_('Invalid filter name!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
                    textCtrl0.SetFocus()
                    return
            elif newName.lower() != enteredName.lower():
                wx.MessageBox(_('Renaming not allowed!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
                textCtrl0.SetFocus()
                return
            if dlg.typeBox.GetCurrentSelection() == 2 and newName.count('_') == 0:
                wx.MessageBox(_('You must use dllname_function naming format for plugins!'), 
                              _('Error'), style=wx.OK|wx.ICON_ERROR)
                textCtrl0.SetFocus()
                return
            event.Skip()
        dlg.Bind(wx.EVT_BUTTON, OnFilterInfoDialogButtonOK, okay)
        cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Size the elements
        sizer01 = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)
        sizer01.Add(staticText0, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer01.Add(textCtrl0, 0, wx.EXPAND|wx.RIGHT, 10)
        sizer01.Add(staticText1, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer01.Add(choiceBox1, 0, wx.EXPAND)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(staticText2, 0, wx.ALL, 0)
        sizer2.Add((-1,-1), 1, wx.EXPAND|wx.ALL, 0)
        sizer2.Add(staticText2_5, 0, wx.RIGHT, 10)
        sizer2.Add(staticText2_4, 0, wx.LEFT|wx.RIGHT, 10)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(staticText3, 0, wx.ALL, 0)
        sizer3.Add((-1,-1), 1, wx.EXPAND|wx.ALL, 0)
        sizer3.Add(checkBox3, 0, wx.RIGHT, 10)
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add((-1,5), 0, wx.EXPAND|wx.ALL, 0)
        dlgSizer.Add(sizer01, 0, wx.EXPAND|wx.ALL, 5)
        dlgSizer.Add(wx.StaticLine(dlg, style=wx.HORIZONTAL), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        #~ dlgSizer.Add(staticText2, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)
        dlgSizer.Add(sizer2, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)
        dlgSizer.Add(textCtrl2, 1, wx.EXPAND|wx.ALL, 5)
        #~ dlgSizer.Add(staticText3, 0, wx.TOP|wx.LEFT, 5)
        dlgSizer.Add(sizer3, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)
        dlgSizer.Add(textCtrl3, 0, wx.EXPAND|wx.ALL, 5)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        dlg.SetSizer(dlgSizer)
        if not resetargsbutton:
            staticText2_5.Hide()
        def SetAutopreset(on=True):
            if on:
                checkBox3.SetValue(True)
                textCtrl3.SetEditable(False)
                colour = self.GetBackgroundColour()
                textCtrl3.SetBackgroundColour(colour)
            else:
                checkBox3.SetValue(False)
                textCtrl3.SetEditable(True)
                textCtrl3.SetBackgroundColour(wx.WHITE)
        dlg.SetAutopreset = SetAutopreset
        dlg.Fit()
        dlgSizer.Layout()
        # Bind variables
        dlg.nameBox = textCtrl0
        dlg.typeBox = choiceBox1
        dlg.argsBox = textCtrl2
        dlg.presetBox = textCtrl3
        dlg.resetCtrl = staticText2_5
        dlg.autopresetCheckbox = checkBox3
        dlg.cancelButton = cancel
        dlg.defaultArgs = ''
        dlg.defaultName = ''
        dlg.enteredName = ''
        self.FilterInfoDialog = dlg
    
    def CreatePluginsContextMenu(self):
        """Chose between long and short names"""
        
        def OnPluginsContextMenu(event):
            name = listbox.GetString(listbox.GetSelection()).split()[0].lower()
            item = menu.FindItemByPosition((self.pluginDict[name] + 2) % 3)
            item.Check()
            listbox.PopupMenu(menu)
        
        def OnContextMenuItem(event):
            id = event.GetId()
            if id in [idLong, idShort, idBoth]:
                if id == idLong:
                    value = 1
                elif id == idShort:
                    value = 2
                elif id == idBoth:
                    value = 0
                name = listbox.GetString(listbox.GetSelection())
                self.pluginDict[name.split()[0].lower()] = value
            else:
                if id == idLongOnly:
                    value = 1
                elif id == idShortOnly:
                    value = 2
                elif id == idAll:
                    value = 0
                for name in self.pluginDict:
                    self.pluginDict[name] = value
        
        listbox = self.notebook.GetPage(1).listbox
        listbox.Bind(wx.EVT_CONTEXT_MENU, OnPluginsContextMenu)
        idLong = wx.NewId()
        idShort = wx.NewId()
        idBoth = wx.NewId()
        idLongOnly = wx.NewId()
        idShortOnly = wx.NewId()
        idAll = wx.NewId()
        menu = wx.Menu()
        menu.AppendRadioItem(idLong, _('Long name'))
        menu.AppendRadioItem(idShort, _('Short name'))
        menu.AppendRadioItem(idBoth, _('Both'))
        menu.AppendSeparator()
        menu.Append(idLongOnly, _('Only long names'))
        menu.Append(idShortOnly, _('Only short names'))
        menu.Append(idAll, _('All names'))
        listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idLong)
        listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idShort)
        listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idBoth)
        listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idLongOnly)
        listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idShortOnly)
        listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idAll)
    
    def CheckAllFunctions(self, check=True):
        listbox = self.notebook.GetCurrentPage().listbox
        for i in xrange(listbox.GetCount()):
            listbox.Check(i, check)

    def _x_ClearLongNames(self):
        listbox = self.notebook.GetCurrentPage().listbox
        for i in xrange(listbox.GetCount()):
            if listbox.GetString(i).count('_') > 0:
                listbox.Check(i, False)

    def SelectInstalledFilters(self):
        index = self.notebook.GetSelection()
        if index == 1:
            filters = self.installed_plugins_filternames
        elif index == 2:
            filters = self.installed_avsi_filternames
        else: return
        listbox = self.notebook.GetCurrentPage().listbox
        for i in xrange(listbox.GetCount()):
            boolCheck = (listbox.GetString(i).split()[0].lower() in filters)
            listbox.Check(i, boolCheck)
    
    def ImportFromFiles(self, wiki=False):
        filenames, filterInfo, unrecognized = [], [], []
        if wiki:
            filenames = (self.GetParent().filterdbremote_plugins, 
                         self.GetParent().filterdbremote_scripts)
        else:
            title = _('Open Customization files, Avisynth scripts or Avsp options files')
            initial_dir = self.GetParent().ExpandVars(self.GetParent().options['pluginsdir'])
            filefilter = (_('All supported') + '|*.txt;*.md;*.avsi;*.avs;*.dat|' + 
                          _('Customization file') + ' (*.txt, *.md)|*.txt;*.md|' + 
                          _('AviSynth script') + ' (*.avs, *.avsi)|*.avs;*.avsi|' + 
                          _('AvsP data') + ' (*.dat)|*.dat|' + 
                          _('All files') + ' (*.*)|*.*')
            dlg = wx.FileDialog(self, title, initial_dir, '', filefilter, 
                                wx.OPEN|wx.MULTIPLE|wx.FILE_MUST_EXIST)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filenames = dlg.GetPaths()            
            dlg.Destroy()
            if not filenames:
                return
        
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            try:
                if ext in ['.avs', '.avsi']:
                    info = self.ParseAvisynthScript(filename)
                elif ext in ['.txt', '.md']:
                    info = self.ParseCustomizations(filename)
                elif ext == '.dat':
                    if filename.startswith('http'):
                        f = urllib2.urlopen(filename)
                    else:
                        f = open(filename, 'rb')
                    data = cPickle.load(f)
                    f.close()
                    info = []
                    for filtername, filterargs, ftype in data['filteroverrides'].values():
                        info.append((filename, filtername, filterargs, ftype))
                else:
                    info = None
            except (urllib2.URLError, urllib2.HTTPError), err:
                wx.MessageBox(u'\n\n'.join((os.path.basename(filename), unicode(err))), 
                              _('Error'), style=wx.OK|wx.ICON_ERROR)
                continue
            except:
                info = None
            if not info:
                unrecognized.append(filename)
            else:
                filterInfo += info
        if filterInfo and (wiki or not self.checkBox.IsChecked()):
            self.SelectImportFilters(filterInfo)
        for filename, filtername, filterargs, ftype in filterInfo:
            self.EditFunctionInfo(filtername, filterargs, ftype)
        if unrecognized:
            wx.MessageBox('\n'.join(unrecognized), _('Unrecognized files'))
    
    def SelectImportFilters(self, filterInfo):
        choices = []
        filterInfo.sort(key=lambda fi:
                    [i.lower() if isinstance(i, basestring) else i for i in fi])
        for filename, filtername, filterargs, ftype in filterInfo:
            choices.append(os.path.basename(filename) + ' -> ' + filtername)
        dlg = wx.Dialog(self, wx.ID_ANY, _('Select the functions to import'), 
                        style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        listbox = wx.CheckListBox(dlg, wx.ID_ANY, choices=choices, style=wx.LB_EXTENDED)
        customized, not_customized = [], []
        for i in range(len(choices)):
            filename, filtername = choices[i].lower().split(' -> ')
            if filtername in self.overrideDict:
                listbox.SetItemForegroundColour(i, wx.RED)
                customized.append(i)
            else:
                not_customized.append(i)
                if filename.find(filtername) != -1:
                    listbox.Check(i)    
        idSelectionAll = wx.NewId()
        idAll = wx.NewId()
        idFileAll = wx.NewId()
        idNotCustomizedAll = wx.NewId()
        idSelectionNone = wx.NewId()
        idNone = wx.NewId()
        idFileNone = wx.NewId()
        idCustomizedNone = wx.NewId()
        
        def OnContextMenuItem(event):
            id = event.GetId()
            value = id in (idSelectionAll, idAll, idFileAll, idNotCustomizedAll)
            if id in [idSelectionAll, idSelectionNone]:
                listbox_range = listbox.GetSelections()
            elif id in [idAll, idNone]:
                listbox_range = range(len(filterInfo))
            elif id in [idFileAll, idFileNone]:
                pos = listbox.GetSelections()
                if not pos:
                    return
                filename = filterInfo[pos[0]][0]
                listbox_range = (i for i in range(len(filterInfo)) 
                                 if filename == filterInfo[i][0])
            elif id == idNotCustomizedAll:
                listbox_range = not_customized
            elif id == idCustomizedNone:
                listbox_range = customized
            for i in listbox_range:
                listbox.Check(i, value)

        def OnContextMenu(event):
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idSelectionAll)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idAll)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idFileAll)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idNotCustomizedAll)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idSelectionNone)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idNone)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idFileNone)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idCustomizedNone)
            menu = wx.Menu()
            menu.Append(idSelectionAll, _('Check selected'))
            menu.Append(idAll, _('Check all'))
            menu.Append(idFileAll, _('Check all in this file'))
            menu.Append(idNotCustomizedAll, _('Check all not customized'))
            menu.AppendSeparator()
            menu.Append(idSelectionNone, _('Uncheck selected'))
            menu.Append(idNone, _('Uncheck all'))
            menu.Append(idFileNone, _('Uncheck all in this file'))
            menu.Append(idCustomizedNone, _('Uncheck all customized'))
            listbox.PopupMenu(menu)
            menu.Destroy()
        
        listbox.Bind(wx.EVT_CONTEXT_MENU, OnContextMenu)
        message = wx.StaticText(dlg, wx.ID_ANY, _('Red - a customized function already exists.'))
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(listbox, 1, wx.EXPAND|wx.ALL,5)        
        sizer.Add(message, 0, wx.LEFT, 5)
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL,5)
        dlg.SetSizerAndFit(sizer)
        ID = dlg.ShowModal()
        for i in range(len(choices)-1, -1, -1):
            if ID != wx.ID_OK or not listbox.IsChecked(i):
                del filterInfo[i]
        dlg.Destroy()
    
    def ParseAvisynthScript(self, *args, **kwargs):
        return self.GetParent().ParseAvisynthScript(*args, **kwargs)
    
    def ParseCustomizations(self, filename):
        if filename.startswith('http'):
            f = urllib2.urlopen(filename)
        else:
            f = open(filename)
        text = '\n'.join([line.strip() for line in f.readlines()])
        f.close()
        if filename.endswith('.md'):
            text = text.split('```text\n', 1)[1].rsplit('```', 1)[0]
        filterInfo = []
        for section in text.split('\n\n['):
            title, data = section.split(']\n',1)
            title = title.strip('[]').lower()
            if title == 'clipproperties':
                for item in data.split('\n'):
                    if not item.strip():
                        continue
                    splitstring = item.split('(', 1)
                    if len(splitstring) == 2:
                        filtername = splitstring[0].strip()
                        filterargs = '('+splitstring[1].strip(' ')
                    else:
                        filtername = item
                        filterargs = ''
                    filterInfo.append((filename, filtername, filterargs, 1))
            elif title == 'scriptfunctions':
                for item in data.split('\n'):
                    if not item.strip():
                        continue
                    splitstring = item.split('(', 1)
                    if len(splitstring) == 2:
                        filtername = splitstring[0].strip()
                        filterargs = '('+splitstring[1].strip(' ')
                    else:
                        filtername = item
                        filterargs = ''
                    filterInfo.append((filename, filtername, filterargs, 4))
            elif title == 'corefilters':
                for s in data.split('\n\n'):
                    splitstring = s.split('(', 1)
                    if len(splitstring) == 2:
                        filtername = splitstring[0].strip()
                        filterargs = '('+splitstring[1].strip(' ')
                        filterInfo.append((filename, filtername, filterargs, 0))
            elif title == 'plugins':
                for s in data.split('\n\n'):
                    splitstring = s.split('(', 1)
                    if len(splitstring) == 2:
                        filtername = splitstring[0].strip()
                        if not self.parent.GetPluginFunctionShortName(filtername.lower()):
                            print>>sys.stderr, '{0}: {1}'.format(_('Error'), _('Invalid plugin '
                                'function name "{name}". Must be "pluginname_functionname".').format(name=filtername))
                            continue
                        filterargs = '('+splitstring[1].strip(' ')
                        filterInfo.append((filename, filtername, filterargs, 2))
            elif title == 'userfunctions':
                for s in data.split('\n\n'):
                    splitstring = s.split('(', 1)
                    if len(splitstring) == 2:
                        filtername = splitstring[0].strip()
                        filterargs = '('+splitstring[1].strip(' ')
                        filterInfo.append((filename, filtername, filterargs, 3))
        return filterInfo
                
    def ExportCustomizations(self):
        if len(self.overrideDict) == 0:
            wx.MessageBox(_('No customizations to export!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        title = _('Save filter customizations')
        initial_dir = self.GetParent().programdir
        filefilter = _('Customization file') + ' (*.txt)|*.txt|' + _('All files') + ' (*.*)|*.*'
        dlg = wx.FileDialog(self, title, initial_dir, '', filefilter, wx.SAVE|wx.OVERWRITE_PROMPT)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            filename = dlg.GetPath()
            self.ExportFilterData(self.overrideDict, filename)
        dlg.Destroy()

    def ClearCustomizations(self):
        dlg = wx.MessageDialog(self, _('This will delete all filter customizations. Continue?'), _('Warning'), wx.YES_NO)
        ID = dlg.ShowModal()
        if ID == wx.ID_YES:
            #~ for lowername, (name, args, ftype) in self.overrideDict.items():
                #~ originalName = self.filterDict.get(lowername, [name])[0]
                #~ newName = originalName+' '
                #~ adjustedName = name+' '
                #~ if lowername in self.overrideDict:
                    #~ adjustedName += '*'
                #~ if lowername in self.presetDict:
                    #~ adjustedName += '~'
                    #~ newName += '~'
                #~ if newName != adjustedName:
                    #~ for index in xrange(self.notebook.GetPageCount()):
                        #~ panel = self.notebook.GetPage(index)
                        #~ if panel.functiontype == ftype:
                            #~ listbox = panel.listbox
                            #~ foundindex = listbox.FindString(adjustedName)
                            #~ if foundindex != wx.NOT_FOUND:
                                #~ listbox.SetString(foundindex, newName)
                            #~ break
            for lowername, (name, args, ftype) in self.overrideDict.iteritems():
                if ftype == 2 and lowername not in self.filterDict:
                    shortname = self.parent.GetPluginFunctionShortName(lowername)
                    if len(self.shortnamesDict[shortname]) == 1:
                        del self.shortnamesDict[shortname]
                    else:
                        self.shortnamesDict[shortname].remove(lowername)
            self.overrideDict = {}
            self.RefreshListNames()
        dlg.Destroy()

    def ClearPresets(self):
        dlg = wx.MessageDialog(self, _('This will delete all manually defined presets. Continue?'), _('Warning'), wx.YES_NO)
        ID = dlg.ShowModal()
        if ID == wx.ID_YES:
            #~ for lowername in self.presetDict.keys():
                #~ value = self.overrideDict.get(lowername)
                #~ if value is None:
                    #~ value = self.filterDict[lowername]
                #~ name, args, ftype = value
                #~ newName = name+' '
                #~ adjustedName = name+' '
                #~ if lowername in self.overrideDict:
                    #~ adjustedName += '*'
                    #~ newName += '*'
                #~ if lowername in self.presetDict:
                    #~ adjustedName += '~'
                #~ if newName != adjustedName:
                    #~ for index in xrange(self.notebook.GetPageCount()):
                        #~ panel = self.notebook.GetPage(index)
                        #~ if panel.functiontype == ftype:
                            #~ listbox = panel.listbox
                            #~ foundindex = listbox.FindString(adjustedName)
                            #~ if foundindex != wx.NOT_FOUND:
                                #~ listbox.SetString(foundindex, newName)
                            #~ break
            self.presetDict = {}
            self.RefreshListNames()
        dlg.Destroy()
        
    def RefreshListNames(self):
        for index in xrange(self.notebook.GetPageCount()):
            panel = self.notebook.GetPage(index)
            listbox = panel.listbox
            deleteIndices = []
            for i in xrange(listbox.GetCount()):
                name = listbox.GetString(i).split()[0]
                lowername = name.lower()
                extra = ' '
                if lowername in self.overrideDict:
                    extra += '*'
                elif lowername not in self.filterDict:
                    deleteIndices.append(i)
                    continue
                if lowername in self.presetDict:
                    extra += '~'
                newname = name+extra
                if listbox.GetString(i) != newname:
                    listbox.SetString(i, newname)
            deleteIndices.reverse()
            for i in deleteIndices:
                listbox.Delete(i)

    def AddNewFunction(self, name='', ftype=3, arg=None, prompt=None):
        dlg = self.FilterInfoDialog
        if ftype == -1:
            index = self.notebook.GetSelection()
            if index != wx.NOT_FOUND:
                ftype = self.notebook.GetPage(index).functiontype
            else:
                ftype = 3
        else:
            for index in xrange(self.notebook.GetPageCount()):
                panel = self.notebook.GetPage(index)
                if panel.functiontype == ftype:
                    self.notebook.SetSelection(index)
                    break
        #~ lowername = name.lower()
        #~ defaultValues = self.filterDict.get(lowername)
        #~ enteredValues = self.overrideDict.get(lowername, defaultValues)
        #~ if enteredValues is not None:
            #~ enteredName, enteredArgs, enteredType = enteredValues
            #~ defaultName, defaultArgs, defaultType = defaultValues
        #~ else:
            #~ enteredName, enteredArgs, enteredType = ('', '', 3)
            #~ defaultName, defaultArgs, defaultType = (None, None, None)
        #~ enteredPreset = self.presetDict.get(lowername)#, defaultPreset)
        #~ if enteredPreset is not None:
            #~ dlg.SetAutopreset(False)
        #~ else:
            #~ dlg.SetAutopreset(True)
            #~ enteredPreset = self.CreateDefaultPreset(name, enteredArgs)
        defaultName = name
        defaultArgs = '()' if not arg else arg
        dlg.nameBox.SetValue(defaultName)
        dlg.typeBox.SetSelection(ftype)
        dlg.typeBox.Enable()
        dlg.argsBox.SetValue(defaultArgs)
        dlg.presetBox.SetValue('')
        dlg.resetCtrl.Hide()
        dlg.SetAutopreset(True)
        dlg.cancelButton.SetFocus()
        dlg.defaultArgs = defaultArgs
        dlg.defaultName = defaultName
        dlg.enteredName = None
        if prompt is None:
            prompt = not bool(arg)
        if not prompt: ID = wx.ID_OK
        else: ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            newName = dlg.nameBox.GetValue()
            newType = dlg.typeBox.GetSelection()
            newArgs = dlg.argsBox.GetValue()
            newPreset = dlg.presetBox.GetValue()
            boolAutoPreset = dlg.autopresetCheckbox.GetValue()
            for index in xrange(self.notebook.GetPageCount()):
                panel = self.notebook.GetPage(index)
                if panel.functiontype == newType:
                    self.notebook.SetSelection(index)
                    listbox = panel.listbox
                    break
            #else:
                #return
            extra = ' '
            # Update the override dict
            #~ if (newName != defaultName) or (newArgs != defaultArgs):
                #~ self.overrideDict[lowername] = (newName, newArgs, newType)
                #~ extra += '*'
            #~ else:
                #~ if lowername in self.overrideDict:
                    #~ del self.overrideDict[lowername]
            lowername = newName.lower()
            self.overrideDict[lowername] = (newName, newArgs, newType)
            if newType == 2:
                self.pluginDict[lowername] = 0
                self.shortnamesDict[self.parent.GetPluginFunctionShortName(lowername)].append(lowername)
            extra += '*'
            # Update the preset dict
            if boolAutoPreset:
                if lowername in self.presetDict:
                    del self.presetDict[lowername]
            else:
                self.presetDict[lowername] = newPreset
                extra += '~'
            #~ listbox.SetString(listbox.GetSelection(), newName+extra)
            index = listbox.Append(newName+extra)
            listbox.Check(index)
            listbox.SetSelection(index)
            listbox.SetFirstItem(index)

    def EditFunctionInfo(self, name=None, arg=None, ftype=None, prompt=None):
        dlg = self.FilterInfoDialog
        if arg and ftype is not None:
            arg = arg.strip()
            name = unicode(name)
            for index in xrange(self.notebook.GetPageCount()):
                panel = self.notebook.GetPage(index)
                if panel.functiontype == ftype:
                    break
        else:
            panel = self.notebook.GetCurrentPage()
        listbox = panel.listbox
        functiontype = panel.functiontype
        if name is None:
            name = listbox.GetStringSelection().split()[0]
        if not name:
            return
        lowername = name.lower()
        if lowername not in self.filterDict and lowername not in self.overrideDict:
            if not ftype:
                self.AddNewFunction(name)
            else:
                self.AddNewFunction(name, ftype, arg)
            return
        # Fill out default values
        #~ defaultName = self.filterDict[lowername][0]
        #~ defaultArgs = self.filterDict[lowername][1]
        defaultName, defaultArgs, defaultType = self.filterDict.get(lowername, ('', '', None))
        #~ defaultPreset = self.CreateDefaultPreset(name, defaultArgs)
        enteredName = name
        enteredType = functiontype
        enteredArgs = self.overrideDict.get(lowername, (None, defaultArgs, None))[1] if not arg else arg
        #~ defaultPreset = self.CreateDefaultPreset(name, enteredArgs)
        enteredPreset = self.presetDict.get(lowername)#, defaultPreset)
        if enteredPreset is not None:
            dlg.SetAutopreset(False)
        else:
            dlg.SetAutopreset(True)
            enteredPreset = self.CreateDefaultPreset(name, enteredArgs)
        dlg.nameBox.SetValue(enteredName)
        dlg.typeBox.SetSelection(enteredType)
        dlg.argsBox.SetValue(enteredArgs)
        dlg.presetBox.SetValue(enteredPreset)
        if lowername in self.filterDict:
            dlg.typeBox.Disable()
            dlg.resetCtrl.Show()
        else:
            dlg.typeBox.Enable()
            dlg.resetCtrl.Hide()
        dlg.cancelButton.SetFocus()
        dlg.defaultArgs = defaultArgs
        #~ self.defaultPreset = defaultPreset
        dlg.defaultName = defaultName
        dlg.enteredName = enteredName
        if prompt is None:
            prompt = not bool(arg)
        if not prompt: ID = wx.ID_OK
        else: ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            newName = dlg.nameBox.GetValue()
            newType = dlg.typeBox.GetSelection()
            newArgs = dlg.argsBox.GetValue()
            newPreset = dlg.presetBox.GetValue()
            boolAutoPreset = dlg.autopresetCheckbox.GetValue()
            extra = ' '
            # Update the override dict
            if (newName != defaultName) or (newArgs != defaultArgs):
                self.overrideDict[lowername] = (newName, newArgs, newType)
                extra += '*'
            else:
                if lowername in self.overrideDict:
                    del self.overrideDict[lowername]
            # Update the preset dict
            if boolAutoPreset:
                if lowername in self.presetDict:
                    del self.presetDict[lowername]
            else:
                self.presetDict[lowername] = newPreset
                extra += '~'
            if newType == enteredType:
                if arg and ftype is not None:
                    for i in xrange(listbox.GetCount()):
                        if newName == listbox.GetString(i).split()[0]:
                            listbox.SetSelection(i)
                            break
                listbox.SetString(listbox.GetSelection(), newName+extra)
            else:
                shortname = self.parent.GetPluginFunctionShortName(lowername)
                if newType == 2:
                    self.pluginDict[lowername] = 0
                    self.shortnamesDict[shortname].append(lowername)
                elif enteredType == 2:
                    del self.pluginDict[lowername]
                    if len(self.shortnamesDict[shortname]) == 1:
                        del self.shortnamesDict[shortname]
                    else:
                        self.shortnamesDict[shortname].remove(lowername)
                for index in xrange(self.notebook.GetPageCount()):
                    panel = self.notebook.GetPage(index)
                    if panel.functiontype == newType:
                        listindex = listbox.GetSelection()
                        ischecked = listbox.IsChecked(listindex)
                        listbox.Delete(listindex)
                        listindex = panel.listbox.Append(newName+extra)
                        panel.listbox.SetSelection(listindex)
                        panel.listbox.SetFirstItem(listindex)
                        panel.listbox.Check(listindex, ischecked)
                        self.notebook.SetSelection(index)
                        break
                else:
                    return

    def DeleteFunction(self):
        panel = self.notebook.GetCurrentPage()
        listbox = panel.listbox
        index = listbox.GetSelection()
        if index == wx.NOT_FOUND:
            return
        complete_string = listbox.GetString(index)
        name = complete_string.split()[0]
        lowername = name.lower()
        added_by_user = lowername not in self.filterDict
        modified = lowername != complete_string.rstrip().lower()
        if not added_by_user and not modified:
            return
        delete = not self.nag
        if self.nag:
            if added_by_user:
                message = _('Do you really want to delete this custom filter?')
            else:
                message = _('Do you really want to reset this filter?')
            dlg = wx.MessageDialog(self, message, _('Warning'), wx.YES_NO)
            ID = dlg.ShowModal()
            if ID == wx.ID_YES:
                delete = True
            dlg.Destroy()
        if delete:
            if lowername in self.overrideDict:
                del self.overrideDict[lowername]
            if lowername in self.presetDict:
                del self.presetDict[lowername]
            if added_by_user:
                if panel.functiontype == 2:
                    del self.pluginDict[lowername]
                    shortname = self.parent.GetPluginFunctionShortName(lowername)
                    if len(self.shortnamesDict[shortname]) == 1:
                        del self.shortnamesDict[shortname]
                    else:
                        self.shortnamesDict[shortname].remove(lowername)
                if lowername in self.removedSet:
                    self.removedSet.remove(lowername)
                listbox.Delete(index)
            else:
                listbox.SetString(index, name)
    
    def GetOverrideDict(self):
        return self.overrideDict

    def GetPresetDict(self):
        return self.presetDict

    def GetRemovedSet(self):
        return self.removedSet

    def GetAutocompletePluginNames(self):
        return self.pluginDict
    
    def GetPluginShortNames(self):
        return self.shortnamesDict


# Dialog specifically for AviSynth filter auto-slider information
class AvsFilterAutoSliderInfo(wx.Dialog):
    def __init__(self, parent, mainFrame, filterName, filterInfo, title=_('Edit filter database')):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.mainFrame = mainFrame
        self.newFilterInfo = None
        # Filter name label
        filterLabel = wx.StaticText(self, wx.ID_ANY, filterName)
        font = filterLabel.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        filterLabel.SetFont(font)
        # Arguments
        argWindow = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        argWindow.SetScrollRate(10, 10)
        argSizer = wx.GridBagSizer(hgap=0, vgap=10)
        row = 0
        growable = False
        self.argctrls = []
        for argInfo in self.mainFrame.currentScript.GetFilterCalltipArgInfo(calltip=filterInfo):
            totalInfo, cArgType, cArgName, boolRepeatArg, boolOptionalArg, cArgInfo = argInfo
            argtype, argname, guitype, defaultValue, other = self.mainFrame.ParseCalltipArgInfo(totalInfo)
            #~ if guitype is None or argname is None or argtype not in ('int', 'float', 'bool', 'string'):
            if argname is None or argtype not in ('int', 'float', 'bool', 'string'):
                self.argctrls.append((argtype, argname, None, boolRepeatArg, boolOptionalArg))
            else:
                argLabel = wx.StaticText(argWindow, wx.ID_ANY, '%(argtype)s %(argname)s' % locals())
                argLabel.controls = []
                argSizer.Add(argLabel, (row,0), wx.DefaultSpan, wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.BOTTOM|wx.RIGHT, 5)
                if argtype in ('int', 'float') and guitype != 'intlist':
                    strDefaultValue = strMinValue = strMaxValue = strMod = ''
                    if other is not None:
                        minValue, maxValue, nDecimal, mod = other
                        if nDecimal is None:
                            nDecimal = 0
                        strTemplate = '%.'+str(nDecimal)+'f'
                        if defaultValue is not None:
                            try:
                                strDefaultValue = strTemplate % defaultValue
                            except TypeError:
                                strDefaultValue = defaultValue
                        if minValue is not None:
                            try:
                                strMinValue = strTemplate % minValue
                            except TypeError:
                                strMinValue = minValue
                        if maxValue is not None:
                            try:
                                strMaxValue = strTemplate % maxValue
                            except TypeError:
                                strMaxValue = maxValue
                        if mod is not None:
                            try:
                                strMod = '%i' % mod
                            except TypeError:
                                strMod = mod
                    elif guitype == 'color':
                        strDefaultValue = '$%s' % defaultValue
                    itemData = (
                        (strDefaultValue, _('Default')),
                        (strMinValue, _('Min value')),
                        (strMaxValue, _('Max value')),
                        (strMod, _('Step size')),
                    )
                    hsizer = wx.BoxSizer(wx.HORIZONTAL)
                    for itemValue, itemName in itemData:
                        itemLabel = wx.StaticText(argWindow, wx.ID_ANY, itemName)
                        itemTextCtrl = wx.TextCtrl(argWindow, wx.ID_ANY, itemValue,size=(75,-1))
                        vsizer = wx.BoxSizer(wx.VERTICAL)
                        vsizer.Add(itemLabel, 0, wx.LEFT, 2)
                        vsizer.Add(itemTextCtrl, 0, wx.ALL, 0)
                        hsizer.Add(vsizer, 0, wx.EXPAND|wx.RIGHT,5)
                        argLabel.controls.append(itemTextCtrl)
                    argSizer.Add(hsizer, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 0)
                elif argtype == 'bool':
                    strDefaultValue = ''
                    if defaultValue is not None:
                        if defaultValue.lower() == 'true':
                            strDefaultValue = 'True'
                        if defaultValue.lower() == 'false':
                            strDefaultValue = 'False'
                    itemLabel = wx.StaticText(argWindow, wx.ID_ANY, _('Default'))
                    itemTextCtrl = wx.ComboBox(argWindow, wx.ID_ANY, strDefaultValue, choices=['True', 'False'], style=wx.CB_DROPDOWN, size=(75,-1))
                    vsizer = wx.BoxSizer(wx.VERTICAL)
                    vsizer.Add(itemLabel, 0, wx.LEFT, 2)
                    vsizer.Add(itemTextCtrl, 0, wx.ALL, 0)
                    argLabel.controls.append(itemTextCtrl)
                    argSizer.Add(vsizer, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 0)
                elif argtype == 'string' or argtype == 'int' and guitype == 'intlist':
                    strDefaultValue = strValuesList = ''
                    if defaultValue is not None:
                        if defaultValue:
                            if argtype == 'string':
                                strDefaultValue = '"%s"' % defaultValue.strip('"')
                            else:
                                strDefaultValue = str(defaultValue)
                    if other is not None:
                        strValuesList = ', '.join(other)
                    hsizer = wx.BoxSizer(wx.HORIZONTAL)
                    # Default control
                    itemLabel = wx.StaticText(argWindow, wx.ID_ANY, _('Default'))
                    itemTextCtrl = wx.TextCtrl(argWindow, wx.ID_ANY, strDefaultValue, size=(75,-1))
                    vsizer = wx.BoxSizer(wx.VERTICAL)
                    vsizer.Add(itemLabel, 0, wx.LEFT, 2)
                    vsizer.Add(itemTextCtrl, 0, wx.ALL, 0)
                    argLabel.controls.append(itemTextCtrl)
                    hsizer.Add(vsizer, 0, wx.EXPAND|wx.RIGHT,5)
                    # Values control
                    itemLabel = wx.StaticText(argWindow, wx.ID_ANY, _('Value list (comma separated)'))
                    itemTextCtrl = wx.TextCtrl(argWindow, wx.ID_ANY, strValuesList, size=(200,-1))
                    vsizer = wx.BoxSizer(wx.VERTICAL)
                    vsizer.Add(itemLabel, 0, wx.LEFT, 2)
                    vsizer.Add(itemTextCtrl, 1, wx.EXPAND|wx.ALL, 0)
                    argLabel.controls.append(itemTextCtrl)
                    hsizer.Add(vsizer, 1, wx.EXPAND|wx.RIGHT,5)

                    argSizer.Add(hsizer, (row,1), wx.DefaultSpan, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 0)
                    if wx.VERSION > (2, 9):
                        if not argSizer.IsColGrowable(1):
                            argSizer.AddGrowableCol(1)
                    else:
                        if not growable:
                            argSizer.AddGrowableCol(1)
                            growable = True
                row += 1
                self.argctrls.append((argtype, argname, argLabel, boolRepeatArg, boolOptionalArg))
        argWindow.SetSizer(argSizer)
        # Standard buttons
        okay  = wx.Button(self, wx.ID_OK, _('OK'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, okay)
        okay.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Set the sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((-1,-1), 0, wx.TOP, 10)
        sizer.Add(filterLabel, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        sizer.Add(argWindow, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        #~ sizer.Add(wx.StaticText(self,wx.ID_ANY, _('* optional value')), 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Layout()
        argWindow.FitInside()
        w, h = argSizer.GetMinSize()
        w = max(w + 10, 400)
        h = min(h + 100, 700)
        self.SetSize(self.ClientToWindowSize((w, h)))
        if argWindow.HasScrollbar(wx.HORIZONTAL):
            scrollbar_w = wx.SystemSettings_GetMetric(wx.SYS_VSCROLL_X)
            self.SetSize(self.ClientToWindowSize((w + scrollbar_w, -1)))
    
    def OnButtonOK(self, event):
        strList = []
        for argtype, argname, argLabel, boolRepeatArg, boolOptionalArg in self.argctrls:
            if argtype is None and argname is None:
                continue
            strBase = '%(argtype)s %(argname)s' % locals()
            strInfoNew = strBase
            if argLabel is None:
                if argname is None:
                    strInfoNew = argtype
            else:
                
                strDef = argLabel.controls[0].GetValue().strip()
                is_list = argtype == 'int' and argLabel.controls[1].GetValue().count(',')
                #~ strList.append('%(strBase)s=%(strDefaultValue)s' % locals())
                if argtype in ('int', 'float') and not is_list:
                    strMin = argLabel.controls[1].GetValue().strip()
                    strMax = argLabel.controls[2].GetValue().strip()
                    strMod = argLabel.controls[3].GetValue().strip()
                    # Validate if any field has input
                    sliderValues = None
                    if strDef or strMin or strMax or strMod:
                        errorType, errorMessage, sliderValues = self.mainFrame.ValidateAvsSliderInputs(strDef, strMin, strMax, strMod)
                        if errorType is not None and errorType != -1:
                            self.ShowWarning(argLabel.controls[errorType], '%(argtype)s %(argname)s: %(errorMessage)s' % locals())
                            return
                    # Create the new string info
                    #~ if sliderValues is not None and len(sliderValues) == 1:
                    if strDef and not strMin and not strMax:
                        strInfoNew = '%(strBase)s=%(strDef)s' % locals()
                    elif not strMin and not strMax:
                        strInfoNew = strBase
                    elif strMod:
                        strInfoNew = '%(strBase)s=%(strDef)s (%(strMin)s to %(strMax)s by %(strMod)s)' % locals()
                    else:
                        strInfoNew = '%(strBase)s=%(strDef)s (%(strMin)s to %(strMax)s)' % locals()
                elif argtype == 'bool':
                    if strDef:
                        if strDef.lower() not in ('true', 'false'):
                            self.ShowWarning(argLabel.controls[0], '%s %s: %s' % (argtype, argname, _('Value must be True or False!')), comboBox=True)
                            return
                        strInfoNew = '%(strBase)s=%(strDef)s' % locals()
                elif argtype == 'string' or argtype == 'int' and is_list:
                    strValues = argLabel.controls[1].GetValue().strip()
                    if strDef or strValues:
                        if not strValues:
                            strValuesNew = ''
                            #~ msg =  _('Must enter a value list!')
                            #~ self.ShowWarning(argLabel.controls[1], '%s %s: %s' % (argtype, argname,msg))
                            #~ return
                            pass
                        else:
                            if argtype == 'int':
                                strValuesNew = ' (%s)' % ' / '.join([s.strip() for s in strValues.split(',')])
                            else:
                                strValuesNew = ' (%s)' % '/ '.join(['"%s"' % s.strip(' "') for s in strValues.split(',')])
                        if strDef and argtype == 'string':
                            strDef = '"%s"' % strDef.strip('"')
                        strInfoNew = '%(strBase)s=%(strDef)s%(strValuesNew)s' % locals()
            strRepeatArg = ''
            if boolRepeatArg:
                strRepeatArg = ' [, ...]'
            if boolOptionalArg:
                strInfoNew = '[{0}]'.format(strInfoNew)
            strList.append(strInfoNew+strRepeatArg)
        self.newFilterInfo = '(\n%s\n)' % ',\n'.join(strList)
        event.Skip()

    def GetNewFilterInfo(self):
        return self.newFilterInfo

    def ShowWarning(self, textCtrl, message, comboBox=False):
        color = textCtrl.GetBackgroundColour()
        textCtrl.SetBackgroundColour('pink')
        textCtrl.Refresh()
        wx.MessageBox(message, _('Error'), style=wx.OK|wx.ICON_ERROR)
        textCtrl.SetBackgroundColour(color)
        textCtrl.Refresh()
        textCtrl.GetParent().Refresh()
        if comboBox:
            textCtrl.SetMark(-1,-1)
        else:
            textCtrl.SetSelection(-1,-1)
        textCtrl.SetFocus()
        textCtrl.Refresh()

# Dialog for filter customization exporting/importing
class AvsFunctionExportImportDialog(wx.Dialog):
    def __init__(self, parent, infoDict, export=True):
        self.export = export
        if export:
            title = _('Export filter customizations')
        else:
            title = _('Import filter customizations')
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, size=(500, 300), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.calltipDict = infoDict[0]
        self.presetDict = infoDict[1]
        self.docpathDict = infoDict[2]
        self.functiontypeDict = infoDict[3]

        # Create the list control using the dictionary
        decList = [(s.lower(), s) for s in self.calltipDict.keys()]
        decList.sort()
        self.names = [s[1] for s in decList]
        self.checkListBox = wx.CheckListBox(self, wx.ID_ANY, choices=self.names)

        # Create extra control buttons
        def OnButtonSelectAll(event):
            for index in xrange(len(self.names)):
                self.checkListBox.Check(index, True)
        def OnButtonClearAll(event):
            for index in xrange(len(self.names)):
                self.checkListBox.Check(index, False)
        buttonSelectAll = wx.Button(self, wx.ID_ANY, _('Select all'))
        self.Bind(wx.EVT_BUTTON, OnButtonSelectAll, buttonSelectAll)
        buttonClearAll = wx.Button(self, wx.ID_ANY, _('Clear all'))
        self.Bind(wx.EVT_BUTTON, OnButtonClearAll, buttonClearAll)

        if export:
            staticText = wx.StaticText(self, wx.ID_ANY, _('Select filters to export:'))
            extraItem = (-1, 20)
        else:
            staticText = wx.StaticText(self, wx.ID_ANY, _('Select filters to import from the file:'))
            # Import dialog, check all names by default
            for index in xrange(len(self.names)):
                self.checkListBox.Check(index)
            # Extra controls to provide options for import information
            #~ self.checkBoxCalltip = wx.CheckBox(self, wx.ID_ANY, _('Calltips'))
            #~ self.checkBoxPreset = wx.CheckBox(self, wx.ID_ANY, _('Presets'))
            #~ self.checkBoxDocpath = wx.CheckBox(self, wx.ID_ANY, _('Docpaths'))
            #~ self.checkBoxType = wx.CheckBox(self, wx.ID_ANY, _('Filter types'))
            #~ staticBox = wx.StaticBox(self, wx.ID_ANY, _('Import from filters:'))
            #~ staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
            #~ for item in (self.checkBoxCalltip, self.checkBoxPreset, self.checkBoxDocpath, self.checkBoxType):
                #~ item.SetValue(True)
                #~ staticBoxSizer.Add(item, 0, wx.ALL, 5)
            self.checkBoxOverwriteAll = wx.CheckBox(self, wx.ID_ANY, _('Overwrite all data'))
            self.checkBoxOverwriteAll.SetValue(True)
            extraItem = wx.BoxSizer(wx.VERTICAL)
            #~ extraItem.Add(staticBoxSizer, 0, wx.BOTTOM, 10)
            extraItem.Add(self.checkBoxOverwriteAll, 0, wx.LEFT|wx.BOTTOM, 5)

        # Standard buttons
        okay  = wx.Button(self, wx.ID_OK, _('OK'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, okay)
        cancel = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()

        # Size the elements
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.Add(buttonSelectAll, 0, wx.ALL, 5)
        buttonSizer.Add(buttonClearAll, 0, wx.ALL, 5)
        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer.Add(self.checkListBox, 1, wx.EXPAND|wx.ALL, 5)
        listSizer.Add(buttonSizer, 0, wx.ALL, 5)
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add((-1,5))
        dlgSizer.Add(staticText, 0, wx.ALL, 5)
        dlgSizer.Add(listSizer, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        dlgSizer.Add(extraItem, 0, wx.ALL, 5)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(dlgSizer)
        dlgSizer.SetSizeHints(self)
        # Misc
        okay.SetDefault()

    def OnButtonOK(self, event):
        self.dlgDataDict = {}
        # Build the dictionnary from the checked filters
        for i, name in enumerate(self.names):
            if self.checkListBox.IsChecked(i):
                calltip = self.calltipDict.get(name, '')
                preset = self.presetDict.get(name, '')
                docpath = self.docpathDict.get(name, '')
                ftype = self.functiontypeDict.get(name, '')
                self.dlgDataDict[name] = (calltip, preset, docpath, ftype)
        if not self.dlgDataDict:
            wx.MessageBox(_('You must select at least one filter!'), _('Warning'))
            return
        event.Skip()

    def GetData(self):
        return self.dlgDataDict

    def GetOverwriteAll(self):
        return self.checkBoxOverwriteAll.GetValue()

# Custom slider
class SliderPlus(wx.Panel):
    def __init__(self, parent, app, id, value=0, minValue=0, maxValue=100, size=(-1, 28), big=False, bookmarkDict={}):
        self.big = big
        if self.big:
            size = size[0], size[1] + 16
        wx.Panel.__init__(self, parent, id, size=size, style=wx.WANTS_CHARS)
        self.bookmarkDict = bookmarkDict
        self.parent = parent
        self.app = app
        self.minValue = minValue
        self.maxValue = maxValue
        self.value = max(min(value, self.maxValue), self.minValue)
        self.bookmarks = {}
        self.mouse_wheel_rotation = 0
        # Internal display variables
        self.isclicked = False
        self.xdelta = None
        self.xo = 15
        self.yo = 5
        self.yo2 = 10
        self.wT = 22
        self.wH = 10
        if self.big:
            self.xo += 8
            self.yo += 4
            self.yo2 += 4
            self.wT += 8
            self.wH += 4
        self.selections = None
        self.selmode = 0
        self._DefineBrushes()
        # Event binding
        self.Bind(wx.EVT_PAINT, self._OnPaint)
        self.Bind(wx.EVT_SIZE, self._OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self._OnLeftDown)
        self.Bind(wx.EVT_MOTION, self._OnMouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self._OnLeftUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self._OnMouseWheel)
        self.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)
        def OnSetFocus(event):
            if not self.HasCapture():
                try:
                    event.GetWindow().SetFocus()
                except AttributeError:
                    event.Skip()
        self.Bind(wx.EVT_SET_FOCUS, OnSetFocus)

    def _DefineBrushes(self):
        #~ colorBackground = self.parent.GetBackgroundColour()
        colorBackground = self.GetBackgroundColour()
        colorHighlight = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT)
        colorHighlight2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DHILIGHT)
        colorShadow = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW)
        colorDarkShadow = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW)
        colorWindow = colorHighlight2#wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        #~ colorHandle = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)
        colorHandle = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        r,g,b = colorHandle.Red(), colorHandle.Green(), colorHandle.Blue()
        #~ colorHandle2 = wx.Colour(min(r+30, 255),min(g+30, 255),min(b+30, 255))#wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR)
        colorHandle2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
        colorGrayText = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self.penWindowBackground = wx.Pen(colorBackground)
        self.brushWindowBackground = wx.Brush(colorBackground)
        self.penBackground = wx.Pen(colorWindow)
        self.brushBackground = wx.Brush(colorWindow)
        self.penShadow = wx.Pen(colorShadow)
        self.penDarkShadow = wx.Pen(colorDarkShadow)
        self.penHighlight = wx.Pen(colorHighlight)
        self.penHighlight2 = wx.Pen(colorHighlight2)
        self.penHandle = wx.Pen(colorHandle)
        self.brushHandle = wx.Brush(colorHandle)
        self.penHandle2 = wx.Pen(colorHandle2)
        self.brushHandle2 = wx.Brush(colorHandle2)
        self.penGrayText = wx.Pen(colorGrayText)
        self.brushGrayText = wx.Brush(colorGrayText)

    def _OnLeftDown(self, event):
        self.app.lastshownframe = self.app.paintedframe
        mousepos = event.GetPosition()
        x, y, w, h = self.GetRect()
        #~ pixelpos = int(self.value * (w-2*self.xo) / float(self.maxValue - self.minValue))
        #~ rectHandle = wx.Rect(pixelpos-self.wH/2+self.xo, self.yo-3, self.wH, h-self.yo-self.yo2+6)
        rectHandle = self._getRectHandle()
        rectBox = wx.Rect(0, 0+self.yo, w, h-self.yo-self.yo2)
        if rectHandle.Inside(mousepos):
            self.isclicked = True
            self.xdelta = mousepos.x - rectHandle.x
            self.CaptureMouse()
            if self.IsDoubleBuffered():
                dc = wx.ClientDC(self)
            else:
                dc = wx.BufferedDC(wx.ClientDC(self))
            dc.Clear()
            self._PaintSlider(dc)
        elif self.selmode == 1 and self._HitTestHandleDeadZone(mousepos):
            pass
        elif rectBox.Inside(mousepos):
            self.isclicked = True
            self.CaptureMouse()
            oldvalue = self.value
            #~ self.SetValue(int(round((mousepos.x-self.xo+self.wH/2) * (self.maxValue - self.minValue) / float(w-2*self.xo))))
            self.SetValue(int(round((mousepos.x-self.xo) * (self.maxValue - self.minValue) / float(w-2*self.xo))))
            if self.value != oldvalue:
                self._SendScrollEvent()
            rectHandle = self._getRectHandle()
            self.xdelta = mousepos.x - rectHandle.x
        event.Skip()

    def _OnMouseMotion(self, event):
        if event.Dragging() and event.LeftIsDown() and self.HasCapture():
            x, y, w, h = self.GetRect()
            xmouse, ymouse = event.GetPosition()
            oldvalue = self.value
            #~ self.value = int(round((xmouse-self.xdelta-self.xo+self.wH/2) * (self.maxValue - self.minValue) / float(w-2*self.xo)))
            #~ self.value = max(min(self.value, self.maxValue), self.minValue)
            self.SetValue(int(round((xmouse-self.xdelta-self.xo+self.wH/2) * (self.maxValue - self.minValue) / float(w-2*self.xo))))
            if self.value != oldvalue:
                self._SendScrollEvent()
            #~ dc = wx.BufferedDC(wx.ClientDC(self))
            #~ dc.Clear()
            #~ self._PaintSlider(dc)

    def _OnLeftUp(self, event):
        self.isclicked = False
        self.xdelta = None
        if self.HasCapture():
            self.ReleaseMouse()
            self.adjust_handle = True
            self._SendScrollEndEvent()
            # Done in ShowVideoFrame by calling SetValue
            #~if self.IsDoubleBuffered():
            #~    dc = wx.ClientDC(self)
            #~else:
            #~    dc = wx.BufferedDC(wx.ClientDC(self))
            #~dc.Clear()
            #~self._PaintSlider(dc)
        else:
            # If clicked on a bookmark, go to that frame
            mousepos = event.GetPosition()
            index = self.HitTestBookmark(mousepos)
            if index is not None:
                self.SetValue(index)
                self.adjust_handle = False
                self._SendScrollEndEvent()
            #~ # If clicked on a selection button, create the selection bookmark
            #~ bmtype = self.HitTestSelectionButton(mousepos)
            #~ if bmtype is not None:
                #~ if self.bookmarks.count((self.value, bmtype)) == 0:
                    #~ self.SetBookmark(self.value, bmtype)
                #~ else:
                    #~ self.RemoveBookmark(self.value, bmtype)
        event.Skip()

    def _OnMouseWheel(self, event):
        #~ if event.LeftIsDown():
        if not self.HasCapture():
            rotation = event.GetWheelRotation()
            if self.mouse_wheel_rotation * rotation < 0:
                self.mouse_wheel_rotation = rotation
            else:
                self.mouse_wheel_rotation += rotation
            if abs(self.mouse_wheel_rotation) >= event.GetWheelDelta():
                delta = -1 if self.mouse_wheel_rotation > 0 else 1 
                if self.app.options['invertscrolling']: delta = -delta
                self.mouse_wheel_rotation = 0
                oldvalue = self.value
                self.SetValue(self.value + delta)
                if self.value != oldvalue:
                    self._SendScrollEvent()

    def _OnKeyDown(self, event):
        if self.HasCapture():
            key = event.GetKeyCode()
            oldvalue = self.value
            if key in (wx.WXK_LEFT, wx.WXK_UP):
                self.SetValue(self.value-1)
            elif key in (wx.WXK_RIGHT, wx.WXK_DOWN):
                self.SetValue(self.value+1)
            if self.value != oldvalue:
                self._SendScrollEvent()

    def _SendScrollEvent(self):
        event = wx.CommandEvent(wx.wxEVT_SCROLL_THUMBTRACK, self.GetId())
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def _SendScrollEndEvent(self):
        event = wx.CommandEvent(wx.wxEVT_SCROLL_ENDSCROLL, self.GetId())
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)

    def _OnSize(self, event):
        if self.IsDoubleBuffered():
            dc = wx.ClientDC(self)
        else:
            dc = wx.BufferedDC(wx.ClientDC(self))
        dc.Clear()
        self._PaintSlider(dc)

    def _OnPaint(self, event):
        # Color info
        self._DefineBrushes()
        dc = wx.PaintDC(self)
        #~ dc = wx.BufferedPaintDC(self)
        self._PaintSlider(dc)

    def _PaintSlider(self, dc):
        boolEnabled = self.IsEnabled()
        # Paint the bar
        x, y = (0, 0)
        w, h = self.GetSize()
        xB, yB, wB, hB = self.xo, self.yo, w-2*self.xo, h-self.yo-self.yo2
        xH, yH, wH, hH = -1, self.yo-3, self.wH, hB+6
        # First paint background
        dc.SetPen(self.penWindowBackground)
        dc.SetBrush(self.brushWindowBackground)
        dc.DrawRectangle(0, 0, w, h)
        dc.SetPen(self.penBackground)
        dc.SetBrush(self.brushBackground)
        dc.DrawRectangle(xB, yB, wB, hB)
        # Then paint the bookmark selections
        if self.selections is not None:
            if boolEnabled:
                dc.SetPen(wx.Pen(wx.BLUE))
                dc.SetBrush(wx.BLUE_BRUSH)
            else:
                color = wx.Colour(200,200,230)
                dc.SetPen(wx.Pen(color))
                dc.SetBrush(wx.Brush(color))
            for start, stop in self.selections:
                start = min(max(start, self.minValue), self.maxValue)
                stop = min(max(stop, self.minValue), self.maxValue)
                pixelstart = int(start * wB / float(self.maxValue - self.minValue)) + self.xo
                pixelstop = int(stop * wB / float(self.maxValue - self.minValue)) + self.xo
                dc.DrawRectangle(pixelstart, yB, pixelstop - pixelstart, hB)
        # Then draw the bookmark triangles
        dc.SetPen(self.penWindowBackground)
        if boolEnabled:
            dc.SetBrush(wx.BLACK_BRUSH)
        else:
            dc.SetBrush(self.brushGrayText)
        wT = self.wT
        drawnBookmarks = dict()
        for value, bmtype in self.bookmarks.items():
            if value > self.maxValue or value < self.minValue:
                continue
            pixelpos = int(value * wB / float(self.maxValue - self.minValue)) + self.xo
            try:
                if drawnBookmarks[pixelpos] == bmtype:
                    continue
            except KeyError:
                pass
            drawnBookmarks[pixelpos] = bmtype

            p1 = wx.Point(pixelpos, h-wT/2)
            if bmtype == 0:
                if value in self.bookmarkDict:                    
                    dc.SetBrush(wx.BLUE_BRUSH)
                else:
                    dc.SetBrush(wx.BLACK_BRUSH)
                p2 = wx.Point(pixelpos-wT/4, h)
                p3 = wx.Point(pixelpos+wT/4, h)
                dc.DrawPolygon((p1, p2, p3))
            elif bmtype == 1:
                p2 = wx.Point(pixelpos-wT/2, h)
                p3 = wx.Point(pixelpos, h)
                dc.DrawPolygon((p1, p2, p3))
                dc.SetPen(wx.BLACK_PEN)
                dc.DrawLine(pixelpos, h-1, pixelpos+wT/4, h-1)
                dc.SetPen(self.penWindowBackground)
            elif bmtype == 2:
                p2 = wx.Point(pixelpos, h)
                p3 = wx.Point(pixelpos+wT/2, h)
                dc.DrawPolygon((p1, p2, p3))
                dc.SetPen(wx.BLACK_PEN)
                dc.DrawLine(pixelpos, h-1, pixelpos-wT/4, h-1)
                dc.SetPen(self.penWindowBackground)
        # Then paint the border
        dc.SetPen(self.penShadow)
        dc.DrawLine(xB, yB, xB+wB, yB)
        dc.DrawLine(xB, yB, xB, yB+hB)
        dc.SetPen(self.penDarkShadow)
        dc.DrawLine(xB+1, yB+1, xB+wB, yB+1)
        dc.DrawLine(xB+1, yB+1, xB+1, yB+hB)
        dc.SetPen(self.penHighlight2)
        dc.DrawLine(xB+wB, yB, xB+wB, yB+hB)
        dc.DrawLine(xB, yB+hB, xB+wB+1, yB+hB)
        dc.SetPen(self.penHighlight)
        dc.DrawLine(xB+wB-1, yB+1, xB+wB-1, yB+hB)
        dc.DrawLine(xB+1, yB+hB-1, xB+wB, yB+hB-1)
        # Then paint the handle
        pixelpos = int(self.value * wB / float(self.maxValue - self.minValue)) + self.xo
        pixelpos0 = pixelpos - self.wH/2
        if self.isclicked or not boolEnabled:
            dc.SetPen(self.penHandle2)
            dc.SetBrush(self.brushHandle2)
        else:
            dc.SetPen(self.penHandle)
            dc.SetBrush(self.brushHandle)
        dc.DrawRectangle(pixelpos0, yH, wH, hH)
        dc.SetPen(self.penHighlight2)
        dc.DrawLine(pixelpos0, yH, pixelpos0+wH, yH)
        dc.DrawLine(pixelpos0, yH, pixelpos0, yH+hH)
        dc.SetPen(self.penDarkShadow)
        dc.DrawLine(pixelpos0+wH, yH, pixelpos0+wH, yH+hH)
        dc.DrawLine(pixelpos0, yH+hH, pixelpos0+wH+1, yH+hH)
        dc.SetPen(self.penShadow)
        dc.DrawLine(pixelpos0+wH-1, yH+1, pixelpos0+wH-1, yH+hH)
        dc.DrawLine(pixelpos0+1, yH+hH-1, pixelpos0+wH, yH+hH-1)
        if self.selmode == 1:
            hH2 = hH/2
            border = 3
            yH2 = yB #yH + hH/4
            for bmtype in (1,2):
                if bmtype == 1:
                    xpos = pixelpos0 - self.wH
                    p1 = wx.Point(xpos+border, yH2+hH2-border)
                    p2 = wx.Point(xpos+self.wH-border, yH2+hH2-border)
                    p3 = wx.Point(xpos+self.wH-border, yH2+border)
                else:
                    xpos = pixelpos0 + self.wH #+ 1
                    p1 = wx.Point(xpos+border, yH2+border)
                    p2 = wx.Point(xpos+border, yH2+hH2-border)
                    p3 = wx.Point(xpos+self.wH-border, yH2+hH2-border)
                # Draw the button
                dc.SetPen(self.penHandle)
                dc.SetBrush(self.brushHandle)
                dc.DrawRectangle(xpos, yH2, self.wH, hH2)
                dc.SetPen(self.penHighlight2)
                dc.DrawLine(xpos, yH2, xpos+wH, yH2)
                dc.DrawLine(xpos, yH2, xpos, yH2+hH2)
                dc.SetPen(self.penDarkShadow)
                if bmtype == 2:
                    dc.DrawLine(xpos+wH, yH2, xpos+wH, yH2+hH2)
                    dc.DrawLine(xpos, yH2+hH2, xpos+wH+1, yH2+hH2)
                else:
                    dc.DrawLine(xpos, yH2+hH2, xpos+wH, yH2+hH2)
                dc.SetPen(self.penShadow)
                dc.DrawLine(xpos+wH-1, yH2+1, xpos+wH-1, yH2+hH2)
                dc.DrawLine(xpos+1, yH2+hH2-1, xpos+wH, yH2+hH2-1)
                # Draw the button image
                if boolEnabled:
                    dc.SetPen(wx.BLACK_PEN)
                    dc.SetBrush(wx.BLACK_BRUSH)
                else:
                    dc.SetPen(self.penGrayText)
                    dc.SetBrush(self.brushGrayText)
                dc.DrawPolygon((p1, p2, p3))


    def _createSelections(self):
        selectionList = []
        start = stop = None
        #~ selectionmarks = self.bookmarks
        selectionmarks = [item for item in self.bookmarks.items() if item[1] != 0]
        selectionmarks.sort()
        if len(selectionmarks) == 0:
            return None
        if selectionmarks[0][1] == 2:
            start =self.minValue
        for value, bmtype in selectionmarks:
            if start is None:
                if bmtype == 1:
                    start = value
            else:
                if bmtype == 2:
                    stop = value
                    selectionList.append((start, stop))
                    start = stop =None
        if start is not None:
            stop = self.maxValue
            selectionList.append((start, stop))
        return selectionList

    def _getRectHandle(self):
        x, y, w, h = self.GetRect()
        pixelpos = int(self.value * (w-2*self.xo) / float(self.maxValue - self.minValue))
        rectHandle = wx.Rect(pixelpos-self.wH/2+self.xo, self.yo-3, self.wH, h-self.yo-self.yo2+6)
        return rectHandle

    def GetValue(self):
        return self.value

    def GetMin(self):
        return self.minValue

    def GetMax(self):
        return self.maxValue

    def SetValue(self, value):
        self.value = max(min(value, self.maxValue), self.minValue)
        if self.IsDoubleBuffered():
            dc = wx.ClientDC(self)
        else:
            dc = wx.BufferedDC(wx.ClientDC(self))
        dc.Clear()
        self._PaintSlider(dc)
        return True

    def SetRange(self, minValue, maxValue, refresh=True):
        if minValue >= maxValue:
            if minValue == 0 and (maxValue == -1 or maxValue ==0):
                maxValue = 1
            else:
                print>>sys.stderr, _('Error: minValue must be less than maxValue')
                return
        self.minValue = minValue
        self.maxValue = maxValue
        self.selections = self._createSelections()
        if refresh:
            if self.IsDoubleBuffered():
                dc = wx.ClientDC(self)
            else:
                dc = wx.BufferedDC(wx.ClientDC(self))
            dc.Clear()
            self._PaintSlider(dc)
        return True

    def SetBookmark(self, value, bmtype=0, refresh=True):
        # Type=0: bookmark, Type=1: selection start, Type=2: selection end
        if bmtype not in (0,1,2):
            return False
        try:
            if self.bookmarks[value] == bmtype:
                return False
        except:
            pass
        self.bookmarks[value] = bmtype

        if refresh:
            if self.bookmarks:
                self.selections = self._createSelections()
            else:
                self.selections = None
            if self.IsDoubleBuffered():
                dc = wx.ClientDC(self)
            else:
                dc = wx.BufferedDC(wx.ClientDC(self))
            dc.Clear()
            self._PaintSlider(dc)
        return True

    def RemoveBookmark(self, value, bmtype=0, refresh=True):
        try:
            del self.bookmarks[value]
            if refresh:
                if self.bookmarks:
                    self.selections = self._createSelections()
                else:
                    self.selections = None
                if self.IsDoubleBuffered():
                    dc = wx.ClientDC(self)
                else:
                    dc = wx.BufferedDC(wx.ClientDC(self))
                dc.Clear()
                self._PaintSlider(dc)
            return True
        except KeyError:
            return False

    def RemoveAllBookmarks(self):
        if self.bookmarks:
            self.bookmarks.clear()
            self.selections = None
            if self.IsDoubleBuffered():
                dc = wx.ClientDC(self)
            else:
                dc = wx.BufferedDC(wx.ClientDC(self))
            dc.Clear()
            self._PaintSlider(dc)
        return True

    def GetBookmarks(self, copy=False):
        if not copy:
            return self.bookmarks
        else:
            return dict(self.bookmarks)

    def GetSelections(self):
        if self.selections:
            return self.selections[:]
        else:
            return self.selections

    def ToggleSelectionMode(self, mode=0):
        if self.selmode == 0 or mode == 1:
            self.selmode = 1
        else:
            self.selmode = 0
        if self.IsDoubleBuffered():
            dc = wx.ClientDC(self)
        else:
            dc = wx.BufferedDC(wx.ClientDC(self))
        dc.Clear()
        self._PaintSlider(dc)

    def HitTestHandle(self, mousepos):
        #~ x, y, w, h = self.GetRect()
        #~ pixelpos = int(self.value * (w-2*self.xo) / float(self.maxValue - self.minValue))
        #~ rectHandle = wx.Rect(pixelpos-self.wH/2+self.xo, self.yo-3, self.wH, h-self.yo-self.yo2+6)
        #~ return rectHandle.Inside(mousepos)
        rectHandle = self._getRectHandle()
        return rectHandle.Inside(mousepos)

    def HitTestBookmark(self, mousepos):
        x, y, w, h = self.GetRect()
        hitlist = []
        wT = self.wT
        for value, bmtype in self.bookmarks.items():
            pixelpos = int(value * (w-2*self.xo) / float(self.maxValue - self.minValue)) + self.xo
            if bmtype == 0:
                rect = wx.Rect(pixelpos-wT/4, h-self.yo2, wT/2, wT/2)
            elif bmtype == 1:
                rect = wx.Rect(pixelpos-wT/2, h-self.yo2, wT/2+wT/4, wT/2)
            elif bmtype == 2:
                rect = wx.Rect(pixelpos-wT/4, h-self.yo2, wT/2+wT/4, wT/2)
            if rect.Inside(mousepos):
                hitlist.append((value, pixelpos))
        if hitlist:
            if len(hitlist) == 1:
                return hitlist[0][0]
            else:
                return min([(abs(pixelpos-mousepos.x), value) for value, pixelpos in hitlist])[1]
        else:
            return None

    def HitTestSelectionButton(self, mousepos):
        if self.selmode == 1:
            x, y, w, h = self.GetRect()
            pixelpos = int(self.value * (w-2*self.xo) / float(self.maxValue - self.minValue))
            rectLeftButton = wx.Rect(pixelpos-self.wH/2+self.xo-self.wH, self.yo-3, self.wH, (h-self.yo-self.yo2+6)/1)
            rectRightButton = wx.Rect(pixelpos-self.wH/2+self.xo+self.wH, self.yo-3, self.wH, (h-self.yo-self.yo2+6)/1)
            bmtype = None
            if rectLeftButton.Inside(mousepos):
                bmtype = 1
            if rectRightButton.Inside(mousepos):
                bmtype = 2
            return bmtype

    def _HitTestHandleDeadZone(self, mousepos):
        rectHandle = self._getRectHandle()
        rectHandle.Inflate(3*self.wH, 0)
        return rectHandle.Inside(mousepos)

# Main program window
class MainFrame(wxp.Frame):
    # Initialization functions
    def __init__(self, parent=None, id=wx.ID_ANY, title=global_vars.name, pos=wx.DefaultPosition, size=(700, 550), style=wx.DEFAULT_FRAME_STYLE):
        wxp.Frame.__init__(self, parent, id, pos=pos, size=size, style=style)
        self.name = title
        self.version = global_vars.version
        self.firsttime = False
        self.x86_64 = sys.maxsize > 2**32
        # Define program directories
        if hasattr(sys,'frozen'):
            self.programdir = os.path.dirname(sys.executable)
        else:
            self.programdir = os.path.abspath(os.path.dirname(sys.argv[0]))
        if type(self.programdir) != unicode:
            self.programdir = unicode(self.programdir, encoding)
        self.initialworkdir = os.getcwdu()
        self.toolsfolder = os.path.join(self.programdir, 'tools')
        sys.path.insert(0, self.toolsfolder)
        self.macrofolder = os.path.join(self.programdir, 'macros')
        self.helpdir = os.path.join(self.programdir, 'help')
        # Get persistent options
        self.optionsfilename = os.path.join(self.programdir, 'options.dat')
        self.filterdbfilename = os.path.join(self.programdir, 'filterdb.dat')
        self.filterdbremote_plugins = r'https://raw.github.com/wiki/AvsPmod/AvsPmod/Plugin-functions.md'
        self.filterdbremote_scripts = r'https://raw.github.com/wiki/AvsPmod/AvsPmod/Script-functions.md'
        self.lastSessionFilename = os.path.join(self.programdir, '_last_session_.ses')
        self.macrosfilename = os.path.join(self.programdir, 'macros', 'macros.dat')
        self.loaderror = []
        self.getOptionsDict()
        self.SetPaths()        
        self.LoadAvisynth()
        self.IdleCall = []
        self.defineFilterInfo()
        if os.path.isfile(self.macrosfilename):
            try:
                with open(self.macrosfilename, 'rb') as f:
                    self.optionsMacros = cPickle.load(f)
            except:
                self.loaderror.append(os.path.basename(self.macrosfilename))
                shutil.copy2(self.macrosfilename, 
                             os.path.splitext(self.macrosfilename)[0] + '.BAD')
                self.optionsMacros = {}
        else:
            self.optionsMacros = {}
        
        # load translation file
        self.translations_dir = os.path.join(self.programdir, 'translations')
        if self.options['lang'] != 'eng':
            sys.path.insert(0, self.translations_dir)
            sys.dont_write_bytecode = True
            try:
                translation = __import__('translation_' + self.options['lang'])
            except ImportError:
                translation = None
            else:
                try:
                    global messages
                    messages = translation.messages
                    helpdir = '_'.join((self.helpdir, self.options['lang']))
                    if os.path.isdir(helpdir):
                        self.helpdir = helpdir
                except AttributeError:
                    pass
            finally:
                sys.dont_write_bytecode = False
        
        self.colour_data = wxp.ColourData() # needed before the following
        self.optionsDlgInfo = self.getOptionsDlgInfo()
        
        # single-instance socket
        self.port = 50009
        self.instance = wx.SingleInstanceChecker(title+wx.GetUserId())
        self.boolSingleInstance = self.options.setdefault('singleinstance', False)
        if self.boolSingleInstance:
            #~ self.port = 50009
            #~ self.instance = wx.SingleInstanceChecker(title+wx.GetUserId())
            if self.instance.IsAnotherRunning():
                # Send data to the main instance via socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', self.port))
                pickledstring = StringIO.StringIO()
                cPickle.dump(sys.argv[1:],pickledstring)
                sock.sendall(pickledstring.getvalue())
                response = sock.recv(8192)
                self.Destroy()
                return None
            else:
                def OnArgs(evt):
                    self.ProcessArguments(evt.data)
                self.Bind(wxp.EVT_POST_ARGS, OnArgs)
                # Start socket server (in a separate thread) to receive arguments from other instances
                self.argsPosterThread = wxp.ArgsPosterThread(self)
                self.argsPosterThread.Start()
        else:
            if self.instance.IsAnotherRunning():
                self.options['exitstatus'] = 0
        
        # Program size and position options
        self.separatevideowindow = self.options['separatevideowindow']
        dimensions = self.options.get('dimensions')
        if dimensions is not None and dimensions[0] > 0 and dimensions[1] > 0:
            self.SetDimensions(*dimensions)
            # Move the window if it's offscreen
            size = self.GetSize()
            pos = self.GetPosition()
            wC, hC = wx.ScreenDC().GetSize()
            # if (pos[0]+size[0]>wC) or (pos[1]+size[1]>hC):
            if (pos[0]+50>wC) or (pos[1]+50>hC):
                #~ self.Center()
                pass
        else:
            #~ self.Center()
            pass
        if self.options['alwaysontop']:
            style = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP
        else:
            style = wx.DEFAULT_FRAME_STYLE
        self.SetWindowStyle(style)
        
        # Drag-and-drop target for main window
        class MainFrameDropTarget(wx.PyDropTarget):
            def __init__(self, win):
                wx.PyDropTarget.__init__(self)
                self.win = win
                self.textdata = wx.TextDataObject()
                self.filedata = wx.FileDataObject()
                self.data = wx.DataObjectComposite()
                self.data.Add(self.textdata)
                self.data.Add(self.filedata)
                self.SetDataObject(self.data)

            def OnData(self, x, y, default):
                self.GetData()
                if self.textdata.GetTextLength() > 1:
                    text = self.textdata.GetText()
                    self.textdata.SetText('')
                    if text == self.win.currentScript.GetSelectedText():
                        self.win.NewTab()
                    else:
                        self.win.NewTab(text=text)
                else:
                    for filename in self.filedata.GetFilenames():
                        self.win.OpenFile(filename=filename)
                return False

        class ScriptDropTarget(wx.DropTarget):
            def __init__(self, win, app):
                wx.PyDropTarget.__init__(self)
                self.win = win
                self.app = app
                self.textdata = wx.TextDataObject()
                self.filedata = wx.FileDataObject()
                self.data = wx.DataObjectComposite()
                self.data.Add(self.textdata)
                self.data.Add(self.filedata)
                self.SetDataObject(self.data)
                self.oldPos = None

            def OnLeave(self):
                self.win.SetCaretWidth(1)

            def OnDragOver(self, x, y, default):
                point = wx.Point(x,y)
                textPos = self.win.PositionFromPoint(point)
                textPoint = self.win.PointFromPosition(textPos)
                if textPos != self.oldPos:
                    self.win.SetCaretWidth(0)
                    self.win.Refresh()
                dc = wx.ClientDC(self.win)
                dc.SetPen(wx.Pen('black', 1))
                dc.DrawLine(
                    textPoint.x,
                    textPoint.y,
                    textPoint.x,
                    textPoint.y + self.win.TextHeight(0)
                )
                self.oldPos = textPos
                return default#wx.DragMove

            def OnData(self, x, y, default):
                script = self.win
                script.SetCaretWidth(1)
                self.GetData()
                if self.textdata.GetTextLength() > 1:
                    # Get the clipboard data
                    text = self.textdata.GetText()
                    self.textdata.SetText('')
                    # Get the current selection positions
                    posA, posB = script.GetSelection()
                    # Go to the current mouse position
                    point = wx.Point(x,y)
                    textPos = script.PositionFromPoint(point)
                    script.GotoPos(textPos)
                    # Erase the old selection if required
                    if default == wx.DragMove:
                        script.SetTargetStart(posA)
                        script.SetTargetEnd(posB)
                        script.ReplaceTarget('')
                    # Insert the clipboard text in the current position
                    curPos = script.GetCurrentPos()
                    script.InsertText(curPos, text)
                    script.SetSelection(curPos, curPos+len(text))
                else:
                    # Go to the current mouse position
                    point = wx.Point(x,y)
                    textPos = script.PositionFromPoint(point)
                    script.GotoPos(textPos)
                    filenames = self.filedata.GetFilenames()
                    if len(filenames) == 1 and os.path.splitext(filenames[0])[1].lower() not in ('.avs', '.avsi', '.vpy', '.ses'):
                        # Insert the single filename as a source
                        self.app.InsertSource(filenames[0])
                    else:
                        # Open each filename as a script
                        for filename in self.filedata.GetFilenames():
                            self.app.OpenFile(filename=filename)
                return True

        self.SetDropTarget(MainFrameDropTarget(self))
        self.scriptDropTarget = ScriptDropTarget
        
        # Create all the program's controls and dialogs
        self.NewFileName = _('New File')
        self.scrapWindow = ScrapWindow(self)
        self.bookmarkDict = {}
        self.recentframes = []
        self.bmpVideo = None
        self.createWindowElements()
        if not __debug__:
            sys.stdout = self.scrapWindow
        if not self.separatevideowindow:
            cropdialogparent = self
        else:
            cropdialogparent = self.videoDialog
        self.cropDialog = self.createCropDialog(cropdialogparent)
        self.trimDialog = self.createTrimDialog(cropdialogparent)
        self.findDialog = wxp.QuickFindDialog(self.scriptNotebook)
        self.replaceDialog = wxp.FindReplaceDialog(self.scriptNotebook)
        
        # Internal class variables
        self.currentframenum = None
        self.zoomfactor = 1
        self.zoomwindow = False
        self.zoomwindowfit = False
        self.zoomwindowfill = False
        #~ self.currentScript = None
        self.lastcrop = ""
        self.oldWidth = 0
        self.oldHeight = 0
        self.oldFramecount = None
        self.oldPreviewtxt = None
        self.oldLastSplitVideoPos = None
        self.oldLastSplitSliderPos = None
        self.oldSliderWindowShown = None
        self.oldBoolSliders = None
        self.xo = self.yo = 5
        self.play_speed_factor = 1.0
        self.play_drop = True
        self.playing_video = False
        self.getPixelInfo = False
        self.sliderOpenString = '[<'
        self.sliderCloseString = '>]'
        self.fc = None
        self.regexp = re.compile(r'\%s.*?\%s' % (self.sliderOpenString, self.sliderCloseString))
        self.cropValues = {
            'left': 0,
            'top': 0,
            '-right': 0,
            '-bottom': 0,
        }
        self.oldCropValues = self.cropValues
        self.middleDownScript = False
        self.refreshAVI = True
        self.lastshownframe = None
        self.paintedframe = None
        self.oldlinenum = None
        self.dlgAvs2avi = None
        #~ self.tab_processed = False
        self.macroVars = {'last': None}
        self.imageFormats = {
            '.bmp': (_('Windows Bitmap') + ' (*.bmp)', wx.BITMAP_TYPE_BMP),
            '.gif': (_('Animation') + ' (*.gif)', wx.BITMAP_TYPE_GIF),
            '.jpg': (_('JPEG') + ' (*.jpg)', wx.BITMAP_TYPE_JPEG),
            '.pcx': (_('Zsoft Paintbrush') + ' (*.pcx)', wx.BITMAP_TYPE_PCX),
            '.png': (_('Portable Network Graphics') + ' (*.png)', wx.BITMAP_TYPE_PNG),
            '.pnm': (_('Netpbm') + ' (*.pnm)', wx.BITMAP_TYPE_PNM),
            '.tif': (_('Tagged Image File') + ' (*.tif)', wx.BITMAP_TYPE_TIF),
            '.xpm': (_('ASCII Text Array') + ' (*.xpm)', wx.BITMAP_TYPE_XPM),
            '.ico': (_('Windows Icon') + ' (*.ico)', wx.BITMAP_TYPE_ICO),
            '.cur': (_('Windows Cursor') + ' (*.cur)', wx.BITMAP_TYPE_CUR),
        }
        self.markFrameInOut = self.options['trimmarkframes']
        if self.options['trimreversechoice'] == 0:
            self.invertSelection = False
        else:
            self.invertSelection = True
        if self.options['videostatusbarinfo'] == None:
            sep = '\t\t' if os.name == 'nt' else '\\T\\T'
            self.videoStatusBarInfo = (_('Frame') + ' %F / %FC  -  (%T)  %BM      %POS  %HEX '
                                       '{sep} %Z %Wx%H (%AR)  -  %FR ' + _('fps') + '  -  %CS').format(sep=sep)
        else:
            self.videoStatusBarInfo = self.options['videostatusbarinfo']
        self.videoStatusBarInfoParsed, self.showVideoPixelInfo = self.ParseVideoStatusBarInfo(self.videoStatusBarInfo)
        self.foldAllSliders = True
        self.reuse_environment = False
        self.matrix = ['auto', 'tv']
        self.interlaced = self.swapuv = self.bit_depth = False
        self.flip = []
        self.titleEntry = None
        self.colour_data.FromString(self.options['colourdata'])
        # Events
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnNotebookPageChanging)
        #~ self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClickWindow)

        if not self.separatevideowindow:
            def OnSize(event):
                if self.zoomwindowfit and self.previewWindowVisible:
                    #~ self.IdleCall = (self.ShowVideoFrame, tuple(), {'forceRefresh': True, 'focus': False})
                    self.IdleCall.append((self.ShowVideoFrame, tuple(), {'focus': False}))
                if self.titleEntry:
                    self.scriptNotebook.SetFocus()
                event.Skip()
            self.Bind(wx.EVT_SIZE, OnSize)
        else:
            def OnSize(event):
                if self.zoomwindow and self.previewWindowVisible:
                    #~ self.IdleCall = (self.ShowVideoFrame, tuple(), {'forceRefresh': True, 'focus': False})
                    self.IdleCall.append((self.ShowVideoFrame, tuple(), {'focus': False}))
                event.Skip()
            self.videoDialog.Bind(wx.EVT_SIZE, OnSize)

        # Command line arguments
        self.UpdateRecentFilesList()
        self.reloadList = []
        self.lastClosed = None
        if self.options['exitstatus']:
            self.IdleCall.append((wx.MessageBox, (_('A crash detected at the last running!'), _('Warning'), wx.OK|wx.ICON_EXCLAMATION, self), {})) 
        use_last_preview_placement = True
        if ((self.options['exitstatus'] or self.options['startupsession'] and 
                (self.options['alwaysloadstartupsession'] or len(sys.argv) <= 1 or not self.options['promptexitsave']))
            and os.path.isfile(self.lastSessionFilename)):
                if self.LoadSession(self.lastSessionFilename, saverecentdir=False, resize=False, backup=True, startup=True):
                    use_last_preview_placement = False
                else:
                    self.loaderror.append(os.path.basename(self.lastSessionFilename))
                    shutil.copy2(self.lastSessionFilename, os.path.splitext(self.lastSessionFilename)[0] + '.BAD')
        if use_last_preview_placement and self.options['last_preview_placement'] != self.mainSplitter.GetSplitMode():
            self.TogglePreviewPlacement()
        if not self.options['exitstatus']:
            self.options['exitstatus'] = 1
            f = open(self.optionsfilename, mode='wb')
            cPickle.dump(self.options, f, protocol=0)
            f.close()
        if len(sys.argv)>1:
            self.ProcessArguments(sys.argv[1:])
        #~ if not self.currentScript.sliderWindowShown:
            #~ self.HideSliderWindow(self.currentScript)
        #~ else:
            #~ newSliderWindow.Show()
            #~ self.ShowSliderWindow(self.currentScript)
        
        if self.previewWindowVisible:
            #~ self.HidePreviewWindow()
            self.need_to_show_preview = True
        else:
            self.need_to_show_preview = False
        # Misc
        self.UpdateProgramTitle()
        self.SetIcon(AvsP_icon.getIcon())

        if self.separatevideowindow:
            def OnActivate(event):
                if event.GetActive():
                    self.currentScript.SetFocus()
                event.Skip()
            self.Bind(wx.EVT_ACTIVATE, OnActivate)


        def OnMove(event):
            self.currentScript.UpdateCalltip()
        self.Bind(wx.EVT_MOVE, OnMove)

        #~ self.firsttime = False
        self.doMaximize = False
        def _x_OnIdle(event):
            if self.doMaximize:
                if self.options.get('maximized'):
                    self.Maximize(True)
                if self.options.get('maximized2') and self.separatevideowindow:
                    self.videoDialog.Maximize(True)
                index = self.scriptNotebook.GetSelection()
                self.ReloadModifiedScripts()
                self.scriptNotebook.SetSelection(index)
                self.currentScript.SetFocus()
                self.doMaximize = False
            if not self.firsttime:
                if self.separatevideowindow:
                    self.Show()
                vidmenu = self.videoWindow.contextMenu
                menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Zoom'))).GetSubMenu()
                menuItem = menu.FindItemByPosition(self.options['zoomindex'])
                if menuItem is not None:
                    self.OnMenuVideoZoom(None, menuItem=menuItem, show=False)
                if self.need_to_show_preview:
                    self.ShowVideoFrame(self.startupframe, forceRefresh=False)
                self.Refresh()
                if self.mainSplitter.IsSplit():
                    self.SplitVideoWindow()
                    #~ self.SplitVideoWindow(forcefit=True)
                    #~ self.lastSplitVideoPos = None
                self.Show()
                self.firsttime = True
                self.doMaximize = True
        #~ self.IdleCall = None
        def OnIdle(event):
            if self.IdleCall:
                func, args, kwargs = self.IdleCall.pop()
                func(*args, **kwargs)
                #~ self.IdleCall = None
        self.Bind(wx.EVT_IDLE, OnIdle)
        
        # Print options
        self.print_data = wx.PageSetupDialogData()
        self.print_data.SetMarginTopLeft(wx.Point(15, 15))
        self.print_data.SetMarginBottomRight(wx.Point(15, 15))
        self.print_header = True
        self.print_wrap = True
        self.print_zoom = False
        
        # Other options
        self.mouse_wheel_rotation = 0
        
        # Display the program
        if self.separatevideowindow:
            self.Show()
        vidmenu = self.videoWindow.contextMenu
        menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Zoom'))).GetSubMenu()
        menuItem = menu.FindItemByPosition(self.options['zoomindex'])
        if menuItem is not None:
            self.OnMenuVideoZoom(None, menuItem=menuItem, show=False)
        if self.options['use_customvideobackground']:
            self.OnMenuVideoBackgroundColor(color=self.options['videobackground'])
        if self.need_to_show_preview:
            #~ self.ShowVideoFrame(self.startupframe, forceRefresh=False)
            self.IdleCall.append((self.ShowVideoFrame, (self.startupframe,), {'forceRefresh':False}))
        #~ self.Refresh()
        if self.mainSplitter.IsSplit():
            self.SplitVideoWindow()
        self.Show()
        if self.options.get('maximized'):
            self.Maximize(True)
        if self.options.get('maximized2') and self.separatevideowindow:
            self.videoDialog.Maximize(True)
        index = self.scriptNotebook.GetSelection()
        self.ReloadModifiedScripts()
        self.scriptNotebook.SetSelection(index)
        self.currentScript.SetFocus()
        
        # Warn if option files are damaged
        if self.loaderror:
            print>>sys.stderr, '{0}: {1}'.format(_('Error'), _('Damaged {0}. Using default settings.').format(', '.join(self.loaderror)))
        
        # Update the translation file if necessary
        for path, lang in self.getTranslations(return_paths=True):
            if not os.stat(path).st_size:
                i18n.UpdateTranslationFile(self.translations_dir, lang, self.version)
        if self.options['lang'] != 'eng':
            if translation:
                try:
                    try:
                        translation_version = translation.version
                    except AttributeError:
                        translation_version = None
                    if translation_version != self.version:
                        if i18n.UpdateTranslationFile(os.path.join(self.translations_dir), 
                                                      self.options['lang'], self.version):
                            wx.MessageBox(_('%s translation file updated with new messages to translate') 
                                            % i18n.display_name(self.options['lang']), _('Translation updated'))
                        else:
                            wx.MessageBox(_('%s translation file updated.  No new messages to translate.') 
                                            % i18n.display_name(self.options['lang']), _('Translation updated'))
                except NameError, err:
                    pass
            else:
                wx.MessageBox(_("%s language couldn't be loaded") % i18n.display_name(self.options['lang']), 
                              _('Error'), style=wx.OK|wx.ICON_ERROR)
                self.options['lang'] = 'eng'
        
        # Timer for saving the session periodically
        class BackupTimer(wx.Timer):
            def __init__(self, parent):
                wx.Timer.__init__(self)
                self.parent = parent
            def Notify(self):
                self.parent.SaveSession(self.parent.lastSessionFilename, saverecentdir=False, previewvisible=False)
        self.backupTimer = BackupTimer(self)
        if self.options['periodicbackup']:
            self.backupTimer.Start(self.options['periodicbackup'] * 60000)
    
    def ProcessArguments(self, args):
        if args:
            self.HidePreviewWindow()
            for arg in args:
                arg = arg.decode(sys.stdin.encoding or encoding)
                if os.path.isfile(arg):
                    if os.path.dirname(arg) == '':
                        arg = os.path.join(self.initialworkdir, arg)
                    self.OpenFile(filename=arg) # BUG: sys.argv gives back short filenames only?!!
                    self.currentScript.GotoPos(0)
                    self.currentScript.EnsureCaretVisible()

    def getOptionsDict(self):
        oldOptions = None
        if os.path.isfile(self.optionsfilename):
            try:
                with open(self.optionsfilename, mode='rb') as f:
                    oldOptions = cPickle.load(f)
            except:
                self.loaderror.append(os.path.basename(self.optionsfilename))
                shutil.copy2(self.optionsfilename, 
                             os.path.splitext(self.optionsfilename)[0] + '.BAD')
                oldOptions = {}
        if oldOptions and oldOptions.get('version').startswith('1.'):
            oldOptions = None
        
        if os.name == 'nt':
            templateDict = {
                'avi': 'AVISource(***)',
                'wav': 'WAVSource(***)',
                'd2v': 'MPEG2Source(***, cpu=0)',
                'dga': 'AVCSource(***)',
                'dgi': 'DGSource(***)',
                'mpg': 'DirectShowSource(***)',
                'mp4': 'DirectShowSource(***)',
                'mkv': 'DirectShowSource(***)',
                'wmv': 'DirectShowSource(***)',
                'avs': 'Import(***)',
                'bmp': 'ImageSource(***)',
                'jpg': 'ImageSource(***)',
                'png': 'ImageSource(***)',
            }
        else:
            templateDict = {
                'avi': 'FFVideoSource(***)',
                'wav': 'FFAudioSource(***)',
                'mpg': 'FFVideoSource(***)',
                'mp4': 'FFVideoSource(***)',
                'mkv': 'FFVideoSource(***)',
                'wmv': 'FFVideoSource(***)',
                'avs': 'Import(***)',
                'bmp': 'FFVideoSource(***, cache=false, seekmode=-1)',
                'jpg': 'FFVideoSource(***, cache=false, seekmode=-1)',
                'png': 'FFVideoSource(***, cache=false, seekmode=-1)',
            }
        snippetsDict = {
        }
        index = os.name == 'nt'
        sans = ('sans', 'Verdana')[index]
        sans2 = ('sans', 'Arial')[index]
        serif = ('serif', 'Georgia')[index]
        serif2 = ('serif', 'Times New Roman')[index]
        mono = ('monospace', 'Courier New')[index]
        mono2 = ('monospace', 'Fixedsys')[index]
        other = ('sans', 'Comic Sans MS')[index]
        rgb = tuple(map(lambda x: (x+255)/2, 
                       wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE).Get()))
        solarized_base03 = '#002b36'
        solarized_base02 = '#073642'
        solarized_base01 = '#586e75'
        solarized_base00 = '#657b83'
        solarized_base0 = '#839496'
        solarized_base1 = '#93a1a1'
        solarized_base2 = '#eee8d5'
        solarized_base3 = '#fdf6e3'
        solarized_yellow = '#b58900'
        solarized_orange = '#cb4b16'
        solarized_red = '#dc322f'
        solarized_magenta = '#d33682'
        solarized_violet = '#6c71c4'
        solarized_blue = '#268bd2'
        solarized_cyan = '#2aa198'
        solarized_green = '#859900'
        solarized_base021 = '#c1c5bb' # added
        solarized_base21 = '#2f525b' # added
        zenburn_normal_fore = '#dcdccc'
        zenburn_normal_back = '#3f3f3f'
        zenburn_low_fore = '#a0a094' # added
        zenburn_comment = '#7f9f7f'
        zenburn_string = '#cc9393'
        zenburn_stringeol_fore = '#ecbcbc'
        zenburn_stringeol_back = '#41363c'
        zenburn_number = '#8cd0d3'
        zenburn_operator = '#f0efd0'
        zenburn_clipproperty = '#9fafaf'
        zenburn_internalfunction = '#c0bed1'
        zenburn_internalfilter = '#6c6c9c'
        zenburn_externalfilter = '#bc6c9c'
        zenburn_userdefined = '#efef8f'
        zenburn_datatype = '#dfdfbf'
        zenburn_keyword = '#f0dfaf'
        zenburn_define = '#ffcfaf'
        zenburn_bad = '#e89393'
        zenburn_cursor_fore = '#000d18'
        zenburn_cursor_back = '#8faf9f'
        zenburn_select_back = '#2f2f2f'
        zenburn_linenumber_fore = '#9fafaf'
        zenburn_linenumber_back = '#262626'
        zenburn_currentline_back = '#434443'
        zenburn_fold_fore = '#93b3a3'
        zenburn_fold_back = '#333333'
        locals_dict = locals()
        self.defaulttextstylesDict = {
            _('Default'): {
                'monospaced': 'face:{mono},size:10',
                'default': 'face:{sans},size:10,fore:#000000,back:#FFFFFF',
                'comment': 'face:{serif},size:9,fore:#007F00,back:#FFFFFF',
                'blockcomment': 'face:{serif},size:9,fore:#007F00,back:#FFFFFF',
                'endcomment': 'face:{sans},size:10,fore:#C0C0C0,back:#FFFFFF',
                'number': 'face:{mono},size:10,fore:#007F7F,back:#FFFFFF',
                'badnumber': 'face:{mono},size:10,fore:#FF0000,back:#FFFFFF',
                'string': 'face:{mono},size:10,fore:#7F007F,back:#FFFFFF',
                'stringtriple': 'face:{mono},size:10,fore:#7F0000,back:#FFFFFF',
                'stringeol': 'face:{mono},size:10,fore:#000000,back:#E0C0E0',
                'operator': 'face:{sans},size:10,fore:#000000,back:#FFFFFF,bold',
                'assignment': 'face:{sans},size:10,fore:#000000,back:#FFFFFF,bold',
                'clipproperty': 'face:{sans},size:10,fore:#00007F,back:#FFFFFF,bold',
                'internalfunction': 'face:{sans},size:10,fore:#007F7F,back:#FFFFFF,bold',
                'internalfilter': 'face:{sans},size:10,fore:#00007F,back:#FFFFFF,bold',
                'externalfilter': 'face:{sans},size:10,fore:#0080C0,back:#FFFFFF,bold',
                'userdefined': 'face:{sans},size:10,fore:#8000FF,back:#FFFFFF,bold',
                'unknownfunction': 'face:{sans},size:10,fore:#E10000,back:#FFFFFF,bold',
                'parameter': 'face:{sans},size:10,fore:#555555,back:#FFFFFF',
                'datatype': 'face:{sans},size:10,fore:#0000FF,back:#FFFFFF',
                'calltip': 'fore:#808080,back:#FFFFFF',
                'calltiphighlight': 'fore:#000000',
                'keyword': 'face:{sans},size:10,fore:#400080,back:#FFFFFF,bold',
                'miscword': 'face:{sans},size:10,fore:#00007F,back:#FFFFFF,bold',
                'userslider': 'face:{sans},size:10,fore:#00007F,back:#FFFFFF',
                'cursor': 'fore:#000000',
                'bracelight': 'face:{sans},size:10,fore:#0000FF,back:#FFFFFF,bold',
                'badbrace': 'face:{sans},size:10,fore:#FF0000,back:#FFFFFF,bold',
                'highlight': 'fore:#000000,back:#C0C0C0',                
                'highlightline': 'back:#E8E8FF',
                'linenumber': 'face:{mono},fore:#555555,back:#C0C0C0',
                'foldmargin': 'fore:#555555,back:#%02X%02X%02X' % rgb,
                'scrapwindow': 'face:{mono},size:10,fore:#0000AA,back:#F5EF90',
            },
            # Based, with some minor changes, on Solarized <http://ethanschoonover.com/solarized>
            _('Solarized light'): {
                'monospaced': 'face:{mono},size:10',
                'default': 'face:{sans},size:10,fore:{solarized_base00},back:{solarized_base3}',
                'comment': 'face:{serif},size:9,fore:{solarized_base1},back:{solarized_base3}',
                'blockcomment': 'face:{serif},size:9,fore:{solarized_base1},back:{solarized_base3}',
                'endcomment': 'face:{sans},size:10,fore:{solarized_base1},back:{solarized_base3}',
                'number': 'face:{mono},size:10,fore:{solarized_cyan},back:{solarized_base3}',
                'badnumber': 'face:{mono},size:10,fore:{solarized_red},back:{solarized_base3}',
                'string': 'face:{mono},size:10,fore:{solarized_cyan},back:{solarized_base3}',
                'stringtriple': 'face:{mono},size:10,fore:{solarized_cyan},back:{solarized_base3}',
                'stringeol': 'face:{mono},size:10,fore:{solarized_cyan},back:{solarized_base2}',
                'operator': 'face:{sans},size:10,fore:{solarized_base00},back:{solarized_base3},bold',
                'assignment': 'face:{sans},size:10,fore:{solarized_base00},back:{solarized_base3},bold',
                'clipproperty': 'face:{sans},size:10,fore:{solarized_blue},back:{solarized_base3},bold',
                'internalfunction': 'face:{sans},size:10,fore:{solarized_blue},back:{solarized_base3},bold',
                'internalfilter': 'face:{sans},size:10,fore:{solarized_violet},back:{solarized_base3},bold',
                'externalfilter': 'face:{sans},size:10,fore:{solarized_magenta},back:{solarized_base3},bold',
                'userdefined': 'face:{sans},size:10,fore:{solarized_yellow},back:{solarized_base3},bold',
                'unknownfunction': 'face:{sans},size:10,fore:{solarized_red},back:{solarized_base3},bold',
                'parameter': 'face:{sans},size:10,fore:{solarized_base1},back:{solarized_base3}',
                'datatype': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base3}',
                'calltip': 'fore:{solarized_base00},back:{solarized_base2}',
                'calltiphighlight': 'fore:{solarized_base21}',
                'keyword': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base3},bold',
                'miscword': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base3},bold',
                'userslider': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base3}',
                'cursor': 'fore:{solarized_base21}',
                'bracelight': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base3},bold',
                'badbrace': 'face:{sans},size:10,fore:{solarized_red},back:{solarized_base3},bold',
                'highlight': 'fore:{solarized_base21},back:{solarized_base021}',             
                'highlightline': 'back:{solarized_base2}',
                'linenumber': 'face:{mono},fore:{solarized_base1},back:{solarized_base2}',
                'foldmargin': 'fore:{solarized_base1},back:{solarized_base2}',
                'scrapwindow': 'face:{mono},size:10,fore:{solarized_base01},back:{solarized_base2}',
            },
            _('Solarized dark'): {
                'monospaced': 'face:{mono},size:10',
                'default': 'face:{sans},size:10,fore:{solarized_base0},back:{solarized_base03}',
                'comment': 'face:{serif},size:9,fore:{solarized_base01},back:{solarized_base03}',
                'blockcomment': 'face:{serif},size:9,fore:{solarized_base01},back:{solarized_base03}',
                'endcomment': 'face:{sans},size:10,fore:{solarized_base01},back:{solarized_base03}',
                'number': 'face:{mono},size:10,fore:{solarized_cyan},back:{solarized_base03}',
                'badnumber': 'face:{mono},size:10,fore:{solarized_red},back:{solarized_base03}',
                'string': 'face:{mono},size:10,fore:{solarized_cyan},back:{solarized_base03}',
                'stringtriple': 'face:{mono},size:10,fore:{solarized_cyan},back:{solarized_base03}',
                'stringeol': 'face:{mono},size:10,fore:{solarized_cyan},back:{solarized_base02}',
                'operator': 'face:{sans},size:10,fore:{solarized_base0},back:{solarized_base03},bold',
                'assignment': 'face:{sans},size:10,fore:{solarized_base0},back:{solarized_base03},bold',
                'clipproperty': 'face:{sans},size:10,fore:{solarized_blue},back:{solarized_base03},bold',
                'internalfunction': 'face:{sans},size:10,fore:{solarized_blue},back:{solarized_base03},bold',
                'internalfilter': 'face:{sans},size:10,fore:{solarized_violet},back:{solarized_base03},bold',
                'externalfilter': 'face:{sans},size:10,fore:{solarized_magenta},back:{solarized_base03},bold',
                'userdefined': 'face:{sans},size:10,fore:{solarized_yellow},back:{solarized_base03},bold',
                'unknownfunction': 'face:{sans},size:10,fore:{solarized_red},back:{solarized_base03},bold',
                'parameter': 'face:{sans},size:10,fore:{solarized_base01},back:{solarized_base03}',
                'datatype': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base03}',
                'calltip': 'fore:{solarized_base0},back:{solarized_base02}',
                'calltiphighlight': 'fore:{solarized_base021}',
                'keyword': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base03},bold',
                'miscword': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base03},bold',
                'userslider': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base03}',
                'cursor': 'fore:{solarized_base021}',
                'bracelight': 'face:{sans},size:10,fore:{solarized_green},back:{solarized_base03},bold',
                'badbrace': 'face:{sans},size:10,fore:{solarized_red},back:{solarized_base03},bold',
                'highlight': 'fore:{solarized_base021},back:{solarized_base21}',             
                'highlightline': 'back:{solarized_base02}',
                'linenumber': 'face:{mono},fore:{solarized_base01},back:{solarized_base02}',
                'foldmargin': 'fore:{solarized_base01},back:{solarized_base02}',
                'scrapwindow': 'face:{mono},size:10,fore:{solarized_base1},back:{solarized_base02}',
            },
            # Based on Zenburn <http://slinky.imukuppi.org/zenburnpage/>
            _('Zenburn'): {
                'monospaced': 'face:{mono},size:10',
                'default': 'face:{sans},size:10,fore:{zenburn_normal_fore},back:{zenburn_normal_back}',
                'comment': 'face:{serif},size:9,fore:{zenburn_comment},back:{zenburn_normal_back},italic',
                'blockcomment': 'face:{serif},size:9,fore:{zenburn_comment},back:{zenburn_normal_back},italic',
                'endcomment': 'face:{sans},size:10,fore:{zenburn_comment},back:{zenburn_normal_back}',
                'number': 'face:{mono},size:10,fore:{zenburn_number},back:{zenburn_normal_back}',
                'badnumber': 'face:{mono},size:10,fore:{zenburn_bad},back:{zenburn_normal_back}',
                'string': 'face:{mono},size:10,fore:{zenburn_string},back:{zenburn_normal_back}',
                'stringtriple': 'face:{mono},size:10,fore:{zenburn_string},back:{zenburn_normal_back}',
                'stringeol': 'face:{mono},size:10,fore:{zenburn_stringeol_fore},back:{zenburn_stringeol_back}',
                'operator': 'face:{sans},size:10,fore:{zenburn_operator},back:{zenburn_normal_back},bold',
                'assignment': 'face:{sans},size:10,fore:{zenburn_normal_fore},back:{zenburn_normal_back},bold',
                'clipproperty': 'face:{sans},size:10,fore:{zenburn_clipproperty},back:{zenburn_normal_back},bold',
                'internalfunction': 'face:{sans},size:10,fore:{zenburn_internalfunction},back:{zenburn_normal_back},bold',
                'internalfilter': 'face:{sans},size:10,fore:{zenburn_internalfilter},back:{zenburn_normal_back},bold',
                'externalfilter': 'face:{sans},size:10,fore:{zenburn_externalfilter},back:{zenburn_normal_back},bold',
                'userdefined': 'face:{sans},size:10,fore:{zenburn_userdefined},back:{zenburn_normal_back},bold',
                'unknownfunction': 'face:{sans},size:10,fore:{zenburn_bad},back:{zenburn_normal_back},bold',
                'parameter': 'face:{sans},size:10,fore:{zenburn_low_fore},back:{zenburn_normal_back}',
                'datatype': 'face:{sans},size:10,fore:{zenburn_datatype},back:{zenburn_normal_back}',
                'calltip': 'fore:{zenburn_low_fore},back:{zenburn_currentline_back}',
                'calltiphighlight': 'fore:{zenburn_normal_fore}',
                'keyword': 'face:{sans},size:10,fore:{zenburn_keyword},back:{zenburn_normal_back},bold',
                'miscword': 'face:{sans},size:10,fore:{zenburn_keyword},back:{zenburn_normal_back},bold',
                'userslider': 'face:{sans},size:10,fore:{zenburn_define},back:{zenburn_normal_back}',
                'cursor': 'fore:{zenburn_cursor_back}',
                'bracelight': 'face:{sans},size:10,fore:{zenburn_fold_fore},back:{zenburn_normal_back},bold',
                'badbrace': 'face:{sans},size:10,fore:{zenburn_bad},back:{zenburn_normal_back},bold',
                'highlight': 'fore:{zenburn_normal_fore},back:{zenburn_select_back}',             
                'highlightline': 'back:{zenburn_currentline_back}',
                'linenumber': 'face:{mono},fore:{zenburn_linenumber_fore},back:{zenburn_linenumber_back}',
                'foldmargin': 'fore:{zenburn_fold_fore},back:{zenburn_fold_back}',
                'scrapwindow': 'face:{mono},size:10,fore:{zenburn_normal_fore},back:{zenburn_currentline_back}',
            },
        }
        for values in self.defaulttextstylesDict.itervalues():
            for key, value in values.items():
                values[key] = value.format(**locals_dict)
        textstylesDict = self.defaulttextstylesDict[_('Default')].copy()
        # Create the options dict
        self.options = global_vars.options
        self.options.update({
            # INTERNAL OPTIONS
            'templates': templateDict,
            'snippets': snippetsDict,
            'textstyles': textstylesDict,
            'theme_set_only_colors': True,
            #~ 'avskeywords': avsKeywords,
            #~ 'avsoperators': avsOperators,
            #~ 'avsdatatypes': avsDatatypes,
            #~ 'avsmiscwords': [],
            'filteroverrides': {},
            'filterpresets': {},
            'filterdefaults_presets': {},
            'filterremoved': set(),
            'shortcuts': [],
            'recentdir': '',
            'userecentdir': True,
            'recentdirPlugins': '',
            'recentdirSession': '',
            'recentfiles': None,
            'lastscriptid': None,
            #~ 'lasthelpdir': None,
            'scraptext': ('', 0, 0),
            'maximized': False,
            'maximized2': False,
            'dimensions': (50, 50, 700, 550),
            'find_recent': [],
            'replace_recent': [],
            'cropchoice': 0,
            'autocrop_samples': 10,
            'triminsertchoice': 0,
            'trimreversechoice': 0,
            'trimmarkframes': True,
            'imagechoice': 0,
            'jpegquality': 70,
            'askjpegquality': True,
            'imagenamedefaultformat': '%s%06d',
            'imagenameformat': '%s%06d',
            'imagesavedir': '',
            'useimagesavedir': True,
            'colourdata': '1',
            'zoomindex': 2,
            'exitstatus': 0,
            'reservedshortcuts': ['Escape', 'Tab', 'Shift+Tab', 'Ctrl+Z', 'Ctrl+Y', 'Ctrl+X', 'Ctrl+C', 'Ctrl+V', 'Ctrl+A'],
            # GENERAL OPTIONS
            'altdir': os.path.join('%programdir%', 'tools'),
            'usealtdir': False,
            'pluginsdir': '',
            'avisynthhelpfile': '',
            'workdir': os.path.join('%programdir%', 'tools'),
            'useworkdir': False,
            'alwaysworkdir': False,
            'externalplayer': '',
            'externalplayerargs': '',
            'docsearchpaths': ';'.join(['%pluginsdir%', 
                    os.path.join('%avisynthdir%' if os.name == 'nt' 
                        else '/usr/local/share', 'docs', 'english', 'corefilters'), 
                    os.path.join('%avisynthdir%' if os.name == 'nt' 
                        else '/usr/local/share', 'docs', 'english', 'externalfilters')]),
            'docsearchurl':'http://www.google.com/search?q=%filtername%+Avisynth',
            # TEXT OPTIONS
            'calltips': True,
            'frequentcalltips': False,
            'syntaxhighlight_preferfunctions': False,
            'syntaxhighlight_styleinsidetriplequotes': False,
            'usestringeol': True,
            'autocomplete': True,
            'autocompletelength': 1,
            'autocompletepluginnames': {},
            'autoparentheses': 1,
            'presetactivatekey': 'return',
            'wrap': False,
            'highlight_fore': False,
            'highlightline': True,
            'usetabs': False,
            'tabwidth': 4,
            'numlinechars': 1,
            'foldflag': 1,
            'autocompletesingle': True,
            'autocompletevariables': True,
            'autocompleteicons': True,
            'calltipsoverautocomplete': False,
            'fdb_plugins': True,
            'fdb_userscriptfunctions': True,
            'autoloadedplugins': True,
            'autoloadedavsi': True,
            # VIDEO OPTIONS
            'dragupdate': True,
            'focusonrefresh': True,
            'previewunsavedchanges': True,
            'hidepreview': False,
            'refreshpreview': True,
            'promptwhenpreview': False,
            'last_preview_placement': wx.SPLIT_HORIZONTAL,
            'separatevideowindow': False,
            'previewontopofmain': True,
            #~ 'showvideopixelinfo': True,
            #~ 'pixelcolorformat': 'hex',
            'videostatusbarinfo': None,
            'use_customvideobackground': False,
            'videobackground': (0, 0, 0),
            'customvideobackground': (0, 0, 0),
            'errormessagefont': ('Arial', 24, '', '', (0, 0, 0)),
            'cropminx': 16,
            'cropminy': 16,
            #~ 'zoomresizescript': 'BicubicResize(width-width%8, height-height%8, b=1/3, c=1/3)',
            'customjump': 10,
            'customjumpunits': 'sec',
            'enabletabscrolling': False,
            'enabletabscrolling_groups': True,
            'enableframepertab': True,
            'enableframepertab_same': True,
            'applygroupoffsets': True,
            'offsetbookmarks': False,
            # AUTOSLIDER OPTIONS
            'keepsliderwindowhidden': False,
            'autoslideron': True,
            'autosliderstartfold': 0, #1,
            'autoslidermakeintfloat': True,
            'autoslidermakeintlist': True,
            'autoslidermakecolor': True,
            'autoslidermakebool': True,
            'autoslidermakestringlist': True,
            'autoslidermakestringfilename': True,
            'autoslidermakeunknown': True,
            'autosliderexclusions': '',
            # MISC OPTIONS
            'lang': 'eng',
            'largeui': False, 
            'startupsession': True,
            'alwaysloadstartupsession': False,
            'closeneversaved': False,
            'promptexitsave': True,
            'savemarkedavs': True,
            'eol': 'auto',
            'loadstartupbookmarks': True,
            'nrecentfiles': 5,
            'allowresize': True,
            'mintextlines': 2,
            'usetabimages': True,
            'multilinetab': False,
            'fixedwidthtab': False,
            'invertscrolling': False,
            'dllnamewarning': True,
            # TOGGLE OPTIONS
            'alwaysontop': False,
            'previewalwaysontop': False,
            'singleinstance': False,
            'usemonospacedfont': False,
            'disablepreview': False,
            'paranoiamode': False,
            'periodicbackup': 0,
            'autoupdatevideo': False,
        })
        # Import certain options from older version if necessary
        if oldOptions is not None:
            # Update the new options dictionnary with the old options
            updateInfo = [(k,v) for k,v in oldOptions.items() if k in self.options]
            self.options.update(updateInfo)
            #~ for key in self.options.keys():
                #~ if key in oldOptions:
                    #~ self.options[key] = optionsDict[key]
            # Update the new options sub-dictionnaries with the old options
            for key, d1 in (('templates', templateDict), ('textstyles', textstylesDict)):
                d2 = oldOptions.get(key)
                if d2 is not None:
                    d1.update(d2)
                self.options[key] = d1
            #~ for key, value in templateDict.items():
                #~ self.options['templates'].setdefault(key, value)
            #~ for key, value in textStyles.items():
                #~ if not self.optionsTextStyles.has_key(key):
                    #~ self.optionsTextStyles[key] = value
        self.options['version'] = self.version
        
        # Fix recentfiles as necessary???
        try:
            for i, s in enumerate(self.options['recentfiles']):
                if type(s) != unicode:
                    self.options['recentfiles'][i] = unicode(s, encoding)
        except TypeError:
            pass
                
        # check new key to make options.dat compatible for all 2.x version
        if len(self.options['textstyles']['highlight'].split(':')) == 2:
            self.options['textstyles']['highlight'] += ',fore:#000000'
        if len(self.options['textstyles']['foldmargin'].split(':')) == 2:
            self.options['textstyles']['foldmargin'] += ',fore:#555555'
        self.options['cropminx'] = self.options['cropminy'] = 1
        self.options['loadstartupbookmarks'] = True
        if oldOptions and 'autocompleteexclusions' in oldOptions:
            for name in oldOptions['autocompleteexclusions']:
                self.options['filterremoved'].add(name.lower())
        if oldOptions and 'parseavsi' in oldOptions:
            self.options['autoloadedavsi'] = oldOptions['parseavsi']
    
    def SetPaths(self):
        '''Set configurable paths'''
        self.avisynthdir = ''
        altdir_exp = self.ExpandVars(self.options['altdir'])
        if os.name == 'nt':
            try:
                # Get the avisynth directory from the registry
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\AviSynth')
                value = os.path.expandvars(_winreg.EnumValue(key, 0)[1])
                if os.path.isdir(value):
                    self.defaultavisynthdir = value
                else:
                    raise WindowsError
                key.Close()
            except WindowsError:
                self.defaultavisynthdir = ''
            if self.options['usealtdir'] and os.path.isdir(altdir_exp):
                self.avisynthdir = self.options['altdir']
                global_vars.avisynth_library_dir = altdir_exp
            else:
                self.options['usealtdir'] = False
                if os.path.isdir(self.defaultavisynthdir):
                    self.avisynthdir = self.ExpandVars(self.defaultavisynthdir, False, '%avisynthdir%')
            avisynthdir_exp = self.ExpandVars(self.avisynthdir)
            if (not os.path.isfile(self.ExpandVars(self.options['avisynthhelpfile'])) and 
                os.path.isfile(os.path.join(avisynthdir_exp, 'docs', 'english', 'index.htm'))):
                    self.options['avisynthhelpfile'] = os.path.join('%avisynthdir%', 'docs', 'english', 'index.htm')
            self.defaultpluginsdir = self.ExpandVars(
                    os.path.join('%avisynthdir%', 'plugins64' if self.x86_64 else 'plugins'))
            try:
                # Get the plugins directory from the registry (current user, only AviSynth 2.6)
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Software\\AviSynth')
                value = os.path.expandvars(_winreg.QueryValueEx(key, 'plugindir2_5')[0])
                if os.path.isdir(value):
                    self.options['pluginsdir'] = self.ExpandVars(value, False, '%pluginsdir%')
                else:
                    raise WindowsError
                key.Close()
            except WindowsError:
                try:
                    # Get the plugins directory from the registry (local machine, AviSynth 2.5-2.6)
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\AviSynth')
                    value = os.path.expandvars(_winreg.QueryValueEx(key, 'plugindir2_5')[0])
                    if os.path.isdir(value):
                        self.options['pluginsdir'] = self.ExpandVars(value, False, '%pluginsdir%')
                    else:
                        raise WindowsError
                    key.Close()
                except WindowsError:
                    if os.path.isdir(self.defaultpluginsdir):
                        self.options['pluginsdir'] = self.defaultpluginsdir
        else:
            if self.options['usealtdir'] and os.path.isdir(altdir_exp):
                self.avisynthdir = self.options['altdir']
                global_vars.avisynth_library_dir = altdir_exp
            else:
                self.options['usealtdir'] = False
                self.avisynthdir = '/usr/local/lib'
            if not os.path.isfile(self.ExpandVars(self.options['avisynthhelpfile'])):
                helpfile = '/usr/local/share/doc/english/index.htm'
                if os.path.isfile(helpfile):
                    self.options['avisynthhelpfile'] = helpfile
            self.defaultpluginsdir = self.ExpandVars(os.path.join('%avisynthdir%', 'avxsynth'))
            pluginsdir_exp = self.ExpandVars(self.options['pluginsdir'])
            if os.path.isdir(pluginsdir_exp):
                os.environ['AVXSYNTH_RUNTIME_PLUGIN_PATH'] = pluginsdir_exp
            else:
                pluginsdir = os.environ.get('AVXSYNTH_RUNTIME_PLUGIN_PATH', '')
                if os.path.isdir(pluginsdir):
                    self.options['pluginsdir'] = self.ExpandVars(pluginsdir, False, '%pluginsdir%')
                elif os.path.isdir(self.defaultpluginsdir):
                    self.options['pluginsdir'] = self.defaultpluginsdir
        if self.options['useworkdir']:
            workdir = self.ExpandVars(self.options['workdir'])
            if os.path.isdir(workdir):
                os.chdir(workdir)
    
    def LoadAvisynth(self):
        '''Load avisynth.dll/avxsynth.so'''    
        global avisynth
        exception = path_used = altdir_used = False
        while True:
            try:
                if self.x86_64:
                    import avisynth_cffi as avisynth
                else:
                    import avisynth
                break
            except OSError, err:
                if __debug__:
                    print err
                exception = True
                if self.options['usealtdir']:
                    if not path_used:
                        global_vars.avisynth_library_dir = ''
                        path_used = True
                        continue
                elif self.options['altdir'] and not altdir_used:
                    global_vars.avisynth_library_dir = self.ExpandVars(self.options['altdir'])
                    altdir_used = True
                    continue
                lib = ('AviSynth', 'avisynth.dll') if os.name == 'nt' else ('AvxSynth', 'libavxsynth.so')
                message = (_('{0}\n\nLoading {1} failed! Make sure that {2} is installed.'
                           '\n\n' + _('Alternatively, specify now its directory.')).format(
                          err, lib[1], lib[0]))
                ret = wx.MessageBox(message, ' '.join((self.name, self.version)), wx.YES_NO|wx.ICON_ERROR)
                if ret == wx.YES:
                        # Get the shared library directory from the user with a dialog box
                        dlg = wx.DirDialog(self, _('Select the {0} directory').format(lib[1]),
                                           os.path.expanduser('~'))
                        ID = dlg.ShowModal()
                        if ID==wx.ID_OK:
                            global_vars.avisynth_library_dir = dlg.GetPath()
                            dlg.Destroy()
                        else:
                            dlg.Destroy()
                            sys.exit(0)
                else:
                    sys.exit(0)
        if exception:
            if global_vars.avisynth_library_dir:
                self.options['usealtdir'] = True
                self.options['altdir'] = self.ExpandVars(
                        global_vars.avisynth_library_dir, False, 'avisynthdir')
            else:
                self.options['usealtdir'] = False
            self.SetPaths() # some paths may depend on %avisynthdir%
        try:
            global pyavs
            import pyavs
        except AttributeError:
            import pyavs_avifile as pyavs #  VFW, not longer supported
        pyavs.InitRoutines()
    
    def defineFilterInfo(self):
        self.plugin_shortnames = collections.defaultdict(list)
        self.optionsFilters = self.getFilterInfoFromAvisynth()
        
        if not self.avisynth_p: # parse avsi files for user script functions
            
            parse_avsi = self.options['autoloadedavsi']
            pluginsdir = self.ExpandVars(self.options['pluginsdir'])
            
            def escape_fnmatch(path):
                """Taken from http://bugs.python.org/issue8402"""
                pattern_chrs = re.compile('([*?[])')
                drive, path = os.path.splitdrive(path)
                path = pattern_chrs.sub(r'[\1]', path)
                return drive + path
            
            filenames = glob.iglob(os.path.join(escape_fnmatch(pluginsdir), '*.avsi'))
            filterInfo = []
            for filename in filenames:
                try:
                    info = self.ParseAvisynthScript(filename, quiet=True)
                except:
                    info = None
                if info:
                    filterInfo += info
            for filename, filtername, filterargs, ftype in filterInfo:
                filtername_lower = filtername.lower()
                if parse_avsi:
                    self.optionsFilters[filtername_lower] = (filtername, filterargs, ftype)
                self.installed_avsi_filternames.add(filtername_lower)
        
        if __debug__:
            self.ExportFilterData(self.optionsFilters, os.path.join(self.programdir, 'tempfilterout.txt'), True)
        
        self.avskeywords = [
            'return', 'global', 'function', 'last',
            'true', 'false', 'try', 'catch',
        ]
        self.avsdatatypes = [
            'clip', 'int', 'float', 'string', 'bool', 'var',
        ]
        self.avsoperators = [
            '-', '*', ',', '.', '/', ':', '?', '\\', '+', '<', '>', '=',
            '(', ')', '[', ']', '{', '}', '!', '%', '&', '|',
        ]
        self.avsmiscwords = ['__end__']
        if os.path.isfile(self.filterdbfilename):
            try:
                with open(self.filterdbfilename, mode='r') as f:
                    text = '\n'.join([line.strip() for line in f.readlines()])
                for section in text.split('\n\n['): # TODO: merge AvsFunctionDialog.ParseCustomizations and this
                    title, data = section.split(']\n',1)
                    title = title.strip('[]').lower()
                    if title == 'keywords':
                        self.avskeywords = data.split()
                    elif title == 'datatypes':
                        self.avsdatatypes = data.split()
                    elif title == 'operators':
                        self.avsoperators = data.split()
                    elif title == 'clipproperties':
                        for item in data.split('\n'):
                            if not item.strip():
                                continue
                            splitstring = item.split('(', 1)
                            if len(splitstring) == 2:
                                filtername = splitstring[0].strip()
                                filterargs = '('+splitstring[1].strip(' ')
                            else:
                                filtername = item
                                filterargs = ''
                            self.optionsFilters[filtername.lower()] = (filtername, filterargs, 1)
                    elif title == 'scriptfunctions':
                        for item in data.split('\n'):
                            if not item.strip():
                                continue
                            splitstring = item.split('(', 1)
                            if len(splitstring) == 2:
                                filtername = splitstring[0].strip()
                                filterargs = '('+splitstring[1].strip(' ')
                            else:
                                filtername = item
                                filterargs = ''
                            self.optionsFilters[filtername.lower()] = (filtername, filterargs, 4)
                    elif title == 'corefilters':
                        for s in data.split('\n\n'):
                            splitstring = s.split('(', 1)
                            if len(splitstring) == 2:
                                filtername = splitstring[0].strip()
                                filterargs = '('+splitstring[1].strip(' ')
                                self.optionsFilters[filtername.lower()] = (filtername, filterargs, 0)
                    elif title == 'plugins':
                        if not self.options['fdb_plugins']:
                            continue
                        for s in data.split('\n\n'):
                            splitstring = s.split('(', 1)
                            if len(splitstring) == 2:
                                filtername = splitstring[0].strip()
                                filterargs = '('+splitstring[1].strip(' ')
                                #~ if filtername.lower() in self.optionsFilters:
                                    #~ self.optionsFilters[filtername.lower()] = (filtername, filterargs, 2)
                                key = filtername.lower()
                                #~ splitname = filtername.split('_', 1)
                                #~ if len(splitname) == 2:
                                    #~ filtername = splitname[1]
                                    #~ self.optionsFilters[filtername.lower()] = (filtername, filterargs, 2)
                                short_name = self.GetPluginFunctionShortName(key)
                                if short_name:
                                    self.optionsFilters[key] = (filtername, filterargs, 2)
                                    self.plugin_shortnames[short_name].append(key)
                                else:
                                    print>>sys.stderr, '{0}: {1}'.format(_('Error'), _('Invalid plugin '
                                        'function name "{name}". Must be "pluginname_functionname".').format(name=key))
                    elif title == 'userfunctions':
                        if not self.options['fdb_userscriptfunctions']:
                            continue
                        for s in data.split('\n\n'):
                            splitstring = s.split('(', 1)
                            if len(splitstring) == 2:
                                filtername = splitstring[0].strip()
                                filterargs = '('+splitstring[1].strip(' ')
                                self.optionsFilters[filtername.lower()] = (filtername, filterargs, 3)
            except:
                self.loaderror.append(os.path.basename(self.filterdbfilename))
                bad0 = os.path.splitext(self.filterdbfilename)[0]
                bad, i = bad0 + '.BAD', 1
                while os.path.isfile(bad):
                    bad = bad0 + str(i) + '.BAD'
                    i += 1
                os.rename(self.filterdbfilename, bad)
        # Clean up override dict
        deleteKeys = []
        #~ for key, value in self.options['filteroverrides'].items():
            #~ if key.count('_') == 0:
                #~ tempList = [(k.split('_', 1), v[0]) for k, v in self.optionsFilters.items()]
                #~ for longKey, v in tempList[:]:
                    #~ if len(longKey) != 2 or longKey[-1] != key:
                        #~ tempList.remove((longKey, v))
                #~ if len(tempList) == 1: 
                    #~ longKey, longName = tempList[0]
                    #~ longKey = '_'.join(longKey)
                    #~ shortname, filterargs, type = value
                    #~ self.options['filteroverrides'][longKey] = (longName, filterargs, type)
                    #~ deleteKeys.append(key)
        for key, value in self.options['filteroverrides'].items():
            if key in self.optionsFilters and self.optionsFilters[key] == value:
                deleteKeys.append(key) 
        for key in deleteKeys:
            del self.options['filteroverrides'][key]        
        # Don't lose edited plugin and user function presets when the plugin/avsi 
        # is removed and the definition was not overrided
        for key, value in self.options['filterdefaults_presets'].items():
            if key not in self.optionsFilters:
                self.options['filteroverrides'][key] = value
        # Define data structures that are used by each script
        self.avsfilterdict = {}
        self.defineScriptFilterInfo()

    def ExportFilterData(self, filterDict, filename, onlylongnames=False):
        order = [1, 4, 0, 2, 3]
        keysdec = [(order.index(v[2]), k) for k,v in filterDict.items()]
        keysdec.sort()
        lines = []
        typeDict = {
            0: '[COREFILTERS]',
            1: '[CLIPPROPERTIES]',
            2: '[PLUGINS]',
            3: '[USERFUNCTIONS]',
            4: '[SCRIPTFUNCTIONS]',
        }
        currentType = None
        for keysortindex, key in keysdec:
            keytype = order[keysortindex]
            if keytype != currentType:
                extra = ''
                if len(lines) > 0:
                    if not lines[-1].endswith('\n\n'):
                        extra = '\n'
                lines.append(extra+typeDict[keytype]+'\n')
                currentType = keytype
            propername, args, ftype = filterDict[key]
            #~ if args.count('\n') != 0:
                #~ continue
            if onlylongnames and ftype == 2 and key.count('_') == 0:
                continue
            if ftype in (1, 4):
                line = propername+args+'\n'
            else:
                if args.count('\n') == 0:
                    line = '%s(\n%s\n)\n\n' % (propername, ',\n'.join(args.strip('()').split(', ')))
                    line = line.replace('[,\n...]', '[, ...]')
                else:
                    line = propername+args+'\n\n'
            lines.append(line)
        f = open(filename, 'w')
        f.writelines(lines)
        f.close()

    def defineScriptFilterInfo(self):
        # Create the basic filter dictionnary - {lowername: (args, style_constant)}
        styleList = [  # order is important here!
            AvsStyledTextCtrl.STC_AVS_COREFILTER,
            AvsStyledTextCtrl.STC_AVS_CLIPPROPERTY,
            AvsStyledTextCtrl.STC_AVS_PLUGIN,
            AvsStyledTextCtrl.STC_AVS_USERFUNCTION,
            AvsStyledTextCtrl.STC_AVS_SCRIPTFUNCTION,
        ]
        self.options['filterdefaults_presets'] = dict(
            [ # plugins and user functions with its preset edited but not the definition
            (lowername, (name, args, ftype)) 
            for lowername, (name, args, ftype) in self.optionsFilters.items() 
            if lowername in self.options['filterpresets'] and 
               lowername not in self.options['filteroverrides'] and
               ftype in (2, 3)
            ]
        )
        self.avsfilterdict.clear()
        self.avsfilterdict.update(dict(
            [
            (lowername, (args, styleList[ftype], name, None))
            for lowername,(name,args,ftype) in self.optionsFilters.items()
            ]
        ))
        overridedict = dict()
        for lowername, (name, args, ftype) in self.options['filteroverrides'].iteritems():
            overridedict[lowername] = args, styleList[ftype], name, None
            if ftype == 2:
                shortname = self.GetPluginFunctionShortName(lowername)
                if lowername not in self.plugin_shortnames[shortname]:
                    self.plugin_shortnames[shortname].append(lowername)
        self.avsfilterdict.update(overridedict)
        # Add short plugin names to avsfilterdict.  Priority rules:
        #   1. no excluded from autocomplete > excluded
        #   2. don't override user script functions
        #   3. autoloaded > filterdb > added by the user
        #   4.1 AviSynth lookup order (autoloaded)
        #   4.2 alphabetical (filterdb)
        #   4.3 undefined (added by the user)
        for shortname, long_name_list in self.plugin_shortnames.items():
            if shortname in self.avsfilterdict and self.avsfilterdict[shortname][1] == styleList[3]:
                if shortname not in self.options['filterremoved']:
                    continue
                user_function = True
            else:
                user_function = False
            for index, long_name in enumerate(long_name_list):
                if long_name not in self.options['filterremoved'] and \
                        self.options['autocompletepluginnames'].get(long_name) != 1:
                    break
            else:
                if user_function:
                    continue
                long_name = long_name_list[0]
            args, styletype, name = self.avsfilterdict[long_name][:3]
            self.avsfilterdict[shortname] = args, styletype, self.GetPluginFunctionShortName(name), long_name
        # Remove unchecked items from autocompletion, delete long and short names as required
        avsfilterdict_autocomplete = self.avsfilterdict.copy()
        for lowername, (args, styletype, name, is_short) in self.avsfilterdict.iteritems():
            if styletype == styleList[2]:
                if is_short:
                    if self.options['autocompletepluginnames'].get(is_short) == 1:
                        del avsfilterdict_autocomplete[lowername]
                else:
                    self.options['autocompletepluginnames'].setdefault(lowername, 0)
                    if self.options['autocompletepluginnames'][lowername] == 2 or \
                            lowername in self.options['filterremoved']:
                        del avsfilterdict_autocomplete[lowername]
            elif lowername in self.options['filterremoved']:
                del avsfilterdict_autocomplete[lowername]
        self.avsazdict = self.GetAutocompleteDict(avsfilterdict_autocomplete)
        self.avsazdict_all = self.GetAutocompleteDict(self.avsfilterdict)
        self.avssingleletters = [
            s for s in (self.avsfilterdict.keys()+self.avskeywords+self.avsmiscwords)
            if (len(s) == 1 and not s.isalnum() and s != '_')
        ]
    
    def GetPluginFunctionShortName(self, long_name):
        """Return the short name from a plugin function's mangled name"""
        for dllname in sorted(self.dllnameunderscored, reverse=True):
            if long_name.lower().startswith(dllname):
                return long_name[len(dllname)+1:]
        splitname = long_name.split('_', 1)
        if len(splitname) == 2:
            return splitname[1]
        return ''
    
    @staticmethod
    def GetAutocompleteDict(filter_dict):
        """Create a list for each letter (for autocompletion)"""
        avsazdict = collections.defaultdict(list)
        for lowername in sorted(filter_dict.keys()):
            first_letter = lowername[0]
            if first_letter.isalpha() or first_letter != '_':
                for char in lowername:
                    if not char.isalnum() and char != '_':
                        break
                else:
                    avsazdict[first_letter].append(filter_dict[lowername][2])
        return avsazdict
    
    def getFilterInfoFromAvisynth(self):
        self.avisynthVersion = (None,) * 3
        self.installed_plugins = set()
        self.installed_plugins_filternames = set()
        self.installed_avsi_filternames = set()
        self.dllnameunderscored = set()
        
        # get version info
        try:
            env = avisynth.AVS_ScriptEnvironment(3)
        except OSError:
            error = _('Make sure you have AviSynth installed and that there are no '
                      'unstable plugins or avsi files in the AviSynth plugins directory.')
            error = '\n'.join(textwrap.wrap(error, 70))
        else:
            if hasattr(env, 'get_error'):
                error = env.get_error()
            else:
                error = None
        if error:
            wx.SafeShowMessage(' '.join((self.name, self.version)), 
                              '\n\n'.join((_('Error loading AviSynth!'), error)))
            sys.exit(0)
        self.avisynthVersion = (env.invoke('VersionString'),
                                env.invoke('VersionNumber'),
                                env.invoke('Version').get_version())
        
        # retrieve existing filters (internal filters, autoloaded plugins and avsi files)
        self.avisynth_p = env.function_exists('AutoloadPlugins') # AviSynth+
        if self.avisynth_p:
            try:
                env.invoke('AutoloadPlugins')
            except avisynth.AvisynthError:
                pass
        # internal filters
        try:
            intfunc = env.get_var("$InternalFunctions$")
        except avisynth.AvisynthError as err:
            if str(err) != "NotFound": raise
            funclist = []
        else:
            funclist = [(name, 0) for name in intfunc.split()]
        # autoladed plugins
        try:
            pluginfunc = env.get_var("$PluginFunctions$")
        except avisynth.AvisynthError as err:
            if str(err) != "NotFound": raise
        else:
            pluginfuncList = []
            baddllnameList = []
            short_name = None
            for name in pluginfunc.split():
                if short_name is None:
                    short_name = name
                    continue
                long_name = name
                pos = long_name.find('_' + short_name)
                if pos == -1:
                    print>>sys.stderr, 'Error parsing plugin string at function "%s"\n' % long_name
                    break
                dllname = long_name[:pos]
                self.installed_plugins.add(dllname)
                if dllname in baddllnameList:
                    pass
                elif not dllname[0].isalpha() and dllname[0] != '_':
                    baddllnameList.append(dllname)
                else:
                    for char in dllname:
                        if not char.isalnum() and char != '_':
                            baddllnameList.append(dllname)
                            break
                if self.options['autoloadedplugins']:
                    pluginfuncList.append((long_name, 2))
                    self.plugin_shortnames[short_name.lower()].append(long_name.lower())
                self.installed_plugins_filternames.add(long_name.lower())
                if dllname.count('_'):
                    self.dllnameunderscored.add(dllname.lower())
                short_name = None
            if self.options['autoloadedplugins']:
                funclist += pluginfuncList
            if baddllnameList and self.options['dllnamewarning']:
                self.IdleCall.append((self.ShowWarningOnBadNaming, (baddllnameList, ), {}))
        # autoloaded avsi files
        try:
            userfunc = env.get_var("$UserFunctions$")
        except avisynth.AvisynthError as err:
            if str(err) != "NotFound": raise
        else:
            userfuncList = []
            for name in userfunc.split():
                self.installed_avsi_filternames.add(name.lower())
                userfuncList.append((name, 3))
            if self.options['autoloadedavsi']:
                funclist += userfuncList
        
        # get parameter info for each filter
        typeDict = {
            'c': 'clip',
            'i': 'int',
            'f': 'float',
            'b': 'bool',
            's': 'string',
            '.': 'var',
            #~ '*': '[...]',
        }
        functionDict = {}
        for name, functionType in funclist:
            if name.strip() == '':
                continue
            try:
                t = env.get_var("$Plugin!"+name+"!Param$")
            except avisynth.AvisynthError as err:
                if str(err) != "NotFound": raise
            else:
                argList = []
                namedarg = False
                namedargname = []
                for i, c in enumerate(t):
                    if c == '[':
                        namedarg = True
                    elif c == ']':
                        namedarg = False
                    elif namedarg:
                        namedargname.append(c)
                    else:
                        namedargindex = len(argList)
                        if c in ('+', '*'):
                            try:
                                typeDict[t[i-1]] # Helps ensure previous arg is valid
                                argList[-1] += ' [, ...]'
                            except (IndexError, KeyError):
                                print>>sys.stderr, (
                                    'Error parsing %s plugin parameters: '
                                    '+ without preceeding argument') % name
                        else:
                            try:
                                typeValue = typeDict[c]
                            except KeyError:
                                print>>sys.stderr, (
                                    'Error parsing %s plugin parameters: '
                                    'unknown character %s') % (name, repr(c))
                                typeValue = '?'
                            argList.append(typeValue)
                        if namedargname:
                            try:
                                argList[namedargindex] += ' "{0}"'.format(''.join(namedargname))
                            except IndexError:
                                print>>sys.stderr, (
                                    'Error parsing %s plugin parameters: '
                                    '[name] without following argument') % name
                                argList.append(''.join(namedargname))
                            namedargname = []
                argstring = '(%s)' % (', '.join(argList))
            if functionType == 0:
                if name.islower():
                    if argstring.startswith('(clip'):
                        functionType = 1
                    else:
                        functionType = 4
                elif argstring == '(clip)':
                    boolIsXXX = len(name) > 2 and name.startswith('Is') and name[2].isupper()
                    boolHasXXX = len(name) > 3 and name.startswith('Has') and name[3].isupper()
                    boolGetXXX = len(name) > 3 and name.startswith('Get') and name[3].isupper()
                    if boolIsXXX or boolHasXXX or boolGetXXX:
                        functionType = 1
            key = name.lower()
            functionDict[key] = (name, argstring, functionType)
        return functionDict

    def ParseAvisynthScript(self, filename='', script_text=None, quiet=False):
        pattern = r'function\s+([^\W_]\w*)\s*\((.*?)\)\s*\{(.+?)\}'
        default = r'default\s*\(\s*%s\s*,\s*(.+?)\s*\)'
        filterInfo, text = [], []
        if script_text is None:
            script_text = self.GetTextFromFile(filename)[0]
        for line in script_text.splitlines():
            line = line.strip().strip('\\')
            if not line.startswith('#'):
                text.append(line)
        text = ' '.join(text)
        matches = re.findall(pattern, text, re.I|re.S)
        for filtername, args, body in matches:
            text = ['(\n']
            varnameDict = {}
            if args.strip():
                for arg in args.split(','):
                    arg = arg.split()
                    if len(arg) == 2:
                        vartype, varname = arg
                    elif len(arg) == 1:
                        sep = arg[0].find('"') 
                        vartype = arg[0][:sep]
                        varname = arg[0][sep:]
                    else:
                        return None
                    text += [vartype, ' ', varname]
                    varname = varname.strip('"')
                    pat = default % varname
                    ret = re.search(pat, body, re.I|re.S)
                    if ret:
                        value = ret.group(1)
                        if (vartype in ['string', 'val'] or value.isdigit() or 
                            value.lower() in ['true', 'false']):
                            text += ['=', value]
                            varnameDict[varname] = value
                        else:
                            for name in varnameDict:
                                value = value.replace(name, varnameDict[name])
                            try:
                                value = str(eval(value))
                            except:
                                if not quiet:
                                    print _('Error'), 'ParseAvisynthScript() try eval(%s)' % value
                            else:
                                text += ['=', value]
                                varnameDict[varname] = value
                    text.append(',\n')
            if text[-1] == ',\n':
                text[-1] = '\n'
            text.append(')')
            filterargs = ''.join(text)
            filterInfo.append((filename, filtername, filterargs, 3))
        return filterInfo
    
    def wrapFilterCalltip(self, txt, maxchars=80):
        if txt.count('\n') > 0:
            return txt
        args = txt.split(',')
        argList = []
        count = 0
        lastArg = len(args) - 1
        for i, arg in enumerate(args):
            arg = arg.strip()
            if i != lastArg: #not arg.endswith(')'):
                arg += ', '
            count += len(arg)
            if count <= maxchars:
                argList.append(arg)
            else:
                argList.append('\n'+arg)
                count = len(arg)
        return ''.join(argList)

    def getOptionsDlgInfo(self):
        return (
            (_('Paths'),
                ((_('Available variables: %programdir%, %avisynthdir%, %pluginsdir%'), wxp.OPT_ELEM_SEP, None, '', dict(width=0, expand=False) ), ),
                ((_('Use a custom AviSynth directory')+' *', wxp.OPT_ELEM_CHECK, 'usealtdir', _('Choose a different version than the installed'), dict() ), ),
                ((_('Custom AviSynth directory:')+' *', wxp.OPT_ELEM_DIR, 'altdir', _('Alternative location of avisynth.dll/avxsynth.so'), dict(buttonText='...', buttonWidth=30) ), ),
                ((_('Plugins autoload directory:'), wxp.OPT_ELEM_DIR, 'pluginsdir', _('Leave blank to use the default directory. Changing it needs admin rights on Windows'), dict(buttonText='...', buttonWidth=30) ), ),
                ((_('Use a custom working directory'), wxp.OPT_ELEM_CHECK, 'useworkdir', _('Override the current working directory'), dict() ),
                 (_('For all scripts'), wxp.OPT_ELEM_CHECK, 'alwaysworkdir', _("Use the custom directory also for scripts saved to file, instead of its parent"), dict() ), ),
                ((_('Working directory:'), wxp.OPT_ELEM_DIR, 'workdir', _('Specify an alternative working directory'), dict(buttonText='...', buttonWidth=30) ), ),
                ((_('External player:'), wxp.OPT_ELEM_FILE, 'externalplayer', _('Location of external program for script playback'), dict(fileMask=(_('Executable files') + ' (*.exe)|*.exe|' if os.name == 'nt' else '') + _('All files') + ' (*.*)|*.*', buttonText='...', buttonWidth=30) ), ),
                ((_('External player extra args:'), wxp.OPT_ELEM_STRING, 'externalplayerargs', _('Additional arguments when running the external player'), dict() ), ),
                ((_('Avisynth help file/url:'), wxp.OPT_ELEM_FILE_URL, 'avisynthhelpfile', _('Location of the avisynth help file or url'), dict(buttonText='...', buttonWidth=30) ), ),
                ((_('Documentation search paths:'), wxp.OPT_ELEM_STRING, 'docsearchpaths', _('Specify which directories to search for docs when you click on a filter calltip'), dict() ), ),
                ((_('Documentation search url:'), wxp.OPT_ELEM_STRING, 'docsearchurl', _("The web address to search if docs aren't found (the filter's name replaces %filtername%)"), dict() ), ),
            ),
            (_('Text'),
                ((_('Style inside triple-quoted strings'), wxp.OPT_ELEM_CHECK, 'syntaxhighlight_styleinsidetriplequotes', _("Highlight the text as if it wasn't enclosed by triple quotes"), dict() ), ),
                ((_('Prefer functions over variables'), wxp.OPT_ELEM_CHECK, 'syntaxhighlight_preferfunctions', _('When a word could be either a function or a variable, highlight it as function'), dict() ), ),
                ((_('Wrap text'), wxp.OPT_ELEM_CHECK, 'wrap', _("Don't allow lines wider than the window"), dict() ), ),
                ((_('Draw lines at fold points'), wxp.OPT_ELEM_CHECK, 'foldflag', _('For code folding, draw a line underneath if the fold point is not expanded'), dict() ), ),
                ((_('Use tabs instead of spaces'), wxp.OPT_ELEM_CHECK, 'usetabs', _('Check to insert actual tabs instead of spaces when using the Tab key'), dict() ), ),
                ((_('Tab width'), wxp.OPT_ELEM_SPIN, 'tabwidth', _('Set the size of the tabs in spaces'), dict(min_val=0) ), ),
                ((_('Line margin width'), wxp.OPT_ELEM_SPIN, 'numlinechars', _('Initial space to reserve for the line margin in terms of number of digits. Set it to 0 to disable showing line numbers'), dict(min_val=0) ), ),
                ((_('Show filter calltips'), wxp.OPT_ELEM_CHECK, 'calltips', _('Turn on/off automatic tips when typing filter names'), dict() ), ),
                ((_('Frequent calltips'), wxp.OPT_ELEM_CHECK, 'frequentcalltips', _("Always show calltips any time the cursor is within the filter's arguments"), dict(ident=20) ), ),
                ((_('Show autocomplete on capital letters'), wxp.OPT_ELEM_CHECK, 'autocomplete', _('Turn on/off automatic autocomplete list when typing words starting with capital letters'), dict() ), ),
                (('       '+_('Amount of letters typed'), wxp.OPT_ELEM_SPIN, 'autocompletelength', _('Show autocomplete list when typing a certain amount of letters'), dict(min_val=0) ), ),
            ),
            (_('Autocomplete'),
                ((_('AviSynth user function database'), wxp.OPT_ELEM_SEP, '', _('Select what functions beside internal and user-defined will be included in the database'), dict(adjust_width=True) ), ),
                ((_('Autoloaded plugin functions')+' *', wxp.OPT_ELEM_CHECK, 'autoloadedplugins', _('Include the functions on autoloaded plugins in the database'), dict() ),
                 (_('Autoloaded script functions')+' *', wxp.OPT_ELEM_CHECK, 'autoloadedavsi', _('Include the functions on autoloaded avsi files in the database'), dict() ), ),
                ((_('Plugin functions from database')+' *', wxp.OPT_ELEM_CHECK, 'fdb_plugins', _("Include plugin functions from the program's database"), dict() ),
                 (_('Script functions from database')+' *', wxp.OPT_ELEM_CHECK, 'fdb_userscriptfunctions', _("Include user script functions from the program's database"), dict() ), ),
                ((_('Autocomplete'), wxp.OPT_ELEM_SEP, '', '', dict(adjust_width=True) ), ),
                ((_('Show autocomplete with variables'), wxp.OPT_ELEM_CHECK, 'autocompletevariables', _('Add user defined variables into autocomplete list'), dict() ), ),
                ((_('Show autocomplete on single matched lowercase variable'), wxp.OPT_ELEM_CHECK, 'autocompletesingle', _('When typing a lowercase variable name, show autocomplete if there is only one item matched in keyword list'), dict(ident=20) ), ),
                ((_('Show autocomplete with icons'), wxp.OPT_ELEM_CHECK, 'autocompleteicons', _("Add icons into autocomplete list. Using different type to indicate how well a filter's presets is defined"), dict() ), ),
                ((_("Don't show autocomplete when calltip is active"), wxp.OPT_ELEM_CHECK, 'calltipsoverautocomplete', _('When calltip is active, autocomplete will not be activate automatically. You can still show autocomplete manually'), dict() ), ),
                ((_('Autoparentheses level'), wxp.OPT_ELEM_RADIO, 'autoparentheses', _('Determines parentheses to insert upon autocompletion'), dict(choices=[(_('None " "'), 0),(_('Open "("'), 1),(_('Close "()"'), 2)])), ),
                ((_('Preset activation key'), wxp.OPT_ELEM_RADIO, 'presetactivatekey', _('Determines which key activates the filter preset when the autocomplete box is visible'), dict(choices=[(_('Tab'), 'tab'),(_('Return'), 'return'),(_('Both'), 'both'),(_('None'), 'none')]) ), ),
            ),
            (_('Video'),
                ((_('Constantly update video while dragging'), wxp.OPT_ELEM_CHECK, 'dragupdate', _('Update the video constantly when dragging the frame slider'), dict() ), ),
                ((_('Enable line-by-line update'), wxp.OPT_ELEM_CHECK, 'autoupdatevideo', _('Enable the line-by-line video update mode (update every time the cursor changes line position)'), dict() ), ),
                ((_('Focus the video preview upon refresh'), wxp.OPT_ELEM_CHECK, 'focusonrefresh', _('Switch focus to the video preview window when using the refresh command'), dict() ), ),
                ((_('Refresh preview automatically'), wxp.OPT_ELEM_CHECK, 'refreshpreview', _('Refresh preview when switch focus on video window or change a value in slider window'), dict() ), ),
                ((_('Shared timeline'), wxp.OPT_ELEM_CHECK, 'enableframepertab', _('Seeking to a certain frame will seek to that frame on all tabs'), dict() ), ),
                ((_('Only on tabs of the same characteristics'), wxp.OPT_ELEM_CHECK, 'enableframepertab_same', _('Only share timeline for clips with the same resolution and frame count'), dict(ident=20) ), ),
                ((_('Enable scroll wheel through similar tabs'), wxp.OPT_ELEM_CHECK, 'enabletabscrolling', _('Mouse scroll wheel cycles through tabs with similar videos'), dict() ), ),
                ((_('Enable scroll wheel through tabs on the same group'), wxp.OPT_ELEM_CHECK, 'enabletabscrolling_groups', _('Mouse scroll wheel cycles through tabs assigned to the same tab group'), dict() ), ),
                ((_('Allow AvsPmod to resize the window'), wxp.OPT_ELEM_CHECK, 'allowresize', _('Allow AvsPmod to resize and/or move the program window when updating the video preview'), dict() ), ),
                ((_('Separate video preview window')+' *', wxp.OPT_ELEM_CHECK, 'separatevideowindow', _('Use a separate window for the video preview'), dict() ), ),
                ((_('Keep it on top of the main window')+' *', wxp.OPT_ELEM_CHECK, 'previewontopofmain', _('Keep the video preview window always on top of the main one and link its visibility'), dict(ident=20) ), ),
                ((_('Min text lines on video preview'), wxp.OPT_ELEM_SPIN, 'mintextlines', _('Minimum number of lines to show when displaying the video preview'), dict(min_val=0) ), ),
                ((_('Customize video status bar...'), wxp.OPT_ELEM_BUTTON, 'videostatusbarinfo', _('Customize the video information shown in the program status bar'), dict(handler=self.OnConfigureVideoStatusBarMessage) ), ),
                ((_('Error message font'), wxp.OPT_ELEM_FONT, 'errormessagefont', _('Set the font used for displaying the error if evaluating the script fails'), dict() ), ),
            ),
            (_('User Sliders'),
                ((_('Hide slider window by default'), wxp.OPT_ELEM_CHECK, 'keepsliderwindowhidden', _('Keep the slider window hidden by default when previewing a video'), dict() ), ),
                ((_('Create user sliders automatically'), wxp.OPT_ELEM_CHECK, 'autoslideron', _('Create user sliders automatically using the filter database'), dict() ), ),
                ((_('type int/float (numerical slider)'), wxp.OPT_ELEM_CHECK, 'autoslidermakeintfloat', _('Create user sliders for int and float arguments'), dict(ident=20) ), ),
                ((_('type int (list)'), wxp.OPT_ELEM_CHECK, 'autoslidermakeintlist', _('Create listboxes for int list arguments'), dict(ident=20) ), ),
                ((_('type int (hex color)'), wxp.OPT_ELEM_CHECK, 'autoslidermakecolor', _('Create color pickers for hex color arguments'), dict(ident=20) ), ),
                ((_('type bool'), wxp.OPT_ELEM_CHECK, 'autoslidermakebool', _('Create radio boxes for bool arguments'), dict(ident=20) ), ),
                ((_('type string (list)'), wxp.OPT_ELEM_CHECK, 'autoslidermakestringlist', _('Create listboxes for string list arguments'), dict(ident=20) ), ),
                ((_('type string (filename)'), wxp.OPT_ELEM_CHECK, 'autoslidermakestringfilename', _('Create filename pickers for string filename arguments'), dict(ident=20) ), ),
                ((_('undocumented'), wxp.OPT_ELEM_CHECK, 'autoslidermakeunknown', _('Create placeholders for arguments which have no database information'), dict(ident=20) ), ),
                ((_('Fold startup setting'), wxp.OPT_ELEM_RADIO, 'autosliderstartfold', _('Determines which filters will initially have hidden arguments in the slider window'), dict(choices=[(_('Fold all'), 0),(_('Fold none'), 1),(_('Fold non-numbers'), 2)]) ), ),
                ((_('Filter exclusion list:'), wxp.OPT_ELEM_STRING, 'autosliderexclusions', _('Specify filters never to build automatic sliders for'), dict() ), ),
            ),
            (_('Save/Load'),
                ((_('Save session for next launch'), wxp.OPT_ELEM_CHECK, 'startupsession', _('Automatically save the session on shutdown and load on next startup'), dict() ), ),
                ((_('Always load startup session'), wxp.OPT_ELEM_CHECK, 'alwaysloadstartupsession', _('Always load the auto-saved session before opening any other file on startup'), dict() ), ),
                ((_("Don't preview when loading a session"), wxp.OPT_ELEM_CHECK, 'hidepreview', _('Always hide the video preview window when loading a session'), dict() ), ),
                ((_('Backup session periodically (minutes)'), wxp.OPT_ELEM_SPIN, 'periodicbackup', _('Backup the session every X minutes, if X > 0'), dict(min_val=0) ), ),
                ((_('Backup session when previewing'), wxp.OPT_ELEM_CHECK, 'paranoiamode', _('If checked, the current session is backed up prior to previewing any new script'), dict() ), ),
                ((_('Prompt to save when previewing'), wxp.OPT_ELEM_CHECK, 'promptwhenpreview', _('Prompt to save a script before previewing (inactive if previewing with unsaved changes)'), dict() ), ),
                ((_('Preview scripts with unsaved changes'), wxp.OPT_ELEM_CHECK, 'previewunsavedchanges', _('Create a temporary preview script with unsaved changes when previewing the video'), dict() ), ),
                ((_("Don't prompt to save scripts without file"), wxp.OPT_ELEM_CHECK, 'closeneversaved', _("When closing a tab, don't prompt to save the script if it doesn't already exist on the filesystem"), dict() ), ),
                ((_('Prompt to save scripts on program exit'), wxp.OPT_ELEM_CHECK, 'promptexitsave', _('Prompt to save each script with unsaved changes when exiting the program'), dict() ), ),
                ((_('Line endings'), wxp.OPT_ELEM_LIST, 'eol', _('Auto: CRLF on Windows and LF on *nix for new scripts, existing scripts keep their current line endings'), dict(choices=[(_('Auto'), 'auto'), (_('Force CRLF'), 'force crlf'), (_('Force LF'), 'force lf')]) ), ),
                ((_('Save *.avs scripts with AvsPmod markings'), wxp.OPT_ELEM_CHECK, 'savemarkedavs', _('Save AvsPmod-specific markings (user sliders, toggle tags, etc) as a commented section in the *.avs file'), dict() ), ),
                ((_('Start dialogs on the last used directory'), wxp.OPT_ELEM_CHECK, 'userecentdir', _("If unchecked, the script's directory is used"), dict() ), ),
                ((_('Start save image dialogs on the last used directory'), wxp.OPT_ELEM_CHECK, 'useimagesavedir', _("If unchecked, the script's directory is used"), dict() ), ),
                ((_('Default image filename pattern'), wxp.OPT_ELEM_STRING, 'imagenamedefaultformat', _("Choose a default pattern for image filenames. %s -> script title, %06d -> frame number padded to six digits"), dict() ), ),
                ((_('Ask for JPEG quality'), wxp.OPT_ELEM_CHECK, 'askjpegquality', _("When saving a JPEG image, prompt for the quality level. Use the value from the last time if not checked"), dict() ), ),
            ),
            (_('Misc'),
                ((_('Language')+' *', wxp.OPT_ELEM_LIST, 'lang', _('Choose the language used for the interface'), dict(choices=self.getTranslations()) ), ),
                ((_('Use large size video controls')+' *', wxp.OPT_ELEM_CHECK, 'largeui', _('Double the size of the buttons on the video control bar'), dict() ), ),
                #~((_('Load bookmarks on startup'), wxp.OPT_ELEM_CHECK, 'loadstartupbookmarks', _('Load video bookmarks from the previous session on program startup'), dict() ), ),
                #~ ((_('Show full pathname in program title'), wxp.OPT_ELEM_CHECK, 'showfullname', _('Show the full pathname of the current script in the program title'), dict() ), ),
                #~ ((_('Use custom AviSynth lexer'), wxp.OPT_ELEM_CHECK, 'usecustomlexer', _('Use the custom AviSynth syntax highlighting lexer (may be slower)'), dict() ), ),
                ((_('Use keyboard images in tabs'), wxp.OPT_ELEM_CHECK, 'usetabimages', _('Show keyboard images in the script tabs when video has focus'), dict() ), ),
                ((_('Show tabs in multiline style'), wxp.OPT_ELEM_CHECK, 'multilinetab', _('There can be several rows of tabs'), dict() ), ),
                ((_('Show tabs in fixed width'), wxp.OPT_ELEM_CHECK, 'fixedwidthtab', _('All tabs will have same width'), dict() ), ),
                ((_('Invert scroll wheel direction'), wxp.OPT_ELEM_CHECK, 'invertscrolling', _('Scroll the mouse wheel up for changing tabs to the right'), dict() ), ),
                ((_('Only allow a single instance of AvsPmod')+' *', wxp.OPT_ELEM_CHECK, 'singleinstance', _('Only allow a single instance of AvsPmod'), dict() ), ),
                ((_('Show warning for bad plugin naming at startup'), wxp.OPT_ELEM_CHECK, 'dllnamewarning', _('Show warning at startup if there are dlls with bad naming in default plugin folder'), dict() ), ),
                ((_('Max number of recent filenames'), wxp.OPT_ELEM_SPIN, 'nrecentfiles', _('This number determines how many filenames to store in the recent files menu'), dict(min_val=0) ), ),
                ((_('Custom jump size:'), wxp.OPT_ELEM_SPIN, 'customjump', _('Jump size used in video menu'), dict(min_val=0) ), ),
                ((_('Custom jump size units'), wxp.OPT_ELEM_RADIO, 'customjumpunits', _('Units of custom jump size'), dict(choices=[(_('frames'), 'frames'),(_('seconds'), 'sec'),(_('minutes'), 'min'),(_('hours'), 'hr')]) ), ),
            ),
        )
    
    def getTranslations(self, return_paths=False):
        '''Return the list of 'translation_lng.py' files within the translations subfolder'''
        if return_paths:
            paths = []
            re_lng = re.compile(r'translation_(\w{3})\.py', re.I)
        else:
            translation_list = set()
            translation_list.add((i18n.display_name('eng'), 'eng'))
            re_lng = re.compile(r'translation_(\w{3})\.py[co]?', re.I)
        if os.path.isdir(self.translations_dir):
            for file in os.listdir(self.translations_dir): 
                match = re_lng.match(file)
                if match:
                    if return_paths:
                        paths.append((os.path.join(self.translations_dir, file), match.group(1)))
                    else:
                        translation_list.add((i18n.display_name(match.group(1)), match.group(1)))
        if return_paths:
            return paths
        return sorted(translation_list)
    
    def createWindowElements(self):
        # Create the program's status bar
        statusBar = self.CreateStatusBar(2)
        statusBar.SetStatusWidths([-1, 0])
        
        class PartialFormatter(string.Formatter):
            
            def get_value(self, key, args, kwds):
                try:
                    return string.Formatter.get_value(self, key, args, kwds)
                except KeyError:
                    return '%' + key
        
        self.status_bar_formatter = PartialFormatter()
        
        # Create the main subwindows
        if wx.VERSION < (2, 9):
            self.programSplitter = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_NOBORDER)
        else:
            self.programSplitter = self
        self.mainSplitter = wx.SplitterWindow(self.programSplitter, wx.ID_ANY, style=wx.SP_3DSASH|wx.SP_NOBORDER|wx.SP_LIVE_UPDATE)
        if not self.separatevideowindow:
            parent = self.mainSplitter
        else:
            #~ self.videoDialog = wx.Dialog(self, wx.ID_ANY, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
            style=wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS
            if self.options['previewontopofmain']:
                style = style|wx.FRAME_FLOAT_ON_PARENT
            if self.options['previewalwaysontop']:
                style = style|wx.STAY_ON_TOP
            self.videoDialog = wx.Frame(self, wx.ID_ANY,style=style)#, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
            if self.options['previewontopofmain']: # main window loses 'always on top' effect
                self.ToggleWindowStyle(wx.STAY_ON_TOP)
                self.ToggleWindowStyle(wx.STAY_ON_TOP)
            dimensions = self.options.get('dimensions2')
            if dimensions is not None and dimensions[0] > 0 and dimensions[1] > 0:
                self.videoDialog.SetDimensions(*dimensions)
                # Move the window if it's offscreen
                size = self.videoDialog.GetSize()
                pos = self.videoDialog.GetPosition()
                wC, hC = wx.ScreenDC().GetSize()
                #~ if (pos[0]+size[0]>wC) or (pos[1]+size[1]>hC):
                if (pos[0]+50>wC) or (pos[1]+50>hC):
                    self.videoDialog.Center()
            self.videoDialog.SetIcon(AvsP_icon.getIcon())
            self.videoDialog.Bind(wx.EVT_CLOSE, self.OnMenuVideoHide)
            def OnVideoDialogActivate(event):
                if event.GetActive():
                    self.ShowVideoFrame()
                event.Skip()
            # It doesn't seem necessary.  Also causes the 'navigate' menu options to malfunction 
            # and the preview to be refreshed when only the title or video control bar is pressed
            #self.videoDialog.Bind(wx.EVT_ACTIVATE, OnVideoDialogActivate)
            self.videoDialog.oldSize = None
            def OnVideoDialogResizeEnd(event):
                if self.zoomwindow:
                    newSize = event.GetSize()
                    oldSize = self.videoDialog.oldSize
                    if oldSize is not None and newSize == oldSize:
                        #~ self.ShowVideoFrame(forceRefresh=True)
                        self.ShowVideoFrame()
                        self.videoDialog.oldSize = None
                    else:
                        self.videoDialog.oldSize = newSize
                event.Skip()
            self.videoDialog.Bind(wx.EVT_SIZING, OnVideoDialogResizeEnd)
            #~ def OnVideoDialogKeyDown(event):
                #~ keycode = event.GetKeyCode()
                #~ if keycode == wx.WXK_DELETE:
            #~ self.videoDialog.Bind(wx.EVT_KEY_DOWN, OnVideoDialogKeyDown)
            parent = self.videoDialog
        self.videoPane = wx.Panel(parent, wx.ID_ANY)
        self.videoSplitter = wx.SplitterWindow(self.videoPane, wx.ID_ANY, style=wx.SP_3DSASH|wx.SP_NOBORDER|wx.SP_LIVE_UPDATE)

        if self.options['largeui']:
            w = 16
            h = 72
            bmpMask = wx.EmptyBitmap(w, h)
            mdc = wx.MemoryDC()
            mdc.SelectObject(bmpMask)
            mdc.DrawPolygon([(14,0), (2,9), (14,18)])
            mdc.DrawPolygon([(14,26), (2,35), (14,44)])
            mdc.DrawPolygon([(14,52), (2,61), (14,70)])
        else:
            w = 10
            h = 50
            bmpMask = wx.EmptyBitmap(w, h)
            mdc = wx.MemoryDC()
            mdc.SelectObject(bmpMask)
            mdc.DrawPolygon([(8,0), (2,6), (8,12)])
            mdc.DrawPolygon([(8,18), (2,24), (8,30)])
            mdc.DrawPolygon([(8,36), (2,42), (8,48)])
        mdc = None
        bmpShow = wx.EmptyBitmap(w, h)
        #~ mdc = wx.MemoryDC()
        #~ mdc.SelectObject(bmpShow)
        #~ mdc.SetBackground(wx.Brush(wx.Colour(90, 90, 90)))
        #~ mdc.Clear()
        #~ mdc = None
        bmpShow.SetMask(wx.Mask(bmpMask))
        bmpHide = bmpShow.ConvertToImage().Mirror().ConvertToBitmap()
        self.toggleSliderWindowButton = wxButtons.GenBitmapButton(self.videoPane, wx.ID_ANY, bmpHide, size=(w,h), style=wx.NO_BORDER)
        self.toggleSliderWindowButton.bmpShow = bmpShow
        self.toggleSliderWindowButton.bmpHide = bmpHide
        def OnTSWButtonSize(event):
            dc = wx.WindowDC(self.toggleSliderWindowButton)
            dc.Clear()
            wButton, hButton = self.toggleSliderWindowButton.GetClientSizeTuple()
            self.toggleSliderWindowButton.DrawLabel(dc, wButton, hButton)
            event.Skip()
        self.toggleSliderWindowButton.Bind(wx.EVT_SIZE, OnTSWButtonSize)
        def OnToggleSliderWindowButton(event):
            self.ToggleSliderWindow(vidrefresh=True)
            script = self.currentScript
            script.userHidSliders = not script.sliderWindowShown
            self.videoWindow.SetFocus()
        self.videoPane.Bind(wx.EVT_BUTTON, OnToggleSliderWindowButton, self.toggleSliderWindowButton)
        #~ forwardButton.SetBackgroundColour(wx.BLACK)

        self.videoPaneSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.videoPaneSizer.Add(self.videoSplitter, 1, wx.EXPAND|wx.ALL, 0)
        self.videoPaneSizer.Add(self.toggleSliderWindowButton, 0, wx.EXPAND|wx.ALL, 0)
        self.videoPane.SetSizer(self.videoPaneSizer)
        #~ self.videoPaneSizer.Layout()


        def OnVideoSplitterPosChanged(event):
            if self.zoomwindowfit:
                self.ShowVideoFrame(focus=False)
                #~ self.ShowVideoFrame(forceRefresh=True, focus=False)
                #~ self.IdleCall = (self.ShowVideoFrame, tuple(), {'forceRefresh': True, 'focus': False})
                #~ wx.FutureCall(100, self.ShowVideoFrame, forceRefresh=True, focus=False)
            event.Skip()
        #~ self.videoSplitter.Bind(wx.EVT_LEFT_UP, OnVideoSplitterPosChanged)

        self.mainSplitter.SetSplitMode(wx.SPLIT_HORIZONTAL)
        self.mainSplitter.SetSashSize(4)
        self.videoSplitter.SetSashSize(4)
        
        self.programSplitterSize = None
        
        self.mainSplitter.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClickWindow)
        self.mainSplitter.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDownWindow)

        self.clicked_on_divider = False
        def OnMainSplitterLeftDown(event):
            pos = event.GetPosition()[self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL]
            if pos > self.mainSplitter.GetMinimumPaneSize():
                self.clicked_on_divider = True
            else:
                self.clicked_on_divider = False
            if self.FindFocus() == self.titleEntry:
                self.scriptNotebook.SetFocus()
            event.Skip()
        self.mainSplitter.Bind(wx.EVT_LEFT_DOWN, OnMainSplitterLeftDown)

        def OnMainSplitterPosChanged(event):
            #~ self.lastSplitVideoPos = event.GetSashPosition()
            if self.clicked_on_divider:
                self.currentScript.lastSplitVideoPos = self.mainSplitter.GetSashPosition() - \
                    self.mainSplitter.GetClientSize()[self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL]
                self.clicked_on_divider = False
                if self.zoomwindow:
                    #~ for index in xrange(self.scriptNotebook.GetPageCount()):
                        #~ script = self.scriptNotebook.GetPage(index)
                        #~ self.UpdateScriptAVI(script, forceRefresh=True)
                    #~ self.ShowVideoFrame(forceRefresh=True, focus=False)
                    self.ShowVideoFrame(focus=False)
            event.Skip()
        self.mainSplitter.Bind(wx.EVT_LEFT_UP, OnMainSplitterPosChanged)
        self.mainSplitterSize = None
        
        self.videoSplitter.Bind(wx.EVT_SPLITTER_DCLICK, self.OnLeftDClickVideoSplitter)
        
        def OnVideoSplitterPosChanged(event):
            sliderWindowWidth = self.videoSplitter.GetClientSize()[0] - self.videoSplitter.GetSashPosition()
            #~ sliderWindowWidth = self.videoPane.GetClientSize()[0] - self.videoSplitter.GetSashPosition()
            if True: #sliderWindowWidth - self.videoSplitter.GetSashSize() > self.videoSplitter.GetMinimumPaneSize():
                newpos = self.videoSplitter.GetSashPosition() - self.videoSplitter.GetClientSize()[0]
                #~ newpos = self.videoSplitter.GetSashPosition() - self.videoPane.GetClientSize()[0]
                self.currentScript.lastSplitSliderPos = newpos
                self.currentScript.sliderWindowShown = True
            else:
                self.currentScript.sliderWindowShown = False
            if self.zoomwindowfit:
                #~ self.ShowVideoFrame(forceRefresh=True, focus=False)
                self.ShowVideoFrame(focus=False)
            event.Skip()            
        self.videoSplitter.Bind(wx.EVT_LEFT_UP, OnVideoSplitterPosChanged)
        #~ self.videoSplitter.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, OnVideoSplitterPosChanged)
        self.videoSplitterSize = None
        
        # Create the program's text editing notebook
        self.scriptNotebook = self.createScriptNotebook()        
        self.scriptNotebook.dblClicked = False
        #~ self.UpdateTabStyle()        
        scriptWindow = self.createScriptWindow()
        self.currentScript = scriptWindow
        self.currentSliderWindow = scriptWindow.sliderWindow
        self.scriptNotebook.AddPage(scriptWindow, self.NewFileName)        
        # Create the program's video preview window
        self.videoWindow = self.createVideoWindow(self.videoSplitter)
        
        # Create the program's menu
        shortcutList = []
        oldShortcuts = ([item[0] for item in self.options['shortcuts']], self.options['shortcuts'])        
        self.menuBackups = [1, 2] #if wx.VERSION > (2, 8) else []
        menuBar = self.createMenuBar(self.menuInfo(), shortcutList, oldShortcuts, self.menuBackups)
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU_OPEN, self.OnMenuBar)
        video_menu = self.GetMenuBar().GetMenu(2)
        self.tab_group_menu = video_menu.FindItemById(video_menu.FindItem(_('Add tab to group'))).GetSubMenu()
        scriptWindow.contextMenu = self.menuBackups[0] if self.menuBackups else self.GetMenuBar().GetMenu(1)
        self.videoWindow.contextMenu = self.menuBackups[1] if self.menuBackups else self.GetMenuBar().GetMenu(2)
        # Add the tools to the menu
        self.createToolsMenu(shortcutList, oldShortcuts)
        # Add the macros to the menu
        self.createMacroMenu(shortcutList, oldShortcuts)
        # Set the shortcut list
        self.options['shortcuts'] = None
        self.options['shortcuts'] = shortcutList
        
        self.bindShortcutsToAllWindows()
        
        # Create the program's video controls
        self.videoControls = self.createVideoControls(self.programSplitter)
        spos = self.videoControls.GetClientSize().height + 6
        self.toolbarHeight = spos
        
        if wx.VERSION < (2, 9):
            self.programSplitter.SetSashSize(0)
            self.programSplitter.SplitHorizontally(self.mainSplitter, self.videoControls, -spos)
        
        # Set the minimum pane sizes
        self.SetMinimumScriptPaneSize()
        self.videoSplitter.SetMinimumPaneSize(3)
        #~ self.videoSplitter.SetMinimumPaneSize(300)
        
        # Manually implement splitter gravity (improper size updating with sub-splitters...)
        #~ self.programSplitter.SetSashGravity(1.0)
        #~ self.mainSplitter.SetSashGravity(1.0)
        self.videoSplitter.SetSashGravity(1.0)
        def OnProgramSplitterSize(event):
            # programSplitter gravity
            if wx.VERSION < (2, 9):
                self.programSplitter.SetSashPosition(-self.toolbarHeight)
                        
            #~ if self.currentScript.sliderWindowShown:
                #~ self.currentScript.lastSplitSliderPos = -widthSliderWindow
            # mainSplitter gravity
            if self.mainSplitter.IsSplit():
                #~ heightVideoWindow = self.mainSplitter.GetSize()[1] - self.mainSplitter.GetSashPosition()
                #~ self.mainSplitter.SetSashPosition(-heightVideoWindow)
                pos = self.GetMainSplitterNegativePosition()
                self.mainSplitter.SetSashPosition(pos)
                self.currentScript.lastSplitVideoPos = pos
            event.Skip()
        self.programSplitter.Bind(wx.EVT_SIZE, OnProgramSplitterSize)

        if not self.separatevideowindow:
            if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                self.mainSplitter.SplitHorizontally(self.scriptNotebook, self.videoPane)
            else:
                self.mainSplitter.SplitVertically(self.scriptNotebook, self.videoPane)
        else:
            self.mainSplitter.SplitHorizontally(self.scriptNotebook, wx.Panel(self.mainSplitter, wx.ID_ANY))
            self.mainSplitter.Unsplit()
            # Layout the separate video window
            self.videoControls2 = self.createVideoControls(self.videoDialog, primary=False)
            self.videoStatusBar = wx.StatusBar(self.videoDialog, wx.ID_ANY)#self.videoDialog.CreateStatusBar()
            self.videoStatusBar.SetFieldsCount(2)
            self.videoStatusBar.SetStatusWidths([-1, 0])
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.videoPane, 1, wx.EXPAND)
            sizer.Add(self.videoControls2, 0, wx.EXPAND|wx.ALL, 0)
            sizer.Add(self.videoStatusBar, 0, wx.EXPAND)
            self.videoDialog.SetSizer(sizer)
            sizer.Layout()
        
        #~ self.videoSplitter.SplitVertically(self.videoWindow, self.currentScript.sliderWindow, self.currentScript.lastSplitSliderPos)
        self.videoSplitter.SplitVertically(self.videoWindow, self.currentScript.sliderWindow, 10)
        #~ self.videoSplitter.UpdateSize()
        #~ self.videoPaneSizer.Layout()
        #~ self.videoSplitter.Unsplit()
        
        if wx.VERSION > (2, 9):
            mainFrameSizer = wx.BoxSizer(wx.VERTICAL)
            mainFrameSizer.Add(self.mainSplitter, 1, wx.EXPAND)
            mainFrameSizer.Add(self.videoControls, 0, wx.EXPAND)
            self.SetSizer(mainFrameSizer)
        
        # Hide the video preview initially
        self.HidePreviewWindow()

        # Misc
        scriptWindow.SetFocus()
        self.SetMinSize((320, 240))

    def SetMinimumScriptPaneSize(self):
        if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            minpanesize = 23
            mintextlines = max(0, self.options['mintextlines'])
            if mintextlines != 0:
                scrollbarheight = self.currentScript.GetSize().height - self.currentScript.GetClientSize().height
                minpanesize = minpanesize + mintextlines * self.currentScript.TextHeight(0) + scrollbarheight + 5
            self.mainSplitter.SetMinimumPaneSize(minpanesize)
        else:
            self.mainSplitter.SetMinimumPaneSize(100)
    
    def bindShortcutsToAllWindows(self):        
        self._shortcutBindWindowDict = {self:[], self.videoWindow:[]}
        self.useEscape = False
        for label, shortcut, id in self.options['shortcuts']:
            if not shortcut:
                continue
            if shortcut.endswith('Escape'):
                self.useEscape = True
            if shortcut in self.exceptionShortcuts:
                self._shortcutBindWindowDict[self.videoWindow].append(id)
            elif shortcut != 'Escape' and shortcut in self.options['reservedshortcuts']:
                if (label, shortcut) not in self.stcShortcuts[-1]:
                    self._shortcutBindWindowDict[self.videoWindow].append(id)
            else:
                self._shortcutBindWindowDict[self].append(id)            
        self.BindShortcutsToWindows(self.options['shortcuts'])
        #~ self.BindShortcutsToWindows(self.optionsShortcuts, forcewindow=self.scrapWindow.textCtrl)
        self.scrapWindow.BindShortcuts()
        # Bind shortcuts to the video window if necessary
        if self.separatevideowindow:
            self.BindShortcutsToWindows(self.options['shortcuts'], forcewindow=self.videoWindow)
        if True:#wx.VERSION > (2, 8):
            if self.useEscape:
                self.Bind(wx.EVT_CHAR_HOOK, self.OnCharHook)
                if self.separatevideowindow:
                    self.videoWindow.Bind(wx.EVT_CHAR_HOOK, self.OnCharHook)
            else:
                self.Unbind(wx.EVT_CHAR_HOOK)
                if self.separatevideowindow:
                    self.videoWindow.Unbind(wx.EVT_CHAR_HOOK)

    def menuInfo(self):
        self.exceptionShortcuts = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'Enter', 'Space', 'Insert', 'Backspace', 'Delete', 
            'Home', 'End', 'PgUp', 'PgDn', 'Up', 'Down', 'Left', 'Right',
            'Numpad 0', 'Numpad 1', 'Numpad 2', 'Numpad 3', 'Numpad 4', 'Numpad 5', 'Numpad 6', 'Numpad 7', 'Numpad 8', 'Numpad 9',
            'Numpad +', 'Numpad -', 'Numpad *', 'Numpad /', 'Numpad .', 'Numpad Enter',
            '`', '-', '=', '\\', '[', ']', ';', "'", ',', '.', '/',
            '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '|', '{', '}', ':', '"', '<', '>', '?',
        ]
        self.stcShortcuts = [
            ('Shift+Down',          _('Extend selection to line down position')),
            ('Ctrl+Down',           _('Scroll down')),
            ('Alt+Shift+Down',      _('Extend rectangular selection to line down position')),
            ('Shift+Up',            _('Extend selection to line up position')),
            ('Ctrl+Up',             _('Scroll up')),
            ('Alt+Shift+Up',        _('Extend rectangular selection to line up position')),
            ('Ctrl+[',			    _('Go to previous paragraph')),
            ('Ctrl+Shift+[',		_('Extend selection to previous paragraph')),
            ('Ctrl+]',			    _('Go to next paragraph')),
            ('Ctrl+Shift+]',		_('Extend selection to next paragraph')),
            ('Shift+Left',		    _('Extend selection to previous character')),
            ('Ctrl+Left',		    _('Go to previous word')),
            ('Ctrl+Shift+Left',	    _('Extend selection to previous word')),
            ('Alt+Shift+Left',	    _('Extend rectangular selection to previous character')),
            ('Shift+Right',		    _('Extend selection to next character')),
            ('Ctrl+Right',		    _('Go to next word')),
            ('Ctrl+Shift+Right',	_('Extend selection to next word')),
            ('Alt+Shift+Right',	    _('Extend rectangular selection to next character')),
            ('Ctrl+/',		        _('Go to previous word part')),
            ('Ctrl+Shift+/',		_('Extend selection to previous word part')),
            ('Ctrl+\\',		        _('Go to next word part')),
            ('Ctrl+Shift+\\',	    _('Extend selection to next word part')),
            ('Shift+Home', 		    _('Extend selection to start of line')),
            ('Ctrl+Home', 		    _('Go to start of document')),
            ('Ctrl+Shift+Home', 	_('Extend selection to start of document')),
            ('Alt+Home', 		    _('Go to start of line')),
            ('Alt+Shift+Home', 	    _('Extend selection to start of line')),
            ('Shift+End', 		    _('Extend selection to end of line')),
            ('Ctrl+End', 		    _('Go to end of document')),
            ('Ctrl+Shift+End', 	    _('Extend selection to end of document')),
            ('Alt+End', 		    _('Go to end of line')),
            ('Alt+Shift+End', 	    _('Extend selection to end of line')),
            ('Shift+PgUp',		    _('Extend selection to previous page')),
            ('Alt+Shift+PgUp',	    _('Extend rectangular selection to previous page')),
            ('Shift+PgDn',		    _('Extend selection to next page')),
            ('Alt+Shift+PgDn',	    _('Extend rectangular selection to next page')),
            ('Shift+Delete',        _('Cut')),
            ('Ctrl+Delete',         _('Delete to end of word')),
            ('Ctrl+Shift+Delete',   _('Delete to end of line')),
            ('Shift+Insert',  	    _('Paste')),
            ('Ctrl+Insert',  	    _('Copy')),
            ('Shift+Backspace',	    _('Delete back')),
            ('Ctrl+Backspace',      _('Delete to start of word')),
            ('Alt+Backspace',       _('Undo')),
            ('Ctrl+Shift+Backspace',_('Delete to start of line')),
            ('Ctrl+Z', 			    _('Undo')),
            ('Ctrl+Y', 			    _('Redo')),
            ('Ctrl+X', 			    _('Cut')),
            ('Ctrl+C', 			    _('Copy')),
            ('Ctrl+V', 			    _('Paste')),
            ('Ctrl+A', 			    _('Select all')),
            ('Escape',              _('Cancel autocomplete or calltip')),
            ('Tab',		            _('Indent selection')),
            ('Shift+Tab',		    _('Unindent selection')),
            ('Shift+Return',        _('Newline')),
            ('Ctrl+Numpad +', 	    _('Zoom in')),
            ('Ctrl+Numpad -', 	    _('Zoom out')),
            ('Ctrl+Numpad /', 	    _('Reset zoom level to normal')),
            ('Ctrl+L', 			    _('Line cut')),
            ('Ctrl+Shift+L', 	    _('Line delete')),
            ('Ctrl+Shift+T', 	    _('Line copy')),
            ('Ctrl+T', 			    _('Transpose line with the previous')),
            ('Ctrl+D', 			    _('Line or selection duplicate')),
            ('Ctrl+U', 			    _('Convert selection to lowercase')),
            ('Ctrl+Shift+U', 	    _('Convert selection to uppercase')),
            (
            ('Edit -> Indent selection', 'Tab'),
            ('Edit -> Unindent selection', 'Shift+Tab'),
            ('Edit -> Undo', 'Ctrl+Z'),
            ('Edit -> Redo', 'Ctrl+Y'),
            ('Edit -> Cut', 'Ctrl+X'),
            ('Edit -> Copy', 'Ctrl+C'),
            ('Edit -> Paste', 'Ctrl+V'),
            ('Edit -> Select All', 'Ctrl+A'),
            ),
        ] 
        self.menuBookmark = self.createMenu(
            (
                (''), 
                (_('sort ascending'), '', self.UpdateBookmarkMenu, _('Sort bookmarks ascending'), wx.ITEM_CHECK, True),
                (_('show time'), '', self.UpdateBookmarkMenu, _('Show bookmarks with timecode'), wx.ITEM_CHECK, False),
                (_('show title'), '', self.UpdateBookmarkMenu, _('Show bookmarks with title'), wx.ITEM_CHECK, True),
            )
        )
        self.yuv2rgbDict = {
            _('Resolution-based'): 'auto',
            _('BT.709'): '709',
            _('BT.601'): '601',
            _('TV levels'): 'tv',
            _('PC levels'): 'pc',
            _('Progressive'): 'Progressive',
            _('Interlaced'): 'Interlaced',
            _('Swap UV'): 'swapuv',
        }
        reverseMatrixDict = dict([(v,k) for k,v in self.yuv2rgbDict.items()])
        self.zoomLabelDict = {
            _('25%'): '25',
            _('50%'): '50',
            _('100% (normal)'): '100',
            _('200%'): '200',
            _('300%'): '300',
            _('400%'): '400',
            _('Fill window'): 'fill',
            _('Fit inside window'): 'fit',
        }
        reverseZoomLabelDict = dict([(v,k) for k,v in self.zoomLabelDict.items()])
        self.flipLabelDict = {
            _('Vertically'): 'flipvertical',
            _('Horizontally'): 'fliphorizontal',
        }
        self.backgroundLabelDict = {
            _('Black'): (0, 0, 0),
            _('Dark grey'): (63, 63, 63),
            _('Medium grey'): (127, 127, 127),
            _('Light grey'): (191, 191, 191),
            _('White'): (255, 255, 255),
        }
        self.backgroundColorDict = dict([(v,k) for k,v in self.backgroundLabelDict.items()])
        return (
            (_('&File'),
                (_('New tab'), 'Ctrl+N', self.OnMenuFileNew, _('Create a new tab')),
                (_('Open...'), 'Ctrl+O', self.OnMenuFileOpen, _('Open an existing script')),
                (_('Undo close tab'), 'Ctrl+Shift+N', self.OnMenuFileUndoCloseTab, _('Reopen the last closed tab')),
                (_('Close tab'), 'Ctrl+W', self.OnMenuFileClose, _('Close the current tab')),
                (_('Close all tabs'), 'Ctrl+Shift+W', self.OnMenuFileCloseAllTabs, _('Close every tab')),
                (_('Rename tab'), '', self.OnMenuFileRenameTab, _('Rename the current tab. If script file is existing, also rename it')),
                (_('Save script'), 'Ctrl+S', self.OnMenuFileSaveScript, _('Save the current script')),
                (_('Save script as...'), 'Ctrl+Shift+S', self.OnMenuFileSaveScriptAs, _('Choose where to save the current script')),
                (_('Reload script'), 'Ctrl+F5', self.OnMenuFileReloadScript, _('Reopen the current script file if it has changed')),
                (_("Open script's directory"), '', self.OnMenuFileOpenScriptDirectory, _('If the current script is saved to a file, open its directory')),
                (_('Export HTML'), '', self.OnMenuFileExportHTML, _('Save the current script as a HTML document')),
                (_('&Print script'),
                    (
                    (_('Page setup'), '', self.OnMenuFilePageSetup, _('Configure page for printing')),
                    (_('Print header'), '', self.OnMenuFilePrintHeader, _('Include the script filename and page number at the top of each page'), wx.ITEM_CHECK, True),
                    (_('Wrap text'), '', self.OnMenuFileWrapText, _('Word-wrap long lines'), wx.ITEM_CHECK,  True),
                    (_('Use zoom'), '', self.OnMenuFileUseZoom, _('Apply the current zoom to the output'), wx.ITEM_CHECK,  False),
                    (_('Print preview'), '', self.OnMenuFilePrintPreview, _('Display print preview')),
                    (_('&Print'), 'Ctrl+P', self.OnMenuFilePrint, _('Print to printer or file')),
                    ),
                ),
                (''),
                (_('Load session...'), 'Alt+O', self.OnMenuFileLoadSession, _('Load a session into the tabs')),
                (_('Save session...'), 'Alt+S', self.OnMenuFileSaveSession, _('Save all the scripts as a session, including slider info')),
                (_('Backup current session'), 'Alt+B', self.OnMenuFileBackupSession, _('Backup the current session for next program run')),
                (''),
                #~ (_('Export filter customizations...'), '', self.OnMenuFileExportFilters, _('Export filter customizations for sharing purposes')),
                #~ (_('Import filter customizations...'), '', self.OnMenuFileImportFilters, _('Import filter customizations from an exported file')),
                #~ (''),
                (_('Next tab'), 'Ctrl+Tab', self.OnMenuFileNextTab, _('Switch to next script tab')),
                (_('Previous tab'), 'Ctrl+Shift+Tab', self.OnMenuFilePrevTab, _('Switch to previous script tab')),
                (''),
                (_('Toggle scrap window'), 'Ctrl+Shift+P', self.OnMenuEditShowScrapWindow, _('Show the scrap window')),
                (''),
                (''),
                (_('&Exit'), 'Alt+X', self.OnMenuFileExit, _('Exit the program')),
            ),
            (_('&Edit'),
                (_('Undo'), 'Ctrl+Z', self.OnMenuEditUndo, _('Undo last text operation')),
                (_('Redo'), 'Ctrl+Y', self.OnMenuEditRedo, _('Redo last text operation')),
                (''),
                (_('Cut'), 'Ctrl+X', self.OnMenuEditCut, _('Cut the selected text')),
                (_('Copy'), 'Ctrl+C', self.OnMenuEditCopy, _('Copy the selected text')),
                (_('Paste'), 'Ctrl+V', self.OnMenuEditPaste, _('Paste the selected text')),
                (''),
                (_('Find...'), 'Ctrl+F', self.OnMenuEditFind, _('Open a find text dialog box')),
                (_('Find next'), 'F3', self.OnMenuEditFindNext, _('Find the next instance of given text')),
                (_('Find previous'), 'Shift+F3', self.OnMenuEditFindPrevious, _('Find the previous instance of given text')),
                (_('Replace...'), 'Ctrl+H', self.OnMenuEditReplace, _('Open a replace text dialog box')),
                (_('Replace next'), 'F4', self.OnMenuEditReplaceNext, _('Replace the next instance of given text')),
                (''),
                (_('Select All'), 'Ctrl+A', self.OnMenuEditSelectAll, _('Select all the text')),
                (''),
                (_('&Insert'),
                    (
                    (_('Insert snippet'), 'F7', self.OnMenuEditInsertSnippet, _('Expand a snippet tag, or select a snippet from the list')),
                    (''),
                    (_('Insert source...'), 'F9', self.OnMenuEditInsertSource, _('Choose a source file to insert into the text')),
                    (_('Insert filename...'), 'Shift+F9', self.OnMenuEditInsertFilename, _('Get a filename from a dialog box to insert into the text')),
                    (_('Insert plugin...'), 'F10', self.OnMenuEditInsertPlugin, _('Choose a plugin file to insert into the text')),
                    (''),
                    (_('Insert user slider...'), 'F12', self.OnMenuEditInsertUserSlider, _('Insert a user-scripted slider into the text')),
                    (_('Insert user slider separator'), 'Shift+F12', self.OnMenuEditInsertUserSliderSeparator, _('Insert a tag which indicates a separator in the user slider window')),
                    (''),
                    (_('Insert frame #'), 'F11', self.OnMenuEditInsertFrameNumber, _('Insert the current frame number into the text')),
                    (''),
                    (_('Tag selection for toggling'), 'Ctrl+T', self.OnMenuEditToggleTagSelection, _('Add tags surrounding the selected text for toggling with the video preview')),
                    (_('Clear all tags'), 'Ctrl+Shift+T', self.OnMenuEditClearToggleTags, _('Clear all toggle tags from the text')),
                    ),
                ),
                (''),
                (_('Indent selection'), 'Tab', self.OnMenuEditIndentSelection, _('Indent the selected lines')),
                (_('Unindent selection'), 'Shift+Tab', self.OnMenuEditUnIndentSelection, _('Unindent the selected lines')),
                (_('Block comment'), 'Ctrl+Q', self.OnMenuEditBlockComment, _('Comment or uncomment selected lines')),
                (_('Style comment'), 'Alt+Q', self.OnMenuEditStyleComment, _('Comment at start of a text style or uncomment')),
                (_('Toggle current fold'), '', self.OnMenuEditToggleCurrentFold, _('Toggle the fold point On/OFF at the current line')),
                (_('Toggle all folds'), '', self.OnMenuEditToggleAllFolds, _('Toggle all fold points On/OFF')),
                (''),
                (_('&AviSynth function'),
                    (
                    (_('Autocomplete'), 'Ctrl+Space', self.OnMenuEditAutocomplete, _('Show list of filternames matching the partial text at the cursor')),
                    (_('Autocomplete all'), 'Alt+Space', self.OnMenuEditAutocompleteAll, _("Disregard user's setting, show full list of filternames matching the partial text at the cursor")),
                    (_('Autocomplete parameter/filename'), 'Ctrl+Alt+Space', self.OnMenuEditAutocompleteParameterFilename, _("If the first characters typed match a parameter name, complete it. If they're typed on a string, complete the filename")),
                    (_('Show calltip'), 'Ctrl+Shift+Space', self.OnMenuEditShowCalltip, _('Show the calltip for the filter (only works if cursor within the arguments)')),
                    (_('Show function definition'), 'Ctrl+Shift+D', self.OnMenuEditShowFunctionDefinition, _('Show the AviSynth function definition dialog for the filter')),
                    (_('Filter help file'), 'Shift+F1', self.OnMenuEditFilterHelp, _("Run the help file for the filter (only works if cursor within the arguments or name is highlighted)")),
                    (_('Parse script for function definitions'), 'Ctrl+Alt+F5', self.OnMenuEditParseFunctions, _('Include functions defined in the current script in the filter database, only for this tab')),
                    ),
                ),
                (''),
                (_('&Miscellaneous'),
                    (
                    (_('Move line up'), 'Ctrl+Shift+Up', self.OnMenuEditMoveLineUp, _('Move the current line or selection up by one line')),
                    (_('Move line down'), 'Ctrl+Shift+Down', self.OnMenuEditMoveLineDown, _('Move the current line or selection down by one line')),
                    (''),
                    (_('Copy unmarked script to clipboard'), 'Ctrl+Shift+C', self.OnMenuCopyUnmarkedScript, _('Copy the current script without any AvsP markings (user-sliders, toggle tags) to the clipboard')),
                    (_('Copy avisynth error to clipboard'), '', self.OnMenuCopyAvisynthError, _('Copy the avisynth error message shown on the preview window to the clipboard')),
                    #~(_('Copy status bar to clipboard'), '', self.OnMenuCopyStatusBar, _('Copy the message shown on the status bar to the clipboard')),
                    ),
                ),
            ),
            (_('&Video'),
                (_('Add/Remove bookmark'), 'Ctrl+B', self.OnMenuVideoBookmark, _('Mark the current frame on the frame slider')),
                (_('Clear all bookmarks'), '', self.OnMenuVideoGotoClearAll, _('Clear all bookmarks')),
                (_('Titled &bookmarks'),
                    (
                    (_('Move titled bookmark'), 'Ctrl+M', self.OnMenuVideoBookmarkMoveTitle, _('Move the nearest titled bookmark to the current position. A historic title will be restored if it matches the condition.')),
                    (_('Restore historic titles'), '', self.OnMenuVideoBookmarkRestoreHistory, _('Restore all historic titles')),
                    (_('Clear historic titles'), '', self.OnMenuVideoBookmarkClearHistory, _('Clear all historic titles')),
                    (_('Set title (auto)'), '', self.OnMenuVideoBookmarkAutoTitle, _("Generate titles for untitled bookmarks by the pattern - 'Chapter %02d'")),
                    (_('Set title (manual)'), '', self.OnMenuVideoBookmarkSetTitle, _('Edit title for bookmarks in a list table')),
                    ),
                ),
                (''),
                (_('Add tab to group'), 
                    (
                    (_('None'), '', self.OnMenuVideoGroupAssignTabGroup, _('Not include this tab on any group'), wx.ITEM_RADIO, True),
                    ('1', '', self.OnMenuVideoGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                    ('2', '', self.OnMenuVideoGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                    ('3', '', self.OnMenuVideoGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                    ('4', '', self.OnMenuVideoGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                    ('5', '', self.OnMenuVideoGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                    ('6', '', self.OnMenuVideoGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                    ('7', '', self.OnMenuVideoGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                    ('8', '', self.OnMenuVideoGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                    (''),
                    (_('Clear current tab group'), '', self.OnMenuVideoGroupClearTabGroup, _('Clear current tab group')),
                    (_('Clear all tab groups'), '', self.OnMenuVideoGroupClearAllTabGroups, _('Clear all tab groups')),
                    (''),
                    (_('Apply offsets'), '', self.OnMenuVideoGroupApplyOffsets, 
                        _('Use the difference between showed frames when the tabs were added to the group as offsets'), 
                        wx.ITEM_CHECK, self.options['applygroupoffsets']),
                    (_('Offset also bookmarks'), '', self.OnMenuVideoGroupOffsetBookmarks, 
                        _('Apply the offset also to the currently set bookmarks'), 
                        wx.ITEM_CHECK, self.options['offsetbookmarks']),
                    ),
                ),
                (_('&Navigate'),
                    (
                    (_('Go to &bookmark'), self.menuBookmark, -1),
                    (_('Next bookmark'), 'F2', self.OnMenuVideoGotoNextBookmark, _('Go to next bookmarked frame')),
                    (_('Previous bookmark'), 'Shift+F2', self.OnMenuVideoGotoPreviousBookmark, _('Go to previous bookmarked frame')),
                    (''),
                    (_('Forward 1 frame'), 'Right', self.OnMenuVideoNextFrame, _('Show next video frame (keyboard shortcut active when video window focused)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (_('Backward 1 frame'), 'Left', self.OnMenuVideoPrevFrame, _('Show previous video frame (keyboard shortcut active when video window focused)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (_('Forward 1 second'), 'Down', self.OnMenuVideoNextSecond, _('Show video 1 second forward (keyboard shortcut active when video window focused)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (_('Backward 1 second'), 'Up', self.OnMenuVideoPrevSecond, _('Show video 1 second back (keyboard shortcut active when video window focused)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (_('Forward 1 minute'), 'PgDn', self.OnMenuVideoNextMinute, _('Show video 1 minute forward (keyboard shortcut active when video window focused)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (_('Backward 1 minute'), 'PgUp', self.OnMenuVideoPrevMinute, _('Show video 1 minute back (keyboard shortcut active when video window focused)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (''),
                    (_('Forward x units'), '', self.OnMenuVideoNextCustomUnit, _('Jump forward by x units (you can specify x in the options dialog)')),
                    (_('Backwards x units'), '', self.OnMenuVideoPrevCustomUnit, _('Jump backwards by x units (you can specify x in the options dialog)')),
                    (''),
                    (_('Go to first frame'), '', self.OnMenuVideoFirstFrame, _('Go to first video frame (keyboard shortcut active when video window focused)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (_('Go to last frame'), '', self.OnMenuVideoLastFrame, _('Go to last video frame (keyboard shortcut active when video window focused)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (''),
                    (_('Last scrolled frame'), 'F8', self.OnMenuVideoGotoLastScrolled, _('Go to last scrolled frame')),
                    (''),
                    (_('Go to frame...'), 'Ctrl+G', self.OnMenuVideoGoto, _('Enter a video frame or time to jump to')),
                    ),
                ),
                (_('&Play video'),
                    (
                    (_('Play/pause video'), 'Ctrl+R', self.OnMenuVideoPlay, _('Play/pause video')),
                    (''),
                    (_('Increment speed'), 'Shift+Numpad +', self.OnMenuVideoPlayIncrement, _('Double the current playback speed')),
                    (_('Decrement speed'), 'Shift+Numpad -', self.OnMenuVideoPlayDecrement, _('Halve the current playback speed')),
                    (_('Normal speed'), 'Shift+Numpad /', self.OnMenuVideoPlayNormal, _('Set the playback speed to the script frame rate')),
                    (_('Maximum speed'), 'Shift+Numpad *', self.OnMenuVideoPlayMax, _('Play the video as fast as possible without dropping frames')),
                    (''),
                    (_('Drop frames'), 'Shift+Numpad .', self.OnMenuVideoPlayDropFrames, _('Maintain correct video speed by skipping frames'), wx.ITEM_CHECK, True),
                    ),
                ),
                (''),
                (_('Crop editor...'), '', self.OnMenuVideoCropEditor, _('Show the crop editor dialog')),
                (_('&Trim selection editor'),
                    (
                    (_('Show trim selection editor'), '', self.OnMenuVideoTrimEditor, _('Show the trim selection editor dialog')),
                    (''),
                    (_('Set selection startpoint'), 'Home', self.OnMenuVideoTrimEditorSetStartpoint, _('Set a selection startpoint (shows the trim editor if not visible)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (_('Set selection endpoint'), 'End', self.OnMenuVideoTrimEditorSetEndpoint, _('Set a selection endpoint (shows the trim editor if not visible)'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (''),
                    (_('Move selections before the current frame'), 'Ctrl+Alt+V', self.OnMenuVideoMoveSelectionsBeforeCurrentFrame, _('The current selections are cut from the timeline and inserted before the current frame. Bookmarks are shifted accordingly.'), wx.ITEM_NORMAL, None, self.videoWindow),
                    (_('Move selections after the current frame'), 'Ctrl+V', self.OnMenuVideoMoveSelectionsAfterCurrentFrame, _('The current selections are cut from the timeline and inserted after the current frame. Bookmarks are shifted accordingly.'), wx.ITEM_NORMAL, None, self.videoWindow),
                    ),
                ),
                (''),
                (_('&Zoom'),
                    (
                    (reverseZoomLabelDict['25'], '', self.OnMenuVideoZoom, _('Zoom video preview to 25%'), wx.ITEM_RADIO, False),
                    (reverseZoomLabelDict['50'], '', self.OnMenuVideoZoom, _('Zoom video preview to 50%'), wx.ITEM_RADIO, False),
                    (reverseZoomLabelDict['100'], 'Numpad /', self.OnMenuVideoZoom, _('Zoom video preview to 100% (normal)'), wx.ITEM_RADIO, True),
                    (reverseZoomLabelDict['200'], '', self.OnMenuVideoZoom, _('Zoom video preview to 200%'), wx.ITEM_RADIO, False),
                    (reverseZoomLabelDict['300'], '', self.OnMenuVideoZoom, _('Zoom video preview to 300%'), wx.ITEM_RADIO, False),
                    (reverseZoomLabelDict['400'], '', self.OnMenuVideoZoom, _('Zoom video preview to 400%'), wx.ITEM_RADIO, False),
                    (reverseZoomLabelDict['fill'], '', self.OnMenuVideoZoom, _('Zoom video preview to fill the entire window'), wx.ITEM_RADIO, False),
                    (reverseZoomLabelDict['fit'], '', self.OnMenuVideoZoom, _('Zoom video preview to fit inside the window'), wx.ITEM_RADIO, False),
                    (''),
                    (_('Zoom in'), 'Numpad +', self.OnZoomInOut, _("Enlarge preview image to next zoom level. Not work under 'Fill window' or 'Fit inside window'")),
                    (_('Zoom out'), 'Numpad -', self.OnZoomInOut, _("Shrink preview image to previous zoom level. Not work under 'Fill window' or 'Fit inside window'")),
                    ),
                ),
                (_('&Flip'),
                    (
                    (_('Vertically'), '', self.OnMenuVideoFlip, _('Flip video preview upside down'), wx.ITEM_CHECK, False),
                    (_('Horizontally'), '', self.OnMenuVideoFlip, _('Flip video preview from left to right'), wx.ITEM_CHECK, False),
                    ),
                ),
                (_('&YUV -> RGB'),
                    (
                    (reverseMatrixDict['swapuv'], '', self.OnMenuVideoYUV2RGB, _('Swap chroma channels (U and V)'), wx.ITEM_CHECK, False),
                    (''),
                    (reverseMatrixDict['auto'], '', self.OnMenuVideoYUV2RGB, _('Use BT.709 coefficients for HD, BT.601 for SD (default)'), wx.ITEM_RADIO, True),
                    (reverseMatrixDict['709'], '', self.OnMenuVideoYUV2RGB, _('Use BT.709 coefficients'), wx.ITEM_RADIO, False),
                    (reverseMatrixDict['601'], '', self.OnMenuVideoYUV2RGB, _('Use BT.601 coefficients'), wx.ITEM_RADIO, False),
                    (''),
                    (reverseMatrixDict['tv'], '', self.OnMenuVideoYUV2RGB, _('Use limited range (default)'), wx.ITEM_RADIO, True),
                    (reverseMatrixDict['pc'], '', self.OnMenuVideoYUV2RGB, _('Use full range'), wx.ITEM_RADIO, False),
                    (''),
                    (reverseMatrixDict['Progressive'], '', self.OnMenuVideoYUV2RGB, _('For YV12 only, assume it is progressive (default)'), wx.ITEM_RADIO, True),
                    (reverseMatrixDict['Interlaced'], '', self.OnMenuVideoYUV2RGB, _('For YV12 only, assume it is interlaced'), wx.ITEM_RADIO, False),
                    ),
                ),
                (_('Bith &depth'),
                    (
                    (_('8-bit'), '', self.OnMenuVideoBitDepth, _('Regular 8-bit depth (default)'), wx.ITEM_RADIO, True),
                    (_('Stacked yuv420p10 or yuv444p10'), '', self.OnMenuVideoBitDepth, _('Stacked 16-bit, MSB on top, range reduced to 10-bit. Requires MaskTools v2 loaded'), wx.ITEM_RADIO, False),
                    (_('Stacked yuv420p16 or yuv444p16'), '', self.OnMenuVideoBitDepth, _('Stacked 16-bit, MSB on top'), wx.ITEM_RADIO, False),
                    (_('Interleaved yuv420p10 or yuv444p10'), '', self.OnMenuVideoBitDepth, _('Interleaved 16-bit (little-endian), range reduced to 10-bit. Requires MaskTools v2 loaded'), wx.ITEM_RADIO, False),
                    (_('Interleaved yuv420p16 or yuv444p16'), '', self.OnMenuVideoBitDepth, _('Interleaved 16-bit (little-endian)'), wx.ITEM_RADIO, False),
                    #(_('Interleaved RGB48'), '', self.OnMenuVideoBitDepth, _('16-bit RGB conveyed on YV12'), wx.ITEM_RADIO, False),
                    ),
                ),
                (_('Background &color'),
                    (
                    (_('Default'), '', self.OnMenuVideoBackgroundColor, _("Follow current theme"), wx.ITEM_RADIO, True),
                    (_('Black'), '', self.OnMenuVideoBackgroundColor, _('Use RGB {hex_value}').format(hex_value='#000000'), wx.ITEM_RADIO, False),
                    (_('Dark grey'), '', self.OnMenuVideoBackgroundColor, _('Use RGB {hex_value}').format(hex_value='#3F3F3F'), wx.ITEM_RADIO, False),
                    (_('Medium grey'), '', self.OnMenuVideoBackgroundColor, _('Use RGB {hex_value}').format(hex_value='#7F7F7F'), wx.ITEM_RADIO, False),
                    (_('Light grey'), '', self.OnMenuVideoBackgroundColor, _('Use RGB {hex_value}').format(hex_value='#BFBFBF'), wx.ITEM_RADIO, False),
                    (_('White'), '', self.OnMenuVideoBackgroundColor, _('Use RGB {hex_value}').format(hex_value='#FFFFFF'), wx.ITEM_RADIO, False),
                    (_('Custom'), '', self.OnMenuVideoBackgroundColor, _('Use a custom color'), wx.ITEM_RADIO, False),
                    (''),
                    (_('Select custom color'), '', self.OnMenuVideoSetCustomBackgroundColor, _("Choose the color used if 'custom' is selected")),
                    ),
                ),
                (_('Keep variables on refreshing'), '', self.OnMenuVideoReuseEnvironment, _('Create the new AviSynth clip on the same environment. Useful for tweaking parameters'), wx.ITEM_CHECK, False),
                (''),
                (_('Save image as...'), '', self.OnMenuVideoSaveImage, _('Save the current frame as a bitmap')),
                (_('Quick save image'), '', self.OnMenuVideoQuickSaveImage, _('Save the current frame as a bitmap with a default filename, overwriting the file if already exists')),
                (_('Copy image to clipboard'), '', self.OnMenuVideoCopyImageClipboard, _('Copy the current frame to the clipboard as a bitmap')),
                (''),
                (_('Refresh preview'), 'F5', self.OnMenuVideoRefresh, _('Force the script to reload and refresh the video frame')),
                (_('Show/Hide the preview'), 'Shift+F5', self.OnMenuVideoToggle, _('Toggle the video preview')),
                (_('Toggle preview placement'), '', self.OnMenuVideoTogglePlacement, _('When not using a separate window for the video preview, toggle between showing it at the bottom (default) or to the right')),
                (_('Release all videos from memory'), '', self.OnMenuVideoReleaseMemory, _('Release all open videos from memory')),
                (_('Switch video/text focus'), 'Escape', self.OnMenuVideoSwitchMode, _('Switch focus between the video preview and the text editor')),
                (_('Toggle the slider sidebar'), 'Alt+F5', self.OnMenuVideoToggleSliderWindow, _('Show/hide the slider sidebar (double-click the divider for the same effect)')),
                (_('Run analysis pass'), '', self.OnMenuVideoRunAnalysisPass, _('Request every video frame once (analysis pass for two-pass filters)')),
                (_('External player'), 'F6', self.OnMenuVideoExternalPlayer, _('Play the current script in an external program')),
                (''),
                (_('Video information'), '', self.OnMenuVideoInfo, _('Show information about the video in a dialog box')),
            ),
            (_('&Options'),
                (_('Always on top'), '', self.OnMenuOptionsAlwaysOnTop, _('Keep this window always on top of others'), wx.ITEM_CHECK, self.options['alwaysontop']),
                (_('Video preview always on top'), '', self.OnMenuOptionsPreviewAlwaysOnTop, _('If the video preview is detached, keep it always on top of other windows'), wx.ITEM_CHECK, self.options['previewalwaysontop']),
                #~(_('Only allow a single instance'), '', self.OnMenuOptionsSingleInstance, _('Only allow a single instance of AvsP'), wx.ITEM_CHECK, self.options['singleinstance']),
                #~(_('Use monospaced font'), '', self.OnMenuOptionsMonospaceFont, _('Override all fonts to use a specified monospace font'), wx.ITEM_CHECK, self.options['usemonospacedfont']),
                (_('Disable video preview'), '', self.OnMenuOptionsDisablePreview, _('If checked, the video preview will not be shown under any circumstances'), wx.ITEM_CHECK, self.options['disablepreview']),
                #~(_('Enable paranoia mode'), '', self.OnMenuOptionsEnableParanoiaMode, _('If checked, the current session is backed up prior to previewing any new script'), wx.ITEM_CHECK, self.options['paranoiamode']),
                #~(_('Enable line-by-line update'), '', self.OnMenuOptionsEnableLineByLineUpdate, _('Enable the line-by-line video update mode (update every time the cursor changes line position)'), wx.ITEM_CHECK, self.options['autoupdatevideo']),
                (''),
                (_('Associate .avs files with AvsP'), '', self.OnMenuOptionsAssociate, _('Configure this computer to open .avs files with AvsP when double-clicked. Run again to disassociate')),
                (''),
                (_('AviSynth function definition...'), '', self.OnMenuOptionsFilters, _('Add or override AviSynth functions in the database')),
                #~ (_('AviSynth function definition...'), '', self.OnMenuOptionsFilters, _('Edit the AviSynth function info for syntax highlighting and calltips')),
                (_('Fonts and colors...'), '', self.OnMenuOptionsFontsAndColors, _('Edit the various AviSynth script fonts and colors')),
                (_('Extension templates...'), '', self.OnMenuOptionsTemplates, _('Edit the extension-based templates for inserting sources')),
                (_('Snippets...'), '', self.OnMenuOptionsSnippets, _('Edit insertable text snippets')),
                (''),
                (_('Keyboard shortcuts...'), '', self.OnMenuConfigureShortcuts, _('Configure the program keyboard shortcuts')),
                (_('Program settings...'), '', self.OnMenuOptionsSettings, _('Configure program settings')),
            ),
            (_('&Help'),
                (_('Animated tutorial'), '', self.OnMenuHelpAnimatedTutorial, _('View an animated tutorial for AvsP (from the AvsP website)')),
                (''),
                (_('Text features'), '', self.OnMenuHelpTextFeatures, _('Learn more about AvsP text features (from the AvsP website)')),
                (_('Video features'), '', self.OnMenuHelpVideoFeatures, _('Learn more about AvsP video features (from the AvsP website)')),
                (_('User sliders'), '', self.OnMenuHelpUserSliderFeatures, _('Learn more about AvsP user sliders (from the AvsP website)')),
                (_('Macros'), '', self.OnMenuHelpMacroFeatures, _('Learn more about AvsP macros (from the AvsP website)')),
                (''),
                (_('Avisynth help'), 'F1', self.OnMenuHelpAvisynth, _('Open the avisynth help html')),
                (_('Open Avisynth plugins folder'), '', self.OnMenuHelpAvisynthPlugins, _('Open the avisynth plugins folder, or the last folder from which a plugin was loaded')),
                (''),
                (_('Changelog'), '', self.OnMenuHelpChangelog, _('Open the changelog file')),
                (_('About AvsPmod'), '', self.OnMenuHelpAbout, _('About this program')),
            ),
        )

    def buttonInfo(self):
        bmpPlay = play_icon.getImage()
        bmpPause = pause_icon.getImage()
        bmpExternal = external_icon.getImage()
        bmpRight = next_icon.getImage()
        bmpSkipRight = skip_icon.getImage()
        if not self.options['largeui']:
            bmpPlay = bmpPlay.Scale(16,16)
            bmpPause = bmpPause.Scale(16,16)
            bmpExternal = bmpExternal.Scale(16,16)
            bmpRight = bmpRight.Scale(16,16)
            bmpSkipRight = bmpSkipRight.Scale(16,16)
        self.bmpPlay = wx.BitmapFromImage(bmpPlay)
        self.bmpPause = wx.BitmapFromImage(bmpPause)
        bmpExternal = wx.BitmapFromImage(bmpExternal)
        self.bmpRightTriangle = spin_icon.GetBitmap() #wx.BitmapFromImage(play_icon.getImage().Scale(10,10))
        self.bmpLeftTriangle = self.bmpRightTriangle.ConvertToImage().Mirror().ConvertToBitmap()
        bmpRight = wx.BitmapFromImage(bmpRight)
        bmpLeft = bmpRight.ConvertToImage().Mirror().ConvertToBitmap()
        self.bmpVidUp = self.bmpPlay.ConvertToImage().Rotate90(False).ConvertToBitmap()
        self.bmpVidDown = self.bmpPlay.ConvertToImage().Rotate90().ConvertToBitmap()
        bmpSkipRight = wx.BitmapFromImage(bmpSkipRight)
        bmpSkipLeft = bmpSkipRight.ConvertToImage().Mirror().ConvertToBitmap()

        return (
            (self.bmpVidUp, self.OnMenuVideoToggle, _('Toggle the video preview')),
            (bmpSkipLeft, self.OnMenuVideoGotoPreviousBookmark,_('Previous bookmark')),
            (bmpLeft, self.OnMenuVideoPrevFrame, _('Previous frame')),
            (bmpRight, self.OnMenuVideoNextFrame, _('Next frame')),
            (bmpSkipRight, self.OnMenuVideoGotoNextBookmark,_('Next bookmark')),
            (self.bmpPlay, self.OnMenuVideoPlay, _('Play/pause video')),
            (bmpExternal, self.OnMenuVideoExternalPlayer, _('Run the script with an external program')),
        )

    def createToolsMenu(self, shortcutList, oldShortcuts):
        menuInfo = []
        self.toolsImportNames = {}
        appendedList = ['toolsmenu']
        # First add items defined by ToolsMenu.py
        try:
            items = __import__('ToolsMenu').menuInfo
        except ImportError:
            items = []
        for item in items:
            if len(item) == 3:
                importName, menuLabel, statusString = item
                id = wx.NewId()
                self.toolsImportNames[id] = importName
                appendedList.append(importName.lower())
                menuInfo.append((menuLabel, '', self.OnMenuToolsRunSelected, statusString, id))
            else:
                menuInfo.append('')
        baseSize = len(menuInfo)
        # Then add any additional python files
        if os.path.isdir(self.toolsfolder):
            namelist = os.listdir(self.toolsfolder)
            namelist.sort()
            for name in namelist:
                root, ext = os.path.splitext(name)
                if ext.lower().startswith('.py') and root.lower() not in appendedList:
                    f = open(os.path.join(self.toolsfolder, name))
                    text = f.read()
                    f.close()
                    if not re.findall(r'\bdef\s+avsp_run\s*\(\):', text):
                        continue
                    splitroot = root.split(']',1)
                    if len(splitroot) == 2 and root.startswith('['):
                        menuLabel = splitroot[1].strip()
                    else:
                        menuLabel = root
                    if len(menuInfo) == baseSize:
                        menuInfo.append('')
                    if menuLabel.strip().startswith('---'):
                        menuInfo.append('')
                    else:
                        id = wx.NewId()
                        self.toolsImportNames[id] = root
                        appendedList.append(root.lower())
                        menuInfo.append((menuLabel, '', self.OnMenuToolsRunSelected, _('Run the selected tool'), id))
        if len(menuInfo) == 0:
            menuInfo.append((''))
        menu = self.createMenu(menuInfo, _('&Tools'), shortcutList, oldShortcuts)
        self.toolsMenuPos = 3
        self.GetMenuBar().Insert(self.toolsMenuPos, menu, _('&Tools'))

    def createMacroMenu(self, shortcutList, oldShortcuts):
        menuInfo = []
        self.macrosImportNames = {}
        self.macrosStack = []
        if os.path.isdir(self.macrofolder):
            def createMenuList(menuList, namelist, dirname):
                namelist.sort()
                for name in namelist:
                    fullname = os.path.join(dirname, name)
                    if os.path.isdir(fullname):
                        submenuList = []
                        createMenuList(submenuList, os.listdir(fullname), fullname)
                        if submenuList:
                            splitname = name.split(']',1)
                            if len(splitname) == 2 and name.startswith('['):
                                name = splitname[1].strip()
                            menuList.append((_(name), submenuList))
                for name in namelist:
                    fullname = os.path.join(dirname, name)
                    root, ext = os.path.splitext(name)
                    if ext.lower() == '.py':
                        splitroot = root.split(']',1)
                        if len(splitroot) == 2 and root.startswith('['):
                            root = splitroot[1].strip()
                        if root.strip().startswith('---'):
                            menuList.append('')
                        else:
                            id = wx.NewId()
                            self.macrosImportNames[id] = fullname
                            if root.strip().startswith('ccc'):
                                root = root.strip()[3:].strip()
                                if not root:
                                    root = self.getMacrosLabelFromFile(fullname)
                                menuList.append((_(root), '', self.OnMenuMacroRunSelected, _('A macro check item'), (wx.ITEM_CHECK, False, id)))
                            elif root.strip().startswith('CCC'):
                                root = root.strip()[3:].strip()
                                if not root:
                                    root = self.getMacrosLabelFromFile(fullname)
                                menuList.append((_(root), '', self.OnMenuMacroRunSelected, _('A macro check item'), (wx.ITEM_CHECK, True, id)))
                            elif root.strip().startswith('rrr'):
                                if not root:
                                    root = self.getMacrosLabelFromFile(fullname)
                                root = root.strip()[3:].strip()
                                menuList.append((_(root), '', self.OnMenuMacroRunSelected, _('A macro radio item'), (wx.ITEM_RADIO, False, id)))
                            elif root.strip().startswith('RRR'):
                                if not root:
                                    root = self.getMacrosLabelFromFile(fullname)
                                root = root.strip()[3:].strip()
                                menuList.append((_(root), '', self.OnMenuMacroRunSelected, _('A macro radio item'), (wx.ITEM_RADIO, True, id)))
                            else:
                                if not root:
                                    root = self.getMacrosLabelFromFile(fullname)
                                menuList.append((_(root), '', self.OnMenuMacroRunSelected, _('Run selected macro'), id))
            createMenuList(menuInfo, os.listdir(self.macrofolder), self.macrofolder)

            menuInfo.append((''))
            menuInfo.append(('macros_readme.txt', '', self.OnMenuMacrosReadme, _('View the readme for making macros')))
            menuInfo.append((_('Open macros folder'), '', self.OnMenuMacrosFolder, _('Open the macros folder')))
        else:
            menuInfo.append((''))
        menu = self.createMenu(menuInfo, _('&Macros'), shortcutList, oldShortcuts)
        self.macroMenuPos = 4
        self.GetMenuBar().Insert(self.macroMenuPos, menu, _('&Macros'))

    def createScriptNotebook(self):
        # Create the notebook
        
        class Notebook(wx.Notebook):
            
            def SetPageText(self, index, text):
                script = self.GetPage(index)
                if script.group is not None:
                    text = u'[{0}] {1}'.format(script.group, text)
                if script.GetModify():
                    text = '* ' + text
                return wx.Notebook.SetPageText(self, index, text)
            
            def GetPageText(self, index, full=False):
                text = wx.Notebook.GetPageText(self, index)
                if not full:
                    script = self.GetPage(index)
                    if script.GetModify():
                        text = text[2:]
                    if script.group is not None:
                        text = text[4:]
                return text
            
            def UpdatePageText(self, index):
                text = wx.Notebook.GetPageText(self, index)
                script = self.GetPage(index)
                if script.old_modified:
                    text = text[2:]
                if script.old_group != script.group:
                    if script.old_group is not None:
                        text = text[4:]
                    if script.group is not None:
                        text = u'[{0}] {1}'.format(script.group, text)
                modified = script.GetModify()
                if modified:
                    text = '* ' + text
                script.old_modified = modified
                script.old_group = script.group
                return wx.Notebook.SetPageText(self, index, text)
        
        style = wx.NO_BORDER
        if self.options['multilinetab']:
            style |= wx.NB_MULTILINE
        if self.options['fixedwidthtab']:
            style |= wx.NB_FIXEDWIDTH
        nb = Notebook(self.mainSplitter, wx.ID_ANY, style=style)
        nb.app = self
        # Create the right-click menu
        menuInfo = (
            (_('Close'), '', self.OnMenuFileClose),
            (_('Rename'), '', self.OnMenuFileRenameTab),
            (_('Group'), 
                (
                (_('None'), '', self.OnGroupAssignTabGroup, _('Not include this tab on any group'), wx.ITEM_RADIO, True),
                ('1', '', self.OnGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                ('2', '', self.OnGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                ('3', '', self.OnGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                ('4', '', self.OnGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                ('5', '', self.OnGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                ('6', '', self.OnGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                ('7', '', self.OnGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                ('8', '', self.OnGroupAssignTabGroup, _('Add tab to this group'), wx.ITEM_RADIO, False),
                (''),
                (_('Clear current tab group'), '', self.OnGroupClearTabGroup, _('Clear current tab group')),
                (_('Clear all tab groups'), '', self.OnGroupClearAllTabGroups, _('Clear all tab groups')),
                (''),
                (_('Apply offsets'), '', self.OnGroupApplyOffsets, 
                    _('Use the difference between showed frames when the tabs were added to the group as offsets'), 
                    wx.ITEM_CHECK, self.options['applygroupoffsets']),
                (_('Offset also bookmarks'), '', self.OnGroupOffsetBookmarks, 
                    _('Apply the offset also to the currently set bookmarks'), 
                    wx.ITEM_CHECK, self.options['offsetbookmarks']),
                ),
            ),
            (''),
            (_('Save'), '', self.OnMenuFileSaveScript),
            (_('Save as...'), '', self.OnMenuFileSaveScriptAs),
            (_('Reload'), '', self.OnMenuFileReloadScript),
            (_('Open directory'), '', self.OnMenuFileOpenScriptDirectory),
            (''),
            (_('Select all'), '', self.OnMenuEditSelectAll),
            (''),
            (_('Copy to new tab'), '', self.OnMenuEditCopyToNewTab),
            (_('Reposition to'), 
                (
                (''),
                ),
            ),
        )
        menu = self.createMenu(menuInfo)
        nb.contextMenu = menu
        nb.dragging = False
        if self.options['usetabimages']:
            color1 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR)
            #~ color1 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNSHADOW)
            color2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW)
            color3 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
            color4 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
            # Create the mask
            w = h = 15
            bmpMask = wx.EmptyBitmap(w, h)
            mdc = wx.MemoryDC()
            mdc.SelectObject(bmpMask)
            mdc.DrawRoundedRectangle(0,0,w,h,3)
            mdc = None
            mask = wx.Mask(bmpMask)
            # Create the bitmap
            bmpBase = wx.EmptyBitmap(w, h)
            bmpBase.SetMask(mask)
            mdc = wx.MemoryDC()
            mdc.SelectObject(bmpBase)
            mdc.SetBackground(wx.Brush(color1))
            mdc.Clear()
            mdc.SetPen(wx.Pen(color2))
            mdc.SetBrush(wx.Brush(color2))
            mdc.DrawPolygon([wx.Point(0,h), wx.Point(w,h), wx.Point(w,0)])
            mdc.SetPen(wx.Pen(color3))
            mdc.SetBrush(wx.Brush(color3))
            th = 3
            mdc.DrawRoundedRectangle(th,th,w-2*th,h-2*th,0)
            mdc = None
            imageBase = bmpBase.ConvertToImage()
            il = wx.ImageList(w, h)
            for i in xrange(10):
                bmp = wx.BitmapFromImage(imageBase)
                mdc = wx.MemoryDC()
                mdc.SelectObject(bmp)
                mdc.SetTextForeground(color4)
                #~ mdc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName='terminal'))
                #~ mdc.DrawText(str(i+1), 4,4)
                #~ mdc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName='verdana'))
                #~ mdc.DrawText(str(i+1), 4,0)
                mdc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName='courier new'))
                mdc.DrawText(str((i+1) % 10), 4,0)
                mdc = None
                il.Add(bmp)
            nb.AssignImageList(il)
        # Event binding
        nb.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDownNotebook)
        nb.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDownNotebook)
        nb.Bind(wx.EVT_LEFT_UP, self.OnLeftUpNotebook)
        nb.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClickNotebook)
        nb.Bind(wx.EVT_RIGHT_UP, self.OnRightClickNotebook)
        nb.Bind(wx.EVT_MOTION, self.OnMouseMotionNotebook)
        nb.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheelNotebook)
        return nb

    def createScriptWindow(self):
        # Create the instance of the window
        scriptWindow = AvsStyledTextCtrl(self.scriptNotebook, self, style=wx.STATIC_BORDER,
            #~ filterDict=self.optionsFilters,
            #~ filterPresetDict=self.options['filterpresets'],
            #~ keywordLists=self.optionsAvsKeywords,
            #~ autocomplete=self.options['autocomplete'],
            #~ autoparentheses=self.options['autoparentheses'],
            #~ usestringeol=self.options['usestringeol'],
            #~ calltips=self.options['calltips'],
            #~ frequentcalltips=self.options['frequentcalltips'],
            #~ usecustomlexer=True, #self.options['usecustomlexer'],
            #~ usetabs=self.options['usetabs'],
            #~ tabwidth=self.options['tabwidth'],
            #~ wrap=self.options['wrap'],
            #~ highlightline=self.options['highlightline'],
            #~ highlightlinecolor=self.options['highlightlinecolor'],
            #~ numlinechars=self.options['numlinechars'],
            #~ usemonospacedfont=self.options['usemonospacedfont'],
            #~ textstyles=self.options['textstyles'],
        )
        # Bind variables to the window instance
        scriptWindow.filename = ""
        scriptWindow.workdir = ""
        scriptWindow.encoding = 'latin1'
        scriptWindow.eol = None
        scriptWindow.AVI = None
        scriptWindow.display_clip_refresh_needed = False
        scriptWindow.previewtxt = []
        scriptWindow.sliderTexts = []
        scriptWindow.sliderProperties = []
        scriptWindow.toggleTags = []
        scriptWindow.autoSliderInfo = []
        scriptWindow.lastSplitVideoPos = None
        scriptWindow.lastSplitSliderPos = -300
        scriptWindow.userHidSliders = False
        scriptWindow.lastFramenum = 0
        scriptWindow.lastLength = None
        scriptWindow.group = None
        scriptWindow.group_frame = 0
        scriptWindow.old_group = None
        scriptWindow.old_modified = False
        scriptWindow.sliderWindowShown = not self.options['keepsliderwindowhidden']
        scriptWindow.autocrop_values = None
        try:
            #scriptWindow.contextMenu = self.GetMenuBar().GetMenu(1)
            scriptWindow.contextMenu = self.menuBackups[0] if self.menuBackups else self.GetMenuBar().GetMenu(1)
        except AttributeError:
            pass

        scriptWindow.sliderWindow = wx.ScrolledWindow(self.videoSplitter, wx.ID_ANY, style=wx.STATIC_BORDER|wx.TAB_TRAVERSAL)
        scriptWindow.sliderWindow.SetScrollRate(10, 10)
        scriptWindow.sliderSizer = wx.GridBagSizer(hgap=0, vgap=10)
        if wx.VERSION < (2, 9):
            scriptWindow.sliderSizer.AddGrowableCol(3)
        #~ scriptWindow.sliderSizerNew = wx.GridBagSizer(hgap=0, vgap=10)
        scriptWindow.sliderSizerNew = wx.GridBagSizer(hgap=0, vgap=0)
        if wx.VERSION < (2, 9):
            scriptWindow.sliderSizerNew.AddGrowableCol(3)
        scriptWindow.sliderSizerNew.SetEmptyCellSize((0,0)) 
        scriptWindow.toggleTagSizer = wx.BoxSizer(wx.VERTICAL)
        scriptWindow.videoSidebarSizer = wx.BoxSizer(wx.VERTICAL)
        scriptWindow.videoSidebarSizer.Add(scriptWindow.toggleTagSizer, 0, wx.TOP|wx.LEFT, 5)
        scriptWindow.videoSidebarSizer.Add(scriptWindow.sliderSizerNew, 0, wx.EXPAND|wx.LEFT, 5)
        scriptWindow.videoSidebarSizer.Add(scriptWindow.sliderSizer, 0, wx.EXPAND|wx.LEFT, 5)
        scriptWindow.sliderWindow.SetSizer(scriptWindow.videoSidebarSizer)
        scriptWindow.sliderWindow.Bind(wx.EVT_LEFT_DOWN, lambda event: self.videoWindow.SetFocus())
        scriptWindow.oldSliderTexts = []
        scriptWindow.oldAutoSliderInfo = []
        scriptWindow.oldToggleTags = []
        #~ scriptWindow.lastSplitVideoPos = None

        # Event binding
        scriptWindow.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        scriptWindow.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDownScriptWindow)
        scriptWindow.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUpScriptWindow)
        scriptWindow.Bind(wx.EVT_SET_FOCUS, self.OnFocusScriptWindow)
        scriptWindow.Bind(stc.EVT_STC_UPDATEUI, self.OnScriptTextChange)
        #~ scriptWindow.Bind(stc.EVT_STC_SAVEPOINTLEFT, self.OnScriptSavePointLeft)
        #~ scriptWindow.Bind(stc.EVT_STC_SAVEPOINTREACHED, self.OnScriptSavePointReached)
        scriptWindow.Bind(stc.EVT_STC_SAVEPOINTLEFT, lambda event: self.UpdateScriptTabname(event.GetEventObject()))
        scriptWindow.Bind(stc.EVT_STC_SAVEPOINTREACHED, lambda event: self.UpdateScriptTabname(event.GetEventObject()))
        scriptWindow.Bind(wx.EVT_KEY_UP, self.OnScriptKeyUp)
        # Drag-and-drop target
        scriptWindow.SetDropTarget(self.scriptDropTarget(scriptWindow, self))
        return scriptWindow

    def createVideoWindow(self, parent):
        videoWindow = wx.ScrolledWindow(parent, style=wx.STATIC_BORDER|wx.WANTS_CHARS)
        videoWindow.SetScrollRate(1, 1)
        try:
            #videoWindow.contextMenu = self.GetMenuBar().GetMenu(2)
            videoWindow.contextMenu = self.menuBackups[1] if self.menuBackups else self.GetMenuBar().GetMenu(2)
        except AttributeError:
            pass
        # Event binding
        videoWindow.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        videoWindow.Bind(wx.EVT_SET_FOCUS, self.OnFocusVideoWindow)
        videoWindow.Bind(wx.EVT_PAINT, self.OnPaintVideoWindow)
        videoWindow.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        videoWindow.Bind(wx.EVT_KEY_DOWN, self.OnKeyDownVideoWindow)
        videoWindow.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheelVideoWindow)
        videoWindow.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDownVideoWindow)
        videoWindow.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDownVideoWindow)
        videoWindow.Bind(wx.EVT_MOTION, self.OnMouseMotionVideoWindow)
        videoWindow.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeaveVideoWindow)
        videoWindow.Bind(wx.EVT_LEFT_UP, self.OnLeftUpVideoWindow)
        return videoWindow

    def createVideoControls(self, parent, primary=True):
        if wx.VERSION < (2, 9):
            height = 40 if self.options['largeui'] else 24
            panel = wx.Panel(parent, style=wx.BORDER_NONE, size=(-1, height))
        else:
            height = 46 if self.options['largeui'] else 30
            panel = wx.Panel(parent, size=(-1, height))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        videoControlWidgets = []
        # Create the playback buttons
        for bitmap, handler, statusTxt in self.buttonInfo():
            button = self.createToolbarButton(panel, bitmap, handler, statusTxt=statusTxt)
            if handler == self.OnMenuVideoToggle:
                if primary:
                    self.toggleButton = button
                else:
                    self.toggleButton2 = button
                    self.toggleButton2.SetBitmapLabel(self.bmpVidDown)
            elif handler == self.OnMenuVideoPlay:
                if primary:
                    self.play_button = button
                else:
                    self.play_button2 = button
            sizer.Add(button, 0, wx.ALIGN_CENTER_VERTICAL)#, wx.EXPAND)#, wx.ALIGN_BOTTOM)#, wx.ALL, 1)
            videoControlWidgets.append(button)
        # Create the frame textbox
        frameTextCtrl = wx.TextCtrl(panel, wx.ID_ANY, size=(80,-1), style=wx.TE_RIGHT|wx.TE_PROCESS_ENTER)
        frameTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnButtonTextKillFocus)
        frameTextCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnButtonTextKillFocus)
        frameTextCtrl.Bind(wx.EVT_SET_FOCUS, self.OnButtonTextSetFocus)        
        frameTextCtrl.Bind(wx.EVT_CONTEXT_MENU, self.OnButtonTextContextMenu)
        frameTextCtrl.Replace(0, -1, str(0))
        sizer.Add(frameTextCtrl, 0, wx.ALIGN_CENTRE_VERTICAL|wx.LEFT, 12 if self.options['largeui'] else 4)
        videoControlWidgets.append(frameTextCtrl)
        if primary:
            self.frameTextCtrl = frameTextCtrl
        else:
            self.frameTextCtrl2 = frameTextCtrl
        # Create the video slider
        if primary:
            #~ self.videoSlider = wxp.Slider(panel, wx.ID_ANY, 0, 0, 240-1, style=wx.SL_HORIZONTAL|wx.SL_SELRANGE|wx.SL_AUTOTICKS, onscroll=self.OnSliderChanged)
            #~ self.videoSlider = wxp.Slider(panel, wx.ID_ANY, 0, 0, 240-1, style=wx.SL_HORIZONTAL|wx.SL_SELRANGE, onscroll=self.OnSliderChanged)
            self.videoSlider = SliderPlus(panel, self, wx.ID_ANY, 0, 0, 240-1, big=self.options['largeui'], bookmarkDict=self.bookmarkDict)
            self.videoSlider.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnSliderChanged)
            self.videoSlider.Bind(wx.EVT_SCROLL_ENDSCROLL, self.OnSliderReleased)
            self.videoSlider.Bind(wx.EVT_RIGHT_UP, self.OnSliderRightUp)
            self.videoSlider.Bind(wx.EVT_MIDDLE_DOWN, self.OnSliderMiddleDown)
            self.videoSlider.Bind(wx.EVT_LEFT_UP, self.OnSliderLeftUp)
            sizer.Add(self.videoSlider, 1, wx.EXPAND)
            videoControlWidgets.append(self.videoSlider)
        else:
            #~ self.videoSlider = wxp.Slider(panel, wx.ID_ANY, 0, 0, 240-1, style=wx.SL_HORIZONTAL|wx.SL_SELRANGE|wx.SL_AUTOTICKS, onscroll=self.OnSliderChanged)
            #~ self.videoSlider2 = wxp.Slider(panel, wx.ID_ANY, 0, 0, 240-1, style=wx.SL_HORIZONTAL|wx.SL_SELRANGE, onscroll=self.OnSliderChanged)
            #~ self.videoSlider.Bind(wx.EVT_SCROLL, self.OnSliderChanged)
            self.videoSlider2 = SliderPlus(panel, self, wx.ID_ANY, 0, 0, 240-1, big=self.options['largeui'], bookmarkDict=self.bookmarkDict)
            self.videoSlider2.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnSliderChanged)
            self.videoSlider2.Bind(wx.EVT_SCROLL_ENDSCROLL, self.OnSliderReleased)
            self.videoSlider2.Bind(wx.EVT_RIGHT_UP, self.OnSliderRightUp)
            self.videoSlider2.Bind(wx.EVT_MIDDLE_DOWN, self.OnSliderMiddleDown)
            self.videoSlider2.Bind(wx.EVT_LEFT_UP, self.OnSliderLeftUp)
            sizer.Add(self.videoSlider2, 1, wx.EXPAND)
            videoControlWidgets.append(self.videoSlider2)

        if primary:
            self.videoControlWidgets = videoControlWidgets
        else:
            self.videoControlWidgets2 = videoControlWidgets

        if self.options['disablepreview'] and primary:
            for ctrl in self.videoControlWidgets:
                ctrl.Disable()
                ctrl.Refresh()
        # Set the sizer and return the panel
        panel.SetSizer(sizer)
        return panel

    def createCropDialog(self, parent):
        dlg = wx.Dialog(parent, wx.ID_ANY, _('Crop editor'),
                        style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP)
        dlg.ctrls = {}
        # Create the crop spin controls
        spinSizer = wx.GridBagSizer(hgap=5, vgap=5)
        spinInfo = (
            ('left', (1,0), (1,1)),
            ('top', (0,2), (0,3)),
            ('-right', (1,4), (1,5)),
            ('-bottom', (2,2), (2,3)),
        )
        width = 50 if wx.version() >= '2.9' else 55 # fix for wxPython v2.8
        for name, txtPos, spinPos in spinInfo:
            staticText = wx.StaticText(dlg, wx.ID_ANY, name)
            spinCtrl = wx.SpinCtrl(dlg, wx.ID_ANY, '', size=(width,-1))
            spinCtrl.Bind(wx.EVT_TEXT, self.OnCropDialogSpinTextChange)
            spinSizer.Add(staticText, txtPos, flag=wx.ALIGN_CENTER|wx.RIGHT, border=5)
            spinSizer.Add(spinCtrl, spinPos, flag=wx.EXPAND|wx.RIGHT, border=0)
            dlg.ctrls[name] = spinCtrl
            dlg.ctrls[name+'Label'] = staticText
        # Create a static text message
        staticText = wx.StaticText(dlg, wx.ID_ANY,
            _(
                'You can drag the crop regions with the left mouse button when '
                'this dialog is visible, cropping the edge closest to the '
                'initial mouse click.'
            )
        )
        staticText.Wrap(spinSizer.GetMinSize()[0])
        # Create the autocrop controls
        buttonAutocrop = wx.Button(dlg, wx.ID_ANY, _('Auto-crop'))
        buttonAutocrop.SetMinSize(wx.Size(
            buttonAutocrop.GetTextExtent(_('Cancel') + ' (10/10)    ')[0], -1))
        buttonAutocrop.running = False
        dlg.Bind(wx.EVT_BUTTON, self.OnCropAutocrop, buttonAutocrop)
        spinAutocrop = wx.SpinCtrl(dlg, wx.ID_ANY, size=(100,-1), 
            value=u'{0} ({1})'.format(_('Samples'), self.options['autocrop_samples']), 
            min=1, initial=self.options['autocrop_samples'], 
            style=wx.TE_PROCESS_ENTER|wx.SP_ARROW_KEYS|wx.ALIGN_RIGHT)
        dlg.Bind(wx.EVT_SPINCTRL, self.OnCropAutocropSamples, spinAutocrop)
        autocropSizer = wx.BoxSizer(wx.HORIZONTAL)
        autocropSizer.Add(buttonAutocrop, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        autocropSizer.Add(spinAutocrop, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        # Create the choice box for insertion options
        choiceBox = wx.Choice(
            dlg, wx.ID_ANY,
            choices=(
                _('At script end'),
                _('At script cursor'),
                _('Copy to clipboard')
            )
        )
        choiceBox.SetSelection(self.options['cropchoice'])
        choiceLabel = wx.StaticText(dlg, wx.ID_ANY, _('Insert Crop() command:'))
        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        choiceSizer.Add(choiceLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        choiceSizer.Add(choiceBox, 1, wx.EXPAND|wx.LEFT, 5)
        dlg.ctrls['choiceInsert'] = choiceBox
        # Create the dialog buttons
        buttonApply = wx.Button(dlg, wx.ID_OK, _('Apply'))
        dlg.Bind(wx.EVT_BUTTON, self.OnCropDialogApply, buttonApply)
        buttonCancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        dlg.Bind(wx.EVT_BUTTON, self.OnCropDialogCancel, buttonCancel)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(buttonApply, 0, wx.ALL, 5)
        buttonSizer.Add(buttonCancel, 0, wx.ALL, 5)
        # Size the elements
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(spinSizer, 0, wx.ALL, 10)
        sizer.Add(autocropSizer, 0, wx.ALIGN_CENTER)
        sizer.Add(choiceSizer, 0, wx.TOP|wx.BOTTOM, 10)
        sizer.Add(wx.StaticLine(dlg), 0, wx.EXPAND)
        sizer.Add(staticText, 0, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 5)
        sizer.Add(buttonSizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        dlg.SetSizer(sizer)
        dlg.Fit()
        # Events
        dlg.Bind(wx.EVT_CLOSE, self.OnCropDialogCancel)
        buttonApply.SetDefault()
        return dlg

    def createTrimDialog(self, parent):
        dlg = wx.Dialog(parent, wx.ID_ANY, _('Trim editor'),
                        style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP)
        dlg.ctrls = {}
        # Create the radio box for Crop() options
        radioBoxTrim = wx.RadioBox(
            dlg, wx.ID_ANY, _('Selection options'),
            choices=(
                _('Keep selected regions'),
                _('Keep unselected regions')
            ),
            majorDimension=2,
            style=wx.RA_SPECIFY_ROWS,
        )
        def OnRadioBoxTrim(event):
            if event.GetSelection() == 0:
                self.invertSelection = False
            else:
                self.invertSelection = True
            self.ShowVideoFrame()
            event.Skip()
        radioBoxTrim.Bind(wx.EVT_RADIOBOX, OnRadioBoxTrim)
        radioBoxTrim.SetSelection(self.options['trimreversechoice'])
        dlg.ctrls['radioTrim'] = radioBoxTrim
        # Create the checkbox for marking frames
        checkBox = wx.CheckBox(dlg, wx.ID_ANY, _('Mark video frames inside/outside selection'))
        def OnCheckBox(event):
            self.markFrameInOut = event.IsChecked()
            self.ShowVideoFrame()
            event.Skip()
        checkBox.Bind(wx.EVT_CHECKBOX, OnCheckBox)
        checkBox.SetValue(self.options['trimmarkframes'])
        # Create a checkbox and a spinctrl for using Dissolve()
        checkBox2 = wx.CheckBox(dlg, wx.ID_ANY, _('Use Dissolve() with overlap frames:'))
        def OnCheckBox2(event):
            if event.IsChecked():
                spinCtrl.Enable(True)
                choiceLabel.SetLabel(dissolveTxt)
            else:
                spinCtrl.Enable(False)
                choiceLabel.SetLabel(trimTxt)
        checkBox2.Bind(wx.EVT_CHECKBOX, OnCheckBox2)
        dlg.ctrls['useDissolve'] = checkBox2
        spinCtrl = wx.SpinCtrl(dlg, wx.ID_ANY, size=(50, -1), max=999)
        spinCtrl.Enable(False)
        if wx.VERSION < (2, 8):
            spinCtrl.SetValue(0)
            spinCtrl.Bind(wx.EVT_TEXT, self.OnTrimDialogSpinTextChange)
        dlg.ctrls['dissolveOverlap'] = spinCtrl
        dissolveSizer = wx.BoxSizer(wx.HORIZONTAL)
        dissolveSizer.Add(checkBox2, 0, wx.TOP, 3)
        dissolveSizer.Add(spinCtrl)
        # Create the choice box for insertion options
        choiceBoxInsert = wx.Choice(
            dlg, wx.ID_ANY,
            choices=(
                _('At script end'),
                _('At script cursor'),
                _('Copy to clipboard')
            )
        )
        choiceBoxInsert.SetSelection(self.options['triminsertchoice'])
        trimTxt = _('Insert Trim() commands:')
        dissolveTxt = _('Insert Dissolve() commands:')
        labelSize = self.GetTextExtent(dissolveTxt)
        choiceLabel = wx.StaticText(dlg, wx.ID_ANY, _('Insert Trim() commands:'),
                                    size=labelSize, style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        choiceSizer.Add(choiceLabel, 0, wx.ALIGN_CENTER_VERTICAL)
        choiceSizer.Add(choiceBoxInsert, 0, wx.RIGHT, 5)
        dlg.ctrls['choiceInsert'] = choiceBoxInsert
        # Create a static text message
        staticText = wx.StaticText(dlg, wx.ID_ANY,
            _(
                'Use the buttons which appear on the video slider '
                'handle to create the frame selections to trim.'
            )
        )
        staticText.Wrap(choiceSizer.GetMinSize()[0])
        # Create the dialog buttons
        buttonApply = wx.Button(dlg, wx.ID_OK, _('Apply'))
        dlg.Bind(wx.EVT_BUTTON, self.OnTrimDialogApply, buttonApply)
        buttonCancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        dlg.Bind(wx.EVT_BUTTON, self.OnTrimDialogCancel, buttonCancel)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(buttonApply, 0, wx.ALL, 5)
        buttonSizer.Add(buttonCancel, 0, wx.ALL, 5)
        # Size the elements
        sizer = wx.BoxSizer(wx.VERTICAL)
        #~ sizer.Add(spinSizer, 0, wx.ALL, 10)
        sizer.Add(radioBoxTrim, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(checkBox, 0, wx.ALL, 10)
        sizer.Add(dissolveSizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        sizer.Add(choiceSizer, 0, wx.ALL, 5)
        sizer.Add(wx.StaticLine(dlg), 0, wx.EXPAND|wx.TOP, 5)
        sizer.Add(staticText, 0, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 5)
        sizer.Add(buttonSizer, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        dlg.SetSizer(sizer)
        dlg.Fit()
        # Events
        dlg.Bind(wx.EVT_CLOSE, self.OnTrimDialogCancel)
        buttonApply.SetDefault()
        return dlg

    # Event functions
    def OnClose(self, event):
        self.ExitProgram()
    
    def OnMenuBar(self, event):
        # tab groups
        if wx.version() >= '2.9':
            tab_group_menu = event.GetMenu()
            if tab_group_menu is not self.tab_group_menu:
                event.Skip()
                return 
        else:
            if event.GetMenu() is None: # None for submenus on 2.8
                event.Skip()
                return 
            tab_group_menu = self.tab_group_menu
        group = self.currentScript.group 
        if group == None:
            group = _('None')
        id = tab_group_menu.FindItem(group)
        tab_group_menu.Check(id, True)
        id = tab_group_menu.FindItem(_('Apply offsets'))
        tab_group_menu.Check(id, self.options['applygroupoffsets'])
        id = tab_group_menu.FindItem(_('Offset also bookmarks'))
        tab_group_menu.Check(id, self.options['offsetbookmarks'])
        event.Skip()
    
    def OnMenuFileNew(self, event):
        self.NewTab()

    def OnMenuFileOpen(self, event):
        self.OpenFile()

    def OnMenuFileUndoCloseTab(self, event):
        self.UndoCloseTab()

    def OnMenuFileClose(self, event):
        self.CloseTab(prompt=True)

    def OnMenuFileCloseAllTabs(self, event):
        self.CloseAllTabs()

    def OnMenuFileSaveScript(self, event):
        index = self.scriptNotebook.GetSelection()
        script = self.scriptNotebook.GetPage(index)
        self.SaveScript(script.filename, index)

    def OnMenuFileSaveScriptAs(self, event):
        self.SaveScript()
    
    def OnMenuFileReloadScript(self, event):
        script = self.currentScript
        if os.path.isfile(script.filename):
            txt, script.encoding, script.eol = self.GetMarkedScriptFromFile(script.filename)
            if txt != script.GetText():
                script.ParseFunctions(txt)
                pos = script.GetCurrentPos()
                script.SetText(txt)
                script.EmptyUndoBuffer()
                script.SetSavePoint()
                script.GotoPos(pos)
    
    def OnMenuFileOpenScriptDirectory(self, event):
        dirname, basename = os.path.split(self.currentScript.filename)
        if basename:
            if os.path.isdir(dirname):
                startfile(dirname)
            else:
                wx.MessageBox(u'\n\n'.join((_("The script's directory doesn't exist anymore!"), 
                              dirname)), _('Error'), style=wx.OK|wx.ICON_ERROR)
    
    def OnMenuFileRenameTab(self, index, pos=None):
        if not self.scriptNotebook.dblClicked\
        and not self.titleEntry\
        and not self.scriptNotebook.HasCapture()\
        and not (pos and index != self.scriptNotebook.GetSelection()):
            if pos == None:
                index = self.scriptNotebook.GetSelection()
                h = self.scriptNotebook.GetCharHeight() + 6
                for row in range(self.scriptNotebook.GetRowCount()):
                    y = h * row + h/2
                    for x in range(0, self.scriptNotebook.GetSizeTuple()[0], h):
                        ipage = self.scriptNotebook.HitTest((x, y))[0]
                        if ipage == index:
                            pos = (x, y)
                            break
                    if pos:
                        break
            if pos == None:
                return
            x, y = pos
            ipage = index
            while ipage == index:
                x -= 1
                ipage = self.scriptNotebook.HitTest((x, y))[0]
            left = x + 1
            x, y = pos
            ipage = index
            while ipage == index:
                y -= 1
                ipage = self.scriptNotebook.HitTest((x, y))[0]
            top = y + 1
            x, y = pos
            ipage = index
            while ipage == index:
                x += 1
                ipage = self.scriptNotebook.HitTest((x, y))[0]
            right = x - 1
            x, y = pos
            ipage = index
            while ipage == index:
                y += 1
                ipage = self.scriptNotebook.HitTest((x, y))[0]
            bottom = y - 1
            title = self.scriptNotebook.GetPageText(index)
            self.titleEntry = wx.TextCtrl(self.scriptNotebook, -1, title, pos=(left, top), size=(right-left, bottom-top), style=wx.TE_PROCESS_ENTER|wx.BORDER_SIMPLE)
            self.titleEntry.SetFocus()
            self.titleEntry.SetSelection(-1, -1)
            
            def OnTabKillFocus(event):
                if self.FindFocus() == self.scriptNotebook:
                    if self.scriptNotebook.GetPageImage(index) == -1:
                        self.currentScript.SetFocus()
                    else:
                        self.videoWindow.SetFocus()
                title = self.titleEntry.GetLineText(0)
                if not self.RenameScript(title):
                    wx.Bell()
                self.IdleCall.append((self.titleEntry.Destroy, tuple(), {}))
                
            def CheckTabPosition():
                try:
                    if self.titleEntry:
                        if self.scriptNotebook.HitTest((left, top))[0] != index\
                        or self.scriptNotebook.HitTest((right, bottom))[0] != index:
                            self.scriptNotebook.SetFocus()
                        else:
                            wx.CallLater(300, CheckTabPosition)
                except wx.PyDeadObjectError:
                    pass
                
            self.titleEntry.Bind(wx.EVT_KILL_FOCUS, OnTabKillFocus)
            self.titleEntry.Bind(wx.EVT_TEXT_ENTER, OnTabKillFocus)
            wx.CallLater(300, CheckTabPosition)
        if self.scriptNotebook.dblClicked:
            wx.CallLater(300, setattr, self.scriptNotebook, 'dblClicked' ,False)        
    
    def OnMenuFileExportHTML(self, event):
        self.ExportHTML()
    
    def OnMenuFilePageSetup(self, event):
        setup_dlg = wx.PageSetupDialog(self, self.print_data)
        if setup_dlg.ShowModal() == wx.ID_OK:
            self.print_data = wx.PageSetupDialogData(setup_dlg.GetPageSetupData())
        setup_dlg.Destroy()
    
    def OnMenuFilePrintHeader(self, event):
        self.print_header = not self.print_header
    
    def OnMenuFileWrapText(self, event):
        self.print_wrap = not self.print_wrap
    
    def OnMenuFileUseZoom(self, event):
        self.print_zoom = not self.print_zoom
    
    def OnMenuFilePrintPreview(self, event):
        filename = self.GetProposedPath(only='base')
        printout = STCPrintout(self.currentScript, page_setup_data=self.print_data, 
                               header=self.print_header, title=filename, job_title=filename, 
                               zoom=self.print_zoom, wrap=self.print_wrap)
        printout2 = STCPrintout(self.currentScript, page_setup_data=self.print_data, 
                                header=self.print_header, title=filename, job_title=filename, 
                                zoom=self.print_zoom, wrap=self.print_wrap)
        preview = wx.PrintPreview(printout, printout2, self.print_data.GetPrintData())
        preview.SetZoom(100)
        if preview.IsOk():
            pre_frame = wx.PreviewFrame(preview, self, _("Print Preview"))
            dsize = wx.GetDisplaySize()
            pre_frame.SetInitialSize((self.GetSize()[0],
                                      dsize.GetHeight() - 100))
            pre_frame.Initialize()
            pre_frame.Show()
        else:
            wx.MessageBox(_("Failed to create print preview"),
                          _("Print Error"),
                          style=wx.ICON_ERROR|wx.OK)
    
    def OnMenuFilePrint(self, event):
        pdd = wx.PrintDialogData(self.print_data.GetPrintData())
        printer = wx.Printer(pdd)
        filename = self.GetProposedPath(only='base')
        printout = STCPrintout(self.currentScript, page_setup_data=self.print_data, 
                               header=self.print_header, title=filename, job_title=filename, 
                               zoom=self.print_zoom, wrap=self.print_wrap)
        result = printer.Print(self.currentScript, printout)
        if result:
            self.print_data.SetPrintData(printer.GetPrintDialogData().GetPrintData())
        elif printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox(_("There was an error when printing.\n"
                            "Check that your printer is properly connected."),
                          _("Printer Error"),
                          style=wx.ICON_ERROR|wx.OK)
        printout.Destroy()
    
    def OnMenuFileLoadSession(self, event):
        if not self.LoadSession():
            wx.MessageBox(_('Damaged session file'), _('Error'), wx.OK|wx.ICON_ERROR)
            return
        self.SaveSession(self.lastSessionFilename, saverecentdir=False, previewvisible=False)
        
    def OnMenuFileSaveSession(self, event):
        self.SaveSession()

    def OnMenuFileBackupSession(self, event):
        self.SaveSession(self.lastSessionFilename, saverecentdir=False, previewvisible=False)

    def _x_OnMenuFileExportFilters(self, event):
        self.ShowFunctionExportImportDialog(export=True)

    def _x_OnMenuFileImportFilters(self, event):
        self.ShowFunctionExportImportDialog(export=False)

    def OnMenuFileNextTab(self, event):
        self.SelectTab(inc=1)

    def OnMenuFilePrevTab(self, event):
        self.SelectTab(inc=-1)

    def OnMenuFileRecentFile(self, event):
        # First find the position of the clicked menu item
        id = event.GetId()
        menuItem = self.GetMenuBar().FindItemById(id)
        menu = menuItem.GetMenu()
        nMenuItems = menu.GetMenuItemCount()
        pos = None
        for i in xrange(nMenuItems):
            if menu.FindItemByPosition(i).GetId() == id:
                pos = i
                break
        if pos is None:
            return
        # Find the menu position of the first filename
        firstpos = None
        i = nMenuItems - 1 - 2
        while i >= 0:
            menuItem = menu.FindItemByPosition(i)
            if menuItem.IsSeparator():
                firstpos = i + 1
                break
            i -= 1
        if firstpos is None:
            return
        # Compute the relative position
        relpos = pos - firstpos
        # Open the corresponding filename
        try:
            filename = self.options['recentfiles'][relpos]
            if os.path.isfile(filename):
                self.OpenFile(filename)
            else:
                wx.MessageBox(_('File does not exist!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
        except IndexError:
            pass

    def OnMenuFileExit(self, event):
        self.ExitProgram()

    def OnMenuEditUndo(self, event):
        script = self.currentScript
        script.Undo()

    def OnMenuEditRedo(self, event):
        script = self.currentScript
        script.Redo()

    def OnMenuEditCut(self, event):
        script = self.currentScript
        script.Cut()

    def OnMenuEditCopy(self, event):
        script = self.currentScript
        script.Copy()

    def OnMenuEditPaste(self, event):
        script = self.currentScript
        script.Paste()

    def OnMenuEditFind(self, event):
        script = self.currentScript
        if self.replaceDialog.IsShown():
            script.ShowFindReplaceDialog(find=True)
        else:
            script.ShowQuickFindDialog()

    def OnMenuEditFindNext(self, event):
        script = self.currentScript
        script.FindNext()

    def OnMenuEditFindPrevious(self, event):
        script = self.currentScript
        script.FindPrevious()
    
    def OnMenuEditReplace(self, event):
        script = self.currentScript
        script.ShowFindReplaceDialog()
    
    def OnMenuEditReplaceNext(self, event):
        script = self.currentScript
        script.ReplaceNext()
    
    def OnMenuEditSelectAll(self, event):
        script = self.currentScript
        script.SelectAll()
    
    def OnMenuEditInsertSnippet(self, event):
        self.currentScript.InsertSnippet()
    
    def OnMenuEditInsertSource(self, event):
        self.InsertSource(check_selection=True)

    def OnMenuEditInsertFilename(self, event):
        filefilter = _('All files') + ' (*.*)|*.*'
        initial_dir = self.GetProposedPath(only='dir')
        dlg = wx.FileDialog(self, _('Select a file'), initial_dir, '', filefilter, wx.OPEN)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            filename = dlg.GetPath()
            self.InsertText(filename, pos=None)
            dirname = os.path.dirname(filename)
            if os.path.isdir(dirname):
                self.options['recentdir'] = dirname
        dlg.Destroy()

    def OnMenuEditInsertPlugin(self, event):
        self.InsertPlugin()

    def OnMenuEditInsertFrameNumber(self, event):
        self.InsertFrameNumber()

    def OnMenuEditInsertUserSlider(self, event):
        self.InsertUserSlider()

    def OnMenuEditInsertUserSliderSeparator(self, event):
        script = self.currentScript
        dlg = wx.TextEntryDialog(self, _('Enter separator label'), _('Create a separator label'))
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            label = dlg.GetValue()
            if label != '':
                script.ReplaceSelection('[<separator="%s">]' % label.replace(',', '_'))
            else:
                script.ReplaceSelection('[<separator>]')
        dlg.Destroy()

    def _x_OnMenuEditInsertBookmarkTrims(self, event):
        self.InsertBookmarkTrims()

    def _x_OnMenuEditInsertTrimSelectedOut(self, event):
        self.InsertSelectionTrims(cutSelected=True)

    def _x_OnMenuEditInsertTrimUnSelectedOut(self, event):
        self.InsertSelectionTrims(cutSelected=False)

    def OnMenuEditToggleTagSelection(self, event):
        script = self.currentScript
        # Get the name of the tag
        label = None
        dlg = wx.TextEntryDialog(self, _('Enter tag name:'), _('Tag definition'), '')
        if dlg.ShowModal() == wx.ID_OK:
            label = dlg.GetValue()
        dlg.Destroy()
        # Insert the tags into the text
        if label is not None:
            startpos, endpos = script.GetSelection()
            startline = script.LineFromPosition(startpos)
            endline = script.LineFromPosition(endpos)
            firstpos = script.PositionFromLine(startline)
            lastpos = script.GetLineEndPosition(endline)
            lastfirstpos = script.PositionFromLine(endline)
            extraA = extraB = ''
            extraAA = extraBB = ''
            if startpos == firstpos and (endpos == lastpos or endpos == lastfirstpos):
                extraA = '\n'
                if endpos == lastpos:
                    extraB = '\n'
                if endpos == lastfirstpos:
                    extraBB = '\n'
            script.InsertText(endpos, '%s[/%s]%s' % (extraB, label, extraBB))
            script.InsertText(startpos, '%s[%s]%s' % (extraAA, label, extraA))

    def OnMenuEditClearToggleTags(self, event):
        script = self.currentScript
        script.SetText(self.cleanToggleTags(script.GetText()))

    def OnMenuEditIndentSelection(self, event=None):
        self.currentScript.CmdKeyExecute(stc.STC_CMD_TAB)
        #~ script = self.currentScript
        #~ lineA = script.LineFromPosition(script.GetSelectionStart())
        #~ lineB = script.LineFromPosition(script.GetSelectionEnd())
        #~ if lineA==lineB:
            #~ script.GotoLine(lineA)
            #~ posA = script.GetCurrentPos()
            #~ script.CmdKeyExecute(stc.STC_CMD_TAB)
            #~ posB = script.GetLineEndPosition(lineA)
            #~ script.SetSelection(posB,posA)
        #~ else:
            #~ script.CmdKeyExecute(stc.STC_CMD_TAB)
        #~ if self.tab_processed:
            #~ self.tab_processed = False
        #~ else:
            #~ script.CmdKeyExecute(stc.STC_CMD_TAB)

    def OnMenuEditUnIndentSelection(self, event):
        script = self.currentScript
        lineA = script.LineFromPosition(script.GetSelectionStart())
        lineB = script.LineFromPosition(script.GetSelectionEnd())
        if lineA==lineB:
            script.GotoLine(lineA)
            posA = script.GetCurrentPos()
            script.CmdKeyExecute(stc.STC_CMD_BACKTAB)
            posB = script.GetLineEndPosition(lineA)
            script.SetSelection(posB,posA)
        else:
            script.CmdKeyExecute(stc.STC_CMD_BACKTAB)

    def OnMenuEditBlockComment(self, event):
        script = self.currentScript
        script.BlockComment()
    
    def OnMenuEditStyleComment(self, event):
        script = self.currentScript
        script.StyleComment()
    
    def OnMenuEditToggleCurrentFold(self, event):
        script = self.currentScript
        script.ToggleFold(script.GetCurrentLine())
        
    def OnMenuEditToggleAllFolds(self, event):
        script = self.currentScript
        script.FoldAll()

    def OnMenuEditMoveLineUp(self, event):
        self.currentScript.MoveSelectionByOneLine(up=True)
        self.AutoUpdateVideo(force=True)

    def OnMenuEditMoveLineDown(self, event):
        self.currentScript.MoveSelectionByOneLine(up=False)
        self.AutoUpdateVideo(force=True)

    def OnMenuEditAutocomplete(self, event):
        script = self.currentScript
        if script.AutoCompActive():
            script.CmdKeyExecute(wx.stc.STC_CMD_CANCEL)
            if script.autocomplete_case == 'function':
                    return
        script.ShowAutocomplete()
        
    def OnMenuEditAutocompleteAll(self, event):
        script = self.currentScript
        if script.AutoCompActive():
            script.CmdKeyExecute(wx.stc.STC_CMD_CANCEL)
            if script.autocomplete_case == 'function':
                    return
        script.ShowAutocomplete(all=True)
    
    def OnMenuEditAutocompleteParameterFilename(self, event):
        script = self.currentScript
        pos = script.GetCurrentPos() - 1
        if script.IsString(pos):
            if script.AutoCompActive():
                script.CmdKeyExecute(wx.stc.STC_CMD_CANCEL)
                if script.autocomplete_case == 'filename':
                    return
            script.AutocompleteFilename()
        else:
            if script.AutoCompActive():
                script.CmdKeyExecute(wx.stc.STC_CMD_CANCEL)
                if script.autocomplete_case in ('parameter name', 
                                                'parameter value'):
                    return
            # prefer name over value
            while pos >= 0:
                chr = unichr(script.GetCharAt(pos))
                if chr == '=':
                    return script.AutocompleteParameterValue()
                elif not (chr.isspace() or chr == '\\'):
                    return script.AutocompleteParameterName()
                pos -= 1
    
    def OnMenuEditShowCalltip(self, event):
        if self.currentScript.CallTipActive():
            self.currentScript.CmdKeyExecute(wx.stc.STC_CMD_CANCEL)
        else:
            self.currentScript.UpdateCalltip(force=True)

    def OnMenuEditShowFunctionDefinition(self, event):
        script = self.currentScript
        name = script.GetSelectedText() or script.GetFilterNameAtCursor()
        if name in script.avsfilterdict.own_dict:
            args = script.avsfilterdict[name][0]
        else:
            args = None
        self.ShowFunctionDefinitionDialog(functionName=name, functionArgs=args)

    def OnMenuEditFilterHelp(self, event):
        script = self.currentScript
        word = script.GetSelectedText() or script.GetFilterNameAtCursor()
        script.ShowFilterDocumentation(word)
    
    def OnMenuEditParseFunctions(self, event):
        self.currentScript.ParseFunctions(refresh_highlighting=True)
    
    def OnMenuEditCopyToNewTab(self, event):
        self.NewTab(copytab=True)
    
    def OnMenuCopyUnmarkedScript(self, event):
        txt = self.getCleanText(self.currentScript.GetText()).replace('\n', '\r\n')
        text_data = wx.TextDataObject(txt)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_data)
            wx.TheClipboard.Close()

    def OnMenuCopyAvisynthError(self, event):
        if self.currentScript.AVI:           
            error_message = self.currentScript.AVI.error_message or self.currentScript.AVI.clip.get_error()
            if error_message and not wx.TheClipboard.IsOpened(): 
                text_data = wx.TextDataObject(error_message)
                wx.TheClipboard.Open()
                wx.TheClipboard.SetData(text_data)
                wx.TheClipboard.Close()
            
    def OnMenuCopyStatusBar(self, event):
        if not wx.TheClipboard.IsOpened():
            statusBar = self.GetStatusBar()
            text = ' '.join(statusBar.GetFields())
            text_data = wx.TextDataObject(text)
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(text_data)
            wx.TheClipboard.Close()
            
    def OnMenuEditShowScrapWindow(self, event):
        scrap = self.scrapWindow
        if scrap.IsShown():
            scrap.Hide()
        else:
            scrap.Show()

    def OnMenuVideoBookmark(self, event):
        framenum = self.GetFrameNumber()
        self.AddFrameBookmark(framenum)

    def _x_OnMenuVideoBookmarkStart(self, event):
        framenum = self.GetFrameNumber()
        self.AddFrameBookmark(framenum, bmtype=1, toggle=False)

    def _x_OnMenuVideoBookmarkEnd(self, event):
        framenum = self.GetFrameNumber()
        self.AddFrameBookmark(framenum, bmtype=2, toggle=False)

    def OnMenuVideoGotoFrameNumber(self, event):
        if self.playing_video:
            self.PlayPauseVideo()
            self.playing_video = ''
        #~ bmenu = self.GetMenuBar().GetMenu(2).FindItemByPosition(1).GetSubMenu()
        #~ framenum = int(bmenu.GetLabel(event.GetId()))
        menuItem = self.GetMenuBar().FindItemById(event.GetId())
        framenum = int(menuItem.GetLabel().split()[0])
        self.ShowVideoFrame(framenum)
        if self.playing_video == '':
            self.PlayPauseVideo()

    def OnMenuVideoBookmarkMoveTitle(self, event):
        if type(event) is int:
            curr = event
        else:
            curr = self.GetFrameNumber()
        bookmarkList = [bookmark for bookmark, bmtype in self.GetBookmarkFrameList().items() if bmtype == 0]
        diffList = [(abs(curr - i), i) for i in self.bookmarkDict if self.bookmarkDict[i]]
        if not diffList:
            return
        diff, bookmark = min(diffList)
        if bookmark not in bookmarkList:
            self.AddFrameBookmark(bookmark)
            return
        if not diff: 
            return
        self.bookmarkDict[curr] = self.bookmarkDict[bookmark]
        del self.bookmarkDict[bookmark]
        if curr not in bookmarkList:
            self.AddFrameBookmark(curr, refreshProgram=False)
        self.DeleteFrameBookmark(bookmark)
            
    def OnMenuVideoBookmarkRestoreHistory(self, event):
        bookmarkList = [bookmark for bookmark, bmtype in self.GetBookmarkFrameList().items() if bmtype == 0]
        for bookmark in self.bookmarkDict.keys():
            if bookmark not in bookmarkList and self.bookmarkDict[bookmark]:
                self.OnMenuVideoBookmarkMoveTitle(bookmark)

    def OnMenuVideoBookmarkClearHistory(self, event=None, start=0, end=None):
        bookmarkList = [bookmark for bookmark, bmtype in self.GetBookmarkFrameList().items() if bmtype == 0]
        for bookmark in self.bookmarkDict.keys():
            if ((bookmark not in bookmarkList or not self.bookmarkDict[bookmark]) and 
                bookmark >= start and (end is None or bookmark <= end)):
                del self.bookmarkDict[bookmark]
                
    def OnMenuVideoBookmarkAutoTitle(self, event):
        bookmarkList = [bookmark for bookmark, bmtype in self.GetBookmarkFrameList().items() if bmtype == 0]
        bookmarkList.sort()
        for i in range(len(bookmarkList)):
            if bookmarkList[i] not in self.bookmarkDict:
                self.bookmarkDict[bookmarkList[i]] = _('Chapter') + (' %02d' % (i+1))
        self.UpdateBookmarkMenu()
        if self.previewWindowVisible:
            self.videoSlider.Refresh()
            if self.separatevideowindow:
                self.videoSlider2.Refresh()
        
    def OnMenuVideoBookmarkSetTitle(self, event):
        bookmarkInfo = []
        historyList = []
        titleList = []
        bookmarkList = [bookmark for bookmark, bmtype in self.GetBookmarkFrameList().items() if bmtype == 0]
        for bookmark in self.bookmarkDict:
            if bookmark in bookmarkList:
                titleList.append(bookmark)
            else:
                historyList.append(bookmark)                
        bookmarkList += historyList
        if not bookmarkList:
            return
        for bookmark in bookmarkList:
            if self.currentScript.AVI:
                sec = bookmark / self.currentScript.AVI.Framerate                    
                min, sec = divmod(sec, 60)
                hr, min = divmod(min, 60)
                timecode = '%02d:%02d:%06.3f' % (hr, min, sec)
            else:
                timecode = '??:??:??.???'
            title = self.bookmarkDict.get(bookmark, '')
            bookmarkInfo.append((bookmark, timecode, title))
        bookmarkInfo.sort()
        dlg = wx.Dialog(self, wx.ID_ANY, _('Set title for bookmarks'), size=(450, 270), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        attrTitle = wx.ListItemAttr()
        attrTitle.SetTextColour(wx.BLUE)
        attrHistory = wx.ListItemAttr()
        attrHistory.SetTextColour(wx.RED)
        # Define the virtual list control
        class VListCtrl(wxp.ListCtrl):                
            def OnGetItemText(self, item, column):
                bookmark, timecode, title = bookmarkInfo[item]
                if column == 0:
                    return title
                elif column == 1:
                    if bookmark in historyList:
                        return '* ' + str(bookmark)
                    return str(bookmark)
                return timecode
                
            def OnGetItemAttr(self, item):
                bookmark, timecode, title = bookmarkInfo[item]
                if bookmark in titleList:
                    return attrTitle
                elif bookmark in historyList:
                    return attrHistory
                    
        listCtrl = VListCtrl(dlg, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL|wx.LC_EDIT_LABELS|wx.LC_HRULES|wx.LC_VRULES)
        listCtrl.InsertColumn(0, _('Title'))
        listCtrl.InsertColumn(1, _('Frame No.'), wx.LIST_FORMAT_RIGHT)
        listCtrl.InsertColumn(2, _('Time **'))
        listCtrl.SetItemCount(len(bookmarkInfo))
        listCtrl.setResizeColumn(1)
        listCtrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        listCtrl.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        
        def OnListCtrlActivated(event):
            listCtrl.EditLabel(event.GetIndex())
            
        def OnListCtrlEndLabelEdit(event):
            i = event.GetIndex()
            bookmark, timecode, oldTitle = bookmarkInfo[i]
            newTitle = event.GetLabel().strip()
            if bookmark not in historyList:
                if oldTitle and not newTitle:
                    titleList.remove(bookmark)
                if not oldTitle and newTitle:
                    titleList.append(bookmark)
            bookmarkInfo[i] = (bookmark, timecode, newTitle)
            
        listCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, OnListCtrlActivated)
        listCtrl.Bind(wx.EVT_LIST_END_LABEL_EDIT, OnListCtrlEndLabelEdit)
        label = wx.StaticText(dlg, wx.ID_ANY, _('Left-click on a selected item or double-click to edit.\n\n'
                                                '*  RED - a historic title, not a real bookmark.\n'
                                                '** Time may be unavailable or incorrect before preview refreshed.'
                                                ))
        # Standard buttons
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Size the elements
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(listCtrl, 1, wx.EXPAND|wx.ALL, 5)
        dlgSizer.Add(label, 0, wx.LEFT, 5)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        dlg.SetSizer(dlgSizer)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            for bookmark, timecode, title in bookmarkInfo:
                self.bookmarkDict[bookmark] = title
                if not title:
                    del self.bookmarkDict[bookmark]
            self.UpdateBookmarkMenu()
            if self.previewWindowVisible:
                self.videoSlider.Refresh()
                if self.separatevideowindow:
                    self.videoSlider2.Refresh()
        dlg.Destroy()
    
    def OnMenuVideoGroupApplyOffsets(self, event):
        self.OnGroupApplyOffsets(event)
    
    def OnMenuVideoGroupOffsetBookmarks(self, event):
        self.OnGroupOffsetBookmarks(event)
    
    def OnMenuVideoGroupClearTabGroup(self, event):
        self.OnGroupClearTabGroup(event)
    
    def OnMenuVideoGroupClearAllTabGroups(self, event):
        self.OnGroupClearAllTabGroups(event)
    
    def OnMenuVideoGroupAssignTabGroup(self, event):
        label = event.GetEventObject().GetLabel(event.GetId())
        self.AssignTabGroup(label)
    
    def OnMenuVideoGotoLastScrolled(self, event):
        if self.playing_video:
            self.PlayPauseVideo()
            self.playing_video = ''
        curPos = self.videoSlider.GetValue()
        self.ShowVideoFrame(self.lastshownframe)
        self.lastshownframe = curPos
        if self.playing_video == '':
            self.PlayPauseVideo()

    def OnMenuVideoGotoNextBookmark(self, event):
        self.GotoNextBookmark()

    def OnMenuVideoGotoPreviousBookmark(self, event):
        self.GotoNextBookmark(reverse=True)

    def OnMenuVideoGotoClearAll(self, event):
        self.DeleteAllFrameBookmarks(bmtype=0)

    def OnMenuVideoGoto(self, event):
        if not self.separatevideowindow or not self.previewWindowVisible or self.FindFocus() != self.videoWindow:
            frameTextCtrl = self.frameTextCtrl
        else:
            frameTextCtrl = self.frameTextCtrl2
        #~ frameTextCtrl.SetSelection(-1, -1)               
        frameTextCtrl.SetFocus()

    def OnMenuVideoPrevFrame(self, event):
        if not self.separatevideowindow:
            self.ShowVideoOffset(-1)
        else:
            if event is not None and event.GetEventObject() in self.videoControlWidgets and self.previewWindowVisible:
                self.ShowVideoOffset(-1, focus=False)
                self.currentScript.SetFocus()
            else:
                self.ShowVideoOffset(-1)

    def OnMenuVideoNextFrame(self, event):
        if not self.separatevideowindow:
            self.ShowVideoOffset(+1)
        else:
            if event is not None and event.GetEventObject() in self.videoControlWidgets and self.previewWindowVisible:
                self.ShowVideoOffset(+1, focus=False)
                self.currentScript.SetFocus()
            else:
                self.ShowVideoOffset(+1)

    def OnMenuVideoPrevSecond(self, event):
        self.ShowVideoOffset(-1, units='sec')

    def OnMenuVideoNextSecond(self, event):
        self.ShowVideoOffset(+1, units='sec')

    def OnMenuVideoPrevMinute(self, event):
        self.ShowVideoOffset(-1, units='min')

    def OnMenuVideoNextMinute(self, event):
        self.ShowVideoOffset(+1, units='min')

    def OnMenuVideoFirstFrame(self, event):
        if self.playing_video:
            self.PlayPauseVideo()
            self.playing_video = ''
        self.ShowVideoFrame(0)
        if self.playing_video == '':
            self.PlayPauseVideo()

    def OnMenuVideoLastFrame(self, event):
        if self.playing_video:
            self.PlayPauseVideo()
        self.ShowVideoFrame(-1)

    def OnMenuVideoPrevCustomUnit(self, event):
        offset = -self.options['customjump']
        units = self.options['customjumpunits']
        self.ShowVideoOffset(offset, units=units)

    def OnMenuVideoNextCustomUnit(self, event):
        offset = +self.options['customjump']
        units = self.options['customjumpunits']
        self.ShowVideoOffset(offset, units=units)

    def OnMenuVideoSaveImage(self, event):
        self.SaveImage()
    
    def OnMenuVideoQuickSaveImage(self, event):
        path = self.SaveImage(silent=True)
        if path:
            text = _(u'Image saved to "{0}"').format(path)
            self.GetStatusBar().SetStatusText(text)
    
    def OnMenuVideoCopyImageClipboard(self, event):
        script = self.currentScript
        if script is None or script.AVI is None:
            wx.MessageBox(_('No image to save'), _('Error'), 
                          style=wx.OK|wx.ICON_ERROR)
            return False
        w = script.AVI.DisplayWidth
        h = script.AVI.DisplayHeight
        bmp = wx.EmptyBitmap(w, h)
        mdc = wx.MemoryDC()
        mdc.SelectObject(bmp)
        if not script.AVI.DrawFrame(self.currentframenum, mdc):
            wx.MessageBox(u'\n\n'.join((_('Error requesting frame {number}').format(number=self.currentframenum), 
                          script.AVI.clip.get_error())), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        bmp_data = wx.BitmapDataObject(bmp)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(bmp_data)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox(_("Couldn't open clipboard"), _('Error'), 
                          style=wx.OK|wx.ICON_ERROR)
            return False
        return True
    
    def OnMenuVideoCropEditor(self, event):
        script = self.currentScript
        dlg = self.cropDialog
        if dlg.IsShown():
            return
        # Show the video preview
        if not self.ShowVideoFrame():
            return False
        if script.AVI.DisplayWidth != script.AVI.Width or \
                script.AVI.DisplayHeight != script.AVI.Height:
            wx.MessageBox(_('Cannot use crop editor unless bit depth is set to 8'), 
                          _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        # Set the spin control ranges
        w = script.AVI.Width
        h = script.AVI.Height
        for key in ('left', '-right'):
            dlg.ctrls[key].SetRange(0, w-self.options['cropminx'])
            dlg.ctrls[key].SetValue(0)
            dlg.ctrls[key].SetSelection(0,-1)
        for key in ('top', '-bottom'):
            dlg.ctrls[key].SetRange(0, h-self.options['cropminy'])
            dlg.ctrls[key].SetValue(0)
            dlg.ctrls[key].SetSelection(0,-1)
        # Show the crop dialog
        self.SetDialogPositionNextToVideo(dlg)
        self.PaintCropWarnings()
        dlg.Show()
        dlg.ctrls['left'].SetFocus()
        dlg.ctrls['left'].SetSelection(0,-1)
        # Set the crop status text
        self.SetVideoStatusText()

    def SetDialogPositionNextToVideo(self, dlg):
        parent = dlg.GetParent()
        xp, yp = parent.GetPositionTuple()
        wp, hp = parent.GetSizeTuple()
        wd, hd = wx.ScreenDC().GetSizeTuple()
        ws, hs = dlg.GetSizeTuple()
        #~ dlg.SetPosition((min(xp+wp-20, wd-ws),-1))
        xSplitter = self.videoSplitter.GetSashPosition()
        wVideo = self.currentScript.AVI.DisplayWidth
        xpos = min(xp+wVideo+30, xp+xSplitter+20)
        dlg.SetPosition((min(xpos, wd-ws), yp+hp-hs-self.mainSplitter.GetMinimumPaneSize()-50))

    def OnMenuVideoTrimEditor(self, event):
        dlg = self.trimDialog
        if dlg.IsShown():
            return
        # Show the video preview
        if not self.ShowVideoFrame():
            return False
        self.SetDialogPositionNextToVideo(dlg)
        for slider in self.GetVideoSliderList():
            slider.ToggleSelectionMode(1)
        dlg.Show()
        self.ShowVideoFrame()

    def OnMenuVideoTrimEditorSetStartpoint(self, event):
        self.SetSelectionEndPoint(1)

    def OnMenuVideoTrimEditorSetEndpoint(self, event):
        self.SetSelectionEndPoint(2)
    
    def OnMenuVideoMoveSelectionsBeforeCurrentFrame(self, event):
        selections = self.GetSliderSelections(self.invertSelection)
        if selections:
            self.MoveFrameRanges(selections, paste_before=True)
    
    def OnMenuVideoMoveSelectionsAfterCurrentFrame(self, event):
        selections = self.GetSliderSelections(self.invertSelection)
        if selections:
            self.MoveFrameRanges(selections, paste_before=False)
    
    def OnMenuVideoZoom(self, event=None, menuItem=None, zoomfactor=None, show=True, scroll=None):
        if zoomfactor is None:
            if True:#wx.VERSION > (2, 8):
                vidmenus = [self.videoWindow.contextMenu, self.GetMenuBar().GetMenu(2)]
                if menuItem is None:
                    id = event.GetId()
                    for vidmenu in vidmenus:
                        menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Zoom'))).GetSubMenu()
                        menuItem = menu.FindItemById(id)
                        if menuItem:
                            menuItem.Check()
                            label = menuItem.GetLabel()
                            zoomvalue = self.zoomLabelDict[label]
                        else:
                            updateMenu = menu
                    id = updateMenu.FindItem(label)
                    menuItem = updateMenu.FindItemById(id)
                    if menuItem is None:
                        print>>sys.stderr, _('Error'), 'OnMenuVideoZoom(): cannot find menu item by id'
                        return
                    menuItem.Check()
                else:
                    menuItem.Check()
                    label = menuItem.GetLabel()
                    zoomvalue = self.zoomLabelDict[label]
                    for vidmenu in vidmenus:
                        menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Zoom'))).GetSubMenu()
                        if menu != menuItem.GetMenu():
                            id = menu.FindItem(label)
                            menuItem = menu.FindItemById(id)
                            if menuItem is None:
                                print>>sys.stderr, _('Error'), 'OnMenuVideoZoom(): cannot find menu item by id'
                                return
                            menuItem.Check()
                            break
            else:
                if menuItem is None:
                    id = event.GetId()
                    vidmenu = self.videoWindow.contextMenu
                    menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Zoom'))).GetSubMenu()
                    menuItem = menu.FindItemById(id)
                if menuItem is None:
                    print>>sys.stderr, _('Error'), 'OnMenuVideoZoom(): cannot find menu item by id'
                    return
                menuItem.Check()
                zoomvalue = self.zoomLabelDict[menuItem.GetLabel()]
            if zoomvalue == 'fill':
                self.zoomwindow = True
                self.zoomwindowfit = False
                self.zoomwindowfill = True
                zoomfactor = 1
            elif zoomvalue == 'fit':
                self.zoomwindow = True
                self.zoomwindowfit = True
                self.zoomwindowfill = False
                zoomfactor = 1
            else:
                try:
                    zoompercent = int(zoomvalue) #int(label.strip(' %'))
                except ValueError:
                    zoompercent = 100
                if zoompercent >= 100:
                    zoomfactor = zoompercent / 100
                else:
                    if zoompercent == 50:
                        zoomfactor = 0.5
                    elif zoompercent == 25:
                        zoomfactor = 0.25
                    else:
                        return
                if self.zoomwindow:
                    self.zoomwindow = False
                    self.zoomwindowfit = False
                    self.zoomwindowfill = False
                    #~ for index in xrange(self.scriptNotebook.GetPageCount()):
                        #~ script = self.scriptNotebook.GetPage(index)
                        #~ script.AVI = None
                    self.currentScript.lastSplitVideoPos = None
        #~ self.ZoomPreviewWindow(zoomfactor, show=show)
        self.zoomfactor = zoomfactor
        if show:
            self.ShowVideoFrame(scroll=scroll)

    def OnMenuVideoFlip(self, event):
        id = event.GetId()
        if True:#wx.VERSION > (2, 8):
            vidmenus = [self.videoWindow.contextMenu, self.GetMenuBar().GetMenu(2)]
            for vidmenu in vidmenus:
                menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Flip'))).GetSubMenu()
                menuItem = menu.FindItemById(id)
                if menuItem: 
                    label = menuItem.GetLabel()
                    value = self.flipLabelDict[label]
                    menuItem.Check(value not in self.flip)
                else:
                    updateMenu = menu
            id = updateMenu.FindItem(label)
            menuItem = updateMenu.FindItemById(id)
            if menuItem is None:
                print>>sys.stderr, _('Error'), 'OnMenuVideoFlip(): cannot find menu item by id'
                return
            menuItem.Check(value not in self.flip)
        else:
            vidmenu = self.videoWindow.contextMenu
            menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Flip'))).GetSubMenu()
            menuItem = menu.FindItemById(id)
            if menuItem is None:
                print>>sys.stderr, _('Error'), 'OnMenuVideoFlip(): cannot find menu item by id'
                return
            value = self.flipLabelDict[menuItem.GetLabel()]            
            menuItem.Check(value not in self.flip)
            
        if value in self.flip:
            self.flip.remove(value)
        else:
            self.flip.append(value)
        self.bmpVideo = None
        self.videoWindow.Refresh()
    
    def OnMenuVideoYUV2RGB(self, event):
        id = event.GetId()
        if True:#wx.VERSION > (2, 8):
            vidmenus = [self.videoWindow.contextMenu, self.GetMenuBar().GetMenu(2)]
            for vidmenu in vidmenus:
                menu = vidmenu.FindItemById(vidmenu.FindItem(_('&YUV -> RGB'))).GetSubMenu()
                menuItem = menu.FindItemById(id)
                if menuItem:
                    label = menuItem.GetLabel()                    
                    value = self.yuv2rgbDict[label]
                    if menuItem.GetKind() == wx.ITEM_RADIO:
                        menuItem.Check()
                    else:
                        menuItem.Check(not getattr(self, value))
                else:
                    updateMenu = menu
            id = updateMenu.FindItem(label)
            menuItem = updateMenu.FindItemById(id)
            if not menuItem:
                print>>sys.stderr, _('Error'), 'OnMenuVideoYUV2RGB(): cannot find menu item by id'
                return
            if menuItem.GetKind() == wx.ITEM_RADIO:
                menuItem.Check()
            else:
                menuItem.Check(not getattr(self, value))
        else:
            vidmenu = self.videoWindow.contextMenu
            menu = vidmenu.FindItemById(vidmenu.FindItem(_('&YUV -> RGB'))).GetSubMenu()
            menuItem = menu.FindItemById(id)
            if menuItem is None:
                print>>sys.stderr, _('Error'), 'OnMenuVideoYUV2RGB(): cannot find menu item by id'
                return
            if menuItem.GetKind() == wx.ITEM_RADIO:
                menuItem.Check()
            else:
                menuItem.Check(not self.swapuv)
            value = self.yuv2rgbDict[menuItem.GetLabel()]
        refresh = False
        AVI = self.currentScript.AVI
        if value == 'swapuv':
            self.swapuv = not self.swapuv
            if AVI:
                refresh = AVI.IsYUV and not AVI.IsY8
        elif value in ['Progressive', 'Interlaced']:
            self.interlaced = not self.interlaced
            if AVI:
                refresh = AVI.IsYV12
        else:
            if value in ('tv', 'pc'):
                self.matrix[1] = value
            else:
                self.matrix[0] = value
            if AVI:
                refresh = AVI.IsYUV
        if refresh:
            for index in xrange(self.scriptNotebook.GetPageCount()):
                script = self.scriptNotebook.GetPage(index)
                script.display_clip_refresh_needed = True
            if self.previewWindowVisible:
                self.ShowVideoFrame(forceRefresh=False, focus=self.options['focusonrefresh'])

    def OnMenuVideoBitDepth(self, event):
        if self.cropDialog.IsShown():
            wx.MessageBox(_('Cannot change bit depth while crop editor is open!'), 
                          _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        vidmenus = [self.videoWindow.contextMenu, self.GetMenuBar().GetMenu(2)]
        id = event.GetId()
        for vidmenu in vidmenus:
            menu = vidmenu.FindItemById(vidmenu.FindItem(_('Bith &depth'))).GetSubMenu()
            menuItem = menu.FindItemById(id)
            if menuItem:
                menuItem.Check()
                label = menuItem.GetLabel()
                if label == _('Stacked yuv420p10 or yuv444p10'):
                    self.bit_depth = 's10'
                elif label == _('Stacked yuv420p16 or yuv444p16'):
                    self.bit_depth = 's16'
                elif label == _('Interleaved yuv420p10 or yuv444p10'):
                    self.bit_depth = 'i10'
                elif label == _('Interleaved yuv420p16 or yuv444p16'):
                    self.bit_depth = 'i16'
                elif label == _('Interleaved RGB48'):
                    self.bit_depth = 'rgb48'
                else:
                    self.bit_depth = None
                for index in xrange(self.scriptNotebook.GetPageCount()):
                    script = self.scriptNotebook.GetPage(index)
                    script.display_clip_refresh_needed = True
                if self.previewWindowVisible:
                    self.ShowVideoFrame(forceRefresh=False, focus=self.options['focusonrefresh'])
            else:
                updateMenu = menu
        id = updateMenu.FindItem(label)
        menuItem = updateMenu.FindItemById(id)
        if not menuItem:
            print>>sys.stderr, _('Error'), 'OnMenuVideoBitDepth(): cannot find menu item by id'
            return
        menuItem.Check()
    
    def OnMenuVideoBackgroundColor(self, event=None, color=None, label=None):
        vidmenus = [self.videoWindow.contextMenu, self.GetMenuBar().GetMenu(2)]
        if event is not None:
            id = event.GetId()
            label = None
        elif color is not None:
            label = self.backgroundColorDict.get(color, _('Custom'))
        elif label is None:
            print>>sys.stderr, _('Error'), 'OnMenuVideoBackgroundColor(): a color or menuItem label is needed'
        updateMenu = None
        for vidmenu in vidmenus:
            menu = vidmenu.FindItemById(vidmenu.FindItem(_('Background &color'))).GetSubMenu()
            if label:
                id = menu.FindItem(label)
            menuItem = menu.FindItemById(id)
            if menuItem:
                menuItem.Check()
                label = menuItem.GetLabel()
                if label == _('Default'):
                    self.options['use_customvideobackground'] = False
                else:
                    self.options['use_customvideobackground'] = True
                    self.options['videobackground'] = self.backgroundLabelDict.get(
                        label, self.options['customvideobackground'])
                self.OnEraseBackground()
            else:
                updateMenu = menu
        if updateMenu is None:
            return
        id = updateMenu.FindItem(label)
        menuItem = updateMenu.FindItemById(id)
        if not menuItem:
            print>>sys.stderr, _('Error'), 'OnMenuVideoBackgroundColor(): cannot find menu item by id'
            return
        menuItem.Check()
    
    def OnMenuVideoSetCustomBackgroundColor(self, event):
        self.colour_data.SetColour(self.options['customvideobackground'])
        dialog = wx.ColourDialog(self, self.colour_data)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.GetColourData()
            self.options['customvideobackground'] = data.GetColour()
            self.OnMenuVideoBackgroundColor(label=_('Custom'))
            for i in range(self.colour_data.NUM_CUSTOM):
                self.colour_data.SetCustomColour(i, data.GetCustomColour(i))
            self.options['colourdata'] = self.colour_data.ToString()
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
        dialog.Destroy()
    
    def OnMenuVideoReuseEnvironment(self, event):
        self.reuse_environment = not self.reuse_environment
    
    def OnMenuVideoRefresh(self, event):
        self.ShowVideoFrame(forceRefresh=True, forceLayout=True, focus=self.options['focusonrefresh'])

    def OnMenuVideoHide(self, event):
        self.HidePreviewWindow()

    def OnMenuVideoReleaseMemory(self, event):
        self.HidePreviewWindow()
        for index in xrange(self.scriptNotebook.GetPageCount()):
            script = self.scriptNotebook.GetPage(index)
            script.AVI = None

    def OnMenuVideoToggle(self, event):
        if self.previewWindowVisible:
            if self.playing_video:
                self.PlayPauseVideo()
            self.HidePreviewWindow()
            self.SetStatusWidths([-1, 0])
        else:
            self.ShowVideoFrame(resize=True)

    def OnMenuVideoSwitchMode(self, event):
        if self.previewWindowVisible:
            if self.FindFocus() == self.videoWindow:
                self.currentScript.SetFocus()
                self.currentScript.EnsureCaretVisible()
            else:
                self.ShowVideoFrame()
        else:
            self.ShowVideoFrame()
    
    def OnMenuVideoTogglePlacement(self, event):
        self.TogglePreviewPlacement()
    
    def OnMenuVideoToggleSliderWindow(self, event):
        #~ self.OnLeftDClickVideoSplitter(None)
        self.ToggleSliderWindow(vidrefresh=True)
    
    def OnMenuVideoRunAnalysisPass(self, event):
        if self.playing_video:
            self.PlayPauseVideo()
        self.refreshAVI = True
        if self.UpdateScriptAVI(forceRefresh=True) is None:
            wx.MessageBox(_('Error loading the script'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        script = self.currentScript
        if script.AVI.IsErrorClip():
            wx.MessageBox(script.AVI.error_message, _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        progress = wx.ProgressDialog(message=_('Starting analysis pass...'), title=_('Run analysis pass'), 
                                     style=wx.PD_CAN_ABORT|wx.PD_ELAPSED_TIME|wx.PD_REMAINING_TIME)
        frame_count = script.AVI.Framecount
        initial_time = previous_time = time.time()
        previous_frame = -1
        for frame in range(frame_count):
            script.AVI.clip.get_frame(frame)
            error = script.AVI.clip.get_error()
            if error:
                progress.Destroy()
                wx.MessageBox(u'\n\n'.join((_('Error requesting frame {number}').format(number=frame), 
                              error)), _('Error'), style=wx.OK|wx.ICON_ERROR)
                return False
            now = time.time()
            delta = now - previous_time
            if delta > 0.1:
                fps = (frame - previous_frame) / delta
                previous_time = now
                previous_frame = frame
                if not progress.Update(frame * 100/ frame_count, 
                                       _('Frame %s/%s (%#.4g fps)') % (frame, frame_count, fps))[0]:
                    progress.Destroy()
                    return False
        elapsed_time = time.time() - initial_time
        progress.Update(100, _('Finished (%s fps average)') % (
                        '%#.4g' % (frame_count / elapsed_time) if elapsed_time else 'INF'))
        progress.Destroy()
        return True
    
    def OnMenuVideoPlay(self, event):
        self.PlayPauseVideo()
    
    def OnMenuVideoPlayDecrement(self, event):
        if self.play_speed_factor == 'max':
            self.play_speed_factor = 0.5
        else:
            self.play_speed_factor /= 2
        if self.playing_video:
            self.PlayPauseVideo()
            self.PlayPauseVideo()
    
    def OnMenuVideoPlayIncrement(self, event):
        if self.play_speed_factor == 'max':
            self.play_speed_factor = 2
        else:
            self.play_speed_factor *= 2
        if self.playing_video:
            self.PlayPauseVideo()
            self.PlayPauseVideo()
    
    def OnMenuVideoPlayNormal(self, event):
        self.play_speed_factor = 1.0
        if self.playing_video:
            self.PlayPauseVideo()
            self.PlayPauseVideo()
    
    def OnMenuVideoPlayMax(self, event):
        self.play_speed_factor = 'max'
        if self.playing_video:
            self.PlayPauseVideo()
            self.PlayPauseVideo()
    
    def OnMenuVideoPlayDropFrames(self, event):
        self.play_drop = not self.play_drop
    
    def OnMenuVideoExternalPlayer(self, event):
        self.RunExternalPlayer()
            
    def OnMenuVideoInfo(self, event):
        dlg = wx.Dialog(self, wx.ID_ANY, _('Video information'))
        vi = self.GetVideoInfoDict()
        labels = (
            (_('Video'),
                (
                (_('Frame size:'), '%ix%i (%s)' % (vi['width'], vi['height'], vi['aspectratio'])),
                (_('Length:'), '%i %s (%s)' % (vi['framecount'], _('frames'), vi['totaltime'])),
                (_('Frame rate:'), '%.03f %s (%i/%i)' % (vi['framerate'], _('fps'), vi['frameratenum'], vi['framerateden'])),
                (_('Colorspace:'), vi['colorspace']),
                (_('Field or frame based:'), vi['fieldframebased']),
                (_('Parity:'), vi['parity']),
                ),
            ),
            (_('Audio'),
                (
                (_('Channels:'), '%i' % (vi['audiochannels'])),
                (_('Sampling rate:'), '%i %s' % (vi['audiorate'], _('Hz'))),
                (_('Sample type:'), '%s %i %s' % (vi['audiotype'], vi['audiobits'], _('bits'))),
                (_('Length:'), '%i %s' % (vi['audiolength'], _('samples'))),
                ),
            ),
        )
        # Main items
        sizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=3)
        for sectionLabel, items in labels:
            staticText = wx.StaticText(dlg, wx.ID_ANY, sectionLabel)
            font = staticText.GetFont()
            #~ font.SetPointSize(10)
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            font.SetUnderlined(True)
            staticText.SetFont(font)
            sizer.Add(staticText, 0, wx.TOP, 5)
            sizer.Add((0,0), 0, 0)
            for label, value in items:
                sizer.Add(wx.StaticText(dlg, wx.ID_ANY, '  ' + label), 0, 0)
                sizer.Add(wx.StaticText(dlg, wx.ID_ANY, value), 0, 0)
        # Standard buttons
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        #~ cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        #~ btns.AddButton(cancel)
        btns.Realize()
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 5)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 10)
        dlg.SetSizer(dlgSizer)
        dlg.Fit()
        ID = dlg.ShowModal()
        dlg.Destroy()

    def OnMenuMacroRunSelected(self, event):
        id = event.GetId()
        macrofilename = self.macrosImportNames[id]
        menuItem = self.GetMenuBar().GetMenu(self.macroMenuPos).FindItemById(id)
        if menuItem.IsCheckable():
            menu = menuItem.GetMenu()
            self.RenameMacro(menu)
        else:
            self.macrosStack.append(id)
            self.ExecuteMacro(macrofilename)
            self.macrosStack.pop()

    def OnMenuMacrosFolder(self, event):
        if os.path.isdir(self.macrofolder):
            startfile(self.macrofolder)
        else:
            wx.MessageBox(_('Could not find the macros folder!'), _('Error'), style=wx.OK|wx.ICON_ERROR)

    def OnMenuMacrosReadme(self, event):
        readme = os.path.join(self.macrofolder, 'macros_readme.txt')
        if not os.path.isfile(readme):
            GenerateMacroReadme(readme)
        startfile(readme)
    
    def OnMenuToolsRunSelected(self, event):
        try:
            name = self.toolsImportNames[event.GetId()]
            obj = __import__(name)
        except (ImportError, KeyError):
            wx.MessageBox(_('Failed to import the selected tool'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        avsp = self.ExecuteMacro(return_env=True)
        #~ avsp.GetWindow = lambda: self
        obj.__dict__['_'] = _
        obj.__dict__['avsp'] = avsp
        obj.__dict__['avsp'].Version = dict(
            AvsP=self.version, 
            AviSynth_string=self.avisynthVersion[0], 
            AviSynth_number=self.avisynthVersion[1], 
            AviSynth_interface=self.avisynthVersion[2])
        obj.__dict__['last'] = self.macroVars['last']
        obj.__dict__['avsp'].Last = self.macroVars['last']
        self.macroVars['last'] = obj.avsp_run()

    def OnMenuOptionsAlwaysOnTop(self, event):
        id = event.GetId()
        menuItem = self.GetMenuBar().FindItemById(id)
        if not self.options['alwaysontop']:
            self.options['alwaysontop'] = True
            menuItem.Check(True)
        else:
            self.options['alwaysontop'] = False
            menuItem.Check(False)
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
    
    def OnMenuOptionsPreviewAlwaysOnTop(self, event):
        id = event.GetId()
        menuItem = self.GetMenuBar().FindItemById(id)
        if not self.options['previewalwaysontop']:
            self.options['previewalwaysontop'] = True
            menuItem.Check(True)
        else:
            self.options['previewalwaysontop'] = False
            menuItem.Check(False)
        if self.separatevideowindow:
            self.videoDialog.ToggleWindowStyle(wx.STAY_ON_TOP)
    
    def OnMenuOptionsSingleInstance(self, event):
        id = event.GetId()
        menuItem = self.GetMenuBar().FindItemById(id)
        if not self.options['singleinstance']:
            self.options['singleinstance'] = True
            menuItem.Check(True)
        else:
            self.options['singleinstance'] = False
            menuItem.Check(False)
        #~ wx.GetApp().boolSingleInstance = self.options['singleinstance']
        #~ self.SetWindowStyle(style)
        wx.MessageBox(_('You must restart for changes to take effect!'), _('Warning'))
        f = open(self.optionsfilename, mode='wb')
        cPickle.dump(self.options, f, protocol=0)
        f.close()

    def OnMenuOptionsFilters(self, event):
        self.ShowFunctionDefinitionDialog()

    def OnMenuOptionsFontsAndColors(self, event):
        dlgInfo = (
            (_('Basic (1)'),
                (
                    ((_('Use monospaced font:'), 'usemonospacedfont', _('Override all fonts to use a specified monospace font (no effect on scrap window)')), 'monospaced'),
                    (_('Default:'), 'default'),
                    (_('Comment:'), 'comment'),
                    (_('Block Comment:'), 'blockcomment'),
                    (_('__END__ Comment:'), 'endcomment'),
                    (_('Number:'), 'number'),
                    (_('String:'), 'string'),
                    (_('Triple-quoted string:'), 'stringtriple'),
                    (_('Assignment:'), 'assignment'),
                    (_('Operator:'), 'operator'),
                ),
            ),
            (_('Basic (2)'),
                (
                    (_('Internal filter:'), 'internalfilter'),
                    (_('External filter:'), 'externalfilter'),
                    (_('Internal function:'), 'internalfunction'),
                    (_('User defined function:'), 'userdefined'),
                    (_('Unknown function:'), 'unknownfunction'),
                    (_('Clip property:'), 'clipproperty'),
                    (_('Parameter:'), 'parameter'),
                    (_('AviSynth data type:'), 'datatype'),
                    (_('AviSynth keyword:'), 'keyword'),
                    (_('AvsP user slider:'), 'userslider'),
                ),
            ),
            (_('Advanced'),
                (
                    ((_('Incomplete string:'), 'usestringeol', _('Syntax highlight strings which are not completed in a single line differently')), 'stringeol'),
                    (_('Brace highlight:'), 'bracelight'),
                    (_('Bad brace:'), 'badbrace'),
                    (_('Bad number:'), 'badnumber'),
                    (_('Margin line numbers:'), 'linenumber'),
                    (_('Miscellaneous word:'), 'miscword'),
                    (_('Calltip:'), 'calltip'),
                    (_('Calltip highlight:'), 'calltiphighlight'),
                    (_('Cursor:'), 'cursor'),
                    ((_('Selection highlight:'), 'highlight_fore', _('If checked, highlight also foreground')), 'highlight'),
                    ((_('Current line highlight:'), 'highlightline', _('Highlight the line that the caret is currently in')), 'highlightline'),
                    (_('Fold margin:'), 'foldmargin'),
                    (_('Scrap window'), 'scrapwindow'),
                ),
            )
        )
        extra = None # adds a single CheckBox, (label, options_dict_key, tooltip)
        dlg = AvsStyleDialog(self, dlgInfo, self.options['textstyles'], self.defaulttextstylesDict, self.colour_data, extra)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            self.options['textstyles'] = dlg.GetDict()
            self.options.update(dlg.GetDict2())
            self.options['colourdata'] = self.colour_data.ToString()
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
            for index in xrange(self.scriptNotebook.GetPageCount()):
                script = self.scriptNotebook.GetPage(index)
                script.SetUserOptions()
            self.SetMinimumScriptPaneSize()
            self.scrapWindow.Style()
        dlg.Destroy()

    def OnMenuOptionsTemplates(self, event):
        # Build and show the dialog
        def keyChecker(key):
            msg = None
            if '.' in key:
                msg = '%s\n%s' % (_('Insert aborted:'), _("File extension shouldn't contain dots!"))
            return msg
        dlg = wxp.EditStringDictDialog(
            self,
            self.options['templates'],
            title=_('Edit extension-based templates'),
            keyTitle='  '+_('File extension'),
            valueTitle=_('Template'),
            editable=False,
            insertable=True,
            keyChecker=keyChecker,
            about='%s\n%s' % (
                _('This info is used for inserting sources based on file extensions.'),
                _('Any instances of *** in the template are replaced with the filename.')
            )+'\n'+_('(If you want relative paths instead of the full filename, use [***].)'),
        )
        ID = dlg.ShowModal()
        # Set the data
        if ID == wx.ID_OK:
            self.options['templates'] = dlg.GetDict()
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
        dlg.Destroy()

    def OnMenuOptionsSnippets(self, event):
        # Build and show the dialog
        def keyChecker(key):
            if not re.match(r'^\w+$', key):
                return '%s\n%s' % (_('Insert aborted:'), _('Only alphanumeric and underscores allowed!'))
        dlg = wxp.EditStringDictDialog(
            self,
            self.options['snippets'],
            title=_('Edit insertable text snippets'),
            keyTitle='  '+_('Tag'),
            valueTitle=_('Snippet'),
            editable=True,
            insertable=True,
            keyChecker=keyChecker,
            nag=False
        )
        ID = dlg.ShowModal()
        # Set the data
        if ID == wx.ID_OK:
            self.options['snippets'] = dlg.GetDict()
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
        dlg.Destroy()

    def OnMenuOptionsEnableLineByLineUpdate(self, event):
        id = event.GetId()
        menuItem = self.GetMenuBar().FindItemById(id)
        if not self.options['autoupdatevideo']:
            self.options['autoupdatevideo'] = True
            menuItem.Check(True)
        else:
            self.options['autoupdatevideo'] = False
            menuItem.Check(False)

    def OnMenuOptionsDisablePreview(self, event):
        id = event.GetId()
        menuItem = self.GetMenuBar().FindItemById(id)
        #~ splitlabel = menuItem.GetText().split('\t', 1)
        #~ acc = ''
        #~ if len(splitlabel) == 2:
            #~ acc = '\t' + splitlabel[1]
        if not self.options['disablepreview']:
            #~ if self.GetFrameNumber() != 0: #self.previewWindowVisible:
                #~ self.ShowVideoFrame(0)
            self.HidePreviewWindow()
            self.options['disablepreview'] = True
            #~ menuItem.SetText('%s%s' % (_('Video preview disabled'), acc))
            menuItem.Check(True)
            for ctrl in self.videoControlWidgets:
                ctrl.Disable()
                ctrl.Refresh()
        else:
            self.options['disablepreview'] = False
            #~ menuItem.SetText('%s%s' % (_('Disable the video preview'), acc))
            menuItem.Check(False)
            for ctrl in self.videoControlWidgets:
                ctrl.Enable()
                ctrl.Refresh()
    
    def OnMenuOptionsMonospaceFont(self, event):
        id = event.GetId()
        menuItem = self.GetMenuBar().FindItemById(id)
        if not self.options['usemonospacedfont']:
            self.options['usemonospacedfont'] = True
            menuItem.Check(True)
        else:
            self.options['usemonospacedfont'] = False
            menuItem.Check(False)
        for index in xrange(self.scriptNotebook.GetPageCount()):
            script = self.scriptNotebook.GetPage(index)
            script.SetTextStyles(self.options['textstyles'], self.options['usemonospacedfont'])

    def OnMenuOptionsEnableParanoiaMode(self, event):
        id = event.GetId()
        menuItem = self.GetMenuBar().FindItemById(id)
        if not self.options['paranoiamode']:
            self.options['paranoiamode'] = True
            menuItem.Check(True)
        else:
            self.options['paranoiamode'] = False
            menuItem.Check(False)
        f = open(self.optionsfilename, mode='wb')
        cPickle.dump(self.options, f, protocol=0)
        f.close()
    
    def OnMenuOptionsAssociate(self, event):
        if os.name == 'nt':
            s1 = _('Associating .avs files will write to the windows registry.')
            s2 = _('Do you wish to continue?')
            ret = wx.MessageBox('%s\n\n%s' % (s1, s2), _('Warning'), wx.YES_NO|wx.ICON_EXCLAMATION)
            if ret == wx.YES:
                try:
                    restore = 'avsp' in _winreg.QueryValue(_winreg.HKEY_CLASSES_ROOT, 'avsfile\\shell\\Open\\command').lower()
                except WindowsError:
                    restore = False
                ret = wx.MessageBox((_('Disassociate avs files for all users?') if restore else _('Associate avs files for all users?')) + 
                                     _(' Admin rights are needed.'), '', wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
                if ret != wx.CANCEL:
                    if hasattr(sys,'frozen'): # run in py2exe binary mode
                        value = u'"%s" "%%1"' % sys.executable
                    else: # run in source mode
                        script = os.path.join(self.programdir, 'run.py')
                        value = u'"%s" -O "%s" "%%1"' % (sys.executable, script)
                    f = tempfile.NamedTemporaryFile(delete=False)
                    if restore:
                        txt = textwrap.dedent(u'''\
                        HKCU\\Software\\Classes\\avsfile\\shell\\Open\\command
                        = notepad "%1"
                        HKCU\\Software\\Classes\\avs_auto_file\\shell\\Open\\command
                        = notepad "%1"''')
                        if ret == wx.YES:
                            txt += textwrap.dedent(u'''
                            HKLM\\Software\\Classes\\avsfile\\shell\\Open\\command
                            = notepad "%1"
                            HKLM\\Software\\Classes\\avs_auto_file\\shell\\Open\\command
                            = notepad "%1"''')
                    else:
                        txt = textwrap.dedent(u'''\
                        HKCU\\Software\\Classes\\avsfile\\shell\\Open\\command
                        = "{value}"
                        HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.avs
                        "Application" = DELETE
                        HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.avs\\UserChoice
                        HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.avs\\UserChoice [DELETE]
                        HKCU\\Software\\Classes\\avs_auto_file\\shell\\Open\\command
                        = "{value}"
                        HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.avsi
                        "Application" = DELETE
                        HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.avsi\\UserChoice
                        HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.avsi\\UserChoice [DELETE]
                        ''').format(value=value)
                        if ret == wx.YES:
                            txt += textwrap.dedent(u'''
                            HKLM\\Software\\Classes\\avsfile\\shell\\Open\\command
                            = "{value}"
                            HKLM\\Software\\Classes\\avs_auto_file\\shell\\Open\\command
                            = "{value}"''').format(value=value)
                    f.write(txt.encode('utf16'))
                    f.close()
                    if ret == wx.YES:
                        ctypes.windll.shell32.ShellExecuteW(None, u'runas', u'cmd', u'/k "regini "{f}" & del "{f}""'.format(f=f.name.decode(encoding)), None, 0)
                    else:
                        os.system('regini "{f}" & del "{f}"'.format(f=f.name))
        else:
            app_file = os.path.join(tempfile.gettempdir(), global_vars.name.lower() + '.desktop')
            with open(app_file, 'w') as f:
                txt = textwrap.dedent('''\
                [Desktop Entry]
                Version=1.0
                Name={name}
                GenericName=Video Editor
                Comment={comment}
                Type=Application
                Exec=python -O {dir}/run.py %F
                Terminal=false
                StartupNotify=true
                Icon={dir}/AvsP.ico
                Categories=AudioVideo;
                MimeType=text/x-avisynth;''').format(name=self.name, 
                    comment=global_vars.description, dir=self.programdir)
                f.write(txt)
            if 'avsp' in subprocess.check_output(['xdg-mime', 'query', 'default', 'text/x-avisynth']):
                text_editor = subprocess.check_output(['xdg-mime', 'query', 'default', 'text/plain']).strip()
                os.system('xdg-desktop-menu uninstall {0} && '
                          'xdg-mime default {1} text/x-avisynth'.format(app_file, text_editor))
            else:
                mime_file = os.path.join(tempfile.gettempdir(), 'avisynth.xml')
                with open(mime_file, 'w') as f:
                    txt = textwrap.dedent('''\
                    <?xml version="1.0"?>
                    <mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
                      <mime-type type="text/x-avisynth">
                        <comment>AviSynth script</comment>
                        <glob pattern="*.avs"/>
                        <glob pattern="*.avsi"/>
                      </mime-type>
                    </mime-info>''')
                    f.write(txt)
                os.system('xdg-mime install --novendor {mime_file} && '
                          'xdg-desktop-menu install --novendor {app_file} && '
                          'xdg-mime default {app_file} text/x-avisynth'.format(mime_file=mime_file, app_file=app_file))
                os.remove(mime_file)
            os.remove(app_file)
    
    def OnMenuConfigureShortcuts(self, event):
        #~ exceptionIds = []
        #~ for window, idList in self._shortcutBindWindowDict.items():
            #~ if window != self:
                #~ exceptionIds += idList
        exceptionIds = (
            self.exceptionShortcuts, 
            self.stcShortcuts,
            self.options['reservedshortcuts'], 
            _('Above keys are built-in editing shortcuts. If item is checked,\n'
              'it will not be overrided by a menu shortcut in script window.')
        )
        dlg = wxp.ShortcutsDialog(self, self.options['shortcuts'], exceptionIds=exceptionIds,
                                  submessage=_('* This shortcut is active only when video window has focus.\n'
                                               '~ This shortcut is active only when script window has focus.'))
        ID = dlg.ShowModal()
        # Set the data
        if ID == wx.ID_OK:
            shortcutList, reservedShortcuts = dlg.GetShortcutList()
            for old, new in zip(self.options['shortcuts'], shortcutList):
                if old != new:
                    menuString, shortcut, id = new
                    menuItem = self.GetMenuBar().FindItemById(id)
                    label = menuItem.GetLabel()
                    if shortcut != '':
                        shortcut = u'\t%s\u00a0' % wxp.GetTranslatedShortcut(shortcut)
                        if os.name != 'nt' and wx.version() >= '2.9': # XXX
                            shortcut = shortcut[:-1]
                    newLabel = '%s%s' % (label, shortcut)
                    menuItem.SetItemLabel(newLabel)
            self.options['shortcuts'] = shortcutList
            self.options['reservedshortcuts'] = reservedShortcuts
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
            self.bindShortcutsToAllWindows()
        dlg.Destroy()

    def OnMenuOptionsSettings(self, event):
        self.ShowOptions()

    def OnMenuHelpAvisynth(self, event):
        helpfile = self.ExpandVars(self.options['avisynthhelpfile'])
        # Check if the given doc path exists on the computer or is a url
        if os.path.isfile(helpfile) or helpfile.startswith('http://'):
            startfile(helpfile)
            return True
        # Give a message if not a file or a url
        wx.MessageBox('Could not find avisynth help file!', _('Error'), style=wx.OK|wx.ICON_ERROR)

    def OnMenuHelpAvisynthPlugins(self, event):
        plugindir = self.options['recentdirPlugins']
        if not os.path.isdir(plugindir):
            plugindir = self.ExpandVars(self.options['pluginsdir'])
        if os.path.isdir(plugindir):
            startfile(plugindir)
        else:
            wx.MessageBox(_('Could not find the Avisynth plugins folder!'), _('Error'), style=wx.OK|wx.ICON_ERROR)

    def OnMenuHelpAnimatedTutorial(self, event):
        filename = os.path.join(self.helpdir, 'Demo.htm')
        if os.path.isfile(filename):
            startfile(filename)
        else:
            startfile('http://avisynth.nl/users/qwerpoi/Demo.htm')

    def OnMenuHelpTextFeatures(self, event):
        filename = os.path.join(self.helpdir, 'Text.html')
        if os.path.isfile(filename):
            startfile(filename)
        else:
            startfile('http://avisynth.nl/users/qwerpoi/Text.html')

    def OnMenuHelpVideoFeatures(self, event):
        filename = os.path.join(self.helpdir, 'Video.html')
        if os.path.isfile(filename):
            startfile(filename)
        else:
            startfile('http://avisynth.nl/users/qwerpoi/Video.html')

    def OnMenuHelpUserSliderFeatures(self, event):
        filename = os.path.join(self.helpdir, 'UserSliders.html')
        if os.path.isfile(filename):
            startfile(filename)
        else:
            startfile('http://avisynth.nl/users/qwerpoi/UserSliders.html')

    def OnMenuHelpMacroFeatures(self, event):
        filename = os.path.join(self.helpdir, 'Macros.html')
        if os.path.isfile(filename):
            startfile(filename)
        else:
            startfile('http://avisynth.nl/users/qwerpoi/Macros.html')

    def OnMenuHelpReadme(self, event):
        readme = os.path.join(self.programdir, 'readme.txt')
        if os.path.isfile(readme):
            startfile(readme)
        else:
            wx.MessageBox(_('Could not find %(readme)s!') % locals(), _('Error'), style=wx.OK|wx.ICON_ERROR)

    def OnMenuHelpChangelog(self, event):
        changelog = os.path.join(self.programdir, 'changelog.txt')
        if os.path.isfile(changelog):
            startfile(changelog)
        else:
            wx.MessageBox(_('Could not find %(changelog)s!') % locals(), _('Error'), style=wx.OK|wx.ICON_ERROR)
    
    def OnMenuHelpAbout(self, event):
        prog_name = global_vars.name
        version = self.version
        arch = u'{0} {1}'.format(platform.system(), 'x86-64' if self.x86_64 else 'x86-32')
        dlg = wx.Dialog(self, wx.ID_ANY, _('About AvsPmod'), size=(220,180))
        bmp = AvsP_icon.getBitmap()
        logo = wx.StaticBitmap(dlg, wx.ID_ANY, bmp)
        title = wx.StaticText(dlg, wx.ID_ANY, _('{prog_name} v{version} ({arch})').format(**locals()))
        font = title.GetFont()
        font.SetPointSize(12)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        description = wx.StaticText(dlg, wx.ID_ANY, _(global_vars.description))
        link = wx.StaticText(dlg, wx.ID_ANY, _('AvsP Website'))
        font = link.GetFont()
        font.SetUnderlined(True)
        link.SetFont(font)
        link.SetForegroundColour(wx.Colour(0,0,255))
        link.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        url = 'http://avisynth.nl/users/qwerpoi/'
        def OnClick(event):
            startfile(url)
        link.SetToolTip(wx.ToolTip(url))
        link.Bind(wx.EVT_LEFT_DOWN, OnClick)
        
        link0 = wx.StaticText(dlg, wx.ID_ANY, _("AvsPmod Website"))
        font = link0.GetFont()
        font.SetUnderlined(True)
        link0.SetFont(font)
        link0.SetForegroundColour(wx.Colour(0,0,255))
        link0.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        url0 = global_vars.url
        def OnClick0(event):
            startfile(url0)
        link0.SetToolTip(wx.ToolTip(url0))
        link0.Bind(wx.EVT_LEFT_DOWN, OnClick0)
        
        link1 = wx.StaticText(dlg, wx.ID_ANY, _("Active thread on Doom9's forum"))
        font = link1.GetFont()
        font.SetUnderlined(True)
        link1.SetFont(font)
        link1.SetForegroundColour(wx.Colour(0,0,255))
        link1.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        url1 = 'http://forum.doom9.org/showthread.php?t=153248'
        def OnClick1(event):
            startfile(url1)
        link1.SetToolTip(wx.ToolTip(url1))
        link1.Bind(wx.EVT_LEFT_DOWN, OnClick1)
        
        staticText = wx.StaticText(dlg, wx.ID_ANY, _('This program is freeware under the GPL license.'))
        url2 = 'http://www.gnu.org/copyleft/gpl.html'
        link2 = wx.StaticText(dlg, wx.ID_ANY, url2)
        font = link2.GetFont()
        font.SetUnderlined(True)
        link2.SetFont(font)
        link2.SetForegroundColour(wx.Colour(0,0,255))
        link2.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        def OnClick2(event):
            startfile(url2)
        link2.SetToolTip(wx.ToolTip(url2))
        link2.Bind(wx.EVT_LEFT_DOWN, OnClick2)

        button = wx.Button(dlg, wx.ID_OK, _('OK'))
        inner = wx.BoxSizer(wx.HORIZONTAL)
        inner.Add(logo, 0, wx.LEFT, 10)
        inner.Add(title, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 10)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(inner, 0, wx.TOP, 20)
        sizer.Add(description, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        sizer.Add(link0, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(link1, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(link, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add((0,5), 0, wx.EXPAND)
        sizer.Add(wx.StaticLine(dlg), 0, wx.EXPAND|wx.TOP, 10)
        sizer.Add(staticText, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(link2, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        dlg.SetSizer(sizer)
        dlg.Layout()
        dlg.Fit()
        dlg.ShowModal()
        dlg.Destroy()

    def OnButtonTextSetFocus(self, event):
        self.SetStatusText(_('Input a frame number or time (hr:min:sec) and hit Enter. Right-click to retrieve from history.'))
        frameTextCtrl = event.GetEventObject()
        frameTextCtrl.SetForegroundColour(wx.BLACK)
        wx.CallAfter(frameTextCtrl.SetSelection, -1, -1)
        event.Skip()

    def OnButtonTextKillFocus(self, event):
        frameTextCtrl = event.GetEventObject()
        txt = frameTextCtrl.GetLineText(0)
        if txt and txt not in self.recentframes:
            self.recentframes.append(txt)
        win = self.FindFocus()
        if  win != frameTextCtrl:
            frame = self.videoSlider.GetValue()
            bms = self.GetBookmarkFrameList()
            if frame in bms and bms[frame] == 0:
                color = wx.RED
            else:
                color = wx.BLACK
            self.frameTextCtrl.SetForegroundColour(color)
            self.frameTextCtrl.Replace(0, -1, str(frame))
            return
        try:
            frame = int(txt)
        except ValueError:
            timetxt = txt.split(':')
            if len(timetxt) == 2:
                timetxt.insert(0, 0)
            try:
                if len(timetxt) != 3: raise
                hours = int(timetxt[0])
                if hours < 0: raise
                minutes = int(timetxt[1])
                if minutes < 0 or minutes >= 60: raise
                seconds = float(timetxt[2])
                if seconds < 0 or seconds >= 60: raise
                total = hours * 60 * 60 + minutes * 60 + seconds
                frame = int(round(self.currentScript.AVI.Framerate * total))                
            except:
                frame = -2
        if frame == -1:
            frame = self.currentScript.AVI.Framecount - 1
        if frame < 0 or (self.currentScript.AVI and frame >= self.currentScript.AVI.Framecount):
            wx.Bell()
            return
        if not self.separatevideowindow:
            self.ShowVideoFrame(frame)
        else:
            if event is not None and event.GetEventObject() in self.videoControlWidgets and self.previewWindowVisible:
                self.ShowVideoFrame(frame, focus=False)
                self.currentScript.SetFocus()
            else:
                self.ShowVideoFrame(frame)
        
    def OnButtonTextContextMenu(self, event):
        textCtrl = event.GetEventObject()
        menu = wx.Menu()
        def OnContextMenuCopyTime(event):
            frame = self.GetFrameNumber()
            try:
                m, s = divmod(frame/self.MacroGetVideoFramerate(), 60)
            except:
                return
            h, m = divmod(m, 60)
            timecode = '%02d:%02d:%06.3f' % (h ,m, s)
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
                wx.TheClipboard.SetData(wx.TextDataObject(timecode))
                wx.TheClipboard.Close()

        def OnContextMenuCopy(event):
            text = textCtrl.GetStringSelection()
            if not text:
                text = textCtrl.GetLineText(0)
            if text and not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
                wx.TheClipboard.SetData(wx.TextDataObject(text))
                wx.TheClipboard.Close()
                
        def OnContextMenuPaste(event):
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
                text = wx.TextDataObject('')
                if wx.TheClipboard.GetData(text):
                    text = text.GetText()
                    if text:
                        frm, to = textCtrl.GetSelection()
                        if textCtrl.FindFocus() != textCtrl:
                            frm, to = 0, -1
                        textCtrl.Replace(frm, to, text)                                                
                        textCtrl.SetFocus()
                wx.TheClipboard.Close()
                
        def OnContextMenuClear(event):
            self.recentframes = []
                
        def OnContextMenuItem(event):
            item = menu.FindItemById(event.GetId())
            textCtrl.Replace(0, -1, item.GetItemLabelText())
            textCtrl.SetFocus()
            
        for text in self.recentframes:
            id = wx.NewId()
            self.Bind(wx.EVT_MENU, OnContextMenuItem, id=id)
            menu.Append(id, text)
        menu.AppendSeparator()
        id = wx.NewId()
        self.Bind(wx.EVT_MENU, OnContextMenuCopyTime, id=id)
        menu.Append(id, _('copy as time'))
        id = wx.NewId()
        self.Bind(wx.EVT_MENU, OnContextMenuCopy, id=id)
        menu.Append(id, _('copy'))
        id = wx.NewId()
        self.Bind(wx.EVT_MENU, OnContextMenuPaste, id=id)
        menu.Append(id, _('paste'))
        id = wx.NewId()
        self.Bind(wx.EVT_MENU, OnContextMenuClear, id=id)
        menu.Append(id, _('clear history'))
        self.PopupMenu(menu)
        menu.Destroy()

    def OnSliderChanged(self, event):
        if self.playing_video:
            self.PlayPauseVideo()
            self.playing_video = ''
        videoSlider = event.GetEventObject()
        frame = videoSlider.GetValue()
        if self.options['dragupdate']:
            if not self.separatevideowindow:
                self.ShowVideoFrame(frame, adjust_handle=True)
            else:
                if event is not None and event.GetEventObject() in self.videoControlWidgets and self.previewWindowVisible:
                    self.ShowVideoFrame(frame, adjust_handle=True, focus=False)
                    self.currentScript.SetFocus()
                else:
                    self.ShowVideoFrame(frame, adjust_handle=True)
        bms = self.GetBookmarkFrameList()
        if frame in bms and bms[frame] == 0:
            color = wx.RED
        else:
            color = wx.BLACK
        self.frameTextCtrl.SetForegroundColour(color)
        self.frameTextCtrl.Replace(0, -1, str(frame))
        if self.separatevideowindow:
            self.frameTextCtrl2.SetForegroundColour(color)
            self.frameTextCtrl2.Replace(0, -1, str(frame))
        self.SetVideoStatusText()
        #~ self.videoWindow.SetFocus()

    def OnSliderReleased(self, event):
        if self.playing_video:
            self.PlayPauseVideo()
            self.playing_video = ''
        videoSlider = event.GetEventObject()
        #~ if self.FindFocus() != videoSlider:
            #~ return
        frame = videoSlider.GetValue()
        if not self.separatevideowindow:
            self.ShowVideoFrame(frame, adjust_handle=videoSlider.adjust_handle)
        else:
            if event is not None and event.GetEventObject() in self.videoControlWidgets and self.previewWindowVisible:
                self.ShowVideoFrame(frame, adjust_handle=videoSlider.adjust_handle, focus=False)
                self.currentScript.SetFocus()
            else:
                self.ShowVideoFrame(frame, adjust_handle=videoSlider.adjust_handle)
        self.videoWindow.SetFocus()
        if self.playing_video == '':
            self.PlayPauseVideo()

    def OnSliderRightUp(self, event):
        slider = event.GetEventObject()
        mousepos = event.GetPosition()
        if slider.HitTestHandle(mousepos):
            frame = slider.GetValue()
            self.AddFrameBookmark(frame, toggle=True)
            colors = [wx.RED, wx.BLACK]
            colors.remove(self.frameTextCtrl.GetForegroundColour())
            self.frameTextCtrl.SetForegroundColour(colors[0])
            self.frameTextCtrl.Refresh()
            if self.separatevideowindow:
                self.frameTextCtrl2.SetForegroundColour(colors[0])
                self.frameTextCtrl2.Refresh()
            if colors[0] == wx.BLACK and frame in self.bookmarkDict and (event.ControlDown() or event.AltDown() or event.ShiftDown()):
                del self.bookmarkDict[frame]
        #~ else:
            #~ index = slider.HitTestBookmark(mousepos)
            #~ if index is not None:
                #~ bookmarks = slider.GetBookmarks()
                #~ value, bmtype = bookmarks[index]
                #~ bmtype += 1
                #~ if bmtype > 2:
                    #~ bmtype = 0
                #~ self.AddFrameBookmark(value, bmtype, toggle=False)
        event.Skip()

    def OnSliderMiddleDown(self, event):
        slider = event.GetEventObject()
        mousepos = event.GetPosition()
        index = slider.HitTestBookmark(mousepos)
        if index is not None:
            bookmarks = slider.GetBookmarks()
            bmtype = bookmarks[index]
            self.DeleteFrameBookmark(index, bmtype)            
            if index in self.bookmarkDict and (event.ControlDown() or event.AltDown() or event.ShiftDown()):
                del self.bookmarkDict[index]
            self.frameTextCtrl.SetForegroundColour(wx.BLACK)
            self.frameTextCtrl.Refresh()
            if self.separatevideowindow:
                self.frameTextCtrl2.SetForegroundColour(wx.BLACK)
                self.frameTextCtrl2.Refresh()

    def OnSliderLeftUp(self, event):
        slider = event.GetEventObject()
        mousepos = event.GetPosition()
        # If clicked on a selection button, create the selection bookmark
        bmtype = slider.HitTestSelectionButton(mousepos)
        if bmtype is not None:
            value = self.GetFrameNumber()
            # bookmarks = list(self.GetBookmarkFrameList().items())
            self.AddFrameBookmark(value, bmtype)
            #~ if bookmarks.count((value, bmtype)) == 0:
                #~ self.AddFrameBookmark(value, bmtype)
            #~ else:
                #~ slider.RemoveBookmark(value, bmtype)
        event.Skip()

    def OnNotebookPageChanged(self, event):
        # Get the newly selected script
        script = self.scriptNotebook.GetPage(event.GetSelection())

        # Set some related key variables (affects other functions)
        self.currentScript = script
        self.refreshAVI = True

        oldSliderWindow = self.currentSliderWindow
        newSliderWindow = script.sliderWindow
        oldSliderWindow.Hide()
        self.currentSliderWindow = newSliderWindow

        # Determine whether to hide the preview or not
        if self.previewWindowVisible:
            forceRefresh = False
            if self.zoomwindow:
                #~ if script.lastSplitVideoPos != self.lastSplitVideoPos:
                    #~ forceRefresh=True
                pass
            #~ if self.zoomwindowfit:
                #~ forceRefresh=True
            if self.UpdateScriptAVI(script, forceRefresh=forceRefresh, prompt=True) is None:
                self.HidePreviewWindow()
                return False
            if (script.AVI.Width, script.AVI.Height) == self.oldVideoSize:
                script.lastSplitVideoPos = self.oldLastSplitVideoPos
                boolSliders = bool(script.sliderTexts or script.sliderProperties or script.toggleTags or script.autoSliderInfo)
                #~ if boolSliders and self.oldBoolSliders:
                if boolSliders and self.oldBoolSliders:
                    #~ if not script.sliderWindowShown and self.oldSliderWindowShown:
                        #~ script.sliderWindowShown = True
                    if self.oldSliderWindowShown != script.sliderWindowShown:
                        script.sliderWindowShown = self.oldSliderWindowShown
                    if self.oldSliderWindowShown is True and script.sliderWindowShown is True:
                        script.lastSplitSliderPos = self.oldLastSplitSliderPos
                    #~ elif self.oldSliderWindowShown != script.sliderWindowShown:
                        #~ script.sliderWindowShown = self.oldSliderWindowShown
                if script.group == self.oldGroup is None and script.AVI.Framecount == self.videoSlider.GetMax()+1 and self.options['enableframepertab']:
                    script.lastFramenum = None
            if script.group is not None and script.group == self.oldGroup:
                if self.options['applygroupoffsets']:
                    offset = script.group_frame - self.oldGroupFrame
                    script.lastFramenum = max(0, self.oldLastFramenum + offset)
                    if self.options['offsetbookmarks']:
                        self.OffsetBookmarks(offset)
                else:
                    script.lastFramenum = None
            elif script.group == self.oldGroup is None and self.options['enableframepertab'] and not self.options['enableframepertab_same']:
                script.lastFramenum = None
            if self.zoomwindowfit:
                script.lastSplitVideoPos = self.oldLastSplitVideoPos
                #~ self.ShowVideoFrame(forceRefresh=True, focus=False)
                #~ self.IdleCall = (self.ShowVideoFrame, tuple(), {'forceRefresh': True, 'focus': False})
                self.IdleCall.append((self.ShowVideoFrame, tuple(), {'focus': False}))
            else:
                self.ShowVideoFrame(forceLayout=True, focus=False)
            #~ if script.sliderWindowShown != self.oldSliderWindowShown:
                #~ # Force a reset
                #~ script.sliderWindowShown = not script.sliderWindowShown
                #~ self.ToggleSliderWindow()
                #~ if script.sliderWindowShown:
                    #~ newSliderWindow.Show()
            if not script.sliderWindowShown:
                self.HideSliderWindow(script)
            else:
                newSliderWindow.Show()
                self.ShowSliderWindow(script)
        else: # Update slider position and frame text control
            frame = script.lastFramenum
            if frame is not None:
                bms = self.GetBookmarkFrameList()
                if frame in bms and bms[frame] == 0:
                    color = wx.RED
                else:
                    color = wx.BLACK
                self.frameTextCtrl.SetForegroundColour(color)
                self.frameTextCtrl.Replace(0, -1, str(frame))
                if self.separatevideowindow:
                    self.frameTextCtrl2.SetForegroundColour(color)
                    self.frameTextCtrl2.Replace(0, -1, str(frame))
                if script.lastLength is not None:
                    self.videoSlider.SetRange(0, script.lastLength - 1, refresh=False)
                    if self.separatevideowindow:
                        self.videoSlider2.SetRange(0, script.lastLength - 1, refresh=False)
                    self.videoSlider.SetValue(frame)
                elif frame == 0:
                    self.videoSlider.SetValue(0)
        
        #~ # Update visuals...
        #~ if script.sliderWindowShown:
            #~ newSliderWindow.Show()
            #~ if self.videoSplitter.IsSplit():# and self.videoSplitter.GetWindow2() == oldSliderWindow:
                #~ self.videoSplitter.ReplaceWindow(oldSliderWindow, newSliderWindow)
            #~ else:
                #~ self.videoSplitter.SplitVertically(self.videoWindow, newSliderWindow, script.lastSplitSliderPos)
        
        # Misc
        #~ if not self.previewWindowVisible:
            #~ script.SetFocus()
        if self.boolVideoWindowFocused:
            self.videoWindow.SetFocus()
        elif self.findDialog.IsShown():
            self.findDialog.SetFocus()
        elif self.replaceDialog.IsShown():
            self.replaceDialog.SetFocus()
        else:
            script.SetFocus()
        self.SetVideoStatusText()
        self.UpdateProgramTitle()
        self.oldlinenum = None

    def OnNotebookPageChanging(self, event):
        if self.cropDialog.IsShown():
            wx.MessageBox(_('Cannot switch tabs while crop editor is open!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            event.Veto()
        if self.trimDialog.IsShown():
            wx.MessageBox(_('Cannot switch tabs while trim editor is open!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            event.Veto()
        if self.playing_video:
            self.PlayPauseVideo()
        if self.FindFocus() == self.videoWindow:
            self.boolVideoWindowFocused = True
        else:
            self.boolVideoWindowFocused = False
        oldSelectionIndex = event.GetOldSelection()
        if oldSelectionIndex >= 0:
            oldScript = self.scriptNotebook.GetPage(oldSelectionIndex)
            self.oldLastFramenum = oldScript.lastFramenum
            self.oldGroup = oldScript.group
            self.oldGroupFrame = oldScript.group_frame
        if self.previewWindowVisible:
            if oldSelectionIndex >= 0:
                if oldScript.lastSplitVideoPos is not None:
                    self.oldLastSplitVideoPos = oldScript.lastSplitVideoPos
                else:
                    self.oldLastSplitVideoPos = oldScript.lastSplitVideoPos
                    #~ self.oldLastSplitVideoPos = self.mainSplitter.GetSashPosition() - self.mainSplitter.GetClientSize()[1]
                self.oldLastSplitSliderPos = oldScript.lastSplitSliderPos
                self.oldSliderWindowShown = oldScript.sliderWindowShown
                self.oldBoolSliders = bool(oldScript.sliderTexts or oldScript.sliderProperties or oldScript.toggleTags or oldScript.autoSliderInfo)
                self.oldVideoSize = (oldScript.AVI.Width, oldScript.AVI.Height)
            else:
                self.oldLastSplitVideoPos = None
                self.oldLastSplitSliderPos = None
                self.oldBoolSliders = None
                self.oldVideoSize = (None, None)

    def OnMiddleDownNotebook(self, event):
        ipage = self.scriptNotebook.HitTest(event.GetPosition())[0]
        if ipage != wx.NOT_FOUND:
            self.CloseTab(ipage, prompt=True)
        else: # for wxGTK
            self.UndoCloseTab()
    
    def OnLeftDownNotebook(self, event):
        self.scriptNotebook.dragging = False
        self.scriptNotebook.oldpage = self.scriptNotebook.GetSelection()
        event.Skip()
            
    def OnLeftUpNotebook(self, event):
        if self.scriptNotebook.dragging:
            self.scriptNotebook.dragging = False
            self.scriptNotebook.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
            if not self.scriptNotebook.dblClicked:
                index = self.scriptNotebook.GetSelection()
                ipage = self.scriptNotebook.HitTest(event.GetPosition())[0]
                if ipage != wx.NOT_FOUND and ipage != index:
                    self.RepositionTab(ipage)
            else:
                wx.CallLater(300, setattr, self.scriptNotebook, 'dblClicked' ,False) 
        else:
            pos = event.GetPosition()
            ipage = self.scriptNotebook.HitTest(pos)[0]
            if ipage == self.scriptNotebook.oldpage:
                wx.CallLater(300, self.OnMenuFileRenameTab, ipage, pos)
        event.Skip()
            
    def OnLeftDClickNotebook(self, event):
        if self.titleEntry:
            return
        self.scriptNotebook.dblClicked = True
        ipage = self.scriptNotebook.HitTest(event.GetPosition())[0]
        if ipage != wx.NOT_FOUND:
            self.NewTab(copytab=True)
        else: # for wxGTK
            self.NewTab()

    def OnRightClickNotebook(self, event):
        win = event.GetEventObject()
        pos = event.GetPosition()
        ipage = self.scriptNotebook.HitTest(pos)[0]
        if ipage != wx.NOT_FOUND:
            script, index = self.getScriptAtIndex(ipage)
            try:
                menu = win.contextMenu
                self.scriptNotebook.SetSelection(index)
                # group
                group_menu = menu.FindItemById(menu.FindItem(_('Group'))).GetSubMenu()
                group = script.group
                if group is None:
                    group = _('None')
                id = group_menu.FindItem(group)
                group_menu.Check(id, True)
                id = group_menu.FindItem(_('Apply offsets'))
                group_menu.Check(id, self.options['applygroupoffsets'])
                id = group_menu.FindItem(_('Offset also bookmarks'))
                group_menu.Check(id, self.options['offsetbookmarks'])
                # reposition
                menuItem = menu.FindItemByPosition(menu.GetMenuItemCount()-1)
                menu = menuItem.GetSubMenu()
                for i in range(menu.GetMenuItemCount()):
                    menu.DestroyItem(menu.FindItemByPosition(0))
                for i in range(self.scriptNotebook.GetPageCount()):
                    label = self.scriptNotebook.GetPageText(i)
                    menuItem = menu.Insert(i, wx.ID_ANY, label)                
                    if i != index:
                        self.Bind(wx.EVT_MENU, self.RepositionTab, menuItem)
                    else:
                        menuItem.Enable(False)
                win.PopupMenu(win.contextMenu, pos)
            except AttributeError:
                pass
    
    def OnGroupApplyOffsets(self, event):
        self.options['applygroupoffsets'] = not self.options['applygroupoffsets']
    
    def OnGroupOffsetBookmarks(self, event):
        self.options['offsetbookmarks'] = not self.options['offsetbookmarks']
    
    def OnGroupClearTabGroup(self, event=None, group=None):
        if group is None:
            group = self.currentScript.group
            if group is None:
                return
        for index in xrange(self.scriptNotebook.GetPageCount()):
            script = self.scriptNotebook.GetPage(index)
            if script.group == group:
                self.AssignTabGroup(None, index)
    
    def OnGroupClearAllTabGroups(self, event):
        for index in xrange(self.scriptNotebook.GetPageCount()):
            self.AssignTabGroup(None, index)
    
    def OnGroupAssignTabGroup(self, event):
        id = event.GetId()
        context_menu = event.GetEventObject()
        group_menu = context_menu.FindItemById(context_menu.FindItem(_('Group'))).GetSubMenu()
        label = group_menu.FindItemById(id).GetLabel()
        self.AssignTabGroup(label)
    
    def AssignTabGroup(self, group, index=None):
        if group == _('None'):
            group = None
        current_tab = self.scriptNotebook.GetSelection()
        if index is None:
            index = current_tab
        script = self.scriptNotebook.GetPage(index)
        script.group = group
        script.group_frame = script.lastFramenum
        self.UpdateScriptTabname(index=index)
    
    def OnMouseMotionNotebook(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.scriptNotebook.dragging = True
            if self.titleEntry:
                self.scriptNotebook.SetFocus()
            index = self.scriptNotebook.GetSelection()
            ipage = self.scriptNotebook.HitTest(event.GetPosition())[0]
            if ipage != wx.NOT_FOUND:
                self.scriptNotebook.SetCursor(wx.CursorFromImage(dragdrop_cursor.GetImage()))
            else:
                self.scriptNotebook.SetCursor(wx.StockCursor(wx.CURSOR_NO_ENTRY))
        else:
            self.scriptNotebook.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

    
    def OnMouseWheelNotebook(self, event):
        '''Rotate between tabs'''
        rotation = event.GetWheelRotation()
        if self.mouse_wheel_rotation * rotation < 0:
            self.mouse_wheel_rotation = rotation
        else:
            self.mouse_wheel_rotation += rotation
        if abs(self.mouse_wheel_rotation) >= event.GetWheelDelta():
            inc = -1 if self.mouse_wheel_rotation > 0 else 1 
            if self.options['invertscrolling']: inc = -inc
            self.SelectTab(inc=inc)
            self.mouse_wheel_rotation = 0
    
    def OnLeftDClickWindow(self, event):
        x, y = event.GetPosition()
        if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            new_tab = y < self.currentScript.GetPosition().y
            pos = y
        else:
            new_tab = y < self.currentScript.GetPosition().y and \
                      x < self.currentScript.GetSize().width
            pos = x
        if new_tab: # event not received on wxGTK
            self.NewTab()
        else:
            lo = self.mainSplitter.GetSashPosition()
            hi = lo + self.mainSplitter.GetSashSize()
            if lo <= pos <= hi and self.mainSplitter.IsSplit():
                #~ self.SplitVideoWindow(forcefit=True)
                self.currentScript.lastSplitVideoPos = None
                if not self.zoomwindow:
                    self.LayoutVideoWindows(forcefit=True)
                else:
                    self.LayoutVideoWindows(forcefit=True)
                    #~ self.ShowVideoFrame(forceRefresh=True)
                    self.ShowVideoFrame()

    def OnMiddleDownWindow(self, event):
        x, y = event.GetPosition()
        if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            if y < self.currentScript.GetPosition().y: # event not received on wxGTK
                self.UndoCloseTab()
        else:
            if y < self.currentScript.GetPosition().y and \
               x < self.currentScript.GetSize().width:
                self.UndoCloseTab()
        event.Skip()
    
    def OnLeftDClickVideoSplitter(self, event):
        #~ self.ToggleSliderWindow(vidrefresh=True)
        pos = self.currentScript.videoSidebarSizer.CalcMin()[0] + 6
        self.videoSplitter.SetSashPosition(-pos)
        self.currentScript.lastSplitSliderPos = self.videoSplitter.GetSashPosition()

    def OnMiddleDownScriptWindow(self, event):
        script = self.currentScript
        xypos = event.GetPosition()
        script.GotoPos(script.PositionFromPoint(xypos))
        self.middleDownScript = True

    def OnMiddleUpScriptWindow(self, event):
        if self.middleDownScript:
            self.InsertSource()
            self.middleDownScript = False

    def OnKeyDownVideoWindow(self, event):
        key = event.GetKeyCode()
        #~ if False:
            #~ pass
        #~ if key == wx.WXK_LEFT:
            #~ self.OnMenuVideoPrevFrame(None)
        #~ elif key == wx.WXK_RIGHT:
            #~ self.OnMenuVideoNextFrame(None)
        #~ elif key == wx.WXK_UP:
            #~ self.OnMenuVideoPrevSecond(None)
        #~ elif key == wx.WXK_DOWN:
            #~ self.OnMenuVideoNextSecond(None)
        #~ elif key in (wx.WXK_PRIOR, wx.WXK_PAGEUP):
            #~ self.OnMenuVideoPrevMinute(None)
        #~ elif key in (wx.WXK_NEXT, wx.WXK_PAGEDOWN):
            #~ self.OnMenuVideoNextMinute(None)
        #~ elif key == wx.WXK_HOME:
            #~ self.ShowVideoFrame(0)
        #~ elif key == wx.WXK_END:
            #~ self.ShowVideoFrame(-1)
        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            if self.cropDialog.IsShown():
                self.OnCropDialogApply(None)
            elif self.trimDialog.IsShown():
                self.OnTrimDialogApply(None)
            else:
                event.Skip()
        elif key == wx.WXK_ESCAPE:
            if self.cropDialog.IsShown():
                self.OnCropDialogCancel(None)
            elif self.trimDialog.IsShown():
                self.OnTrimDialogCancel(None)
            else:
                event.Skip()
        #~ elif key == wx.WXK_HOME:
            #~ if self.trimDialog.IsShown():
                #~ self.SetSelectionEndPoint(1)
        #~ elif key == wx.WXK_END:
            #~ if self.trimDialog.IsShown():
                #~ self.SetSelectionEndPoint(2)
        elif key >= wx.WXK_NUMPAD0 and key <= wx.WXK_NUMPAD9:
            i = (key - wx.WXK_NUMPAD1 + 10) % 10
            self.SelectTab(index=i)
        elif key >= ord('0') and key <= ord('9'):
            i = (key - ord('1') + 10) % 10
            self.SelectTab(index=i)
        else:
            event.Skip()

    def OnMouseWheelVideoWindow(self, event):
        # Zoom preview
        if event.ControlDown():
            # New zoom factor
            rotation = event.GetWheelRotation()
            factor = 1 + 0.25 * abs(rotation) / event.GetWheelDelta()
            old_zoomfactor = self.zoomfactor
            if rotation > 0:
                self.zoomfactor *= factor
            else:
                self.zoomfactor /= factor
            
            # Calculate scroll
            xrel, yrel = self.videoWindow.ScreenToClient(wx.GetMousePosition())
            xpos, ypos = self.videoWindow.CalcUnscrolledPosition(xrel, yrel)
            xpos = (xpos - self.xo) * self.zoomfactor / old_zoomfactor + self.xo
            ypos = (ypos - self.yo) * self.zoomfactor / old_zoomfactor + self.yo
            scroll = xpos - xrel, ypos - yrel
            
            self.OnMenuVideoZoom(zoomfactor=self.zoomfactor, scroll=scroll)
            return
        
        # Scroll similar tabs or tab groups
        group = self.currentScript.group
        tab_groups = self.options['enabletabscrolling_groups'] and group is not None
        similar_clips = self.options['enabletabscrolling']
        similar_clips_groups = self.options['enabletabscrolling'] and not tab_groups
        if similar_clips or tab_groups:
            rotation = event.GetWheelRotation()
            if self.mouse_wheel_rotation * rotation < 0:
                self.mouse_wheel_rotation = rotation
            else:
                self.mouse_wheel_rotation += rotation
            if not abs(self.mouse_wheel_rotation) >= event.GetWheelDelta():
                return
            self.mouse_wheel_rotation = 0
            if self.options['invertscrolling']: rotation = -rotation
            if rotation > 0:
                delta = -1
            else:
                delta = 1
            # Create list of indices to loop through
            index = self.scriptNotebook.GetSelection()
            r = range(self.scriptNotebook.GetPageCount())
            if delta == 1:
                for i in xrange(index+1):
                    j = r.pop(0)
                    r.append(j)
            else:
                r.reverse()
                for i in xrange(index):
                    j = r.pop()
                    r.insert(0,j)
            # Loop through r to find next suitable tab
            curframe = self.videoSlider.GetValue()
            oldInfo = (self.oldWidth, self.oldHeight, self.oldFramecount)
            for index in r:
                script = self.scriptNotebook.GetPage(index)
                if tab_groups and group == script.group:
                    self.SelectTab(index)
                    break
                if (not similar_clips or script.group != group or 
                    script.group is not None and not similar_clips_groups):
                        continue
                self.refreshAVI = True
                if self.UpdateScriptAVI(script, prompt=True) is None:
                    try:
                        if not script.AVI.initialized:
                            continue
                    except AttributeError:
                        return False
                newInfo = (
                    int(script.AVI.DisplayWidth * self.zoomfactor),
                    int(script.AVI.DisplayHeight * self.zoomfactor),
                    script.AVI.Framecount
                )
                if newInfo == oldInfo:
                    self.SelectTab(index)
                    break
        # Scroll video preview
        else:
            x0, y0 = self.videoWindow.GetViewStart()
            scrolls_by_pixel = self.zoomfactor / float(10) * event.GetWheelRotation() / event.GetWheelDelta()
            horizontal = event.ShiftDown()
            if wx.version() >= '2.9':
                horizontal = horizontal or event.GetWheelAxis() == wx.MOUSE_WHEEL_HORIZONTAL
            if horizontal:
                scrolls = int(round(self.currentScript.AVI.DisplayWidth * scrolls_by_pixel))
                self.videoWindow.Scroll(x0 + scrolls, -1)
            else:
                scrolls = int(round(self.currentScript.AVI.DisplayHeight * scrolls_by_pixel))
                self.videoWindow.Scroll(-1, y0 - scrolls)
    
    def OnMiddleDownVideoWindow(self, event):
        self.HidePreviewWindow()

    def OnLeftDownVideoWindow(self, event):
        if self.cropDialog.IsShown() and not self.getPixelInfo:
            # Set focus on video window if necessary
            # Set trim values if clicked within video frame
            script = self.currentScript
            w = script.AVI.Width
            h = script.AVI.Height
            left = self.cropValues['left']
            top = self.cropValues['top']
            mright = self.cropValues['-right']
            mbottom = self.cropValues['-bottom']
            xPos, yPos = self.videoWindow.CalcUnscrolledPosition(event.GetX(), event.GetY())
            xPos -= self.xo
            yPos -= self.yo
            xPos = int(round(xPos / float(self.zoomfactor)))
            yPos = int(round(yPos / float(self.zoomfactor)))
            if 'fliphorizontal' in self.flip:
                xPos = w - xPos
            if 'flipvertical' in self.flip:
                yPos = h - yPos
            xcenter = (w - left - mright) / float(2) + left
            ycenter = (h - top - mbottom) / float(2) + top
            xPos0 = xPos - xcenter
            yPos0 = - (yPos - ycenter)
            if xPos0 == 0:
                choice = 'top' if yPos0 > 0 else '-bottom'
            else:
                m = float(h - top - mbottom) / (w - left - mright)
                mo = yPos0 / xPos0
                if -m < mo < m:
                    choice = '-right' if xPos0 > 0 else 'left'
                else:
                    choice = 'top' if yPos0 > 0 else '-bottom'
            if choice == 'top':
                new_value = min(yPos, h - mbottom - self.options['cropminy'])
            elif choice == '-bottom':
                new_value = min(h - yPos, h - top - self.options['cropminy'])
            elif choice == 'left':
                new_value = min(xPos, w - mright - self.options['cropminx'])
            elif choice == '-right':
                new_value = min(w - xPos, w - left - self.options['cropminx'])
            self.cropDialog.ctrls[choice].SetValue(new_value)
            self.lastcrop = choice
            self.SetVideoStatusText()
            if wx.VERSION > (2, 9):
                self.OnCropDialogSpinTextChange()
        else:
            if self.refreshAVI:
                self.ShowVideoFrame()
            videoWindow = self.videoWindow
            videoWindow.CaptureMouse()
            videoWindow.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            videoWindow.oldPoint = event.GetPosition()
            videoWindow.oldOrigin = videoWindow.GetViewStart()
            if self.getPixelInfo:
                if self.getPixelInfo == 'string':
                    self.pixelInfo = self.GetPixelInfo(event, string_=True)
                else:
                    self.pixelInfo = self.GetPixelInfo(event)
                self.getPixelInfo = False
        event.Skip()
    
    def OnMouseMotionVideoWindow(self, event=None):
        if self.cropDialog.IsShown() and event and event.LeftIsDown():
            script = self.currentScript
            w = script.AVI.Width
            h = script.AVI.Height
            left = self.cropValues['left']
            top = self.cropValues['top']
            mright = self.cropValues['-right']
            mbottom = self.cropValues['-bottom']
            xPos, yPos = self.videoWindow.CalcUnscrolledPosition(event.GetX(), event.GetY())
            xPos -= self.xo
            yPos -= self.yo
            xPos = int(round(xPos / float(self.zoomfactor)))
            yPos = int(round(yPos / float(self.zoomfactor)))
            if 'fliphorizontal' in self.flip:
                xPos = w - xPos
            if 'flipvertical' in self.flip:
                yPos = h - yPos
            if self.lastcrop == 'top':
                top = yPos
                if top < 0:
                    top = 0
                if (h - mbottom) - top < self.options['cropminy']:
                    top = (h - mbottom) - self.options['cropminy']
                self.cropDialog.ctrls['top'].SetValue(top)
            elif self.lastcrop == '-bottom':
                mbottom = h - yPos
                if mbottom < 0:
                    mbottom = 0
                if (h - mbottom) - top < self.options['cropminy']:
                    mbottom = h - top - self.options['cropminy']
                self.cropDialog.ctrls['-bottom'].SetValue(mbottom)
            elif self.lastcrop == 'left':
                left = xPos
                if left < 0:
                    left = 0
                if (w - mright) - left < self.options['cropminx']:
                    left = (w - mright)  - self.options['cropminx']
                self.cropDialog.ctrls['left'].SetValue(left)
            elif self.lastcrop == '-right':
                mright = w - xPos
                if mright < 0:
                    mright = 0
                if (w - mright) - left < self.options['cropminx']:
                    mright = w - left  - self.options['cropminx']
                self.cropDialog.ctrls['-right'].SetValue(mright)
            self.SetVideoStatusText()
            if wx.VERSION > (2, 9):
                self.OnCropDialogSpinTextChange()
        else:
            videoWindow = self.videoWindow
            if event and event.Dragging() and event.LeftIsDown() and videoWindow.HasCapture():
                newPoint = event.GetPosition()
                if videoWindow.GetRect().Inside(newPoint):
                    newOriginX = videoWindow.oldOrigin[0] - (newPoint[0] - videoWindow.oldPoint[0])
                    newOriginY = videoWindow.oldOrigin[1] - (newPoint[1] - videoWindow.oldPoint[1])
                    if newOriginX < 0:
                        videoWindow.oldPoint[0] = newPoint[0] - videoWindow.oldOrigin[0]
                        newOriginX = 0
                    if newOriginY < 0:
                        videoWindow.oldPoint[1] = newPoint[1] - videoWindow.oldOrigin[1]
                        newOriginY = 0
                    xwin, ywin = videoWindow.GetClientSize()
                    xvwin, yvwin = videoWindow.GetVirtualSize()
                    xmax = xvwin - xwin
                    ymax = yvwin - ywin
                    if xmax > 0 and newOriginX > xmax:
                        videoWindow.oldPoint[0] = xmax + newPoint[0] - videoWindow.oldOrigin[0]
                        newOriginX = xmax
                    if ymax > 0 and newOriginY > ymax:
                        videoWindow.oldPoint[1] = ymax + newPoint[1] - videoWindow.oldOrigin[1]
                        newOriginY = ymax
                    videoWindow.Scroll(newOriginX, newOriginY)
                else:
                    videoWindow.ReleaseMouse()
                    videoWindow.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
            elif self.showVideoPixelInfo: #self.options['showvideopixelinfo']:
                if True:#self.FindFocus() == videoWindow:
                    pixelInfo = self.GetPixelInfo(event, string_=True)
                    if pixelInfo[1] is None:
                        self.SetVideoStatusText()
                    else:
                        self.SetVideoStatusText(addon=pixelInfo)#'%s%s, %s' % (' '*5,xystring, colorstring))
                    #~ if self.separatevideowindow:
                        #~ ctrl = self.frameTextCtrl2
                    #~ else:
                        #~ ctrl = self.frameTextCtrl2
                    #~ ctrl.SetBackgroundColour(rgb)
                    #~ ctrl.Refresh()
    
    def OnMouseLeaveVideoWindow(self, event):
        #~ if self.FindFocus() == self.videoWindow:
            #~ self.SetVideoStatusText()
        if self.FindFocus() == self.currentScript:
            self.SetScriptStatusText()
        event.Skip()

    def OnLeftUpVideoWindow(self, event):
        videoWindow = self.videoWindow
        if videoWindow.HasCapture():
            videoWindow.ReleaseMouse()
            videoWindow.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
        event.Skip()

    def OnCropDialogSpinTextChange(self, event=None):
        script = self.currentScript
        # Display actual spin control value (integer only)
        if not event: # SpinCtrl.SetValue() doesn't generate EVT_TEXT in wx2.9 
            if self.lastcrop:
                spinCtrl = self.cropDialog.ctrls[self.lastcrop]
            else:
                spinCtrl = None
        else:
            spinCtrl = event.GetEventObject()
            spinCtrl.SetValue(spinCtrl.GetValue())
        # Update the spin control ranges
        w = script.AVI.Width
        h = script.AVI.Height
        for key in self.cropValues.keys():
            self.cropValues[key] = self.cropDialog.ctrls[key].GetValue()
        self.cropDialog.ctrls['left'].SetRange(0, w-self.options['cropminx']-self.cropValues['-right'])
        self.cropDialog.ctrls['-right'].SetRange(0, w-self.options['cropminx']-self.cropValues['left'])
        self.cropDialog.ctrls['top'].SetRange(0, h-self.options['cropminy']-self.cropValues['-bottom'])
        self.cropDialog.ctrls['-bottom'].SetRange(0, h-self.options['cropminy']-self.cropValues['top'])
        # Paint the crop rectangles
        dc = wx.ClientDC(self.videoWindow)
        dc.SetDeviceOrigin(self.xo, self.yo)
        if self.IsDoubleBuffered():
            bdc = dc
        else:
            w = int(round(w * float(self.zoomfactor)))
            h = int(round(h * float(self.zoomfactor)))
            bdc = wx.BufferedDC(dc, wx.Size(w,h))
        shift = False if os.name == 'nt' else True # XXX
        self.PaintAVIFrame(bdc, script, self.currentframenum, shift=shift)
        self.PaintCropWarnings(spinCtrl)
        self.SetVideoStatusText()

    def OnCropAutocrop(self, event):
        button = event.GetEventObject()
        button.running = not button.running 
        if button.running:
            wx.CallAfter(self.Autocrop, button)
    
    def OnCropAutocropSamples(self, event):
        new_sample_size = event.GetEventObject().GetValue()
        if new_sample_size != self.options['autocrop_samples']:
            self.options['autocrop_samples'] = new_sample_size
            self.currentScript.autocrop_values = None
    
    def Autocrop(self, button):
        '''Run crop editor's auto-crop option'''
        script = self.currentScript
        if script.autocrop_values is None:
            # Get crop values for a number of frames
            samples = self.options['autocrop_samples']
            tol = 70
            clip = script.AVI
            frames = clip.Framecount
            samples = min(samples, frames)
            if samples <= 2:
                frames = range(samples)
            else:
                def float_range(start=0, end=10, step=1):
                    '''Range with float step'''
                    while start < end:
                        yield int(round(start))
                        start += step
                frames = float_range(frames/10, 9*frames/10 - 1, 8.0*frames/(10*samples))
            crop_values = []
            for i, frame in enumerate(frames):
                button.SetLabel(_('Cancel') + ' ({0}/{1})'.format(i+1, samples))
                crop_values_frame = clip.AutocropFrame(frame, tol)
                if not crop_values_frame:
                    button.SetLabel(_('Auto-crop'))
                    return
                crop_values.append(crop_values_frame)
                wx.Yield()
                if not button.running:
                    button.SetLabel(_('Auto-crop'))
                    return
            
            # Get and apply final crop values
            script.autocrop_values = []
            for seq in zip(*crop_values):
                script.autocrop_values.append(self.GetAutocropValue(seq))
        self.cropDialog.ctrls['left'].SetValue(script.autocrop_values[0])
        self.cropDialog.ctrls['top'].SetValue(script.autocrop_values[1])
        self.cropDialog.ctrls['-right'].SetValue(script.autocrop_values[2])
        self.cropDialog.ctrls['-bottom'].SetValue(script.autocrop_values[3])
        self.lastcrop = None
        self.SetVideoStatusText()
        self.OnCropDialogSpinTextChange()
        button.SetLabel(_('Auto-crop'))
        button.running = False
    
    @staticmethod
    def GetAutocropValue(seq):
        """Get the most repeated value on a sequence if it repeats more than 50%, 
        the minimum value otherwise"""
        d = collections.defaultdict(int)
        for i in seq:
            d[i] += 1
        max = sorted(d.keys(), key=lambda x:-d[x])[0]
        if d[max] > len(seq) / 2:
            return max
        else:
            ret_val = max
            for value in seq:
                if value < ret_val:
                    ret_val = value
            return ret_val
    
    def OnCropDialogApply(self, event):
        if self.cropDialog.boolInvalidCrop:
            dlg = wx.MessageDialog(self, _('Invalid crop values detected.  Continue?'),
                _('Warning'), wx.YES_NO|wx.CANCEL)
            ID = dlg.ShowModal()
            dlg.Destroy()
            if ID != wx.ID_YES:
                return
        script = self.currentScript
        # Update the script with the crop text
        croptxt = 'Crop(%(left)i, %(top)i, -%(-right)i, -%(-bottom)i)' % self.cropValues
        # Insert the crop based on the selected radio box option
        choice = self.cropDialog.ctrls['choiceInsert'].GetCurrentSelection()
        if choice == 0:
            # Case 1: Insert at end of script
            self.InsertTextAtScriptEnd(croptxt, script)
        elif choice == 1:
            # Case 2: Insert at script cursor
            script.ReplaceSelection(croptxt)
        if choice == 2:
            # Case 3: Copy Crop() to the clipboard
            text_data = wx.TextDataObject(croptxt)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(text_data)
                wx.TheClipboard.Close()
        # Hide the crop dialog
        self.cropDialog.Hide()
        for key in self.cropValues.keys():
            self.cropValues[key] = 0
        # Show the updated video frame
        self.refreshAVI = True
        self.ShowVideoFrame()

    def OnCropDialogCancel(self, event):
        script = self.currentScript
        for key in self.cropValues.keys():
            self.cropValues[key] = 0
        dc = wx.ClientDC(self.videoWindow)
        self.PaintAVIFrame(dc, script, self.currentframenum)
        self.cropDialog.Hide()
        
    def OnTrimDialogSpinTextChange(self, event):
        spinCtrl = event.GetEventObject() 
        spinCtrl.SetValue(spinCtrl.GetValue())

    def OnTrimDialogApply(self, event):
        insertMode = self.trimDialog.ctrls['choiceInsert'].GetCurrentSelection()
        useDissolve = self.trimDialog.ctrls['useDissolve'].GetValue()
        if useDissolve:
            useDissolve += self.trimDialog.ctrls['dissolveOverlap'].GetValue()
        if not self.InsertSelectionTrims(cutSelected=self.invertSelection,
                                         insertMode=insertMode,
                                         useDissolve=useDissolve):
            wx.MessageBox(_('You must create at least one frame selection first!'), _('Warning'))
            return
        for slider in self.GetVideoSliderList():
            slider.ToggleSelectionMode(0)
        self.trimDialog.Hide()
        if insertMode == 2:
            self.ShowVideoFrame()

    def OnTrimDialogCancel(self, event):
        # Convert selection bookmarks to regular bookmarks
        for value, bmtype in self.GetBookmarkFrameList().items():
            if bmtype != 0:
                if False:
                    self.AddFrameBookmark(value, bmtype=0, toggle=False)
                else:
                    self.DeleteFrameBookmark(value, bmtype)
        for slider in self.GetVideoSliderList():
            slider.ToggleSelectionMode(0)
        self.trimDialog.Hide()
        self.ShowVideoFrame()
        
    # the following 2 func called from wxp.OptionsDialog, not MainFrame
    def x_OnCustomizeAutoCompList(self, event):
        choices = []
        for keywords in self.avsazdict.values():
            choices += keywords
        choices.sort(key=lambda k: k.lower())
        dlg = wx.Dialog(self, wx.ID_ANY, _('Select autocomplete keywords'), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        listbox = wx.CheckListBox(dlg, wx.ID_ANY, choices=choices)
        for i in range(len(choices)):
            if choices[i] not in self.options['autocompleteexclusions']:
                listbox.Check(i)
        idAll = wx.NewId()
        idNone = wx.NewId()
        idExclude = wx.NewId()
        def OnContextMenuItem(event):
            id = event.GetId()
            value = True if id == idAll else False
            if id in [idAll, idNone]:
                for i in range(len(choices)):
                    listbox.Check(i, value)
            else:
                for i in range(len(choices)):
                    if '_' not in choices[i]:
                        continue
                    filtername = choices[i].lower()
                    if filtername in self.optionsFilters\
                    and self.optionsFilters[filtername][2] == 2:
                        listbox.Check(i, False)
                    if filtername in self.options['filteroverrides']\
                    and self.options['filteroverrides'][filtername][2] == 2:
                        listbox.Check(i, False)
        def OnContextMenu(event):
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idAll)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idNone)
            listbox.Bind(wx.EVT_MENU, OnContextMenuItem, id=idExclude)
            menu = wx.Menu()
            menu.Append(idAll, _('select all'))
            menu.Append(idNone, _('select none'))
            menu.Append(idExclude, _('exclude long names'))
            listbox.PopupMenu(menu)
            menu.Destroy()
        listbox.Bind(wx.EVT_CONTEXT_MENU, OnContextMenu)
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(listbox, 1, wx.EXPAND|wx.ALL,5)
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL,5)
        dlg.SetSizerAndFit(sizer)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            for i, keyword in enumerate(choices):
                if listbox.IsChecked(i):
                    try:
                        self.options['autocompleteexclusions'].discard(keyword)
                    except KeyError:
                        pass
                else:        
                    self.options['autocompleteexclusions'].add(keyword)
        dlg.Destroy()

    def OnConfigureVideoStatusBarMessage(self, event):
        dlg = wx.Dialog(self, wx.ID_ANY, _('Customize the video status bar message'))
        label = wx.StaticText(dlg, wx.ID_ANY, _('Video status bar message:'))
        textCtrl = wx.TextCtrl(dlg, wx.ID_ANY, self.videoStatusBarInfo.replace('\t','\\t'), size=(500,-1))
        textCtrl.SetSelection(0,0)
        box = wx.StaticBox(dlg, wx.ID_ANY, _('Legend'))
        staticBoxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        keyList = [
            (
            ('%F', _('Current frame')),
            ('%FC', _('Framecount')),
            ('%T', _('Current time')),
            #('%ST', _('Original source time (ffms only)')),
            ('%TT', _('Total time')),
            ('%W', _('Width')),
            ('%H', _('Height')),
            ('%AR', _('Aspect ratio')),
            ('%FR', _('Framerate')),
            ('%FRN', _('Framerate numerator')),
            ('%FRD', _('Framerate denominator')),
            ('%CS', _('Colorspace')),
            ('%FB', _('Field or frame based')),
            ('%P', _('Parity')),
            ('%PS', _('Parity short (BFF or TFF)')),
            #('%EFT', _('Encoded frame type (ffms only)')),
            ),
            (
            ('%AUR', _('Audio rate')),
            ('%AUL', _('Audio length')),
            ('%AUC', _('Audio channels')),
            ('%AUB', _('Audio bits')),
            ('%AUT', _('Audio type (Integer or Float)')),
            ('%POS', _('Pixel position (cursor based)')),
            ('%HEX', _('Pixel hex color (cursor based)')),
            ('%RGB', _('Pixel rgb color (cursor based)')),
            ('%YUV', _('Pixel yuv color (cursor based)')),
            ('%CLR', _('Pixel color (auto-detect colorspace)')),
            ('%Z', _('Program zoom')),
            ('%BM', _('Bookmark title')),
            ),
        ]
        for eachList in keyList:
            gridSizer = wx.FlexGridSizer(cols=2, hgap=0, vgap=3)
            for key, value in eachList:
                gridSizer.Add(wx.StaticText(dlg, wx.ID_ANY, key), 0, 0)
                gridSizer.Add(wx.StaticText(dlg, wx.ID_ANY, '  -  '+value), 0, 0)
            staticBoxSizer.Add(gridSizer, 0, wx.LEFT|wx.RIGHT, 20)
        noteText = wx.StaticText(dlg, wx.ID_ANY, _('Note: The "\\t\\t" or "\\T\\T" is used to separate the left and right portions of the status bar\n         message.'))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.BOTTOM, 5)
        sizer.Add(textCtrl, 0, wx.EXPAND|wx.BOTTOM, 5)
        sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(noteText, 0, wx.ALL, 5)
        # Standard buttons
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        okay.SetDefault()
        okay.SetFocus()
        cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(sizer, 0, wx.ALL, 5)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        dlg.SetSizer(dlgSizer)
        dlg.Fit()
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            text = textCtrl.GetValue().replace('\\t', '\t')
            self.options['videostatusbarinfo'] = text
            self.videoStatusBarInfo = text
            self.videoStatusBarInfoParsed, self.showVideoPixelInfo = self.ParseVideoStatusBarInfo(self.videoStatusBarInfo)
        dlg.Destroy()

        #~ if self.options['videostatusbarinfo'] == None:
            #~ self.videoStatusBarInfo = ' ' + _('Frame') + ' %F / %FC  -  (%T)      %POS  %RGB \t\t %Z %Wx%H (%AR)  -  %FR ' + _('fps')
        #~ else:
            #~ self.videoStatusBarInfo = self.options['videostatusbarinfo']
        #~ self.videoStatusBarInfoParsed, self.showVideoPixelInfo = self.ParseVideoStatusBarInfo(self.videoStatusBarInfo)

    def OnScrollUserSlider(self, event):
        pass

    def OnLeftUpUserSlider(self, event):
        slider = event.GetEventObject()
        self.UserSliderVideoUpdate(slider)
        event.Skip()

    def UserSliderVideoUpdate(self, slider):
        script = self.currentScript
        keep_env = not self.ScriptChanged(script)
        label = slider.GetName()
        sOpen = self.sliderOpenString
        sClose = self.sliderCloseString
        sliderText = None
        for text in self.regexp.findall(script.GetText()):
            if label == text.lstrip(sOpen).rstrip(sClose).split(',')[0].strip('"').strip("'"):
                sliderText = text
                break
        if sliderText:
            pos = script.FindText(0, script.GetTextLength(), sliderText)
            script.SetTargetStart(pos)
            posEnd = script.FindText(pos, script.GetTextLength(), '>]') + 2
            script.SetTargetEnd(posEnd)
            newVal = slider.GetValue()
            items = [s.strip() for s in sliderText.strip('[]').split(',')]
            if len(items) == 4:
                newSliderText = '%s"%s", %s, %s, %s%s' % (sOpen, label, items[1], items[2], newVal, sClose)
            script.ReplaceTarget(newSliderText)
            self.refreshAVI = True
        self.ShowVideoFrame(userScrolling=True, keep_env=keep_env)

    def OnToggleTagChecked(self, event):
        script = self.currentScript
        keep_env = not self.ScriptChanged(script)
        label = event.GetEventObject().GetName()
        if event.IsChecked():
            value = 1
        else:
            value = 0
        # Update the script
        newText = re.sub('\[%s(\s*=.*?)*?\]' % label, '[%s=%i]' % (label, value), script.GetText())
        script.SetText(newText)
        # Update the video
        self.refreshAVI = True
        self.ShowVideoFrame(userScrolling=False, keep_env=keep_env)

    def OnSliderLabelToggleAllFolds(self, event):
        script = self.currentScript
        numFolded = 0
        for item in script.sliderToggleLabels:
            if item.GetLabel().startswith('+'):
                numFolded += 1
        if numFolded == 0:
            self.foldAllSliders = True
        if numFolded == len(script.sliderToggleLabels):
            self.foldAllSliders = False
        for item in script.sliderToggleLabels:
            self.ToggleSliderFold(item, fold=self.foldAllSliders, refresh=False)
        script.sliderSizerNew.Layout()
        script.sliderWindow.FitInside()
        script.sliderWindow.Refresh()
        self.foldAllSliders = not self.foldAllSliders

    def OnSliderLabelEditDatabase(self, event):
        script = self.currentScript
        ctrl = self.lastContextMenuWin
        name = ctrl.GetLabel().lstrip(' -+').split()[0]
        lowername = name.lower()
        is_short = script.avsfilterdict[lowername][3]
        if is_short:
            lowername = is_short
            name = script.avsfilterdict[lowername][2]
        #~ calltip = self.currentScript.FilterNameArgs[name.lower()]
        calltip = script.avsfilterdict[lowername][0]
        dlg = AvsFilterAutoSliderInfo(self, self, name, calltip)
        ID = dlg.ShowModal()
        # Set the data
        if ID == wx.ID_OK:
            newCalltip = dlg.GetNewFilterInfo()
            if newCalltip == calltip:
                    return
            #~ for key, value in self.optionsFilters.items():
                #~ if key.lower() == name.lower():
                    #~ self.optionsFilters[key] = newCalltip
                    #~ for index in xrange(self.scriptNotebook.GetPageCount()):
                        #~ script = self.scriptNotebook.GetPage(index)
                        #~ script.DefineKeywordCalltipInfo(self.optionsFilters, self.optionsFilterPresets, self.optionsFilterDocpaths, self.optionsFilterTypes, self.optionsKeywordLists)
                    #~ self.ShowVideoFrame(forceRefresh=True)
                    #~ break
            if lowername in self.options['filteroverrides']:
                ftype = self.options['filteroverrides'][lowername][2]
            elif lowername in self.optionsFilters:
                ftype = self.optionsFilters[lowername][2]
            else: # add a new user function definition for functions defined in the current script
                ftype = 3
            self.options['filteroverrides'][lowername] = (name, newCalltip, ftype)
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
            self.defineScriptFilterInfo()
            for i in xrange(self.scriptNotebook.GetPageCount()):
                self.scriptNotebook.GetPage(i).Colourise(0, 0)
        dlg.Destroy()

    def OnSliderLabelSettings(self, event):
        self.ShowOptions(startPageIndex=4)

    def OnSliderLabelModifySliderProperties(self, event):
        ctrl = self.lastContextMenuWin

    def OnContextMenu(self, event):
        win = event.GetEventObject()
        if isinstance(win, wx.ListCtrl): # autocomplete list
            return
        self.lastContextMenuWin = win
        pos = win.ScreenToClient(event.GetPosition())
        # update 'video -> add tab to group' submenu
        group_menu_id = win.contextMenu.FindItem(_('Add tab to group'))
        if group_menu_id != wx.NOT_FOUND:
            group_menu = win.contextMenu.FindItemById(group_menu_id).GetSubMenu()
            group = self.currentScript.group
            if group is None:
                group = _('None')
            id = group_menu.FindItem(group)
            group_menu.Check(id, True)
            id = group_menu.FindItem(_('Apply offsets'))
            group_menu.Check(id, self.options['applygroupoffsets'])
            id = group_menu.FindItem(_('Offset also bookmarks'))
            group_menu.Check(id, self.options['offsetbookmarks'])
        try:
            win.PopupMenu(win.contextMenu, pos)
        except AttributeError:
        #except (AttributeError, wx._core.PyAssertionError):
            pass
            #~ print>>sys.stderr, _('Error: no contextMenu variable defined for window')

    def OnScriptTextChange(self, event):
        if event.GetEventObject() == self.FindFocus():
            self.SetScriptStatusText()
        event.Skip()

    def _x_OnScriptSavePointLeft(self, event):
        script = event.GetEventObject()
        if script == self.scriptNotebook.GetCurrentPage():
            index = self.scriptNotebook.GetSelection()
        else:
            for index in xrange(self.scriptNotebook.GetPageCount()):
                if script == self.scriptNotebook.GetPage(index):
                    break
        title = '* %s' % self.scriptNotebook.GetPageText(index).lstrip('* ')
        self.scriptNotebook.SetPageText(index, title)
        self.UpdateProgramTitle()

    def _x_OnScriptSavePointReached(self, event):
        script = event.GetEventObject()
        if script == self.scriptNotebook.GetCurrentPage():
            index = self.scriptNotebook.GetSelection()
        else:
            for index in xrange(self.scriptNotebook.GetPageCount()):
                if script == self.scriptNotebook.GetPage(index):
                    break
        title = self.scriptNotebook.GetPageText(index).lstrip('* ')
        self.scriptNotebook.SetPageText(index, title)
        self.UpdateProgramTitle()

    def OnScriptKeyUp(self, event):
        self.AutoUpdateVideo()
        event.Skip()

    def OnFocusScriptWindow(self, event):
        self.SetStatusWidths([-1, 0])
        self.SetScriptStatusText()
        #~ event.GetEventObject().SetCaretWidth(1)
        self.refreshAVI = True
        event.Skip()
        self.UpdateTabImages()

    def OnFocusVideoWindow(self, event):
        self.SetVideoStatusText()
        self.UpdateTabImages()
        #~ event.Skip()

    def OnPaintVideoWindow(self, event):
        dc = wx.PaintDC(self.videoWindow)
        if self.previewWindowVisible:
            script = self.currentScript
            self.PaintAVIFrame(dc, script, self.currentframenum, isPaintEvent=True)
    
    def OnEraseBackground(self, event=None):
        if event is not None:
            dc = event.GetDC()
        else:
            dc = wx.ClientDC(self.videoWindow)
        if dc is not None:
            script = self.currentScript
            if script.AVI is not None:
                if self.options['use_customvideobackground']:
                    background_color = self.options['videobackground']
                else: # using a custom handler for EVT_ERASE_BACKGROUND causes 
                      # the background to lose the theme's color on Windows
                    background_color = self.videoWindow.GetBackgroundColour()
                dc.SetBackground(wx.Brush(background_color))
                w_dc, h_dc = dc.GetSize()
                w_scrolled, h_scrolled = self.videoWindow.GetVirtualSize()
                x0, y0 = self.videoWindow.GetViewStart()
                if y0 < self.yo:
                    dc.SetClippingRegion(0, 0, w_dc, self.yo - y0)
                    dc.Clear()
                    dc.DestroyClippingRegion()
                if x0 < self.xo:
                    dc.SetClippingRegion(0, 0, self.xo - x0, h_dc)
                    dc.Clear()
                    dc.DestroyClippingRegion()
                if h_dc == h_scrolled:
                    bottom = h_dc - int(script.AVI.DisplayHeight * self.zoomfactor) - self.yo
                else:
                    bottom = h_dc - (h_scrolled - y0) + 2
                if bottom > 0:
                    dc.SetClippingRegion(0, h_dc - bottom, w_dc, bottom)
                    dc.Clear()
                    dc.DestroyClippingRegion()
                if w_dc == w_scrolled:
                    right = w_dc - int(script.AVI.DisplayWidth * self.zoomfactor) - self.xo
                else:
                    right = w_dc - (w_scrolled - x0) + 2
                if right > 0:
                    dc.SetClippingRegion(w_dc - right, 0, right, h_dc)
                    dc.Clear()
                    dc.DestroyClippingRegion()
                return
        if event is not None:
            event.Skip()
    
    def OnZoomInOut(self, event):
        id = event.GetId()
        vidmenus = [self.videoWindow.contextMenu, self.GetMenuBar().GetMenu(2)]
        for vidmenu in vidmenus:
            menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Zoom'))).GetSubMenu()
            menuItem = menu.FindItemById(id)
            if menuItem:
                label = menuItem.GetLabel()
                break
        for i in range(6):
            menuItem = menu.FindItemByPosition(i)
            if menuItem.IsChecked():
                if label == _('Zoom in') and i < 5:
                    self.OnMenuVideoZoom(None, menu.FindItemByPosition(i+1))
                elif label == _('Zoom out') and i > 0:
                    self.OnMenuVideoZoom(None, menu.FindItemByPosition(i-1))
                break
                
    def OnCharHook(self, event):
        if event.GetKeyCode() != wx.WXK_ESCAPE or not self.useEscape:
            event.Skip()
            return
        shortcut = 'Escape'
        if event.ShiftDown():
            shortcut = 'Shift+' + shortcut
        if event.AltDown():
            shortcut = 'Alt+' + shortcut
        if event.ControlDown():
            shortcut = 'Ctrl+' + shortcut
        IsReserved = shortcut in self.options['reservedshortcuts']
        if IsReserved and self.FindFocus() == self.currentScript\
        and (self.currentScript.AutoCompActive() or self.currentScript.CallTipActive()):
            self.currentScript.CmdKeyExecute(wx.stc.STC_CMD_CANCEL)
        elif IsReserved and self.cropDialog.IsShown():
            self.OnCropDialogCancel(None)
        elif IsReserved and self.trimDialog.IsShown():
            self.OnTrimDialogCancel(None)
        else:
            self.MacroExecuteMenuCommand(shortcut)
                
# Utility functions
    def ExitProgram(self):
        # Don't exit if saving an avi
        try:
            if self.dlgAvs2avi.IsShown():
                return
        except AttributeError:
            pass
        # Check if macros are still running
        for thread in threading.enumerate():
            if thread.name == 'MacroThread':
                dlg = wx.MessageDialog(self, _('A macro is still running. Close anyway?'),
                                       _('Warning'), wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)
                ID = dlg.ShowModal()
                dlg.Destroy()
                if ID == wx.ID_CANCEL:
                    return
                break
        # Stop playback
        if self.playing_video:
            self.PlayPauseVideo()
        # Save scripts if necessary
        frame = self.GetFrameNumber()
        previewvisible = self.previewWindowVisible
        if self.separatevideowindow:
            if self.videoDialog.IsIconized():
                self.videoDialog.Iconize(False)
            self.options['maximized2'] = False
            if self.videoDialog.IsMaximized():
                self.options['maximized2'] = True
                self.videoDialog.Maximize(False)
        self.HidePreviewWindow()
        if self.IsIconized():
            self.Iconize(False)
        if self.cropDialog.IsShown():
            self.OnCropDialogCancel(None)
        if self.trimDialog.IsShown():
            self.OnTrimDialogCancel(None)
        if self.options['promptexitsave']:
            for index in xrange(self.scriptNotebook.GetPageCount()):
                script = self.scriptNotebook.GetPage(index)
                tabTitle = self.scriptNotebook.GetPageText(index)
                if script.GetModify():
                    self.scriptNotebook.SetSelection(index)
                    dlg = wx.MessageDialog(self, _('Save changes before closing?'),
                        tabTitle, wx.YES_NO|wx.CANCEL)
                    ID = dlg.ShowModal()
                    dlg.Destroy()
                    if (ID == wx.ID_YES and not self.SaveScript(script.filename, index) or
                        ID == wx.ID_CANCEL):
                        return
        # Save the session
        if self.backupTimer.IsRunning():
            self.backupTimer.Stop()
        if self.options['startupsession']:
            self.SaveSession(self.lastSessionFilename, saverecentdir=False,
                frame=frame,
                previewvisible=previewvisible,
            )
        self.options['last_preview_placement'] = self.mainSplitter.GetSplitMode()
        # Save the text in the scrap window
        scrapCtrl = self.scrapWindow.textCtrl
        self.options['scraptext'] = (scrapCtrl.GetText(), scrapCtrl.GetAnchor(), scrapCtrl.GetCurrentPos())
        # Save the zoom factor
        vidmenu = self.videoWindow.contextMenu
        menu = vidmenu.FindItemById(vidmenu.FindItem(_('&Zoom'))).GetSubMenu()
        for i, menuItem in enumerate(menu.GetMenuItems()):
            if menuItem.IsChecked():
                self.options['zoomindex'] = i
                break
        # Save the program position
        self.options['maximized'] = False
        if self.IsMaximized():
            self.options['maximized'] = True
            self.Maximize(False)
        x, y, w, h = self.GetRect()
        #~ display = wx.Display(wx.Display.GetFromWindow(self))
        #~ xoffset, yoffset = display.GetGeometry().GetPosition()
        #~ self.options['dimensions'] = (x + xoffset, y + yoffset, w, h)
        self.options['dimensions'] = (max(x,20), max(y,20), w, h)
        if self.separatevideowindow:
            x, y, w, h = self.videoDialog.GetRect()
            #~ display = wx.Display(wx.Display.GetFromWindow(self.videoDialog))
            #~ xoffset, yoffset = display.GetGeometry().GetPosition()
            #~ self.options['dimensions2'] = (x + xoffset, y + yoffset, w, h)
            self.options['dimensions2'] = (x, y, w, h)
        # Save the crop choice
        self.options['cropchoice'] = self.cropDialog.ctrls['choiceInsert'].GetCurrentSelection()
        # Save the trim options
        self.options['triminsertchoice'] = self.trimDialog.ctrls['choiceInsert'].GetCurrentSelection()
        self.options['trimmarkframes'] = self.markFrameInOut
        if self.invertSelection:
            self.options['trimreversechoice'] = 1
        else:
            self.options['trimreversechoice'] = 0
        # Save the persistent options
        self.options['exitstatus'] = 0
        f = open(self.optionsfilename, mode='wb')
        cPickle.dump(self.options, f, protocol=0)
        f.close()
        if os.path.isdir(os.path.dirname(self.macrosfilename)):
            f = open(self.macrosfilename, mode='wb')
            cPickle.dump(self.optionsMacros, f, protocol=0)
            f.close()
        # Clean up
        wx.TheClipboard.Flush()
        for index in xrange(self.scriptNotebook.GetPageCount()):
            script = self.scriptNotebook.GetPage(index)
            script.AVI = None
        pyavs.ExitRoutines()
        if self.boolSingleInstance:
            self.argsPosterThread.Stop()
        self.Destroy()
    
    @AsyncCallWrapper
    def NewTab(self, copyselected=True, copytab=False, text='', select=True):
        r'''NewTab(copyselected=True)
        
        Creates a new tab (automatically named "New File (x)", where x is an appropriate 
        integer).  If any text was selected in the most recent tab and 'copyselected' is 
        True, it is automatically copied over to the new tab's text.
        
        '''
        if self.cropDialog.IsShown():
            wx.MessageBox(_('Cannot create a new tab while crop editor is open!'), 
                          _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        if self.trimDialog.IsShown():
            wx.MessageBox(_('Cannot create a new tab while trim editor is open!'), 
                          _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        self.Freeze()
        # Determine the name of the tab (New File (x))
        index = self.scriptNotebook.GetPageCount()
        if self.options['multilinetab']:
            rows = self.scriptNotebook.GetRowCount()
        iMax = 0
        re_newfile = re.compile(ur'\*?\s*{0}\s*\((\d+)\)\s*(?:\.avsi?)?$'.format(self.NewFileName), re.I)
        for i in range(index):
            title = self.scriptNotebook.GetPageText(i)
            match = re_newfile.match(title)
            if match:
                iNewFile = int(match.group(1))
                if iNewFile > iMax:
                    iMax = iNewFile
        # Create a new script window instance
        scriptWindow = self.createScriptWindow()
        # Get text and set some script variables
        if text:
            copytab = False
        else:
            if copytab:
                text = self.currentScript.GetText()
            elif copyselected:
                text = self.currentScript.GetSelectedText()
                copytab = bool(text.strip())
        # Add the tab to the notebook, pasting the text (unless it only contains whitespace)
        if text.strip():
            if copytab:
                scriptWindow.workdir = self.currentScript.workdir
                scriptWindow.encoding = self.currentScript.encoding
                scriptWindow.eol = self.currentScript.eol
                scriptWindow.group = self.currentScript.group # must be before scriptWindow.SetText (or just call UpdateScriptTabname here)
                scriptWindow.group_frame = self.currentScript.group_frame
                scriptWindow.lastFramenum = self.currentScript.lastFramenum
                scriptWindow.lastLength = self.currentScript.lastLength
            self.scriptNotebook.AddPage(scriptWindow,'%s (%s)' % (self.NewFileName, iMax+1), select=False)
            scriptWindow.ParseFunctions(text)
            scriptWindow.SetText(text)
            scriptWindow.SelectAll()
            if select:
                self.refreshAVI = True
                self.scriptNotebook.SetSelection(self.scriptNotebook.GetPageCount()-1)
        else:
            if select:
                self.HidePreviewWindow()
            self.scriptNotebook.AddPage(scriptWindow,'%s (%s)' % (self.NewFileName, iMax+1), select=select)
        if select:
            self.currentScript = scriptWindow
        scriptWindow.SetFocus()
        self.UpdateTabImages()
        scriptWindow.EnsureCaretVisible()
        # a workaroud for multiline notebook issue
        if self.options['multilinetab']:
            if rows != self.scriptNotebook.GetRowCount():
                w, h = self.scriptNotebook.GetSize()
                self.scriptNotebook.SetSize((w, h-1))
                self.scriptNotebook.SetSize((w, h))
        self.Thaw()
    
    @AsyncCallWrapper
    def OpenFile(self, filename='', default='', f_encoding=None, eol=-1, workdir=None, 
                 scripttext=None, setSavePoint=True, splits=None, framenum=None, 
                 last_length=None, group=-1, group_frame=None):
        r'''OpenFile(filename='', default='')
        
        If the string 'filename' is a path to an Avisynth script, this function opens 
        the script into a new tab.  If 'filename' is a path to a non-script file, the 
        filename is inserted as a source (see the GetSourceString function for details).  
        
        If 'filename' is not supplied, the user is prompted with an Open File dialog 
        box with 'default' as the default filename; it can be just a directory or 
        basename.
        
        '''
        # Get filename via dialog box if not specified
        if not filename:
            default_dir, default_base = (default, '') if os.path.isdir(default) else os.path.split(default)
            initial_dir = default_dir if os.path.isdir(default_dir) else self.GetProposedPath(only='dir')
            #~ filefilter = _('AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|All files (*.*)|*.*')
            extlist = self.options['templates'].keys()
            extlist.sort()
            extlist2 = [s for s in extlist if not s.startswith('avs')]
            extlist1 = ', '.join(extlist2)
            extlist2 = ';*.'.join(extlist2)
            filefilter = (_('AviSynth script') + ' (avs, avsi)|*.avs;*.avsi|' + 
                          _('Source files') + ' (%(extlist1)s)|*.%(extlist2)s|' + 
                          _('All files') + ' (*.*)|*.*') %  locals()
            dlg = wx.FileDialog(self,_('Open a script or source'), initial_dir, default_base, 
                                filefilter, wx.OPEN|wx.FILE_MUST_EXIST|wx.MULTIPLE)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filenames = dlg.GetPaths()
                if len(filenames) == 1:
                    filename = filenames[0]
                else:
                    for filename in filenames:
                        if filename:
                            self.OpenFile(filename)
                    return
            dlg.Destroy()
        # Open script if filename exists (user could cancel dialog box...)
        if filename:
            # Process the filename
            dirname, basename = os.path.split(filename)
            root, ext = os.path.splitext(basename)
            if ext.lower() == '.ses': # Treat the file as a session file
                if not self.LoadSession(filename):
                    wx.MessageBox(_('Damaged session file'), _('Error'), wx.OK|wx.ICON_ERROR)
                return
            if os.path.isdir(dirname):
                self.options['recentdir'] = dirname
            if ext.lower() not in ('.avs', '.avsi', '.vpy'): # Treat the file as a source
                # Make a new tab if current one is not empty
                indexCur = self.scriptNotebook.GetSelection()
                txt = self.scriptNotebook.GetPage(indexCur).GetText()
                title = self.scriptNotebook.GetPageText(indexCur)
                if txt or not title.startswith(self.NewFileName):
                    self.NewTab(copyselected=False)
                self.InsertSource(filename)
                if self.previewWindowVisible:
                    self.ShowVideoFrame()
            else: # Treat the file as an avisynth script
                if scripttext is None:
                    scripttext, f_encoding, eol = self.GetMarkedScriptFromFile(filename)
                # If script already exists in a tab, select it
                for index in xrange(self.scriptNotebook.GetPageCount()):
                    script = self.scriptNotebook.GetPage(index)
                    if filename == script.filename:
                        self.SelectTab(index)
                        if scripttext != script.GetText():
                            dlg = wx.MessageDialog(self, _('Reload the file and lose the current changes?'),
                                                   os.path.basename(filename), wx.YES_NO)
                            ID = dlg.ShowModal()
                            dlg.Destroy()
                            if ID != wx.ID_YES:
                                return
                            script.ParseFunctions(scripttext)
                            pos = script.GetCurrentPos()
                            script.SetText(scripttext)
                            script.GotoPos(pos)
                        break
                else:
                    # Make a new tab if current one is not empty
                    indexCur = self.scriptNotebook.GetSelection()
                    txt = self.scriptNotebook.GetPage(indexCur).GetText()
                    title = self.scriptNotebook.GetPageText(indexCur)
                    if txt == "" and title.startswith(self.NewFileName):
                        index = indexCur
                    else:
                        self.NewTab(select=False)
                        index = self.scriptNotebook.GetPageCount() - 1
                    script = self.scriptNotebook.GetPage(index)
                    if dirname != '':
                        self.SetScriptTabname(basename, script)
                        script.filename = filename
                        script.workdir = dirname
                    elif not root.startswith(self.NewFileName):
                        self.SetScriptTabname(root, script)
                    script.ParseFunctions(scripttext)
                    script.SetText(scripttext)
                    self.UpdateRecentFilesList(filename)
                if f_encoding is not None:
                    script.encoding = f_encoding
                if eol != -1:
                    script.eol = eol
                if workdir is not None:
                    script.workdir = workdir
                if framenum is not None:
                    script.lastFramenum = framenum
                if last_length is not None:
                    script.lastLength = last_length
                if splits is not None:
                    script.lastSplitVideoPos = splits[0]
                    script.lastSplitSliderPos = splits[1]
                    script.sliderWindowShown = splits[2]
                if group != -1 and script.group != group:
                    script.group = group
                    self.UpdateScriptTabname(index=index)
                if group_frame is not None:
                    script.group_frame = group_frame
                if setSavePoint:
                    script.EmptyUndoBuffer()
                    script.SetSavePoint()
                self.scriptNotebook.SetSelection(index)
                self.refreshAVI = True
                if self.previewWindowVisible:
                    self.ShowVideoFrame()
                return index
    
    def GetMarkedScriptFromFile(self, filename, returnFull=False):
        txt, f_encoding, eol = self.GetTextFromFile(filename)
        lines = txt.rstrip().split('\n')
        lines.reverse()
        header = '### AvsP marked script ###'
        if lines[0] == header:
            newlines = []
            for line in lines[1:]:
                if line == header:
                    break
                if line.startswith('# '):
                    newlines.append(line[2:])
                else:
                    if returnFull:
                        return (txt, txt), f_encoding, eol
                    else:
                        return txt, f_encoding, eol
            newlines.reverse()
            if returnFull:
                return ('\n'.join(newlines), txt), f_encoding, eol
            else:
                return '\n'.join(newlines), f_encoding, eol
        else:
            if returnFull:
                return (txt, txt), f_encoding, eol
            else:
                return txt, f_encoding, eol
    
    def GetTextFromFile(self, filename):
        '''Return text and encoding from a file'''
        with open(filename, mode='rb') as f:
            raw_txt = f.read()
        boms = ((codecs.BOM_UTF8, 'utf-8-sig'),
                (codecs.BOM_UTF16_LE, 'utf-16-le'),
                (codecs.BOM_UTF16_BE, 'utf-16-be'),
                (codecs.BOM_UTF32_LE, 'utf-32-le'),
                (codecs.BOM_UTF32_BE, 'utf-32-be'))
        for bom, f_encoding in boms:
            if raw_txt.startswith(bom):
                raw_txt = raw_txt[len(bom):]
                break
        else:
            f_encoding = 'utf8'
        try:
            txt = raw_txt.decode(f_encoding)
        except UnicodeDecodeError:
            f_encoding = encoding
            txt = raw_txt.decode(f_encoding)
        if '\r' in txt:
            eol = 'crlf'
            txt = txt.replace('\r\n', '\n') # to simplify text handling on macros and avoid mixing line endings
        elif '\n' in txt:
            eol = 'lf'
        else:
            eol = None
        return txt, f_encoding, eol
    
    def UpdateRecentFilesList(self, filename=None):
        # Update the persistent internal list
        if filename is not None:
            if type(filename) != unicode:
                filename = unicode(filename, encoding)
            # Add the filename to the internal list
            if not os.path.isfile(filename):
                return
            if self.options['recentfiles'] is None:
                self.options['recentfiles'] = []

            #~ try:
                #~ if filename in self.options['recentfiles']:
                    #~ return
            #~ except UnicodeDecodeError:
                #~ if unicode(filename, encoding) in self.options['recentfiles']:
                    #~ return
            if filename in self.options['recentfiles']:
                return

            self.options['recentfiles'].insert(0, filename)
            n1 = len(self.options['recentfiles'])
            n2 = self.options['nrecentfiles']
            if n1 > n2:
                self.options['recentfiles'] = self.options['recentfiles'][:n2]
            nameList = [filename]
        else:
            if self.options['recentfiles'] is None:
                return
            nameList = self.options['recentfiles'][::-1]
        # Find the menu position
        menu = self.GetMenuBar().GetMenu(0)
        nMenuItems = menu.GetMenuItemCount()
        i = nMenuItems - 1 - 2
        while i >= 0:
            menuItem = menu.FindItemByPosition(i)
            if menuItem.IsSeparator():
                break
            i -= 1
        if i == 0:
            return
        # Insert the new menu items
        pos = i + 1
        for name in nameList:
            if len(name) > 43:
                label = name[:15] + '...' + name[-25:]
            else:
                label = name
            newMenuItem = menu.Insert(pos, wx.ID_ANY, label, _("Open this file"))
            self.Bind(wx.EVT_MENU, self.OnMenuFileRecentFile, newMenuItem)
        # Renumber and delete extra menu items
        nMenuItems = menu.GetMenuItemCount()
        nNameItems = (nMenuItems - 1 - 2) - pos + 1
        nMax = self.options['nrecentfiles']
        if nNameItems > nMax:
            item_pos = pos + nMax
            for i in range(nNameItems-nMax):
                badMenuItem = menu.FindItemByPosition(item_pos)
                menu.Delete(badMenuItem.GetId())
            nNameItems = nMax
        prefix = '&{0}  '
        prefix_len = len(prefix) - 3
        for i in range(nNameItems):
            menuItem = menu.FindItemByPosition(pos + i)
            menuLabel = menuItem.GetItemLabelText()
            if menuLabel != menuItem.GetItemLabel(): # GetAccel
                menuLabel = menuLabel[prefix_len:]
            accel = prefix.format((i + 1) % 10) if i < 10 else ''
            menuItem.SetItemLabel(accel + menuLabel)
    
    def UndoCloseTab(self):
        '''Reopen the last closed tab'''
        if self.lastClosed:
            self.LoadTab(self.lastClosed)
            self.ReloadModifiedScripts()
    
    @AsyncCallWrapper
    def CloseTab(self, index=None, prompt=False, discard=False, boolPrompt=False):
        r'''CloseTab(index=None, prompt=False, discard=False)
        
        Closes the tab at integer 'index', where an index of 0 indicates the first 
        tab. If 'index' is None (the default), the function will close the currently 
        selected tab.  
        
        If the argument 'discard' is True any unsaved changes are lost.  Otherwise, 
        if 'prompt' is True the program will prompt the user with a dialog box to 
        save the file if there are any unsaved changes.  If 'prompt' is False, the 
        function will not prompt the user and will close the script only saving 
        changes on scripts that already exist on the filesytem.
        
        '''
        # 'boolPrompt' was renamed to 'prompt' 
        # Get the script and corresponding index
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        # Prompt user to save changes if necessary
        if not discard and script.GetModify():
            if (prompt or boolPrompt) and not (
                    self.options['closeneversaved'] and not script.filename):
                #~ self.HidePreviewWindow()
                tabTitle = self.scriptNotebook.GetPageText(index)
                dlg = wx.MessageDialog(self, _('Save changes before closing?'),
                    tabTitle, wx.YES_NO|wx.CANCEL)
                ID = dlg.ShowModal()
                dlg.Destroy()
                if (ID == wx.ID_YES and not self.SaveScript(script.filename, index) or
                    ID == wx.ID_CANCEL):
                    return False
            elif script.filename:
                self.SaveScript(script.filename, index)
        # Save last state
        self.lastClosed = self.GetTabInfo(index)
        # Delete the tab from the notebook
        script.AVI = None #self.scriptNotebook.GetPage(index).AVI = None # clear memory
        # If only 1 tab, make another
        if self.scriptNotebook.GetPageCount() == 1:
            self.NewTab(copyselected=False)
            self.SetScriptTabname(self.NewFileName, index=1)
            self.HidePreviewWindow()
        if self.options['multilinetab']:
            rows = self.scriptNotebook.GetRowCount()
        self.scriptNotebook.DeletePage(index)
        self.currentScript = self.scriptNotebook.GetPage(self.scriptNotebook.GetSelection())
        self.UpdateTabImages()
        if self.options['multilinetab']:
            if rows != self.scriptNotebook.GetRowCount():
                w, h = self.scriptNotebook.GetSize()
                self.scriptNotebook.SetSize((w, h-1))
                self.scriptNotebook.SetSize((w, h))
        return True

    def CloseAllTabs(self):
        dlg = wx.MessageDialog(self, _('Save session before closing all tabs?'),
            _('Warning'), wx.YES_NO|wx.CANCEL)
        ID = dlg.ShowModal()
        dlg.Destroy()
        if ID == wx.ID_CANCEL:
            return
        if ID == wx.ID_YES:
            if not self.SaveSession():
                return
        for index in xrange(self.scriptNotebook.GetPageCount()):
            self.CloseTab(0)
    
    @AsyncCallWrapper
    def SaveScript(self, filename='', index=None, default=''):
        r'''SaveScriptAs(filename='', index=None, default='')
        
        Similar to the function SaveScript(), except that if the filename is an empty 
        string, this function will always prompt the user with a dialog box for the 
        location to save the file, regardless of whether or not the script exists on 
        the hard drive.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return None
        # Get filename via dialog box if not specified
        if not filename:           
            initialdir, initialname = (default, '') if os.path.isdir(default) else os.path.split(default)
            isdir = os.path.isdir(initialdir)
            if not isdir or not initialname:
                source_dir, source_base = os.path.split(self.GetProposedPath())
                if not isdir:
                    initialdir = source_dir
                if not initialname:
                    initialname = source_base
            filefilter = (_('AviSynth script') + ' (*.avs, *.avsi)|*.avs;*.avsi|' + 
                          _('All files') + ' (*.*)|*.*')
            dlg = wx.FileDialog(self,_('Save current script'),
                initialdir, initialname, filefilter, wx.SAVE | wx.OVERWRITE_PROMPT)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filename = dlg.GetPath()
            dlg.Destroy()
        # Save script if filename exists (either given or user clicked OK)
        if filename:
            # Process the filename
            dirname, basename = os.path.split(filename)
            root, ext = os.path.splitext(basename)
            if not os.path.isdir(dirname):
                wx.MessageBox(_('Directory %(dirname)s does not exist!') % locals(), _('Error'), style=wx.OK|wx.ICON_ERROR)
                return None
            if ext.lower() not in ('.avs', '.avsi', '.vpy'):
                basename = root+'.avs'
            if os.path.splitext(script.filename)[1].lower() == '.avsi':
                basename = root+'.avsi'
            filename = os.path.join(dirname, basename)
            
            # Get script's text, adding the marked version of the script if required
            #~ txt = self.regexp.sub(self.re_replace, script.GetText())
            scriptText = script.GetText()
            txt = self.getCleanText(scriptText)
            if txt != scriptText and self.options['savemarkedavs']:
                header = '### AvsP marked script ###'
                base = '\n'.join(['# %s' % line for line in scriptText.split('\n')])
                txt = '%(txt)s\n%(header)s\n%(base)s\n%(header)s' % locals()
            
            # Encode text and save it to the specified file
            txt = self.GetEncodedText(txt, bom=True)
            with open(filename, 'wb') as f:
                f.write(txt)
            
            # Misc stuff
            script.SetSavePoint()
            script.filename = filename
            script.workdir = os.path.dirname(filename)
            self.SetScriptTabname(basename, script)
            if os.path.isdir(dirname):
                self.options['recentdir'] = dirname
            self.refreshAVI = True
            #~ script.previewtxt = None
            self.UpdateRecentFilesList(filename)
        else:
            return None
        return filename
    
    def getScriptAtIndex(self, index):
        if index is None:
            script = self.currentScript
            index = self.scriptNotebook.GetSelection()
        else:
            try:
                index = int(index)
                if index < 0:
                    return None, None
                if index >= self.scriptNotebook.GetPageCount():
                    return None, None
                script = self.scriptNotebook.GetPage(index)
            except TypeError:
                return None, None
            except ValueError:
                return None, None
        return script, index

    def getCleanText(self, text):
        text = self.cleanSliders(text)
        text = self.cleanToggleTags(text)
        return text
    
    def GetEncodedText(self, txt, bom=False):
        '''Prepare a script's text for saving it to file
        
        Prefer system's encoding to utf-8, just in case other applications
        won't support it
        
        If bom == True, insert the BOM at the beginning (except for UTF-8 
        without BOM on the original file)
        '''
        script = self.currentScript
        
        # convert line endings to CRLF if necessary
        if self.options['eol'] == 'force crlf' or self.options['eol'] == 'auto' and (
                script.eol == 'crlf' or script.eol is None and os.name == 'nt'):
            txt = txt.replace('\n', '\r\n')
        
        # try current encoding, else filesystem's
        try:
            encoded_txt = txt.encode(script.encoding)
            encoded = True
        except UnicodeEncodeError:
            sys_encoding = sys.getfilesystemencoding()
            if sys_encoding != script.encoding:
                try:
                    script.encoding = sys_encoding
                    encoded_txt = txt.encode(script.encoding)
                    encoded = True
                except UnicodeEncodeError:
                    encoded = False
        # mbcs just replaces invalid characters
        if encoded and script.encoding.lower() == 'mbcs':
            txt2 = encoded_txt.decode(script.encoding)
            if txt != txt2:
                encoded = False
        # fallback to utf-8
        if not encoded:       
            script.encoding = 'utf8'
            encoded_txt = txt.encode(script.encoding)
        
        # Add BOM
        if bom:
            if script.encoding == 'utf-8-sig':
                encoded_txt = codecs.BOM_UTF8 + encoded_txt
            elif script.encoding == 'utf-16-le':
                encoded_txt = codecs.BOM_UTF16_LE + encoded_txt
            elif script.encoding == 'utf-16-be':
                encoded_txt = codecs.BOM_UTF16_BE + encoded_txt
            elif script.encoding == 'utf-32-le':
                encoded_txt = codecs.BOM_UTF32_LE + encoded_txt
            elif script.encoding == 'utf-32-be':
                encoded_txt = codecs.BOM_UTF32_BE + encoded_txt
        
        return encoded_txt
    
    def GetProposedPath(self, index=None, only=None, type_=None):
        r'''Return a proposed filepath for a script based on the script's filename 
        (if saved), its tab's title, the first source in the script and the user 
        preferences.  Posible 'type_' values: 'general', 'image'.
        
        If 'only' is set to 'dir' or 'base', return only the dirname or basename 
        respectively.
        '''
        # Get script
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return ''
        
        # Get script filename
        dirname, basename = os.path.split(script.filename)
        if not basename and not only == 'dir':
            page_text = self.scriptNotebook.GetPageText(index)
            if not page_text.startswith(self.NewFileName):
                basename = page_text
        
        # Get default directory for 'type_'
        if not only == 'base':
            if type_ == 'image':
                type_dirname = self.options['imagesavedir']
                use_type_dirname = self.options['useimagesavedir']
            else:
                type_dirname = self.options['recentdir']
                use_type_dirname = self.options['userecentdir']
            if use_type_dirname:
                dirname = type_dirname
        
        # Use the first source in the script if necessary
        if not dirname and not only == 'base' or not basename and not only == 'dir':
            dir_source, base_source = os.path.split(self.GetSourcePath(script))
            if not basename:
                basename = os.path.splitext(base_source)[0]
            if not dirname:
                dirname = dir_source
        
        # Last fallback and return
        if not dirname and not only == 'base':
            dirname = type_dirname
        if only == 'dir':
            return dirname
        if not basename and not only == 'dir':
            basename = page_text
        if os.path.splitext(basename)[1] not in ('.avs', '.avsi', '.vpy'):
            basename += '.avs'
        if only == 'base':
            return basename
        return os.path.join(dirname, basename)
    
    def GetSourcePath(self, script=None):
        '''Parse script for the path on the first source filter'''
        if script is None:
            script = self.currentScript
        if os.name == 'nt':
            sourceFilterList = set(('directshowsource',))
        else:
            sourceFilterList = set(('ffvideosource', 'ffaudiosource'))
        noMediaFileList = ('import', 'loadplugin', 'loadcplugin', 'load_stdcall_plugin', 
                           'loadvirtualdubplugin', 'loadvfapiplugin')
        re_templates = re.compile(r'\b(\w+)\s*\([^)]*?\[?\*{3}', re.I)
        for template in self.options['templates'].values():
            re_obj = re_templates.search(template)
            if re_obj:
                function_name = re_obj.group(1).lower() 
                if function_name not in noMediaFileList:
                    sourceFilterList.add(function_name)
        findpos = -1
        lastpos = script.GetLength()
        noMediaExtList = ('.dll', '.vdf', 'vdplugin', '.vfp', '.so', '.avs', '.avsi', '.txt', '.log')
        for match in re.finditer('"(.+?)"', script.GetText()):
            s = match.group(1)
            if os.path.splitext(s)[1].lower() not in noMediaExtList and os.path.isfile(s):
                findpos = script.FindText(findpos+1, lastpos, s)
                openpos = script.GetOpenParenthesesPos(findpos)
                if openpos is not None:
                    wordstartpos = script.WordStartPosition(openpos,1)
                    if openpos == wordstartpos:
                        wordstartpos = script.WordStartPosition(script.WordStartPosition(openpos,0),1)
                    if wordstartpos != -1:
                        sourceFilter = script.GetTextRange(wordstartpos, openpos)
                        if sourceFilter.strip().lower() in sourceFilterList:
                            return s
        return ''
    
    @AsyncCallWrapper
    def RenameScript(self, new_title, index=None):
        """RenameScript(new_title, index=None)
        
        Renames the tab located at the integer 'index' to 'new_title'.  If 'index' is 
        None, then the currently selected tab is used.
        
        If the script was saved to the filesystem the file is renamed as well.  Returns 
        False if the file couldn't be renamed, True otherwise.
        
        """
        if index is None:
            index = self.scriptNotebook.GetSelection()
        script = self.scriptNotebook.GetPage(index)
        if script.filename:
            if os.path.splitext(new_title)[1] not in ('.avs', '.avsi', '.vpy'):
                new_title += '.avs'
            src = script.filename
            dirname = os.path.dirname(src)
            dst = os.path.join(dirname, new_title)
            try:
                os.rename(src, dst)
                script.filename = dst
            except OSError:
                return False
        self.SetScriptTabname(new_title, index=index)
        return True
    
    def RepositionTab(self, newIndex):
        if type(newIndex) is not int:        
            id = newIndex.GetId()
            menu = self.scriptNotebook.contextMenu
            menuItem = menu.FindItemByPosition(menu.GetMenuItemCount()-1)
            menu = menuItem.GetSubMenu()
            for newIndex in range(menu.GetMenuItemCount()):
                if id == menu.FindItemByPosition(newIndex).GetId():
                    break        
        index = self.scriptNotebook.GetSelection()
        page = self.scriptNotebook.GetPage(index)
        label = self.scriptNotebook.GetPageText(index, full=True)
        win = self.FindFocus()
        self.scriptNotebook.RemovePage(index)
        self.scriptNotebook.InsertPage(newIndex, page, label, select=True)
        if win:
            win.SetFocus()
        self.UpdateTabImages()

    def cleanSliders(self, text):
        return self.regexp.sub(self.re_replace, text)

    def cleanToggleTags(self, text):
        for endtag in re.findall('\[/.*?\]', text):
            tagname = endtag[2:-1]
            expr = re.compile('\[%s(\s*=.*?)*?\].*?\[/%s\]' % (tagname, tagname), re.IGNORECASE|re.DOTALL)
            text = expr.sub(self.re_replace2, text)
        return text
    
    def ExportHTML(self, filename=None, ext_css=None, index=None):
        """Save a script as a HTML document
        
        If 'index' is None, the current tab is used
        If a filename is not specified, the user is asked for
        'ext_css' can be a filename for saving the style sheet
        """
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return
        if not script.GetLength():
            wx.MessageBox(_('Script has no text!'), _('Error'), 
                          style=wx.OK|wx.ICON_ERROR)
            return
        if not filename:
            filefilter = (_('HTML files') + ' (*.html, *.htm)|*.html;*.htm|' + 
                          _('All files') + ' (*.*)|*.*')
            initial_dir, initial_base = os.path.split(self.GetProposedPath(index))
            initial_base = os.path.splitext(initial_base)[0] + '.html'
            dlg = wx.FileDialog(self, _('Export HTML'), initial_dir, initial_base, 
                                filefilter, wx.SAVE | wx.OVERWRITE_PROMPT)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filename = dlg.GetPath()
            dlg.Destroy()
        if filename:
            script.OnStyleNeeded(None, forceAll=True)
            dirname = os.path.dirname(filename)
            if os.path.isdir(dirname):
                self.options['recentdir'] = dirname
            html = script.GenerateHTML(self.GetProposedPath(only='base'), ext_css)
            if ext_css is not None:
                html, css = html
                with open(os.path.join(dirname, ext_css), 'w') as f:
                    f.write(css.encode('utf-8'))
            with open(filename, 'w') as f:
                f.write(html.encode('utf-8'))
    
    def LoadSession(self, filename=None, saverecentdir=True, resize=True, backup=False, startup=False):
        # Get the filename to load from the user
        if filename is None or not os.path.isfile(filename):
            filefilter = 'Session (*.ses)|*.ses'
            initialdir = self.options['recentdirSession']
            if not os.path.isdir(initialdir):
                initialdir = self.programdir
            dlg = wx.FileDialog(self,_('Load a session'),
                initialdir, '', filefilter, wx.OPEN)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filename = dlg.GetPath()
            dlg.Destroy()
        if filename is not None:
            # Load the session info from filename
            try:
                with open(filename, mode='rb') as f:
                    session = cPickle.load(f)
            except:
                return
            if self.options['hidepreview'] or self.options['paranoiamode'] or (startup and self.options['exitstatus']):
                previewWindowVisible = False
            else:
                previewWindowVisible = session['previewWindowVisible']
            if backup:
                session['previewWindowVisible'] = False
                f = open(filename, mode='wb')
                cPickle.dump(session, f, protocol=0)
                f.close()
            # Load the text into the tabs
            selectedIndex = None
            self.SelectTab(self.scriptNotebook.GetPageCount() - 1)
            #~ for scriptname, boolSelected, scripttext in session['scripts']:
            mapping = session['scripts'] and isinstance(session['scripts'][0], collections.Mapping)
            for item in session['scripts']:
                index = self.LoadTab(item, compat=not mapping)
                if mapping:
                    boolSelected = item['selected']
                else:
                    boolSelected = (item + (None, None)[len(item):])[1]
                if boolSelected:
                    selectedIndex = self.scriptNotebook.GetSelection()
            # Prompt to reload modified files
            if not startup:
                self.ReloadModifiedScripts()
            # Select the last selected script
            if selectedIndex is not None:
                self.scriptNotebook.SetSelection(selectedIndex)
            # Change preview placement if needed
            if session.get('preview_placement', wx.SPLIT_HORIZONTAL) != self.mainSplitter.GetSplitMode():
                self.TogglePreviewPlacement()
            # Set the video slider to last shown frame number
            if startup:
                self.previewWindowVisible = previewWindowVisible
                self.startupframe = session['frame']
            else:
                if not previewWindowVisible:
                    self.HidePreviewWindow()
                else:
                    self.ShowVideoFrame(session['frame'], resize=resize)
            # Set the last closed tab
            if session.get('lastclosed'): # backward compatibility
                self.lastClosed = session['lastclosed']
            # Set the bookmarks
            if 'bookmarks' in session:
                if startup:
                    if self.options['loadstartupbookmarks']:
                        self.SetBookmarkFrameList(session['bookmarks'])
                else:
                    self.SetBookmarkFrameList(session['bookmarks'])
                if 'bookmarkDict' in session:
                    self.bookmarkDict.update(session['bookmarkDict'].items())
            # Save the recent dir
            if saverecentdir:
                dirname = os.path.dirname(filename)
                if os.path.isdir(dirname):
                    self.options['recentdirSession'] = dirname
        return True
    
    def LoadTab(self, item, compat=False):
        '''Open/reload a tab from info returned from GetTabInfo
        
        compat? tuple : dict
        '''
        if compat:
            nItems = len(item)
            defaults = (None, None, None, None, None, 0, 'latin1', '')
            name, selected, text, hash, splits, current_frame, f_encoding, workdir = item + defaults[nItems:]
            item = locals()
        scriptname = item['name']
        dirname, basename = os.path.split(scriptname)
        reload = False
        setSavePoint = False
        if not os.path.isdir(dirname):
            if basename:
                scriptname = '%s.avs' % basename
            else:
                scriptname = '%s.avs' % self.NewFileName
        else:
            if os.path.isfile(scriptname):
                txt, txtFromFile = self.GetMarkedScriptFromFile(scriptname, returnFull=True)[0]
                #~ if txt == self.getCleanText(scripttext):
                try:
                    if txt == item['text']:
                        setSavePoint = True
                    else:
                        setSavePoint = False
                except UnicodeEncodeError:
                    setSavePoint = False
                if item['hash'] is not None:
                    hash = md5(txtFromFile.encode('utf8')).hexdigest()
                    if item['hash'] != hash:
                        reload = True
        index = self.OpenFile(filename=scriptname, f_encoding=item['f_encoding'], 
                              eol=item.get('eol'), workdir=item['workdir'], scripttext=item['text'], 
                              setSavePoint=setSavePoint, splits=item['splits'], 
                              framenum=item['current_frame'], last_length=item.get('last_length'), 
                              group=item.get('group', -1), group_frame=item.get('group_frame'))
        if reload and index is not None: 
            # index is None -> the script was already loaded, different to this other version 
            # but the user chose not to replace it.  If that's the case, don't prompt again 
            # for discarding the current script state.
            self.reloadList.append((index, scriptname, txt))
        return index
    
    def ReloadModifiedScripts(self):
        if self.reloadList:
            for index, filename, text in self.reloadList:
                self.scriptNotebook.SetSelection(index)
                dlg = wx.MessageDialog(self, _('File has been modified since the session was saved. Reload?'),
                    os.path.basename(filename), wx.YES_NO)
                ID = dlg.ShowModal()
                dlg.Destroy()
                if ID == wx.ID_YES:
                    script = self.currentScript
                    script.SetText(text)
                    script.SetSavePoint()
            self.reloadList = []
    
    def SaveSession(self, filename=None, saverecentdir=True, frame=None, previewvisible=None):
        # Get the filename to save from the user
        if filename is None:
            filefilter = 'Session (*.ses)|*.ses'
            initialdir = self.options['recentdirSession']
            if not os.path.isdir(initialdir):
                initialdir = self.programdir
            dlg = wx.FileDialog(self,_('Save the session'),
                initialdir, '', filefilter, wx.SAVE | wx.OVERWRITE_PROMPT)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filename = dlg.GetPath()
            dlg.Destroy()
        if filename is not None:
            # Get the text from each script
            scripts = []
            for index in xrange(self.scriptNotebook.GetPageCount()):
                scripts.append(self.GetTabInfo(index))
            # Get the remaining session information, store in a dict
            session = {}
            if frame is None:
                session['frame'] = self.GetFrameNumber()
            else:
                session['frame'] = frame
            if previewvisible is None:
                session['previewWindowVisible'] = self.previewWindowVisible
            else:
                session['previewWindowVisible'] = previewvisible
            session['preview_placement'] = self.mainSplitter.GetSplitMode()
            session['scripts'] = scripts
            session['lastclosed'] = self.lastClosed
            session['bookmarks'] = list(self.GetBookmarkFrameList().items())
            session['bookmarkDict'] = self.bookmarkDict
            # Save info to filename
            f = open(filename, mode='wb')
            cPickle.dump(session, f, protocol=0)
            f.close()
            # Save the recent dir
            if saverecentdir:
                dirname = os.path.dirname(filename)
                if os.path.isdir(dirname):
                    self.options['recentdirSession'] = dirname
            return True
    
    def GetTabInfo(self, index=None):
        '''Get the script text and other info'''
        if index is None:
            index = self.scriptNotebook.GetSelection()
        boolSelected = index == self.scriptNotebook.GetSelection()
        script = self.scriptNotebook.GetPage(index)
        scriptname = script.filename
        if not os.path.isfile(scriptname):
            hash = None
            title = self.scriptNotebook.GetPageText(index)
            if not title.startswith(self.NewFileName):
                scriptname = title
        else:
            txt = self.GetTextFromFile(scriptname)[0]
            hash = md5(txt.encode('utf8')).hexdigest()
        splits = (script.lastSplitVideoPos, script.lastSplitSliderPos, script.sliderWindowShown)
        return dict(name=scriptname, selected=boolSelected, text=script.GetText(), 
                    hash=hash, splits=splits, current_frame=script.lastFramenum, 
                    last_length=script.lastLength, f_encoding=script.encoding, eol=script.eol,
                    workdir=script.workdir, group=script.group, group_frame=script.group_frame)
    
    def SaveImage(self, filename='', frame=None, silent=False, index=None, avs_clip=None, default='', quality=None, depth=None):
        script, index = self.getScriptAtIndex(index)
        # avs_clip: use 'index' tab, but with an alternative clip
        if not avs_clip:
            avs_clip = script.AVI
        if script is None or avs_clip is None:
            wx.MessageBox(_('No image to save'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        if frame is None:
            frame = self.currentframenum
        extlist = self.imageFormats.keys()
        extlist.sort()
        if not filename:
            defaultdir, title  = (default, '') if os.path.isdir(default) else os.path.split(default)
            isdir = os.path.isdir(defaultdir)
            if not isdir or not title:
                source_dir, source_base = os.path.split(self.GetProposedPath(index, type_='image'))
                if not isdir:
                    defaultdir = source_dir
                if not title:
                    title = os.path.splitext(source_base)[0]
            id = script.GetId()
            if id == self.options['lastscriptid']:
                fmt = self.options['imagenameformat']
            else:
                fmt = self.options['imagenamedefaultformat']
            try:
                defaultname =  fmt % (title, frame)
            except:
                try:
                    defaultname = fmt % frame
                except:
                    try:
                        defaultname = fmt % (frame, title)
                    except:
                        try:
                            defaultname = fmt % title
                        except:
                            defaultname = fmt
            if silent:
                filename = os.path.join(defaultdir, defaultname + 
                                        extlist[self.options['imagechoice']])
                self.options['imagenameformat'] = fmt
                self.options['lastscriptid'] = id
            else:
                if os.name != 'nt' and '2.9' <= wx.version() < '2.9.5': # XXX
                    defaultname = defaultname + extlist[self.options['imagechoice']]
                filefilterList = []
                for ext in extlist:
                    filefilterList.append('%s|*%s' % (self.imageFormats[ext][0], ext))
                maxFilterIndex = len(filefilterList) - 1
                filefilter = '|'.join(filefilterList)
                dlg = wx.FileDialog(self,_('Save current frame'), defaultdir, defaultname,
                    filefilter,wx.SAVE | wx.OVERWRITE_PROMPT,(0,0))
                dlg.SetFilterIndex(min(self.options['imagechoice'], maxFilterIndex))
                ID = dlg.ShowModal()
                if ID == wx.ID_OK:
                    filename = dlg.GetPath()
                    filter = extlist[dlg.GetFilterIndex()]
                    self.options['imagechoice'] = dlg.GetFilterIndex()
                    self.options['imagesavedir'] = os.path.dirname(filename)
                    fmt = os.path.splitext(os.path.basename(filename))[0]
                    fmt = re.sub(re.escape(title), '%s', fmt, 1)
                    fmt = re.sub(r'([0]*?)%d' % frame,
                                 lambda m: '%%0%dd' % len(m.group(0)) if m.group(1) else '%d',
                                 fmt, 1)
                    self.options['imagenameformat'] = fmt
                    self.options['lastscriptid'] = id
                dlg.Destroy()
        else:
            filter = None
        if filename:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in extlist:
                ext = filter if filter else '.bmp'
                filename = '%s%s' % (filename, ext)
            #~if ext == '.png' and depth == 16:
            if ext == '.png' and (depth == 16 or depth is None and self.check_RGB48(script)):
                ret = avs_clip.RawFrame(frame)
                if ret:
                    self.SavePNG(filename, ret, avs_clip.Height / 2)
                    return filename
            else:
                w = avs_clip.DisplayWidth
                h = avs_clip.DisplayHeight
                bmp = wx.EmptyBitmap(w, h)
                mdc = wx.MemoryDC()
                mdc.SelectObject(bmp)
                ret = avs_clip.DrawFrame(frame, mdc)
            if not ret:
                wx.MessageBox(u'\n\n'.join((_('Error requesting frame {number}').format(number=frame), 
                              avs_clip.clip.get_error())), _('Error'), style=wx.OK|wx.ICON_ERROR)
                return
            #~ bmp.SaveFile(filename, self.imageFormats[ext][1])
            img = bmp.ConvertToImage()
            if ext==".jpg":
                if quality is None:
                    quality = self.options['jpegquality']
                    if self.options['askjpegquality'] and not silent:
                        ret = self.MacroGetTextEntry(_('Introduce the JPEG Quality (0-100)'), 
                                       (quality, 0, 100), _('JPEG Quality'), 'spin', 100)
                        if ret != '':
                            quality = self.options['jpegquality'] = ret
                else:
                    quality = int(quality)
                if quality > 100:
                    quality = 100
                elif quality < 0:
                    quality = 0
                img.SetOption(wx.IMAGE_OPTION_QUALITY, str(quality))
            img.SaveFile(filename, self.imageFormats[ext][1])
            return filename
    
    @staticmethod
    def check_RGB48(script):
        """Check if the clip returned by 'script' is RGB48
        
        This is supposed to be removed when SetExtraControlCreator is 
        implemented in wx.FileDialog
        """
        convey = ('Dither_convey_rgb48_on_yv12',  # Dither package
                  'Dither_convert_yuv_to_rgb', 'rgb48yv12')
        re_convey = re.compile(r'[^#]*(?:{0})|({1})\s*\(.*(?(1){2}).*\)'.
                               format(*convey), re.I)
        for i in range(script.GetLineCount() - 1, -1, -1):
            if re_convey.match(script.GetLine(i)):
                return True
    
    @staticmethod
    def SavePNG(filename, buf, height, alpha=False, filter_type=None):
        """PNG encoder in pure Python, based on png.py v0.0.15
        
        Only accepts a RGB48 or RGB64 buffer as input
        """
        # png.py license
        #
        # Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
        # Portions Copyright (C) 2009 David Jones <drj@pobox.com>
        # And probably portions Copyright (C) 2006 Nicko van Someren <nicko@nicko.org>
        #
        # Original concept by Johann C. Rocholl.
        #
        # LICENCE (MIT)
        #
        # Permission is hereby granted, free of charge, to any person
        # obtaining a copy of this software and associated documentation files
        # (the "Software"), to deal in the Software without restriction,
        # including without limitation the rights to use, copy, modify, merge,
        # publish, distribute, sublicense, and/or sell copies of the Software,
        # and to permit persons to whom the Software is furnished to do so,
        # subject to the following conditions:
        #
        # The above copyright notice and this permission notice shall be
        # included in all copies or substantial portions of the Software.
        #
        # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
        # NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
        # BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
        # ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
        # CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        # SOFTWARE.        
        
        # http://www.w3.org/TR/PNG/
        
        byte_depth = 2
        if alpha:
            channels = 4
            color_type = 6
        else:
            channels = 3
            color_type = 2
        bpp = channels * byte_depth
        scanline_size = len(buf) / height
        width = scanline_size / channels / byte_depth
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be greater than zero")
        if width > 2**32-1 or height > 2**32-1:
            raise ValueError("width and height cannot exceed 2**32-1")
        
        def sub_filter(scanline):
            """Apply 'Sub' filter (type 1) to a scanline"""
            for i in range(scanline_size - 1, bpp - 1, -1):
                scanline[i] = (scanline[i] - scanline[i - bpp]) & 0xFF
            return scanline
        
        if filter_type is None:
            filter_type = 0 if width * height > 6e5 else 1 # don't filter HD
        if filter_type == 0: # no filter
            filter = lambda x:x
        elif filter_type == 1: # 10-20% better compression, x3-6 overall time
            filter = sub_filter
        
        def write_chunk(file, tag, data=''):
            """
            Write a PNG chunk to the output file, including length and
            checksum.
            """
            file.write(struct.pack("!I", len(data)))
            file.write(tag)
            file.write(data)
            checksum = zlib.crc32(tag)
            checksum = zlib.crc32(data, checksum)
            checksum &= 2**32-1 # signed int -> unsigned
            file.write(struct.pack("!I", checksum))
        
        with open(filename, 'wb') as file:
            
            # PNG signature
            signature = struct.pack('8B', 137, 80, 78, 71, 13, 10, 26, 10)
            file.write(signature)
            
            # Image header
            write_chunk(file, 'IHDR', struct.pack("!2I5B", width, height, 
                                           byte_depth * 8, color_type, 0, 0, 0))
            # Image data
            compressor = zlib.compressobj(9)
            chunk_limit = 2**20 # 1 MiB
            data = array.array('B') # ugly memory management ahead
            for i in range(0, len(buf), scanline_size):
                data.append(filter_type)
                scanline = array.array('H', buf[i:i + scanline_size])
                scanline.byteswap() # network order (big-endian)
                data.extend(filter(array.array('B', scanline.tostring())))
                if len(data) > chunk_limit:
                    compressed = compressor.compress(data)
                    if len(compressed):
                        write_chunk(file, 'IDAT', compressed)
                    del data[:]
            if len(data):
                compressed = compressor.compress(data)
            else:
                compressed = ''
            flushed = compressor.flush()
            if len(compressed) or len(flushed):
                write_chunk(file, 'IDAT', compressed + flushed)
            
            # Image trailer
            write_chunk(file, 'IEND')
    
    #~ def ZoomPreviewWindow(self, zoomfactor, show=True):
        #~ self.zoomfactor = zoomfactor
        #~ if show:
            #~ self.ShowVideoFrame(forceRefresh=True)
            #self.videoWindow.Refresh()
    
    @AsyncCallWrapper
    def InsertText(self, txt, pos=-1, index=None):
        r'''InsertText(txt, pos=-1, index=None)
        
        Inserts the string 'txt' into the script of the tab located at the zero-based 
        integer 'index' at the text position 'pos'.
        
        If the input 'index' is None, the text is inserted into the script of the 
        currently selected tab.  The input 'pos' can be either an integer representing 
        the zero-based position in the text document (a value of -1 is equivalent 
        to the last position) or a tuple representing the zero-based line and column 
        numbers (a value of -1 is equivalent to the last line or column, respectively).  
        Alternatively, if 'pos' is equal to None, the text is inserted at the current 
        cursor position in the document, replacing any existing selection.  In all 
        cases, the cursor is positioned at the end of the inserted text.
        
        Returns False if insert failed (due to bad inputs), True otherwise.
        
        '''
        # Get the desired script
        if index == -1:
            script = self.scrapWindow.textCtrl
        else:
            script, index = self.getScriptAtIndex(index)
            if script is None:
                return False
        # Insert the text based on the input pos
        #~ try:
            #~ txt = str(txt)
        #~ except UnicodeEncodeError:
            #~ txt = unicode(txt, encoding)
        if type(txt) != unicode:
            txt = unicode(txt, encoding)
        if pos is None:
            script.ReplaceSelection(txt)
            return True
        elif type(pos) == type(0):
            if pos == -2:
                self.InsertTextAtScriptEnd(txt, script)
                return True
            if pos == -1 or pos > script.GetLength():
                pos = script.GetLength()
            if pos < 0:
                pos = 0
            scriptpos = pos
        elif type(pos) == type((0,0)):
            if len(pos) != 2:
                return False
            line, col = pos
            try:
                line = int(line)
                col = int(col)
            except ValueError:
                return False
            if line == - 1 or line >= script.GetLineCount():
                line = script.GetLineCount() - 1
            if line < 0:
                line = 0
            linepos = script.PositionFromLine(line)
            maxCol = script.GetLineEndPosition(line) - linepos
            if col == -1 or col > maxCol:
                col = maxCol
            if col < 0:
                col = 0
            scriptpos = linepos + col
        script.InsertText(scriptpos, txt)
        script.GotoPos(scriptpos + len(txt))
        return True

    def AutoUpdateVideo(self, force=False):
        script = self.currentScript
        newlinenum = script.LineFromPosition(script.GetCurrentPos())
        if self.options['autoupdatevideo']:
            marker = '__END__'
            pos = script.FindText(0, script.GetTextLength(), marker+'$', stc.STC_FIND_REGEXP)
            if pos != -1:
                line = script.LineFromPosition(pos)
                if newlinenum != line:
                    script.SetTargetStart(pos)
                    script.SetTargetEnd(script.GetLineEndPosition(line))
                    script.ReplaceTarget('')
                    pos = script.GetLineEndPosition(newlinenum)
                    script.InsertText(pos, marker)
            if self.oldlinenum is None:
                pass
            elif newlinenum != self.oldlinenum or force:
                script.OnUpdateUI(None)
                self.refreshAVI = True
                self.IdleCall.append((self.ShowVideoFrame, tuple(), dict(focus=False)))
        self.oldlinenum = newlinenum

    def InsertSource(self, filename='', check_selection=False):
        script = self.currentScript
        if check_selection and not filename:
            text = script.GetSelectedText()
            ext = os.path.splitext(text)[1].lstrip('.')
            if ext in self.options['templates']:
                filename = text
        strsource, filename = self.GetSourceString(filename, return_filename=True)
        if script.GetText() == '' and filename is not None and os.path.splitext(filename)[1].lower() in ('.avs', '.avsi', '.vpy'):
            self.OpenFile(filename)
        else:
            if strsource != '':
                script.ReplaceSelection('%s\n' % strsource)
                script.SetFocus()
                self.AutoUpdateVideo()
                if self.FindFocus() == self.videoWindow:
                    self.refreshAVI = True
                    self.ShowVideoFrame()
    
    @AsyncCallWrapper
    def GetSourceString(self, filename='', default='', return_filename=False):
        r'''GetSourceString(filename='', default='')
        
        Returns an appropriate source string based on the file extension of the input 
        string 'filename'.  For example, if 'filename' is "D:\test.avi", the function 
        returns the string "AviSource("D:\test.avi")".  Any unknown extension is wrapped 
        with "DirectShowSource(____)" (AviSynth) or "FFVideoSource(____)" (AvxSynth).  
        Templates can be viewed and defined in the options menu of the program.
        
        If 'filename' is empty, the user is prompted to select a file from a dialog box 
        with 'default' as the default filename; it can be just a directory or basename.
        
        '''
        if not filename or not os.path.isfile(filename):
            extlist = self.options['templates'].keys()
            extlist.sort()
            extlist1 = ', '.join(extlist)
            extlist2 = ';*.'.join(extlist)
            filefilter = (_('Source files') + ' (%(extlist1)s)|*.%(extlist2)s|' + 
                          _('All files') + ' (*.*)|*.*') %  locals()
            default_dir, default_base = (default, '') if os.path.isdir(default) else os.path.split(default)
            initial_dir = default_dir if os.path.isdir(default_dir) else self.GetProposedPath(only='dir')
            dlg = wx.FileDialog(self, _('Insert a source'), initial_dir, default_base, 
                                filefilter, wx.OPEN|wx.FILE_MUST_EXIST)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filename = dlg.GetPath()
            else:
                filename = None
            dlg.Destroy()
        if filename is not None and os.path.isfile(filename):
            dirname = os.path.dirname(filename)
            if os.path.isdir(dirname):
                self.options['recentdir'] = dirname
            ext = os.path.splitext(filename)[1][1:].lower()
            strsource = self.options['templates'].get(ext)
            # TODO: fix unicode bug here?
            if not strsource:
                strsource = self.GetPluginString(filename)
                if not strsource:
                   strsource = u'DirectShowSource(***)' if os.name == 'nt' else  u'FFVideoSource(***)'
            strsource = strsource.replace(u'[***]', u'"%s"' % os.path.basename(filename))
            strsource = strsource.replace(u'***', u'"%s"' % filename)
        else:
            strsource = ''
        if return_filename:
            return (strsource, filename)
        else:
            return strsource

    def InsertPlugin(self, filename=''):
        txt = self.GetPluginString(filename)
        if txt != '':
            script = self.currentScript
            script.ReplaceSelection('%s\n' % txt)
            script.SetFocus()
            self.AutoUpdateVideo()
            if self.FindFocus() == self.videoWindow:
                self.refreshAVI = True
                self.ShowVideoFrame()
    
    @AsyncCallWrapper
    def GetPluginString(self, filename='', default=''):
        r'''GetPluginString(filename='', default='')
        
        Returns an appropriate load plugin string based on the file extension of the 
        input string 'filename'.  For example, if 'filename' is "D:\plugin.dll", the 
        function returns the string "LoadPlugin("D:\plugin.dll")".  VirtualDub and 
        VFAPI (TMPGEnc) plugins are also supported.
        
        If 'filename' is empty, the user is prompted to select a file with a dialog 
        box, always started on the last directory from which a plugin was loaded for 
        easy selection and with 'default' as the default filename; it can be just a 
        directory or basename.
        
        '''
        # It would be a good idea to deprecate this function as macro in favour of 
        # using 'GetSourceString' for both sources and plugins (already does so)
        
        #~ script = self.currentScript
        if not filename or not os.path.isfile(filename):
            if os.name == 'nt':
                filefilter = (_('All supported plugins') + ' (*.dll;*.vdf;*.vdplugin;*.vfp)|*.dll;*.vdf;*.vdplugin;*.vfp|' + 
                              _('AviSynth plugins') + ' (*.dll)|*.dll|' + 
                              _('VirtualDub plugins') + ' (*.vdf;*.vdplugin)|*.vdf;*.vdplugin|' + 
                              _('VFAPI plugins') + ' (*.vfp)|*.vfp|' + 
                              _('All files') + ' (*.*)|*.*')
            else:
                filefilter = (_('AvxSynth plugins') + ' (*.so)|*.so|' + 
                              _('All files') + ' (*.*)|*.*')
            default_dir, default_base = (default, '') if os.path.isdir(default) else os.path.split(default)
            initial_dir = default_dir if os.path.isdir(default_dir) else self.options['recentdirPlugins']
            if not os.path.isdir(initial_dir):
                initial_dir = self.ExpandVars(self.options['pluginsdir'])
            dlg = wx.FileDialog(self, _('Insert a plugin'), initial_dir, default_base, 
                                filefilter, wx.OPEN|wx.FILE_MUST_EXIST)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filename = dlg.GetPath()
            else:
                filename = None
            dlg.Destroy()
        if filename:
            dirname, name = os.path.split(filename)
            basename, ext = os.path.splitext(name)
            ext = ext.lower()
            if ext in ('.dll', '.so'):
                txt = 'LoadPlugin("%s")' % filename
            elif ext in ('.vdf', '.vdplugin'):
                txt = 'LoadVirtualDubPlugin("%s", "%s", 0)' % (filename, basename)
            elif ext == '.vfp':
                txt = 'LoadVFAPIPlugin("%s", "%s")' % (filename, basename)
            else:
                txt = ''
            if os.path.isdir(dirname):
                self.options['recentdirPlugins'] = dirname
        else:
            txt = ''
        return txt

    def InsertFrameNumber(self):
        script = self.currentScript
        txt = str(self.GetFrameNumber())
        script.ReplaceSelection(txt)
        if self.FindFocus() == self.videoWindow:
            self.refreshAVI = True
            self.ShowVideoFrame()

    def InsertSelectionTrims(self, cutSelected=True, insertMode=0, useDissolve=0):
        script = self.currentScript
        selections = self.GetSliderSelections(invert=cutSelected)
        if not selections:
            return False
        trimText = ' ++ '.join(['Trim(%i, %i)' % (start, stop) for start, stop in selections])
        if useDissolve and len(selections) > 1:
            trimText = 'Dissolve(%s, %s)' % (trimText.replace(' ++', ','), useDissolve-1)
        #~ script.ReplaceSelection(trimText)
        if insertMode == 0:
            self.InsertTextAtScriptEnd(trimText, script)
        elif insertMode == 1:
            script.ReplaceSelection(trimText)
        else:
            text_data = wx.TextDataObject(trimText)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(text_data)
                wx.TheClipboard.Close()
        if insertMode in (0,1):
            self.refreshAVI = True
            # Kill all bookmarks (rebuild non-selection bookmarks...)
            bookmarks = [value for value, bmtype in self.GetBookmarkFrameList().items() if bmtype ==0]
            newbookmarks = bookmarks[:]
            self.DeleteAllFrameBookmarks(refreshVideo=False)
            gapframes = 0
            framenum = self.GetFrameNumber()
            newframenum = framenum
            nSelections = len(selections)
            for i in xrange(nSelections):
                # Get the current and previous selection endpoints
                if i == 0:
                    a, b = selections[0]
                    c, d = selections[0]
                    gapframes += a
                else:
                    a, b = selections[i-1]
                    c, d = selections[i]
                    gapframes += (c - b - 1)
                # Create the bookmark marking the removed section
                if i != nSelections - 1:
                    self.AddFrameBookmark(d-gapframes, toggle=False, refreshVideo=False)
                # Update the video slider handle position
                if framenum <= d and framenum > b:
                    if framenum >= c:
                        newframenum -= gapframes
                    else:
                        newframenum = (c-gapframes)
                elif i == 0 and framenum <= b:
                    if framenum >= a:
                        newframenum -= gapframes
                    else:
                        newframenum = 0
                # Update the old bookmarks
                for j in xrange(len(bookmarks)):
                    if bookmarks[j] <= d and bookmarks[j] > b:
                        if bookmarks[j] >= c:
                            newbookmarks[j] -= gapframes
                        else:
                            newbookmarks[j] = (c-gapframes)
            for newbookmark in newbookmarks:
                self.AddFrameBookmark(newbookmark, toggle=False, refreshVideo=False)
            self.ShowVideoFrame(newframenum)
        return True

    def GetSliderSelections(self, invert=False):
        script = self.currentScript
        selections = self.videoSlider.GetSelections()
        if not selections:
            return selections
        if not invert:
            return selections
        else:
            invertedselections = []
            nSelections = len(selections)
            lastframe = script.AVI.Framecount - 1
            for i in xrange(nSelections):
                if i == 0:
                    a, b = selections[0]
                    c, d = selections[0]
                    if a != 0:
                        invertedselections.append((0, a-1))
                else:
                    a, b = selections[i-1]
                    c, d = selections[i]
                    invertedselections.append((b+1, c-1))
                if i == nSelections - 1:
                    if d != lastframe:
                        invertedselections.append((d+1, lastframe))
            return invertedselections

    def ValueInSliderSelection(self, value):
        selections = self.GetSliderSelections(self.invertSelection)
        if selections:
            for start, stop in selections:
                if value >= start and value <= stop:
                    return True
        else:
            return None
        return False

    def _x_InsertBookmarkTrims(self):
        script = self.currentScript
        # Get the bookmarks
        bookmarks = list(self.GetBookmarkFrameList().items())
        nBookmarks = len(bookmarks)
        if nBookmarks <= 0:
            wx.MessageBox(_('No bookmarks defined!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        # Sort and make the bookmarks unique (not required?)
        bookmarks.sort()
        #~ bookmarks2 = []
        #~ for bm in bookmarks:
            #~ if bm not in bookmarks2:
                #~ bookmarks2.append(bm)
        #~ bookmarks = bookmarks2
        if nBookmarks == 1:
            wx.MessageBox(_('There must be more than one unique bookmark to use this feature!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        # Create the Trim commands with pairs of bookmarks
        nPairs = nBookmarks/2
        lastframe = script.AVI.Framecount - 1
        txt = 'Trim(0, '
        for i in xrange(nPairs):
            iA = i * 2
            iB = iA + 1
            lastA = max(bookmarks[iA] - 1, 0)
            firstB = bookmarks[iB]
            txt += '%i) ++ Trim(%i, ' % (lastA, firstB)
        txt += '%i)' % lastframe
        txt = txt.replace('Trim(0, 0) ++ ', '').replace(' ++ Trim(%i, %i)' % (lastframe, lastframe), '')
        script.ReplaceSelection(txt)
        if self.FindFocus() == self.videoWindow:
            self.refreshAVI = True
            # Determine appropriate frame to show
            framenum = self.GetFrameNumber()
            newframenum = framenum
            for i in xrange(nPairs):
                a = bookmarks[i * 2]
                b = bookmarks[i * 2+1]
                if framenum < a:
                    break
                elif framenum < b:
                    newframenum -= (framenum - a)
                    break
                else:
                    newframenum -= (b-a)
            self.ShowVideoFrame(newframenum)

    def InsertTextAtScriptEnd(self, txt, script=None, replaceReturn=False):
        if script is None:
            script = self.currentScript
        text = script.GetText()
        # Find the first valid "return" statement (not in a function)
        lastline = script.GetLineCount() - 1
        maxpos = script.GetTextLength()
        findpos = script.FindText(0, maxpos, 'return', stc.STC_FIND_WHOLEWORD)
        def FindUncommentedText(text, startpos, endpos):
            pos = script.FindText(startpos, endpos, text, 0)
            while pos != -1:
                #~ if script.GetStyleAt(pos) == script.commentStyle:
                if script.GetStyleAt(pos) in script.nonBraceStyles:
                    if startpos < endpos:
                        pos = script.FindText(pos+1, endpos, text, 0)
                    else:
                        pos = script.FindText(pos-1, endpos, text, 0)
                else:
                    return pos
            if startpos < endpos:
                return maxpos + 1
            else:
                return pos
        while findpos != -1:
            # Check if line is commented
            #~ boolComment = script.GetStyleAt(findpos) == script.commentStyle
            boolComment = script.GetStyleAt(findpos) in script.nonBraceStyles
            # Check if the return is inside a function
            openposPre = FindUncommentedText('{', findpos, 0)
            closeposPre = FindUncommentedText('}', findpos, 0)
            openposPost = FindUncommentedText('{', findpos, maxpos)
            closeposPost = FindUncommentedText('}', findpos, maxpos)
            boolFunction = closeposPost < openposPost and openposPre > closeposPre
            # Find the next return if current one is invalid
            if boolComment or boolFunction:
                findpos = script.FindText(findpos+1, maxpos, 'return', stc.STC_FIND_WHOLEWORD)
            else:
                break
        if findpos == -1:
            for line in range(lastline, -1, -1):
                linetxt = script.GetLine(line)
                if linetxt.strip():
                    if linetxt.strip().startswith('#'):
                        continue
                    else:
                        if line < lastline:
                            pos = script.PositionFromLine(line+1)
                            script.GotoPos(pos)
                            script.ReplaceSelection('%s\n' % txt)
                        else:
                            pos = script.GetLineEndPosition(line)
                            script.GotoPos(pos)
                            script.ReplaceSelection('\n%s' % txt)
                    return
            script.GotoPos(0)
            script.ReplaceSelection(txt)
        else:
            line = script.LineFromPosition(findpos)
            endpos = script.GetLineEndPosition(line)
            text = script.GetTextRange(findpos, endpos)
            if text.count('+') > 0 or replaceReturn:
                # Possible conflict with + or ++ shorthand for Aligned/UnalignedSplice()
                script.SetTargetStart(findpos)
                script.SetTargetEnd(findpos+len('return'))
                script.ReplaceTarget('last =')
                while script.GetLine(line).strip()[-1] == '\\' and line < lastline:
                    line += 1
                if line < lastline:
                    pos = script.PositionFromLine(line+1)
                    script.GotoPos(pos)
                    script.ReplaceSelection('return %s\n' % txt)
                else:
                    pos = script.GetLineEndPosition(line)
                    script.GotoPos(pos)
                    script.ReplaceSelection('\nreturn %s' % txt)
            else:
                while script.GetLine(line).strip()[-1] == '\\' and line < lastline:
                    line += 1
                pos = script.GetLineEndPosition(line)
                while unichr(script.GetCharAt(pos-1)).strip() == '' or script.GetStyleAt(pos-1) in script.nonBraceStyles:
                    pos -= 1
                script.GotoPos(pos)
                script.ReplaceSelection('.%s' % txt)

    def GetBookmarkFrameList(self, copy=False):
        return self.videoSlider.GetBookmarks(copy)

    def SetBookmarkFrameList(self, bookmarks):
        self.DeleteAllFrameBookmarks()
        lastindex = len(bookmarks) - 1
        for i, item in enumerate(bookmarks):
            try:
                value, bmtype = item
            except TypeError:
                value = item
                bmtype = 0
            if i != lastindex:
                self.AddFrameBookmark(value, bmtype, refreshProgram=False)
            else:
                self.AddFrameBookmark(value, bmtype, refreshProgram=True)

    def DeleteFrameBookmark(self, value, bmtype=0, refreshVideo=True, refreshProgram=True):
        sliderList = [self.videoSlider]
        if self.separatevideowindow:
            sliderList.append(self.videoSlider2)
        for slider in sliderList:
            if value is None:
                slider.RemoveAllBookmarks()
            else:
                slider.RemoveBookmark(value, bmtype, refresh=refreshProgram)
        if refreshProgram:
            self.UpdateBookmarkMenu()
            if refreshVideo and self.trimDialog.IsShown():
                self.ShowVideoFrame()

    def DeleteAllFrameBookmarks(self, bmtype=None, start=0, end=None, refreshVideo=True):
        if bmtype is None:
            self.DeleteFrameBookmark(None, refreshVideo=refreshVideo)
        else:
            sliderList = [self.videoSlider]
            if self.separatevideowindow:
                sliderList.append(self.videoSlider2)
            for slider in sliderList:
                #~ bmList = self.GetBookmarkFrameList()
                bookmarks = slider.GetBookmarks()
                lastindex = len(bookmarks) - 1
                bm = [(value, bmType) for (value, bmType) in bookmarks.items() 
                      if bmtype == bmType and value >= start and (end is None or value <= end)]
                if not bm:
                    return
                toggle_color = False
                for value, bmType in bm[:-1]:
                    slider.RemoveBookmark(value, bmtype, refresh=False)
                    if not toggle_color and self.currentframenum == value:
                        toggle_color = True
                slider.RemoveBookmark(bm[-1][0], bmtype, refresh=True)
            if toggle_color:
                self.frameTextCtrl.SetForegroundColour(wx.BLACK)
                self.frameTextCtrl.Refresh()
                if self.separatevideowindow:
                    self.frameTextCtrl2.SetForegroundColour(wx.BLACK)
                    self.frameTextCtrl2.Refresh()
            self.UpdateBookmarkMenu()

    def AddFrameBookmark(self, value, bmtype=0, toggle=True, refreshVideo=True, refreshProgram=True):
        #~ sliderList = [self.videoSlider]
        #~ if self.separatevideowindow:
            #~ sliderList.append(self.videoSlider2)
        sliderList = self.GetVideoSliderList()
        if not toggle:
            for slider in sliderList:
                slider.SetBookmark(value, bmtype)
        else:
            # Check if bookmark already exists
            bookmarks = self.GetBookmarkFrameList()
            try:
                bmtype2 = bookmarks[value]
                for slider in sliderList:
                    if bmtype != bmtype2:
                        slider.SetBookmark(value, bmtype, refresh=refreshProgram)
                        color = wx.RED
                    else:
                        self.DeleteFrameBookmark(value, bmtype, refreshProgram=refreshProgram)
                        #~ self.DeleteFrameBookmark(value, bmtype)
                        color = wx.BLACK
            except KeyError:
                # Bookmark does not already exists
                for slider in sliderList:
                    slider.SetBookmark(value, bmtype, refresh=refreshProgram)
                    color = wx.RED
            value = str(value)
            if value == self.frameTextCtrl.GetLineText(0):
                self.frameTextCtrl.SetForegroundColour(color)
                self.frameTextCtrl.Refresh()
            if self.separatevideowindow and value == self.frameTextCtrl2.GetLineText(0):
                self.frameTextCtrl2.SetForegroundColour(color)
                self.frameTextCtrl2.Refresh()
        if refreshProgram:
            self.UpdateBookmarkMenu()
            if refreshVideo and self.trimDialog.IsShown():
                self.ShowVideoFrame()
    
    def OffsetBookmarks(self, offset):
        if not offset:
            return
        bookmarkList = [frame + offset for frame, bmtype in 
                         self.GetBookmarkFrameList().iteritems() if bmtype == 0]
        self.DeleteAllFrameBookmarks(bmtype=0)
        self.MacroSetBookmark(frame for frame in bookmarkList if frame >= 0)
    
    def GetVideoSliderList(self):
        sliderList = [self.videoSlider]
        if self.separatevideowindow:
            sliderList.append(self.videoSlider2)
        return sliderList

    def UpdateBookmarkMenu(self, event=None):
        #~ bookmarks = [bookmark for bookmark, bmtype in self.GetBookmarkFrameList()]
        #~ nBookmarks = len(bookmarks)
        for i in xrange(self.menuBookmark.GetMenuItemCount()-4):
            self.menuBookmark.DestroyItem(self.menuBookmark.FindItemByPosition(0))
        pos = 0
        bookmarkList = list(self.GetBookmarkFrameList().items())
        if len(bookmarkList) > 1000: return
        #~for key in self.bookmarkDict.keys():
            #~if (key, 0) not in bookmarkList:
                #~del self.bookmarkDict[key]
        sortItem = self.menuBookmark.FindItemByPosition(1)
        timecodeItem = self.menuBookmark.FindItemByPosition(2)
        titleItem = self.menuBookmark.FindItemByPosition(3)
        if sortItem.IsChecked():
            bookmarkList.sort()
        width = len(str(max(bookmarkList)[0])) if bookmarkList else 0
        fmt = '%%%dd ' % width
        for bookmark, bmtype in bookmarkList:
            if bmtype == 0:
                label = fmt % bookmark
                if timecodeItem.IsChecked():
                    if self.currentScript.AVI:
                        sec = bookmark / self.currentScript.AVI.Framerate
                        min, sec = divmod(sec, 60)
                        hr, min = divmod(min, 60)
                        label += '[%02d:%02d:%06.3f]' % (hr, min, sec)
                    else:
                        label += '[??:??:??.???]'
                if titleItem.IsChecked():
                    label += ' ' + self.bookmarkDict.get(bookmark, '')
                menuItem = self.menuBookmark.Insert(pos, wx.ID_ANY, label, _('Jump to specified bookmark'))
                self.Bind(wx.EVT_MENU, self.OnMenuVideoGotoFrameNumber, menuItem)
                pos += 1

    def SetSelectionEndPoint(self, bmtype):
        if bmtype not in (1,2):
            return
        if not self.trimDialog.IsShown():
            self.OnMenuVideoTrimEditor(None)
        self.AddFrameBookmark(self.GetFrameNumber(), bmtype)
    
    def MoveFrameRanges(self, ranges, paste_frame=None, paste_before=False, 
                        insert_in_script=True):
        """Cut frames ranges from the timeline and paste them before or after a specified frame
        
        'ranges' is a sequence of (start, end) pairs. Return value is 
        the new timeline in the same format.
        
        If 'paste_frame' is not given then the current frame is taken
        
        By default the ranges are inserted after 'paste_frame', set 
        'paste_before' to True to insert them before.
        
        By default a line of Trims according to the new timeline is 
        inserted at the end of the script and bookmarks are shifted, 
        it can be disabled by setting 'insert_in_script' to False.
        
        """
        script = self.currentScript
        self.refreshAVI = True
        if self.UpdateScriptAVI() is None:
            wx.MessageBox(_('Error loading the script'), _('Error'), 
                          style=wx.OK|wx.ICON_ERROR)
            return False
        
        # Construct the new timeline
        cut_ranges = []
        new_timeline_left = []
        new_timeline_right = []
        last_end = -1
        if paste_frame is None:
            paste_frame = self.GetFrameNumber()
        paste_frame_done = False
        last_frame = script.AVI.Framecount - 1
        if paste_before:
            for (start, end) in sorted(ranges):
                if start - last_end >= 2:
                    if paste_frame_done:
                        new_timeline_right.append((last_end + 1, start - 1))
                    else:
                        if paste_frame <= end:
                            if paste_frame >= start:
                                new_timeline_left.append((last_end + 1, start - 1))
                            elif last_end + 1 == paste_frame:
                                new_timeline_right.append((last_end + 1, start - 1))
                            else:
                                new_timeline_left.append((last_end + 1, paste_frame - 1))
                                new_timeline_right.append((paste_frame, start - 1))
                            paste_frame_done = True
                        else:
                            new_timeline_left.append((last_end + 1, start - 1))
                elif not paste_frame_done and paste_frame <= end:
                    paste_frame_done = True
                cut_ranges.append((start, end))
                last_end = end
            if not paste_frame_done:
                new_timeline_left.append((last_end + 1, paste_frame - 1))
                new_timeline_right.append((paste_frame, last_frame))
            elif last_end < last_frame:
                new_timeline_right.append((last_end + 1, last_frame))
        else:
            for (start, end) in sorted(ranges):
                if start - last_end >= 2:
                    if paste_frame_done:
                        new_timeline_right.append((last_end + 1, start - 1))
                    else:
                        if paste_frame <= end:
                            if paste_frame >= start - 1:
                                new_timeline_left.append((last_end + 1, start - 1))
                            else:
                                new_timeline_left.append((last_end + 1, paste_frame))
                                new_timeline_right.append((paste_frame + 1, start - 1))
                            paste_frame_done = True
                        else:
                            new_timeline_left.append((last_end + 1, start - 1))
                elif not paste_frame_done and paste_frame <= end:
                    paste_frame_done = True
                cut_ranges.append((start, end))
                last_end = end
            if not paste_frame_done:
                if paste_frame == last_frame:
                    new_timeline_left.append((last_end + 1, last_frame))
                else:
                    new_timeline_left.append((last_end + 1, paste_frame))
                    new_timeline_right.append((paste_frame + 1, last_frame))
            elif last_end < last_frame:
                new_timeline_right.append((last_end + 1, last_frame))
        new_timeline = new_timeline_left + cut_ranges + new_timeline_right
        
        if not insert_in_script:
            return new_timeline
        
        # Shift bookmarks as needed
        
        # Get a dictionary {frame range: bookmarks in that range}
        range_bm_dict = collections.defaultdict(list)
        for frame, bmtype in self.GetBookmarkFrameList().iteritems():
            if bmtype != 0:
                continue
            for i, (start, end) in enumerate(new_timeline):
                if start <= frame <= end:
                    range_bm_dict[i].append(frame)
                    break
        
        # Get the new bookmark list
        new_bookmarks = []
        frame_count = 0
        new_frame = None
        for i, (start, end) in enumerate(new_timeline):
            offset = frame_count - start
            new_bookmarks.extend([bm + offset for bm in range_bm_dict[i]])
            frame_count += end - start + 1 
            if new_frame is None and start <= paste_frame <= end:
                new_frame = paste_frame + offset
        
        # Replace the current bookmarks with the new ones
        self.DeleteAllFrameBookmarks(bmtype=0)
        self.MacroSetBookmark(new_bookmarks)
        
        # Fix case Trim(0,0)
        new_timeline2 = new_timeline[:]
        try: # 'end' parameter is only available in avisynth v2.6+
            new_timeline2[new_timeline.index((0,0))] = (0, -1)
        except ValueError:
            pass
        
        # Insert a line of Trims at the end of the script
        pos = script.GetLength()
        new_timeline_str = '++'.join(
                     ['Trim({},{})'.format(*trim) for trim in new_timeline2])
        script.InsertText(pos, '\n' + new_timeline_str)
        script.GotoPos(pos + 1 + len(new_timeline_str))
        
        # Navigate to the initial frame and hide trim selection editor
        self.refreshAVI = True
        self.ShowVideoFrame(new_frame)
        if self.trimDialog.IsShown():
            self.OnTrimDialogCancel(None)
        
        return new_timeline
    
    @AsyncCallWrapper
    def GetFrameNumber(self):
        r'''GetFrameNumber()
        
        Returns the current integer frame number of the video preview slider.
        
        '''
        return self.videoSlider.GetValue()

    def InsertUserSlider(self):
        script = self.currentScript
        sliderTexts, sliderProperties = self.GetScriptSliderProperties(script.GetText())
        #~ labels = [str(p[0].strip('"')) for p in sliderProperties]
        labels = []
        for p in sliderProperties:
            if p is None:
                continue
            try:
                temp = str(p[0].strip('"'))
            except UnicodeEncodeError:
                temp = p[0].strip('"')
            labels.append(temp)
        # Check if user selected a number to replace
        txt = script.GetSelectedText()
        try:
            float(txt)
            dlg = UserSliderDialog(self, labels, initialValueText=txt)
        except ValueError:
            dlg = UserSliderDialog(self, labels)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            script.ReplaceSelection(dlg.GetSliderText())
            if self.FindFocus() == self.videoWindow:
                self.refreshAVI = True
                self.ShowVideoFrame()
        dlg.Destroy()

    def SetScriptStatusText(self, line=None, col=None):
        if line==None or col==None:
            script = self.currentScript
            pos = script.GetCurrentPos()
            line = script.LineFromPosition(pos)
            col = script.GetColumn(pos)
        line += 1
        text = _('Line: %(line)i  Col: %(col)i') % locals()
        statusBar = self.GetStatusBar()
        width = min(statusBar.GetClientSize()[0] - statusBar.GetTextExtent(text)[0] - 6,
                    statusBar.GetTextExtent(text)[0] + 40)
        width = max(0, width)
        statusBar.SetStatusWidths([-1, width])
        statusBar.SetStatusText(text, 1)
        #~ self.SetStatusWidths([-1, 0])
        #~ self.SetStatusText(' '+_('Line: %(line)i  Col: %(col)i') % locals())

    def SetVideoStatusText(self, frame=None, primary=True, addon=''):
        if self.cropDialog.IsShown():
            self.SetVideoCropStatusText()
            return
        if not frame:
            frame = self.videoSlider.GetValue()
        script = self.currentScript
        if script.AVI:
            text = self.status_bar_formatter.vformat(
                                ' ' + self.videoStatusBarInfoParsed + '      ', 
                                [], self.GetVideoInfoDict(script, frame, addon))
        else:
            text = ' %s %i'  % (_('Frame'), frame)
        text2 = text.rsplit('\\T\\T', 1)
        if primary:
            if len(text2) == 2:
                statusBar = self.GetStatusBar()
                width = min(statusBar.GetClientSize()[0] - statusBar.GetTextExtent(text2[0])[0] - 6,
                            statusBar.GetTextExtent(text2[1])[0] + 18)
                if width < 0:
                    width = 0
                statusBar.SetStatusWidths([-1, width])
                statusBar.SetStatusText(text2[0], 0)
                statusBar.SetStatusText(text2[1], 1)
            else:
                self.SetStatusWidths([-1, 0])
                self.SetStatusText(text)
        if self.separatevideowindow:
            if len(text2) == 2:
                width = min(self.videoStatusBar.GetClientSize()[0] - self.videoStatusBar.GetTextExtent(text2[0])[0] - 6,
                            self.videoStatusBar.GetTextExtent(text2[1])[0] + 18)
                if width < 0:
                    width = 0
                self.videoStatusBar.SetStatusWidths([-1, width])
                self.videoStatusBar.SetStatusText(text2[0], 0)
                self.videoStatusBar.SetStatusText(text2[1], 1)
            else:
                self.videoStatusBar.SetStatusWidths([-1, 0])
                self.videoStatusBar.SetStatusText(text)

    def SetVideoCropStatusText(self):
        script = self.currentScript
        left = self.cropValues['left']
        top = self.cropValues['top']
        mright = self.cropValues['-right']
        mbottom = self.cropValues['-bottom']
        wcrop = script.AVI.Width - left - mright
        if wcrop % 32 == 0:
            wmod = 'WMOD = 32'
        elif wcrop % 16 == 0:
            wmod = 'WMOD = 16'
        elif wcrop % 8 == 0:
            wmod = 'WMOD =  8'
        elif wcrop % 4 == 0:
            wmod = 'WMOD =  4'
        elif wcrop % 2 == 0:
            wmod = 'WMOD =  2'
        else:
            wmod = 'WMOD =  1'
        hcrop = script.AVI.Height - top - mbottom
        if hcrop % 32 == 0:
            hmod = 'HMOD = 32'
        elif hcrop % 16 == 0:
            hmod = 'HMOD = 16'
        elif hcrop % 8 == 0:
            hmod = 'HMOD =  8'
        elif hcrop % 4 == 0:
            hmod = 'HMOD =  4'
        elif hcrop % 2 == 0:
            hmod = 'HMOD =  2'
        else:
            hmod = 'HMOD =  1'
        arCrop = '%.03f:1' % (wcrop / float(hcrop))
        if arCrop == '1.000:1':
            arCrop = '1:1'
        if arCrop == '1.333:1':
            arCrop = '4:3'
        if arCrop == '1.778:1':
            arCrop = '16:9'
        ar = '%.03f:1' % (script.AVI.Width / float(script.AVI.Height))
        if ar == '1.000:1':
            ar = '1:1'
        if ar == '1.333:1':
            ar = '4:3'
        if ar == '1.778:1':
            ar = '16:9'
        zoom = ''
        if self.zoomfactor != 1:
            if self.zoomfactor < 1 or self.zoomwindow:
                zoom = '(%.2fx) ' % self.zoomfactor
            else:
                zoom = '(%ix) ' % self.zoomfactor
        text = (
            ' Crop(%i,%i,-%i,-%i) - %ix%i (%s) - %s  %s \\T\\T %s %ix%i (%s)  -  %.03f fps      ' %
            (
                left, top, mright, mbottom,
                wcrop, hcrop, arCrop, wmod, hmod,
                zoom, script.AVI.Width, script.AVI.Height, ar, script.AVI.Framerate
            )
        )
        text2 = text.rsplit('\\T\\T', 1)
        statusBar = self.GetStatusBar()
        width = min(statusBar.GetClientSize()[0] - statusBar.GetTextExtent(text2[0])[0] - 6,
                    statusBar.GetTextExtent(text2[1])[0] + 12)
        if width < 0:
            width = 0
        statusBar.SetStatusWidths([-1, width])
        statusBar.SetStatusText(text2[0], 0)
        statusBar.SetStatusText(text2[1], 1)
        if self.separatevideowindow:
            width = min(self.videoStatusBar.GetClientSize()[0] - self.videoStatusBar.GetTextExtent(text2[0])[0] - 6,
                        self.videoStatusBar.GetTextExtent(text2[1])[0] + 12)
            if width < 0:
                width = 0
            self.videoStatusBar.SetStatusWidths([-1, width])
            self.videoStatusBar.SetStatusText(text2[0], 0)
            self.videoStatusBar.SetStatusText(text2[1], 1)

    def ResetStatusText(self):
        if self.FindFocus() == self.videoWindow:
            #~ self.SetStatusText('video message')
            self.SetVideoStatusText()
        else:
            #~ self.SetStatusText('text message')
            self.SetScriptStatusText()

    def GetVideoInfoDict(self, script=None, frame=None, addon=''):
        if script is None:
            script = self.currentScript
        if script.AVI is None:
            self.UpdateScriptAVI(script)
        if not frame:
            frame = self.videoSlider.GetValue()
        v = script.AVI
        # read ffms global variables
        try:
            ffms_encodedframetype, ffms_sourcetime = v.ffms_info_cache[self.currentframenum]
        except KeyError:
            try:
                ffms_prefix = script.AVI.env.get_var('FFSARFFVAR_PREFIX')
            except avisynth.AvisynthError as err:
                if str(err) != "NotFound":
                    raise
                ffms_prefix = ''
            try:
                ffms_encodedframetype = chr(script.AVI.env.get_var(ffms_prefix + 'FFPICT_TYPE'))
            except avisynth.AvisynthError as err:
                if str(err) != "NotFound":
                    raise
                ffms_encodedframetype = ''
            try:
                ffms_sourcetime = self.FormatTime(script.AVI.env.get_var(ffms_prefix + 'FFVFR_TIME') / 1000.0)
            except avisynth.AvisynthError as err:
                if str(err) != "NotFound":
                    raise
                ffms_sourcetime = ''
            v.ffms_info_cache[self.currentframenum] = ffms_encodedframetype, ffms_sourcetime
        framerate = v.Framerate
        framecount = v.Framecount
        time = self.FormatTime(frame/framerate)
        totaltime = self.FormatTime(framecount/framerate)
        bookmarktitle = self.bookmarkDict.get(frame, '')
        zoom = ''
        width, height = v.DisplayWidth, v.DisplayHeight
        if self.zoomfactor != 1:
            if self.zoomfactor < 1 or self.zoomwindow:
                zoom = '(%.2fx) ' % self.zoomfactor
            else:
                zoom = '(%ix) ' % self.zoomfactor
        aspectratio = '%.03f:1' % (width / float(height))
        if aspectratio == '1.000:1':
            aspectratio = '1:1'
        if aspectratio == '1.333:1':
            aspectratio = '4:3'
        if aspectratio == '1.778:1':
            aspectratio = '16:9'
        if addon:
            pixelpos, pixelhex, pixelrgb, pixelrgba, pixelyuv = addon
            if v.IsYUV:
                pixelclr = pixelyuv
            elif v.IsRGB32:
                pixelclr = pixelrgba
            else:
                pixelclr = pixelrgb
        else:
            pixelpos, pixelhex, pixelrgb, pixelrgba, pixelyuv, pixelclr = '', '', '', '', '', ''
        frameratenum, framerateden, audiorate, audiolength, audiochannels, audiobits, colorspace, parity = v.FramerateNumerator, v.FramerateDenominator, v.Audiorate, v.Audiolength, v.Audiochannels, v.Audiobits, v.Colorspace, v.GetParity
        if v.IsFrameBased:
            fieldframebased = _('Frame Based')
        else:
            fieldframebased = _('Field Based')
        if parity == 0:
            parity = _('Bottom Field First')
            parityshort = _('BFF')
        else:
            parity = _('Top Field First')
            parityshort = _('TFF')
        if v.IsAudioInt:
            audiotype = _('Integer')
        else:
            audiotype = _('Float')
        return locals()

    def ParseVideoStatusBarInfo(self, info):
        showVideoPixelInfo = False
        for item in ('%POS', '%HEX', '%RGB', '%YUV', '%CLR'):
            if info.count(item) > 0:
                showVideoPixelInfo = True
                break
        keyList = [
            ('%POS', '{pixelpos}'),
            ('%HEX', '{pixelhex}'),
            ('%RGB', '{pixelrgb}'),
            ('%YUV', '{pixelyuv}'),
            ('%CLR', '{pixelclr}'),
            ('%FRN', '{frameratenum}'),
            ('%FRD', '{framerateden}'),
            ('%AUR', '{audiorate:.3f}'),
            ('%AUL', '{audiolength}'),
            ('%AUC', '{audiochannels}'),
            ('%AUB', '{audiobits}'),
            ('%AUT', '{audiotype}'),
            ('%FC', '{framecount}'),
            ('%TT', '{totaltime}'),
            ('%FR', '{framerate:.3f}'),
            ('%CS', '{colorspace}'),
            ('%AR', '{aspectratio}'),
            ('%FB', '{fieldframebased}'),
            ('%PS', '{parityshort}'),
            ('%EFT', '{ffms_encodedframetype}'),
            ('%ST', '{ffms_sourcetime}'),
            ('%BM', '{bookmarktitle}'),
            ('%W', '{width}'),
            ('%H', '{height}'),
            ('%F', '{frame}'),
            ('%T', '{time}'),
            ('%P', '{parity}'),
            ('%Z', '{zoom}'),
        ]
        for key, item in keyList:
            info = info.replace(key, item)
        return info, showVideoPixelInfo
    
    def GetPixelInfo(self, event, string_=False):
        videoWindow = self.videoWindow
        script = self.currentScript
        if script.AVI is None:
            self.UpdateScriptAVI(script, forceRefresh=True)
        w, h = script.AVI.DisplayWidth, script.AVI.DisplayHeight
        dc = wx.ClientDC(videoWindow)
        dc.SetDeviceOrigin(self.xo, self.yo)
        try: # DoPrepareDC causes NameError in wx2.9.1 and fixed in wx2.9.2
            videoWindow.DoPrepareDC(dc)
        except:
            videoWindow.PrepareDC(dc)
        zoomfactor = self.zoomfactor
        if zoomfactor != 1:
            dc.SetUserScale(zoomfactor, zoomfactor)
        if event:
            xpos, ypos = event.GetPosition()
        else:
            xpos, ypos = videoWindow.ScreenToClient(wx.GetMousePosition())
        x = dc.DeviceToLogicalX(xpos)
        y = dc.DeviceToLogicalY(ypos)
        #~ x, y = min(max(x,0),w-1), min(max(y,0),h-1)
        xposScrolled, yposScrolled = self.videoWindow.CalcUnscrolledPosition(xpos,ypos)
        if 0 <= x < w and 0 <= y < h and xposScrolled>=self.xo and yposScrolled>=self.yo:
            #~ xystring = 'xy = (%i,%i)' % (x,y)
            #~ format = self.options['pixelcolorformat']
            #~ if format == 'rgb':
                #~ colorstring = 'rgb = (%i,%i,%i)' % (R,G,B)
            #~ elif format == 'yuv':
                #~ colorstring = 'yuv = (%i,%i,%i)' % (Y,U,V)
            #~ else: #elif format == 'hex':
                #~ colorstring = 'hex = %s' % hexcolor.upper()
            #~ self.SetVideoStatusText(addon='%s%s, %s' % (' '*5,xystring, colorstring))
            
            # Get color from display
            rgb = dc.GetPixel(x, y)
            R,G,B = rgb.Get()
            A = 0
            hexcolor = '$%02x%02x%02x' % (R,G,B)
            Y = 0.257*R + 0.504*G + 0.098*B + 16
            U = -0.148*R - 0.291*G + 0.439*B + 128
            V = 0.439*R - 0.368*G - 0.071*B + 128
            if 'flipvertical' in self.flip:
                y = script.AVI.DisplayHeight - 1 - y
            if 'fliphorizontal' in self.flip:
                x = script.AVI.DisplayWidth - 1 - x
            # Get color from AviSynth
            if not self.bit_depth:
                try:
                    avsYUV = script.AVI.GetPixelYUV(x, y)
                    if avsYUV != (-1,-1,-1):
                        Y,U,V = avsYUV
                    if script.AVI.IsRGB32:
                        avsRGBA = script.AVI.GetPixelRGBA(x, y)
                        if avsRGBA != (-1,-1,-1,-1):
                            R,G,B,A = avsRGBA
                    else:
                        avsRGB = script.AVI.GetPixelRGB(x, y)
                        if avsRGB != (-1,-1,-1):
                            R,G,B = avsRGB
                except:
                    pass
            if not string_:
                return (x, y), hexcolor.upper()[1:], (R, G, B), (R, G, B, A), (Y, U, V)
            xystring = '%s=(%i,%i)' % (_('pos'),x,y)
            hexstring = '%s=%s' % (_('hex'),hexcolor.upper())
            rgbstring = '%s=(%i,%i,%i)' % (_('rgb'),R,G,B)
            rgbastring = '%s=(%i,%i,%i,%i)' % (_('rgba'),R,G,B,A)
            yuvstring = '%s=(%i,%i,%i)' % (_('yuv'),Y,U,V)
            return xystring, hexstring, rgbstring, rgbastring, yuvstring
        else:
            if not 0 <= x < w:
                x = 0 if x < 0 else w - 1
            if not 0 <= y < h:
                y = 0 if y < 0 else h - 1
            if 'flipvertical' in self.flip:
                y = script.AVI.DisplayHeight - 1 - y
            if 'fliphorizontal' in self.flip:
                x = script.AVI.DisplayWidth - 1 - x
            xystring = '%s=(%i,%i)' % (_('pos'),x,y)
            return xystring if string_ else (x, y), None, None, None, None
    
    @AsyncCallWrapper
    def SelectTab(self, index=None, inc=0):
        r'''SelectTab(index=None, inc=0)
        
        Selects the tab located at the integer 'index', where an index of 0 indicates 
        the first tab.  If the 'index' is None, the integer 'inc' is used instead 
        to determine which tab to select, where inc is an offset from the currently 
        selected tab (negative values for inc are allowable).  Returns False upon 
        failure (invalid input), True otherwise.
        
        '''
        nTabs = self.scriptNotebook.GetPageCount()
        if nTabs == 1:
            self.scriptNotebook.SetSelection(0)
            return True
        if index is None:
            index = inc + self.scriptNotebook.GetSelection()
            # Allow for wraparound with user-specified inc
            if index<0:
                index = nTabs - abs(index) % nTabs
                if index == nTabs:
                    index = 0
            if index > nTabs-1:
                index = index % nTabs
        # Limit index if specified directly by user
        if index < 0:
            return False
        if index > nTabs - 1:
            return False
        if not self.separatevideowindow:
            self.scriptNotebook.SetSelection(index)
        else:
            self.Freeze()
            self.scriptNotebook.SetSelection(index)
            self.Thaw()
        return True

    def ShowFunctionDefinitionDialog(self, functionName=None, functionArgs=None):
        dlg = AvsFunctionDialog(
            self,
            self.optionsFilters,
            self.options['filteroverrides'],
            self.avsfilterdict,
            self.options['filterpresets'],
            self.options['filterremoved'],
            self.options['autocompletepluginnames'],
            self.plugin_shortnames,
            self.installed_plugins_filternames,
            self.installed_avsi_filternames,
            functionName=functionName,
            functionArgs=functionArgs,
            CreateDefaultPreset=self.currentScript.CreateDefaultPreset,
            ExportFilterData=self.ExportFilterData,
            
        )
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            self.options['filteroverrides'] = dlg.GetOverrideDict()
            self.options['filterremoved'] = dlg.GetRemovedSet()
            self.options['filterpresets'] = dlg.GetPresetDict()
            self.options['autocompletepluginnames'] = dlg.GetAutocompletePluginNames()
            self.plugin_shortnames = dlg.GetPluginShortNames()
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
            self.defineScriptFilterInfo()
            for i in xrange(self.scriptNotebook.GetPageCount()):
                self.scriptNotebook.GetPage(i).Colourise(0, 0) # set script.GetEndStyled() to 0
        dlg.Destroy()

    def _x_ShowFunctionDefinitionDialog(self, functionName=None):
        # Build and show the dialog
        startDirectory = self.options['lasthelpdir']
        if startDirectory is None:
            startDirectory = self.avisynthdir
            if startDirectory is None:
                startDirectory = '.'
        dlg = AvsFunctionDialog(
            self,
            (self.optionsFilters, self.optionsFilterPresets, self.optionsFilterDocpaths, self.optionsFilterTypes, self.optionsKeywordLists),
            title=_('Edit AviSynth function information'),
            keyTitle=_('  Function name'),
            valueTitle=_('Function arguments'),
            editable=True,
            insertable=True,
            functionName=functionName,
            startDirectory=startDirectory,
        )
        ID = dlg.ShowModal()
        # Set the data
        if ID == wx.ID_OK:
            self.optionsFilters, self.optionsFilterPresets, self.optionsFilterDocpaths, self.optionsFilterTypes, self.optionsKeywordLists = dlg.GetDict()
            self.options['lasthelpdir'] = dlg.GetLastDirectory()
            for index in xrange(self.scriptNotebook.GetPageCount()):
                script = self.scriptNotebook.GetPage(index)
                script.DefineKeywordCalltipInfo(self.optionsFilters, self.optionsFilterPresets, self.optionsFilterDocpaths, self.optionsFilterTypes, self.optionsKeywordLists)
        dlg.Destroy()

    def _x_ShowFunctionExportImportDialog(self, export=True):
        if export:
            infoDict = (self.optionsFilters, self.optionsFilterPresets, self.optionsFilterDocpaths, self.optionsFilterTypes)
        else:
            # Prompt for the import file
            dlg2 = wx.FileDialog(
                self,
                _('Open filter customization file'),
                self.programdir,
                '',
                '%s|%s' % (_('Filter customization file') + ' (*.tag)|*.tag', 
                           _('Calltip-only text file') + ' (*.txt)|*.txt'),
                wx.OPEN
            )
            ID = dlg2.ShowModal()
            if ID == wx.ID_OK:
                filename = dlg2.GetPath()
                dlg2.Destroy()
                ext = os.path.splitext(filename)[1]
                if ext == '.tag':
                    f = open(filename, mode='rb')
                    try:
                        tempDict = cPickle.load(f)
                        f.close()
                    except cPickle.UnpicklingError:
                        wx.MessageBox(_('Invalid filter customization file!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
                        f.close()
                        dlg2.Destroy()
                        return
                    optionsFilters = dict([(k,v[0]) for k,v in tempDict.items()])
                    optionsFilterPresets = dict([(k,v[1]) for k,v in tempDict.items()])
                    optionsFilterDocpaths = dict([(k,v[2]) for k,v in tempDict.items()])
                    optionsFilterTypes = dict([(k,v[3]) for k,v in tempDict.items()])
                elif ext == '.txt':
                    f = open(filename, mode='r')
                    text = f.read()
                    f.close()
                    filterInfoList = text.split('\n\n')
                    optionsFilters = {}
                    for s in filterInfoList:
                        splitstring = s.split('(', 1)
                        if len(splitstring) == 2:
                            optionsFilters[splitstring[0].strip()] = '('+splitstring[1].strip(' ')
                    optionsFilterPresets = dict([(k,None) for k in optionsFilters.keys()])
                    optionsFilterDocpaths = dict([(k,None) for k in optionsFilters.keys()])
                    optionsFilterTypes = dict([(k,None) for k in optionsFilters.keys()])
                infoDict = (optionsFilters, optionsFilterPresets, optionsFilterDocpaths, optionsFilterTypes)
            else:
                dlg2.Destroy()
                return
        # Build and show the export/import dialog
        dlg = AvsFunctionExportImportDialog(self, infoDict, export=export)
        ID = dlg.ShowModal()
        # Set the data
        if ID == wx.ID_OK:
            dataDict = dlg.GetData()
            if export:
                # Prompt to save the export file
                dlg2 = wx.FileDialog(
                    self,
                    _('Save filter customization file'),
                    self.programdir,
                    '',
                    '%s|%s' % (_('Filter customization file') + ' (*.tag)|*.tag', 
                               _('Calltip-only text file') + ' (*.txt)|*.txt'),
                    wx.SAVE | wx.OVERWRITE_PROMPT
                )
                ID = dlg2.ShowModal()
                if ID == wx.ID_OK:
                    filename = dlg2.GetPath()
                    dlg2.Destroy()
                    ext = os.path.splitext(filename)[1]
                    if ext == '.tag':
                        f = open(filename, mode='wb')
                        cPickle.dump(dataDict, f, protocol=0)
                        f.close()
                    elif ext == '.txt':
                        keys = dataDict.keys()
                        keys.sort()
                        textlines = []
                        for key in keys:
                            textlines.append(key+dataDict[key][0].split('\n\n')[0])
                            textlines.append('')
                        f = open(filename, 'w')
                        f.write('\n'.join(textlines))
                        f.close()
                else:
                    dlg2.Destroy()
                    dlg.Destroy()
                    return
            else:
                # Overwrite AvsP filter information using the imported data
                overwriteAll = dlg.GetOverwriteAll()
                self.UpdateFunctionDefinitions(dataDict, overwriteAll=overwriteAll, wrapCalltip=False)
        dlg.Destroy()

    def _x_UpdateFunctionDefinitions(self, filterInfo, overwriteAll=False, wrapCalltip=True):
        # Validate the filterInfo input
        if type(filterInfo) != dict:
            wx.MessageBox(_('Invalid argument!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        for value in filterInfo.values():
            if len(value) != 4:
                wx.MessageBox(_('Invalid argument!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
                return
        # Create filter info data structure to iterate upon
        a, b, c, d = self.optionsFilters, self.optionsFilterPresets, self.optionsFilterDocpaths, self.optionsFilterTypes
        filterDataDict = dict([(key, (a[key], b[key], c[key], d[key])) for key in self.optionsFilters.keys()])
        filterDataDictKeys = filterDataDict.keys()
        filterDataDictKeysLower = [s.lower() for s in filterDataDictKeys]
        # Update the filter information
        for key, value in filterInfo.items():
            newCalltip, newPreset, newDocpath, newFilterType = value
            # Wrap the newCalltip as necessary
            if wrapCalltip:
                newCalltip = self.wrapFilterCalltip(newCalltip)
            # Validate the newDocpath, set to empty string if invalid
            if newDocpath is not None:
                if not newDocpath.startswith('http://') and not os.path.isfile(newDocpath):
                    newDocpath = ''
            newValue = [newCalltip, newPreset, newDocpath, newFilterType]
            try:
                # Update the existing info
                index = filterDataDictKeysLower.index(key.lower())
                oldkey = filterDataDictKeys[index]
                oldCalltip, oldPreset, oldDocpath, oldFilterType = filterDataDict[oldkey]
                if overwriteAll:
                    if oldkey != key:
                        del filterDataDict[oldkey]
                    for i, oldItem in enumerate((oldCalltip, oldPreset, oldDocpath, oldFilterType)):
                        if newValue[i] is None:
                            newValue[i] = oldItem
                    filterDataDict[key] = newValue
                else:
                    if oldCalltip or newValue[0] is None: newValue[0] = oldCalltip
                    if oldPreset or newValue[1] is None: newValue[1] = oldPreset
                    if oldDocpath or newValue[2] is None: newValue[2] = oldDocpath
                    if True: newValue[3] = oldFilterType
                    filterDataDict[oldkey] = newValue
            except ValueError:
                # Key does not exist, add the new info
                for i in xrange(len(newValue)):
                    if newValue[i] is None:
                        newValue[i] = ''
                        if i == 3:
                            newValue[i] = 0
                filterDataDict[key] = newValue
        self.optionsFilters = dict([(key, value[0]) for key, value in filterDataDict.items()])
        self.optionsFilterPresets = dict([(key, value[1]) for key, value in filterDataDict.items()])
        self.optionsFilterDocpaths = dict([(key, value[2]) for key, value in filterDataDict.items()])
        self.optionsFilterTypes = dict([(key, value[3]) for key, value in filterDataDict.items()])
        # Update the open scripts to reflect filter info changes
        for index in xrange(self.scriptNotebook.GetPageCount()):
            script = self.scriptNotebook.GetPage(index)
            script.DefineKeywordCalltipInfo(self.optionsFilters, self.optionsFilterPresets, self.optionsFilterDocpaths, self.optionsFilterTypes, self.optionsKeywordLists)
    
    def TogglePreviewPlacement(self):
        if self.separatevideowindow:
            return
        if self.previewWindowVisible:
            self.HidePreviewWindow()
            show_preview = True
        else:
            show_preview = False
        if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            self.mainSplitter.SetSplitMode(wx.SPLIT_VERTICAL)
        else:
            self.mainSplitter.SetSplitMode(wx.SPLIT_HORIZONTAL)
        self.SetMinimumScriptPaneSize()
        if show_preview:
            self.ShowVideoFrame()
    
    @AsyncCallWrapper
    def HidePreviewWindow(self):
        r'''HideVideoWindow()
        
        Hides the video preview window if it is visible (note that the video controls 
        are always visible).
        
        '''
        if not self.separatevideowindow:
            self.mainSplitter.Unsplit()
        else:
            self.videoDialog.Hide()
        #~ self.sizer.Show(self.previewWindow, 0, 0)
        #~ self.sizer.Layout()
        self.previewWindowVisible = False
        #~ self.RefitWindow(move=False)

        try:
            if self.cropDialog.IsShown():
                self.OnCropDialogCancel(None)
        except AttributeError:
            pass

        self.toggleButton.SetBitmapLabel(self.bmpVidUp)
        self.toggleButton.Refresh()

        self.currentScript.SetFocus()

    def ShowVideoFrame(self, framenum=None, forceRefresh=False, wrap=True, script=None, 
                       userScrolling=False, keep_env=None, forceLayout=False, doLayout=True, 
                       resize=None, scroll=None, focus=True, adjust_handle=False, check_playing=False):
        if check_playing and not self.playing_video:
            return
        # Exit if disable preview option is turned on
        if self.options['disablepreview']:
            return
        # Update the script AVI
        if script is None:
            script = self.currentScript
        if script.AVI is None:
            forceRefresh = True
        display_clip_refresh_needed = script.display_clip_refresh_needed
        if self.UpdateScriptAVI(script, forceRefresh, keep_env=keep_env) is None:
            #~ wx.MessageBox(_('Error loading the script'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        #~ # Exit if invalid user sliders
        #~ labels = []
        #~ for sliderText in script.sliderTexts:
            #~ try:
                #~ label, minValue, maxValue, value = self.parseSliderText(sliderText)
                #~ labels.append(label)
            #~ except ValueError:
                #~ pass
        # Reset the video frame slider range if necessary
        if self.videoSlider.GetMax() != script.AVI.Framecount-1:
            if adjust_handle:
                pos = float(framenum - self.videoSlider.minValue) / (
                        self.videoSlider.maxValue - self.videoSlider.minValue)
                framenum = int(round(pos * script.AVI.Framecount))
            self.videoSlider.SetRange(0, script.AVI.Framecount-1, refresh=False)
            if self.separatevideowindow:
                self.videoSlider2.SetRange(0, script.AVI.Framecount-1, refresh=False)
        # Get the desired AVI frame to display
        if framenum is None:
            framenum = script.lastFramenum
        try:
            # assume framenum is an integer
            if framenum is None:
                framenum = self.videoSlider.GetValue()
            framenum += 0
        except TypeError:
            # assume framenum is a string (time)
            timetxt = framenum.split(':')
            if len(timetxt) == 3:
                try:
                    hours = int(timetxt[0])
                    minutes = int(timetxt[1])
                    seconds = float(timetxt[2])
                    total_seconds = hours * 60 * 60 + minutes * 60 + seconds
                    framenum = int(round((script.AVI.Framerate * total_seconds)))
                except ValueError:
                    framenum = 0
            else:
                framenum = 0
        except AttributeError: # don't know what framenum is
            framenum = 0
        if framenum < 0:
            if wrap:
                while framenum < 0:
                    framenum += script.AVI.Framecount
            else:
                framenum = 0
        if framenum >= script.AVI.Framecount:
            framenum = script.AVI.Framecount-1
        self.currentframenum = framenum
        
        # Update video slider
        self.videoSlider.SetValue(framenum)
        bms = self.GetBookmarkFrameList()
        if framenum in bms and bms[framenum] == 0:
            color = wx.RED
        else:
            color = wx.BLACK
        self.frameTextCtrl.SetForegroundColour(color)
        self.frameTextCtrl.Replace(0, -1, str(framenum))
        if self.separatevideowindow:
            self.videoSlider2.SetValue(framenum)
            self.frameTextCtrl2.SetForegroundColour(color)
            self.frameTextCtrl2.Replace(0, -1, str(framenum))
        
        # Check for errors when retrieving the frame before updating the gui
        script.AVI.display_clip.get_frame(framenum)
        error = script.AVI.display_clip.get_error()
        if error is not None:
            self.HidePreviewWindow()
            wx.MessageBox(u'\n\n'.join((_('Error requesting frame {number}').format(number=framenum), 
                          error)), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        
        self.videoPaneSizer.Layout()
        #~ self.videoSplitter.UpdateSize()

        # Update sliders...
        doFocusScript = False
        toggleTagNames = [a for a,b in script.toggleTags]
        oldToggleTagNames = [a for a,b in script.oldToggleTags]
        if forceRefresh:
            script.oldSliderTexts = oldToggleTagNames = script.oldAutoSliderInfo = None
        if not userScrolling and (script.sliderTexts != script.oldSliderTexts or toggleTagNames != oldToggleTagNames or script.autoSliderInfo != script.oldAutoSliderInfo):
            if toggleTagNames != oldToggleTagNames:
                self.createToggleTagCheckboxes(script)
            if script.autoSliderInfo != script.oldAutoSliderInfo:
                self.createAutoUserSliders(script)
            if script.sliderTexts != script.oldSliderTexts:
                if not self.createUserSliders(script):
                    #~ return False
                    doFocusScript = True
            script.videoSidebarSizer.Layout()
            script.sliderWindow.FitInside()
            script.sliderWindow.Refresh()

        # Resize the video window as necessary
        oldSize = self.videoWindow.GetVirtualSize()
        videoWidth = w = int(script.AVI.DisplayWidth * self.zoomfactor)
        videoHeight = h = int(script.AVI.DisplayHeight * self.zoomfactor)
        if self.zoomwindowfit:
            self.videoWindow.SetVirtualSize((0, 0))
        if doLayout:
            if forceLayout or not self.previewWindowVisible or videoWidth != self.oldWidth or videoHeight != self.oldHeight:
                self.videoWindow.SetVirtualSize((w+self.xo + 2, h+self.yo + 2))
                if resize is None:
                    if self.currentScript.lastSplitVideoPos is not None:
                        resize = False
                    else:
                        resize = True
                self.LayoutVideoWindows(w, h, resize, forceRefresh=forceRefresh or 
                                                      display_clip_refresh_needed)

                self.toggleButton.SetBitmapLabel(self.bmpVidDown)
                self.toggleButton.Refresh()
        else:
            #~ self.videoWindow.Refresh()
            pass
        newSize = self.videoWindow.GetVirtualSize()
        # Force a refresh when resizing the preview window
        oldVideoSize = (self.oldWidth, self.oldHeight)
        newVideoSize = (videoWidth, videoHeight)        
        self.bmpVideo = None
        if scroll is not None:
            self.Freeze()
        if newSize != oldSize or newVideoSize != oldVideoSize or not self.previewWindowVisible:
            self.videoWindow.Refresh()
            self.previewWindowVisible = True
        else:
            self.previewWindowVisible = True
            # Paint the frame
            dc = wx.ClientDC(self.videoWindow)
            self.PaintAVIFrame(dc, script, self.currentframenum)
        if scroll is not None:
            self.videoWindow.Scroll(*scroll)
            self.Thaw()
        # If error clip, highlight the line with the error
        errmsg = script.AVI.error_message
        if errmsg is not None and not self.options['autoupdatevideo']:
            #~ items = errmsg.lower().split()
            lines = errmsg.lower().split('\n')
            items = lines[-1].split()
            try:
                index = items.index('line') + 1
                if index < len(items):
                    try:
                        linenum = int(items[index].strip('),')) - 1
                        if linenum < script.GetLineCount():
                            posA = script.PositionFromLine(linenum)
                            posB = script.GetLineEndPosition(linenum)
                            script.SetSelection(posA, posB)
                            doFocusScript = True
                    except ValueError:
                        pass
            except ValueError:
                pass
        if doFocusScript:
            #~ self.HidePreviewWindow()
            script.SetFocus()
            script.EnsureCaretVisible()
        else:
            if focus or self.playing_video:
                if focus:
                    self.videoWindow.SetFocus()
                #~ self.SetVideoStatusText(framenum)
                # Update pixel info if cursor in preview windows or playing
                self.IdleCall.append((self.OnMouseMotionVideoWindow, tuple(), {}))
            else:
                primary = self.FindFocus() == self.videoWindow
                addon = ''
                if self.zoomwindowfit:
                    pixelInfo = self.GetPixelInfo(event=None, string_=True)
                    if pixelInfo[1] is not None:
                        addon = pixelInfo
                self.SetVideoStatusText(framenum, primary=primary, addon=addon)
        # Store video information (future use)
        self.oldWidth = videoWidth
        self.oldHeight = videoHeight
        self.oldFramecount = script.AVI.Framecount
        script.oldSliderTexts = script.sliderTexts
        script.oldAutoSliderInfo = script.autoSliderInfo
        script.oldToggleTags = script.toggleTags
        script.lastFramenum = framenum
        script.lastLength = script.AVI.Framecount
        return True

    def LayoutVideoWindows(self, w=None, h=None, resize=True, forcefit=False, forceRefresh=False):
        if w is None:
            w = int(self.currentScript.AVI.DisplayWidth * self.zoomfactor)
        if h is None:
            h = int(self.currentScript.AVI.DisplayHeight * self.zoomfactor)
        # Show or hide slider window
        #~ if not self.zoomwindowfit or self.separatevideowindow:
        if True:
            boolSliders = bool(self.currentScript.sliderTexts or self.currentScript.sliderProperties or self.currentScript.toggleTags or self.currentScript.autoSliderInfo)
            if boolSliders:
                self.toggleSliderWindowButton.Enable()
                if self.currentScript.sliderWindowShown:
                    self.currentScript.sliderWindow.Show()

                    #~ window2 = self.videoSplitter.GetWindow2()
                    #~ if window2 != self.currentScript.sliderWindow:
                        #~ self.videoSplitter.ReplaceWindow(window2, self.currentScript.sliderWindow)
                    #~ else:
                        #~ self.videoSplitter.SetSashPosition(self.currentScript.lastSplitSliderPos)
                    self.ShowSliderWindow(self.currentScript)

                else:
                    if forceRefresh and not self.videoSplitter.IsSplit() and not self.options['keepsliderwindowhidden'] and not self.currentScript.userHidSliders:
                        self.ToggleSliderWindow()
                        #~ pass
                    else:
                        self.HideSliderWindow(self.currentScript)
            else:
                #~ if self.currentScript.sliderWindowShown:
                    #~ self.ToggleSliderWindow()
                #~ else:
                    #~ self.videoSplitter.SetSashPosition(-self.videoSplitter.GetMinimumPaneSize())
                self.currentScript.sliderWindowShown = True
                self.ToggleSliderWindow()
                self.toggleSliderWindowButton.Disable()
        if self.separatevideowindow:
            if self.options['allowresize'] and not self.videoDialog.IsMaximized():
                #~ sizer = self.videoDialog.GetSizer()
                #~ sizer.SetItemMinSize(0, w + 2*self.xo + 300, h + 2*self.yo)
                #~ sizer.Fit(self.videoDialog)
                wA, hA = self.videoDialog.GetSize()
                if self.currentScript.sliderWindowShown:
                    wslider = -self.currentScript.lastSplitSliderPos
                else:
                    wslider = self.videoSplitter.GetMinimumPaneSize() + 5
                wB = (w + 2*self.xo + 20) + (wslider) + self.toggleSliderWindowButton.GetSize()[0] + 5
                hB = (h + 2*self.yo) + 75# + (200)
                #~ wC, hC = wx.ScreenDC().GetSize()
                winpos = self.videoDialog.GetPosition()
                imonitor = max(0, wx.Display.GetFromPoint(winpos))
                display = wx.Display(imonitor)
                wC, hC = display.GetGeometry().GetSize()
                if wB > 0.9 * wC:
                    wB = wA
                if hB > 0.9 * hC:
                    hB = hA
                #~ newsize = (max(wA, wB), max(hA, hB))
                newsize = (max(wA, wB), hB)
                if not self.zoomwindow and newsize != (wA, hA):
                    self.videoDialog.SetSize(newsize)
                    # Move the window if it's offscreen
                    size = self.videoDialog.GetSize()
                    pos = self.videoDialog.GetPosition()
                    if (pos[0]+size[0]>wC) or (pos[1]+size[1]>hC):
                        self.videoDialog.Center()
            self.UpdateProgramTitle()
            self.videoDialog.Show()
            #~ self.videoSplitter.SetSashPosition(self.currentScript.lastSplitSliderPos)
            return
        if resize and self.options['allowresize'] and not self.IsMaximized():
            # Resize the window as necessary
            wA, hA = self.GetSize()
            #~ wB = (w + 2*self.xo + 20) + (self.currentScript.sliderSizer.GetMinSize()[0] + 30) + 5
            if self.currentScript.sliderWindowShown:
                wslider = -self.currentScript.lastSplitSliderPos
            else:
                wslider = self.videoSplitter.GetMinimumPaneSize() + 5
            wB = (w + 2*self.xo + 20) + (wslider) + self.toggleSliderWindowButton.GetSize()[0] + 5
            hB = (h + 2*self.yo) + (200)
            #~ wC, hC = wx.ScreenDC().GetSize()
            winpos = self.GetPosition()
            index = max(0, wx.Display.GetFromPoint(winpos))
            display = wx.Display(index)
            wC, hC = display.GetGeometry().GetSize()
            if wB > 0.9 * wC:
                wB = wA
            if hB > 0.9 * hC:
                hB = hA
            newsize = (max(wA, wB), max(hA, hB))
            if newsize != (wA, hA):
                self.SetSize(newsize)
                # Move the window if it's offscreen
                size = self.GetSize()
                pos = self.GetPosition()
                if (pos[0]+size[0]>wC) or (pos[1]+size[1]>hC):
                    self.Center()
        #~ if self.lastSplitVideoPos is not None:
            #~ self.lastSplitVideoPos = self.mainSplitter.GetSashPosition()
        # Set the splitter positions
        if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            self.SplitVideoWindow(h, forcefit=forcefit)
        else:
            self.SplitVideoWindow(w, forcefit=forcefit)
        #~ self.SplitSliderWindow(w)

    def SplitVideoWindow(self, pos=None, forcefit=False):
        sash_pos = self.GetMainSplitterNegativePosition(pos=pos, forcefit=forcefit)
        if self.mainSplitter.IsSplit():
            self.mainSplitter.SetSashPosition(sash_pos)
        else:
            if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                self.mainSplitter.SplitHorizontally(self.scriptNotebook, self.videoPane, sash_pos)
            else:
                self.mainSplitter.SplitVertically(self.scriptNotebook, self.videoPane, sash_pos)

    def GetMainSplitterNegativePosition(self, pos=None, forcefit=False):
        if not forcefit and self.currentScript.lastSplitVideoPos is not None:
            pos = self.currentScript.lastSplitVideoPos
        else:
            script = self.currentScript
            if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                if pos is None:
                    if script.AVI is None:
                        #~ self.UpdateScriptAVI(script, forceRefresh=True)
                        vidheight = 0
                    else:
                        vidheight = script.AVI.DisplayHeight
                    h = int(vidheight * self.zoomfactor)
                else:
                    h = pos
                pos = -(h + 2 * self.yo + 5 + self.mainSplitter.GetSashSize()/2)
            else:
                if pos is None:
                    if script.AVI is None:
                        #~ self.UpdateScriptAVI(script, forceRefresh=True)
                        vidwidth = 0
                    else:
                        vidwidth = script.AVI.DisplayWidth
                    w = int(vidwidth * self.zoomfactor)
                else:
                    w = pos
                pos = -(w + 2 * self.xo + 5 + self.mainSplitter.GetSashSize()/2 + 
                        self.toggleSliderWindowButton.GetSize()[0])
        return pos

    def ToggleSliderWindow(self, vidrefresh=False):
        self.videoPaneSizer.Layout()
        # TODO...
        if True: #button.IsEnabled():
            #~ self.SplitSliderWindow(forcefit=True)
            if self.currentScript.sliderWindowShown:
                self.HideSliderWindow(self.currentScript)
            else:
                self.ShowSliderWindow(self.currentScript)
        if vidrefresh:
            #~ self.IdleCall = (self.ShowVideoFrame, tuple(), {'forceRefresh': True, 'focus': False})
            if self.zoomwindowfit:
                self.ShowVideoFrame(focus=False, doLayout=False)
                #~ self.ShowVideoFrame(forceRefresh=True, focus=False, doLayout=False)
                #~ self.videoWindow.Refresh()
            #~ wx.FutureCall(100, self.ShowVideoFrame, forceRefresh=True, focus=False)

    def ShowSliderWindow(self, script):
        button = self.toggleSliderWindowButton
        # Show the sliders
        #~ self.videoSplitter.SetSashPosition(self.currentScript.lastSplitSliderPos)
        if self.videoSplitter.IsSplit():
            #~ self.videoSplitter.Unsplit()
            #~ self.videoSplitter.SplitVertically(self.videoWindow, script.sliderWindow, self.currentScript.lastSplitSliderPos)
            self.videoSplitter.ReplaceWindow(self.videoSplitter.GetWindow2(), script.sliderWindow)
            self.videoSplitter.SetSashPosition(self.currentScript.lastSplitSliderPos)
        else:
            self.videoSplitter.SplitVertically(self.videoWindow, script.sliderWindow, self.currentScript.lastSplitSliderPos)
        #~ self.currentScript.lastSplitSliderPos = self.videoSplitter.GetSashPosition() - self.videoSplitter.GetClientSize()[0]
        script.sliderWindow.Show()
        script.sliderWindowShown = True
        button.SetBitmapLabel(button.bmpHide)
        #~ button.SetToolTip(wx.ToolTip(_('Hide slider window')))
        button.Refresh()

    def HideSliderWindow(self, script):
        button = self.toggleSliderWindowButton
        # Hide the sliders
        #~ self.videoSplitter.SetSashPosition(-self.videoSplitter.GetMinimumPaneSize())
        self.videoSplitter.Unsplit()
        script.sliderWindow.Hide()
        script.sliderWindowShown = False
        #~ self.currentScript.lastSplitSliderPos = self.videoSplitter.GetSashPosition() - self.videoSplitter.GetClientSize()[0]
        button.SetBitmapLabel(button.bmpShow)
        #~ button.SetToolTip(wx.ToolTip(_('Show slider window')))
        button.Refresh()

    def ShowVideoOffset(self, offset=0, units='frames', focus=True):
        if self.playing_video:
            self.PlayPauseVideo()
            self.playing_video = ''
        script = self.currentScript
        if script.AVI is None:
            self.UpdateScriptAVI()
        units = units.lower()
        if units == 'frames':
            offsetFrames = offset
        elif units in ('sec', 'seconds'):
            offsetFrames = offset * int(round(script.AVI.Framerate))
        elif units in ('min', 'minutes'):
            offsetFrames = offset * int(round(script.AVI.Framerate * 60))
        elif units in ('hr', 'hours'):
            offsetFrames = offset * int(round(script.AVI.Framerate * 60 * 60))
        framenum = offsetFrames + self.videoSlider.GetValue()
        self.ShowVideoFrame(framenum, wrap=False, script=script, focus=focus)
        if self.playing_video == '':
            self.PlayPauseVideo()

    def GotoNextBookmark(self, reverse=False):
        if self.playing_video:
            self.PlayPauseVideo()
            self.playing_video = ''
        current_frame = self.GetFrameNumber()
        clip = self.currentScript.AVI
        if clip is not None:
            bookmarkValues = [value for value in self.GetBookmarkFrameList().keys() 
                              if value < clip.Framecount]
        else:
            bookmarkValues = [value for value in self.GetBookmarkFrameList().keys()]
        bookmarkValues.sort()
        if len(bookmarkValues) == 0:
            return

        if reverse:
            idx = bisect.bisect_left(bookmarkValues, current_frame) or len(bookmarkValues)
            new_frame = bookmarkValues[idx-1]
        else:
            idx = bisect.bisect_right(bookmarkValues, current_frame)
            if idx == len(bookmarkValues):
                new_frame = bookmarkValues[0]
            else:
                new_frame = bookmarkValues[idx]

        self.ShowVideoFrame(new_frame)
        if self.playing_video == '':
            self.PlayPauseVideo()

    def UpdateScriptAVI(self, script=None, forceRefresh=False, keep_env=None, prompt=True):
        if not script:
            script = self.currentScript
            index = self.scriptNotebook.GetSelection()
        else:
            index = 0
            for index in xrange(self.scriptNotebook.GetPageCount()):
                if script == self.scriptNotebook.GetPage(index):
                    break
        updateDisplayClip = False
        if script.AVI is None:
            self.firstToggled = forceRefresh = True
        elif self.zoomwindow:
            try:
                fitWidth, fitHeight = self.GetFitWindowSize()
                zoomfactorWidth = float(fitWidth) / script.AVI.DisplayWidth
                zoomfactorHeight = float(fitHeight) / script.AVI.DisplayHeight
                if self.zoomwindowfill:
                    self.zoomfactor = zoomfactorHeight if self.mainSplitter.GetSplitMode() == \
                                        wx.SPLIT_HORIZONTAL else zoomfactorWidth
                else:                    
                    self.zoomfactor = min(zoomfactorWidth, zoomfactorHeight)
            except TypeError:
                pass
        fitHeight = fitWidth = None
        #~ if not self.zoomwindow:
            #~ fitHeight = fitWidth = None
        #~ else:
            #~ fitWidth, fitHeight = self.GetFitWindowSize()
            #~ if self.zoomwindowfill:
                #~ fitWidth = None
        #~ if self.zoomwindowfit:
            #~ if script.AVI is not None:
                #~ if script.AVI.Width != fitWidth and script.AVI.Height != fitHeight:
                    #~ forceRefresh = True
                    #~ updateDisplayClip = True
        boolNewAVI = False
        if self.refreshAVI and self.options['refreshpreview'] or forceRefresh:
            if not script.previewtxt:
                script.Colourise(0, script.GetTextLength())
            if self.ScriptChanged(script) or forceRefresh:
                if self.playing_video:
                    self.PlayPauseVideo()
                    self.playing_video = ''
                script.display_clip_refresh_needed = False
                scripttxt = script.GetText()
                # Replace any user-inserted sliders (defined with self.regexp)
                #~ script.SetFocus()
                #~ newScripttxt = self.getCleanText(scripttxt)
                # Backup the current session if paranoia mode is on
                if self.options['paranoiamode']:
                    self.SaveSession(self.lastSessionFilename, saverecentdir=False, previewvisible=False)
                #~ previewname = self.MakePreviewScriptFile(script)
                #~ AVI = PyAVIFile(previewname)
                sDirname = os.path.dirname(script.filename)
                sBasename = self.scriptNotebook.GetPageText(index)
                filename = os.path.join(sDirname, sBasename)
                if script.AVI is None:
                    oldFramecount = 240
                    boolOldAVI = False
                    env = None
                else:
                    oldFramecount = script.AVI.Framecount
                    oldWidth, oldHeight = script.AVI.DisplayWidth, script.AVI.DisplayHeight
                    boolOldAVI = True
                    env = script.AVI.env if keep_env or self.reuse_environment else None
                if updateDisplayClip and False:
                    script.AVI.CreateDisplayClip(fitHeight, fitWidth)
                else:
                    workdir_exp = self.ExpandVars(self.options['workdir'])
                    if (self.options['useworkdir'] and self.options['alwaysworkdir']
                        and os.path.isdir(workdir_exp)):
                            workdir = workdir_exp
                    else:
                        workdir = script.workdir
                    # vpy hack, remove when VapourSynth is supported
                    if os.name == 'nt' and filename.endswith('.vpy'):
                        self.SaveScript(filename)
                    wx.BeginBusyCursor()
                    script.AVI = None
                    script.AVI = pyavs.AvsClip(
                        self.getCleanText(scripttxt), filename, workdir=workdir, env=env, 
                        fitHeight=fitHeight, fitWidth=fitWidth, oldFramecount=oldFramecount, 
                        matrix=self.matrix, interlaced=self.interlaced, swapuv=self.swapuv, 
                        bit_depth=self.bit_depth)
                    wx.EndBusyCursor()
                if not script.AVI.initialized:
                    if prompt:
                        self.HidePreviewWindow()
                        s1 = _('Error loading AviSynth!')
                        if script.AVI.error_message:
                            s2 = script.AVI.error_message
                        else:
                            s2 = _(
                                'Make sure you have AviSynth installed and that there are no '
                                'unstable plugins or avsi files in the AviSynth plugins directory.'
                            )
                            s2 = '\n'.join(textwrap.wrap(s2, 70))
                        wx.MessageBox('%s\n\n%s' % (s1, s2), _('Error'), style=wx.OK|wx.ICON_ERROR)
                    script.AVI = None
                    return None
                # Update the script tag properties
                self.UpdateScriptTagProperties(script, scripttxt)
                self.GetAutoSliderInfo(script, scripttxt)
                script.previewtxt = self.ScriptChanged(script, return_styledtext=True)[1]
                boolNewAVI = True
            if script == self.currentScript:
                self.refreshAVI = False
        if script.display_clip_refresh_needed and not boolNewAVI:
            script.display_clip_refresh_needed = False
            oldWidth, oldHeight = script.AVI.DisplayWidth, script.AVI.DisplayHeight
            boolOldAVI = True
            wx.BeginBusyCursor()
            ok = script.AVI.CreateDisplayClip(matrix=self.matrix, interlaced=self.interlaced, 
                                              swapuv=self.swapuv, bit_depth=self.bit_depth)
            wx.EndBusyCursor()
            if ok:
                boolNewAVI = True
            else:
                return None
        if boolNewAVI:
            if not self.zoomwindow and boolOldAVI and \
                    (oldWidth, oldHeight) != (script.AVI.DisplayWidth, script.AVI.DisplayHeight):
                script.lastSplitVideoPos = None
            script.autocrop_values = None
            if self.cropDialog.IsShown():
                self.PaintCropWarnings()
            self.SetVideoStatusText()
            if self.playing_video == '':
                self.PlayPauseVideo()

        return boolNewAVI
    
    def ScriptChanged(self, script=None, return_styledtext=False):
        """Compare scripts including style, but excluding comment/newline/space"""
        if script is None:
            script = self.currentScript
        scripttxt = script.GetStyledText(0, script.GetTextLength())
        styledtxt = []
        for i in range(0, len(scripttxt), 2):
            style = ord(scripttxt[i+1]) & 31
            if style in script.commentStyle\
            or (style == script.STC_AVS_DEFAULT and scripttxt[i] in ' \t\n'):
                continue
            styledtxt.append(scripttxt[i])
            styledtxt.append(style)
        script_changed = styledtxt != script.previewtxt
        if return_styledtext:
            return script_changed, styledtxt
        return script_changed
    
    def UpdateScriptTagProperties(self, script, scripttxt=None):
        if scripttxt is None:
            scripttxt = script.GetText()
        # First strip out comments from scripttxt
        scripttxt = re.sub(r'#.*?\n', r'\n', '%s\n' % scripttxt)
        # Get the toggle tag info
        script.toggleTags = self.GetScriptToggleTagProperties(scripttxt, stripComments=False)
        # Get the slider info
        script.sliderTexts, script.sliderProperties = self.GetScriptSliderProperties(scripttxt, stripComments=False)
        if script.AVI.IsErrorClip():
            script.toggleTags = []
            script.sliderProperties = []
            script.sliderTexts = []

    def GetAutoSliderInfo(self, script, scripttxt=None):
        script.OnStyleNeeded(None, forceAll=True)
        autoSliderInfo = []
        if script.AVI.IsErrorClip() or not self.options['autoslideron']:
            script.autoSliderInfo = []
            return
        nameDict = {}
        posA = posB = 0
        lastpos = script.GetTextLength()
        while posB < lastpos:
            posB = script.WordEndPosition(posA, 1)
            word = script.GetTextRange(posA, posB)
            #~ if word.lower() in script.keywords:
            if script.GetStyleAt(posA) in script.keywordStyleList:
                filterInfo = self.GetFilterArgMatchedInfo(script, posA)
                if filterInfo is not None:
                    wordlower = word.lower()
                    if not wordlower in nameDict:
                        nameDict[wordlower] = 1
                        filterName = word
                    else:
                        nameDict[wordlower] += 1
                        filterName = '%s (%i)' % (word, nameDict[wordlower])
                    if filterInfo:
                        autoSliderInfo.append((filterName,filterInfo))
            posA = posB+1
        script.autoSliderInfo = autoSliderInfo

    def GetFilterArgMatchedInfo(self, script, startwordpos):
        filterMatchedArgs = script.GetFilterMatchedArgs(startwordpos)
        returnInfo = []
        for index, info in enumerate(filterMatchedArgs):
            calltipIndex, calltipArgEntry, argname, argvalue = info
            if argvalue.count(self.sliderOpenString) > 0:
                continue
            if not calltipArgEntry:
                return []
            if not argname:
                argname = None
            returnInfo.append((calltipArgEntry, argname, argvalue, index))
        return returnInfo

    def GetScriptSliderProperties(self, scripttxt, stripComments=True):
        # First strip out comments from scripttxt
        if stripComments:
            scripttxt = re.sub(r'#.*?\n', r'\n', '%s\n' % scripttxt)
        # Then strip out toggle tags
        scripttxt = self.cleanToggleTags(scripttxt)
        # Then find any user sliders
        sliderTexts = self.regexp.findall(scripttxt)
        sliderProperties = []
        for text in sliderTexts:
            items = [s.strip() for s in text.lstrip(self.sliderOpenString).rstrip(self.sliderCloseString).split(',')]
            if len(items) == 4:
                info = (items[0], items[1], items[2])
            else:
                info = None
            sliderProperties.append(info)
        return sliderTexts, sliderProperties

    def GetScriptToggleTagProperties(self, scripttxt, stripComments=True):
        # First strip out comments from scripttxt
        if stripComments:
            scripttxt = re.sub(r'#.*?\n', r'\n', '%s\n' % scripttxt)
        # Then find any toggle tags
        toggleTags = []
        for endtag in re.findall('\[/.*?\]', scripttxt):
            tagname = endtag[2:-1]
            #~ expr = re.compile('\[%s(\s*=.*?)*?\].*?\[/%s\]' % (tagname, tagname), re.IGNORECASE|re.DOTALL)
            expr = re.compile('\[%s.*?\].*?\[/%s\]' % (tagname, tagname), re.IGNORECASE|re.DOTALL)
            try:
                txt = expr.findall(scripttxt)[0]
                toggleTags.append((tagname, self.boolToggleTag(txt)))
            except IndexError:
                pass
        return toggleTags

    def MakePreviewScriptFile(self, script):
        txt = self.getCleanText(script.GetText())
        txt = self.GetEncodedText(txt, bom=True)
        # Construct the filename of the temporary avisynth script
        dirname = self.GetProposedPath(only='dir')
        if os.path.isdir(dirname):
            altdir_tried = False
        else:
            dirname = self.programdir
            altdir_tried = True
        while True: # os.access doesn't work properly on Windows, let's just try
            previewname = os.path.join(dirname, 'preview.avs')
            i = 1
            while os.path.exists(previewname):
                previewname = os.path.join(dirname, 'preview%i.avs' % i)
                i = i+1
            try:
                with open(previewname, 'wb') as f:
                    f.write(txt)
            except IOError, err: # errno 13 -> permission denied
                if err.errno != 13 or altdir_tried:
                    raise
                dirname = self.programdir
                altdir_tried = True
            else:
                return previewname
    
    def GetFitWindowSize(self):
        wA, hA = self.videoWindow.GetSize()
        w, h = wA - 2 * self.xo, hA - 2 * self.yo
        if not self.separatevideowindow:
            if self.zoomwindowfit and not self.previewWindowVisible:
                w = h = None
            else:
                if self.previewWindowVisible:
                    splitpos = self.mainSplitter.GetSashPosition() - \
                               self.mainSplitter.GetClientSize()[
                                   self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL]
                elif self.currentScript.lastSplitVideoPos is not None:
                    splitpos = self.currentScript.lastSplitVideoPos
                elif self.oldLastSplitVideoPos is not None:
                    splitpos = self.oldLastSplitVideoPos
                else:
                    splitpos = self.GetMainSplitterNegativePosition()
                #~ if self.zoomwindowfit:
                    #~ if self.previewWindowVisible:
                        #~ splitpos = self.mainSplitter.GetSashPosition() - self.mainSplitter.GetClientSize()[1]
                    #~ else:
                        #~ if self.oldLastSplitVideoPos is not None:
                            #~ splitpos = self.oldLastSplitVideoPos
                        #~ else:
                            #~ splitpos = self.GetMainSplitterNegativePosition()
                #~ elif self.currentScript.lastSplitVideoPos is None:
                    #~ splitpos = self.mainSplitter.GetSashPosition() - self.mainSplitter.GetClientSize()[1]
                #~ else:
                    #~ splitpos = self.currentScript.lastSplitVideoPos
                if self.mainSplitter.GetSplitMode() == wx.SPLIT_HORIZONTAL:
                    h = abs(splitpos) - (2 * self.yo + 5 + self.mainSplitter.GetSashSize()/2)
                else:
                    w = abs(splitpos) - (2 * self.xo + 5 + self.mainSplitter.GetSashSize()/2 + 
                                         self.toggleSliderWindowButton.GetSize()[0])
        if h < 4:
            h = None
        if w < 4:
            w = None
        return (w, h)

    def PaintAVIFrame(self, inputdc, script, frame, shift=True, isPaintEvent=False):
        if script.AVI is None:
            if __debug__:
                print>>sys.stderr, 'Error in PaintAVIFrame: script is None'
            return
        if self.zoomwindow or self.zoomfactor != 1 or self.flip:
            try: # DoPrepareDC causes NameError in wx2.9.1 and fixed in wx2.9.2
                self.videoWindow.DoPrepareDC(inputdc)
            except: 
                self.videoWindow.PrepareDC(inputdc)
            if (self.zoomwindow or self.zoomfactor != 1) and self.flip:
                inputdc.SetBrush(wx.RED_BRUSH)
            elif self.flip:
                inputdc.SetBrush(wx.CYAN_BRUSH)
            inputdc.DrawPolygon([wx.Point(0,0), wx.Point(8,0), wx.Point(0,8)])
        if shift:
            inputdc.SetDeviceOrigin(self.xo, self.yo)
        else:
            inputdc.SetDeviceOrigin(0, 0)
        if self.zoomfactor == 1 and not self.flip and not self.zoomwindow:            
            w = script.AVI.DisplayWidth
            h = script.AVI.DisplayHeight
            if self.cropDialog.IsShown() or self.trimDialog.IsShown():
                dc = wx.MemoryDC()
                bmp = wx.EmptyBitmap(w,h)
                dc.SelectObject(bmp)
                if not script.AVI.DrawFrame(frame, dc):
                    wx.MessageBox(u'\n\n'.join((_('Error requesting frame {number}').format(number=frame), 
                                  script.AVI.clip.get_error())), _('Error'), style=wx.OK|wx.ICON_ERROR)
                    return
                self.PaintCropRectangles(dc, script)
                self.PaintTrimSelectionMark(dc, script, frame)
                try: # DoPrepareDC causes NameError in wx2.9.1 and fixed in wx2.9.2
                    self.videoWindow.DoPrepareDC(inputdc)
                except:
                    self.videoWindow.PrepareDC(inputdc)
                inputdc.Blit(0, 0, w, h, dc, 0, 0)
            else:
                dc = inputdc
                try: # DoPrepareDC causes NameError in wx2.9.1 and fixed in wx2.9.2
                    self.videoWindow.DoPrepareDC(dc)
                except:
                    self.videoWindow.PrepareDC(dc)
                if not script.AVI.DrawFrame(frame, dc):
                    wx.MessageBox(u'\n\n'.join((_('Error requesting frame {number}').format(number=frame), 
                                  script.AVI.clip.get_error())), _('Error'), style=wx.OK|wx.ICON_ERROR)
                    return
        else:
            dc = wx.MemoryDC()
            w = script.AVI.DisplayWidth
            h = script.AVI.DisplayHeight
            if isPaintEvent and self.bmpVideo:
                dc.SelectObject(self.bmpVideo)                    
            else:
                bmp = wx.EmptyBitmap(w,h)
                dc.SelectObject(bmp)
                if not script.AVI.DrawFrame(frame, dc):
                    wx.MessageBox(u'\n\n'.join((_('Error requesting frame {number}').format(number=frame), 
                                  script.AVI.clip.get_error())), _('Error'), style=wx.OK|wx.ICON_ERROR)
                    return
                if self.flip:
                    img = bmp.ConvertToImage()
                    if 'flipvertical' in self.flip:
                        img = img.Mirror(False)
                    if 'fliphorizontal' in self.flip:
                        img = img.Mirror()
                    bmp = wx.BitmapFromImage(img)
                    dc.SelectObject(bmp)
                self.PaintTrimSelectionMark(dc, script, frame)
                if self.cropDialog.IsShown():
                    self.PaintCropRectangles(dc, script)
                self.bmpVideo = bmp
            try: # DoPrepareDC causes NameError in wx2.9.1 and fixed in wx2.9.2
                self.videoWindow.DoPrepareDC(inputdc)
            except:
                self.videoWindow.PrepareDC(inputdc)
            inputdc.SetUserScale(self.zoomfactor, self.zoomfactor)
            inputdc.Blit(0, 0, w, h, dc, 0, 0)
            if isPaintEvent and self.zoomwindowfill and self.firstToggled:
                wx.CallAfter(self.ShowVideoFrame)
                self.firstToggled = False
        self.paintedframe = frame
        return True

    def PaintTrimSelectionMark(self, dc, script, frame):
        if self.trimDialog.IsShown() and self.markFrameInOut:
            boolInside = self.ValueInSliderSelection(frame)
            if boolInside is not None:
                dc.SetLogicalFunction(wx.COPY)
                dc.SetPen(wx.Pen(wx.BLACK, 2))
                if boolInside:
                    dc.SetBrush(wx.GREEN_BRUSH)
                    dc.DrawCircle(25, 25, 20)
                else:
                    #~ dc.SetLogicalFunction(wx.COPY)
                    #~ dc.SetBrush(wx.RED_BRUSH)
                    #~ w = script.AVI.Width
                    #~ h = script.AVI.Height
                    #~ a = w/20
                    #~ b = w/10
                    #~ dc.DrawPolygon([(a,a), (a+b,a), (w-a,h-a), (w-a-b,h-a)])
                    #~ dc.DrawPolygon([(w-a,a), (w-a-b,a), (a,h-a), (a+b,h-a)])
                    dc.SetBrush(wx.RED_BRUSH)
                    dc.DrawCircle(25, 25, 20)

    def PaintCropRectangles(self, dc, script):
        '''Paint the crop editor's rectangles'''
        w = script.AVI.Width
        h = script.AVI.Height
        left = self.cropValues['left']
        top = self.cropValues['top']
        mright = self.cropValues['-right']
        mbottom = self.cropValues['-bottom']
        dc.SetLogicalFunction(wx.INVERT)
        if 'flipvertical' in self.flip:
            top, mbottom = mbottom, top
        if 'fliphorizontal' in self.flip:
            left, mright = mright, left
        if top > 0:
            dc.DrawRectangle(0, 0, w, top)
        if mbottom > 0:
            dc.DrawRectangle(0, h - mbottom, w, h)
        if left > 0:
            dc.DrawRectangle(0, top, left, h - mbottom - top)
        if mright > 0:
            dc.DrawRectangle(w - mright, top, mright, h - mbottom - top)
        self.oldCropValues = self.cropValues

    def PaintCropWarnings(self, spinCtrl=None):
        script = self.currentScript
        keys = ('left', 'top', '-right', '-bottom')
        if spinCtrl is not None:
            keys = [key for key in keys if self.cropDialog.ctrls[key] == spinCtrl]
        self.cropDialog.boolInvalidCrop = False
        for key in keys:
            labelCtrl = self.cropDialog.ctrls[key+'Label']
            textCtrl = self.cropDialog.ctrls[key]
            value = textCtrl.GetValue()
            colorspace = script.AVI.Colorspace.lower()
            if (colorspace in ('yuy2', 'yv16') and key in ('left', '-right') and value % 2 or 
                colorspace == 'yv411' and key in ('left', '-right') and value % 4 or 
                colorspace == 'yv12' and value % 2):
                    labelCtrl.SetForegroundColour('red')
                    self.cropDialog.boolInvalidCrop = True
            else:
                    labelCtrl.SetForegroundColour(wx.NullColour)
            labelCtrl.Refresh()
    
    def PlayPauseVideo(self, debug_stats=False):
        """Play/pause the preview clip"""
        if self.playing_video:
            if os.name == 'nt':
                self.timeKillEvent(self.play_timer_id)
                self.timeEndPeriod(self.play_timer_resolution)
            else:
                self.play_timer.Stop()
                #signal.setitimer(signal.ITIMER_REAL, 0) # see below
                #signal.signal(signal.SIGALRM, self.previous_signal_handler)
            self.playing_video = False
            self.play_button.SetBitmapLabel(self.bmpPlay)
            self.play_button.Refresh()
            if self.separatevideowindow:
                self.play_button2.SetBitmapLabel(self.bmpPlay)
                self.play_button2.Refresh()
        elif self.ShowVideoFrame(focus=False) and not self.currentScript.AVI.IsErrorClip():
            script = self.currentScript
            if self.currentframenum == script.AVI.Framecount - 1:
                return
            self.playing_video = True
            self.play_button.SetBitmapLabel(self.bmpPause)
            self.play_button.Refresh()
            if self.separatevideowindow:
                self.play_button2.SetBitmapLabel(self.bmpPause)
                self.play_button2.Refresh()
            if self.play_speed_factor == 'max':
                interval = 1.0 # use a timer anyway to avoid GUI refreshing issues
            else:
                interval =  1000 / (script.AVI.Framerate * self.play_speed_factor)
            
            if os.name == 'nt': # default Windows resolution is ~10 ms
                
                def playback_timer(id, reserved, factor, reserved1, reserved2):
                    """"Callback for a Windows Multimedia timer"""
                    if not self.playing_video:
                        return
                    if debug_stats:
                        current_time = time.time()
                        debug_stats_str = str((current_time - self.previous_time) * 1000)
                        self.previous_time = current_time
                    if self.play_drop and self.play_speed_factor != 'max':
                        frame = self.play_initial_frame
                        increment = int(round(1000 * (time.time() - self.play_initial_time) / interval)) * factor
                        if debug_stats:
                            debug_stats_str += ' dropped: ' + str(increment - self.increment - 1)
                            self.increment = increment
                    else:
                        frame = self.currentframenum
                        increment = 1
                    if debug_stats:
                        print debug_stats_str
                    if not AsyncCall(self.ShowVideoFrame, frame + increment, 
                                     check_playing=True, focus=False).Wait():
                        return
                    if self.currentframenum == script.AVI.Framecount - 1:
                        self.PlayPauseVideo()
                    else:
                        wx.Yield()
                
                def WindowsTimer(interval, callback, periodic=True):
                    """High precision timer (1 ms) using Windows Multimedia"""
                    
                    self.timeGetDevCaps = ctypes.windll.winmm.timeGetDevCaps
                    self.timeBeginPeriod = ctypes.windll.winmm.timeBeginPeriod
                    self.timeEndPeriod = ctypes.windll.winmm.timeEndPeriod
                    self.timeSetEvent = ctypes.windll.winmm.timeSetEvent
                    self.timeKillEvent = ctypes.windll.winmm.timeKillEvent
                    
                    callback_prototype = ctypes.WINFUNCTYPE(None, ctypes.c_uint, 
                        ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong)
                    self.timeSetEvent.argtypes = [ctypes.c_uint, ctypes.c_uint, 
                        callback_prototype, ctypes.c_ulong, ctypes.c_uint]
                    
                    class TIMECAPS(ctypes.Structure):
                        _fields_ = [("wPeriodMin", ctypes.c_uint), 
                                    ("wPeriodMax", ctypes.c_uint)]
                    
                    caps = TIMECAPS()
                    self.timeGetDevCaps(ctypes.byref(caps), ctypes.sizeof(caps))
                    self.play_timer_resolution = max(1, caps.wPeriodMin)
                    self.timeBeginPeriod(self.play_timer_resolution)
                    
                    interval0 = interval
                    factor = max(1, int(round(self.play_timer_resolution / interval)))
                    interval = int(round(interval * factor))
                    self.callback_c = callback_prototype(callback)
                    self.play_initial_frame = self.currentframenum
                    self.play_initial_time = time.time()
                    if debug_stats:
                        print 'speed_factor: {0}, required_interval: {1} '\
                              'interval: {2} interval_factor: {3}'.format(
                              self.play_speed_factor, interval0, interval, factor)
                        self.increment = 0
                        self.previous_time = self.play_initial_time
                    self.play_timer_id = self.timeSetEvent(interval, 
                        self.play_timer_resolution, self.callback_c, factor, periodic)
                
                WindowsTimer(interval, playback_timer)
            
            else: # wx.Timer on *nix.  There's some pending events issues
                # TODO: fix/replace wx.Timer
                
                # signal module causes segmentation fault on high fps
                # similar issues using librt with ctypes
                '''
                global signal
                import signal
                
                def playback_timer(signum, frame):
                    """"SIGALRM handler"""
                    if not self.playing_video:
                        return
                    if debug_stats:
                        current_time = time.time()
                        debug_stats_str = str((current_time - self.previous_time) * 1000)
                        self.previous_time = current_time
                    if self.play_drop and self.play_speed_factor != 'max':
                        frame = self.play_initial_frame
                        increment = int(round((time.time() - self.play_initial_time) / interval)) * factor
                        if debug_stats:
                            debug_stats_str += ' dropped: ' + str(increment - self.increment - 1)
                            self.increment = increment
                    else:
                        frame = self.currentframenum
                        increment = 1
                    if debug_stats:
                        print debug_stats_str
                    if not AsyncCall(self.ShowVideoFrame, frame + increment, 
                                     check_playing=True, focus=False).Wait():
                        return
                    if self.currentframenum == script.AVI.Framecount - 1:
                        self.PlayPauseVideo()
                    elif not wx.GetApp().Yield(True):
                        self.parent.PlayPauseVideo()
                
                interval0 = interval
                factor = max(1, int(round(1 / interval)))
                interval = interval * factor / 1000
                self.previous_signal_handler = signal.signal(signal.SIGALRM, playback_timer)
                self.play_initial_frame = self.currentframenum
                self.play_initial_time = time.time()
                if debug_stats:
                    print 'speed_factor: {0}, required_interval: {1} '\
                          'interval: {2} interval_factor: {3}'.format(
                          self.play_speed_factor, interval0, interval * 1000, factor)
                    self.increment = 0
                    self.previous_time = self.play_initial_time
                signal.setitimer(signal.ITIMER_REAL, interval, interval)
                
                return
                '''
                
                class RunVideoTimer(wx.Timer):
                    def __init__(self, parent, factor=1):
                        wx.Timer.__init__(self)
                        self.parent = parent
                        self.factor = factor
                        self.play_initial_frame = self.parent.currentframenum
                        self.play_initial_time = time.time()
                        self.Yield = wx.GetApp().Yield
                        if debug_stats:
                            self.increment = 0
                            self.previous_time = self.play_initial_time
                    def Notify(self):
                        if not self.parent.playing_video:
                            self.parent.PlayPauseVideo()
                            return
                        if debug_stats:
                            current_time = time.time()
                            debug_stats_str = str((current_time - self.previous_time) * 1000)
                            self.previous_time = current_time
                        if self.parent.play_drop and self.parent.play_speed_factor != 'max':
                            frame = self.play_initial_frame
                            increment = int(round(1000 * (time.time() - self.play_initial_time) / self.GetInterval())) * self.factor
                            if debug_stats:
                                debug_stats_str += ' dropped: ' + str(increment - self.increment - 1)
                                self.increment = increment
                        else:
                            frame = self.parent.currentframenum
                            increment = 1
                        if debug_stats:
                            print debug_stats_str
                        if not self.parent.ShowVideoFrame(frame + increment, 
                                                          check_playing=True, focus=False):
                            return
                        if self.parent.currentframenum == script.AVI.Framecount - 1:
                            self.parent.PlayPauseVideo()
                        elif not self.Yield(True):
                            self.parent.PlayPauseVideo()
                
                interval0 = interval
                factor = max(1, int(round(1 / interval)))
                interval = int(round(interval * factor))
                self.play_timer = RunVideoTimer(self, factor)
                if debug_stats:
                    print 'speed_factor: {0}, required_interval: {1} '\
                          'interval: {2} interval_factor: {3}'.format(
                          self.play_speed_factor, interval0, interval, factor)
                self.play_timer.Start(interval)
    
    def RunExternalPlayer(self, path=None, script=None, args=None, prompt=True):
        if script is None:
            script = self.currentScript
        index = self.scriptNotebook.GetSelection()
        tabTitle = self.scriptNotebook.GetPageText(index)
        if not script.GetModify() and os.path.isfile(script.filename):
            # Always use original script if there are no unsaved changes
            previewname = script.filename
            boolTemp = False
        elif self.options['previewunsavedchanges'] or not os.path.isfile(script.filename):
            previewname = self.MakePreviewScriptFile(script)
            boolTemp = True
        else:
            if self.options['promptwhenpreview']:
                if script.GetModify():
                    dlg = wx.MessageDialog(self, _('Save changes before previewing?'),
                        tabTitle, wx.YES_NO|wx.CANCEL)
                    ID = dlg.ShowModal()
                    dlg.Destroy()
                    if ID == wx.ID_YES:
                        self.SaveScript(script.filename, index)
                    elif ID == wx.ID_CANCEL:
                        pass
            previewname = script.filename
            boolTemp = False
        if path is None:
            path = self.options['externalplayer']
        if args is None:
            args = self.options['externalplayerargs']
        path = self.ExpandVars(path)
        if not os.path.isfile(path):
            if not prompt:
                return False
            filefilter = (_('Executable files') + ' (*.exe)|*.exe|' if os.name == 'nt' else '') + _('All files') + ' (*.*)|*.*'
            dlg = wx.FileDialog(self, _('Select an external player'), '', '', filefilter, wx.OPEN)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                path = dlg.GetPath()
            else:
                path = ''
            dlg.Destroy()
        if not os.path.isfile(path):
            if path != '':
                wx.MessageBox(_('A program must be specified to use this feature!'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        self.options['externalplayer'] = self.ExpandVars(path, False)
        # Run the process
        process = wx.Process(self)
        def OnEndProcess(event):
            try:
                os.remove(previewname)
            except OSError:
                pass
        #~ process.Bind(wx.EVT_END_PROCESS, lambda event: os.remove(previewname))
        if boolTemp:
            process.Bind(wx.EVT_END_PROCESS, OnEndProcess)
        self.pid = wx.Execute('%s "%s" %s' % (path, previewname, args), wx.EXEC_ASYNC, process)
        return True

    def re_replace(self, mo):
        items = mo.group().lstrip(self.sliderOpenString).rstrip(self.sliderCloseString).split(',')
        if len(items) == 4:
            return items[3].strip()
        elif len(items) == 1 and 'separator' in items[0]:
            return ''
        else:
            return mo.group()

    def re_replace2(self, mo):
        txt = mo.group()
        if self.boolToggleTag(txt):
            posA = txt.find(']') + 1
            posB = txt.rfind('[')
            return txt[posA:posB]
        else:
            return ''

    def boolToggleTag(self, txt):
        starttag = txt[1:txt.find(']')]
        boolKeep = True
        try:
            name, value = starttag.split('=')
            try:
                boolKeep = bool(int(value))
            except ValueError:
                pass
        except ValueError:
            pass
        return boolKeep

    def _x_re_replaceStrip(self, mo):
        return ''.join(re.split('\[.*?\]', mo.group()))

    def createAutoUserSliders(self, script):
        script.sliderWindow.Freeze()
        script.sliderSizerNew.Clear(deleteWindows=True)
        script.sliderToggleLabels = []
        menuInfoGeneral = [
            (_('Edit filter database'), '', self.OnSliderLabelEditDatabase, ''),
            (''),
            (_('Toggle all folds'), '', self.OnSliderLabelToggleAllFolds, ''),
            (_('General settings...'), '', self.OnSliderLabelSettings, ''),
        ]
        menuGeneral = self.createMenu(menuInfoGeneral)
        #~ menuInfoNumberSlider = [
            #~ (_('Modify slider properties'), '', self.OnSliderLabelModifySliderProperties, _('')),
        #~ ] + menuInfoGeneral
        #~ menuNumberSlider = self.createMenu(menuInfoNumberSlider)
        exclusionList = self.options['autosliderexclusions'].lower().split()
        row = 0
        for filterName, filterInfo in script.autoSliderInfo:
            if filterName.lower() in exclusionList:
                continue
            separator = None
            for info, enteredName, enteredValue, argIndex in filterInfo:
                # Parse the argument info entered into the script
                splitEnteredValue = enteredValue.split('=')
                if len(splitEnteredValue) == 2:
                    namedArg, strValue = splitEnteredValue
                else:
                    namedArg = None
                    strValue = enteredValue
                strValue = strValue.strip(string.whitespace+'\\')
                if strValue.startswith(self.sliderOpenString) and strValue.endswith(self.sliderCloseString):
                    continue
                # Parse the calltip info and build the appropriate slider
                argtype, argname, guitype, defaultValue, other = self.ParseCalltipArgInfo(info, strValue=strValue)
                if argtype is None or argname is None or guitype is None or argtype not in ('int', 'float', 'bool', 'string'):
                    continue
                if enteredName is not None:
                    if argname.startswith('"') and argname.endswith('"'):
                        argname = '"%s"' % enteredName.strip('"')
                    else:
                        argname = enteredName
                boolException = False
                if guitype == 'slider':
                    # Create a numerical slider
                    if not self.options['autoslidermakeintfloat']:
                        continue
                    minValue, maxValue, nDecimal, mod = other
                    try:
                        value = float(strValue)
                    except ValueError:
                        boolException = True
                        value = None
                    if value is None:
                        value = minValue
                    if value < minValue:
                        minValue = value
                    if value > maxValue:
                        maxValue = value
                    if separator is None:
                        separator = self.addAvsSliderSeparatorNew(script, label=filterName, menu=menuGeneral, row=row, sizer=script.sliderSizerNew)
                        row += 1
                    if boolException:
                        self.addAvsGenericArg(script, argname, strValue, row, separator, filterName, argIndex)
                    else:
                        self.addAvsSliderNew(script, argname, value, minValue, maxValue, defaultValue, nDecimal, mod, row, sizer=script.sliderSizerNew, separator=separator, filterName=filterName, argIndex=argIndex)
                    row += 1
                elif guitype == 'color':
                    # Create a color picker button
                    if not self.options['autoslidermakecolor']:
                        continue
                    if strValue.startswith('$'):
                        try:
                            value = strValue.split('$', 1)[1]
                            int(value, 16)
                        except ValueError:
                            boolException = True
                    else:
                        try:
                            value = '%X' % int(strValue)
                            if len(value) <= 6:
                                value = value.rjust(6, '0')
                            else:
                                boolException = True
                        except ValueError:
                            boolException = True
                    if separator is None:
                        separator = self.addAvsSliderSeparatorNew(script, label=filterName, menu=menuGeneral, row=row, sizer=script.sliderSizerNew)
                        row += 1
                    if boolException:
                        self.addAvsGenericArg(script, argname, strValue, row, separator, filterName, argIndex)
                    else:
                        self.addAvsColorPicker(script, argname, value, defaultValue, row, separator, filterName, argIndex)
                    row += 1
                elif guitype == 'boolradio':
                    # Create a true/false radio box
                    if not self.options['autoslidermakebool']:
                        continue
                    if strValue.lower() in ('true', 'false'):
                        if strValue.lower() == 'true':
                            value = True
                        else:
                            value = False
                    else:
                        boolException = True
                    if separator is None:
                        separator = self.addAvsSliderSeparatorNew(script, label=filterName, menu=menuGeneral, row=row, sizer=script.sliderSizerNew)
                        row += 1
                    if boolException:
                        self.addAvsGenericArg(script, argname, strValue, row, separator, filterName, argIndex)
                    else:
                        self.addAvsBooleanRadio(script, argname, value, defaultValue, row, separator, filterName, argIndex)
                    row += 1
                elif guitype in ('intlist', 'stringlist'):
                    if guitype == 'intlist':
                        if not self.options['autoslidermakeintlist']:
                            continue
                    else:
                        if not self.options['autoslidermakestringlist']:
                            continue
                        if not strValue.startswith('"') or not strValue.endswith('"'):
                            boolException = True
                        else:
                            strValue = strValue.strip('"')
                    choices = other
                    if separator is None:
                        separator = self.addAvsSliderSeparatorNew(script, label=filterName, menu=menuGeneral, row=row, sizer=script.sliderSizerNew)
                        row += 1
                    if boolException:
                        self.addAvsGenericArg(script, argname, strValue, row, separator, filterName, argIndex)
                    else:
                        self.addAvsChoice(script, argname, strValue, choices, defaultValue, guitype, row, separator, filterName, argIndex)
                    row += 1
                elif guitype == 'stringfilename':
                    if not self.options['autoslidermakestringfilename']:
                        continue
                    extList = other
                    if not strValue.startswith('"') or not strValue.endswith('"'):
                        boolException = True
                    else:
                        value = strValue.strip('"')
                    if separator is None:
                        separator = self.addAvsSliderSeparatorNew(script, label=filterName, menu=menuGeneral, row=row, sizer=script.sliderSizerNew)
                        row += 1
                    if boolException:
                        self.addAvsGenericArg(script, argname, strValue, row, separator, filterName, argIndex)
                    else:
                        self.addAvsFilenamePicker(script, argname, value, extList, row, separator, filterName, argIndex)
                    row += 1
                elif guitype in ('undocumented', 'error'):
                    # Undocumented argument
                    if not self.options['autoslidermakeunknown']:
                        continue
                    if separator is None:
                        separator = self.addAvsSliderSeparatorNew(script, label=filterName, menu=menuGeneral, row=row, sizer=script.sliderSizerNew)
                        row += 1
                    self.addAvsGenericArg(script, argname, strValue, row, separator, filterName, argIndex)
                    row += 1
        if row == 0:
            script.autoSliderInfo = []
        else:
            # Add a spacer
            height = 0
            if script.sliderTexts != []:
                height = 20
            script.sliderSizerNew.Add((5, height), (row, 7))
        if wx.VERSION > (2, 9):
            script.sliderSizerNew.Add((0, 0), (row, 3))
            if not script.sliderSizerNew.IsColGrowable(3):
                script.sliderSizerNew.AddGrowableCol(3)
        # Fold according to user set preference
        foldLevel = self.options['autosliderstartfold']
        if foldLevel == 0:
            # Fold all filters
            for item in script.sliderToggleLabels:
                self.ToggleSliderFold(item, fold=True, refresh=False)
            self.foldAllSliders = False
        elif foldLevel == 1:
            # Fold none, don't need to do anything
            self.foldAllSliders = True
        elif foldLevel == 2:
            # Fold only filters without numerical sliders
            boolAnyUnfolded = False
            for item in script.sliderToggleLabels:
                if not item.hasNumericalSlider:
                    self.ToggleSliderFold(item, fold=True, refresh=False)
                else:
                    boolAnyUnfolded = True
            if boolAnyUnfolded:
                self.foldAllSliders = True
        else:
            pass
        script.sliderWindow.Thaw()

    def ParseCalltipArgInfo(self, info, strValue=None):
        # TODO: handle repeating args [, ...]
        info = re.sub(r'\[.*\]', '', info)
        argtypename = info.split('=', 1)[0].strip()
        splitargtypename = argtypename.split()
        if len(splitargtypename) != 2:
            if len(splitargtypename) == 1:
                return (argtypename.lower(), None, None, None, None)
            else:
                return (None, None, None, None, None)
        argtype, argname = splitargtypename
        argtype = argtype.lower()
        if info.count('=') > 0:
            argInfo = info.split('=', 1)[1].strip()
            splitargtypename = argtypename.split()
            if argtype in ('float', 'int'):
                defaultValue = minValue = maxValue = nDecimal = mod = None
                strDefaultValue = strMinValue = strMaxValue = strStepSize = ''
                splitargInfo = argInfo.split('(',1)
                if len(splitargInfo) == 1:
                    strDefaultValue = argInfo
                    if strDefaultValue.startswith('$'):
                        try:
                            hexstring = strDefaultValue.split('$', 1)[1]
                            int(hexstring, 16)
                            return (argtype, argname, 'color', hexstring, None)
                        except ValueError:
                            return (argtype, argname, 'error', strDefaultValue, None)
                    else:
                        if argtype == 'int':
                            try:
                                defaultValue = int(strDefaultValue)
                                nDecimal = 0
                            except ValueError:
                                defaultValue = strDefaultValue
                        elif argtype == 'float':
                            try:
                                defaultValue = float(strDefaultValue)
                                splitStrvalue = strDefaultValue.split('.')
                                if len(splitStrvalue) == 2:
                                    nDecimal = len(splitStrvalue[1].strip())
                                else:
                                    nDecimal = 0
                            except ValueError:
                                defaultValue = strDefaultValue
                        return (argtype, argname, 'error', defaultValue, (minValue, maxValue, nDecimal, mod))
                elif len(splitargInfo) == 2:
                    strDefaultValue, rest = splitargInfo
                    strDefaultValue = strDefaultValue.strip()
                    boolValueError = False
                    try:
                        defaultValue = float(strDefaultValue)
                    except ValueError:
                        if strDefaultValue.startswith('$'):
                            try:
                                hexstring = strDefaultValue.split('$', 1)[1]
                                int(hexstring, 16)
                                return (argtype, argname, 'color', hexstring, None)
                            except ValueError:
                                return (argtype, argname, 'error', None, None)
                        else:
                            try:
                                defaultValue = float(strValue)
                                strDefaultValue = strValue
                            except:
                                defaultValue = None
                                #~ strDefaultValue = ''
                    splitrest = rest.split(')', 1)
                    if len(splitrest) == 2:
                        rangeInfo, extra = splitrest
                    else:
                        rangeInfo = rest
                        extra = ''
                    splitrangeInfo = rangeInfo.split(' to ')
                    if len(splitrangeInfo) == 2:
                        strMinValue, restRangeInfo = [s.strip() for s in splitrangeInfo]
                        try:
                            minValue = float(strMinValue)
                        except ValueError:
                            #~ return (argtype, argname, 'error', None, None)
                            #~ return (argtype, argname, 'error', strDefaultValue, (strMinValue, strMaxValue, 0, strStepSize))
                            boolValueError = True
                        splitrestRangeInfo = restRangeInfo.split(' by ')
                        if len(splitrestRangeInfo) == 2:
                            strMaxValue, strStepSize = [s.strip() for s in splitrestRangeInfo]
                        else:
                            strMaxValue = restRangeInfo.strip()
                            strStepSize = None
                        try:
                            maxValue = float(strMaxValue)
                        except ValueError:
                            #~ return (argtype, argname, 'error', None, None)
                            #~ return (argtype, argname, 'error', strDefaultValue, (strMinValue, strMaxValue, 0, strStepSize))
                            boolValueError = True
                        if argtype == 'int':
                            nDecimal = 0
                        if strStepSize is None and not boolValueError:
                            strStepSize = ''
                            # Get the step size from the strDefaultValue, strMinValue, strMaxValue
                            nDecimals = []
                            for eachValue in (strDefaultValue, strMinValue, strMaxValue):
                                splitStrvalue = eachValue.split('.')
                                if len(splitStrvalue) == 2:
                                    nDecimal = len(splitStrvalue[1].strip())
                                else:
                                    nDecimal = 0
                                nDecimals.append(nDecimal)
                            nDecimal = max(nDecimals)
                        elif not boolValueError:
                            try:
                                stepSize = float(strStepSize)
                                if stepSize > 1.0:
                                    nDecimal = 0
                                    mod = int(stepSize)
                                else:
                                    try:
                                        nDecimal = len(strStepSize.split('.')[1].strip())
                                    except IndexError:
                                        nDecimal = 0
                                        mod = None
                            except ValueError:
                                #~ return (argtype, argname, 'error', None, None)
                                #~ return (argtype, argname, 'error', strDefaultValue, (strMinValue, strMaxValue, 0, strStepSize))
                                boolValueError = True
                    else:
                        choices = rangeInfo.split('/')
                        if len(choices) > 1: # list of integers
                            try:
                                defaultValue = int(defaultValue)
                            except TypeError:
                                defaultValue = strDefaultValue
                            choices = [choice.strip() for choice in choices]
                            return (argtype, argname, 'intlist', defaultValue, choices)
                    if boolValueError:
                        return (argtype, argname, 'error', strDefaultValue, (strMinValue, strMaxValue, 0, strStepSize))
                errType, errMsg, sliderValues = self.ValidateAvsSliderInputs(strDefaultValue, strMinValue, strMaxValue, strStepSize)
                if errType is not None:
                    #~ return (argtype, argname, 'error', None, None)
                    return (argtype, argname, 'error', strDefaultValue, (strMinValue, strMaxValue, 0, strStepSize))
                if None in (defaultValue, minValue, maxValue, nDecimal):
                    return (argtype, argname, 'error', strDefaultValue, (strMinValue, strMaxValue, 0, strStepSize))
                if argtype == 'int':
                    defaultValue = int(defaultValue)
                    minValue = int(minValue)
                    maxValue = int(maxValue)
                return (argtype, argname, 'slider', defaultValue, (minValue, maxValue, nDecimal, mod))
            elif argtype == 'bool':
                defaultValue = argInfo.strip()
                if defaultValue.lower() in ('true', 'false'):
                    return (argtype, argname, 'boolradio', defaultValue, None)
                else:
                    return (argtype, argname, 'error', defaultValue, None)
            elif argtype == 'string':
                splitargInfo = argInfo.split('(',1)
                defaultValue = None
                if len(splitargInfo) == 2:
                    strDefaultValue, rest = splitargInfo
                    defaultValue = strDefaultValue.strip()
                    if defaultValue:
                        defaultValue = '"%s"' % defaultValue.strip('"')
                    choices = ['"%s"' % s.strip(' "') for s in rest.split(')')[0].split('/')]
                else:
                    return (argtype, argname, 'error', argInfo.strip(), None)
                #~ if argInfo.count('*.') > 0:
                if '/'.join(choices).count('*.') > 0:
                    # Filename selector
                    #~ extList = [s.strip(' "') for s in argInfo.split('(',1)[0].split('/') if s.strip(' "').startswith('*.')]
                    extList = [s.strip('"') for s in choices if s.strip('"').startswith('*.')]
                    return (argtype, argname, 'stringfilename', defaultValue, extList)
                else:
                    #~ # String list
                    #~ splitargInfo = argInfo.split('(',1)
                    #~ if len(splitargInfo) == 2:
                        #~ strDefaultValue, rest = splitargInfo
                        #~ defaultValue = strDefaultValue.strip(' "')
                        #~ choices = [s.strip(' "') for s in rest.split(')')[0].split('/')]
                    #~ else:
                        #~ return (argtype, argname, 'error', None, None)
                    return (argtype, argname, 'stringlist', defaultValue, choices)
            else:
                return (argtype, argname, 'clip', None, None)
        else:
            # No database info
            if argtype == 'bool':
                return (argtype, argname, 'boolradio', None, None)
            return (argtype, argname, 'undocumented', None, None)

    def createUserSliders(self, script, parseonly=False):
        sliderTexts = script.sliderTexts
        # Parse the slider texts
        labels = []
        argsList = []
        for text in sliderTexts:
            items = [s.strip() for s in text.lstrip(self.sliderOpenString).rstrip(self.sliderCloseString).split(',')]
            if len(items) != 4:
                if len(items) == 1:
                    splititem = items[0].split('=',1)
                    if len(splititem) == 2:
                        argsList.append([splititem[1].strip('"')])
                    else:
                        argsList.append([''])
                continue
            minValue = maxValue = value = None
            try:
                # Store the items
                label = items[0].strip(''' "' ''')#strip('"').strip("'")
                minValue = float(items[1])
                maxValue = float(items[2])
                value = float(items[3])
                if minValue >= maxValue:
                    #~ print>>sys.stderr, _('Error: invalid slider text:'), text
                    #~ continue
                    self.displaySliderWarning(script, text, items[1], _('Invalid slider text: min > max'))
                    return False
                if value < minValue or value > maxValue:
                    #~ print>>sys.stderr, _('Error: invalid slider text:'), text
                    #~ continue
                    self.displaySliderWarning(script, text, items[3], _('Invalid slider text: value not in bounds'))
                    return False
                # Get the number of decimals (to determine slider increments)
                nDecimal = 0
                items = [s.strip() for s in text.lstrip(self.sliderOpenString).rstrip(self.sliderCloseString).split(',')]
                for strnum in items[1:]:
                    strsplit = strnum.split('.')
                    if len(strsplit) == 2:
                        n = len(strsplit[1])
                    else:
                        n = 0
                    if n > nDecimal:
                        nDecimal = n
                # Get the modulo (slider step size)
                mod = None
                splitlabel = label.split('%', 1)
                if len(splitlabel) == 2:
                    try:
                        mod = int(splitlabel[1])
                    except ValueError:
                        #~ print>>sys.stderr, _('Error: invalid slider text:'), text
                        #~ continue
                        self.displaySliderWarning(script, text, splitlabel[1].strip(), _('Invalid slider text: bad modulo label'))
                        return False
                if mod is not None:
                    #~ tempMinValue = minValue + minValue % mod
                    #~ tempMaxValue = maxValue - maxValue % mod
                    if mod == 0:
                        mod = None
                    else:
                        invalidNumber = False
                        if (int(value) - int(minValue)) % mod != 0 or (int(maxValue) - int(minValue)) % mod != 0:
                            invalidNumber = True
                        if invalidNumber or mod > maxValue - minValue:
                            mod = None
                    if mod is not None:
                        nDecimal = 0
                        minValue = int(minValue) #tempMinValue
                        maxValue = int(maxValue) #tempMaxValue
                        value = int(value) #min(value + value % mod, maxValue)
                if label not in labels:
                    #~ self.addAvsSlider(script, label, minValue, maxValue, value, nDecimal, mod)
                    argsList.append((script, label, minValue, maxValue, value, nDecimal, mod))
                    labels.append(label)
                else:
                    #~ print>>sys.stderr, _('Error: User slider %(label)s already exists!') % locals()
                    self.displaySliderWarning(script, text, label, _('Invalid slider text: slider label already exists'))
                    return False
            except ValueError:
                #~ print>>sys.stderr, _('Error: invalid slider text:'), text
                #~ continue
                if minValue is None:
                    highlightText = items[1]
                elif maxValue is None:
                    highlightText = items[2]
                elif value is None:
                    highlightText = items[3]
                else:
                    highlightText = items[0]
                self.displaySliderWarning(script, text, highlightText, _('Invalid slider text: invalid number'))
                return False
        if parseonly:
            parsedInfo = [arg[1:] for arg in argsList]
            return zip(sliderTexts, parsedInfo)
        # Create the new sliders
        script.sliderSizer.Clear(deleteWindows=True)
        for row, args in enumerate(argsList):
            if len(args) == 1:
                self.addAvsSliderSeparator(script, label=args[0], row=row)
            else:
                args = args + (row,)
                self.addAvsSlider(*args)
        if wx.VERSION > (2, 9):
            script.sliderSizer.Add((0, 0), (len(argsList), 3))
            if not script.sliderSizer.IsColGrowable(3):
                script.sliderSizer.AddGrowableCol(3)
        return True

    def displaySliderWarning(self, script, sliderText, highlightText, msg):
        pos = script.FindText(0, script.GetTextLength(), sliderText)
        posA = script.FindText(pos, script.GetTextLength(), highlightText, stc.STC_FIND_WHOLEWORD)
        posB = posA + len(highlightText)
        script.SetSelection(posA, posB)
        script.SetFocus()
        wx.MessageBox(msg, _('Warning'))

    def addAvsSlider(self, script, labelTxt, minValue, maxValue, value, nDecimal, mod=None, row=None, sizer=None):
        if minValue is None or maxValue is None or value is None or nDecimal is None:
            return
        if sizer is None:
            sizer = script.sliderSizer
        parent = script.sliderWindow
        isRescaled = False
        if not mod:            
            if labelTxt[-1] == '+':
                minValue2 = 0
                mod = (maxValue - minValue) / 100.
                isRescaled = True
            elif labelTxt[-1] == '-':
                minValue2 = -100
                mod = (maxValue - minValue) / 200.
                isRescaled = True
        if isRescaled:
            def Rescale(val):
                return minValue2 + (val - minValue)/mod
        # Construct the format string based on nDecimal
        strTemplate = '%.'+str(nDecimal)+'f'
        strTemplate2 = '(%.'+str(nDecimal)+'f)'
        def OnScroll(event):
            value = slider.GetValue()
            valTxtCtrl.SetLabel(strTemplate % value)
            if isRescaled:
                valTxtCtrl2.SetLabel(strTemplate2 % Rescale(value))
        # Create the slider
        slider = wxp.Slider(parent, wx.ID_ANY,
            value, minValue, maxValue,
            size=(50,-1),
            style=wx.SL_BOTH,
            name=labelTxt,
            nDecimal=nDecimal,
            mod=mod,
            #~ onscroll= lambda event: valTxtCtrl.SetLabel(strTemplate % slider.GetValue())
            onscroll = OnScroll,
        )
        # Slider event binding
        slider.Bind(wx.EVT_LEFT_UP, self.OnLeftUpUserSlider)
        # Create the static text labels
        labelTxtCtrl = wx.StaticText(parent, wx.ID_ANY, labelTxt)
        minTxtCtrl = wx.StaticText(parent, wx.ID_ANY, strTemplate % minValue)
        maxTxtCtrl = wx.StaticText(parent, wx.ID_ANY, strTemplate % maxValue)
        valTxtCtrl = wx.StaticText(parent, wx.ID_ANY, strTemplate % value)
        valTxtCtrl.SetForegroundColour(wx.BLUE)
        valTxtCtrl.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        value_formatted = strTemplate % value
        valTxtCtrl.SetToolTip(wx.ToolTip(_('Reset to initial value: %(value_formatted)s') % locals()))
        if isRescaled:
            minTxtCtrl2 = wx.StaticText(parent, wx.ID_ANY, strTemplate2 % minValue2)
            minTxtCtrlSizer = wx.BoxSizer(wx.VERTICAL)
            minTxtCtrlSizer.Add(minTxtCtrl, 0, wx.ALIGN_CENTER)
            minTxtCtrlSizer.Add(minTxtCtrl2, 0, wx.ALIGN_CENTER)
            maxTxtCtrl2 = wx.StaticText(parent, wx.ID_ANY, strTemplate2 % Rescale(maxValue))
            maxTxtCtrlSizer = wx.BoxSizer(wx.VERTICAL)
            maxTxtCtrlSizer.Add(maxTxtCtrl, 0, wx.ALIGN_CENTER)
            maxTxtCtrlSizer.Add(maxTxtCtrl2, 0, wx.ALIGN_CENTER)
            value2_formatted = strTemplate2 % Rescale(value)
            valTxtCtrl2 = wx.StaticText(parent, wx.ID_ANY, value2_formatted)
            valTxtCtrlSizer = wx.BoxSizer(wx.VERTICAL)
            valTxtCtrlSizer.Add(valTxtCtrl, 0, wx.EXPAND)
            valTxtCtrlSizer.Add(valTxtCtrl2, 0, wx.EXPAND)
            valTxtCtrl2.SetForegroundColour(wx.RED)
            valTxtCtrl2.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            valTxtCtrl2.SetToolTip(wx.ToolTip(_('Reset to initial value: %(value2_formatted)s') % locals()))
        def OnTextLeftDown(event):
            valTxtCtrl.SetLabel(value_formatted)
            if isRescaled:
                valTxtCtrl2.SetLabel(value2_formatted)
            slider.SetValue(value)
            self.UserSliderVideoUpdate(slider)
        valTxtCtrl.Bind(wx.EVT_LEFT_DOWN, OnTextLeftDown)
        if isRescaled:
            valTxtCtrl2.Bind(wx.EVT_LEFT_DOWN, OnTextLeftDown)
        #~ leftCtrl = wxButtons.GenButton(parent, wx.ID_ANY, '<', size=(16,16))
        leftCtrl = wxButtons.GenBitmapButton(parent, wx.ID_ANY, self.bmpLeftTriangle, size=(16,16))
        leftCtrl.SetBezelWidth(1)
        leftCtrl.SetUseFocusIndicator(False)
        #~ leftCtrl.SetToolTip(wx.ToolTip('Decrement slider'))
        #~ def OnButtonLeftIncrement(event):
            #~ newvalue = slider.Decrement()
            #~ valTxtCtrl.SetLabel(strTemplate % newvalue)
            #~ self.UserSliderVideoUpdate(slider)
        #~ parent.Bind(wx.EVT_BUTTON, OnButtonLeftIncrement, leftCtrl)
        def OnLeftTimer(event):
            newvalue = slider.Decrement()
            valTxtCtrl.SetLabel(strTemplate % newvalue)
            if isRescaled:
                valTxtCtrl2.SetLabel(strTemplate2 % Rescale(newvalue))
            if leftCtrl.up:
                leftTimer.Stop()
                self.UserSliderVideoUpdate(slider)
                if leftCtrl.HasCapture():
                    leftCtrl.ReleaseMouse()
            event.Skip()
        leftTimer = wx.Timer(leftCtrl)
        leftCtrl.Bind(wx.EVT_TIMER, OnLeftTimer)
        def OnButtonDecLeftDown(event):
            newvalue = slider.Decrement()
            valTxtCtrl.SetLabel(strTemplate % newvalue)
            if isRescaled:
                valTxtCtrl2.SetLabel(strTemplate2 % Rescale(newvalue))
            self.fc = wx.FutureCall(300, leftTimer.Start, 100)
            #~ leftTimer.Start(100)
            event.Skip()
        def OnButtonDecLeftUp(event):
            if self.fc is not None:
                self.fc.Stop()
            leftTimer.Stop()
            self.UserSliderVideoUpdate(slider)
            event.Skip()
        leftCtrl.Bind(wx.EVT_LEFT_DOWN, OnButtonDecLeftDown)
        leftCtrl.Bind(wx.EVT_LEFT_UP, OnButtonDecLeftUp)
        #~ rightCtrl = wxButtons.GenButton(parent, wx.ID_ANY, '>', size=(16,16))
        rightCtrl = wxButtons.GenBitmapButton(parent, wx.ID_ANY, self.bmpRightTriangle, size=(16,16))
        rightCtrl.SetBezelWidth(1)
        rightCtrl.SetUseFocusIndicator(False)
        #~ def OnButtonRightIncrement(event):
            #~ newvalue = slider.Increment()
            #~ valTxtCtrl.SetLabel(strTemplate % newvalue)
            #~ self.UserSliderVideoUpdate(slider)
        #~ parent.Bind(wx.EVT_BUTTON, OnButtonRightIncrement, rightCtrl)
        def OnRightTimer(event):
            newvalue = slider.Increment()
            valTxtCtrl.SetLabel(strTemplate % newvalue)
            if isRescaled:
                valTxtCtrl2.SetLabel(strTemplate2 % Rescale(newvalue))
            if rightCtrl.up:
                rightTimer.Stop()
                self.UserSliderVideoUpdate(slider)
                if rightCtrl.HasCapture():
                    rightCtrl.ReleaseMouse()
            event.Skip()
        rightTimer = wx.Timer(rightCtrl)
        rightCtrl.Bind(wx.EVT_TIMER, OnRightTimer)
        def OnButtonIncLeftDown(event):
            newvalue = slider.Increment()
            valTxtCtrl.SetLabel(strTemplate % newvalue)
            if isRescaled:
                valTxtCtrl2.SetLabel(strTemplate2 % Rescale(newvalue))
            self.fc = wx.FutureCall(300, rightTimer.Start, 100)
            #~ rightTimer.Start(100)
            event.Skip()
        def OnButtonIncLeftUp(event):
            if self.fc is not None:
                self.fc.Stop()
            rightTimer.Stop()
            self.UserSliderVideoUpdate(slider)
            event.Skip()
        rightCtrl.Bind(wx.EVT_LEFT_DOWN, OnButtonIncLeftDown)
        rightCtrl.Bind(wx.EVT_LEFT_UP, OnButtonIncLeftUp)
        # Add the elements to the sliderSizer
        sizer.Add(labelTxtCtrl, (row,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        if isRescaled:
            sizer.Add(minTxtCtrlSizer, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        else:
            sizer.Add(minTxtCtrl, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        sizer.Add(leftCtrl, (row,2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        sizer.Add(slider, (row,3), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        sizer.Add(rightCtrl, (row,4), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        if isRescaled:
            sizer.Add(maxTxtCtrlSizer, (row,5), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
            sizer.Add(valTxtCtrlSizer, (row,6), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 0)
        else:
            sizer.Add(maxTxtCtrl, (row,5), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
            sizer.Add(valTxtCtrl, (row,6), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 0)
        #sizer.Add((10, -1), (row,7))

        #~ script.sliderSizer.Layout()
        #~ slider.Refresh()

    def addAvsSliderSeparator(self, script, label='', row=None, sizer=None):
        if sizer is None:
            sizer = script.sliderSizer
        parent = script.sliderWindow
        color1 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW)
        color2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DHILIGHT)
        # Add a separator
        tempsizer = wx.BoxSizer(wx.VERTICAL)
        if row == 0: border = 0
        else: border = 10
        if label == '':
            tempsizer.Add(wx.StaticLine(parent), 0, wx.EXPAND|wx.ALIGN_BOTTOM|wx.TOP, border)
        else:
            staticText = wx.StaticText(parent, wx.ID_ANY, label)
            font = staticText.GetFont()
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            staticText.SetFont(font)
            tempsizer.Add(staticText, 0, wx.ALIGN_BOTTOM|wx.TOP, border)
            tempsizer.Add(wx.StaticLine(parent), 0, wx.EXPAND|wx.ALIGN_BOTTOM)
        sizer.Add(tempsizer, (row,0), (1,7), wx.EXPAND)

    def addAvsSliderNew(self, script, labelTxt, value, minValue, maxValue, defaultValue, nDecimal, mod=None, row=None, sizer=None, separator=None, filterName=None, argIndex=None):
        if minValue is None or maxValue is None or value is None or nDecimal is None:
            return
        if sizer is None:
            sizer = script.sliderSizer
        parent = script.sliderWindow
        # Construct the format string based on nDecimal
        strTemplate = '%.'+str(nDecimal)+'f'
        # Create the slider
        slider = wxp.Slider(parent, wx.ID_ANY,
            value, minValue, maxValue,
            size=(50,-1),
            style=wx.SL_BOTH,
            name=labelTxt,
            nDecimal=nDecimal,
            mod=mod,
            onscroll= lambda event: valTxtCtrl.SetLabel(strTemplate % slider.GetValue())
        )
        slider.filterName = filterName
        slider.argName = labelTxt
        slider.script = script
        slider.argIndex = argIndex

        # Slider event binding
        def UserSliderVideoUpdateNew(slider):
            # Create the new arg text
            newVal = slider.GetValueAsString()
            self.SetNewAvsValue(slider, newVal)

        #~ slider.Bind(wx.EVT_LEFT_UP, self.OnLeftUpUserSlider)
        def OnLeftUpUserSlider(event):
            UserSliderVideoUpdateNew(slider)
            event.Skip()
        slider.Bind(wx.EVT_LEFT_UP, OnLeftUpUserSlider)

        # Create the static text labels
        labelTxtCtrl = self.MakeArgNameStaticText(parent, labelTxt, filterName, script, argIndex)
        minTxtCtrl = wx.StaticText(parent, wx.ID_ANY, strTemplate % minValue)
        maxTxtCtrl = wx.StaticText(parent, wx.ID_ANY, strTemplate % maxValue)
        valTxtCtrl = wx.StaticText(parent, wx.ID_ANY, strTemplate % value)
        valTxtCtrl.SetForegroundColour(wx.BLUE)
        valTxtCtrl.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        value_formatted = strTemplate % defaultValue
        valTxtCtrl.SetToolTip(wx.ToolTip(_('Reset to default value: %(value_formatted)s') % locals()))
        def OnTextLeftDown(event):
            valTxtCtrl.SetLabel(value_formatted)
            slider.SetValue(defaultValue)
            UserSliderVideoUpdateNew(slider)
        valTxtCtrl.Bind(wx.EVT_LEFT_DOWN, OnTextLeftDown)
        leftCtrl = wxButtons.GenBitmapButton(parent, wx.ID_ANY, self.bmpLeftTriangle, size=(16,16))
        leftCtrl.SetBezelWidth(1)
        leftCtrl.SetUseFocusIndicator(False)
        def OnLeftTimer(event):
            newvalue = slider.Decrement()
            valTxtCtrl.SetLabel(strTemplate % newvalue)
            if leftCtrl.up:
                leftTimer.Stop()
                UserSliderVideoUpdateNew(slider)
                if leftCtrl.HasCapture():
                    leftCtrl.ReleaseMouse()
            event.Skip()
        leftTimer = wx.Timer(leftCtrl)
        leftCtrl.Bind(wx.EVT_TIMER, OnLeftTimer)
        def OnButtonDecLeftDown(event):
            newvalue = slider.Decrement()
            valTxtCtrl.SetLabel(strTemplate % newvalue)
            self.fc = wx.FutureCall(300, leftTimer.Start, 100)
            event.Skip()
        def OnButtonDecLeftUp(event):
            if self.fc is not None:
                self.fc.Stop()
            leftTimer.Stop()
            UserSliderVideoUpdateNew(slider)
            event.Skip()
        leftCtrl.Bind(wx.EVT_LEFT_DOWN, OnButtonDecLeftDown)
        leftCtrl.Bind(wx.EVT_LEFT_UP, OnButtonDecLeftUp)
        rightCtrl = wxButtons.GenBitmapButton(parent, wx.ID_ANY, self.bmpRightTriangle, size=(16,16))
        rightCtrl.SetBezelWidth(1)
        rightCtrl.SetUseFocusIndicator(False)
        def OnRightTimer(event):
            newvalue = slider.Increment()
            valTxtCtrl.SetLabel(strTemplate % newvalue)
            if rightCtrl.up:
                rightTimer.Stop()
                UserSliderVideoUpdateNew(slider)
                if rightCtrl.HasCapture():
                    rightCtrl.ReleaseMouse()
            event.Skip()
        rightTimer = wx.Timer(rightCtrl)
        rightCtrl.Bind(wx.EVT_TIMER, OnRightTimer)
        def OnButtonIncLeftDown(event):
            newvalue = slider.Increment()
            valTxtCtrl.SetLabel(strTemplate % newvalue)
            self.fc = wx.FutureCall(300, rightTimer.Start, 100)
            event.Skip()
        def OnButtonIncLeftUp(event):
            if self.fc is not None:
                self.fc.Stop()
            rightTimer.Stop()
            UserSliderVideoUpdateNew(slider)
            event.Skip()
        rightCtrl.Bind(wx.EVT_LEFT_DOWN, OnButtonIncLeftDown)
        rightCtrl.Bind(wx.EVT_LEFT_UP, OnButtonIncLeftUp)
        # Add the elements to the sliderSizer
        sizer.Add(labelTxtCtrl, (row,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 10)
        sizer.Add(minTxtCtrl, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        sizer.Add(leftCtrl, (row,2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        sizer.Add(slider, (row,3), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        sizer.Add(rightCtrl, (row,4), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(maxTxtCtrl, (row,5), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        sizer.Add(valTxtCtrl, (row,6), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 0)
        #sizer.Add((10, -1), (row,7))
        separator.controls += [labelTxtCtrl, minTxtCtrl, leftCtrl, slider, rightCtrl, maxTxtCtrl, valTxtCtrl]
        separator.hasNumericalSlider = True

    def ValidateAvsSliderInputs(self, strDef, strMin, strMax, strMod):
        # Returns (error type, error message)
        # Error types: None: good / 0: bad default / 1: bad min / 2: bad max / 3: bad mod / -1: non-number
        errortype = errormessage = None
        if strDef.startswith('$'):
            try:
                hexstring = strDef.split('$', 1)[1]
                int(hexstring, 16)
                return (None, None, [hexstring])
            except ValueError:
                return (0, _('Invalid hexadecimal color!'), None)
        if strMin and not strMax:
            return (2, _('Must specify a max value!'), None)
        if strMax and not strMin:
            return (1, _('Must specify a min value!'), None)
        try:
            minValue = float(strMin)
        except ValueError:
            #~ return (1, _('Min value must be a number!'), None)
            errortype = 1
            errormessage = _('Min value must be a number!')
        try:
            maxValue = float(strMax)
        except ValueError:
            #~ return (2, _('Max value must be a number!'), None)
            errortype = 2
            errormessage = _('Max value must be a number!')
        if not strDef:
            defValue = minValue
        else:
            try:
                defValue = float(strDef)
            except ValueError:
                #~ return (0, _('Default value must be a number!'), None)
                errortype = 0
                errormessage = _('Default value must be a number!')
        if not strMod:
            modValue = None
        else:
            try:
                modValue = int(float(strMod))
            except ValueError:
                #~ return (3, _('Step size must be an number!'), None)
                errortype = 3
                errormessage = _('Step size value must be a number!')
        if errormessage is not None:
            return (-1, errormessage, (strDef, strMin, strMax, strMod))
        if minValue >= maxValue:
            return (1, _('The min value must be less than the max!'), None)
        if defValue < minValue or defValue > maxValue:
            return (0,  _('The initial value must be between the min and the max!'), None)
        if modValue is not None and modValue >= 1:
            mod = modValue
            if int(minValue) % mod != 0:
                return (1, _('The min value must be a multiple of %(mod)s!') % locals(), None)
            if int(maxValue) % mod != 0:
                return (2, _('The max value must be a multiple of %(mod)s!') % locals(), None)
            if int(defValue) % mod != 0:
                return (0, _('The initial value must be a multiple of %(mod)s!') % locals(), None)
            if mod > (maxValue - minValue):
                return (0, _('The difference between the min and max must be greater than %(mod)s!') % locals(), None)
        return (None, None, (defValue, minValue, maxValue, modValue))

    def addAvsBooleanRadio(self, script, argname, value, defaultValue, row, separator, filterName, argIndex):
        parent = script.sliderWindow
        sizer = script.sliderSizerNew
        # Create window elements
        #~ labelTxtCtrl = wx.StaticText(parent, wx.ID_ANY, argname)
        labelTxtCtrl = self.MakeArgNameStaticText(parent, argname, filterName, script, argIndex)
        radioButtonTrue = wx.RadioButton(parent, wx.ID_ANY, 'true', style=wx.RB_GROUP, size=(-1,20))
        radioButtonFalse = wx.RadioButton(parent, wx.ID_ANY, 'false', size=(-1,20))
        if value:
            radioButtonTrue.SetValue(True)
        else:
            radioButtonFalse.SetValue(True)
        def OnRadioButton(event):
            button = event.GetEventObject()
            if button == radioButtonTrue:
                newVal = 'true'
            else:
                newVal = 'false'
            self.SetNewAvsValue(button, newVal)
            event.Skip()
        for ctrl in (radioButtonTrue, radioButtonFalse):
            ctrl.filterName = filterName
            ctrl.argName = argname
            ctrl.script = script
            ctrl.argIndex = argIndex
            ctrl.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        if defaultValue is not None:
            if defaultValue.lower() == 'true':
                font = radioButtonTrue.GetFont()
                font.SetUnderlined(True)
                radioButtonTrue.SetFont(font)
            else:
                font = radioButtonFalse.GetFont()
                font.SetUnderlined(True)
                radioButtonFalse.SetFont(font)
        radioSizer = wx.BoxSizer(wx.HORIZONTAL)
        #~ radioSizer.Add((20,-1))
        radioSizer.Add(radioButtonTrue, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5)
        radioSizer.Add(radioButtonFalse, 0, wx.ALL, 5)
        # Add the elements to the slider sizer
        sizer.Add(labelTxtCtrl, (row,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 10)
        #~ sizer.Add(radioButtonTrue, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        #~ sizer.Add(radioButtonFalse, (row,2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        sizer.Add(radioSizer, (row, 1), (1,6), wx.ALIGN_CENTER_VERTICAL)
        #sizer.Add((10, -1), (row,7))
        separator.controls += [labelTxtCtrl, radioSizer]
        #~ separator.controls += [labelTxtCtrl]

    def addAvsColorPicker(self, script, argname, value, defaultValue, row, separator, filterName, argIndex):
        parent = script.sliderWindow
        sizer = script.sliderSizerNew
        # Create window elements
        #~ labelTxtCtrl = wx.StaticText(parent, wx.ID_ANY, argname)
        labelTxtCtrl = self.MakeArgNameStaticText(parent, argname, filterName, script, argIndex)
        try:
            r = int(defaultValue[0:2],16)
            g = int(defaultValue[2:4],16)
            b = int(defaultValue[4:6],16)
            defaultColor = wx.Colour(r, g, b)
        except:
            defaultColor = wx.Colour()
        try:
            r = int(value[0:2],16)
            g = int(value[2:4],16)
            b = int(value[4:6],16)
        except:
            r=g=b=0
        colorButton = wxp.ColourSelect(parent, wx.ID_ANY, colour=wx.Colour(r,g,b), size=(50,23), colour_data=self.colour_data)
        def OnSelectColour(event):
            self.options['colourdata'] = self.colour_data.ToString()
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
            strColor = '$%02x%02x%02x' % colorButton.GetColour().Get()
            self.SetNewAvsValue(colorButton, strColor.upper())
        colorButton.Bind(colourselect.EVT_COLOURSELECT, OnSelectColour)
        def OnRightUpButtonColor(event):
            colorButton.SetColour(defaultColor)
            self.SetNewAvsValue(colorButton, '$%s' % defaultValue.upper())
        colorButton.Bind(wx.EVT_RIGHT_UP, OnRightUpButtonColor)
        colorButton.SetToolTip(wx.ToolTip(_('Left-click to select a color, right click to reset to default')+' ($%s)' % defaultValue))

        colorButton.filterName = filterName
        colorButton.argName = argname
        colorButton.script = script
        colorButton.argIndex = argIndex

        #TODO: FIX
        colorSizer = wx.BoxSizer(wx.HORIZONTAL)
        colorSizer.Add(colorButton, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5)
        # Add the elements to the slider sizer
        sizer.Add(labelTxtCtrl, (row,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 10)
        #~ sizer.Add(radioButtonTrue, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        #~ sizer.Add(radioButtonFalse, (row,2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        sizer.Add(colorSizer, (row, 1), (1,6), wx.ALIGN_CENTER_VERTICAL)
        #sizer.Add((10, -1), (row,7))
        separator.controls += [labelTxtCtrl, colorSizer]
        #~ separator.controls += [labelTxtCtrl]

    def addAvsChoice(self, script, argname, value, choices, defaultValue, guitype, row, separator, filterName, argIndex):
        parent = script.sliderWindow
        sizer = script.sliderSizerNew
        # Create window elements
        labelTxtCtrl = self.MakeArgNameStaticText(parent, argname, filterName, script, argIndex)
        if guitype == 'stringlist':
            choices2 = [s.strip('"') for s in choices]
            try:
                #~ index = choices.index(defaultValue)
                index = [s.lower() for s in choices2].index(defaultValue.strip('"').lower())
                choices2[index] = choices2[index] + ' *'
            except ValueError:
                pass
            choiceBox = wx.Choice(parent, wx.ID_ANY, choices=choices2)
            try:
                index = [s.strip('"').lower() for s in choices].index(value.strip('"').lower())
                choiceBox.SetSelection(index)
            except ValueError:
                pass
            def OnChoice(event):
                newVal = '"%s"' % choices[choiceBox.GetCurrentSelection()].strip('"')
                self.SetNewAvsValue(choiceBox, newVal)
                event.Skip()
        else:
            try:
                #~ index = choices.index(defaultValue)
                index = choices.index(str(defaultValue))
                choices2 = [str(i) for i in choices]
                choices2[index] = choices2[index] + ' *'
            except ValueError:
                choices2 = choices
            choiceBox = wx.Choice(parent, wx.ID_ANY, choices=choices2)
            try:
                choiceBox.SetSelection(choices.index(value))
            except ValueError:
                pass
            def OnChoice(event):
                newVal = choices[choiceBox.GetCurrentSelection()]
                self.SetNewAvsValue(choiceBox, newVal)
                event.Skip()
        choiceBox.filterName = filterName
        choiceBox.argName = argname
        choiceBox.script = script
        choiceBox.argIndex = argIndex
        choiceBox.Bind(wx.EVT_CHOICE, OnChoice)
        # Add the elements to the slider sizer
        sizer.Add(labelTxtCtrl, (row,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 10)
        #~ sizer.Add(radioButtonTrue, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        #~ sizer.Add(radioButtonFalse, (row,2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        sizer.Add(choiceBox, (row, 1), (1,6), wx.ALIGN_CENTER_VERTICAL)
        #sizer.Add((10, -1), (row,7))
        separator.controls += [labelTxtCtrl, choiceBox]

    def addAvsFilenamePicker(self, script, argname, value, extList, row, separator, filterName, argIndex):
        parent = script.sliderWindow
        sizer = script.sliderSizerNew
        # Create window elements
        #~ labelTxtCtrl = wx.StaticText(parent, wx.ID_ANY, argname)
        extList = [s.strip() for s in extList if not s.strip().startswith('*.*')]
        labelTxtCtrl = self.MakeArgNameStaticText(parent, argname, filterName, script, argIndex)
        textCtrl = wx.TextCtrl(parent, wx.ID_ANY, value, style=wx.TE_PROCESS_ENTER)
        browseButton = wx.Button(parent, wx.ID_ANY, '...', size=(20, -1))
        def OnTextChange(event):
            script.oldAutoSliderInfo = None
            event.Skip()
        def OnTextEnter(event):
            newVal = '"%s"' % textCtrl.GetValue().strip(' "')
            self.SetNewAvsValue(textCtrl, newVal)
            event.Skip()
        def OnBrowseButton(event):
            dirname = os.path.dirname(textCtrl.GetValue())
            if os.path.isdir(dirname):
                initial_dir = dirname
            else:
                initial_dir = self.GetProposedPath(only='dir')
            extlist = self.options['templates'].keys()
            extlist.sort()
            extlist2 = [s for s in extlist if not s.startswith('avs')]
            extlist1 = ', '.join(extlist2)
            extlist2 = ';*.'.join(extlist2)
            s1 = '%s|%s' % (', '.join(extList), ';'.join(extList))
            s2 = _('Source files') + ' (%(extlist1)s)|*.%(extlist2)s' % locals() #'%s|%s' % (', '.join(extList), ';'.join(extList))
            s3 = _('All files') + ' (*.*)|*.*'
            if extList:
                filefilter = '%s|%s|%s' % (s1, s2, s3) #_('AviSynth script (avs, avsi)|*.avs;*.avsi|Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*') %  locals()
            else:
                filefilter = s3
            dlg = wx.FileDialog(self,_('Select a file'), initial_dir, '', filefilter, wx.OPEN)
            ID = dlg.ShowModal()
            if ID == wx.ID_OK:
                filename = dlg.GetPath()
                newVal = '"%s"' % filename
                self.SetNewAvsValue(browseButton, newVal)
                textCtrl.SetValue(filename)
                dirname = os.path.dirname(filename)
                if os.path.isdir(dirname):
                    self.options['recentdir'] = dirname
            dlg.Destroy()
            event.Skip()
        for ctrl in (textCtrl, browseButton):
            ctrl.filterName = filterName
            ctrl.argName = argname
            ctrl.script = script
            ctrl.argIndex = argIndex
        self.Bind(wx.EVT_BUTTON, OnBrowseButton, browseButton)
        textCtrl.Bind(wx.EVT_TEXT_ENTER, OnTextEnter)
        textCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        browseSizer = wx.BoxSizer(wx.HORIZONTAL)
        #~ radioSizer.Add((20,-1))
        browseSizer.Add(textCtrl, 1, wx.EXPAND|wx.RIGHT, 2)#|wx.TOP|wx.BOTTOM|wx.RIGHT, 5)
        browseSizer.Add(browseButton, 0)#, wx.ALL, 5)
        # Add the elements to the slider sizer
        sizer.Add(labelTxtCtrl, (row,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 10)
        #~ sizer.Add(radioButtonTrue, (row,1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        #~ sizer.Add(radioButtonFalse, (row,2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        #~ sizer.Add(textCtrl, (row, 3), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        #~ sizer.Add(browseButton, (row, 4), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(browseSizer, (row,1), (1,6), wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        #sizer.Add((10, -1), (row,7))
        #~ separator.controls += [labelTxtCtrl, textCtrl, browseButton]
        separator.controls += [labelTxtCtrl, browseSizer]
        #~ separator.controls += [labelTxtCtrl]

    def addAvsGenericArg(self, script, argname, strValue, row, separator, filterName, argIndex):
        parent = script.sliderWindow
        sizer = script.sliderSizerNew
        # Create window elements
        labelTxtCtrl = self.MakeArgNameStaticText(parent, argname, filterName, script, argIndex)

        textCtrl = wx.TextCtrl(parent, wx.ID_ANY, strValue, style=wx.TE_PROCESS_ENTER)
        def OnTextChange(event):
            self.SetNewAvsValue(textCtrl, textCtrl.GetValue(), refreshvideo=False)
            #~ script.oldAutoSliderInfo = None
            event.Skip()
        def OnTextEnter(event):
            self.SetNewAvsValue(textCtrl, textCtrl.GetValue())
            #~ event.Skip()
        textCtrl.Bind(wx.EVT_TEXT, OnTextChange)
        textCtrl.Bind(wx.EVT_TEXT_ENTER, OnTextEnter)
        textCtrl.filterName = filterName
        textCtrl.argName = argname
        textCtrl.script = script
        textCtrl.argIndex = argIndex

        #~ tempSizer = wx.BoxSizer()
        #~ tempSizer.Add(labelTxtCtrl, 0, wx.TOP|wx.BOTTOM, 4)
        #~ sizer.Add(tempSizer, (row,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 10)
        #~ sizer.Add((10, -1), (row,7))
        #~ separator.controls += [tempSizer]
        sizer.Add(labelTxtCtrl, (row,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT, 10)
        sizer.Add(textCtrl, (row,1), (1,6), wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        #sizer.Add((10, -1), (row,7))
        separator.controls += [labelTxtCtrl, textCtrl]

    def MakeArgNameStaticText(self, parent, labelTxt, filterName, script, argIndex, size=wx.DefaultSize):
        labelTxtCtrl = wx.StaticText(parent, wx.ID_ANY, labelTxt, size=size)
        labelTxtCtrl.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
        labelTxtCtrl.filterName = filterName
        labelTxtCtrl.argName = labelTxt
        labelTxtCtrl.script = script
        labelTxtCtrl.argIndex = argIndex
        def OnLeftDown(event):
            selText, selA, selB = self.GetArgTextAndPos(labelTxtCtrl)
            if selText.startswith('"') and selText.endswith('"'):
                selA += 1
                selB -= 1
            script.SetSelection(selA, selB)
            script.EnsureCaretVisible()
            script.SetFocus()
            event.Skip()
        labelTxtCtrl.Bind(wx.EVT_LEFT_DOWN, OnLeftDown)
        return labelTxtCtrl

    def SetNewAvsValue(self, control, newValue, refreshvideo=True):
        script = control.script
        argText, posA, posB = self.GetArgTextAndPos(control)
        if argText is None:
            return
        # Create the new arg text
        if refreshvideo:
            keep_env = not self.ScriptChanged(script)
        script.SetTargetStart(posA)
        script.SetTargetEnd(posB)
        script.ReplaceTarget(newValue)
        if refreshvideo:
            self.refreshAVI = True
            self.ShowVideoFrame(userScrolling=True, keep_env=keep_env)

    def GetArgTextAndPos(self, slider):
        # Find the filter in the text
        script = slider.script
        splitFilterName = slider.filterName.split('(', 1)
        if len(splitFilterName) == 2:
            filterName = splitFilterName[0].strip()
            iFilter = splitFilterName[1].split(')')[0]
            try:
                iFilter = int(iFilter)
            except ValueError:
                return (None, None, None)
        else:
            filterName = slider.filterName
            iFilter = 1
        startpos = 0
        for i in range(iFilter):
            startpos = script.FindText(startpos, script.GetTextLength(), filterName, stc.STC_FIND_WHOLEWORD)
            if startpos == -1:
                return (None, None, None)
            startpos += 1
            while script.GetStyleAt(startpos) not in script.keywordStyleList:
                startpos = script.FindText(startpos, script.GetTextLength(), filterName, stc.STC_FIND_WHOLEWORD)
                if startpos == -1:
                    return (None, None, None)
                startpos += 1
        # Find the argument in the text
        endwordpos = script.WordEndPosition(startpos, 1)
        while chr(script.GetCharAt(endwordpos)) in (' ', '\t'):
            endwordpos += 1
        posEnd = script.BraceMatch(endwordpos)
        if posEnd == -1:
            return (None, None, None)
        argIndex = slider.argIndex
        for i in xrange(argIndex):
            endwordpos = script.GetNextValidCommaPos(endwordpos+1)
            if endwordpos is None:
                return (None, None, None)
        posA = endwordpos+1
        posB = script.GetNextValidCommaPos(posA)
        if posB is None or posB > posEnd:
            posB = posEnd
        text = script.GetTextRange(posA, posB)
        posEqualSign = script.GetNextValidCommaPos(posA, checkChar='=')
        if posEqualSign is not None and posEqualSign < posB:
            posA = posEqualSign+1
        pos = posA
        while pos < posB:
            c = unichr(script.GetCharAt(pos))
            if c.strip() and c != '\\':
                posA = pos
                break
            pos += 1
        pos = posB
        while pos > posA:
            c = unichr(script.GetCharAt(pos-1))
            if c.strip() and c != '\\':
                posB = pos
                break
            pos -= 1
        return script.GetTextRange(posA, posB), posA, posB

    def addAvsSliderSeparatorNew(self, script, label='', menu=None, row=None, sizer=None):
        if sizer is None:
            sizer = script.sliderSizer
        parent = script.sliderWindow
        color1 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW)
        color2 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DHILIGHT)
        # Add a separator
        tempsizer = wx.BoxSizer(wx.VERTICAL)
        if row == 0: border = 0 if wx.VERSION < (2, 9) else 5
        else: border = 10
        if label == '':
            tempsizer.Add(wx.StaticLine(parent), 0, wx.EXPAND|wx.ALIGN_BOTTOM|wx.TOP, border)
        else:
            staticText = wx.StaticText(parent, wx.ID_ANY, ' - '+label)
            staticText.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            def OnLeftDown(event):
                separator = event.GetEventObject()
                self.ToggleSliderFold(separator, separator.IsControlsVisible)
                event.Skip()
            staticText.Bind(wx.EVT_LEFT_DOWN, OnLeftDown)

            if menu is not None:
                staticText.contextMenu = menu
                staticText.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

            font = staticText.GetFont()
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            staticText.SetFont(font)
            tempsizer.Add(staticText, 0, wx.ALIGN_BOTTOM|wx.TOP, border)
            tempsizer.Add(wx.StaticLine(parent), 0, wx.EXPAND|wx.ALIGN_BOTTOM)
        sizer.Add(tempsizer, (row,0), (1,7), wx.EXPAND)
        staticText.controls = []
        staticText.hasNumericalSlider = False
        staticText.IsControlsVisible = True
        script.sliderToggleLabels.append(staticText)
        return staticText

    def ToggleSliderFold(self, separator, fold=True, refresh=True):
        sizer = self.currentScript.sliderSizerNew
        parent = separator.GetParent()
        parent.Freeze()
        if fold:
            for item in separator.controls:
                sizer.Hide(item)
            separator.SetLabel('+ '+separator.GetLabel().strip(' -+'))
            separator.IsControlsVisible = False
        else:
            for item in separator.controls:
                sizer.Show(item)
            separator.SetLabel(' - '+separator.GetLabel().strip(' -+'))
            separator.IsControlsVisible = True
        if refresh:
            sizer.Layout()
            parent.FitInside()
            parent.Refresh()
            if separator.IsControlsVisible and separator.controls:
                lastitem = separator.controls[-1]
                if lastitem.GetPosition()[1]+lastitem.GetSize()[1] > parent.GetSize()[1]:
                    xscrollpixels, yscrollpixels = parent.GetScrollPixelsPerUnit()
                    pos = parent.CalcUnscrolledPosition(separator.GetPosition())
                    parent.Scroll(-1, (pos[1]-10)/yscrollpixels)
        parent.Thaw()

    def createToggleTagCheckboxes(self, script):
        toggleTags = script.toggleTags
        # First remove all old checkboxes
        script.toggleTagSizer.Clear(deleteWindows=True)
        labels = []
        # Then add the new checkboxes
        for tag in toggleTags:
            label, boolCheck = tag
            if label not in labels:
                checkbox = wx.CheckBox(script.sliderWindow, wx.ID_ANY, _('Toggle "%(label)s" section') % locals(), name=label)
                checkbox.SetValue(boolCheck)
                checkbox.Bind(wx.EVT_CHECKBOX, self.OnToggleTagChecked)
                script.toggleTagSizer.Add(checkbox, 0, wx.BOTTOM, 15)
                labels.append(label)
    
    def SetScriptTabname(self, name, script=None, index=None):
        if index is not None:
            self.scriptNotebook.SetPageText(index, name)
            if index == self.scriptNotebook.GetSelection():
                self.UpdateProgramTitle()
            return
        if script == self.scriptNotebook.GetCurrentPage():
            index = self.scriptNotebook.GetSelection()
            self.scriptNotebook.SetPageText(index, name)
            self.UpdateProgramTitle()
        else:
            for index in xrange(self.scriptNotebook.GetPageCount()):
                if script == self.scriptNotebook.GetPage(index):
                    self.scriptNotebook.SetPageText(index, name)
                    return
    
    def UpdateScriptTabname(self, script=None, index=None):
        if index is not None:
            self.scriptNotebook.UpdatePageText(index)
            if index == self.scriptNotebook.GetSelection():
                self.UpdateProgramTitle()
            return
        if script == self.scriptNotebook.GetCurrentPage():
            index = self.scriptNotebook.GetSelection()
            self.scriptNotebook.UpdatePageText(index)
            self.UpdateProgramTitle()
        else:
            for index in xrange(self.scriptNotebook.GetPageCount()):
                if script == self.scriptNotebook.GetPage(index):
                    self.scriptNotebook.UpdatePageText(index)
                    return
    
    def UpdateProgramTitle(self, title=None):
        if title is None:
            title = self.GetProgramTitle()
        self.SetTitle('%s - %s' % (title, self.name))
        if self.separatevideowindow:
            self.videoDialog.SetTitle('%s - [%s]' % (title, self.name))
    
    def GetProgramTitle(self, allowfull=True):
        script = self.currentScript
        filename = script.filename
        #~ if allowfull and self.options['showfullname'] and filename:
        if allowfull and filename:
            tabname = filename
            if script.group is not None:
                tabname = u'[{0}] {1}'.format(script.group, tabname)
            if script.GetModify():
                tabname = '* ' + tabname
        else:
            index = self.scriptNotebook.GetSelection()
            tabname = self.scriptNotebook.GetPageText(index, full=True)
        return tabname
    
    def UpdateTabImages(self):
        if self.options['usetabimages']:
            if self.options['multilinetab']:
                rows = self.scriptNotebook.GetRowCount()
            if self.FindFocus() == self.videoWindow:
                for i in xrange(min(self.scriptNotebook.GetPageCount(), 10)):
                    self.scriptNotebook.SetPageImage(i, i)
            else:
                #~ il = self.scriptNotebook.GetImageList()
                for i in xrange(self.scriptNotebook.GetPageCount()):
                    self.scriptNotebook.SetPageImage(i, -1)
            if self.options['multilinetab']:
                if rows != self.scriptNotebook.GetRowCount():
                    w, h = self.scriptNotebook.GetSize()
                    self.scriptNotebook.SetSize((w, h-1))
                    self.scriptNotebook.SetSize((w, h))

    def ShowWarningOnBadNaming(self, baddllnameList):
        wx.Bell()
        dlg = wx.Dialog(self, wx.ID_ANY, _('Warning'))
        bmp = wx.StaticBitmap(dlg, wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_WARNING))
        baddllnameList.append('\n')
        message = wx.StaticText(dlg, wx.ID_ANY, '.{0}\n'.format('dll' if os.name == 'nt' else 'so').join(baddllnameList) +\
                                                _('Above plugin names contain undesirable symbols.\n'
                                                  'Rename them to only use alphanumeric or underscores,\n'
                                                  'or make sure to use them in short name style only.'))
        msgsizer = wx.BoxSizer(wx.HORIZONTAL)
        msgsizer.Add(bmp)
        msgsizer.Add(message, 0, wx.LEFT, 10)
        
        checkbox = wx.CheckBox(dlg, wx.ID_ANY, _("Don't show me this again"))
        btnsizer = dlg.CreateStdDialogButtonSizer(wx.OK)
        
        dlgsizer = wx.BoxSizer(wx.VERTICAL)
        dlgsizer.Add(msgsizer, 0, wx.ALL, 10)
        dlgsizer.Add(checkbox, 0, wx.LEFT, 10)
        dlgsizer.Add(btnsizer, 0, wx.ALL|wx.ALIGN_CENTER, 10)
        dlg.SetSizerAndFit(dlgsizer)
        dlg.ShowModal()
        self.options['dllnamewarning'] = not checkbox.IsChecked()
        dlg.Destroy()
    
    def ShowOptions(self, startPageIndex=0):
        '''Show the program settings dialog, save them, apply them if necessary and save to file'''
        dlg = wxp.OptionsDialog(self, self.optionsDlgInfo, self.options, 
                                startPageIndex=startPageIndex, 
                                invert_scroll=self.options['invertscrolling'])
        ID = dlg.ShowModal()
        # Set the data
        if ID == wx.ID_OK:
            old_plugins_directory = self.ExpandVars(self.options['pluginsdir'])
            old_prefer_functions = self.options['syntaxhighlight_preferfunctions']
            old_style_triple_quotes = self.options['syntaxhighlight_styleinsidetriplequotes']
            old_use_custom_video_background = self.options['use_customvideobackground']
            old_custom_video_background = self.options['customvideobackground']
            self.options.update(dlg.GetDict())
            if self.options['pluginsdir'] != old_plugins_directory:
                self.SetPluginsDirectory(old_plugins_directory)
            for key in ['altdir', 'workdir', 'pluginsdir', 'avisynthhelpfile', 
                        'externalplayer', 'docsearchpaths']:
                self.options[key] = self.ExpandVars(self.options[key], False, '%' + key + '%')
            self.options['colourdata'] = self.colour_data.ToString()
            with open(self.optionsfilename, mode='wb') as f:
                cPickle.dump(self.options, f, protocol=0)
            if self.options['useworkdir'] and self.options['workdir']:
                os.chdir(self.ExpandVars(self.options['workdir']))
            else:
                os.chdir(self.initialworkdir)
            for i in xrange(self.scriptNotebook.GetPageCount()):
                script = self.scriptNotebook.GetPage(i)
                if (self.options['syntaxhighlight_preferfunctions'] != old_prefer_functions or 
                    self.options['syntaxhighlight_styleinsidetriplequotes'] != old_style_triple_quotes):
                        script.styling_refresh_needed = True
                script.SetUserOptions()
                if not self.options['usetabimages']:
                    self.scriptNotebook.SetPageImage(i, -1)            
            self.UpdateProgramTitle()
            style = wx.NO_BORDER
            if self.options['multilinetab']:
                style |= wx.NB_MULTILINE
            if self.options['fixedwidthtab']:
                style |= wx.NB_FIXEDWIDTH
            self.scriptNotebook.SetWindowStyleFlag(style)
            # a workaroud for multiline notebook issue
            w, h = self.scriptNotebook.GetSize()
            self.scriptNotebook.SetSize((w, h-1))
            self.scriptNotebook.SetSize((w, h))
            self.SetMinimumScriptPaneSize()
            if self.options['periodicbackup']:
                self.backupTimer.Start(self.options['periodicbackup'] * 60000)
            elif self.backupTimer.IsRunning():
                self.backupTimer.Stop()
            if (old_use_custom_video_background != self.options['use_customvideobackground'] or 
                self.options['use_customvideobackground'] and
                old_custom_video_background != self.options['customvideobackground']):
                    self.OnEraseBackground()
        dlg.Destroy()
    
    def SetPluginsDirectory(self, oldpluginsdirectory):
        '''Set the plugins autoload directory
        
        AviSynth: write to registry (admin rights needed)
        AvxSynth: set an environment variable
        '''
        if not self.options['pluginsdir']:
            self.options['pluginsdir'] = self.defaultpluginsdir
        pluginsdir_exp = self.ExpandVars(self.options['pluginsdir'])
        if os.name == 'nt':
            s1 = (_('Changing the plugins autoload directory writes to the Windows registry.') + 
                  _(' Admin rights are needed.'))
            s2 = _('Do you wish to continue?')
            ret = wx.MessageBox('%s\n\n%s' % (s1, s2), _('Warning'), wx.YES_NO|wx.ICON_EXCLAMATION)
            if ret == wx.YES:
                f = tempfile.NamedTemporaryFile(delete=False)
                txt = textwrap.dedent(u'''\
                HKCU\\Software\\Avisynth
                'plugindir2_5'= DELETE
                HKLM\\Software\\Avisynth
                'plugindir2_5'= "{dir}"
                ''').format(dir=pluginsdir_exp)
                f.write(txt.encode('utf16'))
                f.close()
                if ctypes.windll.shell32.ShellExecuteW(None, u'runas', u'cmd', 
                        u'/k "regini "{f}" & del "{f}""'.format(f=f.name), None, 0) > 32:
                    return
            self.options['pluginsdir'] = oldpluginsdirectory
        else:
            pluginsdir_exp = self.ExpandVars(self.options['pluginsdir'])
            os.environ['AVXSYNTH_RUNTIME_PLUGIN_PATH'] = pluginsdir_exp
            shell = os.environ.get('SHELL') # write to the shell's rc file
            if shell:
                rc = os.path.expandvars(os.path.join('$HOME', '.{0}rc'.format(
                                        os.path.basename(shell))))
                if os.path.isfile(rc):
                    warning = _("You're changing the plugins autoload directory.\n"
                                'Do you wish to change it for all applications? This will\n'
                                'require writing to {0}'
                               ).format(rc)
                    ret = wx.MessageBox(warning, _('Warning'), wx.YES_NO|wx.ICON_EXCLAMATION)
                    if ret == wx.YES:
                        export = u'export AVXSYNTH_RUNTIME_PLUGIN_PATH="{0}"'.format(pluginsdir_exp)
                        with open(rc, 'r+') as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines):
                                if 'AVXSYNTH_RUNTIME_PLUGIN_PATH' in line:
                                    lines[i] = export
                                    f.seek(0)
                                    f.truncate()
                                    f.writelines(lines)
                                    break
                            else:
                                f.write(export)
    
    def getMacrosLabelFromFile(self, filename):
        f = open(filename)
        text = f.readline().strip('#').strip()
        f.close()
        return text
    
    def ExpandVars(self, text, expand=True, blacklist=''):
        '''Expand and unexpand program variables
        
        Variables: %programdir%, %avisynthdir%, %pluginsdir%
        
        '''
        vars_ = [('%pluginsdir%', self.options['pluginsdir']), 
                 ('%avisynthdir%', self.avisynthdir), 
                 ('%programdir%', self.programdir)]
        blacklist = blacklist.split(';')
        if expand:
            index = 0, 1
            text = os.path.expandvars(text)
        else:
            index = 1, 0
            if '%altdir%' in blacklist:
                blacklist.append('%avisynthdir%')
        vars_ = filter(lambda x:x[0] not in blacklist, vars_)
        for var in [var for var in vars_ if var[1]]:
            text = text.replace(var[index[0]], var[index[1]])
        return text
    
    def FormatTime(self, s):
        '''Format seconds (int/float) to hours, minutes and seconds (str)'''
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return '%02i:%02i:%06.3f' % (h ,m, s)
    
    # Macro-related functions
    @AsyncCallWrapper
    def MacroIsMenuChecked(self, text):
        r'''IsMenuChecked(text)
        
        Retrieve the state of a menu item under Macros menu. The parameter 'text' has 
        the same meaning as that one of ExecuteMenuCommand function.
        
        '''
        if text.count('->') > 0:
            # text is the menu command name
            index = 0
        else:
            # text is the menu command shortcut string
            index = 1
        # Search through self.optionsShortcuts for a match
        if text == '':
            return False
        if self.macrosStack:
            menuItem = self.GetMenuBar().GetMenu(self.macroMenuPos).FindItemById(self.macrosStack[-1])
            menu = menuItem.GetMenu()
        else:
            menu = None
        for item in self.options['shortcuts']:
            if text.lower() == item[index].lower():
                id = item[2]
                menuItem = self.GetMenuBar().FindItemById(id)
                if menuItem.IsCheckable():
                    return menuItem.IsChecked()
                return False
            # assume using a incomplete text, search under the menu of the current running macro
            elif menu and item[0].lower().endswith(text.lower()):
                id = item[2]
                menuItem = menu.FindItemById(id)
                if menuItem:
                    if menuItem.IsCheckable():
                        return menuItem.IsChecked()
                    return False
        return False
    
    @AsyncCallWrapper
    def MacroExecuteMenuCommand(self, text, callafter=False):
        r'''ExecuteMenuCommand(text, callafter=False)
        
        Executes one of AvsP's menu commands as specified by the input 'text', which 
        can either be the name of the menu command or the keyboard shortcut.  
        
        For example, you can create a new tab in a macro by using either 
        "avsp.ExecuteMenuCommand('File -> New Tab')" or by using 
        "avsp.ExecuteMenuCommand('Ctrl+N')".  In this manner all menu commands are 
        available to AvsP's macro language.  The input text is not case sensitive, 
        but must be spelled precisely in order to work (a complete list of all the 
        commands and shortcuts with precise spelling can be found in the 
        "Options -> Configure shortcuts..." dialog).  If callafter=True, the menu 
        command will run after the current macro has exited.
        
        Returns True if successful, False otherwise.
        
        '''
        if text.count('->') > 0:
            # text is the menu command name
            index = 0
        else:
            # text is the menu command shortcut string
            index = 1
        # Search through self.optionsShortcuts for a match
        if text == '':
            return False
        if self.macrosStack:
            menuItem = self.GetMenuBar().GetMenu(self.macroMenuPos).FindItemById(self.macrosStack[-1])
            menu = menuItem.GetMenu()
        else:
            menu = None
        for item in self.options['shortcuts']:
            if text.lower() == item[index].lower():
                id = item[2]
                event = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, id)
                if callafter:
                    self.GetEventHandler().AddPendingEvent(event)
                else:
                    self.GetEventHandler().ProcessEvent(event)
                return True
            # assume using a incomplete text, search under the menu of the current running macro
            elif menu and item[0].lower().endswith(text.lower()):
                id = item[2]
                menuItem = menu.FindItemById(id)
                if menuItem:
                    event = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, id)
                    if callafter:
                        self.GetEventHandler().AddPendingEvent(event)
                    else:
                        self.GetEventHandler().ProcessEvent(event)
                    return True
        return False
    
    @AsyncCallWrapper
    def MacroSaveScript(self, filename='', index=None, default=''):
        r'''SaveScript(filename='', index=None, default='')
        
        Saves all the unsaved changes of the script in the tab located at the integer 
        'index'.  If 'index' is None, the script in the currently selected tab is used.
        
        The function will prompt the user with a dialog box for the location to save 
        the file if the string 'filename' is not provided and the script does not 
        already exist on the hard drive, using 'default' as the default filename; 
        it can be just a directory or basename.
        
        If a file with the same name as 'filename' already exists, it is overwritten 
        without any prompting.  The function returns the filename of the saved file.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return ''
        if filename == '':
            filename = script.filename
        self.SaveScript(filename, index, default=default)
        return script.filename
    
    @AsyncCallWrapper
    def MacroIsScriptSaved(self, index=None):
        r'''IsScriptSaved(index=None)
        
        Returns a boolean indicating whether the script in the tab located at the 
        integer 'index' has any unsaved changes.  If 'index' is None, the script in 
        the currently selected tab is used.  Returns False if there are any unsaved 
        changes, True otherwise.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        return (not script.GetModify())
    
    @AsyncCallWrapper
    def MacroGetScriptFilename(self, index=None, propose=None, only=None):
        r'''GetScriptFilename(index=None, propose=None, only=None)
        
        Returns the name of the script at the tab located at the integer 'index', 
        where an index of 0 indicates the first tab.  If 'index' is None, the 
        currently selected tab is used.  The returned name is the filename of the 
        script on the hard drive.  If the script has never been saved to the hard 
        drive, the returned name is an empty string.
        
        If 'propose' is set, return a proposed save filepath for the script based 
        on its filename, tab's title, first source in the script and user preferences.  
        This path can be useful to open/save other files.  Posible 'propose' values: 
        'general', 'image'.  If 'only' is set to 'dir' or 'base', return only the 
        directory or basename respectively.
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return None
        if propose:
            return self.GetProposedPath(index, type_=propose, only=only)
        if only:
            dir, base = os.path.split(script.filename)
            if only == 'dir':
                return dir
            if only == 'base':
                return base
        return script.filename
    
    @AsyncCallWrapper
    def MacroShowVideoFrame(self, framenum=None, index=None, forceRefresh=False):
        r'''ShowVideoFrame(framenum=None, index=None, forceRefresh=False)
        
        This function refreshes the video preview (unhiding it if it is hidden) using 
        the frame specified by the integer 'framenum', using the script of the tab 
        located at the integer 'index'.  The function also automatically selects the 
        tab located at 'index'.
        
        If 'framenum' is None, it uses the current frame number from the video preview 
        slider.  If 'index' is None, the frame of the currently selected tab is shown.  
        If the input 'forceRefresh' equals True, then the script is reloaded before 
        showing the video frame (normally the script is reloaded only when the text 
        has changed).
        
        '''
        # Get the desired script
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        self.ShowVideoFrame(framenum, forceRefresh=forceRefresh, script=script)
        self.SelectTab(index)
        self.Refresh()
        self.Update()
        if script.AVI.IsErrorClip():
            return False
        return True
    
    @AsyncCallWrapper
    def MacroShowVideoOffset(self, offset=0, units='frames', index=None):
        r'''ShowVideoOffset(offset=0, units='frames', index=None)
        
        Similar to ShowVideoFrame(), except the user specifies an offset instead of 
        the direct frame.  Offset can be positive or negative (for backwards jumping).  
        The string argument 'units' specifies the units of the offset, and can be either 
        'frames', 'seconds', 'minutes', or 'hours'.
        
        '''
        # Get the desired script
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        self.ShowVideoOffset(offset=offset, units=units)
        self.SelectTab(index)
        #~ self.Refresh()
        self.Update()
    
    @AsyncCallWrapper
    def MacroUpdateVideo(self, index=None):
        r'''UpdateVideo(index=None)
        
        This function is similar to ShowVideoFrame(), but does not force the video 
        preview to be shown if it is hidden.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        if self.previewWindowVisible:
            self.ShowVideoFrame(forceRefresh=True, script=script)
        else:
            self.UpdateScriptAVI(script, forceRefresh=True)
        if script.AVI is None or script.AVI.IsErrorClip():
            return False
        return True
    
    @AsyncCallWrapper
    def MacroWriteToScrap(self, txt, pos=-1):
        r'''WriteToScrap(txt, pos=-1)
        
        This function is identical to InsertText, except that instead of writing to 
        one of the existing tabs, it writes to a scrap window (which is always on top, 
        making it useful to keep track of the text as it changes).  Any inserted text 
        is highlighted temporarily.
        
        '''
        if not self.scrapWindow.IsShown():
            win = self.FindFocus()
            if win is None:
                win = self.currentScript
            self.scrapWindow.Show()
            win.SetFocus()
        if self.InsertText(txt, pos, index=-1):
            scrap = self.scrapWindow.textCtrl
            txtLength = len(txt)
            txtPos = scrap.GetCurrentPos() - txtLength
            scrap.StartStyling(txtPos, 31)
            scrap.SetStyling(txtLength, stc.STC_P_WORD)
            scrap.nInserted += 1
            scrap.Refresh()
            scrap.Update()
            def UndoStyling(scrap):
                #~ totalLength = scrap.GetTextLength()
                #~ if txtPos > totalLength:
                    #~ return
                #~ scrap.StartStyling(txtPos, 31)
                #~ scrap.SetStyling(min(txtLength, totalLength - txtPos), stc.STC_STYLE_DEFAULT)
                if scrap.nInserted > 0:
                    scrap.nInserted -= 1
                if scrap.nInserted == 0:
                    scrap.StartStyling(0, 31)
                    scrap.SetStyling(scrap.GetTextLength(), stc.STC_STYLE_DEFAULT)
            wx.FutureCall(1000, UndoStyling, scrap)
            return True
        else:
            return False
    
    @AsyncCallWrapper
    def MacroGetScrapText(self):
        r'''GetScrapText()
        
        Identical to the GetText function, except that it retrieves all text from the 
        scrap window.
        
        '''
        return self.scrapWindow.GetText()
    
    @AsyncCallWrapper
    def MacroReplaceText(self, old, new):
        script = self.currentScript
        txt = script.GetText().replace(old, new)
        script.SetText(txt)
        script.GotoPos(script.GetLength())
    
    @AsyncCallWrapper
    def MacroSetText(self, txt, index=None):
        r'''SetText(txt, index=None)
        
        Similar to InsertText, but replaces all the text in the script of the tab 
        located at the zero-based integer 'index' with the string 'txt'.  If the 
        input 'index' is None, the text is inserted into the script of the currently 
        selected tab.  Returns False if the operation failed, True otherwise.
        
        '''
        # Get the desired script
        script, index = self.getScriptAtIndex(index)
        if script is None or not isinstance(txt, basestring):
            return False
        # Replace the script's text
        script.SetText(txt)
        return True
    
    @AsyncCallWrapper
    def MacroGetText(self, index=None, clean=False):
        r'''GetText(index=None, clean=False)
        
        Returns the string containing all the text in the script of the tab located 
        at the zero-based integer 'index'.  If the input 'index' is None, the text 
        is retrieved from the script of the currently selected tab.  If 'clean' is 
        True, strip sliders and tags from the returned text.  Returns False 
        if the operation failed.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        txt = script.GetText()
        if clean:
            txt = self.getCleanText(txt)
        return txt
    
    @AsyncCallWrapper
    def MacroGetSelectedText(self, index=None):
        r'''GetSelectedText(index=None)
        
        Similar to GetText(), but returns only the selected text.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        return script.GetSelectedText()
    
    @AsyncCallWrapper
    def MacroGetFilename(self, title=_('Open a script or source'), filefilter=None, default=''):
        r'''GetFilename(title='Open a script or source', filefilter=None, default='')
        
        Displays an open file dialog box, returning the filename of the selected file 
        if the user clicked "OK", returning an empty string otherwise.  filefilter=None 
        means to apply those extensions defined at "Options|Extension templates".  
        'default' is the default filename set in the dialog box; it can be just a 
        directory or basename.
        
        '''
        default_dir, default_base = (default, '') if os.path.isdir(default) else os.path.split(default)
        initial_dir = default_dir if os.path.isdir(default_dir) else self.GetProposedPath(only='dir')
        if filefilter is None:
            extlist = self.options['templates'].keys()
            extlist.sort()
            extlist1 = ', '.join(extlist)
            extlist2 = ';*.'.join(extlist)
            filefilter = (_('Source files') + ' (%(extlist1)s)|*.%(extlist2)s|' + 
                          _('All files') + ' (*.*)|*.*') %  locals()
        dlg = wx.FileDialog(self, title, initial_dir, default_base, filefilter, 
                            wx.OPEN|wx.FILE_MUST_EXIST)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            filename = dlg.GetPath()
            dirname = os.path.dirname(filename)
            if os.path.isdir(dirname):
                self.options['recentdir'] = dirname
        else:
            filename = ''
        dlg.Destroy()
        return filename
    
    @AsyncCallWrapper
    def MacroGetSaveFilename(self, title=_('Save as'), filefilter = _('All files') + ' (*.*)|*.*', default=''):
        r'''GetSaveFilename(title='Save as', filefilter=_('All files') + ' (*.*)|*.*', default='')
        
        Displays an save file dialog box, returning the entered filename if the user 
        clicked "OK", returning an empty string otherwise.  'default' is the default 
        filename set in the dialog box; it can be just a directory or basename.
        
        '''
        default_dir, default_base = (default, '') if os.path.isdir(default) else os.path.split(default)
        initial_dir = default_dir if os.path.isdir(default_dir) else self.GetProposedPath(only='dir')
        dlg = wx.FileDialog(self, title, initial_dir, default_base, filefilter, 
                            wx.SAVE|wx.OVERWRITE_PROMPT)
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            filename = dlg.GetPath()
            dirname = os.path.dirname(filename)
            if os.path.isdir(dirname):
                self.options['recentdir'] = dirname
        else:
            filename = ''
        dlg.Destroy()
        return filename
    
    @AsyncCallWrapper
    def MacroGetDirectory(self, title=_('Select a directory'), default=''):
        r'''GetDirectory(title='Select a directory')
        
        Displays a dialog box to select a directory, returning the name of the 
        selected directory if the user clicked "OK", returning an empty string 
        otherwise.  'default' is the dialog's starting directory.
        
        '''
        initial_dir = default if os.path.isdir(default) else self.GetProposedPath(only='dir')
        dlg = wx.DirDialog(self, title, initial_dir)
        ID = dlg.ShowModal()
        if ID==wx.ID_OK:
            dirname = dlg.GetPath()
            if os.path.isdir(dirname):
                self.options['recentdir'] = dirname
        else:
            dirname = ''
        dlg.Destroy()
        return dirname
    
    @AsyncCallWrapper
    def MacroGetTextEntry(self, message=[''], default=[''], title=_('Enter information'), types=[''], width=400):
        r'''GetTextEntry(message='', default='', title='Enter information', types='text', width=400)
        
        Multiple entry dialog box.  In its more simple form displays a dialog box with 
        the string 'message' along with a field for text entry, initially filled with 
        the string 'default', returning the string from the text entry field if the 
        user clicked "OK", an empty string otherwise.
        
        title: title of the dialog box.
        
        The 'message', 'default' and 'types' parameters are list of lists.  If a list 
        were to contain only one component then it's not mandatory to wrap it as list.
        
        message: list of the lines of the dialog box, in which every component is a 
        list of the corresponding text strings to the entries in that line.  There must 
        be as many strings as desired entries.
        
        default: list of lists holding tuples with the default values for each entry.  
        In the same way as lists, if a tuple were to contain only one element then 
        it's not necessary to wrap it.  Each tuple and the whole parameter are optional 
        except for list entry type.
        
        types: list of lists containing the types of each entry.  Each value and the 
        whole parameter are optional.  Every omitted entry type defaults to a regular 
        text field.
        
        Types available:
        
        - 'text': regular text field.
          'default' values: 1-tuple with the initial field text.
        
        - 'file_open': text field with additional browse for file button ("open" 
              dialog).
          'default' values: 1-tuple or 2-tuple, with the initial field text and an 
              optional file wildcard with this syntax: 
              "BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif"
        
        - 'file_save': same as 'file_open', but with a "save" dialog.
        
        - 'dir': text field with additional browse for directory button.
          'default' values: 1-tuple with the initial field text.
        
        - 'list_read_only': drop-down list.  The 'default' tuple is mandatory.
          'default' values: n+1 tuple, where the first n elements are the strings 
              than compose the list and the last one is the entry selected by default.
        
        - 'list_writable': same as above but with the text field direcly writable, so 
              the return value is not limited to a selection from the list.
        
        - 'check': simple check box, returning True if checked.
          'default' values: 1-tuple with the predetermined boolean value, False as 
              default.
        
        - 'spin': numeric entry, with arrows to increment and decrement the value.
          'default' values: up-to-5-tuple, containing the default, minimum, maximum, 
              decimal digits shown and increment when using the arrows. With zero 
              decimal digits returns int, float otherwise. 
              Default: (0, None, None, 0, 1)
        
        - 'slider_h': horizontal slider. Similar to 'spin', but with a draggable handle.
          'default' values: up-to-4-tuple containing the default, minimum, maximum and 
              space between ticks marks that can be displayed alongside the slider. 
              Default: (50, 0, 100, no ticks)
        
        - 'slider_v': vertical slider, same as above.
        
        - 'sep': separator formed by a text string and a horizontal line.
          'default' values: 1-tuple with an optional fixed line length (by default 
              it extends through all the dialog's width).  Set it to -1 to auto-adjust 
              to the text length.  Note that an invisible separator can be created by 
              setting 'message' to '' and 'default' to 0 or -1.  To include the 'default' 
              parameter but don't give a fixed length (e.g. there's more entries 
              following that one) set the tuple to None or any not-convertible-to-int 
              value, like ''.
        
        A not recognized type string, including '', defaults to 'text' type.
        
        width: minimal horizontal length of the dialog box.  The width is distributed 
        uniformly between the entries in each line.
        
        Return values: list of entered values if the user clicks "OK", empty list 
        otherwise.
        
        '''
        # Complete the 'default' and 'types' lists
        optionsDlgInfo = [['']]
        options = dict()
        key = 0
        if not isinstance(message, collections.MutableSequence): message = [message]
        if not isinstance(default, collections.MutableSequence): default = [default] 
        if not isinstance(types, collections.MutableSequence): types = [types] 
        default += [''] * (len(message) - len(default))
        types +=  [''] * (len(message) - len(types))
        for eachMessageLine, eachDefaultLine, eachTypeLine in zip(message, default, types):
            if not isinstance(eachMessageLine, collections.MutableSequence): eachMessageLine = [eachMessageLine] 
            if not isinstance(eachDefaultLine, collections.MutableSequence): eachDefaultLine = [eachDefaultLine] 
            if not isinstance(eachTypeLine, collections.MutableSequence): eachTypeLine = [eachTypeLine] 
            lineLen=len(eachMessageLine)
            eachDefaultLine += [''] * (lineLen - len(eachDefaultLine))
            eachTypeLine +=  [''] * (lineLen - len(eachTypeLine))
            rowOptions = []
            for eachMessage, eachDefault, eachType in zip(eachMessageLine, eachDefaultLine, eachTypeLine):
                if not isinstance(eachDefault, collections.Sequence) or isinstance(eachDefault, basestring):
                    eachDefault = (eachDefault,)

                #  Set 'optionsDlgInfo' and 'options' from the kind of more user friendly 'message', 'default' and 'types'
                
                if eachType in ('file_open', 'file_save'):
                    key += 1
                    flag = (wxp.OPT_ELEM_FILE_OPEN if eachType == 'file_open' 
                            else wxp.OPT_ELEM_FILE_SAVE )
                    startDirectory = eachDefault[0] if os.path.isdir(eachDefault[0]) else os.path.dirname(eachDefault[0])
                    if not os.path.isdir(startDirectory):
                        startDirectory = self.GetProposedPath(only='dir')
                    misc = dict(width=width / lineLen, 
                        fileMask=eachDefault[1] if len(eachDefault) > 1 else '*.*', 
                        startDirectory=startDirectory, 
                        buttonText='...', buttonWidth=30, label_position=wx.VERTICAL, 
                        expand=True)
                    colOptions = [eachMessage, flag, key, '', misc]
                    options[key] = eachDefault[0]
                
                elif eachType == 'dir':
                    key += 1
                    flag = wxp.OPT_ELEM_DIR
                    startDirectory = eachDefault[0] if os.path.isdir(eachDefault[0]) else self.GetProposedPath(only='dir')
                    misc = dict(width=width / lineLen, 
                        startDirectory=startDirectory, 
                        buttonText='...', buttonWidth=30, label_position=wx.VERTICAL, 
                        expand=True)
                    colOptions = [eachMessage, flag, key, '', misc]
                    options[key] = eachDefault[0]
                
                elif eachType in ('list_writable', 'list_read_only'):
                    key += 1
                    flag = wxp.OPT_ELEM_LIST
                    misc = dict(width=width / lineLen, choices=eachDefault[:-1], 
                        writable=True if eachType == 'list_writable' else False, 
                        label_position=wx.VERTICAL, expand=True)
                    colOptions = [eachMessage, flag, key, '', misc]
                    options[key] = eachDefault[-1]
                
                elif eachType == 'check':
                    key += 1
                    flag = wxp.OPT_ELEM_CHECK
                    misc = dict(width=width / lineLen)
                    colOptions = [eachMessage, flag, key, '', misc]
                    options[key] = eachDefault[0] if eachDefault[0] else False
                
                elif eachType == 'spin':
                    key += 1
                    flag = wxp.OPT_ELEM_SPIN
                    misc = dict(width=width / lineLen, label_position=wx.VERTICAL, 
                                expand=True)
                    params = ('min_val', 'max_val', 'digits', 'increment')
                    for i, param in enumerate(eachDefault[1:]):
                        if isinstance(param, basestring):
                            try:
                                misc[params[i]] = int(param)
                            except:
                                misc[params[i]] = float(param)
                        else:
                            misc[params[i]] = param
                    colOptions = [eachMessage, flag, key, '', misc]
                    options[key] = float(eachDefault[0]) if eachDefault[0] else 0
                
                elif eachType in ('slider_h', 'slider_v'):
                    key += 1
                    flag = wxp.OPT_ELEM_SLIDER
                    if eachType == 'slider_v':
                        orientation = wx.VERTICAL
                        width = 150
                    else:
                        orientation = wx.HORIZONTAL
                        width = width / lineLen
                    misc = dict(width=width, label_position=wx.VERTICAL, 
                                orientation=orientation, expand=True)
                    params = ('minValue', 'maxValue', 'TickFreq')
                    for i, param in enumerate(eachDefault[1:]):
                        misc[params[i]] = int(param)
                    colOptions = [eachMessage, flag, key, '', misc]
                    options[key] = int(eachDefault[0]) if eachDefault[0] != '' else 50
                
                elif eachType == 'sep':
                    flag = wxp.OPT_ELEM_SEP
                    try:
                        sep_width = int(eachDefault[0])
                    except:
                        misc = dict()
                    else:
                        misc = dict(expand=False)
                        if sep_width == -1:
                            misc['adjust_width'] = True
                        else:
                            misc['width'] = sep_width
                    colOptions = [eachMessage, flag, 'mgte_sep', '', misc]
                
                else:
                    key += 1
                    flag = ''
                    misc = dict(width=width / lineLen, label_position=wx.VERTICAL)
                    colOptions = [eachMessage, flag, key, '', misc]
                    options[key] = str(eachDefault[0])
                
                rowOptions.append(colOptions)        
            optionsDlgInfo[0].append(rowOptions)
        
        # Open the dialog box and get the values
        dlg = wxp.OptionsDialog(self, optionsDlgInfo, options, title, starText=False, 
                                invert_scroll=self.options['invertscrolling'])
        ID = dlg.ShowModal()
        values = []
        if ID == wx.ID_OK:
            values_dic = dlg.GetDict()
            for key in range(1, len(options.keys()) + 1):
                values.append(values_dic[key])
        dlg.Destroy()
        if len(message) == 1:
            if values:
                return values[0]
            return ''
        return values
    
    @AsyncCallWrapper
    def MacroMsgBox(self, message, title='', cancel=False):
        r'''MsgBox(message, title='', cancel=False)
        
        Displays a simple dialog box with the text string 'message' and title 'title', 
        and an additional cancel button if 'cancel' is True.  Returns True if the user 
        presses 'OK' and the cancel button is present, or always True if it's not.
        
        '''
        style = wx.OK
        if title == _('Error'):
            style |= wx.ICON_ERROR
        elif title == _('Warning'):
            style |= wx.ICON_EXCLAMATION
        if cancel:
            style |= wx.CANCEL
        action = wx.MessageBox(message, title, style)
        return True if action == wx.OK else False
    
    @AsyncCallWrapper
    def MacroProgressBox(self, max=100, message='', title=_('Progress')):
        r'''ProgressBox(max=100, message='', title='Progress')
        
        Returns a wxPython dialog control which displays the progress of any given 
        task as a fraction of the input integer 'max'.
        
        In order to display the dialog, use its method Update(value, message), which 
        takes in the new progress value and optionally a new message.  The method 
        Update returns a tuple where its first component is False if the user clicked 
        on the Cancel button, True otherwise.  Wrap this method with SafeCall if it's 
        called within a thread.
        
        IMPORTANT: You must use the Destroy() method to destroy the dialog after you 
        are done with it.
        
        '''
        return wx.ProgressDialog(
            title, message, max,
            style=wx.PD_CAN_ABORT|wx.PD_ELAPSED_TIME|wx.PD_REMAINING_TIME
        )
    
    @AsyncCallWrapper
    def MacroGetScriptCount(self):
        r'''GetTabCount()
        
        Returns the number of scripts currently open.
        
        '''
        return self.scriptNotebook.GetPageCount()
    
    @AsyncCallWrapper
    def MacroGetCurrentIndex(self):
        r'''GetCurrentTabIndex()
        
        Returns the zero-based index of the currently selected tab.
        
        '''
        return self.scriptNotebook.GetSelection()

    def _x_MacroGetTabFilename(self, index=None):
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        return script.filename
    
    @AsyncCallWrapper
    def MacroSaveImage(self, filename='', framenum=None, index=None, default='', quality=None, depth=None):
        r'''SaveImage(filename='', framenum=None, index=None, default='', quality=None, depth=8)
        
        Saves the video frame specified by the integer 'framenum' as a file specified 
        by the string 'filename', where the video corresponds with the script at the 
        tab integer 'index'.  
        
        If 'filename' is an empty string, then the user is prompted with a dialog box 
        with 'default' as the default filename; it can be just a directory or basename.  
        If 'index' is None, then the currently selected tab is used.
        
        A quality level (0-100) can be specified for JPEG output. If the quality is 
        not specified, it gets prompted from a dialog window.
        
        The image can be saved as RGB48 if 'depth' is 16 and the ouptut format PNG.  
        In this case it's assumed that the script returns a fake clip double the real 
        height.
        
        Returns the choosen filename if the image was saved, None otherwise.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        self.refreshAVI = True
        self.MacroShowVideoFrame(framenum, index)
        if self.UpdateScriptAVI(script) is None:
            wx.MessageBox(_('Error loading the script'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        return self.SaveImage(filename, index=index, default=default, quality=quality, depth=depth)
    
    @AsyncCallWrapper
    def MacroGetVideoWidth(self, index=None):
        r'''GetVideoWidth(index=None)
        
        Returns the width of the video of the script at the tab integer 'index'.  If 
        'index' is None, then the currently selected tab is used.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        self.refreshAVI = True
        #~ self.MacroShowVideoFrame(None, index)
        if self.UpdateScriptAVI(script) is None:
            wx.MessageBox(_('Error loading the script'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        return script.AVI.Width
    
    @AsyncCallWrapper
    def MacroGetVideoHeight(self, index=None):
        r'''GetVideoHeight(index=None)
        
        Returns the height of the video of the script at the tab integer 'index'.  If 
        'index' is None, then the currently selected tab is used.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        self.refreshAVI = True
        #~ self.MacroShowVideoFrame(None, index)
        if self.UpdateScriptAVI(script) is None:
            wx.MessageBox(_('Error loading the script'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        return script.AVI.Height
    
    @AsyncCallWrapper
    def MacroGetVideoFramerate(self, index=None):
        r'''GetVideoFramerate(index=None)
        
        Returns the framerate of the video of the script at the tab integer 'index'.  
        If 'index' is None, then the currently selected tab is used.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        self.refreshAVI = True
        #~ self.MacroShowVideoFrame(None, index)
        if self.UpdateScriptAVI(script) is None:
            wx.MessageBox(_('Error loading the script'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        return script.AVI.Framerate
    
    @AsyncCallWrapper
    def MacroGetVideoFramecount(self, index=None):
        r'''GetVideoFramecount(index=None)
        
        Returns the framecount of the video of the script at the tab integer 'index'.  
        If 'index' is None, then the currently selected tab is used.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        self.refreshAVI = True
        #~ self.MacroShowVideoFrame(None, index)
        if self.UpdateScriptAVI(script) is None:
            wx.MessageBox(_('Error loading the script'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        return script.AVI.Framecount
    
    @AsyncCallWrapper
    def MacroGetPixelInfo(self, color='hex', wait=False, lines=False):
        '''GetPixelInfo(color='hex', wait=False, lines=False)
        
        Waits for the user to left-click in a position of the video preview, showing 
        it if hidden, and returns a tuple with the position and colour of the clicked 
        pixel.  The colour representation can be specified with the 'color' parameter.  
        Valid values: 'hex', 'rgb', 'rgba', 'yuv', None.  If None, only returns the 
        position.  
        
        The position is counted from the top left corner.  If the user clicks on a 
        part of the preview outside the video, the returned coordinates are set to 
        the nearest video pixel and the colour to None. 
        
        If the user doesn't click the video within the first 5 seconds after the 
        preview is refreshed, returns None.
        
        If 'wait' is True waits for multiple clicks with a 5 seconds time-out between 
        each one and returns a list with the pixel data, empty list if not pixel was 
        clicked.  Lines are marked over the video preview if 'lines' is True.
        
        '''
        if self.getPixelInfo:
            wx.MessageBox(_('A get pixel info operation has already started'), 
                             _('Error'), style=wx.OK|wx.ICON_ERROR)
            return
        if not self.MacroShowVideoFrame():
            return
        if color:
            color = color.lower() 
        if color == 'hex':
            i = 1
        elif color == 'rgb':
            i = 2
        elif color == 'rgba':
            i = 3
        elif color == 'yuv':
            i = 4
        else:
            i = 0
        if wait:
            pixelInfo_list = []
            pixelColor_list = []
            starting_script = self.currentScript
            oldzoomfactor = self.zoomfactor
            old_flip_h = 'fliphorizontal' in self.flip
            old_flip_v = 'flipvertical' in self.flip
            dc = wx.ClientDC(self.videoWindow)
            dc.SetLogicalFunction(wx.INVERT) # TODO: delete old pen color code
            dc.SetDeviceOrigin(self.xo, self.yo)
            dc.SetUserScale(self.zoomfactor, self.zoomfactor)
            pen_width = 1.0 if lines else 3.0
            while True:
                start = time.time()
                self.getPixelInfo = True
                while self.getPixelInfo:
                    time.sleep(0.05)
                    if (oldzoomfactor != self.zoomfactor or old_flip_h != ('fliphorizontal' in self.flip) or
                            old_flip_v != ('flipvertical' in self.flip)):
                        pixelScrolledXY_list = []
                        dc.SetUserScale(self.zoomfactor, self.zoomfactor)
                        oldzoomfactor = self.zoomfactor
                        old_flip_h = 'fliphorizontal' in self.flip
                        old_flip_v = 'flipvertical' in self.flip
                        for xy in pixelInfo_list:
                            pen_color = None
                            for color in reversed(pixelColor_list):
                                if color:
                                    pen_color = color
                                    break
                            if pen_color:
                                x, y = xy[0] if isinstance(xy[0], tuple) else xy
                                dc.SetPen(wx.Pen(wx.Colour(*((component + 128) % 256 for component in pen_color)), 
                                                 round(pen_width / self.zoomfactor)))
                                if old_flip_h:
                                    x = self.currentScript.AVI.DisplayWidth - 1 - x
                                if old_flip_v:
                                    y = self.currentScript.AVI.DisplayHeight - 1 - y
                                x = dc.LogicalToDeviceX(x) - self.xo
                                y = dc.LogicalToDeviceY(y) - self.yo
                                p2 = [float(c) / self.zoomfactor for c in self.videoWindow.CalcScrolledPosition(x, y)]
                                pixelScrolledXY_list.append(p2)
                                p1 = pixelScrolledXY_list[-2] if lines and len(pixelScrolledXY_list) > 1 else p2
                                dc.DrawLinePoint(p1, p2)
                    if time.time() - start >= 5:
                        break
                    wx.Yield()
                else:
                    if i:
                        pixelInfo_list.append((self.pixelInfo[0], self.pixelInfo[i]))
                    else:
                        pixelInfo_list.append(self.pixelInfo[0])
                    pixelColor_list.append(self.pixelInfo[2])
                    pen_color = None
                    for color in reversed(pixelColor_list):
                        if color:
                            pen_color = color
                            break
                    if pen_color:
                        x, y = self.pixelInfo[0]
                        dc.SetPen(wx.Pen(wx.Colour(*((component + 128) % 256 for component in pen_color)), 
                                         round(pen_width / self.zoomfactor)))
                        if old_flip_h:
                            x = self.currentScript.AVI.DisplayWidth - 1 - x
                        if old_flip_v:
                            y = self.currentScript.AVI.DisplayHeight - 1 - y
                        x = dc.LogicalToDeviceX(x) - self.xo
                        y = dc.LogicalToDeviceY(y) - self.yo
                        p2 = [float(c) / self.zoomfactor for c in self.videoWindow.CalcScrolledPosition(x, y)]
                        if lines and len(pixelInfo_list) > 1:
                            x0, y0 = pixelInfo_list[-2][0] if i else pixelInfo_list[-2]
                            if old_flip_h:
                                x0 = self.currentScript.AVI.DisplayWidth - 1 - x0
                            if old_flip_v:
                                y0 = self.currentScript.AVI.DisplayHeight - 1 - y0
                            x0 = dc.LogicalToDeviceX(x0) - self.xo
                            y0 = dc.LogicalToDeviceY(y0) - self.yo
                            p1 = [float(c) / self.zoomfactor for c in self.videoWindow.CalcScrolledPosition(x0, y0)]
                        else:
                            p1 = p2
                        dc.DrawLinePoint(p1, p2)
                    continue
                self.getPixelInfo = False
                break
            if starting_script == self.currentScript:
                self.PaintAVIFrame(dc, self.currentScript, self.currentframenum)
            return pixelInfo_list
        else:
            start = time.time()
            self.getPixelInfo = True
            while self.getPixelInfo:
                time.sleep(0.05)
                if time.time() - start >= 5:
                    break
                wx.Yield()
            else:
                if i:
                    return self.pixelInfo[0], self.pixelInfo[i]
                else:
                    return self.pixelInfo[0]
            self.getPixelInfo = False
    
    @AsyncCallWrapper
    def MacroGetVar(self, var, index=None, forceRefresh=False):
        r'''GetVar(var, index=None)
        
        Returns the content of the avisynth variable 'var' at the tab integer 'index'.  
        If 'index' is None, then the currently selected tab is used.  Returns None if 
        the specified variable is not defined.
        
        Warning: If the variable is frame-dependent the returned value may be unreliable.  
        Two conditions must be met to ensure that is correct:
        - Avisynth frame cache must be disabled, e.g. SetMemoryMax(1)
        - No filters that request multiple frames can be used in the script.
        
        '''
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        self.refreshAVI = True
        #~ self.MacroShowVideoFrame(None, index)
        if self.UpdateScriptAVI(script, forceRefresh=forceRefresh) is None:
            wx.MessageBox(_('Error loading the script'), _('Error'), style=wx.OK|wx.ICON_ERROR)
            return False
        try:
            return script.AVI.env.get_var(var)
        except avisynth.AvisynthError as err:
            if str(err) != "NotFound":
                raise
            return
    
    @AsyncCallWrapper
    def MacroRunExternalPlayer(self, executable=None, args='', index=None):
        r'''RunExternalPlayer(executable=None, args='', index=None)
        
        Runs the external program specified by the string argument 'executable'.
        
        The first argument passed to the program is the filename of the preview script 
        generated from the script located at the tab integer 'index'.  If 'index' is 
        None, then the currently selected tab is used.  Additional arguments can be 
        passed to the external program using the string parameter 'args'.  
        
        If the specified executable does not exist, then the function returns False, 
        otherwise it runs the executable program with the appropriate arguments and 
        returns True.
        
        '''
        if executable is None:
            executable = self.options['externalplayer']
        script, index = self.getScriptAtIndex(index)
        if script is None:
            return False
        if not self.RunExternalPlayer(executable, script, args, prompt=False):
            return False
        return True
    
    # Don't use decorator on this one
    def MacroPipe(self, cmd, text=None, frames=None, y4m=False, reorder_rgb=False, wait=False, callback=None, stdout=None, stderr=None):
        r"""Pipe(cmd, text=None, frames=None, y4m=False, reorder_rgb=False, wait=False, callback=None, stdout=None, stderr=None)
        
        Pipe raw frame data to an external application (video only)
        
        cmd: right side of the pipe (Unicode string). Accepts several variables: 
             {height}, {width}, {fps}, {frame_count}.
        text : script evaluated.  Defaults to the script in the current tab.  It 
               can also be a path to an AviSynth script.
        frames: sequence of frames to send.  Defaults to the complete frame range 
                of the evaluated text.
        y4m: add a yuv4mpeg2 header.  It can be a logical value or optionally a 
             dict with some of the following keys: 
             - colorspace: overrides the clip colorspace.
             - depth: for >8 bits per channel. It's appended to 'colorspace'.
             - width, height: may be necessary when piping fake data. It can be 
               either an int or a modifier '[x*/]\d+', e.g. 'width':'/2' will 
               signal half the width of the evaluated clip.
             - sar: 'X:Y' string.
             - X_stream, X_frame.
        reorder_rgb: convert BGR to RGB and BGRA to RGBA before piping.
        wait: wait for the process to finish.  If False, return the Popen object.  
              If True, return a tuple (Popen object, return code).  The return code 
              is 1 if the user cancels.
        callback: user function called before each frame is sent and after all frames 
                  are piped.  It receives three arguments, number of the current frame 
                  in the sequence, number of the current frame in the clip and total 
                  frame count, and must return True to keep piping, False to cancel. 
        stdout: file object where redirect stdout.  Defaults to sys.stdout on __debug__, 
                nowhere otherwise.
        stderr: file object where redirect stderr.  Defaults to stdout.
        
        """
        
        # Evaluate text
        workdir_exp = self.ExpandVars(self.options['workdir'])
        if (self.options['useworkdir'] and self.options['alwaysworkdir']
            and os.path.isdir(workdir_exp)):
                workdir = workdir_exp
        else:
            workdir = self.currentScript.workdir if text is None else ''
        if text is None:
            text = self.getCleanText(self.currentScript.GetText())
            filename = self.currentScript.filename
            # vpy hack, remove when VapourSynth is supported
            if os.name == 'nt' and filename.endswith('.vpy'):
                self.SaveScript(filename)
        else:
            if os.path.isfile(text):
                filename = text
                text = self.GetTextFromFile(text)[0]
            else:
                filename = 'AVS script'
        clip = pyavs.AvsClip(text, filename, workdir, display_clip=False, 
                             reorder_rgb=reorder_rgb, interlaced=self.interlaced)   
        if not clip.initialized or clip.IsErrorClip():
            self.MacroMsgBox(u'\n\n'.join((_('Error loading the script'), clip.error_message)), 
                             _('Error'))
            return
        if not frames:
            frames = range(clip.Framecount)
            total_frames = clip.Framecount
        elif callback:
            total_frames = len(frames)
        
        # Create pipe
        cmd = cmd.format(height=clip.Height, width=clip.Width, fps=clip.Framerate, 
                         frame_count=clip.Framecount)
        cmd = cmd.encode(encoding)
        cmd = shlex.split(cmd)
        if stdout is None:
            stdout = sys.stdout if __debug__ else subprocess.PIPE
        if stderr is None:
            stderr = subprocess.STDOUT
        if os.name == 'nt':
            info = subprocess.STARTUPINFO()
            try:
                info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = subprocess.SW_HIDE
            except AttributeError:
                import _subprocess
                info.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = _subprocess.SW_HIDE
            cmd = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, 
                                   stderr=stderr, startupinfo=info)
        else:
            cmd = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=stdout, 
                                   stderr=stderr)
        
        # Pipe the data and wait for the process to finish
        try:
            if y4m:
                if isinstance(y4m, dict):
                    y4m_frame = y4m.pop('X_frame', True)
                    if 'X_stream' in y4m:
                        y4m['X'] = y4m.pop('X_stream')
                    cmd.stdin.write(clip.Y4MHeader(**y4m))
                else:
                    y4m_frame = True
                    cmd.stdin.write(clip.Y4MHeader())
            else:
                y4m_frame = False
            for i, frame in enumerate(frames):
                if not callback or callback(i, frame, total_frames):
                    buf = clip.RawFrame(frame, y4m_frame)
                    error = clip.clip.get_error()
                    if not error:
                        cmd.stdin.write(buf)
                        continue
                    else:
                        self.MacroMsgBox(u'\n\n'.join((_('Error requesting frame {number}').
                                         format(number=frame), error)), _('Error'))
                cmd.terminate()
                if wait:
                    return cmd, 1
                return cmd
            cmd.stdin.close()
            if callback and not callback(total_frames, frame, total_frames):
                cmd.terminate()
                if wait:
                    return cmd, 1
                return cmd
            if wait:
                return cmd, cmd.wait()
            return cmd
        except Exception, err:
            try:
                if cmd.poll() is None:
                    cmd.terminate()
            except: pass
            raise err
    
    @AsyncCallWrapper
    def MacroGetBookmarkFrameList(self, title=False):
        r'''GetBookmarkList(title=False)
        
        Returns a list containing the video frame bookmarks currently set by the 
        user.  Note that these are the standard frame bookmarks, and do not contain 
        any selection startpoints or endpoints which may exist. If 'title' is True, 
        returns a list of tuple (frame, title).
        
        '''
        bookmarkList = [value for value, bmtype in self.GetBookmarkFrameList().items() if bmtype == 0]
        if title:
            for i in range(len(bookmarkList)):
                title = self.bookmarkDict.get(bookmarkList[i], '')
                bookmarkList[i] = (bookmarkList[i], title)
        return bookmarkList
    
    @AsyncCallWrapper
    def MacroSetBookmark(self, input):
        r'''SetBookmark(input)
        
        Toggle 'input' as a video frame bookmark.  If 'input' is a list, toggle each 
        of its values as a video frame bookmark.  Each bookmark can be a single integer 
        or a tuple (frame , title).  Returns True if successful, False otherwise.
        
        '''
        bmtype = 0
        try:
            value = int(input)
            self.AddFrameBookmark(value, bmtype)
            return True
        except (TypeError, ValueError):
            try:
                values = []
                for item in input:
                    if isinstance(item, basestring):
                        return self.MacroSetBookmark2(input)
                    values.append(int(item))
            except (TypeError, ValueError):
                return self.MacroSetBookmark2(input)
            lastindex = len(values) - 1
            for i, value in enumerate(values):
                if i != lastindex:
                    self.AddFrameBookmark(value, bmtype, refreshProgram=False)
                else:
                    self.AddFrameBookmark(value, bmtype, refreshProgram=True)
            return True
        return False
    
    def MacroSetBookmark2(self, input):
        r'''Set bookmarks from tuples (frame, title)'''
        bmtype = 0
        try:
            value, title = input
            value = int(value)
            if not isinstance(title, basestring): return False
            title = title.strip()
            self.bookmarkDict[value] = title
            if not title:
                del self.bookmarkDict[value]
            self.AddFrameBookmark(value, bmtype)
            return True
        except (TypeError, ValueError):
            if not isinstance(input, collections.Iterable):
                return False
            try:
                items = [(int(value), title.strip()) for value, title in input 
                         if isinstance(title, basestring)]
                if len(items) != len(input): return False
            except (TypeError, ValueError):
                return False            
            lastindex = len(items) - 1
            for i, item in enumerate(items):
                value, title = item
                self.bookmarkDict[value] = title
                if not title:
                    del self.bookmarkDict[value]
                if i != lastindex:
                    self.AddFrameBookmark(value, bmtype, refreshProgram=False)
                else:
                    self.AddFrameBookmark(value, bmtype, refreshProgram=True)
            return True
        return False
    
    @AsyncCallWrapper
    def MacroClearBookmarks(self, start=0, end=None, clear_current=True, clear_historic=False):
        r'''ClearBookmarks(start=0, end=None, clear_current=True, clear_historic=False)
        
        Clear all video frame bookmarks in the range [start, end], optionally 
        deleting also historic bookmarks.
        
        '''
        if clear_current:
            self.DeleteAllFrameBookmarks(bmtype=0, start=start, end=end)
        if clear_historic:
            self.OnMenuVideoBookmarkClearHistory(start=start, end=end)
    
    @AsyncCallWrapper
    def MacroGetSliderSelections(self):
        r'''GetSelectionList()
        
        Returns a list containing the video frame selections created by AvsP's trim 
        selection editor, where each element of the list is a 2-element tuple containing 
        the startpoint and the endpoint of a selection.  Note that the trim selection 
        editor must be visible for any selections to exist.
        
        '''
        return self.GetSliderSelections(self.invertSelection)

    def _x_MacroGetAvs2aviDir(self):
        return self.options['avs2avidir']

    def _x_MacroSetAvs2aviDir(self, exename):
        if os.path.isfile(exename):
            self.options['avs2avidir'] = exename
            return True
        return False
    
    @AsyncCallWrapper
    def MacroGetSliderInfo(self, index=None):
        r'''GetSliderInfo(index=None)
        
        Returns a list containing information for each slider in the script located 
        at the tab integer 'index'.  If 'index' is None, then the currently selected 
        tab is used.
        
        The slider information consists of 4 items.  The first item is the slider text 
        itself.  The second item is the slider label.  The third item is the list of 
        numbers which the graphical slider represents.  The fourth item is the number 
        of decimal places for the slider numbers as specified by the user.
        
        '''
        script, index = self.getScriptAtIndex(index)
        self.UpdateScriptTagProperties(script)
        #~ self.UpdateScriptAVI(script, forceRefresh=True)
        data = self.createUserSliders(script, parseonly=True)
        info = []
        for text, values in data:
            if values is None:
                info.append((text, values))
                continue
            label, minval, maxval, val, nDecimal, step = values
            #~ if step is None:
                #~ if nDecimal == 0:
                    #~ step = 1
                #~ else:
                    #~ step = 1/(nDecimal*10.0)
            #~ count = int((maxval - minval) / step)
            if step is None:
                step = 1/float(10**nDecimal)
            else:
                step = float(step)
            count = int(round((maxval - minval) / step + 1))
            numlist = [minval,] + map(lambda x: step*x + minval, range(1, count)) #+ [maxval,]
            if nDecimal == 0:
                numlist = [int(x) for x in numlist]
            info.append((text, label, numlist, nDecimal))
        return info

    @staticmethod
    def FormatDocstring(method=None, docstring=None):
        '''Format docstrings, adapted from PEP 257'''
        if docstring is None:
            docstring = method.__doc__
        if not docstring:
            return ''
        # Convert tabs to spaces (following the normal Python rules)
        # and split into a list of lines:
        lines = docstring.expandtabs().splitlines()
        # Determine minimum indentation (first line doesn't count):
        indent = sys.maxint
        for line in lines[1:]:
            stripped = line.lstrip()
            if stripped:
                indent = min(indent, len(line) - len(stripped))
        # Remove indentation (first line is special):
        trimmed = [lines[0].strip()]
        if indent < sys.maxint:
            for line in lines[1:]:
                trimmed.append(line[indent:].rstrip())
        doc = '\n'.join(trimmed).split('\n', 1)
        return doc[0] + '\n' + '='*len(doc[0]) + '\n' + doc[1] + '\n'
    
    
    class AvsP_functions(object):
        
        def __init__(self, parent):
            self.__doc__ = parent.FormatDocstring(docstring='''AVSPMOD MACRO API
                
                    AvsP allows you to define your own macros using the Python programming 
                language.  In order to use this functionality, simply write your own Python 
                code in a text file and save it in the "macros" directory with the extension 
                ".py".  The next time you start AvsP.exe, your macro will appear in the 
                "Macros" menu (the macros are sorted alphabetically).  The extension and 
                any initial open-close brackets are removed in the displayed name - the file 
                "[001] My Macro.py" shows up in the menu as "My Macro", in order to help 
                order the macros in the menu.  If the striped name is empty, the first line 
                from the script is used as the display name, removing '#' if present.  
                Separators can be inserted in the menu by creating empty macro files with 
                name "[001] ---.py".  To help further organize your macros, you can put 
                macros in any subdirectories you create in the "macros" folder, which will 
                automatically create submenus in the "Macros" menu.
                
                    Macro files can also be used to add options to the macro menu that can 
                be read by any macro through the IsMenuChecked macro function.  To include 
                a check option, create an empty macro and prefix its name with "ccc", e.g. 
                "[001] ccc option name.py".  To add exclusive choices, create a macro for 
                each option with the prefix "rrr".
                
                    Macros can optionally run in its own thread if the script includes a 
                commentary line like "# run macro in new thread" (without quotes).  This 
                makes possible to wait for the end of external commands started from the 
                macro without locking AvsPmod.
                
                    You need to have a pretty good understanding of Python to write your own 
                macros (plenty of documentation and tutorials for Python can be found on the 
                web).  Several examples are provided in the "macros" directory to show basic 
                usage, many more things are possible.  The following is a description of the 
                functions provided in the local module avsp to give you control over the 
                program itself (see the examples for appropriate usage).  This information 
                can also be retrieved from the module or functions' docstring (help(avsp) or 
                help(avsp.FunctionName)).\n
                ''')
            # Text setting and retrieving
            self.InsertText = parent.InsertText
            self.__doc__ += parent.FormatDocstring(self.InsertText)
            self.SetText = parent.MacroSetText
            self.__doc__ += parent.FormatDocstring(self.SetText)
            #~ ReplaceText = parent.MacroReplaceText
            self.GetText = parent.MacroGetText
            self.__doc__ += parent.FormatDocstring(self.GetText)
            self.GetSelectedText = parent.MacroGetSelectedText
            self.__doc__ += parent.FormatDocstring(self.GetSelectedText)
            self.GetSourceString = parent.GetSourceString
            self.__doc__ += parent.FormatDocstring(self.GetSourceString)
            self.GetPluginString = parent.GetPluginString
            self.__doc__ += parent.FormatDocstring(self.GetPluginString)
            self.GetFilename = parent.MacroGetFilename
            self.__doc__ += parent.FormatDocstring(self.GetFilename)
            self.GetSaveFilename = parent.MacroGetSaveFilename
            self.__doc__ += parent.FormatDocstring(self.GetSaveFilename)
            self.GetDirectory = parent.MacroGetDirectory
            self.__doc__ += parent.FormatDocstring(self.GetDirectory)
            self.GetTextEntry = parent.MacroGetTextEntry
            self.__doc__ += parent.FormatDocstring(self.GetTextEntry)
            self.WriteToScrap = parent.MacroWriteToScrap
            self.__doc__ += parent.FormatDocstring(self.WriteToScrap)
            self.GetScrapText = parent.MacroGetScrapText
            self.__doc__ += parent.FormatDocstring(self.GetScrapText)
            # Program tab control
            self.NewTab = parent.NewTab
            self.__doc__ += parent.FormatDocstring(self.NewTab)
            self.CloseTab = parent.CloseTab
            self.__doc__ += parent.FormatDocstring(self.CloseTab)
            self.SelectTab = parent.SelectTab
            self.__doc__ += parent.FormatDocstring(self.SelectTab)
            #~ GetTabFilename = parent.MacroGetTabFilename
            self.GetTabCount = parent.MacroGetScriptCount
            self.__doc__ += parent.FormatDocstring(self.GetTabCount)
            self.GetCurrentTabIndex = parent.MacroGetCurrentIndex
            self.__doc__ += parent.FormatDocstring(self.GetCurrentTabIndex)
            self.GetScriptFilename = parent.MacroGetScriptFilename
            self.__doc__ += parent.FormatDocstring(self.GetScriptFilename)
            # File opening and saving
            self.OpenFile = parent.OpenFile
            self.__doc__ += parent.FormatDocstring(self.OpenFile)
            self.SaveScript = parent.MacroSaveScript
            self.__doc__ += parent.FormatDocstring(self.SaveScript)
            self.SaveScriptAs = parent.SaveScript
            self.__doc__ += parent.FormatDocstring(self.SaveScriptAs)
            self.IsScriptSaved = parent.MacroIsScriptSaved
            self.__doc__ += parent.FormatDocstring(self.IsScriptSaved)
            self.RenameScript = parent.RenameScript
            self.__doc__ += parent.FormatDocstring(self.RenameScript)
            # Video related functions
            self.ShowVideoFrame = parent.MacroShowVideoFrame
            self.__doc__ += parent.FormatDocstring(self.ShowVideoFrame)
            self.ShowVideoOffset = parent.MacroShowVideoOffset
            self.__doc__ += parent.FormatDocstring(self.ShowVideoOffset)
            self.UpdateVideo = parent.MacroUpdateVideo
            self.__doc__ += parent.FormatDocstring(self.UpdateVideo)
            self.HideVideoWindow = parent.HidePreviewWindow
            self.__doc__ += parent.FormatDocstring(self.HideVideoWindow)
            #~ ToggleVideoWindow = parent.MacroToggleVideoWindow
            self.GetFrameNumber = parent.GetFrameNumber
            self.__doc__ += parent.FormatDocstring(self.GetFrameNumber)
            self.GetVideoWidth = parent.MacroGetVideoWidth
            self.__doc__ += parent.FormatDocstring(self.GetVideoWidth)
            self.GetVideoHeight = parent.MacroGetVideoHeight
            self.__doc__ += parent.FormatDocstring(self.GetVideoHeight)
            self.GetVideoFramerate = parent.MacroGetVideoFramerate
            self.__doc__ += parent.FormatDocstring(self.GetVideoFramerate)
            self.GetVideoFramecount = parent.MacroGetVideoFramecount
            self.__doc__ += parent.FormatDocstring(self.GetVideoFramecount)
            self.GetPixelInfo = parent.MacroGetPixelInfo
            self.__doc__ += parent.FormatDocstring(self.GetPixelInfo)
            self.GetVar = parent.MacroGetVar
            self.__doc__ += parent.FormatDocstring(self.GetVar)
            self.RunExternalPlayer = parent.MacroRunExternalPlayer
            self.__doc__ += parent.FormatDocstring(self.RunExternalPlayer)
            self.Pipe = parent.MacroPipe
            self.__doc__ += parent.FormatDocstring(self.Pipe)
            self.SaveImage = parent.MacroSaveImage
            self.__doc__ += parent.FormatDocstring(self.SaveImage)
            # Bookmarks
            self.GetBookmarkList = parent.MacroGetBookmarkFrameList
            self.__doc__ += parent.FormatDocstring(self.GetBookmarkList)
            self.SetBookmark = parent.MacroSetBookmark
            self.__doc__ += parent.FormatDocstring(self.SetBookmark)
            self.ClearBookmarks = parent.MacroClearBookmarks
            self.__doc__ += parent.FormatDocstring(self.ClearBookmarks)
            self.GetSelectionList = parent.MacroGetSliderSelections
            self.__doc__ += parent.FormatDocstring(self.GetSelectionList)
            # Miscellaneous
            self.MsgBox = parent.MacroMsgBox
            self.__doc__ += parent.FormatDocstring(self.MsgBox)
            self.ProgressBox = parent.MacroProgressBox
            self.__doc__ += parent.FormatDocstring(self.ProgressBox)
            #~ GetAvs2aviDir = parent.MacroGetAvs2aviDir
            #~ SetAvs2aviDir = parent.MacroSetAvs2aviDir
            self.GetSliderInfo = parent.MacroGetSliderInfo
            self.__doc__ += parent.FormatDocstring(self.GetSliderInfo)
            #~ UpdateFunctionDefinitions = parent.UpdateFunctionDefinitions
            self.ExecuteMenuCommand = parent.MacroExecuteMenuCommand
            self.__doc__ += parent.FormatDocstring(self.ExecuteMenuCommand)
            self.IsMenuChecked = parent.MacroIsMenuChecked
            self.__doc__ += parent.FormatDocstring(self.IsMenuChecked)
            def GetWindow():
                r'''GetWindow()
                
                Get the handler of AvsP's main window.  Don't use this except you know what 
                you are doing.
                
                '''
                return parent
            self.GetWindow = GetWindow
            self.__doc__ += parent.FormatDocstring(self.GetWindow)
            def SafeCall(method, *args, **kwargs):
                r'''SafeCall(callable [, param1, ...])
                
                Run the function or method specified in a thread-safe way.  This wrapper is 
                usually necessary when the code is run from a thread and the callable is not 
                part of the macro API and interacts with the GUI:
                - Update method of ProgressBox
                - Resources obtained through GetWindow
                - Other wxPython resources obtained through importing wx.
                
                '''
                return AsyncCallWrapper(method)(*args, **kwargs)
            self.SafeCall = SafeCall
            self.__doc__ += parent.FormatDocstring(self.SafeCall)
            self.__doc__ += '\n' + '** VARIABLES **' + '\n'*3
            self.__doc__ += ('Version\n=======\n\nDictionary containing version info.  Keys:\n'
                             '[AvsP, AviSynth_string, AviSynth_number, AviSynth_interface]\n\n\n')
            self.__doc__ += ('Options\n=======\n\nThis dictionary can be used to store persistent '
                             'data.  Each macro have its \nown dictionary.\n\n\n')
            self.__doc__ += ('Last\n====\n\nThis variable contains the return value of the latest '
                             'executed macro.  It is \nuseful to create reusable macros.\n')
        
    
    def ExecuteMacro(self, macrofilename='', return_env=False):
        
        if return_env:
            return self.AvsP_functions(self)
            
        def ShowException():
            if __debug__:
                raise
            match = re.match('\w+\((?:\d+,)?\s*[\'"](.*)[\'"],?\)$', 
                             repr(sys.exc_info()[1]).decode('string_escape').decode(encoding))
            message = match.group(1) if match else sys.exc_info()[1]
            extra = ''
            for line in traceback.format_exc().split('\n'):
                if line.endswith('in AvsP_macro_main'):
                    try:
                        linenumber = int(line.split(',')[1].split()[1]) - 1
                        extra = ' (%s, line %i)' % (os.path.basename(macrofilename), linenumber)
                    except:
                        pass
                    break
            error_string = '%s\n\n%s%s' % (_('Error in the macro:'), message, extra)
            AsyncCall(wx.MessageBox, error_string, _('Error'), style=wx.OK|wx.ICON_ERROR).Wait()  
        
        if os.path.isfile(macrofilename):
            try:
                #~ execfile(macrofilename, {'avsp':AvsP_functions}, {})
                # Read the macro text
                f = open(macrofilename)
                #~ macroLines = f.readlines()
                txt = f.read()
                f.close()
                macroLines = txt.split('\n')
                # Check if the macro should run in its own thread
                re_thread = re.compile(r'\s*#\s*run[\s_]*(macro)?[\s_]*in[\s_]*(new)?[\s_]*thread', re.I)
                for line in macroLines:
                    if re.match(re_thread, line):
                        thread = True
                        break
                else:
                    thread = False
                # Check for syntax errors (thows SyntaxError exception with line number)
                try:
                    compile('\n'.join(macroLines+['pass']), macrofilename, 'exec')
                except SyntaxError, e:
                    if not str(e).startswith("'return' outside function"):
                        raise
                # Wrap the macro in a function (allows top-level variables to be treated "globally" within the function)
                lineList = []
                while macroLines and macroLines[0].lstrip().startswith('#'):
                    lineList.append(macroLines.pop(0))
                lineList += ['def AvsP_macro_main():'] + ['\t%s' % line for line in macroLines] + ['global last\nlast = AvsP_macro_main()']
                macrotxt = '\n'.join(lineList)
                # Prepare the macro variables
                self.macroVars['avsp'] = self.AvsP_functions(self)
                self.macroVars['avsp'].Version = dict(AvsP=self.version, 
                                    AviSynth_string=self.avisynthVersion[0], 
                                    AviSynth_number=self.avisynthVersion[1], 
                                    AviSynth_interface=self.avisynthVersion[2])
                macrobasename = os.path.splitext(os.path.basename(macrofilename))[0]
                match = re.match(r'\[\s*\d+\s*\]\s*(.*)', macrobasename)
                if match:
                    macrobasename = match.group(1)
                if macrobasename not in self.optionsMacros:
                    self.optionsMacros[macrobasename] = {}
                self.macroVars['avsp'].Options = self.optionsMacros[macrobasename]
                hash_pre = hash(repr(self.optionsMacros[macrobasename].items()))
                self.macroVars['avsp'].Last = self.macroVars['last']
                def MacroHelp(function):
                    '''help(function)\nPrint the function's description of use'''
                    print self.FormatDocstring(function)
                self.macroVars['help'] = MacroHelp
                self.macroVars['_'] = _
                # Execute the macro
                def MacroFunction():
                    try:
                        exec macrotxt in self.macroVars, {}
                    except:
                        ShowException()
                    if (hash(repr(self.optionsMacros[macrobasename].items())) != hash_pre and
                        os.path.isdir(os.path.dirname(self.macrosfilename))):
                            f = open(self.macrosfilename, mode='wb')
                            cPickle.dump(self.optionsMacros, f, protocol=0)
                            f.close()
                if thread:    
                    thread = threading.Thread(target=MacroFunction, name='MacroThread')
                    thread.daemon = True
                    thread.start()
                else:
                    MacroFunction()
            except:
                ShowException()
        else:
            wx.MessageBox(_("Couldn't find %(macrofilename)s") % locals(), _('Error'), style=wx.OK|wx.ICON_ERROR)
    
    def RenameMacro(self, menu):
        for menuItem in menu.GetMenuItems():
            if menuItem.IsCheckable():
                id = menuItem.GetId()
                macrofilename = self.macrosImportNames[id]
                newname = macrofilename
                if menuItem.IsChecked():
                    newname = newname.replace('ccc', 'CCC')
                    newname = newname.replace('rrr', 'RRR')
                else:
                    newname = newname.replace('CCC', 'ccc')
                    newname = newname.replace('RRR', 'rrr')
                if newname != macrofilename:
                    try:
                        os.rename(macrofilename, newname)
                    except OSError:
                        pass
                    
class MainApp(wxp.App):
    def OnInit(self):
        self.frame = MainFrame()
        self.SetTopWindow(self.frame)
        return True

def main():
    try:
        ctypes.CDLL('libX11.so').XInitThreads()
    except:
        pass
    threading.current_thread().name = 'MainThread'
    try:
        redirect_flag = not __debug__
        #~ app = MainApp(redirect_flag, name='AvsP')
        app = MainApp(redirect_flag)
        app.MainLoop()
    except SystemExit:
        sys.exit(0)

if __name__ == '__main__':
    main()
