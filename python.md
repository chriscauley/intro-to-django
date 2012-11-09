A Quick Guide to Python
========

REPL vs files
--------

Typing `python` and hitting enter will open a python prompt. Here you can enter python and the output of every line is automatically printed after the line. For this reason, the python prompt is known as a read-eval-print loop (REPL). Here `$` denotes a bash prompt while `>>>` denotes a python prompt.

```python
$ python
>>> 'arst'
'arst'
>>> print 'arst'
arst
>>> x = 'arst'
>>> print x.upper()
ARST
```

If you put a file name after python, it will execute the file as a python file. This is no different than typing the file into python line by line, except that nothing is printed unless you explictly type `print` before a line. Here `cat` is a bash program that simply prints a files contents to a command line. All files are in the same folder as this file.

```python
$ cat example1.py
x = "Hello nurse!"
x.upper() #this line is not printed.
print x
y = 100

$ python example1.py
Hello nurse!
```

You can load code from external python files (or "modules") by typing `import` followed by the module name. When you do this the code is executed and the code in the module is accessible via a variable with the name of the module. This can be used with `from`, commas, and as to tailor how code is imported from modules.

```python

>>> import example1
Hello nurse!
>>> print example1.x
Hello nurse!
>>> from example1 import x as hello_nurse, y
>>> print hello_nurse.upper()
HELLO NURSE!
>>> print y*50
500
```

A complete explanation of the syntax would be written like `[from <module> ]import <variable_1>[as <variable_1_name][, <variable_2> [as <variable_2_name>]]`. Here [brackets] denote optional parameters. If you open any python file you'll see many tens of examples of this syntax.

Folders as modules
--------

Any folder that has an `__init__.py` file in it will bet treated as a module. A large group of these modules is often times refered to as a library. The import syntax makes no distinction for files vs folders. For example `from django.contrib.auth.models import User` refers to the class `User` found in the file found at `django/contrib/auth/models.py`. Here are a few ways to access user:

```python
>>> from django.contrib.auth.models import User
>>> import django
>>> django.contrib.auth.models == User
True
>>> from django.contrib.auth import models as auth_models
>>> auth_models.User == User
True
```

This is useful because you can import a library and use all of it's functions/classes or just import a single object. At this point you're probably wondering what the hell an `object` is.

What the hell is an object
--------

The short answer is everything. In python everything inherits from the class object. This means that every variable you use can be `dir`ed to find out what you can do to it. dir returns all the attributes and methods of an object.

```python
>>> x = "hello nurse"
>>> print dir(x)
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser', 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
>>> x.islower()
True
>>> x.upper()
'HELLO NURSE'
>>> x.upper().islower()
False
>>> x.isdigit()
False
>>> x.startswith('hello')
True
```

Here `x` is a string. Attributes are accessed with `variable.attribute`. Attributes which are variables are called properties. Variables that are functions are called methods.

Data types
--------

* Integers

Python has many built in data types and many more importable data types. When you create a `class` as we'll do in django, you're essentially creating a new data type. The first data type we'll look at is the integer

```python
>>> x = 1
>>> y = 2
>>> x + y
3
>>> x - y
-1
>>> x * (y + 15)
17
>>> x / y # truncating division
0
>>> x % y # modular (remainder) division
1
```

Integers work as you'd expect for all mathematical functions except division (in the last two examples above this result is because 1 / 2 gives 0 with a remainder of 1)

* Strings

Strings are just blocks of characters surrounded by quotes. Strings, also have a variety of mathematical functions.

```python
>>> x = 'blarg'
>>> y = 'foo'
>>> x + y
'blargfoo'
>>> x * 5
'blargblargblargblargblarg'
>>> "My name is " + x + " and I like to" y #Note the lack of a space
'My name is blarg and I like tofoo'
>>> x + 5 #generates a type error
>>> "%s is a nonsense word."%x
'blarg is a nonsense word."
>>> "%s and %s are often times used as dummy variables in programming examples"%(x,y)
'blarg and foo are often times used as dummy variables in programming examples'
```

The last two inputs are examples of string formatting, which is one of the coolest features of python. String formatting creates much more readable code than adding strings.

* Type

Now that we have two kinds of data we can understand how types work. For every built in data type there is a type object. This can be used to convert data types between each other. There's even a type for types! A type can be used as a function to convert a piece of data from one type to another.

