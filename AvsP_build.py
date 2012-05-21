# Build script for AvsP
# Dependencies:
#     Python (tested with v2.4.2)
#     py2exe (tested with v0.6.5)
# Scripts:
#     AvsP_setup.py
#     AvsP_i18n.py
#     AvsP.py

import os
import shutil
import zipfile
import subprocess
import AvsP
import AvsP_i18n

def main():
    # Define names and paths
    pythonexe = r'D:\Programs\Python25\python.exe'
    upx = r'D:\Programs\upx\upx.exe'
    programdirname = 'AvsP'
    zipname = 'AvsP_v%s.zip' % AvsP.version
    if os.path.isdir(programdirname):
        shutil.rmtree(programdirname)

    # Make the translation file
    if not AvsP_i18n.main():
        return
        
    # Create the program executable using py2exe
    os.system('%s -OO AvsP_setup.py py2exe' % pythonexe)
    
    # Compress the files with UPX
    for dir in ('dist', 'dist\lib'):
        for name in os.listdir(dir):
            if os.path.splitext(name)[1] in ('.exe','.dll','.pyd'):
                print 'Compressing '+name+'...'
                #~ os.spawnl(os.P_WAIT,upx,'0',os.path.join(dir,name),'--lzma','--best')
                subprocess.call([upx, os.path.join(dir,name), '--lzma', '--best'], shell=True)
                
    # Manage the files
    os.rename('dist\\run.exe', 'dist\\AvsP.exe')
    shutil.copytree('dist', programdirname)
    shutil.rmtree('build')
    shutil.rmtree('dist')
    
    # Create the zip file for distribution
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