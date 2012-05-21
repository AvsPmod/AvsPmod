
DESCRIPTION
===========
    AvsP is at its core a tabbed text editor with features specific for creating AviSynth scripts.  It has text editing features such as AviSynth-specific syntax highlighting and autocompletion to simplify the task of writing scripts.  However, its primary advantage over other editors is its integrated video preview, which remains attached to the main window at all times.  Comparing the visual results of several different scripts is as easy as writing the scripts into several different tabs and activating the video preview, switching between tabs gives instantaneous feedback on visual differences (anyone remember lining up multiple instances of VirtualDub and alt-tabbing?).  Furthermore, the program offers a unique way for the user to define sliders for any number in the script, giving AviSynth a unique graphical interface never known before.  The following are an outline of the program's main features:

 > tabbed text editor
 > AviSynth-specific syntax highlighting and autocompletion
 > integrated video preview for easy script comparison
 > unique user-defined sliders for rapid filter setting comparison
 > built-in crop editor in video preview
 > bookmark any number of frames for quick access
 > complete macro language using the Python programming language
 > graphical front-end for command-line compression tool avs2avi

You can find out more by reading the html docs provided with the program.  For an animated demonstration of AvsP in action, check out:
http://www.avisynth.org/qwerpoi/Demo.htm

If you're interested in making suggestions or discussing about the program in general, here's the AvsP discussion thread:
http://forum.doom9.org/showthread.php?p=871134#post871134



CHANGELOG
=========

version 2.0.2 (10/27/07)

* added numerous entries to function database (contributions by Harukalover, danielkun)

* added ability to open multiple scripts in Open dialog (suggested by Underground78)

* new syntax in extension templates for relative paths (suggested by krisq)

* changed database editing for plugins to reduce redundancy with short and long names

+ fixed program hanging on text highlight (thanks miamicanes, Harukalover, foxyshadis)

+ fixed issue with translation messages (thanks zemog)

+ fixed crash when deleting existing bookmark (thanks AlanHK)

+ manually hidden sliders now stay hidden on video refresh (thanks AlanHK)

+ fixed minor bug with autocompletion and underscore character



version 2.0.1 (9/16/07)

* improved automatic user slider construction (suggested by AlanHK, bidmead)

* added line number traceback for macro errors (suggestedy by foxyshadis)

* disabled error line highlight when line-by-line update enabled (suggested by Zarxrax)

* added warnings to crop editor for invalid crop values (suggested by AlanHK)

* brought back shortcuts for function definitions in script menu (suggested by Alain2)

* added close all tabs function (suggested by Serbianboss)

* added option to disable scroll wheel through tabs (suggested by foxyshadis)

* added option to disable frames for each tab (suggested by Harukalover)

* changed autocomplete to show single item lists (suggested by Alain2)

* changed title for separate video window to full script name (suggeseted by Alain2)

+ fixed minor error when configuring shortcuts (thanks RedDwarf1, krisq)

+ fixed next bookmark function to always search forward (thanks AlanHK)

+ changed "True" and "False" in database to lowercase (thanks AlanHK)

+ fixed typo in options dialog (thanks AlanHK)

+ fixed bug with manual activation of filter help (thanks Alain2)

+ fixed bug with macro functions GetWidth/GetHeight returning zoomed values (thanks Alain2)

+ fixed display issue with slider window and zoom window fit (thanks rfmmars)



version 2.0.0 (8/29/07)

* fully automatic user sliders (enabled by default in this release)

* added default presets for each filter (suggested by Zarxrax)

* new "Tools" directory designed for AvsP plugins (suggested by Rahima, Fizick)

* new resize calculator tool (suggested by chipzoller)

* new encoder tool supporting any command line encoders (through presets)

* script tabs now keep track of their own frames

* added new side button to toggle sliders

* added reminder images in the script tabs when video has focus

* added several new configurable text colors

* improved filter documentation filename searching

* added configurable web search for filter docs whenever local docs not found

* changed external player to use original script whenever possible

* changed program to open socket for single instance check only when necessary

* improved rules for displaying calltips

* improved macros menu organization with submenus defined by subdirectories

* improved SetBookmark() macro performance with large lists (suggested by AlanHK)

+ fixed calltip bug with parentheses inside string (thanks niiyan)

+ fixed calltip bug with filters with zero arguments (thanks niiyan)

+ fixed calltip bug with "Frequent calltips" turned off (thanks Alain2)

+ fixed asterisk on title bar in separate video window (thanks krisq)

+ fixed color customization to allow non-white default background (thanks RedDwarf1)

+ fixed open with unicode filename bug (thanks Zarxrax)



version 1.4.0 (6/5/07)

* fully automatic sliders (experimental, turned off by default)

