# memory management

a=1
del a

# How do you assign multiple variables in a single line? 

a,b,c=1,2,3

print(f'a={a}\nb={b}\nc={c}')

p=q=r=0

print(f'p={p}\nq={q}\nr={r}')

# How do you swap two variables without using a third variable? 

# Ans:
first=10
second=20
print("\n\n\n")
print(f"original first={first} second={second}")
first,second=second,first
print(f"after swapping first={first} second={second}")

# How do you check the type of a variable? 
print("\n\ncheck datatypes:")
sample=1
print(type(sample))
sample='a'
print(type(sample))
sample=45.99
print(type(sample))
sample=[1,2,'a']
print(type(sample))
sample={'a':1,'b':2}
print(type(sample))


# mutable and immutable datatypes

# mutable datatypes were the datatypes which we can change the value e.g list,dict,set etc.

# immutable datatypes where we cannot change the values 
# although it seems we can change but it was a new value and previous name was pointed to new ocntainer

print(f"\n\n immutable proof")
a=10
print(f"a={a} and id = {id(a)}")
a=a+10
print(f"a={a} and id = {id(a)}")

# common string operations

samplest='Adithya Sai'
print(f"common string operations:")

print(f"lower:{samplest.lower()}")
print(f"upper:{samplest.upper()}")
samp="   aditya   "
print(f"strip :{samp.strip()}")

#searching 

sample="Adithya Sai"

print("finding:\n\n")
print(sample.find('a'))
print(sample.find('A'))
print(sample.find('S'))
print(sample.find('z'))# returns -1 if letter is not there

print("checking:\n\n")

print(sample.startswith("a"))
print(sample.startswith('A'))

print(sample.endswith('i'))
print(sample.endswith('z'))

#replace and replace and split

print(sample.replace('a','A'))

print(sample.split(" "))

sample=sample.replace('a','A')
print(sample)

# How do you check the type of a variable? 

# How do you convert between data types? 

# How do you concatenate strings? 

# How do you format strings? 

print(type(sample))

a='100.0'
print(type(a))
a=float(a)
print(type(a))

print("\n\nconcatination of strings \n")
print('Aditya'+" "+'sai')

# format strings in pythin

# /we can use the fstrings
# we can use the format

print(f"THe sample string is {sample}")
print("The variables used is {} and {}".format(a,sample))

print("The PI value {:.2f}".format(3.1423))

print("The value {0}  {1}".format(a,sample))
print("The value {a} and {b}".format(a=a,b=sample))


# list operations

nums = [1, 2, 3]



nums.append(4)
print(nums)

nums.remove(2)
print(nums)

# we can append at the end 
# we can specify the index st which it can insert

nums.insert(1,[1,2,3])
print(nums)

nums.extend([2,3])

nums.remove([1,2,3])
print(nums)

nums.remove(3)
print(nums)
# this will remove the first three

print(nums.count(3))
nums.sort()
print(nums)

nums.reverse()
print(nums)


# How do you create a list? 

# How do you access list elements? 

print(nums[0])

# How do you update elements? 

nums[0]=99
print(nums)

# How do you remove elements? 

nums.remove(99)
print(nums)



# How do you iterate through a list? 

for i in nums:
    print(i,end=" ")

# How do you sort a list? 

nums.sort()
print(nums)
nums.reverse()
print(nums)