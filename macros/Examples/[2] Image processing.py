# This example shows how to use AvsP's macros to turn AviSynth into an
# all-purpose image editor.  It's similar to the batch example, but instead
# of getting all sources in a directory and generating AviSynth scripts, this
# macro gets all the bitmaps or jpgs in a directory and generates a bunch of
# new pngs filtered according to the specified AviSynth functions.  The 
# macro also shows how to get image properties such as width and height, 
# necessary in this example to ensure the width and height are both acceptable
# for a ConvertToYV12() (assumming you are using YV12 specific filters).
# Also demonstrated is the progress box, which shows elapsed and remaining
# time and allows you to cancel the processing whenever you want.

import os

# Get the directory containing  files
dirname = avsp.GetDirectory()

if dirname and avsp.GetText() == '':
    # Create the list of file names in the directory which are bitmaps or jpegs
    namelist = []
    for name in os.listdir(dirname):
        if os.path.splitext(name)[1] in ('.bmp', '.jpg'):
            namelist.append(name)
    # Create a progress box
    pbox = avsp.ProgressBox(len(namelist), _('Processing images...'))
    # Generate each of the image files
    for i, filename in enumerate(namelist):
        fullname = os.path.join(dirname, filename)
        # Clear all the text in the tab
        avsp.SetText('')
        # Get the extension-based template string
        srctxt = avsp.GetSourceString(fullname)
        avsp.InsertText('%s\n' % srctxt)
        # Get the width and height of the video
        w = avsp.GetVideoWidth()
        h = avsp.GetVideoHeight()
        # Add borders to make the width and height mod 32
        wpad = 32 - w % 32
        hpad = 32 - h % 32
        txt = 'AddBorders(0,0,%i,%i)\n' % (wpad, hpad)
        avsp.InsertText(txt)
        # Add the rest of the script
        # (the crop at the end gets rid of any borders added earlier)
        avsp.InsertText(
            'ConvertToYV12()\n'
            'SwapUV()\n'
            'Sharpen(1.0)\n'
            'ConvertToRGB32()\n'
            'Crop(0,0,-%i,-%i)\n' % (wpad, hpad)
        )
        # Save the image as a png
        newname = os.path.join(dirname, filename+'.png')
        avsp.SaveImage(newname)
        # Update the progress box, exit if user canceled
        if not pbox.Update(i)[0]:
            break
    # Destroy the progress box
    pbox.Destroy()
    # Clear the remaining text
    avsp.SetText('')
else:
    avsp.MsgBox(_('Macro aborted'))