* simplified translation update procedure (suggested by Henrikx)

* added option for single instance (suggested by krisq, foxyshadis)

* added source extension filters to "Open..." dialog (suggested by 3ngel)

* changed default filename to work with unknown extensions (suggested by Zarxrax)

* opening an already opened file prompts for reload if changes exist (suggested by Kuukunen)

* toggle scrap window now works when scrap window focused (thanks AlanHK)

* changed error message when Avisynth fails to load video (thanks lolent)

* added macro for setting bookmarks (suggested by AlanHK)

* sliders no longer generated on error clips

* improved filter calltips to work with script line breaks

* added clear all text option for scrap window

* minor improvements to window layout code

+ fixed translation import problem (thanks Henrikx)

+ fixed bug with AvsP installed in directory with unicode characters (thanks Aeolis)

+ fixed display bug when resizing the script window with separate video window (thanks Alain2)

+ fixed several unicode bugs (thanks Zarxrax)

+ fixed crash when avisynth output has no video



version 1.3.9 (5/5/07)

* remember the last saved image path (suggested by 3ngel)

* changed "Show calltip" to work when cursor is in filter name (thanks AlanHK)

* changed editor to properly clear undo buffer when loading a file

* merged windows xp and 98 versions

+ fixed parity info reported by AvsP (thanks krisq, ChiDragon)

+ fixed crash when switching zoom modes (thanks Alain2)

+ fixed unnecessary scrollbars with zoom "fit inside window" (thanks foxyshadis)

+ fixed unicode bug when saving script

+ fixed unicode bug with recent file list (thanks Henrikx)

+ fixed unicode bug with Avisynth install directory (thanks Aeolis, foxyshadis)

+ minor fixes to window layout code



version 1.3.8 (4/24/07)

* changed display code to retrieve frames directly from Avisynth (contributed by tsp)

* highlight error line in script on error clip

* added new video zoom option to fit entirely inside the window (suggested by Alain2)

* added "always on top" option for main window (suggested by Alain2)

* added method to specify cursor position in filter presets (suggested by krisq)

* allow for global variables in macros (suggested by Eggroll)

* remember last path when configuring doc path/url for function help (suggested by Spuds)

* path to AvsP help directory now configurable (suggested by Fizick)

* dump program error messages to both window and log file for easier bug reporting

+ fixed unicode error on startup (thanks Spuds)

+ fixed unicode error on file open (thanks martino)

+ fixed bug with avs2avi gui and spaces in avs filename (thanks tony62)

+ accurate yuv colors reported in video status bar (thanks jmac698)

+ minor fixes to window layout code



version 1.3.7 (3/07/07)

* make up/down/left/right video shortcuts editable (suggested by Alain2, avid_avs_user)

* removed modifier restrictions for keyboard shortcuts (suggested by avid_avs_user)

* allow language translation for Ctrl, Alt, Shift (suggested by Henrikx)

* added menu items for trim selection start/end (suggested by avid_avs_user)

* added ability to export/import individual filter presets (suggested by krisq)

* added pixel position and color information to status bar (suggested by nibbles, jmac698)

* added macro to get filter info from avisynth (needs Avisynth 2.5.7+) (contributed by tsp)

* added ability to label user slider separators (suggested by R3Z)

* added ability to free all script videos from memory (suggested by foxyshadis)

* use the source filename as default in the file save dialog (suggested by Zarxrax)

* updated extension-based templates with .dga files and AVCSource() (suggested by unskinnyboy)

* added option to not prompt to unsaved scripts on program exit (suggested by foxyshadis)

* added several help menu items linking to website documentation

* improved subwindow layout management

* improved calltip displaying during window focus/motion

* minor changes to the display code

+ fixed issues with syntax highlighting default style (thanks Alain2)

+ fixed bug with unicode characters in script (thanks Spuds)

+ added workaround for top-level variables in macros (thanks tsp)

+ fixed minor bug when switching from zoom fit to regular zoom

+ fixed several subwindow positioning issues



version 1.3.6 (2/20/07)

* saved files no longer lose user slider/toggle tag info (suggested by foxyshadis)

* prompt to reload modified files when loading a session (suggested by foxyshadis)

* added visual bookmarks along the video slider (suggested by doxville, avid_avs_user)

* added trim selection editor (suggested by Zarxrax, doxville, avid_avs_user)

* added option to not load bookmarks on startup (suggested by avid_avs_user)

* added crop editor options to insert at cursor, copy to clipboard (suggested by krisq)

* improved end of script detection for crop editor

* reorganized video menu for clarity (suggested by avid_avs_user)

* improved save image dialog with specific extensions (suggested by foxyshadis)

