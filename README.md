# Projecy Overview
The file utility program can be invoked as follows on the console:
  ```
  filelist [options] [directory list]
  ```
The arguments in [ ] are optional. If they are not given, the default action will be carried out. If no directory list is given, the default will be the current directory. If no optional arguments are given, pathnames of all files will be printed by the program.

The following options will be available. Note that if multiple options are present, the files satisfying conditions of all options will be returned (i.e. option conditions are ANDed).

- -before datetime 
  - Files last modified before a date (YYYYMMDD) or a datetime (YYYMMDDTHHMMSS)
- -after datetime
  - Files last modified after a date (YYYYMMDD) or a datetime (YYYMMDDTHHMMSS)
- -match <pattern>
  - Filenames matching a Python regular expression <pattern>
- -bigger <int>
  - Files having sizes greater than or equal to <int> bytes. Note that <int> can also be given as kilobytes, megabytes, and gigabytes, for example as, 2K, 3M, 7G.
- -smaller <int>
  - Files having sizes less than or equal to <int> bytes. Note that <int> can also be given as kilobytes, megabytes, and gigabytes, for example as, 2K, 3M, 7G.
- -delete
  - The files should be deleted.
- -zip <zipfile>
  - The files should be packed as zip file.
- -duplcont
  - Files whose contents are the same should be listed. The listing should be in sorted order with a line of ------ characters separating the duplicate sets of files.
- -duplname
  - Files whose names are the same should be listed. The listing should be in sorted order with a line of ------ characters separating the duplicate sets of files.
- Note that only one of -duplcont or –duplname can be given.
- -stats
  - Traversal statistics should be printed at the end of files listing output. The statistics will be as follows: the total number of files visited, the total size of files visited in bytes, the total number of files listed, the total size of files listed in bytes.
  - If –duplcont option is given, additionally, the following information will be printed: the total number of unique files listed, the total size of unique files in bytes.
  - If –duplname option is given, additionally, the following information will be printed: the total number of files with unique names.
- -nofilelist
  - No file listing will be printed
