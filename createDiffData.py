# -*- coding: utf-8 -*-
'''
#
# createDiffData.py 
# Connor Riddell
# 
'''

import sys
import string
import re
import os
import re
from difflib import ndiff

#------------- Set Up -------------#

# user input file name to be parsed
rev_dir    = sys.argv[1]
revis_file_num = sys.argv[2]
#gv_words   = []
#bi_words   = []
is_words   = []

# open language word list
#with open("gv_word_list.txt") as word_f:
#with open("bi_word_list_lower.txt") as word_f:
with open("is_word_list_lower.txt") as word_f:
    words = word_f.readlines()
word_f.close()

for word in words:
    is_words.append(word.rstrip())
#end for

#------------- Functions -------------#

#
# Function to calculate diff between two files
# Arg: (int) file number
# Return: N/A
#
def get_revision(file_num):
    prev_text       = "" # prevision revision to compare to current revision
    curr_text       = ""
    revision_total  = 0
    
    # open previous file
    with open(rev_dir + str(file_num) + "_revision.txt") as f:
        prev_text = f.readlines()
    f.close()
    
    # open new file (revised file)
    with open(rev_dir + str(file_num+1) + "_revision.txt") as f:
        curr_text = f.readlines()
    f.close()
    
    diff = ""
    line_num = 1
    
    # set up variables to written in file
    changed_words = ["",""]
    changed_chars = ""
    prev_llen = 0
    new_llen = 0
    change_dist = 0
    add_delete = "0"
    
    # loop over each line of file and calculate diff
    for line in range(0, min(len(prev_text),len(curr_text))): 
        # calculate diff
        diff = list(ndiff(prev_text[line].decode('utf8'),curr_text[line].decode('utf8')))

        # find + and - changes in diff
        times_inside = 0
        for char in range(0, len(diff)):
            if diff[char][0] == "+" or diff[char][0] == "-":
                revision_total += 1
                
                # what to do if first time inside
                if times_inside == 0:

                    # calcate word by diff indexes (previous index)
                    prev_index = char
                    run = True
                    while run:
                        if prev_index == 0:
                            run = False
                        elif not diff[prev_index-1][2].isalpha():
                            if diff[prev_index-1][2] == '-':
                                prev_index -= 1
                            elif (diff[prev_index-1] == '-  ') or (diff[prev_index-1] == '+  '):
                                prev_index -= 1
                                run = False
                            else:
                                run = False
                        else:
                             prev_index -= 1
                    
                    # calcate word by diff indexes (post index index)
                    post_index = char
                    run = True
                    while run:
                        if post_index == len(diff)-1:
                            run = False
                        elif not diff[post_index+1][2].isalpha():
                            if diff[post_index+1][2] == "-":
                                post_index += 1
                            elif (diff[post_index+1] == '-  ') or (diff[post_index+1] == '+  '):
                                post_index += 1
                                run = False
                            else:
                                run = False
                        else:
                            post_index += 1

                    prev_word = ""
                    new_word = ""
                    in_plus = False
                    in_minus = False
                    first_round = True
                    first_index = 0
                    last_round = 0
                    round_num = 0
                    
                    # put indexes together to get words 
                    for index in diff[prev_index:post_index+1]:
                        if index[0] == '-':
                            in_minus = True

                            if first_round:
                                first_index = round_num

                            first_round = False
                            last_round  = round_num

                            prev_word = prev_word + index[2]
                            if index[2] == '\n':
                                changed_chars = changed_chars + '\\n'
                            else:
                                changed_chars = changed_chars + index[2]
                        elif index[0] == '+':
                            in_plus = True

                            if first_round:
                                first_index = round_num

                            first_round = False
                            last_round  = round_num

                            new_word = new_word + index[2]
                            if index[2] == '\n':
                                changed_chars = changed_chars + '\\n'
                            else:
                                changed_chars = changed_chars + index[2]
                        else:
                            prev_word = prev_word + index[2]
                            new_word = new_word + index[2]

                        round_num += 1
                    # end for index in diff

                    # calculate if word was added or deleted
                    change_dist = last_round - first_index
                    if (' ' in changed_chars) and (changed_chars.count(' ') == 1) and (len(changed_chars) == change_dist+1):
                        if changed_chars.replace(' ','').isalpha():
                            if (in_plus and not in_minus) or (in_minus and not in_plus):
                                add_delete = "1"

                    changed_words[0] = prev_word.rstrip()
                    changed_words[1] = new_word.rstrip()

                    prev_llen = len(prev_text[line].split())
                    new_llen = len(curr_text[line].split())

                    if revision_total == 1 and changed_chars == ' ':
                        if ' ' in changed_words[0]:
                            changed_words[0] = ' ' 
                            changed_words[1] = ""
                        else:
                            changed_words[0] = ""
                            changed_words[1] = ' ' 
                        #end if/else
                    #end if
                    
                    new_dir = "is_diff_data_sets_"+revis_file_num+"/"
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                    
                    # create file and write all features to it
                    feature_file = open(new_dir + str(file_num) + "_features.txt",'w+')
                    feature_file.write(str(prev_llen) + '\n')
                    feature_file.write(str(new_llen) + '\n')
                    feature_file.write(changed_words[0].encode('utf8') + '\n')
                    feature_file.write(changed_words[1].encode('utf8') + '\n')
                    feature_file.write(changed_chars.encode('utf8') + '\n')
                    feature_file.write(str(change_dist) + '\n')
                    feature_file.write(str(add_delete) + '\n')
                    feature_file.close()

                #end if timesinside

                times_inside += 1
            #end if
        #end inner for
        line_num += 1
    #end if
    #end outter for 

#end get_revision

def main():
    
    # get all the files to loop over
    with open("is_"+revis_file_num+"_revis.txt") as prev_f:
    #with open("bi_"+revis_file_num+"_revis.txt") as prev_f:
    #with open('bi_revis_summary_prev.txt') as prev_f:
        files = prev_f.readlines()
    prev_f.close()
    
    # loop over files and create diff data
    count = 1
    for rv_file in files:
        # some output to see where the script is at
        if count%500 == 0:
            print 'On #' + str(count) + ', ' + str(len(files)-count) + ' to go...'
        file_num = int(rv_file.rstrip())

        get_revision(file_num)
        count += 1
    #end for
#end main

main()

