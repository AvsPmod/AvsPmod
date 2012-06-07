value = avsp.GetTextEntry([_('Choose a frame step or a number of intervals'),
                           _('Frame step'), _('Number of intervals')],
                            '', _('Bookmarks at Intervals'), 'sep', width=100)
if any(value):
    totalframes = avsp.GetVideoFramecount()
    step = float(value[0]) if value[0] else totalframes / float(value[1])
    def float_range(start=0, end=10, step=1):
        while start < end:
            yield start
            start += step
    avsp.SetBookmark(float_range(0, totalframes - 1, step))
