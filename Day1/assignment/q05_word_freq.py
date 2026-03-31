# Word Frequency Counter (File Handling) 

# Problem Statement: 
# Read a .txt file and count frequency of each word. 

# Input (file content): 

# hello world 
# hello python 

# Output: 
# {'hello':2,'world':1,'python':1} 

# Constraints: 

# Case insensitive 

# Ignore punctuation 

# File size ≤ 10MB 

import re


wordfreq={}

    
with open('sampletext.txt','r') as f:
    for i in f.readlines():
        words=i.split(" ")
        for word in words:
            word=word.replace("\n","")
            if word in wordfreq:
                wordfreq[word]+=1
            else:
                wordfreq[word]=1       

print(wordfreq)


