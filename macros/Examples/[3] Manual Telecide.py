# This is an advanced macro designed to aid in the process of manual
# deinterlacing.  In order to use this macro, you must first have a general
# understanding of the Telecide AviSynth filter, otherwise most of the stuff
# the macro does (and most of the description here) will be meaningless to
# you.  You can learn everything you need to know about the Telecide filter
# from the Decomb tutorial and reference manual in the AviSynth help.
#
# The macro itself has three different modes - the first mode retrieves
# the source file and sets up a script to help determine the field order,
# the second mode creates several scripts related to the Telecide filter, 
# and the third mode writes override information to a text file, line by
# line. The following is a general description of how to use the macro.
#
# To begin, first start up AvsP.exe and run the macro.  It will prompt you for
# the source file, then it creates a script with the top and bottom
# fields of the video seperated and stacked vertically.  Go through some of
# the video frame by frame to determine the field order.  When you determined
# the field order, run the macro again, this time it will prompt you for the
# field order (0 or 1), then it creates and saves four scripts.  The first
# script is the source with Telecide applied, the other three scripts
# represent the frames which the filter Telecide can choose from, "current",
# "next", and "previous".  Once these scripts are open, go through the
# Telecide script (the first script) frame by frame, starting from the
# beginning.  If you see an interlaced frame, look at the "current",
# "next", and "previous" scripts to see if there's a better non-interlaced
# frame. If so, running the macro again will record the frame number and the
# letter "c", "n", or "p" (depending on which tab is currently selected) into
# the override text file, and show the Telecide video again, this time with
# the overridden frame.  Note that running the macro when the first tab is
# selected (the Telecide tab) is not appropriate, and the macro issues a
# warning with a MsgBox.

import os

if avsp.GetTabCount() == 1 and avsp.GetText() == '':
    #== FIRST MODE ==#
    # Get the filename of the source to de-interlace from a dialog box
    filename = avsp.GetFilename(_('Open a source to Telecide'))
    if filename:
        # Make the script to determine field order
        # Note: the filename is stored on the first line, used by the second mode
        avsp.InsertText('# TELECIDE FILENAME: %s\n' % filename)
        srcstring = avsp.GetSourceString(filename)
        avsp.InsertText('src = %s\n' % srcstring)
        avsp.InsertText(
            'top = src.AssumeTFF().SeparateFields().Subtitle("order = 1")\n'
            'bot = src.AssumeBFF().SeparateFields().Subtitle("order = 0")\n'
            'StackVertical(top, bot)\n'
        )
        avsp.ShowVideoFrame(0)
elif avsp.GetTabCount() == 1 and avsp.GetText().startswith('# TELECIDE FILENAME: '):
    #== SECOND MODE ==#
    # Get the filename of the source from the first line of the script
    firstline = avsp.GetText().split('\n')[0]
    filename = firstline.split('# TELECIDE FILENAME: ')[1]
    # If the filename somehow got mangled, get it again with a dialog box
    if not os.path.isfile(filename):
        avsp.MsgBox(_('Filename was mangled! Get it again!'), _('Error'))
        filename = avsp.GetFilename(_('Open a source to Telecide'))
    # Get the field order from the user, make sure it's either 0 or 1
    order = avsp.GetTextEntry(_('Enter the field order:'))
    try:
        order = int(order)
        if order not in (0,1):
            avsp.MsgBox(_('Must enter either a 0 or 1!'))
    except ValueError:
        avsp.MsgBox(_('Must enter an integer!'))
    # Make the Telecide-related scripts
    if filename and order in (0,1):
        # Close the field order script
        avsp.CloseTab(0)
        # Make the telecide override text file (empty for now)
        dir, base = os.path.split(filename)
        ovrName = 'telecide_override.txt'
        f = open(os.path.join(dir, ovrName), 'w')
        #~ f.write('\n')
        f.close()
        # Make the telecide script
        name = os.path.join(dir, 'telecideBase.avs')
        avsp.InsertText('# TELECIDE OVERRIDE NAME: %s\n' % os.path.join(dir, ovrName))
        srcstring = avsp.GetSourceString(filename)
        avsp.InsertText('%s\n' % srcstring)
        avsp.InsertText('Telecide(order=%i, guide=1, post=0, show=true, ovr="%s")\n' % (order, ovrName))
        avsp.SaveScript(name)
        # Make the "current" script
        name = os.path.join(dir, 'telecideCurrent.avs')
        avsp.NewTab()
        avsp.InsertText('%s\nSubtitle("Current")\n' % srcstring)
        avsp.SaveScript(name)
        # Make the "next" script
        name = os.path.join(dir, 'telecideNext.avs')
        avsp.NewTab()
        avsp.InsertText('src = %s\n' % srcstring)
        if order == 0:
            avsp.InsertText('sep = src.AssumeBFF().SeparateFields()\n')
        else:
            avsp.InsertText('sep = src.AssumeTFF().SeparateFields()\n')
        avsp.InsertText(
            'first = sep.SelectEven().Trim(1,0)\n'
            'second = sep.SelectOdd()\n'
            'new = Interleave(first, second).Weave()\n'
            'new.Subtitle("Next")\n'
        )
        avsp.SaveScript(name)
        # Make the "previous" script
        name = os.path.join(dir, 'telecidePrevious.avs')
        avsp.NewTab()
        avsp.InsertText('src = %s\n' % srcstring)
        if order == 0:
            avsp.InsertText('sep = src.AssumeBFF().SeparateFields()\n')
        else:
            avsp.InsertText('sep = src.AssumeTFF().SeparateFields()\n')
        avsp.InsertText(
            'first = sep.SelectEven()\n'
            'second = sep.SelectOdd().DuplicateFrame(0).Trim(0, src.Framecount()-1)\n'
            'new = Interleave(first, second).Weave()\n'
            'new.Subtitle("Previous")\n'
        )
        avsp.SaveScript(name)
        # Select the first tab and show the video preview
        avsp.SelectTab(0)
        avsp.ShowVideoFrame(0)
elif avsp.GetTabCount() == 4 and avsp.GetText(0).startswith('# TELECIDE OVERRIDE NAME: '):
    #== THIRD MODE ==#
    # Get the filename of the override text file from the first line of the script
    firstline = avsp.GetText(0).split('\n')[0]
    filename = firstline.split('# TELECIDE OVERRIDE NAME: ')[1]
    # If the filename somehow got mangled, get it again with a dialog box
    if not os.path.isfile(filename):
        avsp.MsgBox(_('Override filename was mangled! Get it again!'), _('Error'))
        filename = avsp.GetFilename('Get the Telecide overrride text file')
    if filename:
        # Get the index of the currently selected tab
        index = avsp.GetCurrentTabIndex()
        if index == 0:
            # Don't write anything if base Telecide tab was selected
            avsp.MsgBox(_('Not allowed to select base Telecide tab!'), _('Error'))
        else:
            # Create the text to write depending on which tab was selected
            frame = avsp.GetFrameNumber()
            if index == 1:
                txt = '%s c\n' % frame
            elif index == 2:
                txt = '%s n\n' % frame
            elif index == 3:
                txt = '%s p\n' % frame
            # Write the text to the override file
            f = open(filename, 'a')
            f.write(txt)
            f.close()
            # Show the video of the Telecide script
            # Force the video to refresh (AviSynth script hasn't changed, but override file has)
            avsp.ShowVideoFrame(index=0, forceRefresh=True)
else:
    # Unknown mode
    avsp.MsgBox(_('Unknown mode!'), _('Error'))
    