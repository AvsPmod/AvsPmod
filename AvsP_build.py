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
import zipfile
import subprocess
import AvsP
import AvsP_i18n

def main():
    # Define names and paths
    pythonexe = os.path.join(sys.prefix, 'python.exe')
    upx = 'upx.exe'
    programdirname = 'AvsPmod'
    zipname = 'AvsPmod_v%s.zip' % AvsP.version
    if os.path.isdir(programdirname):
        shutil.rmtree(programdirname)
        
    # Check if current dir contains filterdb.dat, help, macros and tools
    for dst in ['filterdb.dat', 'help', 'macros', 'tools']:
        if not os.path.exists(dst):
            src = '../' + dst
            if os.path.isfile(src):
                shutil.copyfile(src, dst)
            elif os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                print "file/dir '%s' not found" % dst
                return

    # Make the translation file
    if not AvsP_i18n.main():
        return

    # Create the program executable using py2exe
    os.system('%s -OO AvsP_setup.py py2exe' % pythonexe)
    
    # Compress the files with UPX
    if os.system(upx + ' -V') == 0:
        for dir in ('dist', 'dist\\lib'):
            for name in os.listdir(dir):
                if os.path.splitext(name)[1] in ('.exe','.dll','.pyd'):
                    print 'Compressing '+name+'...'
                    #~ os.spawnl(os.P_WAIT,upx,'0',os.path.join(dir,name),'--lzma','--best')
                    subprocess.call([upx, os.path.join(dir,name), '--lzma', '--best', '--no-progress'], shell=True)
            
    # Manage the files
    os.rename('dist\\run.exe', 'dist\\AvsPmod.exe')
    shutil.copytree('dist', programdirname)
    shutil.rmtree('build')
    shutil.rmtree('dist')

    # Create the zip file for distribution
    exe7z = os.path.join(os.environ['PROGRAMFILES'], '7-zip/7z.exe')
    if os.path.exists(exe7z):
        zipname = zipname.replace('.zip', '.7z')
        if os.path.isfile(zipname):
            os.remove(zipname)
        subprocess.call([exe7z, 'a', '-bd', '-r', zipname, programdirname])
        return
        
    if os.path.isfile(zipname):
        os.remove(zipname)
    zip = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(programdirname):
        for name in files:
            zip.write(os.path.join(root, name))
    zip.close()
    
if __name__ == '__main__':
    main()
    raw_input('Press enter to continue')
