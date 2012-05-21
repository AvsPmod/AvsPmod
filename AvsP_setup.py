from distutils.core import setup
import os
import py2exe
import AvsP

manifest = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Python"
    type="win32"
/>
<description>Python Interpreter</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

setup(
    version = AvsP.version,
    description = "AvsP - an AviSynth script editor",
    name = "AvsP",
    options = {"py2exe":{
        "compressed": 1,
        "optimize": 2,
        "excludes": ["translation", "Tkconstants", "Tkinter", "tcl"],
        #~ "dll_excludes": ['MSVCR71.dll', 'w9xpopen.exe', 'mfc71.dll'],
        "dll_excludes": ['w9xpopen.exe', 'mfc71.dll'],
        #~ "bundle_files": 1
    }},
    zipfile = 'lib/library.zip',
    data_files = [
        #~ ('', ['readme.txt', 'translation_readme.txt', 'autoslider_database.txt', 'Copying.txt', r'C:\Programs\Python25\unicows.dll']),
        ('', ['filterdb.dat', 'readme.txt', 'translation_readme.txt', 'Copying.txt']),
        ('src', [
            'run.py',
            '__translation_new.py',
            'AvsP.py',
            'wxp.py',
            'avisynth.py',
            'pyavs.py',
            'pyavs_avifile.py',
            'AvsP_icon.py',
            'next_icon.py',
            'play_icon.py',
            'AvsP_build.py',
            'AvsP_setup.py',
            'AvsP_i18n.py',
            'AvsP.ico',
            'notes.txt',
        ]),
        #~ ('macros', [os.path.join('macros',f) for f in os.listdir('macros')])
    ] +
    [(root, [os.path.join(root,name) for name in files]) for root, dirs, files in os.walk('macros')] +
    [(root, [os.path.join(root,name) for name in files]) for root, dirs, files in os.walk('help')] +
    [(root, [os.path.join(root,name) for name in files if os.path.splitext(name)[1] in ('.py', '.presets')]) for root, dirs, files in os.walk('tools')],
    windows = [
        {
            "script": "run.py",
            "icon_resources": [(1, "AvsP.ico")],
            "other_resources": [(24,1,manifest)]
        }
    ],
)