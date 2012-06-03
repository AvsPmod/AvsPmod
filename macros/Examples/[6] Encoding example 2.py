# This macro is a more detailed version of the "Encoding example" macro.  The
# macro uses the avsp.GetTextEntry() function to retrieve multiple inputs from
# the user, then runs the appropriate external program.  The lines which
# actually run the external program are commented out, if you wish to use the
# macro you'll need to uncomment them and change the macro appropriately for
# your specific application.

import subprocess

# Save any unsaved changes to the script and get the filename
infile = avsp.SaveScript()

# Get basic encoder options with a dialog box
labels = [_('Bitrate:'), _('Output width:'), _('Output height:'), _('Output filename:')]
defaults = ['500', '320', '240', infile+'.avi']
entries = avsp.GetTextEntry(labels, defaults, _('Enter encoder info'))

if entries:
    # Run the encoder
    bitrate, width, height, outfile = entries
    if True:
        # SINGLE PASS MODE (run the encoder and give control back to AvsP)
        args = [
            r'C:\Progam Files\ffmpeg\ffmpeg.exe',
            '-i', infile,
            '-s', width+'x'+height,
            '-b', bitrate,
            '-y', outfile,
        ]
        # subprocess.Popen(args)
    else:    
        # MULTI-PASS MODE (you cannot use AvsP until both passes finish!)
        args = [
            r'C:\Progam Files\ffmpeg\ffmpeg.exe',
            '-i', infile,
            '-s', width+'x'+height,
            '-b', bitrate,
            '-pass', '1',
            '-y', outfile,
        ]
        # Run the first pass
        # subprocess.call(args)
        # Run the second pass
        # args[-3] = '2'
        # subprocess.call(args)    
    avsp.MsgBox(_('Encoding is disabled, please read the "Encoding example 2.py" macro for info'))