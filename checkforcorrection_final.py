# -*- coding: utf-8 -*-
'''
#    checkforcorrection_beta.py
#    By: Connor Riddell
#    Takes highlighted word and checks whether it has a correction for it
#    Then asks for correction confirmation before correcting word
'''

import uno, string
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK, BUTTONS_YES_NO 
from com.sun.star.awt.MessageBoxType import MESSAGEBOX

# global dictionary to check for words
correction_dict = {'bun-stooghyn':'bunstooghyn', 'feaillyn':'feaillaghyn', 'chynney':'kynney', 'ny':'y', 'e':'y','yn':'y',
                    'vaaish':'baaish', 'y':'ny', 'yn':'ny', 'countee':'coontae', 'çheeroaylleeaght':'çheer-oaylleeaght', 
                    'stetayn':'steatyn', 'seatyn':'steatyn', 'loayreydyryn':'loayreyderyn', 'man':'mann', 'biyetnam':'vietnam',
                    'bietnam':'vietnam', 'fo_heidyl':'fo-heidyl', 'fo-heidl':'fo-heidyl'}

# helper function to get correction
def make_correction(correction_candid):
    if not correction_candid or len(correction_candid) == 0 :
        return None
    
    # initialize correction to be returned later
    correction = ""
    
    # loop over keys in dictionary and break when correction is found
    for key in correction_dict:
        if unicode(correction_candid) == key.decode("utf-8"): # handles unicode comparison
            correction = correction_dict.get(key).decode("utf-8") # sets correction to the decoded unicode string
            break

    return correction

# main function to look look for correction
def check_for_correction(dummy_arg): 
    """Checks highlighted word for any correction that may need to take place"""
    #space_indexes = []
    #new_space_indexes = []
    #punct_dict = {}

    # Get current document and attributes for doc
    doc = XSCRIPTCONTEXT.getDocument()
    selection_supplier = doc.getCurrentController()
    indexAccess = selection_supplier.getSelection()
    #count = indexAccess.getCount() # don't really need this right now. Only loop once..

    # get cursor to write corrected word highlighted in blue
    text = doc.Text
    vis_cursor = doc.getCurrentController().getViewCursor() # visible cursor in OpenOffice
    nvis_cursor= vis_cursor.getText().createTextCursorByRange(vis_cursor) # not visible cursor place at same place as visible
        
    # set str and txt for use
    highlighted_txt = indexAccess.getByIndex(0)
    highlighted_str = highlighted_txt.getString()
    
    # strip punctuation from string
    punctuation = set(string.punctuation)
    '''
    for letter in highlighted_str:
        if letter == ' ':
            sp_index = highlighted_str.index(letter)
            space_indexes.append(sp_index + len(space_indexes))
            highlighted_str = highlighted_str.replace(letter,'',1)
    
    for index in space_indexes:
        highlighted_str = highlighted_str[:index] + ' ' + highlighted_str[index:]

    
    for letter in highlighted_str:
        if letter in punctuation:
            punc_index = highlighted_str.index(letter)
            punct_dict[letter] = punc_index
            highlighted_str = highlighted_str.replace(letter,'',1)
    '''
    highlighted_str = ''.join(ch for ch in highlighted_str if ch not in punctuation) 
    highlighted_str_arr = highlighted_str.split()

    corrected_sent = highlighted_str # correct sentence to be displayed at end

    # check for correction for each word highlighted
    for word in highlighted_str_arr:

        if len(highlighted_str) == 0:
            return None

        # call make_correction helper function to correct highlighted word
        else:
            correction = make_correction(word)
            
            # make sure new correction word is present
            if correction:
                # get parent window from document
                parentwin = doc.CurrentController.Frame.ContainerWindow
                # make window
                correction_query_str = word + " => " + correction # show old word => new word
                prompt = MessageBox(parentwin, correction_query_str, "Correction:", MESSAGEBOX, BUTTONS_YES_NO)
                
                # if yes button pressed, replace word
                if prompt == 2:
                    # replace wrong word with corrected word
                    corrected_sent = corrected_sent.replace(word, correction)
    '''
    for letter in corrected_sent:
        if letter == ' ':
            sp_index = corrected_sent.index(letter)
            new_space_indexes.append(sp_index + len(new_space_indexes))
            corrected_sent = corrected_sent.replace(letter,'',1)
    
    for index in new_space_indexes:
        corrected_sent = corrected_sent[:index] + ' ' + corrected_sent[index:]
    
   
    punc_location = {}
    for key in punct_dict:
        p_index = punct_dict[key]
        for s_index in space_indexes:
            if abs(p_index-s_index) == 1:
                location_index = space_indexes.index(s_index)
                if p_index-s_index > 0:
                    punc_location[key] = new_space_indexes[location_index+1]
                else:
                    punc_location[key] = new_space_indexes[location_index-1]


    for key in punc_location:
        index = punc_location[key]
        corrected_sent = key
        #corrected_sent = corrected_sent[:index] + key + corrected_sent[index:]
    ''' 
    #highlighted_txt.setString(highlighted_str)
    highlighted_txt.setString(corrected_sent) # replace old word with nothing

# helper function to create window for choosing whether correction correct
def MessageBox(ParentWin, MsgText, MsgTitle, MsgType=MESSAGEBOX, MsgButtons=BUTTONS_OK):
    com_context = uno.getComponentContext()
    serv_man = com_context.ServiceManager
    sv = serv_man.createInstanceWithContext("com.sun.star.awt.Toolkit", com_context) 
    window = sv.createMessageBox(ParentWin, MsgType, MsgButtons, MsgTitle, MsgText)
    return window.execute()
