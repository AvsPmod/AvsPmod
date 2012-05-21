# Imports all files from a directory and joins them in a random order
# All files must have the same attributes such as size and framerate

import os
import random
import string
# Get the directory containing source files
dirname = avsp.GetDirectory()

if dirname:
    avsp.NewTab()
    scripttxt = ''
    counter = 0
    #import each clip
    for filename in os.listdir(dirname):
        fullname = os.path.join(dirname, filename)
        if os.path.isfile(fullname):
            counter += 1
            scripttxt += 'video' + str(counter) + ' = ' + avsp.GetSourceString(fullname) + '\n'
    scripttxt += '\n'
    #join clips together
    cliplist = []
    cliptxt = ''
    while counter > 0:
        cliplist.append('video' + str(counter))
        counter -= 1
    random.shuffle(cliplist)
    for clip in cliplist:
        cliptxt += clip + ' ++ '
    cliptxt = cliptxt[:-4] #remove extra ++ from end
    scripttxt += cliptxt
    avsp.SetText(scripttxt)