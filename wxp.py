# wxp - General framework classes for wxPython
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

# Dependencies:
# Python (tested with v2.5.1)
# wxPython (tested with v2.6.3.3 unicode)

import wx
import wx.lib.buttons as wxButtons
import  wx.lib.mixins.listctrl  as  listmix
import  wx.lib.filebrowsebutton as filebrowse
import  wx.lib.colourselect as  colourselect
from wx import stc
import string
import keyword
import os
import sys
import copy
import time

import wx.lib.newevent
import socket
import thread
import StringIO
import cPickle

from icons import checked_icon, unchecked_icon

OPT_ELEM_STRING = 0
OPT_ELEM_INT = 1
OPT_ELEM_CHECK = 2
OPT_ELEM_FLOAT = 3
OPT_ELEM_RADIO = 4
OPT_ELEM_FILE = 5
OPT_ELEM_DIR = 6
OPT_ELEM_COLOR = 7
OPT_ELEM_FONT = 8
OPT_ELEM_FILE_URL = 9
OPT_ELEM_DIR_URL = 10
OPT_ELEM_BUTTON = 11

keyStringList = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
    'Enter', 'Space', 'Escape', 'Tab', 'Insert', 'Backspace', 'Delete', 
    'Home', 'End', 'PgUp', 'PgDn', 'Up', 'Down', 'Left', 'Right',
    'Numpad 0', 'Numpad 1', 'Numpad 2', 'Numpad 3', 'Numpad 4', 'Numpad 5', 'Numpad 6', 'Numpad 7', 'Numpad 8', 'Numpad 9',
    'Numpad +', 'Numpad -', 'Numpad *', 'Numpad /', 'Numpad .', 'Numpad Enter',
    '`', '-', '=', '\\', '[', ']', ';', "'", ',', '.', '/',
    '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '|', '{', '}', ':', '"', '<', '>', '?',
]

numpadDict = {
    'Numpad 0': wx.WXK_NUMPAD0, 
    'Numpad 1': wx.WXK_NUMPAD1, 
    'Numpad 2': wx.WXK_NUMPAD2, 
    'Numpad 3': wx.WXK_NUMPAD3, 
    'Numpad 4': wx.WXK_NUMPAD4,
    'Numpad 5': wx.WXK_NUMPAD5, 
    'Numpad 6': wx.WXK_NUMPAD6, 
    'Numpad 7': wx.WXK_NUMPAD7, 
    'Numpad 8': wx.WXK_NUMPAD8, 
    'Numpad 9': wx.WXK_NUMPAD9,
    'Numpad +': wx.WXK_NUMPAD_ADD, 
    'Numpad -': wx.WXK_NUMPAD_SUBTRACT,
    'Numpad *': wx.WXK_NUMPAD_MULTIPLY,
    'Numpad /': wx.WXK_NUMPAD_DIVIDE,
    'Numpad .': wx.WXK_NUMPAD_DECIMAL, 
    'Numpad Enter': wx.WXK_NUMPAD_ENTER,
}

(PostArgsEvent, EVT_POST_ARGS) = wx.lib.newevent.NewEvent()

try: _
except NameError:
    def _(s): return s

def MakeWindowTransparent(window, amount, intangible=False):
    import ctypes
    user32 = ctypes.windll.user32
    hwnd = window.GetHandle()
    style = user32.GetWindowLongA(hwnd, 0xffffffecL)
    style |= 0x00080000
    if intangible:
        style |= 0x00000020L
        window.SetWindowStyleFlag(window.GetWindowStyleFlag()|wx.STAY_ON_TOP)
    user32.SetWindowLongA(hwnd, 0xffffffecL, style)
    user32.SetLayeredWindowAttributes(hwnd, 0, amount, 2)
    
def GetTranslatedShortcut(shortcut):
        return shortcut.replace('Ctrl', _('Ctrl')).replace('Shift', _('Shift')).replace('Alt', _('Alt'))
        
class CharValidator(wx.PyValidator):
    def __init__(self, flag):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)
        
    def Clone(self):
        return CharValidator(self.flag)
        
    def Validate(self, win):
        return True
        
    def TransferToWindow(self):
        return True
        
    def TransferFromWindow(self):
        return True
        
    def OnChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if self.flag == 'alpha' and chr(key) in string.letters:
            event.Skip()
            return
        if self.flag == 'digit' and chr(key) in string.digits:
            event.Skip()
            return
        return
        
class ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.parent = parent
        
    def SelectItem(self, item):
        self.SetItemState(item, wx.LIST_STATE_SELECTED|wx.LIST_STATE_FOCUSED, wx.LIST_STATE_SELECTED|wx.LIST_STATE_FOCUSED)
        self.EnsureVisible(item)
        self.SetFocus()
        
    def SelectLabel(self, label):
        item = self.FindItem(-1, label)
        self.SelectItem(item)
            
    def GetSelectedItem(self):
        return self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        
class MenuItemInfo(object):
    def __init__(self, label=None, handler=None, status=None, submenu=None, id=wx.ID_ANY):
        self.label = label
        self.handler = handler
        self.submenu = submenu
        self.id = id

