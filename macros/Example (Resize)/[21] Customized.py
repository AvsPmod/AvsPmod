# Customized pixel ratio

# If this macro is called by another macro, retrieve the return values 
# from 'avsp.Last'.  Otherwise, pop up an input box.
boolsize = False
try:
    x, y = avsp.Last
except:
    text = avsp.GetTextEntry(_('Enter a pixel ratio or new size. e.g. 40:33, 1.212 or 640x360'), '', _('Customized aspect ratio'))
    text = text.lower()
    try:
        if ':' in text:
            x, y = [int(s) for s in text.split(':')]
        elif 'x' in text:
            boolsize = True
            x, y = [int(s) for s in text.split('x')]            
        else:
            x, y = float(text), 1
    except:
        return
        
# calculate new size. exit if 1:1 or same size
width, height = avsp.GetVideoWidth(), avsp.GetVideoHeight()
if boolsize:
    if width == x and height == y:
        return
    width, height = x, y
else:    
    if x > y:
        width = int(float(width)*x/y)
    elif x < y:
        height = int(float(height)*y/x)
    else:
        return

# retrieve menu item's state to create a suitable avs statement
if avsp.IsMenuChecked(_('create new tab')):
    text = avsp.GetText()
    avsp.NewTab()
    avsp.SetText(text)
    
if avsp.IsMenuChecked(_('force mod 2')):
    width += width%2
    height += height%2
    
if avsp.IsMenuChecked(_('bilinear')):
    filter = 'BilinearResize'
elif avsp.IsMenuChecked(_('bicubic')):
    filter = 'BicubicResize'
elif avsp.IsMenuChecked(_('lanczos')):
    filter = 'LanczosResize'
elif avsp.IsMenuChecked(_('spline36')):
    filter = 'Spline36Resize'
    
# insert text and refresh preview
text = '%s(%d, %d)' % (filter, width, height)
avsp.InsertText(text)
avsp.ShowVideoFrame(forceRefresh=True)