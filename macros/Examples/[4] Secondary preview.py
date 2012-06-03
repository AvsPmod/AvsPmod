# This example shows how to run an external player with macros.  This 
# functionality is already provided with AvsP's external preview, but macros
# allow you to define as many different external programs as you want.  The
# first argument to the function is the path to the executable (you'll have to
# change this path to something appropriate for your pc).  The second argument
# to the function is any additional command line arguments you wish to pass to
# the external program.

exe = r'C:\Program Files\mplayer\mplayer.exe'
args = '-fs -monitoraspect 16:9'
success = avsp.RunExternalPlayer(exe, args)

if not success:
    avsp.MsgBox(
        _('Failed to run the external player!\n\n'
          'Open the macro file in the "Macros" subdirectory\n'
          'with a text editor and edit the executable\n'
          'directory appropriately!'),
        _('Error')
    )