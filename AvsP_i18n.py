
import __builtin__
import sys
import os
import os.path
import glob
import re

def _(s): return s
__builtin__._ = _

pythonexe = sys.executable 
pygettextpath = os.path.join(sys.prefix, 'Tools', 'i18n', 'pygettext.py')
toolsdir = 'tools'
macrosdir = 'macros'

def main(version=None):
    if version is None:
        from AvsP import version
    
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
    
    newlines = ['messages = {\n']
    messageSet = set()
    for args in argsList:
        newlines.extend(GenerateMessages(messageSet, args))
    
    # Include the macros' filenames
    newlines.append('\n    #--- Macros ---#\n')
    macro_list = []
    label_list = []
    global macrosdir
    if not os.path.isdir(macrosdir):
        macrosdir = os.path.join('..', macrosdir)
        if not os.path.isdir(macrosdir):
            exit('Macros directory not found')
    re_macro = re.compile(r'(?:\[\s*\d+\s*\]\s+)?((?P<chr>\w)(?P=chr){2}\s+)?\s*([^\[].+?)\s*\.py')
    for dirpath, dirnames, filenames in os.walk(macrosdir):
        for filename in filenames:
            match = re_macro.match(filename)
            if match and match.group(3) != '---':
                newlines.append('    "%s" : u"",\n' % match.group(3))
                messageSet.add('"%s"' % match.group(3))
                if not match.group('chr'):
                    macro_list.append('"%s" ' % os.path.abspath(os.path.join(dirpath, filename)))
                    label_list.append(match.group(3))
        for dirname in dirnames:
            newlines.append('    "%s" : u"",\n' % dirname)
    
    # Include the macros
    for macro, label in zip(macro_list, label_list):
        lines = GenerateMessages(messageSet, macro)
        if lines:
            newlines.append('\n    #--- Macro: %s ---#\n' % label)
            newlines.extend(lines)
    newlines.append('\n    #--- Macros - Extra ---#\n')
    
    newlines.append('}')

    f = open('__translation_new.py', 'w')
    f.write("new_translation_string = r'''")
    f.write('version = "%s"\n\n' % version)
    f.writelines(newlines)
    f.write("'''")
    f.close()
    
    return True

def GenerateMessages(messageSet, args):
    
    oldline = ''
    newlines = []
    if isinstance(args, basestring):
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
    multiline = False
    for i, line in enumerate(lines):
        line = line.strip()
        if not multiline:
            if line.startswith('msgid '):
                text = line.split('msgid ')[1]
                if text.strip('"'):
                    if oldline.startswith('#:') and text not in messageSet:
                        #~ comment = ' %s' % oldline
                        #~ s = '    %s : u"",%s\n' % (text, comment)
                        s = '    %s : u"",\n' % (text)
                        newlines.append(s)
                        messageSet.add(text)
                else:
                    multiline = i
                    text = '"'
            oldline = line
        else:
            if not line.startswith('msgstr '):
                text += line.strip('"')
            else:
                text += '"'
                if i - multiline > 1 and text not in messageSet:
                    s = '    %s : u"",\n' % (text)
                    newlines.append(s)
                    messageSet.add(text)
                multiline = False
    return newlines

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
            '# touch line breaks (\\n) and any words inside formatted strings (ie, any \n'
            '# portions of the text which look like %(...)s, %(...)i, etc.)\n'
            ).split('\n')
        else:
            newlines = []
            boolStartLines = True
            re_mark = re.compile(r'(.*(?<![\'"])[\'"],)\s*#')
            txt, extra_sep, extra_txt = txt.partition('\n    #--- Macros - Extra ---#\n')
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
        if extra_txt:
            newlines[-1] = extra_txt
        
        # Overwrite the text file with the new data
        f = open(filename, 'w')
        f.write('\n'.join(newlines))
        f.close()
    return not allMessagesMatched
    
if __name__ == '__main__':
    main()