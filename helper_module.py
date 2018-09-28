import os
import time
import datetime


# returns list that containing files in the running_directory usings stack.
def directory_traversal(running_directory):
    files_list = []
    directory_stack = [running_directory]
    while directory_stack:
        current_dir = directory_stack.pop()
        if os.path.exists(current_dir):
            read_access = os.access(current_dir, os.R_OK)
            if read_access:
                dir_contents = os.listdir(current_dir)
                for name in dir_contents:
                    current_item = current_dir + "/" + name
                    if os.path.isdir(current_item):
                        directory_stack.append(current_item)
                    else:
                        files_list.append(current_item)
            else:
                print "No read access for ", current_dir
                quit()
        else:
            print current_dir, "is not exist!"

    return files_list


# convert given date string to unix time
def date_string_to_unix_timestamp(v):
    if len(v) > 8:
        # YYYYMMDD case
        try:
            start = datetime.datetime(int(v[0:4]), int(v[4:6]), int(v[6:8]), int(v[9:11]), int(v[11:13]), int(v[13:]))
            before_time = time.mktime(start.timetuple())
            return before_time
        except ValueError:
            print "Wrong time format"
            quit()
    else:
        # YYYYMMDDTHHMMSS case
        try:
            start = datetime.datetime(int(v[0:4]), int(v[4:6]), int(v[6:]))
            before_time = time.mktime(start.timetuple())
            return before_time
        except ValueError:
            print "Wrong time format"
            quit()


# convert given string to the bytes
def size_string_to_bytes(s):
    if s[-1] == 'K':  # kilobytes
        return int(int(s[:-1]) * 1024)
    elif s[-1] == 'M':  # megabytes
        return int(int(s[:-1]) * 1024 * 1024)
    elif s[-1] == 'G':  # gigabytes
        return int(int(s[:-1]) * 1024 * 1024 * 1024)
    else:
        return int(s)


# return total size of files in files_list
def find_total_size_of_files(files_list):
    total_size = 0
    for f in files_list:
        total_size += os.path.getsize(f)
    return total_size


# return total number of file_list according to given check_bool
def number_of_files(l, check_bool):
    counter = 0
    for e in l:
        if e is check_bool:
            counter += 1
    return counter


# return total size of file_list according to given check_bool
def size_of_files(bool_list, file_list, check_bool):
    total_size = 0
    for index in range(len(file_list)):
        if bool_list[index] is check_bool:
            total_size += os.path.getsize(file_list[index])
            # print file_list[index],os.path.getsize(file_list[index])
    return total_size


# print given statistics
def print_given_stats(totalNumberOfFileVisited, totalSizeOfFilesVisited, totalNumberOfFileListed,
                      totalSizeOfFilesListed):
    print "Total number of files visited: ", totalNumberOfFileVisited
    print "Total size of files visited in bytes: ", totalSizeOfFilesVisited
    print "Total number of files listed: ", totalNumberOfFileListed
    print "Total size of files listed in bytes: ", totalSizeOfFilesListed


# return true when we have duplicate files in files_list after index index
def check_duplicates_in_zipfile(index, files_list, current_file):
    my_range = range(index, -1, -1)[1:]
    for i in my_range:
        if os.path.basename(files_list[i]) == os.path.basename(current_file):
            return True
    return False
