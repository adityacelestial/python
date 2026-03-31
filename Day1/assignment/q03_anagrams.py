"""
    Group Anagrams 

Problem Statement: 
Group strings that are anagrams of each other. 

Input: 
words = ["eat","tea","tan","ate","nat","bat"] 

Output: 
[["eat","tea","ate"],["tan","nat"],["bat"]] 

Constraints: 

1 ≤ len(words) ≤ 10^4 

Each word length ≤ 100 

Time Complexity: O(n * k log k) 
"""
from collections import defaultdict

def groupAnagrams(words):
    groups = defaultdict(list)

    for word in words:
        key = ''.join(sorted(word)) 
        groups[key].append(word)

    return list(groups.values())


words = ["eat","tea","tan","ate","nat","bat"]
print(groupAnagrams(words))



    
    
    