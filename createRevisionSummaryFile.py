# -*- coding: utf-8 -*-
'''
#
# createRevisionSummaryFile.py 
# Connor Riddell
# Creates files with amount of revisions and previous and recurrent file number on each line
# 
'''

import sys
import os
from difflib import ndiff

# input for folder with all revision files
rev_dir    = sys.argv[1]

#
# Calculate revision between two files
# Args: file_num (int) 
# Return: revision amount (int)
#
def get_revision(file_num):
    prev_text   = "" # text from first file 
    curr_text   = "" # text from second file
 
    # open previous file and get lines
    with open(rev_dir + str(file_num) + "_revision.txt") as f:
        prev_text = f.readlines()
    f.close()

    # open next file (the revision)    
    with open(rev_dir + str(file_num+1) + "_revision.txt") as f:
        curr_text = f.readlines()
    f.close()

    # total amount of revisions in file & current amount
    revision_total = 0
    line_num = 1

    #check each line in the file
    for line in range(0, min(len(prev_text),len(curr_text))): 
        # calculate difference between files
        diff = list(ndiff(prev_text[line],curr_text[line]))
        
        # count number of + and - in file 
        for char in range(0, len(diff)):
            if diff[char][0] == "+" or diff[char][0] == "-":
                revision_total += 1
        #end inner for
        
        line_num += 1
    # end outter for
    return revision_total
#end get_revision

#
# Main to loop over revision files and make summary file
#
def main():
    #make array of revision files ddin director
    
    rev_f_amount = len(os.listdir(rev_dir))
   
    f = open(rev_dir[:2] + '_revisions_summary.txt', 'w+')
  
    # loop over files and print to file
    for count in range(27000,rev_f_amount):
        print count
        revis_total = get_revision(count)

        f.write(str(revis_total) + ' - prev: ' + str(count) + ' curr: ' + str(count+1) + '\n')
        print count
        #if count % 1000 == 0:
        #    print count 
    #end for
    f.close()
#end main

main()
