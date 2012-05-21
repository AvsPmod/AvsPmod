import math
#file extension to use
ext = ".png"
#number of leading zeros to put in filename. -1 will autodetect based on framecount
zeros = -1

# Get the directory to save files to
dirname = avsp.GetDirectory()

# get the number of frames
totalframes = avsp.GetVideoFramecount()
# Create a progress box
pbox = avsp.ProgressBox(max=totalframes, message = "0 / " + str(totalframes), title="Saving images...")

#find number of leading zeros to use
if (zeros < 0):
    zeros = int(math.floor(math.log10(totalframes)) + 1)

#save the images
for frame in range(0,totalframes):
    if dirname=="":
        break
    avsp.SaveImage(filename=dirname+"\\"+str(frame).zfill(zeros)+ext, framenum=frame)
    # Update the progress box, exit if user canceled
    if not pbox.Update(frame+1, str(frame+1) + " / " + str(totalframes)):
        break
# Destroy the progress box
pbox.Destroy()