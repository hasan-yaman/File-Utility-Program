#!/usr/bin/env python

import helper_module
import os
import sys
import zipfile
import filecmp
import re

commandLineArguments = sys.argv  # get command line arguments
optionsDic = dict()  # create empty dictionary
directoryList = []  # create empty list
iterable_commandLineArguments = iter(commandLineArguments[1:])
# iterate over the command line arguments
for args in iterable_commandLineArguments:
    # if we have option
    if args[0] == '-':
        # if we have option that have a argument
        if args == '-before' or args == '-after' or args == '-bigger' or args == '-smaller' or args == '-zip' or args == '-match':
            secondArg = ""
            try:
                secondArg = iterable_commandLineArguments.next()  # get argument of option
            except StopIteration:
                print args, "must have argument!"
                quit()
            if os.path.isdir(secondArg) or secondArg[0] == '-':  # if it is not an argument, print error
                print "Syntax error.(No arguments for given option/options)"
                quit()
            else:
                optionsDic[args] = secondArg
        else:
            optionsDic[args] = ''
    else:
        directoryList.append(args)

if len(directoryList) == 0:  # if no directory list is given, add current directory to the list
    directoryList.append(os.getcwd())

# print optionsDic
# print directoryList

files_list = []  # create empty list that containing files

# add files that in the directoryList to files_list
for dirs in directoryList:
    files_list.extend(helper_module.directory_traversal(dirs))

print_normal_output = True  # true when we don't have -duplname or -duplcont options
print_no_file_list = False  # true when we have -nofilelist option
print_statistics = False  # true when we have -stats option
totalNumberOfFileVisited = 0  # to keep track of number of files visited
totalSizeOfFilesVisited = 0  # to keep track of size  of files visited
if '-duplname' in optionsDic.keys() and '-duplcont' in optionsDic.keys():
    # print error
    print "Error!Only one of -duplname or -duplcont can be given."
    quit()
if '-stats' in optionsDic.keys():
    # get statistics about visited files
    print_statistics = True
    totalNumberOfFileVisited = len(files_list)
    totalSizeOfFilesVisited = helper_module.find_total_size_of_files(files_list)
if '-nofilelist' in optionsDic.keys():
    # in this case no file listing will be printed
    print_no_file_list = True
# for every file fil in the files_list perform options
for fil in files_list[:]:
    for k, v in optionsDic.iteritems():
        if fil in files_list:
            if k == '-before':
                modificationTime = int(os.path.getmtime(fil))  # find modification time of file
                beforeTime = helper_module.date_string_to_unix_timestamp(v)  # convert given time formant to unix time
                if modificationTime >= beforeTime:
                    files_list.remove(fil)  # delete item
            elif k == '-after':
                modificationTime = int(os.path.getmtime(fil))  # find modification time of file
                afterTime = helper_module.date_string_to_unix_timestamp(v)  # convert given time formant to unix time
                if modificationTime <= afterTime:
                    files_list.remove(fil)  # delete item
            elif k == '-bigger':
                fileSize = os.path.getsize(fil)  # find size of the file
                biggerSize = helper_module.size_string_to_bytes(v)  # convert given size to the bytes
                if fileSize < biggerSize:
                    files_list.remove(fil)  # delete item
            elif k == '-smaller':
                fileSize = os.path.getsize(fil)  # find size of the file
                smallerSize = helper_module.size_string_to_bytes(v)  # convert given size to the bytes
                if fileSize > smallerSize:
                    files_list.remove(fil)  # delete item
            elif k == '-match':
                found = re.search(v, os.path.basename(fil))  # look for given pattern
                if not found:  # if given pattern is not found delete file from files_list
                    files_list.remove(fil)

if '-zip' in optionsDic.keys():
    # if we have zip option, create zip file in current directory
    zipFileName = optionsDic['-zip'] + ".zip"
    zipFile = zipfile.ZipFile(zipFileName, "w")
    # add created zip file to the files
    # if we have duplicate files names, change the name of the file.
    zipFileCounter = 1
    for index, fil in enumerate(files_list):
        if helper_module.check_duplicates_in_zipfile(index, files_list, fil):  # to eliminate duplicate elements in zip
            zipFile.write(fil, os.path.basename(fil) + "(" + str(zipFileCounter) + ")")
            zipFileCounter += 1
        else:
            zipFile.write(fil, os.path.basename(fil))  # to eliminate absolute path in zip archive
    zipFile.close()
