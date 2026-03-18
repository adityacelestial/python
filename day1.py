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

# How do you remove duplicates from a list? 

nums.append(3)
s=set(nums)
nums=list(s)
print(nums)
# How do you find the largest number in a list? 

largest=max(nums)
print(max(nums))

# How do you reverse a list? 
nums.reverse()


# How do you create a dictionary? 

aditya={}

# How do you add new key value pairs? 
aditya['name']='Aditya Sai'
print(aditya)

# How do you access dictionary values? 

print(aditya['name'])

aditya['age']=20

print(aditya)

# How do you iterate through a dictionary? 

for (key,value) in aditya.items():
    print(key)


# How do you merge dictionaries? 

aditya1={
    'uni':'VIT university'
}

print(aditya1)

aditya.update(aditya1)
print(aditya)

# How do you create a set? 

s1=set()

# How do you add elements to a set? 

for i in range(10):
    s1.add(i)
s1.add(1)
print(s1)

# How do you remove elements from a set? 

s1.remove(2)
print(s1)

# How do you perform union, intersection, and difference? 

s2=set()
for i in range(4,15):
    s2.add(i)

print(s2)

print(s1.union(s2))
print(s1.intersection(s2))
print(s1.difference(s2))



# How do you check multiple conditions? 

age=18
if age>=18:
    print('major')
elif age>=15 and age<18:
    print('race to major')
else:
    print("minor")
# How do you combine conditions using logical operators? 

# How do you implement nested conditions? 


user_exists = True
password_correct = True
account_active = False

if(user_exists):
    if(account_active):
        if(password_correct):
            print('login success')
        else:
            print('unsuccessful')
    else:
        print("Account deactivated")
else:
    print("user does not exist")




# How do you iterate over a list? 

for i in nums:
    print(i)

# How do you iterate over dictionary keys and values? 

for (key,value) in aditya.items():
    print(key,value)

# How do you break a loop? 

n=[i for i in range(11)]
for i in n:
    if i==7:
        break
    print(i)

# What does continue do? 
# Ans:

    # continue will skip that iteration when given condition was met

print("\n\n Functions")
# How do you define a function? 

def square_of_num(n):
    return n**2

print(square_of_num(2))
print(square_of_num(3))
# What are positional arguments? 

def positional(first_name,last_name,company='celestial'):
    print(f"HEllo {first_name}.{last_name} from {company}")
positional('Aditya','v','celes')
# What are keyword arguments? 

positional(last_name='v',first_name='ADitya',company='cel')

# What are default parameters? 

positional('aditya','v')

# What are variable length arguments? 
# /it will take variable length arguments 
# that will take all variables as input and do operatoins

def variablesum(*args):
    #here args is a tuple
    return sum(args)

print(variablesum(1,2,3,4))

print(variablesum(1,2,3,3,4,5,6))

# How do you create a lambda function? 
add=lambda a,b:a+b
print(add(5,9))

# How do you use lambda with map? 

# How do you use lambda with filter? 

# How do you uselambda with sorted?  


add=lambda a,b:a+b
print(add(5,4))


# map function on the lambda function
# map(function,iterable)
# map is something that will pump the values into the lanmbda function
l=[1,2,3,4]
outputs= map(lambda x:x*2,l)
print(list(outputs))

# outputs is a map object

# map option in filter

# filter the outputs according to the expression
l=[1,2,3,4,5]
outputs=filter(lambda a:a%2==0,l)
print(list(outputs))

nums=[-5,2,-1,7]
sorted_nums=sorted(nums,key=lambda a:abs(a))

sorted_nums=sorted(nums,key=lambda x:abs(x))
print(sorted_nums)

sample_strings=['Adithya','sai','vidivada']
sorted_str=sorted(sample_strings,key=lambda a:len(a))

print(list(sorted_str))

# we can order a dictionary witht the lambda function


students = [
    {"name": "Adithya", "age": 23},
    {"name": "Sai", "age": 21},
    {"name": "Bob", "age": 25}
]

sorted_dict=sorted(students,key=lambda a:a['age'])
print(list(sorted_dict))