# Build script for AvsP
# Dependencies:
#     Python
#     py2exe
# Scripts:
#     AvsP_setup.py
#     AvsP_i18n.py
#     AvsP.py

import os
import sys
import shutil
import tempfile
import zipfile
import subprocess
import AvsP
import AvsP_i18n

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
    programdirname = 'AvsPmod'
    zipname = 'AvsPmod_v%s.zip' % AvsP.version
    upx = os.path.join(os.environ['PROGRAMFILES'], 'upx', 'upx.exe')
    exe7z = os.path.join(os.environ['PROGRAMFILES'], '7-Zip', '7z.exe')
    editbin = os.path.join(os.environ['PROGRAMFILES'], 'Microsoft Visual Studio 10.0', 
                          'VC', 'bin', 'amd64', 'editbin.exe')
    tempdir = tempfile.mkdtemp()
    programdirname = os.path.join(tempdir, programdirname)
    
    # Create/update the master translation file
    if not AvsP_i18n.main():
        return
    
    # Create the program executable using py2exe
    if os.system('""%s" -OO AvsP_setup.py py2exe -d %s"' % (pythonexe, programdirname)):
        return
    
    # Update the translation files in the temporal subdirectory
    AvsP_i18n.UpdateTranslationFile(os.path.join(programdirname, 'translations'), version=AvsP.version)
    
    # Create/update 'macros_readme.txt' in the macros subdirectory
    AvsP.GenerateMacroReadme(os.path.join(programdirname, 'macros', 'macros_readme.txt'))
    
    # Set the large address aware flag in the executable
    if not os.path.isfile(editbin):
        editbin = isinpath('editbin.exe')
    if editbin:
        print '\nSetting large address aware flag...'
        if os.system('""%s" /LARGEADDRESSAWARE "%s""' % (editbin, os.path.join(programdirname, 'run.exe'))):
            print 'Failed'
    else:
        print "\neditbin not found.  Large address aware flag not set"
    
    # Compress the files with UPX, if available
    if not os.path.isfile(upx):
        upx = isinpath('upx.exe')
    if upx:
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
              os.path.join(programdirname, 'AvsPmod.exe'))
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
