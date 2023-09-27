import os
import re
'''
    TODO: how to allow change in order of runs in folder?
    easiest way would be to change name of file
    other way to have external file storing order of runs
    that can be changed; and then read by fds code
    fds code removes file name from list after run
'''
def read_progress(output_folder_path):
    folders = os.listdir(output_folder_path)
    progress_object = {}
    for folder in folders:
        progress_object[folder] = {}
        # find progress file
        folder_path = f'{output_folder_path}/{folder}'
        files = os.listdir(folder_path)
        progress_file_path = f'{folder_path}/fds_progress.txt'
        has_started = False
        time_progress = None
        has_progress_file = False
        total_sim_time = None 
        starting_date = None

        from datetime import datetime

        if os.path.exists(progress_file_path):
            has_progress_file = True
            with open (progress_file_path, "r") as myfile:
                data = myfile.read().splitlines()
                starting_lines = [f for f in data if  'Current Date' in f]
                if len(starting_lines) > 0:
                    starting_line = starting_lines[0]
                    # Use regular expression to extract the date-time string
                    match = re.search(r'(\w+ \d+, \d+  \d+:\d+:\d+)', starting_line)
                    if match:
                        date_time_str = match.group(1)
                        
                        # Parse the date-time string into a datetime object
                        starting_date = datetime.strptime(date_time_str, '%B %d, %Y  %H:%M:%S') 

                time_lines = [f for f in data if 'Simulation Time' in f]
                if len(time_lines) > 0:
                    has_started = True
                    latest_time_line = time_lines[-1]
                    regex = r'\d+\.?\d*'
                    time_progress = re.findall(regex, latest_time_line)[-1]
                    

        # read fds for total sim time
        fds_file = [f for f in files if '.fds' in f]
        if len(fds_file) > 0:
            fds_file_path = f'{folder_path}/{fds_file[0]}'
            with open (fds_file_path, "r") as myfile:
                data = myfile.read().splitlines()
                time_lines = [f for f in data if 'T_END' in f]
                if len(time_lines) > 0:
                    total_sim_time = re.findall(r'\d+', time_lines[0])[0]

        progress_object[folder]['starting_time'] = starting_date
        progress_object[folder]['total_time'] = total_sim_time
        progress_object[folder]['has_started'] = has_started
        progress_object[folder]['time'] = time_progress
        progress_object[folder]['has_progress_file'] = has_progress_file
        # store time started, finished and total duration
        
    projects = list(progress_object.keys())
    progress_list = []
    for project in projects:
        temp = progress_object[project]
        temp['name'] = project
        progress_list.append(temp)
    return progress_list


read_progress('./output')