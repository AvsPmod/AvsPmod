# This example shows how to automatically generate multiple scripts given a 
# directory with several source files.  Note that this example doesn't even
# directly interact with the AvsP program itself, it's almost entirely using
# pure Python for batch processing, with conviniece gui functions provided by
# the avsp module.

import os

# Get the directory containing source files
dirname = avsp.GetDirectory()

if dirname:
    # Generate each of the avisynth scripts
    for filename in os.listdir(dirname):
        fullname = os.path.join(dirname, filename)
        if os.path.isfile(fullname):
            # Get the extension-based template string
            srctxt = avsp.GetSourceString(fullname)
            # Create the script string
            scripttxt = srctxt + '\n' + 'Sharpen(1.0)\nInfo()'
            # Write the script text to a file
            f = open(fullname + '.avs', 'w')
            f.write(scripttxt)
            f.close()