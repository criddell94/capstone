'''
#
# runDiffs.py
# Connor Riddell
#
'''
import os
import sys
import re

#------------------------ Set up variables and create directory ----------------------------------

# get wiki name
wiki_name = re.search(r".*_f", sys.argv[1]).group(0)
wiki_name = wiki_name[:-2]

# create new directory name for output files
new_dir    = os.getcwd() + '/' + wiki_name + '_runDiffs_outputs/'

# create new directory if not already made
if not os.path.exists(new_dir):
        os.makedirs(new_dir)

# directory of files to run diff on
files_dir = os.getcwd() + '/' + sys.argv[1]

# add slash if isn't already in path name
if not files_dir[len(files_dir)-1] == '/':
    files_dir = files_dir + '/'

# number of files in directory
path, dirs, files = os.walk(files_dir).next()
file_amount = len(files)/2

# start number
file_num = 1

#----------------------------- Main loop to run diff on all the files --------------------------------

while file_num <= file_amount:
    print "Creating file #" + str(file_num) + " ..."
    
    # create file path names
    file1 = files_dir + "changePREVTEXT." + str(file_num)
    file2 = files_dir + "changeTEXT." + str(file_num)
    out_file = new_dir + "change_breakdown." + str(file_num)
    
    # run diff on them
    os.system("diff " + file1 + " " + file2 + " > " + out_file)

    file_num += 1

# end script

