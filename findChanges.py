'''
# findChanges.py
# Connor Riddell
# 
'''
import xml.etree.ElementTree as ET
import sys
import re
import os
from difflib import Differ

#------------------------- Parse XML and set up variables -----------------------------------------

# user input file name to be parsed
xml_file    = sys.argv[1]

# check to make sure it's an xml file and nothing else
if xml_file[-3:] != "xml":
    print "Incorrect file format. Must be of file-type XML."
    exit()

print "Parsing XML..."

# parse file
tree        = ET.parse(xml_file)
root        = tree.getroot()

# get first part of element tag
id_tag      = re.search(r"{.*}", root.tag).group(0)

typo_count  = 0 # count of amount of typos found between two revisions
prev_text   = "" # prevision revision to compare to current revision
first_round = True # boolean for first run through the loop

count = 0 # count for file names

# get wiki name for new folder
wiki_name   = re.search(r".*-[0-9]", xml_file).group(0)
wiki_name   = wiki_name[:-2]

# create new directory name for output files
new_dir    = os.getcwd() + '/' + wiki_name + '_findChanges_outputs/'

# create new directory if not already made
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

#------------------------ Main loop to get text and find changes ------------------------------------

# nested for loop to go into the structure properly
for page in root.findall(id_tag + 'page'):
    for revision in page.findall(id_tag + 'revision'):
        # check if this is first revision found b/c there is nothing to compare it to
        if first_round == True:
            # Get text and set prev_revision then set firstRound to false
            prev_text = revision.find(id_tag + 'text').text
            first_round = False
        else:
            # Get text from each revision   
            print "Getting new text..."
            text = revision.find(id_tag + 'text').text

            # check for NoneType so it does NOT error
            if text is not None:
                # compare text to prev_text
                print "Comparing texts..."
                diff = list(Differ().compare(prev_text,text))

                change_count = 0
                #print "Checking amount of changes..."
                
                for character in diff:
                    # how many characters were changed in the revision
                    if character[0] == "-" or character[0] == "+":
                        change_count += 1
               
                # if the change count under a certain amount and greater than 0, take notice
                if change_count < 10 and change_count > 0:
                    count += 1 # increment count for new file names
    
                    # print a significant revision was found
                    print "Found revisions with change count of " + str(change_count)
                    # open new files
                    f = open((new_dir + 'changeTEXT.' + str(count)), 'w+')
                    f2 = open ((new_dir + 'changePREVTEXT.' + str(count)), 'w+')
                    
                    # write to them with unicode text (original text)
                    output_text = text.encode('utf8', 'replace')
                    f.write(text.encode('utf8', 'replace'))
                    f.close()
    
                    output_text = prev_text.encode('utf8','replace')
                    f2.write(prev_text.encode('utf8', 'replace'))
                    f2.close()
             
                prev_text = text # set prev_text for next round
            else:
                # handle and notify that there was a NONETYPE
                print "FOUND NONETYPE"

# end of script

