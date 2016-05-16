# -*- coding: utf-8 -*-
'''
#   pullRevisions.py
#   Connor Riddell
#   pulls the revision text out of XML and puts the text in its own file
'''
import xml.etree.ElementTree as ET
import sys 
import re
import os

#------------------------- Parse XML and set up variables -----------------------------------------

# user input file name to be parsed
xml_file    = sys.argv[1]

print "Parsing XML..."

# parse file
tree        = ET.parse(xml_file)
root        = tree.getroot()

# get first part of element tag
id_tag      = re.search(r"{.*}", root.tag).group(0)

# get wiki name for new folder
wiki_name   = re.search(r".*-[0-9]", xml_file).group(0)
wiki_name   = wiki_name[:-2]

# create new directory name for output files
new_dir    = os.getcwd() + '/' + wiki_name + '_revisions/'

# create new directory if not already made
if not os.path.exists(new_dir):
        os.makedirs(new_dir)

#------------------------ Main loop to write revisions to files ------------------------------------

count = 1

print "Writing revisions to files..."

# nested for loop to go into the structure properly
for page in root.findall(id_tag + 'page'):
        for revision in page.findall(id_tag + 'revision'):
            text = revision.find(id_tag + 'text').text
            
            # filter out revisions with no text
            if text is not None:
                f = open((new_dir + str(count) + '_revision' + '.txt'), 'w+')
                f.write(text.encode('utf8', 'replace'))
                f.close()
            
                count += 1
            # end if
        # end for
# end outter for
