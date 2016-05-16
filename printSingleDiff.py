# -*- coding: utf-8 -*-
'''
#
# printSingleDiff.py
# Connor Riddell
# Prints single diff between two files
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
file_number = int(sys.argv[2])
gv_words   = []

# open word list for language
with open("gv_word_list.txt") as word_f:
    words = word_f.readlines()
word_f.close()

for word in words:
    gv_words.append(word.lower().rstrip())
#end for

#------------- Functions -------------#

def is_gv(input_text):
    is_gv_lan = False
    input_slist = re.split(r'[ ,.?/ \\:{}\[\]\";!@#$%^&*()+=|~<>]+', input_text) 
    
    for index in input_slist:
        if index.lower() in gv_words:
            is_gv_lan = True
            break
        #end if
    #end for
    return is_gv_lan
#end is_gv

#
# get diff from two files
#
def get_revision(file_num):
    prev_text       = "" # prevision revision to compare to current revision
    curr_text       = ""
    revision_total  = 0

    # open previous and next files to compare diffs
    with open(rev_dir + str(file_num) + "_revision.txt") as f:
        prev_text = f.readlines()
    f.close()

    with open(rev_dir + str(file_num+1) + "_revision.txt") as f:
        curr_text = f.readlines()
    f.close()
   
    diff = ""
    line_num = 1

    changed_words = ["",""]
    changed_chars = ""
    prev_llen = 0
    new_llen = 0
    change_dist = 0

    # loop over the lines of the files and calculate diff
    for line in range(0, min(len(prev_text),len(curr_text))): 
        diff = list(ndiff(prev_text[line].decode('utf8'),curr_text[line].decode('utf8')))
        
        # print information about diff 
        times_inside = 0
        for char in range(0, len(diff)):
            if diff[char][0] == "+" or diff[char][0] == "-":
                revision_total += 1
               
                if times_inside == 0:
                       
                    print("             ******             ")
                    print("             * 01 *              ")
                    print("********************************\n")

                    print(diff)
                    print("\n")
                    print("Previous Text:  " + prev_text[line])
                    print("Revised Text:   " + curr_text[line])
                     
                    loc_help = "                "
                    for i in range(0, char):
                        loc_help = loc_help + ">"

                    loc_help = loc_help + "&\n"
                    print loc_help

                    print("Revision Location: Line " + str(line_num))
                   
                    # calculate previous word and new word indexes
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
                    
                    # calculate previous and new word, also add letters to changed chars
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

                    #end for
                    
                    # print if the words are in the language
                    print "IS GV PREV: " + str(is_gv(prev_word.encode('utf8')))
                    print "IS GV NEW:  " + str(is_gv(new_word.encode('utf8')))

                    changed_words[0] = prev_word
                    changed_words[1] = new_word

                    prev_llen = len(prev_text[line].split())
                    new_llen = len(curr_text[line].split())

                    change_dist = last_round - first_index

                    print "PREVIOUS WORD: " + repr(prev_word)
                    print "NEW WORD: " + repr(new_word)
                #end if timesinside
                
                # print more information
                print("Index is: " + str(char))
                print("Different Character: " + repr(diff[char]))
                print "CHANGE DIST: " + str(change_dist)
                times_inside += 1
            #end if
        #end inner for
        line_num += 1
    #end if
    #end outter for 
    
    if revision_total == 1 and changed_chars == ' ':
        if ' ' in changed_words[0]:
            changed_words[0] = ' '
            changed_words[1] = ""
        else:
            changed_words[0] = ""
            changed_words[1] = ' '
        #end if/else
    #end if
#end get_revision

#
# Main to call get_revision
#
def main():
    get_revision(file_number)
#end main

main()

