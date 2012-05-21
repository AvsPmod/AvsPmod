# Customized pixel ratio

# if this macro is called by another macro, retrieve return values from 'last'
# otherwise, pop up an input box
boolsize = False
try:
    x, y = last
except:
    text = avsp.GetTextEntry('Enter a pixel ratio or new size. e.g. 40:33, 1.212 or 640x360', '', 'Customized aspect ratio')
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
if avsp.IsMenuChecked('create new tab'):
    text = avsp.GetText()
    avsp.NewTab()
    avsp.SetText(text)
    
if avsp.IsMenuChecked('force mod 2'):
    width += width%2
    height += height%2
    
if avsp.IsMenuChecked('bilinear'):
    filter = 'BilinearResize'
elif avsp.IsMenuChecked('bicubic'):
    filter = 'BicubicResize'
elif avsp.IsMenuChecked('lanczos'):
    filter = 'LanczosResize'
elif avsp.IsMenuChecked('spline36'):
    filter = 'Spline36Resize'
    
# insert text and refresh preview
text = '%s(%d, %d)' % (filter, width, height)
avsp.InsertText(text)
avsp.ShowVideoFrame(forceRefresh=True)