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

path_to_cfd_dir = './cfd'
output_dir = './output'
output_base = os.path.abspath(output_dir)
while True:   ## infinite loop to allow people to add files whilst it is running
    files = os.listdir(path_to_cfd_dir)
    fds_files = []
    # base = (os.getcwd(path_to_cfd_dir))
    base = os.path.abspath(path_to_cfd_dir)
    cmd = 'cmd.exe'
    
    for i in files:
        if '.fds' in i:
            fds_files.append(i)
            
    print(fds_files)
    if fds_files == []:   ## if no more files, then stop loop  
        break
    
    for i in fds_files:
        current_file_path = f"{base}/{i}"
        meshes = Count_Meshes(current_file_path)
        print(meshes)
        current_output_path = f"{output_base}/{i[:4]}2" # changed from current_file_path
        # folder_path = current_output_path.replace('.fds','')
        folder_path = current_output_path
        os.mkdir(folder_path)
        dest_dir = folder_path
        src_file = current_file_path
        shutil.copy(src_file, dest_dir)
        # os.remove(current_file_path) # should be removed on mod comp
        string = folder_path
        os.chdir(string)
        progress_file = f'{os.path.abspath("")}/fds_progress2.txt'
        error_file = f'{os.path.abspath("")}/error.txt'
        string2 = str.encode(f"fds_local -p {meshes} -o {32-meshes} {i}\n")

        with open(progress_file, 'a') as log_file:
            with open(error_file, 'a') as error_file:
                # TODO: 
                p = Popen(cmd, stdin=PIPE, stdout=log_file, stderr=error_file, bufsize=1, shell=True)
                p.stdin.write(b"fdsinit\n")
                p.stdin.write(string2)
                p.stdin.close()
                p.wait()    

        os.chdir(base)

