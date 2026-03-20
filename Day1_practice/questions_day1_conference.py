a=[1,2,3]
a.insert(0,99)
print(a)

a1=[3]
a2=[4,5,7]
a1.extend(a2)
print(a1)

# creating an empty set

s=set()
print(s)

# 
sample='adityasai'
dict={}

for char in sample:
    if char in dict.keys():
       dict[char]=dict[char]+1
    else:
        dict[char]=1
        
print(dict)

sample=['adityasai  ','    adityasai']
for i in range(0,len(sample)):
    sample[i]=sample[i].strip()
    
print(sample)

# how do i define global variable?

#garbage collection ( )

# why python was not used in low latency use cases

# exception handling