# -*- coding: utf-8 -*-
"""
Created on Tue May  3 09:17:18 2022

@author: sambe
"""

import os
import shutil
from subprocess import Popen, PIPE

def Count_Meshes(filename):
    filename = open(filename)
    data = filename.read()
    occurrences = data.count("&MESH ID=")    
    return int(occurrences)

while True:   ## infinite loop to allow people to add files whilst it is running
    files = os.listdir()
    fds_files = []
    base = (os.getcwd())
    cmd = 'cmd.exe'
    
    for i in files:
        if '.fds' in i:
            fds_files.append(i)
            
    print(fds_files)
    if fds_files == []:   ## if no more files, then stop loop  
        break
    
    for i in fds_files:
        meshes = Count_Meshes(i)
        print(meshes)
        foldername = i.replace('.fds','')
        os.mkdir(f"{foldername}")
        dest_dir = f"{foldername}" 
        src_file = f"{i}"
        shutil.copy(src_file, dest_dir)
        os.remove(f"{i}")
        string = f"{base}/{foldername}"
        os.chdir(string)
        string2 = str.encode(f"fds_local -p {meshes} -o {32-meshes} {i}\n")
        p = Popen(cmd, stdin=PIPE , stdout=PIPE, bufsize=0, shell=True)  
        p.stdin.write(b"fdsinit\n")
        p.stdin.write(string2)
        p.stdin.close()
        p.wait();
        os.chdir(base)
    
# import os
# import shutil
# from subprocess import Popen, PIPE

import os
import shutil
from subprocess import Popen, PIPE

while True:
    files = os.listdir()
    fds_files = []
    base = os.getcwd()
    cmd = 'cmd.exe'

    for i in files:
        if '.fds' in i:
            fds_files.append(i)

    print(fds_files)

    if fds_files == []:
        break

    for i in fds_files:
        meshes = Count_Meshes(i)
        print(meshes)
        foldername = i.replace('.fds', '')
        os.mkdir(f"{foldername}")
        dest_dir = f"{foldername}"
        src_file = f"{i}"
        shutil.copy(src_file, dest_dir)
        os.remove(f"{i}")
        string = f"{base}/{foldername}"
        os.chdir(string)
        # TODO: get total sim time from fds file

        with open('fds_progress.txt', 'a') as log_file:
            string2 = str.encode(f"fds_local -p {meshes} -o {32-meshes} {i}\n")
            p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1, shell=True, universal_newlines=True)
            p.stdin.write("fdsinit\n")
            p.stdin.write(string2)
            p.stdin.close()

            # Read output line by line, and print it to console and write it to the log file
            # TODO: update progress object in log file
            # start time; total sim time; progress
            # get current progress; if changed from last update
            # wait 10 secs between checking?
            for line in p.stdout:
                # if sim time > current sim time => change object
                print(line.strip())  # Print to console
                log_file.write(line)  # Write to log file

            p.wait()

        os.chdir(base)
