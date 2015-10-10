import xml.etree.ElementTree as ET
import sys
import re

# user input file name to be parsed
xml_file = sys.argv[1]

# check to make sure it's an xml file and nothing else
if xml_file[-3:] != "xml":
    print "Incorrect file format. Must be of file-type XML."
    exit()

print "Parsing XML..."

# parse file
tree = ET.parse(xml_file)
root = tree.getroot()

# get first part of element tag
id_tag = re.search(r"{.*}", root.tag).group(0)

print "Printing comments..."

ncrCounter = 0 # non-comment revision counter
typo_count = 0 # count of amount of typos found

# nested for loop to go into the structure properly
for page in root.findall(id_tag + 'page'):
    for revision in page.findall(id_tag +'revision'):
        # try block to catch the time when there are revisions with no
        # comment section
        try:
            comment = revision.find(id_tag + 'comment').text
            if comment.lower() == "typo" or comment.lower() == "spelling":
                typo_count += 1
                print "\n##################################################################################################################################"
                print "#####################################                      NEW REVISION                      #####################################"
                print "##################################################################################################################################\n"

                print revision.find(id_tag + 'text').text

        except AttributeError:
           ncrCounter += 1 
           

print "\n###############################"
print "## Amount of typos found: " + str(typo_count) + " ##"
print "###############################\n"
