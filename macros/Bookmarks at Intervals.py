last_frame = avsp.GetVideoFramecount() - 1
options = avsp.GetTextEntry(
    [_('Choose a frame step or a number of intervals'),
     [_('Frame step'), _('Number of intervals')],
     [_('Start frame'), _('End frame')], 
     _('Clear bookmarks in the same range')],
    ['', [(0, 0), (0, 0)], [(0, 0, last_frame), (last_frame, 0, last_frame)]], 
    _('Bookmarks at Intervals'),
    ['sep', ['spin', 'spin'], ['spin', 'spin'], 'check'], width=100)
if options:
    step, intervals, start, end, clear = options
else:
    return
if clear:
    avsp.ClearBookmarks(start, end)
if intervals:
    step = float(end - start + 1) / intervals
if step:
    def float_range(start, end, step):
        while start <= end:
            yield start
            start += step
    avsp.SetBookmark(float_range (start, end, step))
