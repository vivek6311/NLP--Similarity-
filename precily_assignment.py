#!/usr/bin/env python
# coding: utf-8

# Submitted by:- Vivek Kumar, 9818076031

import numpy as np #  Used for scientific computing in Python
import pandas as pd # USed for DataFrames and Series 

import re  # used for describing a search pattern
from tqdm import tqdm #  means "progress" it will show the progress bar

import collections

from sklearn.cluster import KMeans # Used for Deep learning

from nltk.stem import WordNetLemmatizer  # For Lemmetization of words it converts the word into its root word.
from nltk.corpus import stopwords  # Load list of stopwords like (to, are, is etc.)
from nltk import word_tokenize # Convert paragraph in tokens

import pickle
import sys
import gensim.downloader as api 

from gensim.models import word2vec # For represent words in vectors
import gensim #gensim is Used for topic modeling and document similarity




#Load the assignment data from Vivek Sharma download folder and call it as df
df= pd.read_csv('/Users/vivek_sharma/Downloads/Precily Assessment/Text_Similarity_Dataset.csv')


# In[3]:


# Checks the Shape 
df.shape


# In[4]:


df.head()


# In[5]:


# TO Check if text data have any null values
df.isnull().sum() 


# In[6]:


# Here we will define the short cuts, Phrases used in normal english language
# and will seperate them into full word. for ex- are't into are not.

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


# In[7]:


# Combining all the above stundents 
# We have 3 colluns the 2nd column contains the text1, We replace all kinds of Special char which has been used here 
preprocessed_text1 = [] 

#  means "progress" it will show the progress bar

for sentance in tqdm(df['text1'].values):
    sent = decontracted(sentance)
    sent = sent.replace('\\r', ' ')
    sent = sent.replace('\\"', ' ')
    sent = sent.replace('\\n', ' ')
    sent = re.sub('[^A-Za-z0-9]+', ' ', sent)

    sent = ' '.join(e for e in sent.split() if e not in stopwords.words('english'))
    preprocessed_text1.append(sent.lower().strip())


# In[8]:


#  Then we Merge the preprocessed_text1 in df

df['text1'] = preprocessed_text1
df.head()


# In[11]:


#Similar Process for collumn 3 which has text2
from tqdm import tqdm  # tqdm means "progress" it will show the progress bar
preprocessed_text2 = []

for sentance in tqdm(df['text2'].values):
    sent = decontracted(sentance)
    sent = sent.replace('\\r', ' ')
    sent = sent.replace('\\"', ' ')
    sent = sent.replace('\\n', ' ')
    sent = re.sub('[^A-Za-z0-9]+', ' ', sent)
   
    sent = ' '.join(e for e in sent.split() if e not in stopwords.words('english'))
    preprocessed_text2.append(sent.lower().strip())


# In[12]:


#  Then we Merge the preprocessed_text1 in df

df['text2'] = preprocessed_text2

df.head()


# In[13]:


def word_tokenizer(text):
            #tokenizes and stems the text
            tokens = word_tokenize(text)
            lemmatizer = WordNetLemmatizer() 
            tokens = [lemmatizer.lemmatize(t) for t in tokens]
            return tokens


# In[15]:


# Load pre_trained Google News Vectors after downloading file, This contains the english vocab
#wordmodelfile = api.load('word2vec-google-news-300')
wordmodelfile="/Users/vivek_sharma/Downloads/GoogleNews-vectors-negative300.bin.gz"
wordmodel= gensim.models.KeyedVectors.load_word2vec_format(wordmodelfile, binary=True)


# In[18]:


# Here we will check if words in text1 & text2 present in our google news vectors vocabalry.

# if not it removes that word and if present it compares similarity score between text1 and text2 words


similarity = [] # List for store similarity score



for ind in df.index:
    
    
        W1 = df['text1'][ind]
        W2 = df['text2'][ind]
        
        if W1==W2:
                 similarity.append(0.0) # 0 means highly similar
                
        else:   

            W1words = word_tokenizer(W1)
            W2words = word_tokenizer(W2)
            
           
            
            vocab = wordmodel.vocab #the vocabulary considered in the word embeddings
            
            if len(W1words and W2words)==0:
                    similarity.append(1.0)

            else:
                
                for word in W1words.copy(): #remove sentence words not found in the vocab
                    if (word not in vocab):
                           
                            
                            W1words.remove(word)
                        
                    
                for word in W2words.copy(): #idem

                    if (word not in vocab):
                           
                            W2words.remove(word)
                            
                            
                similarity.append((1-wordmodel.n_similarity(W1words, W2words)))
                # as it is given 1 means highly dissimilar & 0 means highly similar




# Get Unique_ID and similarity Score for each row

final_score = pd.DataFrame({'Unique_ID':df.Unique_ID,
                     'Similarity_score':similarity})
final_score.head(3)




# Final Score save

final_score.to_csv('final_score.csv',index=False)




#End of Note Book