```python
>>> x = 1
>>> y = '1'
>>> x
1
>>> y
'1'
>>> x == y
False
>>> x == int(y)
True
>>> str(x) == y
True
>>> str
<type 'str'>
>>> type('arstarst')
<type 'str'>
>>> type(1) == int
True
>>> x + y # Throws a TypeError
>>> int('arst') # Throws a ValueError
>>> 'arst'.isdigit()
False
>>> '1'.isdigit()
True
```

As you can see, in python you have to be careful when mixing different types of variables. This is because python is a "strongly type" language (look up strong typing on wikipedia for more info). If you want to use two variables of different types you must convert between the two in many cases.

* Floats


Floats are just like ints, but they have decimal values instead of whole numbers. Any time an int interacts with a float it is first converted to a float.

```python
x = 1
y = 2
float_y = 2.0
x + y # returns 3
x + float_y # returns 3.0000
x / y # returns 0 since 1/2 is float_yero with a remainder of 1
x / float_y # returns 0.5 since float_y is a float
y == float_y # returns True since y is converted to a float
```

* Booleans

There are only two boolean values, True and False. Any python object is automatically converted to a boolean when placed in a conditional statement (if, elif, and, or, or while). Python has the standard set of boolean operators (==,!=, >, >=, <, <=) which all return a boolean.

```python
>>> x = 1
>>> bool(x)
True
>>> if x:
...     print "this will get printed"
... else:
...     print "this won't get printed"
>>> 1 > 2
False
>>> 1 <= 2
True
>>> 1 == x
True
>>> 1 != x
False
```

Calling `bool` on a variable is basically like asking "is this of any value?". The following objects return False, while any other value of that type is True. We'll learn about lists, tuples, and dicts in a moment. For now just know they are false if they are empty.

|int|0|
|str|''|
|list|[]|
|tuple|()|
|dict|{}|

Python also has `and` and `or`, which convert the variables they join to booleans and then return a boolean. `and` asks if both are `True`. `or` asks if either or both ar `True`. The final boolean keyword is `not`, which converts a boolean to it's opposite.

```python
>>> True or False
True
>>> False or False
False
>>> True and False
False
>>> True and True
True
>>> False or 0 or '' or {} or () or [] # all convert to False
False
>>> True and 1 and 3204 and -234 and {'name': bob} and [1] and [0] and 'this' and '0'
True
```

* Lists

Lists are a series of objects in an ordered array. 

```python
>>> [1,2,3]
[1,2,3]
>>> list('blarg foo')
['b','l','a','r''g',' ','f','o','o']
>>> 'blarg foo'.split(' ')
['blarg','foo']
>>> list(1) # returns type error
```

Lists are the primary "iterable" type in python. A list can be iterated over with a forloop. In python this uses the following syntax:

```python
$ cat example2.py
for i in [1,2,3,4]:
    print i
$ python example2.py
1
2
3
4
```

The `range` function produces a list from 0 to n-1 for any input n (so the length of the list is n). With two inputs, `range(n,m)` will go from n to m-1.

```python
>>> x = 5
>>> y = 2
>>> counter = 0
>>> for i in range(x):
...     counter = counter + i
...
>>> print counter # sum of 0, 1, 2, 3, 4
10
>>> for i in range(y,x):
...     counter = counter + i
...
>>> print counter # sum of 2, 3, 4 and the counter value from above
19
```

Lists can be a mix of any type of object. Individual list items can be accessed with brakets[]. This is called indexing. `len` is a function that returns the length of an object

```python
>>> total = 0
>>> blarg = [0,1,10,'100','foo']
>>> blarg[1] + blarg[2]
11
>>> for i in range(len(blarg)):
...     item = blarg[i]
...     print type(item)
...     if type(item) == in:
...         total = total + item
...     if type(item) == str:
...         if item.isdigit():
...             total = total + int(item)
...
<type 'int'>
<type 'int'>
<type 'int'>
<type 'str'>
<type 'str'>
>>> print total
111
>>> blarg[3] = 'monkey'
>>> blarg[3].upper()
'MONKEY'
```

* Dictionaries

Dictionaries (called associative arrays or hash table in other languages) are lists with objects as indexes instead of integers. Dictionaries are unordered. Their syntax is `{key1: value, key2:value2...}`. `some_dict.values()` returns a list of values. `some_dict.keys()` returns a list of keys. `some_dict.items()` returns a list of tuples (another kind of list) like `[(key1,value1), (key2,value2)]`. These are all unordered. 

```python
scores = {'james': 80, 'bill': 90}
scores['james'] # returns 80
scores['jane'] # raises a KeyError
scores['jane'] = 100
high = 0
for item in scores.items():
    if high < item[1]:
        high = item[1]
        leader = item[0]
print "%s has a the class high (%s)"%(leader,high)
# output is "jane has the class high (100)"
```