if '-duplcont' in optionsDic.keys():
    # if we have duplcont option, find files that have the same content
    print_normal_output = False
    bool_list = []
    for i in range(len(files_list)):
        bool_list.append(False)
    for i in range(len(files_list)):
        files_with_same_content = [files_list[i]]
        for j in range(i + 1, len(files_list)):
            if bool_list[j] is False and filecmp.cmp(files_list[i], files_list[j]):
                files_with_same_content.append(files_list[j])
                bool_list[i], bool_list[j] = True, True
        if len(files_with_same_content) > 1 and not print_no_file_list:
            # print files with sorted order by file name
            files_with_same_content.sort(key=os.path.basename)
            print "\n".join(files_with_same_content)
            print "------"
    if print_statistics:
        # if we have -stats option, print statistics
        if print_no_file_list:  # in this case, no file will be listed
            totalNumberOfUniqueFileListed = 0
            totalSizeOfUniqueFileListed = helper_module.size_of_files(bool_list, files_list, False)
            totalNumberOfFileListed = 0
            totalSizeOfFilesListed = 0
            helper_module.print_given_stats(totalNumberOfFileVisited, totalSizeOfFilesVisited,
                                            totalNumberOfFileListed, totalSizeOfFilesListed)
            print "Total number of unique files listed: ", totalNumberOfUniqueFileListed
            print "Total size of unique files in bytes: ", totalSizeOfUniqueFileListed
        else:
            totalNumberOfUniqueFileListed = helper_module.number_of_files(bool_list, False)
            totalSizeOfUniqueFileListed = helper_module.size_of_files(bool_list, files_list, False)
            totalNumberOfFileListed = helper_module.number_of_files(bool_list, True)
            totalSizeOfFilesListed = helper_module.size_of_files(bool_list, files_list, True)
            helper_module.print_given_stats(totalNumberOfFileVisited, totalSizeOfFilesVisited,
                                            totalNumberOfFileListed, totalSizeOfFilesListed)
            print "Total number of unique files listed: ", totalNumberOfUniqueFileListed
            print "Total size of unique files in bytes: ", totalSizeOfUniqueFileListed
if '-duplname' in optionsDic.keys():
    # if we have duplcont option, find files that have the same name
    print_normal_output = False
    bool_list = []
    files_list.sort(key=os.path.basename)  # sort files by their name
    for i in range(len(files_list)):
        bool_list.append(False)
    for i in range(len(files_list)):
        files_with_same_name = [files_list[i]]
        for j in range(i + 1, len(files_list)):
            if bool_list[j] is False and os.path.basename(files_list[i]) == os.path.basename(files_list[j]):
                files_with_same_name.append(files_list[j])
                bool_list[i], bool_list[j] = True, True
        if len(files_with_same_name) > 1 and not print_no_file_list:
            print "\n".join(files_with_same_name)
            print "------"
    if print_statistics:
        # if we have -stats option, print statistics
        totalNumberOfUniqueNameFiles = helper_module.number_of_files(bool_list, False)
        if print_no_file_list:  # in this case, no file will be listed
            totalNumberOfFileListed = 0
            totalSizeOfFilesListed = 0
            helper_module.print_given_stats(totalNumberOfFileVisited, totalSizeOfFilesVisited,
                                            totalNumberOfFileListed, totalSizeOfFilesListed)
            print "Total number of files with unique names: ", totalNumberOfUniqueNameFiles
        else:
            totalNumberOfFileListed = helper_module.number_of_files(bool_list, True)
            totalSizeOfFilesListed = helper_module.size_of_files(bool_list, files_list, True)
            helper_module.print_given_stats(totalNumberOfFileVisited, totalSizeOfFilesVisited,
                                            totalNumberOfFileListed, totalSizeOfFilesListed)
            print "Total number of files with unique names: ", totalNumberOfUniqueNameFiles

if '-delete' in optionsDic.keys():  # if we have delete option delete all the files in files_list
    for fil in files_list:
        os.remove(fil)
# print output such as files list, statistics
if print_normal_output:
    if not print_no_file_list:
        print "\n".join(files_list)
    if print_statistics:
        if print_no_file_list:  # in this case no file list will be printed
            totalNumberOfFileListed = 0
            totalSizeOfFilesListed = 0
            helper_module.print_given_stats(totalNumberOfFileVisited, totalSizeOfFilesVisited,
                                            totalNumberOfFileListed, totalSizeOfFilesListed)
        else:
            totalNumberOfFileListed = len(files_list)
            totalSizeOfFilesListed = helper_module.find_total_size_of_files(files_list)
            helper_module.print_given_stats(totalNumberOfFileVisited, totalSizeOfFilesVisited,
                                            totalNumberOfFileListed, totalSizeOfFilesListed)
