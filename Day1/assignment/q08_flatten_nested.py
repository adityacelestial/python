"""
        Flatten Nested List (Recursive) 

Problem Statement: 
Flatten a nested list of arbitrary depth. 

Input: 
[1,[2,[3,4],5],6] 

Output: 
[1,2,3,4,5,6] 

Constraints: 

Depth ≤ 1000 

Use recursion 
        
        """

global unpackedlist
unpackedlist=[]
def listunpacking(packedlist):
    # we use the isinstance to compare the types
    for item in packedlist:
        if isinstance(item,list):
            listunpacking(item)
        else:
            unpackedlist.append(item)

packed=[1,[2,[3,4],5],6] 

listunpacking(packed)
print(unpackedlist)

