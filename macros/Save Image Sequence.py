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
quality = self.options['jpegquality']
depth = avsp.Options.get('depth', 8)
use_dir = avsp.Options.get('use_dir', False)
use_base = avsp.Options.get('use_base', False)
if use_dir and not dirname:
    dirname = avsp.Options.get('dirname', '')
if use_base and not basename:
    basename = avsp.Options.get('basename', '')
use_subdirs = avsp.Options.get('use_subdirs', False)
frame_suffix = avsp.Options.get('frame_suffix', True)
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
            message=[[_('Select frames'), _('Output format')], 
                     [_('Quality (JPEG only)'), _('Depth (PNG only)'), _('Show saving progress')], 
                     _('Output directory and basename. A padded number is added as suffix'), 
                     [_('Use always this directory'), _('Use always this basename')],
                     [_('Save ranges to subdirectories'), _('Add the frame number as the suffix')]],
            default=[[(_('Bookmarks'), _('Range between bookmarks'), _('Trim editor selections'), 
                       _('All frames'), frames), sorted(format_dict.keys()) + [format]],
                     [(quality, 0, 100), (depth, 8, 16, 0, 8), show_progress], 
                     filename, [use_dir, use_base], [use_subdirs, frame_suffix]],
            types=[['list_read_only', 'list_read_only'], ['spin', 'spin', 'check'], 'file_save', 
                   ['check', 'check'], ['check', 'check']],
            )
    if not options: return
    frames, format, quality, depth, show_progress, filename, use_dir, use_base, use_subdirs, frame_suffix = options
    if not filename:
        avsp.MsgBox(_('Select an output directory and basename for the new images files'), _('Error'))
    else: break

# Save options
avsp.Options['frames'] = frames
avsp.Options['show_progress'] = show_progress
avsp.Options['format'] = format
self.options['jpegquality'] = quality
avsp.Options['depth'] = depth
avsp.Options['use_dir'] = use_dir
avsp.Options['use_base'] = use_base
dirname, basename = os.path.split(filename)
if use_dir:
    avsp.Options['dirname'] = dirname
if use_base:
    avsp.Options['basename'] = basename
avsp.Options['use_subdirs'] = use_subdirs
avsp.Options['frame_suffix'] = frame_suffix

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
    use_subdirs = False
    bookmarks = avsp.GetBookmarkList()
    if bookmarks:
        frames = sorted(filter(lambda x: x < frame_count, set(bookmarks))),
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
                    frames.append(range(bookmarks[i - 1], frame_count))
                    break
                frames.append(range(bookmarks[i - 1], bookmark + 1))
        if not i%2 and not bookmark >= frame_count and not avsp.MsgBox(_('Odd number of bookmarks'), 
                                                                       _('Warning'), True):
            return
    else:
        avsp.MsgBox(_('There is not bookmarks'), _('Error'))
        return
elif frames == _('Trim editor selections'):
    selections = avsp.GetSelectionList()
    if selections:
        frames = [range(lo, hi+1) for lo, hi in selections]
    else:
        avsp.MsgBox(_('There is not Trim editor selections'), _('Error'))
        return
elif frames == _('All frames'):
    use_subdirs = False
    frames = range(frame_count),
scene_digits = len(str(len(frames)))
total_frames = sum(len(i) for i in frames)

# Prepare filename template
ext = format_dict[format][0]
suffix_added = re.search(r'%0\d+[di]', basename)
if suffix_added:
    if not basename.endswith(ext):  
        if use_subdirs:
            basename += ext
        else:
            filename += ext
else:
    if basename.endswith(ext):  
        basename = basename[:-len(ext)]
    if not use_subdirs:
        basename += '%%0%dd%s' % (max(padding, len(str(frames[-1][-1])) 
                        if frame_suffix else len(str(total_frames))), ext)
        filename = os.path.join(dirname, basename)

# Save the images
paths = []
if show_progress:
    progress = avsp.ProgressBox(total_frames, '', _('Saving images...'))
for i, frame_range in enumerate(frames):
    if use_subdirs:
        dirname2 = os.path.join(dirname, self.bookmarkDict.get(frame_range[0], 
                                         _('scene_{0:0{1}}').format(i+1, scene_digits)))
        if not os.path.isdir(dirname2): os.mkdir(dirname2)
        if not suffix_added:
            basename2 = '%s%%0%dd%s' % (basename, max(padding, len(str(frame_range[-1])) 
                if frame_suffix else len(str(len(frame_range)))), ext)
        else:
            basename2 = basename
        filename = os.path.join(dirname2, basename2)
        frame_index = 1
    else:
        frame_index = len(paths) + 1
    for j, frame in enumerate(frame_range):
        if show_progress and not avsp.SafeCall(progress.Update, len(paths), 
                                str(len(paths)) + ' / ' + str(total_frames))[0]:
            break
        ret = self.SaveImage(filename % (frame if frame_suffix else frame_index + j), 
                             frame=frame, avs_clip=AVS, quality=quality, depth=depth)
        if not ret:
            break
        paths.append(ret)
if show_progress:
    avsp.SafeCall(progress.Destroy)
else:
    avsp.MsgBox(_('%d image files created.') % len(paths), _('Information'))
return paths
