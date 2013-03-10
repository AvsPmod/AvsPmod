# AvsP - an AviSynth editor
# 
# Copyright 2007 Peter Jang <http://www.avisynth.org/qwerpoi>
#           2010-2013 the AvsPmod authors <https://github.com/avspmod/avspmod>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA, or visit
#  http://www.gnu.org/copyleft/gpl.html .

# build - build script for AvsP
#
# Dependencies:
#     Python (tested on v2.6 and v2.7)
#     wxPython (tested on v2.8 Unicode and v2.9)
#     py2exe (tested on v0.6.9)

import os
import sys
import shutil
import tempfile
import zipfile
import subprocess

import avsp
import i18n
import global_vars

def isinpath(path):
    '''Check if a file is in PATH or in the working directory'''
    basename = os.path.basename(path)
    path = os.path.join(os.getcwdu(), basename)
    if os.path.isfile(path):
        return path
    for dir in os.environ['PATH'].split(os.pathsep):
        path = os.path.join(dir, basename)
        if os.path.isfile(path):
            return path

def main():
    # Define names and paths
    pythonexe = sys.executable
    zipname = '{0}_v{1}.zip'.format(global_vars.name, global_vars.version)
    upx = os.path.join(os.environ['PROGRAMFILES'], 'upx', 'upx.exe')
    exe7z = os.path.join(os.environ['PROGRAMFILES'], '7-Zip', '7z.exe')
    editbin = os.path.join(os.environ['PROGRAMFILES'], 'Microsoft Visual Studio 10.0', 
                          'VC', 'bin', 'editbin.exe')
    tempdir = tempfile.mkdtemp()
    programdirname = os.path.join(tempdir, global_vars.name)
    
    # Create/update the master translation file
    print '\nCreating translation file...'
    if not i18n.main():
        return
    
    # Create the program executable using py2exe
    if os.system('""%s" -OO setup.py py2exe -d %s"' % (pythonexe, programdirname)):
        return
    
    # Update the translation files in the temporal subdirectory
    i18n.UpdateTranslationFile(os.path.join(programdirname, 'translations'), version=global_vars.version)
    
    # Create/update 'macros_readme.txt' in the macros subdirectory
    avsp.GenerateMacroReadme(os.path.join(programdirname, 'macros', 'macros_readme.txt'))
    
    # Set the large address aware flag in the executable
    if not os.path.isfile(editbin):
        editbin = isinpath('editbin.exe')
    if editbin:
        mspdb100_dir = os.path.join(os.environ['PROGRAMFILES'], 'Microsoft Visual Studio 10.0', 
                                    'Common7', 'IDE')
        if os.path.isdir(mspdb100_dir):
            os.environ['PATH'] += os.pathsep + mspdb100_dir
        print '\nSetting large address aware flag...'
        if os.system('""%s" /LARGEADDRESSAWARE "%s""' % (editbin, os.path.join(programdirname, 'run.exe'))):
            print 'Failed'
    else:
        print "\neditbin not found.  Large address aware flag not set"
    
    # Compress the files with UPX, if available
    if not os.path.isfile(upx):
        upx = isinpath('upx.exe')
    if upx and not __debug__:
        for root, dirs, files in os.walk(programdirname):
            for file in files:
                if os.path.splitext(file)[1] in ('.exe','.dll','.pyd'):
                    print '\nCompressing '+file+'...'
                    #~ os.spawnl(os.P_WAIT,upx,'0',os.path.join(dir,name),'--lzma','--best')
                    subprocess.call([upx, os.path.join(root, file), '--lzma', '--best', '--no-progress'], shell=True)
    else:
        print "\nUPX not found"
    
    # Manage the files
    os.rename(os.path.join(programdirname, 'run.exe'), 
              os.path.join(programdirname, '{0}.exe'.format(global_vars.name)))
    os.rename(os.path.join(programdirname, 'README.md'), 
              os.path.join(programdirname, 'readme.txt'))
    shutil.rmtree('build')

    # Create the zip file for distribution.  Use 7-Zip if available
    if not os.path.isfile(exe7z):
        exe7z = isinpath('7z.exe')
    if exe7z:
        print '\nCreating 7z archive...'
        zipname = zipname.replace('.zip', '.7z')
        if os.path.isfile(zipname):
            os.remove(zipname)
        subprocess.call([exe7z, 'a', '-bd', '-r', zipname, programdirname])
    else:
        print '\nCreating ZIP archive...'
        if os.path.isfile(zipname):
            os.remove(zipname)
        zip = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(programdirname):
            for name in files:
                real_path = os.path.join(root, name)
                archive_path = os.path.relpath(real_path, tempdir)
                zip.write(real_path, archive_path)
        zip.close()
    shutil.rmtree(tempdir)
    
if __name__ == '__main__':
    main()
    raw_input('\nPress enter to continue')
