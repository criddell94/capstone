# -*- coding: utf-8 -*-
'''
#
# id_diff.py
# Connor Riddell
# Calculate error type with Naive Bayes Classifier
#
'''
import nltk
import os
import random

# open language word list
#gv_words   = []
#bi_words   = []
is_words   = []

#with open("gv_word_list.txt") as word_f:
#with open("bi_word_list.txt") as word_f:
with open("is_word_list.txt") as word_f:
    words = word_f.readlines()
word_f.close()

for word in words:
    #gv_words.append(word.lower().rstrip())
    #bi_words.append(word.lower().rstrip())
    is_words.append(word.lower().rstrip())
#end for

#
# calculate error features
#
def error_features(input_list):
    # set original variables
    prev_llen       = int(input_list[0].rstrip())
    new_llen        = int(input_list[1].rstrip())
    prev_word       = input_list[2].rstrip().lower()
    
    if 'Ç' in prev_word:
        prev_word = prev_word.replace('Ç','ç')
   
    new_word        = input_list[3].rstrip().lower()
  
    if 'Ç' in new_word:
        new_word = new_word.replace('Ç','ç')
 
    changed_chars   = input_list[4].rstrip()
    change_dist     = int(input_list[5].rstrip())

    features = {}
    
    features["Change Distance"] = change_dist
    
    # set grammar-change
    if len(changed_chars) == 1:
        if changed_chars[0] == "," or (changed_chars[0] == "'" and new_word not in is_words):
            features["grammar-change"] = True
        else:
            features["grammar-change"] = False
    else:
        features["grammar-change"] = False
    
    # set is spelling error
    for char in changed_chars:
        if char.isalpha() or char == "\xe7" or char == "'" or char == '-':
            features["is-sp-error chars"] = True
        else:
            features["is-sp-error chars"] = False 
            break

    # set add/delete
    if prev_llen != new_llen:
        features["Add/Delete Word"] = True
    else:
        features["Add/Delete Word"] = False
    
    # set formatting
    for char in changed_chars:
        if not char.isalpha() or char != '-' or char != '\xe7':
            features["Formatting"] = True
        else:
            features["Formatting"] = False 
    
    if changed_chars == '\\n':
        features["Formatting"] = True

    # set non-word to word
    if prev_word not in is_words and new_word in is_words:
        features["non-word => word"] = True
    else:
        features["non-word => word"] = False

    # set word to word
    if prev_word in is_words and new_word in is_words:
        features["word => word"] = True
    else:
        features["word => word"] = False
   
    return features
#end error_features

print "Loading in training data..."

# open all the test set files and load them into labeled errors by type
labeled_errors = []
for form_file in os.listdir("classifiers/formatting"):
    if form_file == '.DS_Store':
        continue
    else:
        with open("classifiers/formatting/" + form_file) as f:
            lines = f.readlines()
        f.close()

        labeled_errors.append((lines,'formatting'))

for sp_file in os.listdir("classifiers/spelling"):
    if sp_file == '.DS_Store':
        continue
    else:
        with open("classifiers/spelling/" + sp_file) as f:
            lines = f.readlines()
        f.close()
        
        labeled_errors.append((lines,'spelling'))

for gram_file in os.listdir("classifiers/grammar"):
    if gram_file == '.DS_Store':
        continue
    else:
        with open("classifiers/grammar/" + gram_file) as f:
            lines = f.readlines()
        f.close()

        labeled_errors.append((lines,'grammar'))

for add_file in os.listdir("classifiers/add_delete"):
    if add_file == '.DS_Store':
        continue
    else:
        with open("classifiers/add_delete/" + add_file) as f:
            lines = f.readlines()
        f.close()

        labeled_errors.append((lines,'add/delete'))

# shuffle up labeled errors for testing
random.shuffle(labeled_errors)

# load in all unlabeled data from folders
print "Loading in uncategorized data..."
unlabeled_errors = []
for new_file in os.listdir("is_diff_data_sets_1"):
    if new_file == '.DS_Store':
        continue
    else:
        with open("is_diff_data_sets_1/" + new_file) as f:
            lines = f.readlines()
        f.close()
        
        unlabeled_errors.append(lines)

for new_file in os.listdir("is_diff_data_sets_2"):
    if new_file == '.DS_Store':
        continue
    else:
        with open("is_diff_data_sets_2/" + new_file) as f:
            lines = f.readlines()
        f.close()
        
        unlabeled_errors.append(lines)

for new_file in os.listdir("is_diff_data_sets_3"):
    if new_file == '.DS_Store':
        continue
    else:
        with open("is_diff_data_sets_3/" + new_file) as f:
            lines = f.readlines()
        f.close()
        
        unlabeled_errors.append(lines)

for new_file in os.listdir("is_diff_data_sets_4"):
    if new_file == '.DS_Store':
        continue
    else:
        with open("is_diff_data_sets_4/" + new_file) as f:
            lines = f.readlines()
        f.close()
        
        unlabeled_errors.append(lines)

for new_file in os.listdir("is_diff_data_sets_5"):
    if new_file == '.DS_Store':
        continue
    else:
        with open("is_diff_data_sets_5/" + new_file) as f:
            lines = f.readlines()
        f.close()
        
        unlabeled_errors.append(lines)

for new_file in os.listdir("is_diff_data_sets_6"):
    if new_file == '.DS_Store':
        continue
    else:
        with open("is_diff_data_sets_6/" + new_file) as f:
            lines = f.readlines()
        f.close()
        
        unlabeled_errors.append(lines)

# create featuresets
print "Training..."
featuresets = []
for (feature_list, error_type) in labeled_errors:
    featuresets.append((error_features(feature_list), error_type))

halfway = len(featuresets)/2
#train_set, test_set = featuresets[:halfway], featuresets[halfway:]
classifier = nltk.NaiveBayesClassifier.train(featuresets)

# classify data for all unlabeled errors
counter = 1
num_symbol = ''
print "Calculating categories..."
class_f = open("classified_errors.txt", "w+")
for error in unlabeled_errors:
    error_class =  classifier.classify(error_features(error))
    #print error_class + "  Prev Word: " + error[2].rstrip() + "  New Word: " + error[3].rstrip()

    prev_word = error[2].lower().rstrip()
    if 'Ç' in prev_word:
        prev_word = prev_word.replace('Ç','ç')
    
    new_word = error[3].lower().rstrip()
    if 'Ç' in new_word:
        new_word = new_word.replace('Ç','ç')

    class_f.write(error_class + "  Prev Word: " + prev_word + "  New Word: " + new_word + '\n')

    num_symbol = num_symbol + '*'
    if len(num_symbol) == 125:
        print str(125*counter) + ":  " + num_symbol
        num_symbol = ''
        counter += 1

class_f.close()


#print(nltk.classify.accuracy(classifier, test_set))