class StdoutStderrWindow:
    """
    A class that can be used for redirecting Python's stdout and
    stderr streams.  It will do nothing until something is wrriten to
    the stream at which point it will create a Frame with a text area
    and write the text there.
    """
    def __init__(self, title = "Error Window"):
        self.frame  = None
        self.title  = title
        self.pos    = wx.DefaultPosition
        self.size   = (450, 300)
        self.parent = None
        logname = 'avsp_error_log.txt'
        if hasattr(sys,'frozen'):
            self.logfilename = os.path.join(os.path.dirname(sys.executable), logname)
        else:
            self.logfilename = os.path.join(os.getcwd(), logname)
        self.firstTime = True

    def SetParent(self, parent):
        """Set the window to be used as the popup Frame's parent."""
        self.parent = parent


    def CreateOutputWindow(self, st):
        self.frame = wx.Frame(self.parent, -1, self.title, self.pos, self.size,
                              style=wx.DEFAULT_FRAME_STYLE)
        self.text  = wx.TextCtrl(self.frame, -1, "",
                                 style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.text.AppendText(st)
        self.frame.Show(True)
        wx.EVT_CLOSE(self.frame, self.OnCloseWindow)
        

    def OnCloseWindow(self, event):
        if self.frame is not None:
            self.frame.Destroy()
        self.frame = None
        self.text  = None


    # These methods provide the file-like output behaviour.
    def write(self, text):
        """
        Create the output window if needed and write the string to it.
        If not called in the context of the gui thread then uses
        CallAfter to do the work there.
        """        
        if self.frame is None:
            if not wx.Thread_IsMain():
                wx.CallAfter(self.CreateOutputWindow, text)
            else:
                self.CreateOutputWindow(text)
        else:
            if not wx.Thread_IsMain():
                wx.CallAfter(self.text.AppendText, text)
            else:
                self.text.AppendText(text)
        f = open(self.logfilename, 'a')
        if self.firstTime:
            f.write('\n[%s]\n' % time.asctime())
            self.firstTime = False
        f.write(text)
        f.close()


    def close(self):
        if self.frame is not None:
            wx.CallAfter(self.frame.Close)


    def flush(self):
        pass
        
class App(wx.App):
    outputWindowClass = StdoutStderrWindow

class SingleInstanceApp(wx.App):
    outputWindowClass = StdoutStderrWindow
    port = 50009
    name = 'SingleInstanceApp'
    IsFirstInstance = True
    boolSingleInstance = True
    def __init__(self, *args, **kwargs):
        # Get extra keyword arguments
        if kwargs.has_key('name'):
            self.name = kwargs.pop('name')
        if kwargs.has_key('port'):
            self.port = kwargs.pop('port')
        # Determine if program is already running or not
        self.instance = wx.SingleInstanceChecker(self.name+wx.GetUserId())
        if self.instance.IsAnotherRunning():
            self.IsFirstInstance = False
            if self.boolSingleInstance:
                # Send data to the main instance via socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', self.port))
                pickledstring = StringIO.StringIO()
                cPickle.dump(sys.argv[1:],pickledstring)
                sock.sendall(pickledstring.getvalue())
                response = sock.recv(8192)
            # Start the wx.App (typically check self.IsFirstInstance flag and return False)
            wx.App.__init__(self, *args, **kwargs)
        else:
            self.IsFirstInstance = True
            wx.App.__init__(self, *args, **kwargs)
            # Start socket server (in a separate thread) to receive arguments from other instances
            self.argsPosterThread = ArgsPosterThread(self)
            self.argsPosterThread.Start()
            
    def OnExit(self):
        if self.IsFirstInstance:
            wx.Yield()
            self.argsPosterThread.Stop()
            running = 1
            while running:
                running = 0
                running = running + self.argsPosterThread.IsRunning()
                time.sleep(0.1)

class ArgsPosterThread:
    def __init__(self, app):
        self.app = app
        
    def Start(self):
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())
        
    def Stop(self):
        self.keepGoing = False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', self.app.port))
        sock.close()
        
    def IsRunning(self):
        return self.running
        
    def Run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost',self.app.port))
        sock.listen(5)
        try:
            while self.keepGoing:
                newSocket, address = sock.accept()
                while True:
                    receivedData = newSocket.recv(8192)
                    if not receivedData: break
                    # Post a wxPython event with the unpickled data
                    pickledstring = StringIO.StringIO(receivedData)
                    unpickled = cPickle.load(pickledstring)
                    evt = PostArgsEvent(data=unpickled)
                    wx.PostEvent(self.app, evt)
                    newSocket.sendall(receivedData)
                newSocket.close()
        finally:
            sock.close()
        self.running = False
        
