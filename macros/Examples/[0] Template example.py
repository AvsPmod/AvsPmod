# This example shows how to create a custom template function, which
# automatically gets the source filename via an open dialog box.  These
# types of macros can be made if you find AvsP's extension-based templates
# too limiting.  Note that the save command at the end of the macro was
# commented out, feel free to uncomment it or simply save the script using
# the regular program's interface.

# Get the filename via an open dialog box
filename = avsp.GetFilename()

if filename:
    # Create a new tab
    avsp.NewTab()
    # Create and insert the script into the tab
    avsp.InsertText(
        'AviSource("' + filename + '")\n'
        'Sharpen(1.0)\n'
        'Info()\n'
    )
    # Show the video preview
    avsp.ShowVideoFrame()
    # Save the script
    #avsp.SaveScript(filename + '.avs')