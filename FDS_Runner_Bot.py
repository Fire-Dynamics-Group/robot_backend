# -*- coding: utf-8 -*-
"""
Created on Tue May  3 09:17:18 2022

@author: sambe
"""

import os
import shutil
from subprocess import Popen, PIPE, STDOUT

def Count_Meshes(filename):
    filename = open(filename)
    data = filename.read()
    occurrences = data.count("&MESH ID=")    
    return int(occurrences)

spare_cfd_dir = './spare_cfd' # used for testing - copied across to dropbox
path_to_cfd_dir = r'C:\Users\IanShaw\Dropbox\CFD_queue' # dropbox folder
run_dir = './cfd_run' # fast hard drive - queued jobs
run_base = os.path.abspath(run_dir)
'''
    # TODO: copy over from spare_cfd to dropbox

'''
output_dir = r'C:\Users\IanShaw\Dropbox\CFD_completed' # final location - completed jobs - dropbox folder
output_base = os.path.abspath(output_dir)
isTesting = True
# if isTesting:
#     # TODO: delete all files in dropbox
#     base_remove = os.path.abspath(path_to_cfd_dir)

#     for filename in os.listdir(base_remove):
#         file_path = os.path.join(base_remove, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except Exception as e:
#             print('Failed to delete %s. Reason: %s' % (file_path, e))

#     # copy over from spare_cfd to dropbox/prequeue
#     base = os.path.abspath(spare_cfd_dir)
#     files_to_copy = os.listdir(spare_cfd_dir)
#     for file in files_to_copy:
#         src_file = f'{base}/{file}'
#         dest_dir = path_to_cfd_dir
#         shutil.copy(src_file, dest_dir)

    # TODO: delete all files in fast hard drive/queue that are in the prequeue if testing


while True:   ## infinite loop to allow people to add files whilst it is running
    # TODO: transfer files from dropbox/prequeue to fast hard drive
    files = os.listdir(path_to_cfd_dir)
    fds_files = []
    # base = (os.getcwd(path_to_cfd_dir))
    base = os.path.abspath(path_to_cfd_dir)
    cmd = 'cmd.exe'
    
    ''' TODO: how to allow reordering of files to be ran?'''
    for i in files:
        if '.fds' in i:
            fds_files.append(i)
            
    print(fds_files)
    if fds_files == []:   ## if no more files, then stop loop  
        break
    
    for i in fds_files: # read order from external source?
        current_file_path = f"{base}/{i}"
        
        meshes = Count_Meshes(current_file_path)
        print(meshes)
        current_output_path = f"{run_base}/{i[:4]}" # changed from current_file_path
        # folder_path = current_output_path.replace('.fds','')
        folder_path = current_output_path
        os.mkdir(folder_path)
        dest_dir = folder_path
        src_file = current_file_path
        # TODO: try and catch for file already existing -> add number to end of file
        shutil.move(src_file, dest_dir)
        string = folder_path
        os.chdir(string)
        progress_file = f'{os.path.abspath("")}/fds_progress.txt'
        error_file = f'{os.path.abspath("")}/error.txt'
        string2 = str.encode(f"fds_local -p {meshes} -o {32-meshes} {i}\n")

        if not isTesting: # does not run fds sim if testing
            with open(progress_file, 'a') as log_file:
                with open(error_file, 'a') as error_file:
                    # TODO: 
                    p = Popen(cmd, stdin=PIPE, stdout=log_file, stderr=error_file, bufsize=1, shell=True)
                    p.stdin.write(b"fdsinit\n")
                    p.stdin.write(string2)
                    p.stdin.close()
                    p.wait()    
        os.chdir(base)
        # TODO: copy over from dropbox to fast hard drive
        # TODO: transfer to output folder - run in output folder
        original = dest_dir
        target = output_base
        shutil.move(original, target)
        

