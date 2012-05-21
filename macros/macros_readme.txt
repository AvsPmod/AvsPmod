
    AvsP allows you to define your own macros using the Python programming language.  In order to use this functionality, simply write your own Python code in a text file and save it in the "macros" directory with the extension ".py".  The next time you start AvsP.exe, your macro will appear in the "Macros" menu (the macros are sorted alphabetically).  The extension and any initial open-close brackets removed in the displayed name - the file "[001] My Macro.py" shows up in the menu as "My Macro", in order to help order the macros in the menu.  To help further organize your macros, you can put macros in any subdirectories you create in the "macros" folder, which will automatically create submenus in the "Macros" menu.
    You need to have a pretty good understanding of Python to write your own macros (plenty of documentation and tutorials for Python can be found on the web).  Several examples are provided in the "macros" directory to show basic usage, many more things are possible.  The following is a description of the functions provided in the local module avsp to give you control over the program itself (see the examples for appropriate usage).


InsertText(txt, pos=-1, index=None)
===================================
Inserts the string txt into the script of the tab located at the zero-based integer index at the text position pos.  If the input index is None, the text is inserted into the script of the currently selected tab.  The input pos can be either an integer representing the zero-based position in the text document (a value of -1 is equivalent to the last position) or a tuple representing the zero-based line and column numbers (a value of -1 is equivalent to the last line or column, respectively).  Alternatively, if pos is equal to None, the text is inserted at the current cursor position in the document, replacing any existing selection.  In all cases, the cursor is positioned at the end of the inserted text.  Returns False if insert failed (due to bad inputs), True otherwise.


SetText(txt, index=None)
========================
Similar to InsertText, but replaces all the text in the script of the tab located at the zero-based integer index with the string txt.  If the input index is None, the text is inserted into the script of the currently selected tab.  Returns False if the operation failed, True otherwise.


GetText(index=None)
===================
Returns the string containing all the text in the script of the tab located at the zero-based integer index.  If the input index is None, the text is retrieved from the script of the currently selected tab.  Returns False if the operation failed.


GetSelectedText(index=None)
===========================
Similar to GetText(), but returns only the selected text.


GetSourceString(filename='')
============================
Returns an approprate source string based on the file extension of the input string filename.  For example, if filename is "D:\test.avi", the function returns the string "AviSource("D:\test.avi")".  Any unknown extension is wrapped with "DirectShowSource(____)".  Templates can be viewed and defined in the options menu of the program.  If filename is empty, the user is promted to select a file with a dialog box.


GetPluginString(filename='')
============================
This function is similar to GetSourceString(), with 2 primary differences.  The first difference is that it always uses the template "LoadPlugin(____)", with the assumption that filename is an Avisynth plugin dll.  The second difference is that if filename is empty, the open file dialog box displayed always starts in the AviSynth plugin directory for easy selection, whereas the dialog box in the GetSourceString() function always starts in the most recently used directory.


GetFilename(title='Open a script or source')
============================================
Displays an open file dialog box, returning the filename of the selected file if the user clicked "OK", returning an empty string otherwise.


GetSaveFilename(title='Save as')
================================
Displays an save file dialog box, returning the entered filename if the user clicked "OK", returning an empty string otherwise.


GetDirectory(title='Select a directory')
========================================
Displays a dialog box to select a directory, returning the name of the selected directory if the user clicked "OK", returning an empty string otherwise.


GetTextEntry(message, default='', title='Enter information')
============================================================
Displays a dialog box with the string message along with a field for text entry, initially filled with the string default, returning the string from the text entry field if the user clicked "OK", returning an empty string otherwise.  The message argument can optionally be a Python list of strings - in this case, the dialog box will have the appropriate number of text entries, and the function returns the list of entered strings if the user clicks "OK", 
and returns an empty list otherwise.


WriteToScrap(txt, pos=-1)
=========================
This function is identical to InsertText, except that instead of writing to one of the existing tabs, it writes to a scrap window (which is always on top, making it useful to keep track of the text as it changes).  Any inserted text is highlighted temporarily.


GetScrapText()
==============
Identical to the GetText function, except that it retrieves all text from the scrap window.


NewTab()
========
Creates a new tab (automatically named "New File (x)", where x is an appropriate integer).  If any text was selected in the most recent tab, it is automatically copied over to the new tab's text.


CloseTab(index=None, boolPrompt=False)
======================================
Closes the tab at integer index, where an index of 0 indicates the first tab. If index is None (the default), the function will close the currently selected tab.  If the argument boolPrompt is True, the program will prompt the user with a dialog box to save the file if there are any unsaved changes.  If boolPrompt is False, the function will not prompt the user and will close the script without saving any changes.


SelectTab(index=None, inc=0)
============================
Selects the tab located at the integer index, where an index of 0 indicates the first tab.  If the index is None, the integer inc is used instead to determine which tab to select, where inc is an offset from the currently selected tab (negative values for inc are allowable).  Returns False upon failure (invalid input), True otherwise.


GetTabCount()
=============
Returns the number of scripts currently open.


GetCurrentTabIndex()
====================
Returns the zero-based index of the currently selected tab.


GetScriptFilename(index=None)
=============================
Returns the name of the script at the tab located at the integer index, where an index of 0 indicates the first tab.  If index is None, the currently selected tab is used.  The returned name is the filename of the script on the hard drive.  If the script has never been saved to the hard drive, the returned name is an empty string.


