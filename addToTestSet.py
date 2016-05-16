# -*- coding: utf-8 -*-
#
# addToTestSet.py
# Connor Riddell
# Add revisions to test set to then be looked over later
#
import os
import sys

# open folder with revisions
folder_num = sys.argv[1]

# open language file and get words
#bi_words = []
#gv_words = []
is_words = []
#with open("gv_word_list_lower.txt") as word_f:
#with open("bi_word_list_lower.txt") as word_f:
with open("is_word_list_lower.txt") as word_f:
    words = word_f.readlines()
word_f.close()

for word in words:
    #gv_words.append(word.rstrip())
    #bi_words.append(word.rstrip())
    is_words.append(word.rstrip())

#data_files = os.listdir("gv_diff_data_sets_" + folder_num)
#data_files = os.listdir("bi_diff_data_sets_" + folder_num)
data_files = os.listdir("is_diff_data_sets_" + folder_num)
format_chars = '~`@#$%^&*()_+={}[]\|":;/><'

gram_count  = 0
spell_count = 0
ad_count = 0
form_count = 0
num_indictor = ''
print_num = 0
counter = 0

# loop over files and sort 
run = True
while run:
    if counter == len(data_files)-1:
        break
    
    if data_files[counter] != '.DS_Store':
        # open file
        #with open("gv_diff_data_sets_"+folder_num+"/" + data_files[counter]) as f:
        #with open("bi_diff_data_sets_"+folder_num+"/" + data_files[counter]) as f:
        with open("is_diff_data_sets_"+folder_num+"/" + data_files[counter]) as f:
            lines = f.readlines()
        f.close()
        
        # set previous word, new word, changed chars, and add_delete
        prev_word   = lines[2].lower().rstrip()
        if 'Ç' in prev_word:
            prev_word = prev_word.replace('Ç','ç')

        new_word    = lines[3].lower().rstrip()
        if 'Ç' in new_word:
            new_word = new_word.replace('Ç','ç')
        
        changed_chars = lines[4].rstrip()
        add_delete = int(lines[6].rstrip())
        
        moved = False
       
        # add to add_delete by moving file
        if ad_count != 11130:
            if not moved:
                if add_delete == 1:
                    #os.system("mv gv_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/add_delete/")
                    #os.system("mv bi_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/add_delete/")
                    os.system("mv is_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/add_delete/")
                    moved = True
                    print "Moved " + data_files[counter] + " to add_delete..."
                    ad_count += 1
                 #end if
             #end if
         #end if
        
        # add to grammar by moving file
        if gram_count != 11150:
            if not moved:
                if (prev_word in is_words) and (new_word in is_words):
                    #os.system("mv gv_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/grammar/")
                    #os.system("mv bi_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/grammar/")
                    os.system("mv is_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/grammar/")
                    moved = True
                    print "Moved " + data_files[counter] + " to grammar..."
                    gram_count += 1
                #end if
            #end if
        #end if
        
        # add to spelling by moving file
        if spell_count != 11150:
            if not moved:
                if (prev_word not in is_words) and (new_word in is_words):
                    #os.system("mv gv_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/spelling/")
                    #os.system("mv bi_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/spelling/")
                    os.system("mv is_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/spelling/")
                    moved = True
                    print "Moved " + data_files[counter] + " to spelling..."
                    spell_count += 1
                #end if
            #end if
        #end if
        
        # add to formatting by moving file
        if form_count != 11150:
            if not moved:
                if (len(changed_chars) == 1) and changed_chars == '\\n':
                    #os.system("mv gv_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/formatting/")
                    #os.system("mv bi_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/formatting/")
                    os.system("mv is_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/formatting/")
                    moved = True
                    print "Moved " + data_files[counter] + " to formatting..."
                    form_count += 1
                
                elif not changed_chars.isalpha():
                    all_chars_form = True
                    for char in changed_chars:
                        if char not in format_chars:
                            all_chars_form = False
                    #end for

                    if all_chars_form:
                        #os.system("mv gv_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/formatting/")
                        #os.system("mv bi_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/formatting/")
                        os.system("mv is_diff_data_sets_"+folder_num+"/" + data_files[counter] + " classifiers/formatting/")
                        moved = True
                        print "Moved " + data_files[counter] + " to formatting..."
                        form_count += 1
                #end if/else
            #end if
        #end if

    #end if

    '''    
    # stop if each of the counts have met their quota
    if (gram_count == 50):
        if (spell_count == 50):
            if (ad_count == 30):
                if (form_count == 50):
                    run = False
    '''
    counter += 1



