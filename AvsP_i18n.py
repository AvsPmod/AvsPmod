import os
import sys
import __builtin__
import AvsP

def _(s): return s
__builtin__._ = _

def main():
    pythonexe = sys.executable 
    pygettextpath = os.path.join(sys.prefix, 'Tools\i18n\pygettext.py')
    toolsdir = 'tools'
    
    argsList = ['AvsP.py wxp.py pyavs.py pyavs_avifile.py']
    # Get additional files to translate from the tools directory
    sys.path.insert(0, toolsdir)
    try:
        items = __import__('ToolsMenu').menuInfo
    except ImportError:
        items = []
    for item in items:
        if len(item) == 3:
            argsList.append(item)
            
    oldline = ''
    messageDict = {}
    newlines = ['messages = {\n']
    for args in argsList:
        if len(args) != 3:
            os.system('""%s" "%s" %s"' % (pythonexe, pygettextpath, args))
        else:
            filename, menuLabel, statusString = args
            filename += '.py'
            fullname = os.path.join(toolsdir, filename)
            s = '\n    #--- Tool: %s ---#\n' % (filename)
            newlines.append(s)
            s = '    "%s" : u"",\n' % (menuLabel)
            newlines.append(s)
            s = '    "%s" : u"",\n' % (statusString)
            newlines.append(s)
            os.system('""%s" "%s" %s"' % (pythonexe, pygettextpath, fullname))
        f = open('messages.pot', 'r')
        lines = f.readlines()
        f.close()
        os.remove('messages.pot')
        for line in lines:
            line = line.strip()
            if line.startswith('msgid '):
                text = line.split('msgid ')[1]
                if oldline.startswith('#:') and text not in messageDict:
                    comment = ' %s' % oldline
                    #~ s = '    %s : u"",%s\n' % (text, comment)
                    s = '    %s : u"",\n' % (text)
                    newlines.append(s)
                    messageDict[text] = None
            oldline = line
    newlines.append('}')
    
    f = open('__translation_new.py', 'w')
    f.write("new_translation_string = r'''")
    f.write('version = "%s"\n\n' % AvsP.version)
    f.writelines(newlines)
    f.write("'''")
    f.close()
    
    return True
    
if __name__ == '__main__':
    main()