* created windows 98 version (suggested by affter333)

+ fixed crash when creating a new tab while crop editor is shown

+ fixed small bug on program exit with multi-monitor setup (thanks foxyshadis)

+ fixed several issues with syntax highlighting (thanks Alain2)



version 1.3.5 (1/14/07)

* added more font and color options (suggested by Alain2)

* added customizable keyword lists (suggested by Alain2)

* updated filter information with internal clip properties and functions

* improved autocompletion for functions with no arguments

* added several new macro functions (ExecuteMenuCommand, GetBookmarkList, GetAvs2aviDir, GetSliderTexts)

* added slider optimization macro with complete genetic algorithm implementation

* added option to associate .avs files with AvsP (suggested by foxyshadis, JoeTF)

+ fixed minor issue with potential conflicting keyboard shortcuts (thanks Alain2)



version 1.3.4 (12/16/06)

* support for separate video window zoom fit

* updated included core filter definitions to AviSynth v2.56

* added menu options for goto next/previous bookmark (suggested by Alain2)

* option to quickly show AviSynth function definition dialog (suggested by Alain2)

* added new tag for separators in slider window (suggested by krisq)

* minor rearrangement of menu items for clarity (suggested by Fizick)

+ fixed several issues with zoom fit feature (thanks foxyshadis, zemog, doxville, Alain2)

+ fixed small bug with slider validation (thanks zemog)



version 1.3.3 (11/14/06)

* added video preview zoom to fit window (suggested by Alain2)

* remember last zoom setting on startup

* added small indicator when zoom not at 100%

* added right-click menu to script tabs (suggested by zemog)

* added video custom jump size (suggested by Alain2)

* register all keyboard shortcuts with separate video window (suggested by krisq)

* improved auto-fit for separate video window (suggested by foxyshadis)

* updated about box with website info (suggested by krisq)

* added extra validation for user sliders (suggested by Naito)

* prevent showing preview on startup if script causes hard crash (suggested by jmac698)

+ fixed positioning issues for multi-monitor setup (thanks foxyshadis)

+ fixed bug with manual autocomplete on number (thanks Alain2)

+ fixed small bug with offscreen window layout code (thanks Alain2)

+ fixed issue with saving files with unicode text and line breaks (thanks Naito)

+ allow tab as keyboard shortcut for separate video window (thanks krisq)



version 1.3.2 (11/02/06)

* added option to make video preview a separate window

* added option to quickly backup the current session (suggested by foxyshadis)

* added "paranoia mode" to backup the current session whenever video is refreshed

* increased size of window dividers to make easier to click (suggested by Alain2)

* change autoparentheses levels option labels to be clearer (suggested by Alain2)

* added option to set minimum text window size (suggested by foxyshadis)

* added option to not focus video window when refreshing (suggested by krisq)

* added ability to clear a shortcut in the shortcut editor

* minor improvements to line-by-line update mode

* improved to multi-monitor support

+ fixed bug with dragging crop edges (thanks krisq)

+ fixed left-click to focus video window (thanks krisq)

+ fixed autocomplete before operator (thanks foxyshadis)

+ fixed bug with remembering program size when maximized (thanks krisq)



version 1.3.1 (10/24/06)

* click and drag video preview similar to Acrobat Reader

* store last program size and position (suggested by Alain2)

* minor improvements to window layout code

* refresh video appropriately when creating new scripts

+ fixed bug with unicode characters in slider labels (thanks Rippraff)



version 1.3.0 (10/23/06)

* rewrote entire layout code, size-adjustable subwindows

* make cursor visible when using shift-tab shortcut (suggested by Alain2)

* option to show full pathname on program title (suggested by Alain2)

* filter help shortcut now works when cursor within filtername (suggested by Alain2)

* don't change position when disabling preview (suggested by Alain2)

* added option to allow multi-line non-triple strings (thanks Alain2)

* option to use actual avs script with external preview (suggested by Alain2)

* added ability to copy script to clipboard (suggested by communist)

+ fixed minor bug with calltip and selecting text

+ fixed status bar message for 25% and 50% zoom



version 1.2.1 (10/07/06)

* custom syntax highlighter, more than 30 individually configurable fonts/colors

* added ability to override all fonts with a monospaced font (suggested by Richard Berg)

* added recent files menu (suggested by check)

* added shortcut for moving lines up/down (suggested by communist)

* added method to disable video preview (suggested by Alain2)

* added option to specify initial line margin width (suggested by nibbles)

* added optional arguments to pass to external player

* updated several macro functions, see new examples and macros_readme.txt for info

* added option to disable frequent calltips, show only upon typing open parentheses

* added ability to use keyboard shortcut for filter help file (suggested by Alain2)

