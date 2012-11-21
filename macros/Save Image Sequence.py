# PREFERENCES

# Save the images always to this directory
dirname = ur''

# Save the images always with this basename
basename = ur''

# Use always at least this number of digits for padding
padding = 0


# ------------------------------------------------------------------------------


import os
import os.path
import re
import wx
import pyavs

# run in thread

self = avsp.GetWindow()

# Get options
frames = avsp.Options.get('frames', _('Bookmarks'))
show_progress = avsp.Options.get('show_progress', False)
format = avsp.Options.get('format', _('Portable Network Graphics') + ' (*.png)')
quality = avsp.Options.get('quality', 90)
use_dir = avsp.Options.get('use_dir', False)
use_base = avsp.Options.get('use_base', False)
if use_dir and not dirname:
    dirname = avsp.Options.get('dirname', '')
if use_base and not basename:
    basename = avsp.Options.get('basename', '')
isdir = os.path.isdir(dirname)
if not isdir or not basename:
    source_dir, source_base = os.path.split(avsp.GetScriptFilename(propose='image'))
    if not isdir:
        dirname = source_dir
    if not basename:
        basename = os.path.splitext(source_base)[0]
filename = os.path.join(dirname, basename)
format_dict = dict([(name[0], (ext, name[1])) for ext, name in self.imageFormats.iteritems()])
while True:
    options = avsp.GetTextEntry(title=_('Save image sequence'),
            message=[[_('Select frames'), _('Show saving progress')], 
                     [_('Output format'), _('Quality (JPEG only)')], 
                     _('Output directory and basename. The padded frame number is added as suffix'), 
                     [_('Use always this directory'), _('Use always this basename')]],
            default=[[(_('Bookmarks'), _('Range between bookmarks'), _('Trim editor selections'), 
                       _('All frames'), frames), show_progress], 
                     [sorted(format_dict.keys()) + [format], (quality, 0, 100)], 
                     filename, [use_dir, use_base]],
            types=[['list_read_only', 'check'], ['list_read_only', 'spin'], 'file_save', 
                   ['check', 'check']],
            )
    if not options: return
    frames, show_progress, format, quality, filename, use_dir, use_base = options
    if not filename:
        avsp.MsgBox(_('Select an output directory and basename for the new images files'), _('Error'))
    else: break

# Save options
avsp.Options['frames'] = frames
avsp.Options['show_progress'] = show_progress
avsp.Options['format'] = format
avsp.Options['quality'] = quality
avsp.Options['use_dir'] = use_dir
avsp.Options['use_base'] = use_base
if use_dir:
    avsp.Options['dirname'] = os.path.dirname(filename)
if use_base:
    avsp.Options['basename'] = os.path.basename(filename)

# Eval the script. Return if error
# vpy hack, remove when VapourSynth is supported
if os.name == 'nt' and avsp.GetScriptFilename().endswith('.vpy'):
    avsp.SaveScript()
AVS = pyavs.AvsClip(avsp.GetText(clean=True), matrix=self.matrix, interlaced=self.interlaced, swapuv=self.swapuv)
if AVS.IsErrorClip():
    avsp.MsgBox(AVS.error_message, _('Error'))
    return

# Get list of frames
frame_count = avsp.GetVideoFramecount()
if frames == _('Bookmarks'):
    bookmarks = avsp.GetBookmarkList()
    if bookmarks:
        frames = filter(lambda x: x < frame_count, set(bookmarks))
        frames.sort()
    else:
        avsp.MsgBox(_('There is not bookmarks'), _('Error'))
        return
elif frames == _('Range between bookmarks'):
    bookmarks = avsp.GetBookmarkList()
    if bookmarks:
        bookmarks = list(set(bookmarks))
        bookmarks.sort() 
        frames = []
        for i, bookmark in enumerate(bookmarks):
            if i%2:
                if bookmarks[i - 1] >= frame_count:
                    break
                if bookmark >= frame_count:
                    frames.extend(range(bookmarks[i - 1], frame_count))
                    break
                frames.extend(range(bookmarks[i - 1], bookmark + 1))
        if not i%2 and not bookmark >= frame_count and not avsp.MsgBox(_('Odd number of bookmarks'), 
                                                                       _('Warning'), True):
            return
    else:
        avsp.MsgBox(_('There is not bookmarks'), _('Error'))
        return
elif frames == _('Trim editor selections'):
    selections = avsp.GetSelectionList()
    if selections:
        frames = [i for lo, hi in selections for i in range(lo, hi+1)]
    else:
        avsp.MsgBox(_('There is not Trim editor selections'), _('Error'))
        return
elif frames == _('All frames'):
    frames = range(frame_count)

# Prepare filename template
ext = format_dict[format][0]
if filename.endswith(ext):  
    filename = filename[:-len(ext)]
if not re.search(r'%0\d+[di]', filename):    
    filename += '%%0%dd' % max(padding, len(str(frames[-1])))
filename += ext

# Save the images
bmp = wx.EmptyBitmap(AVS.Width, AVS.Height)
mdc = wx.MemoryDC()
mdc.SelectObject(bmp)
total_frames = len(frames)
if show_progress:
    progress = avsp.ProgressBox(total_frames, '', _('Saving images...'))
for i, frame in enumerate(frames):
    if show_progress and not avsp.SafeCall(progress.Update, 
                                           i, str(i+1) + ' / ' + str(total_frames))[0]:
        break
    dc = mdc# if avsp.Version['AvsP'] > '2.3.1' else mdc.GetHDC()
    AVS.DrawFrame(frame, dc)
    if ext == '.jpg':
        img = bmp.ConvertToImage()
        img.SetOptionInt(wx.IMAGE_OPTION_QUALITY, quality)
        if not img.SaveFile(filename % frame, format_dict[format][1]): break
    elif not bmp.SaveFile(filename % frame, format_dict[format][1]): break
if show_progress:
    avsp.SafeCall(progress.Destroy)
else:
    avsp.MsgBox(_('%d image files created.') % (i+1), _('Information'))
