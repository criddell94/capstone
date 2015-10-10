import urllib
import bz2

print "Downloading File..."
testfile = urllib.URLopener()
testfile.retrieve("https://dumps.wikimedia.org/gvwiki/20151002/gvwiki-20151002-pages-meta-history.xml.bz2", "gvwiki-20151002-pages-meta-history.xml.bz2")

filepath = "/Users/connor/projects/capstone/gvwiki-20151002-pages-meta-history.xml.bz2"
newFilePath = "/Users/connor/projects/capstone/gvwiki-20151002-pages-meta-history.xml"

print "Decompressing file..."

with open(newFilePath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
   for data in iter(lambda : file.read(100 * 1024), b''):
        new_file.write(data)





