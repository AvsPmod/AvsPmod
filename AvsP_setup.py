from distutils.core import setup
import os, sys
import py2exe
import AvsP

appName = "AvsPmod"
description = "%s - an AviSynth script editor" % appName
url = ''
license = 'GNU GPL v2'
isVC90 = sys.version_info > (2, 6)

MANIFEST_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="asInvoker"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>%(extra)s
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
"""

manifest_extra = {
    0: '',
    1: """\
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="x86"
            publicKeyToken="1fc8b3b9a1e18e3b">
      </assemblyIdentity>
    </dependentAssembly>
  </dependency>
""",}

lib_extra = {
    0: [],
    1: [os.path.join(os.path.dirname(AvsP.wx.__file__), 'gdiplus.dll')],
    }

data_files = [
        ('', [
            'filterdb.dat',
            'readme.md',
            'changelog.txt',
            'copying.txt',
            ]
        ),
        ('lib', lib_extra[isVC90]),
        ('src', [
            'run.py',
            'AvsP.py',
            'wxp.py',
            'avisynth.py',
            'pyavs.py',
            'pyavs_avifile.py',
            'AvsP_build.py',
            'AvsP_setup.py',
            'AvsP_i18n.py',
            'AvsP.ico',
            'icons.py',
            'build_instructions.txt',
        ]),
    ]

# Include the Microsoft Visual C runtime DLLs for Python 2.6+
# v9.0.21022.8, available in the Microsoft Visual C++ 2008 Redistributable Package (x86)
# <https://www.microsoft.com/en-us/download/details.aspx?id=29>
if isVC90:
    crt_dst_dir = 'Microsoft.VC90.CRT'
    crt_version = 'x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91'
    crt_files = ('msvcm90.dll', 'msvcp90.dll', 'msvcr90.dll')
    crt_dirs = (os.path.expandvars(os.path.join('%windir%', 'winsxs', crt_version)), 
                sys.prefix, os.path.join(sys.prefix, 'DLLs'))
    crt_paths = []
    for file in crt_files:
        for dir in crt_dirs:
            path = os.path.join(dir, file)
            if os.path.isfile(path):
                crt_paths.append(path)
                break
        else:
            crt_paths.append(file)
#    data_files.append((crt_dst_dir, crt_paths)) # it doesn't seem to work
    data_files.append(('', crt_paths))
# Include MSVCR71.dll for Python 2.5
#else:
#    data_files.append(('', 'msvcr71.dll'))

# If a resource file doesn't exist in the current directory, take it from its parent
for i, (dsr, files) in enumerate(data_files):
    for j, file in enumerate(files):
        if not os.path.isfile(file):
            basename = os.path.basename(file)
            if basename != file and os.path.isfile(basename):
                data_files[i][1][j] = basename
                continue    
            file_up = os.path.join('..', basename)
            if os.path.isfile(file_up):
                data_files[i][1][j] = file_up
            else:
                exit("Couldn't find '%s'" % basename)

# Add whole directories, optionally filtering by extension and including explicitly some files
# If a directory doesn't exist within the current one, search in its parent
dirs = (
    ('help', None, None),
    ('translations', None, None), 
    ('macros', ('.py'), None), 
    ('tools', ('.py', '.presets'), ('avs2avi.exe', 'avs2avi_src.zip'))
       )
for dir, ext_filter, include in dirs:
    if not os.path.isdir(dir):
        dir_up = os.path.join('..', dir)
        if os.path.isdir(dir_up):
            dir = dir_up
        else:
            exit("Couldn't find '%s' directory" % dir)
    data_files.extend(
        [(root.split(os.sep, 1)[1] if root.startswith('..') else root, 
          [os.path.join(root, file) for file in files 
                if (not ext_filter or os.path.splitext(file)[1] in ext_filter or 
                    include and file in include)]
         ) for root, dirs, files in os.walk(dir)])

# Generate the dist files
setup(
    name = appName,
    description = description,
    version = AvsP.version,
    url = url,
    license = license,
    options = {"py2exe":{
        "compressed": True,
        "optimize": 1,
        "includes": ['glob', 'shutil'],
        "excludes": ["translation", "Tkconstants", "Tkinter", "tcl", '_ssl', 'pyreadline'],
        "dll_excludes": ['MSVCP90.dll', 'w9xpopen.exe', 'mswsock.dll', 'powrprof.dll'],
    }},
    zipfile = 'lib/library.zip',
    data_files = data_files,
    windows = [
        {  
            'copyright' : license,
            "script": "run.py",
            "icon_resources": [(1, "AvsP.ico")],
            "other_resources" : [(24, 1, MANIFEST_TEMPLATE % 
                dict(prog=appName, extra=manifest_extra[isVC90])
            )],
        }
    ],
)

# Write the manifest file for the CRT DLLs
if isVC90:
    manifest = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!-- Copyright (c) Microsoft Corporation.  All rights reserved. -->
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <noInheritable/>
    <assemblyIdentity
        type="win32"
        name="Microsoft.VC90.CRT"
        version="9.0.21022.8"
        processorArchitecture="x86"
        publicKeyToken="1fc8b3b9a1e18e3b"
    />
    <file name="msvcr90.dll" /> <file name="msvcp90.dll" /> <file name="msvcm90.dll" />
</assembly>'''
    for i, arg in enumerate(sys.argv):
        if arg.lower() == '-d':
            dist_dir = sys.argv[i+1].strip('"')
            break
        else:
            dir = arg.lower().partition('--dist-dir=')[2]
            if dir:
                dist_dir = dir.strip('"')
                break
    else:
        dist_dir = 'dist'
#    f = open(os.path.join(dist_dir, crt_dst_dir, crt_dst_dir + '.manifest'), 'w') # it doesn't seem to work
    f = open(os.path.join(dist_dir, '', crt_dst_dir + '.manifest'), 'w')
    f.write(manifest)
    f.close()