'''
    checkforcorrection.py
    By: Connor Riddell
'''

# global dictionary to check for words
correction_dict = {"function":"FUNCTION", "test":"TEST"}

# helper function
def make_correction(correction_candid):
    if not correction_candid or len(correction_candid) == 0 :
        return None
    
    # initialize correction to be returned later
    correction = ""
    
    # loop over keys in dictionary and break when correction is found
    for key in correction_dict:
        if correction_candid == key:
            correction = correction_dict.get(key)
            break

    return correction

# main function to look look for correction
def check_for_correction(dummy_arg): 
    """Checks highlighted word for any correction that may need to take place"""

    # Get current document and attributes for doc
    doc = XSCRIPTCONTEXT.getDocument()
    selection_supplier = doc.getCurrentController()
    indexAccess = selection_supplier.getSelection()
    count = indexAccess.getCount() # don't really need this right now. Only loop once..

    # get cursor to write corrected word highlighted in blue
    text = doc.Text
    vis_cursor = doc.getCurrentController().getViewCursor()
    nvis_cursor= vis_cursor.getText().createTextCursorByRange(vis_cursor)
        
    # Don't really need this right now, maybe later. (loop that is)
    for i in range(count):
        # set str and txt for use
        highlighted_txt = indexAccess.getByIndex(i)
        highlighted_str = highlighted_txt.getString()
        
        # check if nothing is highlighted & return nothing if nothing is 
        if len(highlighted_str) == 0:
            return None

        # call make_correction helper function to correct highlighted word
        else:
            correction = make_correction(highlighted_str)
            
            # make sure new correction word is present
            if correction:
                highlighted_txt.setString("") # replace old word with nothing
                selection_supplier.select(highlighted_txt)
                nvis_cursor.setPropertyValue("CharBackColor", 13421823) # set background to blue
                text.insertString(nvis_cursor, correction, 0) # write correction

g_exportedScripts = check_for_correction,
