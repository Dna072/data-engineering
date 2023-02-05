#!/usr/bin/env python
"""mapper.py"""

import sys
import re
import json

def find_words(text):
    words = re.findall(r'\b(han|hon|det|den|denna|denne|hen)\b', text, re.IGNORECASE)
    return words

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    if len(line) == 0:
        continue
        
    data = {}
    
    try:
        data = json.loads(line)
    except ValueError as e:
        continue
    
    if data.get('retweeted_status'):
        continue
        
    # split the line into words
    text = data['text'].strip().lower()
    words = find_words(text)
    word_dict = {}
    
    # increase counters
    for word in words:
        if word_dict.get(word):
            word_dict[word] += 1
        else:
            word_dict[word] = 1
        
    for k, v in word_dict.items():
        print('%s\t%s'%(k, v))
        
    if len(words) > 0:
        print("-\t1")