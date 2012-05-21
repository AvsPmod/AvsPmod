totalframes = avsp.GetVideoFramecount()
value = avsp.GetTextEntry("Values of 1 or greater will create bookmarks at that interval. \ne.g. a value of 1000 will create a bookmark every 1000 frames. \nValues between 0 and 1 will distribute bookmarks \nat even intervals throughout the video. \ne.g. a value of 0.2 will create 5 evenly spaced bookmarks.", default="1000", title="Bookmark Interval")
value = float(value)
if value >= 1:
    currentframe = 0
    while currentframe < totalframes:
        avsp.SetBookmark(currentframe)
        currentframe += value
else:
    currentframe = 0
    avsp.SetBookmark(currentframe)
    interval = totalframes * value
    while currentframe < totalframes:
        avsp.SetBookmark(currentframe)
        currentframe += interval