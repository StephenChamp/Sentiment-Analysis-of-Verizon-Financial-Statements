
# coding: utf-8

# In[1]:


import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import string


# # Tokenize the Sentences and words

# In[2]:




def token_the_words(file):
    doc16 = []
    doc16sent = []
    nothin = 0

    with open(file) as f:
        for line in f:
            if line == "\n" or line == " \n":
                nothin +=0
            else:
                line = line.strip("\n")
                line = line.replace("\t", " ")
                doc16.append(line)


    #tokenize the sentence
    for line in doc16:
        doc16sent.append(sent_tokenize(line))


    #tokenize words
    doc16word = []
    for item in doc16:
        doc16word.append(word_tokenize(item))
    
    return doc16word, doc16sent
    


# # Count Non GAAP & other word Occurances

# In[3]:


def count_non_gaap(words, sentence): 
    
    counter = 0
    counter1 = 0
    counter2 = 0
    sentences = []
    combined = []

    for sent in words:
        for word in sent:
            if word.lower() == "non-gaap":
                counter += 1
                sentences.append(sent)

    for sent in words:
        for word in sent:
            if word.lower() == "adjusted":
                counter1 += 1
                sentences.append(sent)

    for sent in words:
        for word in sent:
            if word.lower() == "forma":
                counter2 += 1
                sentences.append(sent)


    for s in sentences:
        middle = ""
        for w in s:
            middle = middle + " " + w
        combined.append(middle)

    print("This report has {0} non-GAAP occurances".format(counter))
    print("This report has {0} adjusted occurances".format(counter1))
    print("This report has {0} forma occurances".format(counter2))

    return combined


# # Remove Punctuation

# In[5]:


def remove_punc(words): 
    doc16strip = []
    nothin = 0
    #needed to locate key for punctutation dictionary in python 3 compared to python 2
    table = str.maketrans({key: None for key in string.punctuation})



    for sent in words:
        for word in sent:
            word = word.translate(table)
            if word == "":
                nothin += 0
            else:
                doc16strip.append(word)

    doc_length = len(doc16strip)
    return doc16strip, doc_length


# # Remove stop words... "and, the, this..."

# In[4]:


def remove_stop_words(words):
    #remove stop words except no or not and never (never is not in list)
    swords = set(stopwords.words('english'))
    swords.remove("no")
    swords.remove("not")


    doc16stop = [w for w in words if not w.lower() in swords]
    
    return doc16stop


# # Top words for the report
# 

# In[6]:


def top_words(wordss):
    
    #return the top words in the document
    word_dist_16 = nltk.FreqDist(word.lower() for word in wordss)

    top_words16 = word_dist_16.most_common(15)

    count16 = 0

    for item in top_words16:
        count16 += item[1]

    print("The top words are:")
    print(top_words16)
    
    return top_words16


# # Analyze Sentiment

# In[10]:


def ananlyze_senti(doc16stop, doc_length):  
   
   negw = pd.read_table(r"C:\Users\scham\Desktop\ACC FIN HW\HW2\LM_neg_words.txt", encoding = "ISO-8859-1", header = None)
   posw = pd.read_table(r"C:\Users\scham\Desktop\ACC FIN HW\HW2\LM_pos_words.txt", encoding = "ISO-8859-1", header = None)

   negw = negw[0].str.lower()
   posw = posw[0].str.lower()

   neglist = negw.tolist()
   poslist = posw.tolist()

   neglist = set(neglist)
   poslist = set(poslist)


   score16 = {"good": 0, "bad": 0}
   word123 = {}
   word1234 = {}

   poscount16 = []
   negate16 = 0

   check = set(["no", "not"])

   for a in doc16stop:
       if a in neglist:
           score16["bad"] += 1
           word123[a] = word123.get(a, 0) + 1

   for a in doc16stop:
       if a in poslist:
           score16["good"] += 1
           word1234[a] = word1234.get(a, 0) + 1
           if poscount16[-1] in check or poscount16[-2] in check or poscount16[-3] in check:
               negate16 +=1
       poscount16.append(a)


   first = (score16["good"] - score16["bad"]) / len(doc16stop)   
   print("")
   print("Sentiment", "{0:.3f}% compound".format(first))        
   print("Sentiment", score16, "{0:.3f}% pos and {1:.3f}% neg".format(score16["good"]/doc_length, score16["bad"]/ doc_length))
   print("There are {0} negators within 3 tokens.".format(negate16))
   
   top_bad = []
   bad = len(word123)
   for items in word123:
       if word123[items] > 1:
           top_bad.append(items)
           
   good = len(word1234)
   top_good = []
   for items in word1234:
       if word1234[items] > 10:
           top_good.append(items)
   
   return score16, top_bad, bad, top_good, good


# # Loop Through Years

# In[11]:


annual_report = [r"C:\Users\scham\Desktop\ACC FIN HW\Project\2013.txt",r"C:\Users\scham\Desktop\ACC FIN HW\Project\2014.txt", r"C:\Users\scham\Desktop\ACC FIN HW\Project\2015.txt", r"C:\Users\scham\Desktop\ACC FIN HW\Project\2016.txt", r"C:\Users\scham\Desktop\ACC FIN HW\Project\2017.txt"]
ten_ks = [r"C:\Users\scham\Desktop\ACC FIN HW\Project\10K2013.txt",r"C:\Users\scham\Desktop\ACC FIN HW\Project\10K2014.txt",r"C:\Users\scham\Desktop\ACC FIN HW\Project\10K2015.txt",r"C:\Users\scham\Desktop\ACC FIN HW\Project\10K2016.txt",r"C:\Users\scham\Desktop\ACC FIN HW\Project\10K2017.txt"]

year = 2013
a = [r"C:\Users\scham\Desktop\ACC FIN HW\Project\10K2014.txt"]

for file in ten_ks:
    print("")
    print("{0}".format(year))
    print("")
    words, sentences = token_the_words(file)
    bad_sentences = count_non_gaap(words, sentences)
    word_strip, doc_length = remove_punc(words)
    word_stop = remove_stop_words(word_strip)
    #top_words = top_words(word_stop)
    print("")
    print("Length of this annual report is {0}".format(doc_length))
    year_sentiment, bad_words, bad, good_words, good = ananlyze_senti(word_stop, doc_length)
    year += 1
    print("Top Bad")
    print(bad_words)
    print(bad)
    print("Top Good")
    print(good_words)
    print(good)
  
    
    
    

