from distutils.core import setup
import os, sys
import py2exe
import AvsP

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

isVC90 = 1 if sys.version > '2.6' else 0
appName = "AvsPmod"

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

root_vc90crt = 'C:\Python27'
root_extra = {
    0: [],
    1: [os.path.join(root_vc90crt, 'msvcr90.dll'),
        os.path.join(root_vc90crt, 'msvcp90.dll'),
        'Microsoft.VC90.CRT.manifest'],
    }
    
lib_extra = {
    0: [],
    1: [os.path.join(os.path.dirname(AvsP.wx.__file__), 'gdiplus.dll')],
    }
    
setup(
    version = AvsP.version,
    description = "%s - an AviSynth script editor" % appName,
    name = appName,
    options = {"py2exe":{
        "compressed": 1,
        "optimize": 2,
        "excludes": ["translation", "Tkconstants", "Tkinter", "tcl"],
        "dll_excludes": ['MSVCP90.dll', 'w9xpopen.exe'],
    }},
    zipfile = 'lib/library.zip',
    data_files = [
        ('', [
            'filterdb.dat',
            '../readme.txt',
            '../translation_readme.txt',
            '../Copying.txt',
            ] + root_extra[isVC90]
        ),
        ('lib', lib_extra[isVC90]),
        ('src', [
            'run.py',
            '__translation_new.py',
            'AvsP.py',
            'wxp.py',
            'avisynth.py',
            'pyavs.py',
            'pyavs_avifile.py',
            'AvsP_build.py',
            'AvsP_setup.py',
            'AvsP_i18n.py',
            'AvsP.ico',
            'Microsoft.VC90.CRT.manifest',
            'icons.py',
            'build_instructions.txt',
        ]),
    ] +
    [(root, [os.path.join(root,name) for name in files]) for root, dirs, files in os.walk('macros')] +
    [(root, [os.path.join(root,name) for name in files]) for root, dirs, files in os.walk('help')] +
    [(root, [os.path.join(root,name) for name in files if os.path.splitext(name)[1] in ('.py', '.presets', '.exe', '.dat')]) for root, dirs, files in os.walk('tools')],
    windows = [
        {
            "script": "run.py",
            "icon_resources": [(1, "AvsP.ico")],
            "other_resources" : [(24, 1, MANIFEST_TEMPLATE % 
                dict(prog=appName, extra=manifest_extra[isVC90])
            )],
        }
    ],
)