class Frame(wx.Frame):
    def createMenuBar(self, menuBarInfo, shortcutList, oldShortcuts, menuBackups=[]):
        '''
        General utility function to create a menu bar of menus
        Input is a list of label/menuInfo tuples
        The function utilizes the createMenu function (defined below)
        '''
        buckups = menuBackups[:]
        menuBackups[:] = []
        index = 0
        self._shortcutBindWindowDict = {}
        menuBar = wx.MenuBar()
        for eachMenuBarInfo in menuBarInfo:
            menuLabel = eachMenuBarInfo[0]
            menuInfo = eachMenuBarInfo[1:]
            menu = self.createMenu(menuInfo, menuLabel, shortcutList, oldShortcuts)
            menuBar.Append(menu, menuLabel)
            if index in buckups:
                menuBackups.append(self.createMenu(menuInfo, menuLabel, shortcutList, oldShortcuts, True))
            index += 1
        return menuBar
    
    def createMenu(self, menuInfo, name='', shortcutList = None, oldShortcuts=None, backup=False):
        menu = wx.Menu()
        if shortcutList is None:
            shortcutList = []
        if oldShortcuts is None:
            oldShortcutNames = []
            oldShortcuts = []
        else:
            try:
                oldShortcutNames, oldShortcutInfos = oldShortcuts
            except ValueError:
                oldShortcutNames = []
                oldShortcuts = []
        for eachMenuInfo in menuInfo:
            # Get the info, fill in missing info with defaults
            nItems = len(eachMenuInfo)
            # Special case: separator
            if eachMenuInfo == '' or nItems == 1:
                menu.AppendSeparator()
                continue
            if nItems > 7:
                raise
            defaults = ('', '', None, '', wx.ITEM_NORMAL, None, self)
            label, shortcut, handler, status, attr, state, bindwindow = eachMenuInfo + defaults[nItems:]
            # Special case: submenu
            if handler is None: #not isinstance(handler, FunctionType):
                submenu = self.createMenu(shortcut, '%s -> %s'% (name, label), shortcutList, oldShortcuts, backup)
                menu.AppendMenu(wx.ID_ANY, label, submenu, status)
                continue
            elif handler == -1:
                submenu = shortcut #self.createMenu(shortcut, '%s -> %s'% (name, label), shortcutList, oldShortcuts, bindwindow)
                menu.AppendMenu(wx.ID_ANY, label, submenu, status)
                continue
            # Get the id and type (normal, checkbox, radio)
            if attr in (wx.ITEM_CHECK, wx.ITEM_RADIO):
                kind = attr
                id = wx.ID_ANY
            elif attr == wx.ITEM_NORMAL:
                kind = attr
                id = wx.ID_ANY
            else:
                kind = wx.ITEM_NORMAL
                id = attr
            # Get the shortcut string
            itemName = '%s -> %s'% (name, label)
            itemName = itemName.replace('&', '')
            try:
                index = oldShortcutNames.index(itemName)
                shortcut = oldShortcutInfos[index][1]
            except ValueError:
                pass
            if shortcut != '' and shortcut not in [item[1] for item in shortcutList]:
                if True:#wx.VERSION > (2, 8):
                    shortcutString = u'\t%s\u00a0' % GetTranslatedShortcut(shortcut)
                else:
                    shortcutString = '\t%s ' % GetTranslatedShortcut(shortcut)
            else:
                shortcutString = ''
            # Append the menu item
            menuItem = menu.Append(id, '%s%s' % (label, shortcutString), status, kind)
            id = menuItem.GetId()
            self.Bind(wx.EVT_MENU, handler, menuItem)
            # Add the accelerator
            if shortcut is not None:
                if not backup and (shortcut == '' or not shortcut[-1].isspace()):
                    shortcutList.append([itemName, shortcut, id])
                try:
                    bindShortcutIdList = self._shortcutBindWindowDict.setdefault(bindwindow, [])
                    bindShortcutIdList.append(id)
                except AttributeError:
                    pass
            # Extra properties (enable/disable, check)
            if state is not None:
                if kind == wx.ITEM_NORMAL:
                    menuItem.Enable(state)
                else:
                    menuItem.Check(state)
        return menu
        
    def BindShortcutsToWindows(self, shortcutInfo, forcewindow=None):
        idDict = dict([(id, shortcut) for itemName, shortcut, id in shortcutInfo])
        forceAccelList = []
        for window, idList in self._shortcutBindWindowDict.items():
            accelList = []
            #~ for label, data in value.items():
                #~ accelString, id = data
                #~ accel = wx.GetAccelFromString('\t'+accelString)
                #~ accelList.append((accel.GetFlags(), accel.GetKeyCode(), id))
            for id in idList:
                try:
                    accelString = idDict[id]
                except KeyError:
                    continue
                #~ index = [z for x,y,z in shortcutInfo].index(id)
                accel = wx.GetAccelFromString('\t'+accelString)
                if accel is not None:
                    accelList.append((accel.GetFlags(), accel.GetKeyCode(), id))
                else:
                    for key in numpadDict:
                        if accelString.endswith(key):
                            break
                    accelString = accelString.replace(key, 'Space')
                    accel = wx.GetAccelFromString('\t'+accelString)
                    accelList.append((accel.GetFlags(), numpadDict[key], id))
            if forcewindow is None:
                accelTable = wx.AcceleratorTable(accelList)
                window.SetAcceleratorTable(accelTable)
            else:
                forceAccelList += accelList
        if forcewindow is not None:
            accelTable = wx.AcceleratorTable(forceAccelList)
            forcewindow.SetAcceleratorTable(accelTable)
        
    def accelListFromMenu(self, menu, accelList):
        for menuItem in menu.GetMenuItems():
            submenu = menuItem.GetSubMenu()
            if submenu is not None:
                self.accelListFromMenu(submenu, accelList)
            else:
                id = menuItem.GetId()
                text = menuItem.GetText()
                accel = wx.GetAccelFromString(text)
                if accel is not None:
                    accelList.append((accel.GetFlags(), accel.GetKeyCode(), id))
                    
    def createButton(self, parent, label='', id=wx.ID_ANY, handler=None, pos=(0,0)):
        button = wx.Button(parent, id, label, pos)
        if handler:
            #~ self.Bind(wx.EVT_BUTTON, handler, button)
            button.Bind(wx.EVT_BUTTON, handler)
        return button
        
    def createToolbarButton(self, parent, label, handler, pos=(0, 0), size=wx.DefaultSize, style=wx.NO_BORDER, toolTipTxt=None, statusTxt=None):
        # Return a static line if empty
        if type(label) == type('') and label == '':
            return wx.StaticLine(parent, style=wx.LI_VERTICAL)
        # Create the button
        try: # label is a bitmap
            w,h = label.GetSize()
            button = wxButtons.GenBitmapButton(parent, wx.ID_ANY, label, pos, size, style)
            button.SetBestSize((w+7, h+7))
        except AttributeError: # label is a string
            button = wxButtons.GenButton(parent, wx.ID_ANY, label, pos, size, style)
        # Bind the button to the given handler
        #~ self.Bind(wx.EVT_BUTTON, handler, button)
        button.Bind(wx.EVT_BUTTON, handler)
        # Set the tool tip string if given
        if toolTipTxt:
            button.SetToolTipString(toolTipTxt)
        # Define mouse event functions (change status bar text and button bevel width)
        def OnMouseMove(event):
            if statusTxt:
                self.SetStatusText(statusTxt)
        def OnMouseOver(event):
            if statusTxt:
                self.SetStatusText(statusTxt)
            b = event.GetEventObject()
            b.SetBezelWidth(b.GetBezelWidth()+1)
            b.Refresh()
        def OnMouseLeave(event):
            if statusTxt:
                try:
                    self.ResetStatusText()
                except AttributeError:
                    self.SetStatusText('')
            b = event.GetEventObject()
            b.SetBezelWidth(b.GetBezelWidth()-1)
            b.Refresh()
        button.Bind(wx.EVT_ENTER_WINDOW, OnMouseOver)
        button.Bind(wx.EVT_MOTION, OnMouseMove)
        button.Bind(wx.EVT_LEAVE_WINDOW, OnMouseLeave)
        return button
        