* added option to wrap the text (suggested by Alain2)

* added option to highlight current line (suggested by Alain2)

* added 25% and 50% zoom levels (suggested by communist)

* moved line-by-line update mode to menu option, to allow for keyboard shortcut

* changed data format for options files to editable text files

+ fixed minor bug with improper video updating (thanks nibbles)

+ fixed small mistakes with some messages (thanks zemog)

+ fixed minor bug with tabs and spaces

+ fixed minor bug with session saving/loading

+ cleaned up minor issues with tooltip code



version 1.2.0 (10/02/06)

* customizable keyboard shortcuts (suggested by Zarxrax)

* aspect ratio info on status bar in video mode (suggested by krisq)

* added option for constant video update when dragging (suggested by doxville)

* added option for line-by-line video preview update (suggested by Zarxrax)

* center window when it goes off the screen (suggested by Ebobtron)

* added ability to mark and add trim selections (suggested by doxville)

* make shortcut Ctrl-G highlight frame text ctrl (suggested by Champs)

* copy a script by double-clicking the tab (suggested by Zarxrax)

* added options for using text tabs, tab length (suggested by foxyshadis)

* auto save session on exit, load on startup if no args (suggested by foxyshadis)

* minor improvements to calltip argument highlight code (suggested by tsp)

* minor improvements to avs2avi frontend

+ fixed bug in "Options -> Settings" dialog (thanks nibbles)

+ fixed bug with avs2avi frontend and translation (thanks Fizick)

+ fixed error when right-clicking a popup tooltip (thanks Zarxrax)

+ fixed bug saving .avsi file with .avs extension (thanks foxyshadis)



version 1.1.6 (09/26/06)

* added ability to specify a file or url for AviSynth help (suggested by Fizick)

* added shortcut Shift-Tab to switch focus between the text and video (suggested by krisq)

+ fixed bug with one frame long video (thanks mkanel)

+ fixed read from avsfilters.txt feature (thanks mkanel)

+ fixed minor bug with Replace and Find Next (thanks mkanel)

+ cleaned up calltip and argument highlight code to be more robust



version 1.1.5 (09/23/06)

* show filter documentation by clicking the calltip (suggested by Fizick)

* toggle portions of script text (suggested by Dr. D)

* now possible to specify modulo values with user sliders (suggested by krisq)

* remember path of last saved session (suggested by Dr. D)

* reworked filter presets to be easier to edit

+ fixed mouse wheel tab switching when zoomed (thanks Dr. D)

+ fixed text visibility issue when using Find or Find next (thanks mkanel)

+ fixed small mistakes with some messages (thanks niiyan)

+ fixed small bug with recentdir pathname

+ fixed minor video preview window sizing issues

+ fixed minor bug when closing the only tab



version 1.1.2 (09/14/06)

* highlight current argument in calltips (suggested by tsp)

* editing AviSynth filter info no longer requires program restart

* enable localization of program's interface language (suggested by Fizick)

* added popup messages to example macros to prevent confusion

+ fixed issue with case-sensitive extensions (thanks midelic)

+ cleaned up dynamic preview sizing code (thanks matrix)

+ fixed some stray bugs with wx namespace

+ fixed program association with .ses file



version 1.1.0 (09/10/06)

* scrolled window for user sliders (suggested by Mtz, mimage)

* buttons on user sliders for fine tuning (suggested by Mtz)

* click blue slider value to reset to initial value (suggested by Mtz, mimage)

* method for storing filter auto-complete presets (suggested by mimage)

* separate filters.dat (suggested by foxyshadis, Fizick)

* save all scripts as session with user sliders (suggested by Dr. D)

* preview zoom levels (suggested by Dr. D)

* validate unique slider name

* set initial maxWidth, maxHeight from user resolution

+ fixed improper opening files of .avsi files (thanks mkanel)

+ fixed minor issue with working dir when opening files (thanks krisq)

+ fixed commented sliders (thanks vcmohan)

+ fixed issue of multiple tabs of same filename

+ fixed multi-calltip bug

+ fixed off-screen calltips

+ fixed float/integer issue with setting user slider value (thanks matrix)




version 1.0.4 (09/06/06)

* read in filter info from text file named "avsfilters.txt" (suggested by foxyshadis, tsp)

* popup calltips show whenever cursor is anywhere inside a filter's arguments (suggested by foxyshadis)

* calltips close on left mouse click in the text



version 1.0.3 (09/04/06)

* fixed issue with spaces in filenames when using external preview (thanks unskinnyboy, pookie)

* changed refresh keyboard shortcut to F5 (to be more similar to vdub), shift-F5 now hides the preview (suggested by Mug Funky)



version 1.0.2 (09/04/06)

* first release