* Tuples 

A tuple is a special type of list. It is "immutable" which means it can't be changes. All you really need to know is that a tuple is a list with parentheses around it.

Tuples can be "unpacked", which means the values of a tuple can be assigned to multiple variables. This makes for much friendlier code. (Also notice the improved dict syntax here)

```python
a,b,c = (1,2,3)
print a # outputs 1
my_tuple = (3,2,1)
a,b,c = my_tuple #values are now reversed
print a #outputs 3
scores = {
    'jonathan': 80,
    'tony': 100,
    'angela': 95,
    'samantha': 90,
    'mona': 99
    }
high = 0
for name, score in scores.items(): #Tuples are unpacked into two variables!!
    if score > high:
        high = score
        leader = name
print "%s is the boss!"%leader
```

Tuples are important because they can't change order, while lists can. This implies the order of a tuple is relevant! This is usefull for unpacking tuples as seen above. Another example would be if you stored dates as (year,month,date), you wouldn't want the tuples to be sorted.

Functions
--------

We've already seen many types of functions in the form of methods and types and the range funciton. Functions take in arguments in the form `func(arg1,arg2,arg3...)`. If a function has an argument it is required!

A function is defined with `def` and usually `return`s a value. If no value is returned, `None` will be returned (`None` is `False` for all intents and purposes).

```python
>>> def top_three(some_list):
...     some_list.sort() # The list is now sorted, low to high
...     length = len(some_list)
...     return some_list[length-3:length] #the last 3 values in the sorted list
... 
>>> top_three()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  TypeError: top_three expected at least 1 arguments, got 0
>>> import random
>>> numbers = []
>>> for x in range(100):
...     numbers.append(random.randint(1,100))
...
>>> # at this point numbers is 100 numbers between 1 and 100, there may be repeats
>>> first, second, third = top_three(numbers)
>>> first
99
>>> second
98
>>> third
98
```

Typically you'd put top_three in some file (eg. math_toolf.py) to be imported elsewhere.

You can also specify optional arguments with key word arguments. Key word arguments MUST come after arguments. They can be in any order. The syntax is `def function(arg1,arg2,arg3...,kwarg1=value1,kwarg2=value2...):` A great example of this is the `datetime.datetime` funciton, which returns a datetime object. Somewhere in pythons built in code is the line:

```python datetime.py
def datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
```

This means you MUST have a year, month and day to make a datetime. If you only provide these, all other values will be zero except for the time zone (which will be empty). This means `datetime.datetime(2012,1,1)` is January 1, 2012 at midnight. All of these would produce the same thing:

```python
from datetime import datetime as dt #done for brevity
dt(2012,1,1)
dt(2012,1,1,0,0,0,0)
dt(2012,1,1,hour=0)
dt(2012,1,1,minute=0)
dt(2012,1,1,microsecond=0,hour=0)
```

All of these would cause errors

```python
dt(2012) # not enough arguments
dt(2012,1,minute=0,1) #kwarg should NOT be before an arg
dt(2012,1,1,'monkey') # it's looking for a number for hour
dt(2012,1,1,monkey=5) # no such keyword argument
dt(2012,1,1,hour=5,hour=5) #repeat kwarg
dt(2012,1,1,5,hour=5) # same as above because the fourth arg is the kwarg hour!
dt(2012,1,1,0,0,0,0,None,0) # too may args, there's nothing after the final kwarg, tzinfo
```

One of the strongest features of python is once again unpacking (gasp!). You can create a function with a variable number of `args` and `kwargs` using `*args` and `**kwargs`. So the following funciton has an infinite number of `args` or `kwargs` as needed. 

```python
>>> def wackey_function(*args,**kwargs):
...     print "args is a %s which is %s items long"%(type(args),len(args))
...     print "kwargs is a %s with %s for keys"%(type(kwargs),kwargs.keys())
...
>>> wakey_function()
args is a <type 'list'> which is 0 items long
kwargs is a <type 'dict'> with [] for keys 
>>> wackey_function(1,2,3,4,name="bill",favorite_band="Journey",music
args is a <type 'list'> which is 4 items long
kwargs is a <type 'dict'> with ['name','favorite_band'] for keys
>>> x = [1,2,3,4,5]
>>> y = {'blood': 0,'sex': 0, 'sugar': 0, 'magic': 0}
>>> wackey_function(*x,**y)
args is a <type 'list'> which is 5 items long
kwargs is a <type 'dict'> with ['blood','magic','sugar','sex'] for keys
```