OpenFile(filename='')
=====================
If the string filename is a path to an Avisynth script, this function opens the script into a new tab.  If filename is a path to a non-script file, this function inserts the filename as a source (see the InsertSource function for details).  If filename is not supplied, the user is prompted with an Open File dialog box.


SaveScript(filename='', index=None)
===================================
Saves all the unsaved changes of the script in the tab located at the integer index.  If index is None, the script in the currently selected tab is used.  The function will prompt the user with a dialog box for the location to save the file if the string filename is not provided and the script does not already exist on the hard drive.  If a file with the same name as filename already exists, it is overwritten without any prompting.  The function returns the filename of the saved file.


SaveScriptAs(filename='', index=None)
=====================================
Similar to the function SaveScript(), except that if the filename is an empty string, this function will always prompt the user with a dialog box for the location to save the file, regardeless of whether or not the script exists on the hard drive.


IsScriptSaved(index=None)
=========================
Returns a boolean indicating whether the script in the tab located at the integer index has any unsaved changes.  If index is None, the script in the currently selected tab is used.  Returns False if there are any unsaved changes, True otherwise.


ShowVideoFrame(framenum=None, index=None, forceRefresh=False)
=============================================================
This function refreshes the video preview (unhiding it if it is hidden) using the frame specified by the integer framenum, using the script of the tab located at the integer index.  The function also automatically selects the tab located at index.  If framenum is None, it uses the current frame number from the video preview slider.  If index is None, the frame of the currently selected tab is shown.  If the input forceRefresh equals True, then the script is reloaded before showing the video frame (normally the script is reloaded only when the text has changed).


ShowVideoOffset(self, offset=0, units='frames', index=None)
===========================================================
Similar to ShowVideoFrame(), except the user specifies an offset instead of the direct frame.  Offset can be positive or negative (for backwards jumping).  The string argument units specifies the units of the offset, and can be either 'frames', 'seconds', 'minutes', or 'hours'.


UpdateVideo(index=None)
=======================
This function is similar to ShowVideoFrame(), but does not force the video preview to be shown if it is hidden.


HideVideoWindow()
=================
Hides the video preview window if it is visible (note that the video controls are always visible).


GetFrameNumber()
================
Returns the current integer frame number of the video preview slider.


GetVideoWidth(index=None)
=========================
Returns the width of the video of the script at the tab integer index.  If index is None, then the currently selected tab is used.


GetVideoHeight(index=None)
==========================
Returns the height of the video of the script at the tab integer index.  If index is None, then the currently selected tab is used.


GetVideoFramerate(index=None)
=============================
Returns the framerate of the video of the script at the tab integer index.  If index is None, then the currently selected tab is used.


GetVideoFramecount(index=None)
==============================
Returns the framecount of the video of the script at the tab integer index.  If index is None, then the currently selected tab is used.


RunExternalPlayer(executable=None, args='', index=None)
=======================================================
Runs the external program specified by the string argument executable.  The first argument passed to the program is the filename of the preview script generated from the script located at the tab integer index.  If index is None, then the currently selected tab is used.  Additional arguments can be passed to the external program using the string parameter args.  If the specified executable does not exist, then the function returns False, otherwise it runs the executable program with the appropriate arguments and returns True.


SaveImage(filename='', framenum=None, index=None)
=================================================
Saves the video frame specified by the integer framenum as a file specified by the string filename, where the video corresponds with the script at the tab integer index.  If filename is an empty string, then the user is prompted with a dialog box.  If index is None, then the currently selected tab is used.  Returns True if the image was saved, False otherwise.


GetBookmarkList()
=================
Returns a list containing the video frame bookmarks currently set by the user.  Note that these are the standard frame bookmarks, and do not contain any selection startpoints or endpoints which may exist.


SetBookmark(bm)
===============
Sets the input integer bm as a video frame bookmark.  If bm is a list, sets each of the values in bm as a video frame bookmark.  Returns True if successful, False otherwise.


GetSelectionList()
==================
Returns a list containing the video frame selections created by AvsP's trim selection editor, where each element of the list is a 2-element tuple containing the startpoint and the endpoint of a selection.  Note that the trim selection editor must be visible for any selections to exist.


MsgBox(message, title='')
=========================
Displays a simple dialog box with the string message.


ProgressBox(max=100, message='', title='Progress')
==================================================
Returns a wxPython dialog control which displays the progress of any given task as a fraction of the input integer max.  In order to display the dialog, use its method Update(value), which takes in the new progress value.  The method Update returns False if the user clicked on the Cancel button, and returns True otherwise.  IMPORTANT: You must use the Destroy() method to destroy the dialog after you are done with it.


GetSliderInfo(index=None)
=========================
Returns a list containing information for each slider in the script located at the tab integer index.  If index is None, then the currently selected tab is used.  The slider information consists of 4 items.  The first item is the slider text itself.  The second item is the slider label.  The third item is the list of numbers which the graphical slider represents.  The fourth item is the number of decimal places for the slider numbers as specified by the user.


ExecuteMenuCommand(text)
========================
Executes one of AvsP's menu commands as specified by the input text, which can either be the name of the menu command or the keyboard shortcut.  For example, you can create a new tab in a macro by using either "avsp.ExecuteMenuCommand('File -> New Tab')" or by using "avsp.ExecuteMenuCommand('Ctrl+N')".  In this manner all menu commands are available to AvsP's macro language.  The input text is not case sensitive, but must be spelled precisely in order to work (a complete list of all the commands and shortcuts with precise spelling can be found in the "Options -> Configure shortcuts..." dialog).  Returns True if successful, False otherwise.


