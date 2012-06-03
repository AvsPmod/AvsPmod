# This opens an external player and previews the video from the current point rather than from the beginning
# You need to edit the following line to point to a player on your computer 

exe = r'C:\Program Files (x86)\MPC HomeCinema\mpc-hc.exe'

######
import time
trimmed = avsp.GetFrameNumber()
originaltext = avsp.GetText()
avsp.SetText(originaltext+"\ntrim("+str(trimmed)+',0)', index=None)
success = avsp.RunExternalPlayer(exe)
time.sleep(1)
avsp.SetText(originaltext, index=None)
#####

if not success:
    avsp.MsgBox(
        _('Failed to run the external player!\n\n'
          'Open the macro file in the "Macros" subdirectory\n'
          'with a text editor and edit the executable\n'
          'directory appropriately!'),
        _('Error')
    )