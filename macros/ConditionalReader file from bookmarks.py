# -*- coding: utf-8 -*-
"""
Generate a ConditionalReader file from the video bookmarks
    
This macro takes the list of the current video bookmarks and generates a 
new text file to be used with ConditionalReader.  Each frame can represent a 
single frame or the start or end of a range of frames.  If the 'interpolation' 
option is selected (only valid for int and float), 'Value' must consist in 
two space-separated values.

If a bookmark have a title, it can be used as its value instead of the one 
introduced in the prompt dialog.  For ranges of frames, the value can be put 
in the title of either the start or end frame.  When using interpolation the 
two values can be introduced both in the same bookmark or separately.

More info on ConditionalReader:
http://avisynth.org/mediawiki/ConditionalReader


Written by vdcrim
Original macro idea by Bernardd
"""

# PREFERENCES

default_type = 'Bool'
default_default = ''
default_value = ''
default_bm_meaning = 'Single frames'
default_use_title = True
default_filename = ur''  #  ur''  ->  avs filename + suffix
suffix = '.cr.txt'
default_insert_path = True


# ------------------------------------------------------------------------------


# Run in thread
from os.path import splitext

# Get the bookmarks
bmlist = avsp.GetBookmarkList(title=True)
if not bmlist:
    avsp.MsgBox('There is not bookmarks', 'Error')
    return
bmlist.sort()

# Prompt for options
if not default_filename:
    avs = avsp.GetScriptFilename()
    if avs: default_filename = splitext(avs)[0] + suffix
txt_filter = (_('Text files') + ' (*.txt)|*.txt|' + _('All files') + '|*.*')
while True:
    options = avsp.GetTextEntry(
        title='ConditionalReader file from bookmarks', 
        message=[['Type', 'Default', 'Value'], 
                 ['Bookmarks represent...', 
                  "Override 'Value' with the bookmark's title"], 
                 'ConditionalReader file', 
                 'Insert the ConditionalReader file path at the current cursor '
                 'position'
                ], 
        default=[[('Bool', 'Int', 'Float', 'String', default_type), 
                  ('True', 'False', default_default), 
                  ('True', 'False', default_value)], 
                 [('Single frames', 'Ranges of frames', 
                   'Ranges of frames (with interpolation)', default_bm_meaning), 
                   default_use_title], 
                 (default_filename, txt_filter), default_insert_path
                ], 
        types=[['list_read_only', 'list_writable', 'list_writable'], 
               ['list_read_only', 'check'], 'file_save', 'check'], 
        width=415)
    if not options or not options[5]:
        return
    if (options[3] == 'Ranges of frames (with interpolation)' and 
            options[0] not in ('Int', 'Float')):
        avsp.MsgBox('Interpolation only available for Int and Float', 'Error')
    else: break

# Write the ConditionalReader file
value_default = options[2].strip()
text = ['Type {}\n'.format(options[0])]
if options[1]: text.append(u'Default {}\n'.format(options[1].strip()))
if options[3] == 'Single frames':
    for frame, title in bmlist:
        text.append(u'{} {}\n'.format(frame, 
                    title.strip() if options[4] and title else value_default))
else:
    if len(bmlist) % 2 and not avsp.MsgBox('Odd number of bookmarks', 
                                           title='Warning', cancel=True):
        return
    prefix = 'R' if options[3] == 'Ranges of frames' else 'I'
    for i, bm in enumerate(bmlist):
        if i%2:
            value = None
            if options[4]:
                if bmlist[i-1][1]:
                    value = bmlist[i-1][1].strip()
                if bm[1]:
                    if value and options[3] != 'Ranges of frames':
                        value += ' ' + bm[1].strip()
                    else:
                        value = bm[1].strip()
                if not value:
                    value = value_default
            else:
                value = value_default
            text.append(u'{} {} {} {}\n'.format(
                        prefix, bmlist[i-1][0], bm[0], value))
with open(options[5], 'w') as file:
    file.writelines(text)
if options[6]:
    avsp.InsertText(u'"{}"'.format(options[5]), pos=None)