class OptionsDialog(wx.Dialog):
    def __init__(self, parent, dlgInfo, options, title=_('Program Settings'), startPageIndex=0):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title)
        self.options = options.copy()
        self.optionsOriginal = options
        # Create the options tabs
        self.controls = {}
        nb = self.nb = wx.Notebook(self, wx.ID_ANY, style=wx.NO_BORDER)
        for tabInfo in dlgInfo:
            tabPanel = wx.Panel(nb, wx.ID_ANY)
            nb.AddPage(tabPanel, tabInfo[0], select=True)
            def OnNotebookPageChanged(event):
                event.GetEventObject().GetCurrentPage().SetFocus()
                event.Skip()
            self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, OnNotebookPageChanged)
            tabSizer = wx.BoxSizer(wx.VERTICAL)
            boolStar = False
            for label, flag, key, tip, misc in tabInfo[1:]:
                try:
                    optionsValue = self.options[key]
                    if optionsValue is None:
                        optionsValue = ''
                except KeyError:
                    optionsValue = ''
                if flag is None:
                    itemSizer.Add((-1,10), 0)
                elif flag in (OPT_ELEM_FILE, OPT_ELEM_FILE_URL):
                    browseCtrl = filebrowse.FileBrowseButton(tabPanel, wx.ID_ANY, size=(400,-1),
                        labelText=label,
                        toolTip=tip,
                        initialValue=optionsValue,
                        fileMask=misc,
                        buttonText = _('Browse'),
                    )
                    ctrl = browseCtrl.textControl
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    itemSizer.Add(browseCtrl, 1, wx.EXPAND)
                elif flag in (OPT_ELEM_DIR, OPT_ELEM_DIR_URL):
                    browseCtrl = filebrowse.DirBrowseButton(tabPanel, wx.ID_ANY, size=(400,-1),
                        labelText=label,
                        toolTip=tip,
                        startDirectory=optionsValue,
                        buttonText = _('Browse'),
                    )
                    browseCtrl.SetValue(optionsValue)
                    ctrl = browseCtrl.textControl
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    itemSizer.Add(browseCtrl, 1, wx.EXPAND)
                elif flag == OPT_ELEM_COLOR:
                    staticText = wx.StaticText(tabPanel, wx.ID_ANY, label)
                    ctrl = colourselect.ColourSelect(tabPanel, wx.ID_ANY, colour=wx.Colour(*optionsValue), size=(50,23))
                    if tip:
                        ctrl.SetToolTipString(tip)
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    itemSizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
                    itemSizer.Add(ctrl, 0)
                elif flag == OPT_ELEM_FONT:
                    #~ staticText = wx.StaticText(tabPanel, wx.ID_ANY, label)
                    ctrl = wxButtons.GenButton(tabPanel, wx.ID_ANY, label=label)
                    ctrl.SetUseFocusIndicator(False)
                    self.Bind(wx.EVT_BUTTON, self.OnButtonFont, ctrl)
                    fontFace, fontSize, fontWeight, fontStyle, fontColorTuple = optionsValue
                    weight = wx.FONTWEIGHT_NORMAL
                    if fontWeight == 'bold':
                        weight = wx.FONTWEIGHT_BOLD
                    style = wx.FONTSTYLE_NORMAL
                    if fontStyle == 'italic':
                        style = wx.FONTSTYLE_ITALIC
                    font = wx.Font(fontSize, wx.FONTFAMILY_DEFAULT, style, weight, faceName=fontFace)
                    ctrl.SetFont(font)
                    ctrl.SetForegroundColour(wx.Colour(*fontColorTuple))
                    if tip:
                        ctrl.SetToolTipString(tip)
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    #~ itemSizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
                    itemSizer.Add(ctrl, 0)
                elif flag == OPT_ELEM_INT:
                    staticText = wx.StaticText(tabPanel, wx.ID_ANY, label)
                    ctrl = wx.TextCtrl(tabPanel, wx.ID_ANY, value=str(optionsValue), size=(50,-1))
                    if tip:
                        staticText.SetToolTipString(tip)
                        ctrl.SetToolTipString(tip)
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    itemSizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
                    itemSizer.Add(ctrl, 0)
                elif flag == OPT_ELEM_CHECK:
                    ctrl = wx.CheckBox(tabPanel, wx.ID_ANY, label)
                    ctrl.SetValue(optionsValue)
                    if tip:
                        ctrl.SetToolTipString(tip)
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    border = 2
                    if type(misc) == int:
                        itemSizer.Add((misc, -1), 0)
                        border = 0
                    itemSizer.Add(ctrl, 0, wx.ALL, border)
                elif flag == OPT_ELEM_RADIO:
                    choices = [s for s,v in misc]
                    ctrl = wx.RadioBox(tabPanel, wx.ID_ANY, label=label, choices=choices, style=wx.RA_SPECIFY_ROWS, majorDimension=1)
                    ctrl.items = misc
                    ctrl.SetSelection(0)
                    for s, v in misc:
                        if v == optionsValue:
                            ctrl.SetStringSelection(s)
                            break
                    if tip:
                        ctrl.SetToolTipString(tip)
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    itemSizer.Add(ctrl, 0)
                elif flag == OPT_ELEM_BUTTON:
                    #~ staticText = wx.StaticText(tabPanel, wx.ID_ANY, label)
                    #~ ctrl = wxButtons.GenButton(tabPanel, wx.ID_ANY, label=label)
                    ctrl = wx.Button(tabPanel, wx.ID_ANY, label=label)
                    #~ ctrl.SetUseFocusIndicator(False)
                    handler = misc
                    self.Bind(wx.EVT_BUTTON, handler, ctrl)
                    if tip:
                        ctrl.SetToolTipString(tip)
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    #~ itemSizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
                    itemSizer.Add(ctrl, 0, wx.TOP|wx.BOTTOM, 5)
                else: #elif flag == OPT_ELEM_STRING:
                    staticText = wx.StaticText(tabPanel, wx.ID_ANY, label)
                    ctrl = wx.TextCtrl(tabPanel, wx.ID_ANY, value=optionsValue)
                    if tip:
                        staticText.SetToolTipString(tip)
                        ctrl.SetToolTipString(tip)
                    itemSizer = wx.BoxSizer(wx.HORIZONTAL)
                    itemSizer.Add(staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
                    itemSizer.Add(ctrl, 1, wx.EXPAND|wx.BOTTOM, 5)
                #~ if label.startswith('*'):
                if label.rstrip(' :').endswith('*'):
                    boolStar = True
                tabSizer.Add(itemSizer, 0, wx.EXPAND|wx.ALL, 5)
                self.controls[key] = (ctrl, flag, nb.GetSelection())
            if boolStar:
                tabSizer.Add((0,0),1)
                tabSizer.Add(wx.StaticText(tabPanel, wx.ID_ANY, '    '+_('* Requires program restart for full effect')), 0, wx.TOP, 20)
            tabSizerBorder = wx.BoxSizer()
            tabSizerBorder.Add(tabSizer, 1, wx.EXPAND|wx.ALL, 5)
            tabPanel.SetSizer(tabSizerBorder)
            tabSizerBorder.Layout()
        if startPageIndex >=0 and startPageIndex < nb.GetPageCount():
            nb.SetSelection(startPageIndex)
        else:
            nb.SetSelection(0)
        # Standard buttons
        okay = wx.Button(self, wx.ID_OK, _('OK'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, okay)
        cancel = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Size the elements
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(nb, 0, wx.EXPAND|wx.ALL, 5)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizer(dlgSizer)
        dlgSizer.Fit(self)
        self.sizer = dlgSizer
        # Misc
        okay.SetDefault()
        
    def OnButtonOK(self, event):
        if self.UpdateDict():
            event.Skip()
            
    def OnButtonFont(self, event):
        button = event.GetEventObject()
        font = button.GetFont()
        colour = button.GetForegroundColour()
        # Show the font dialog
        data = wx.FontData()
        data.EnableEffects(False)
        #~ data.SetColour(button.GetForegroundColour())
        data.SetInitialFont(font)
        dlg = wx.FontDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
        # Show the color dialog
        data = wx.ColourData()
        data.SetColour(colour)
        dlg2 = wx.ColourDialog(self, data)
        dlg2.GetColourData().SetChooseFull(True)
        if dlg2.ShowModal() == wx.ID_OK:
            data = dlg2.GetColourData()
            colour = data.GetColour()
        button.SetFont(font)
        button.SetForegroundColour(colour)
        button.SetBestSize()
        button.Refresh()
        self.sizer.Fit(self)
        dlg2.Destroy()
        dlg.Destroy()
        
    
    def GetDict(self):
        return self.options
        
    def UpdateDict(self):
        for key, value in self.controls.items():
            ctrl, flag, tabIndex = value
            if flag in (OPT_ELEM_DIR, OPT_ELEM_DIR_URL):
                entry = ctrl.GetValue()
                if entry == '' or os.path.isdir(entry):
                    newValue = entry
                elif flag == OPT_ELEM_DIR_URL and entry.lstrip().startswith('http://'):
                    newValue = entry
                else:
                    self.ShowWarning(ctrl, _('Invalid directory!'), tabIndex)
                    return False
            elif flag in (OPT_ELEM_FILE, OPT_ELEM_FILE_URL):
                entry = ctrl.GetValue()
                if entry == '' or os.path.isfile(entry):
                    newValue = entry
                elif flag == OPT_ELEM_FILE_URL and entry.lstrip().startswith('http://'):
                    newValue = entry
                else:
                    self.ShowWarning(ctrl, _('Invalid filename!'), tabIndex)
                    return False
            elif flag == OPT_ELEM_COLOR:
                #~ newValue = ctrl.GetBackgroundColour().Get()
                newValue = ctrl.GetColour().Get()
            elif flag == OPT_ELEM_FONT:
                font = ctrl.GetFont()
                bold = ''
                if font.GetWeight() == wx.FONTWEIGHT_BOLD:
                    bold = 'bold'
                italic = ''
                if font.GetStyle() == wx.FONTSTYLE_ITALIC:
                    italic = 'italic'
                color = ctrl.GetForegroundColour()
                newValue = (font.GetFaceName(), font.GetPointSize(), bold, italic, color.Get())
            elif flag == OPT_ELEM_INT:
                entry = ctrl.GetValue()
                try:
                    newValue = int(entry)
                except ValueError:
                    self.ShowWarning(ctrl, _('Value must be an integer!'), tabIndex)
                    return False
            elif flag == OPT_ELEM_CHECK:
                newValue = ctrl.GetValue()
            elif flag == OPT_ELEM_RADIO:
                index = ctrl.GetSelection()
                newValue = ctrl.items[index][1]
            elif flag == OPT_ELEM_BUTTON:
                newValue = self.optionsOriginal[key]
            else: # flag == OPT_ELEM_STRING:
                newValue = ctrl.GetValue()
            self.options[key] = newValue
        return True
        
    def ShowWarning(self, ctrl, message, tabIndex):
        self.nb.SetSelection(tabIndex)
        color = ctrl.GetBackgroundColour()
        ctrl.SetBackgroundColour('pink')
        ctrl.Refresh()
        wx.MessageBox(message, 'Error')
        ctrl.SetBackgroundColour(color)
        ctrl.Refresh()
        ctrl.SetFocus()
        
class ShortcutsDialog(wx.Dialog):
    def __init__(self, parent, shortcutList, title=_('Edit shortcuts'), exceptionIds=None, submessage=None):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parent = parent
        self.shortcutList = copy.deepcopy(shortcutList)#shortcutList[:]
        if exceptionIds is None:
            exceptionIds = []
        if type(exceptionIds) is tuple:
            exceptionShortcuts = exceptionIds[0]            
            self.advancedShortcuts = advancedShortcuts = exceptionIds[1]
            self.reservedShortcuts = reservedShortcuts = exceptionIds[2][:]
            self.advancedInfo = exceptionIds[3]
            advanced = wx.Button(self, wx.ID_ANY, _('Advanced'))
            advanced.Bind(wx.EVT_BUTTON, self.OnAdvancedButton)
        else:
            advanced = None
        # Define the shortcut editing modal dialog (used later)
        self.dlgEdit = self.defineShortcutEditDialog()
        # Define the virtual list control
        class VListCtrl(ListCtrl):                
            def OnGetItemText(self, item, column):
                label, shortcut, id = self.parent.shortcutList[item]
                if column == 0:
                    if advanced:
                        if shortcut in exceptionShortcuts:
                            label = '* %s' % label
                        elif shortcut in reservedShortcuts:
                            if (label, shortcut) in advancedShortcuts[-1]:
                                label = '~ %s' % label
                            else:
                                label = '* %s' % label
                    elif id in exceptionIds:
                        label = '* %s' % label
                    return label
                elif column == 1:
                    return GetTranslatedShortcut(shortcut)
                #~ return self.parent.shortcutList[item][column]
        listCtrl = VListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES)
        listCtrl.InsertColumn(0, _('Menu label'))
        listCtrl.InsertColumn(1, _('Keyboard shortcut'))
        nItems = len(self.shortcutList)
        listCtrl.SetItemCount(nItems)
        listCtrl.setResizeColumn(1)
        listCtrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)        
        listCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListCtrlActivated)
        self.listCtrl = listCtrl
        # Standard buttons
        okay  = wx.Button(self, wx.ID_OK, _('OK'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, okay)
        cancel = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, cancel)
        btns = wx.StdDialogButtonSizer()
        if advanced:
            btns.Add(advanced)
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Size the elements
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(listCtrl, 1, wx.EXPAND|wx.ALL, 5)
        if submessage is not None:
            dlgSizer.Add(wx.StaticText(self, wx.ID_ANY, submessage), 0, wx.ALIGN_LEFT|wx.LEFT|wx.BOTTOM, 10)
        message = _('Double-click or hit enter on an item in the list to edit the shortcut.')
        dlgSizer.Add(wx.StaticText(self, wx.ID_ANY, message), 0, wx.ALIGN_CENTER|wx.ALL, 5)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizerAndFit(dlgSizer)
        width, height = self.GetSize()
        self.SetSize((width, height*2))
        self.sizer = dlgSizer
        # Misc
        #okay.SetDefault()
        # explictly destroy self.dlgEdit as self.OnButtonOK does
        self.Bind(wx.EVT_CLOSE, self.OnButtonClick)
        
    def OnAdvancedButton(self, event):
        dlg = wx.Dialog(self, wx.ID_ANY, _('Advanced'), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        class CheckListCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin):
            def __init__(self, parent):
                wx.ListCtrl.__init__(self, parent, wx.ID_ANY, style=wx.LC_REPORT)
                listmix.CheckListCtrlMixin.__init__(self, checked_icon.GetBitmap(), unchecked_icon.GetBitmap())
        checklist = CheckListCtrl(dlg)
        checklist.InsertColumn(0, _('Shortcut'))
        checklist.InsertColumn(1, _('Action'))
        for index in range(0, len(self.advancedShortcuts)-1):
            shortcut, action = self.advancedShortcuts[index]
            checklist.InsertStringItem(index, shortcut) 
            checklist.SetStringItem(index, 1, action)
            if index % 2:
                checklist.SetItemBackgroundColour(index, '#E8E8FF')
            if shortcut in self.reservedShortcuts:
                checklist.CheckItem(index)
        checklist.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        checklist.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        # Standard buttons
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Dialog layout
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(checklist, 1, wx.EXPAND|wx.ALL, 5)
        if self.advancedInfo:
            dlgSizer.Add(wx.StaticText(dlg, wx.ID_ANY, self.advancedInfo), 0, wx.LEFT|wx.BOTTOM, 10)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 10)
        dlg.SetSizerAndFit(dlgSizer)
        width = checklist.GetColumnWidth(0) + checklist.GetColumnWidth(1) + 40
        dlg.SetSize((width, width*3/4))
        if wx.ID_OK == dlg.ShowModal():
            while self.reservedShortcuts:
                self.reservedShortcuts.pop()
            for index in range(0, len(self.advancedShortcuts)-1):
                if checklist.IsChecked(index):
                    self.reservedShortcuts.append(self.advancedShortcuts[index][0])
            self.listCtrl.RefreshItems(0, len(self.shortcutList)-1)
        dlg.Destroy()
        
    def GetShortcutList(self):
        return self.shortcutList, self.reservedShortcuts
        
    def defineShortcutEditDialog(self):
        dlg = wx.Dialog(self, wx.ID_ANY, _('Edit the keyboard shortcut'))
        # Menu string label
        dlg.menuLabel = wx.StaticText(dlg, wx.ID_ANY, '')
        # Main controls
        dlg.checkBoxCtrl = wx.CheckBox(dlg, wx.ID_ANY, _('Ctrl'))
        dlg.checkBoxAlt = wx.CheckBox(dlg, wx.ID_ANY, _('Alt'))
        dlg.checkBoxShift = wx.CheckBox(dlg, wx.ID_ANY, _('Shift'))
        dlg.listBoxKey = wx.Choice(dlg, wx.ID_ANY, choices=keyStringList)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(dlg.checkBoxCtrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 15)
        sizer.Add(dlg.checkBoxAlt, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 15)
        sizer.Add(dlg.checkBoxShift, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 15)
        sizer.Add(wx.StaticText(dlg, wx.ID_ANY, _('Key:')), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sizer.Add(dlg.listBoxKey, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 15)
        # Standard buttons
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        dlg.Bind(wx.EVT_BUTTON, self.OnEditButtonOK, okay)
        clear = wx.Button(dlg, wx.ID_NO, _('Clear'))
        dlg.Bind(wx.EVT_BUTTON, self.OnEditButtonClear, clear)
        cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.AddButton(clear)
        btns.Realize()
        # Size the elements
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(dlg.menuLabel, 0, wx.TOP|wx.LEFT, 10)
        dlgSizer.Add(sizer, 0, wx.EXPAND|wx.ALL, 15)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 10)
        dlg.SetSizer(dlgSizer)
        dlgSizer.Fit(dlg)
        # Misc
        okay.SetDefault()
        return dlg
        
    def OnListCtrlActivated(self, event):
        dlg = self.dlgEdit
        index = event.GetIndex()
        dlg.listIndex = index
        label, shortcut, id = self.shortcutList[index]
        dlg.menuLabel.SetLabel(label)
        if shortcut == '':
            dlg.checkBoxCtrl.SetValue(False)
            dlg.checkBoxAlt.SetValue(False)
            dlg.checkBoxShift.SetValue(False)
            dlg.listBoxKey.SetSelection(wx.NOT_FOUND)
        else:
            items = [s.upper() for s in shortcut.split('+')]
            if not items[-1]:
                del items[-1]
                items[-1] += '+'                
            boolCtrl = False
            boolAlt = False
            boolShift = False
            if 'CTRL' in items:
                boolCtrl = True
            if 'ALT' in items:
                boolAlt = True
            if 'SHIFT' in items:
                boolShift = True
            if len(items) == 1:
                keyString = items[0]
            else:
                keyString = items[-1]
            dlg.checkBoxCtrl.SetValue(boolCtrl)
            dlg.checkBoxAlt.SetValue(boolAlt)
            dlg.checkBoxShift.SetValue(boolShift)
            if not dlg.listBoxKey.SetStringSelection(keyString):
                print>>sys.stderr, _('%(keyString)s not found in key string list') % locals()
        ID = dlg.ShowModal()
        # Set the data
        if ID == wx.ID_OK:
            pass
            #~ self.options = dlg.GetDict()
        #~ dlg.Destroy()
        
    def OnEditButtonOK(self, event):
        # Get the values from the dialog
        dlg = self.dlgEdit
        boolCtrl = dlg.checkBoxCtrl.GetValue()
        boolAlt = dlg.checkBoxAlt.GetValue()
        boolShift = dlg.checkBoxShift.GetValue()
        keyString = dlg.listBoxKey.GetStringSelection()
        # Check basic invalid cases
        if keyString == '':
            wx.MessageBox(_('You must specify a key!'), _('Error'), style=wx.ICON_ERROR)
            return
        #~ if (len(keyString) == 1 or keyString in ('Home', 'End', 'PgUp', 'PgDn', 'Up', 'Down', 'Left', 'Right')) and (not boolCtrl and not boolAlt and not boolShift):
        #~ if (len(keyString) == 1) and (not boolCtrl and not boolAlt and not boolShift):
            #~ wx.MessageBox(_('You must check at least one modifier!'), _('Error'), style=wx.ICON_ERROR)
            #~ return
        # Build the shortcut string
        shortcut = ''
        if boolCtrl:
            shortcut += 'Ctrl+'
        if boolAlt:
            shortcut += 'Alt+'
        if boolShift:
            shortcut += 'Shift+'
        shortcut += keyString
        # Check if keyboard shortcut already exists
        oldShortcut = self.shortcutList[dlg.listIndex][1]
        shortcutUpper = shortcut.upper()
        if shortcutUpper != oldShortcut.upper():
            #~ if shortcutUpper in [info[1].upper() for info in self.shortcutList]:
            for info in self.shortcutList:
                if shortcutUpper == info[1].upper():
                    line1 = _('This shortcut is being used by:')
                    line2 = info[0]
                    line3 = _('Do you wish to continue?')
                    ret = wx.MessageBox('%s\n\n%s\n\n%s' % (line1, line2 , line3), _('Warning'),
                                        wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION, dlg)
                    if ret == wx.OK:
                        info[1] = ''
                        #~ self.updateMenuLabel(info[2], '')
                    else:
                        return
                    break
            self.shortcutList[dlg.listIndex][1] = shortcut
            #~ self.updateMenuLabel(self.shortcutList[dlg.listIndex][2], shortcut)
            self.listCtrl.Refresh()
        event.Skip()
        
    def OnEditButtonClear(self, event):
        dlg = self.dlgEdit
        msgDlg = wx.MessageDialog(self, _('Are you sure you want to clear this shortcut?'), _('Warning'))
        ID = msgDlg.ShowModal()
        msgDlg.Destroy()
        if ID == wx.ID_OK:
            self.shortcutList[dlg.listIndex][1] = ''
            dlg.EndModal(wx.ID_NO)
            self.listCtrl.Refresh()
        else:
            dlg.EndModal(wx.ID_CANCEL)
        
    def _x_updateMenuLabel(self, id, shortcut):
        menuItem = self.parent.GetMenuBar().FindItemById(id)
        label = menuItem.GetLabel()
        newLabel = '%s\t%s' % (label, shortcut)
        menuItem.SetText(newLabel)
        
    def OnButtonClick(self, event):
        self.dlgEdit.Destroy()
        if event.GetEventType() == wx.wxEVT_CLOSE_WINDOW:
            self.EndModal(wx.ID_CANCEL)
        else:
            event.Skip()
        
