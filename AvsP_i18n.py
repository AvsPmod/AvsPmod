
import __builtin__
import sys
import os
import os.path
import glob
import re

def _(s): return s
__builtin__._ = _

def main(version=None):
    if version is None:
        from AvsP import version
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
    f.write('version = "%s"\n\n' % version)
    f.writelines(newlines)
    f.write("'''")
    f.close()
    
    return True

def UpdateTranslationFile(dir, lang=None, version=None):
    if version is None:
        from AvsP import version
    try:
        from __translation_new import new_translation_string
    except ImportError:
        if hasattr(sys,'frozen'):
            raise
        else:
            main(version)
            from __translation_new import new_translation_string
    newmark = ' # New in v%s' % version
    # Get the text from the translation file
    file_list = ([os.path.join(dir, 'translation_%s.py' % lang)] if lang
                 else glob.glob(os.path.join(dir, 'translation_*.py')))
    for filename in file_list:
        if os.path.isfile(filename):
            f = open(filename, 'r')
            txt = f.read()
            f.close()
        else:
            txt = ''
        # Setup the new text...
        oldMessageDict = {}
        oldMessageDict2 = {}
        allMessagesMatched = True
        if not txt.strip():
            newmark = ''
            newlines = (
            '# -*- coding: utf-8 -*-\n'
            '\n'
            '# This file is used to translate the messages used in the AvsPmod interface.\n'
            '# To use it, make sure it is named "translation_lng.py" where "lng" is the \n'
            '# three-letter code corresponding to the language that is translated to \n'
            '# (see <http://www.loc.gov/standards/iso639-2/php/code_list.php>), \n'
            '# and is placed in the "%s" subdirectory.\n' % os.path.basename(dir) +
            '# \n'
            '# Simply add translated messages next to each message (any untranslated \n'
            '# messages will be shown in English).  You can type unicode text directly \n'
            '# into this document - if you do, make sure to save it in the appropriate \n'
            '# format.  If required, you can change the coding on the first line of this \n'
            '# document to a coding appropriate for your translated language. DO NOT \n'
            '# translate any words inside formatted strings (ie, any portions of the \n'
            '# text which look like %(...)s, %(...)i, etc.)\n'
            ).split('\n')
        else:
            newlines = []
            boolStartLines = True
            re_mark = re.compile(r'(.*(?<![\'"])[\'"],)\s*#')
            for line in txt.split('\n'):
                # Copy the start lines
                if line.strip() and not line.lstrip('\xef\xbb\xbf').strip().startswith('#'):
                    boolStartLines = False
                if boolStartLines:
                    newlines.append(line)
                # Get the key
                splitline = line.split(' : ', 1)
                if len(splitline) == 2:
                    key = splitline[0].strip()
                    match = re_mark.match(line)
                    oldMessageDict[key] = match.group(1) if match else line
                    # Heuristically add extra keys for similar enough messages
                    if splitline[1].strip().startswith('u"'):
                        rawkey = key.strip('"')
                        splitvalue = splitline[1].strip().split('"')
                        if rawkey.endswith(':'):
                            key2 = '"%s"' % rawkey.rstrip(':')
                            splitvalue[1] = splitvalue[1].rstrip(':')
                            line2 = '    ' + key2 + ' : ' + '"'.join(splitvalue)
                            oldMessageDict2[key2] = line2
                        elif rawkey.endswith(' *'):
                            key2 = '"%s"' % rawkey.rstrip(' *')
                            splitvalue[1] = splitvalue[1].rstrip(' *')
                            line2 = '    ' + key2 + ' : ' + '"'.join(splitvalue)
                            oldMessageDict2[key2] = line2
                        elif rawkey and (rawkey[0].isspace() or rawkey[-1].isspace()):
                            key2 = '"%s"' % rawkey.strip()
                            splitvalue[1] = splitvalue[1].strip()
                            line2 = '    ' + key2 + ' : ' + '"'.join(splitvalue)
                            oldMessageDict2[key2] = line2
        # Get the new translation strings and complete the new text
        curlines = new_translation_string.split('\n')
        for line in curlines:
            splitline = line.split(' : ')
            if line.startswith('    ') and len(splitline) > 1:
                key = splitline[0].strip()
                if key in oldMessageDict:
                    newlines.append(oldMessageDict[key])
                elif key in oldMessageDict2:
                    newlines.append(oldMessageDict2[key])
                else:
                    newlines.append(line+newmark)
                    allMessagesMatched = False
            else:
                newlines.append(line)
        # Overwrite the text file with the new data
        f = open(filename, 'w')
        f.write('\n'.join(newlines))
        f.close()
    return not allMessagesMatched
    
if __name__ == '__main__':
    main()