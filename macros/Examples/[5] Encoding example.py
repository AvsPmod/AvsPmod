# This example is almost identical to the "Secondary preview" macro, the only
# difference is that in this example, we are using the actual avs script instead
# of creating a temporary preview.avs script.  The macro saves any unsaved
# changes and runs an external program using Python's subprocess module
# (note that it is commented out, if you wish to use the macro you'll need to
# uncomment the line and change the arguments appropriately for your specific
# application).
import subprocess

# Automatically save any unsaved changes
# Use avsp.SaveScriptAs() instead if you want to always prompt the user
filename = avsp.SaveScript()

# Run the external program using Python's subprocess module
# The subprocess.Popen function takes in a list of command line arguments,
# automatically taking care of any spaces in the filenames.
exe = r'C:\Progam Files\ffmpeg\ffmpeg.exe'
outputfilename = filename+'.avi'
#subprocess.Popen([exe, filename, '-b', '500', outputfilename])
avsp.MsgBox(_('Encoding is disabled, please read the "Encoding example.py" macro for info'))