class EditStringDictDialog(wx.Dialog):
    def __init__(self, parent, infoDict, title='Edit', keyTitle='Key', valueTitle='Value', editable=False, insertable=False, about='', keyChecker=None, valueChecker=None):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title, size=(500, 300), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.infoDict = infoDict.copy()
        self.keyTitle = keyTitle
        self.valueTitle = valueTitle
        self.keyChecker = keyChecker
        self.valueChecker = valueChecker
        self.previousKey = None
        self.editName = ''
        self.textChanged = False
        # Create the key and value static text labels
        keyLabel = wx.StaticText(self, wx.ID_ANY, keyTitle)
        valueLabel = wx.StaticText(self, wx.ID_ANY, valueTitle)
        # Create the list control using the dictionary
        style = wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_SORT_ASCENDING|wx.LC_SINGLE_SEL
        if editable:
            style |= wx.LC_EDIT_LABELS
        self.listCtrl = ListCtrl(self, wx.ID_ANY, style=style)
        self.listCtrl.InsertColumn(0, 'Column 0')
        for row, key in enumerate(self.infoDict.keys()):
            self.listCtrl.InsertStringItem(row, key)
        self.listCtrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        self.listCtrl.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnListItemEdit)
        self.listCtrl.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnListItemEdited)
        # Create the text control
        self.textCtrl = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE|wx.HSCROLL)
        self.textCtrl.Bind(wx.EVT_TEXT, self.OnValueTextChanged)
        # Create the insert/delete buttons
        if insertable:
            insertButton = wx.Button(self, wx.ID_ANY, _('Insert'))
            self.Bind(wx.EVT_BUTTON, self.OnButtonInsert, insertButton)
            deleteButton = wx.Button(self, wx.ID_ANY, _('Delete'))
            self.Bind(wx.EVT_BUTTON, self.OnButtonDelete, deleteButton)
            insSizer = wx.BoxSizer(wx.HORIZONTAL)
            insSizer.Add(insertButton, 1, wx.ALIGN_CENTER|wx.ALL, 5)
            insSizer.Add(deleteButton, 1, wx.ALIGN_CENTER|wx.ALL, 5)
        # Standard buttons
        okay  = wx.Button(self, wx.ID_OK, _('OK'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, okay)
        cancel = wx.Button(self, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Size the elements
        gridSizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=5)
        gridSizer.AddGrowableCol(1, 1)
        gridSizer.AddGrowableRow(1)
        gridSizer.Add(keyLabel, 0)
        gridSizer.Add(valueLabel, 0, wx.ALIGN_CENTER)
        gridSizer.Add(self.listCtrl, 2, wx.EXPAND|wx.RIGHT, 10)
        gridSizer.Add(self.textCtrl, 3, wx.EXPAND)
        minWidth = max(self.listCtrl.GetColumnWidth(0), keyLabel.GetSize()[0])
        gridSizer.SetItemMinSize(self.listCtrl, min(minWidth+20, 250), 20)
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(gridSizer, 1, wx.EXPAND|wx.ALL, 10)
        if insertable:
            dlgSizer.Add(insSizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.BOTTOM, 15)
        if about:
            dlgSizer.Add(wx.StaticText(self, wx.ID_ANY, about), 0, wx.ALIGN_CENTER|wx.BOTTOM, 10)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(dlgSizer)
        # Misc
        self.listCtrl.SelectItem(0)
        okay.SetDefault()
        
    def GetDict(self):
        return self.infoDict
        
    def UpdateDictEntry(self):
        if self.infoDict.has_key(self.previousKey) and self.textChanged:
            self.infoDict[self.previousKey] = self.textCtrl.GetValue()
        
    def OnValueTextChanged(self, event):
        self.textChanged = True
        
    def OnListItemSelected(self, event):
        # Update the previously selected key
        self.UpdateDictEntry()
        # Display the value associated with the selected key
        key = event.GetText()
        value = self.infoDict.get(key)
        if value is not None:
            self.textCtrl.Replace(0, -1, value)
            self.textCtrl.SetInsertionPoint(0)
            self.textChanged = False
        else:
            print>>sys.stderr, _('Error: key %(key)s does not exist!') % locals()
        self.previousKey = key
            
    def OnListItemEdit(self, event):
        self.editName = event.GetText()
        
    def OnListItemEdited(self, event):
        if event.IsEditCancelled():
            return
        newName = event.GetLabel()
        if newName.lower() != self.editName.lower():
            oldName = self.editName
            dlg = wx.MessageDialog(self, _('Are you sure you want to rename from %(oldName)s to %(newName)s?') % locals(), _('Question'))
            ID = dlg.ShowModal()
            dlg.Destroy()
            if ID != wx.ID_OK:
                event.Veto()
                return
        # "Rename" the key in the dictionary
        del self.infoDict[self.editName]
        self.infoDict[newName] = self.textCtrl.GetValue()
        
    def OnButtonInsert(self, event):
        dlg = wx.Dialog(self, wx.ID_ANY, _('Insert a new item'))
        sizer = wx.BoxSizer(wx.VERTICAL)
        keyTextCtrl = wx.TextCtrl(dlg, wx.ID_ANY)
        valueTextCtrl = wx.TextCtrl(dlg, wx.ID_ANY, style=wx.TE_MULTILINE|wx.HSCROLL)
        sizer.Add(wx.StaticText(dlg, wx.ID_ANY, self.keyTitle.strip()), 0, wx.EXPAND)
        sizer.Add(keyTextCtrl, 0, wx.EXPAND|wx.BOTTOM, 10)
        sizer.Add(wx.StaticText(dlg, wx.ID_ANY, self.valueTitle.strip()), 0, wx.EXPAND)
        sizer.Add(valueTextCtrl, 1, wx.EXPAND|wx.BOTTOM, 10)
        # Standard buttons
        okay  = wx.Button(dlg, wx.ID_OK, _('OK'))
        cancel = wx.Button(dlg, wx.ID_CANCEL, _('Cancel'))
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        # Size the elements
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(sizer, 1, wx.EXPAND|wx.ALL, 10)
        dlgSizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        dlg.SetSizer(dlgSizer)
        # Show the dialog
        ID = dlg.ShowModal()
        newKey = keyTextCtrl.GetValue()
        newValue = valueTextCtrl.GetValue()
        dlg.Destroy()
        # Add the new item to the dictionary as well as the listCtrl
        if ID == wx.ID_OK:
            if not newKey:
                wx.MessageBox(_('Must enter a name!'), _('Error'), style=wx.ICON_ERROR)
                return
            if self.infoDict.has_key(newKey):
                wx.MessageBox(_('Item %(newKey)s already exists!') % locals(), _('Error'), style=wx.ICON_ERROR)
                return
            if self.keyChecker:
                msg = self.keyChecker(newKey)
                if msg is not None:
                    wx.MessageBox(msg, _('Error'), style=wx.ICON_ERROR)
                    return
            if self.valueChecker:
                msg = self.valueChecker(newValue)
                if msg is not None:
                    wx.MessageBox(msg, _('Error'), style=wx.ICON_ERROR)
                    return
            self.infoDict[newKey] = newValue
            self.listCtrl.InsertStringItem(0, newKey)
            self.listCtrl.SelectLabel(newKey)
            if newValue == '':
                wx.MessageBox(_('Warning: no value entered for item %(newKey)s!') % locals(), _('Warning'))
                self.textCtrl.SetFocus()
        
    def OnButtonDelete(self, event):
        index = self.listCtrl.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
        if index == -1:
            wx.MessageBox(_('Select an item to delete first'), _('Message'))
            return
        key = self.listCtrl.GetItemText(index)
        dlg = wx.MessageDialog(self, _('Are you sure you want to delete item %(key)s?') % locals(), _('Question'))
        ID = dlg.ShowModal()
        if ID == wx.ID_OK:
            del self.infoDict[key]
            self.listCtrl.DeleteItem(index)
            if index - 1 < 0:
                self.listCtrl.SelectItem(0)
            else:
                self.listCtrl.SelectItem(index-1)
        dlg.Destroy()
        
        
    def OnButtonOK(self, event):
        # Update the previously selected key
        self.UpdateDictEntry()
        event.Skip()
        
class Slider(wx.Slider):
    def __init__(self, parent, id=wx.ID_ANY, 
            value=0, minValue=0, maxValue=100,
            point=wx.DefaultPosition, size=wx.DefaultSize,
            style=wx.SL_HORIZONTAL, validator=wx.DefaultValidator,
            name="slider", nDecimal=0, mod=None, onscroll=None):
        # Class variables
        self.parent = parent
        self.onscroll = onscroll
        self.wxMaxValueLimit = 10000
        # User slider values
        self.uValue = value
        self.uMinValue = minValue
        self.uMaxValue = maxValue
        if mod is not None:
            if mod > maxValue - minValue:
                mod = None
            else:
                minValue = minValue + minValue % mod
                maxValue = maxValue - maxValue % mod
                if mod > maxValue - minValue:
                    mod = None
                else:
                    nDecimal = 0
                    self.uMinValue = minValue
                    self.uMaxValue = maxValue
                    self.uValue = min(value + value % mod, maxValue)
        self.uSelStart = 0
        self.uSelEnd = 0
        self.nDecimal = nDecimal
        # Determine the internal slider range (0 to wxMaxValue)
        self.wxMaxValue = self._get_wxMaxValue(minValue, maxValue, nDecimal, mod)
        # Create the slider control
        aValue = self._upos2wxpos(value)
        aMaxValue = self._upos2wxpos(maxValue)
        wx.Slider.__init__(self, parent, id,
            aValue, 0, self.wxMaxValue,
            point=point, size=size, style=style,
            validator=validator, name=name
        )
        self.name = self.GetName()
        # Event binding
        #EVT_SCROLL_ENDSCROLL(self,self.OnSliderChanged)
        self.Bind(wx.EVT_SCROLL, self._OnSliderChanging)
        #~ super(Slider, self).Bind(wx.EVT_SCROLL, self._OnSliderChanged)
        
    def _get_wxMaxValue(self, uMinValue, uMaxValue, nDecimal, mod):
        if mod is None:
            step = 1/float(10**nDecimal)
        else:
            step = mod
        wxMaxValue = (uMaxValue - uMinValue) / step
        wxMaxValue = int(round(wxMaxValue))
        if wxMaxValue >= self.wxMaxValueLimit:
            wxMaxValue = self.wxMaxValueLimit
        return wxMaxValue
        
    def _upos2wxpos(self, upos):
        ''' Converts user pos to actual wxSlider pos '''
        wxpos = self.wxMaxValue * (upos - self.uMinValue) / float(self.uMaxValue - self.uMinValue)
        return int(round(wxpos))
    
    def _wxpos2upos(self, wxpos):
        ''' Converts actual wxSlider pos to user pos '''
        upos = self.uMinValue + (self.uMaxValue - self.uMinValue) * wxpos / float(self.wxMaxValue)
        if self.nDecimal == 0:
            upos = int(round(upos))
        #~ else:
            #~ upos = round(upos, 4)
        return upos
        
    def _OnSliderChanging(self, event):
        self.uValue = self._wxpos2upos(super(Slider, self).GetValue())
        if self.onscroll:
        #~ if False:
            self.onscroll(event)
        event.Skip()
        
    def GetValue(self):
        #~ self.uValue = self._wxpos2upos(super(Slider, self).GetValue())
        return self.uValue
        
    def GetValueAsString(self):
        strTemplate = '%.'+str(self.nDecimal)+'f'
        return strTemplate % self.uValue
        
    def GetMin(self):
        return self.uMinValue
        
    def GetMax(self):
        return self.uMaxValue
        
    def _GetSelStart(self):
        return self.uSelStart
        
    def _GetSelEnd(self):
        return self.uSelEnd
        
    def _GetLineSize(self):
        pass
        
    def _GetPageSize(self):
        pass
        
    def _GetThumbLength(self):
        pass
        
    def _GetTickFreq(self):
        pass
        
    def SetValue(self, value):
        if self.nDecimal == 0:
            value = int(round(value))
        self.uValue = value
        super(Slider, self).SetValue(self._upos2wxpos(value))
        #~ self.uValue = self._wxpos2upos(super(Slider, self).GetValue())
        
    def SetRange(self, minValue, maxValue, nDecimal=None, mod=None):
        if minValue >= maxValue:
            if minValue == 0 and (maxValue == -1 or maxValue ==0):
                maxValue = 1
            else:
                print>>sys.stderr, _('Error: minValue must be less than maxValue')
                return
        self.uMinValue = minValue
        self.uMaxValue = maxValue
        if nDecimal is not None:
            self.nDecimal = nDecimal
        self.wxMaxValue = self._get_wxMaxValue(minValue, maxValue, self.nDecimal, mod)
        super(Slider, self).SetRange(0, self.wxMaxValue)
        
    def SetSelection(self, startPos, endPos):
        self.uSelStart = startPos
        self.uSelEnd = endPos
        super(Slider, self).SetSelection(self._upos2wxpos(startPos), self._upos2wxpos(endFrame))
        
    def Increment(self):
        wxpos = super(Slider, self).GetValue()
        if wxpos < super(Slider, self).GetMax():
            wxpos += 1
            self.uValue = self._wxpos2upos(wxpos)
            super(Slider, self).SetValue(wxpos)
        return self.uValue
        
    def Decrement(self):
        wxpos = super(Slider, self).GetValue()
        if wxpos > super(Slider, self).GetMin():
            wxpos -= 1
            self.uValue = self._wxpos2upos(wxpos)
            super(Slider, self).SetValue(wxpos)
        return self.uValue
            
    def _SetLineSize(self):
        pass
        
    def _SetPageSize(self):
        pass
        
    def _SetThumbLength(self):
        pass
        
    def _SetTickFreq(self):
        pass
        
    def SetTick(self, upos):
        super(Slider, self).SetTick(self._upos2wxpos(upos))
        