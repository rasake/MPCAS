# -*- coding: utf-8 -*-
from nltk.corpus import gutenberg

"""  
Answer Exercise 2.8

The regex is /ab(ab|aba)*/

"""


# NLTK chapter 2

# You can use addition, multiplication, etc, and they have the usual precedence
print(3+1*2-7/10)
# Normal division in Python3 is float division
print(2/3)
# Integer division uses the special operator //
print(2//3)
# adding lists concatenates them
print(["a1", "a2"]+["b1", "b2"])
# Python has zero indexing
my_list = ["first entry", "last entry"]
print(my_list[0])
# You can get the last entry like this
print(my_list[-1])
# Slicing
my_list = [22, 321, 5234, "a string", 9.8]
print(my_list[1:4])

emma = gutenberg.words('austen-emma.txt')
print("Number of word tokens = " + str(len(emma)))
print("Number of word types = " + str(len(set(w.lower() for w in emma))))



""" 
Answers NLTK 3.6

1. Any combination of lower and uppercase letters (in the English alphabet)
2. Any word starting with a capital letter
3. Any word starting with "p", followed with one or two vowels (excluding y),
   and ending with "t"

"""