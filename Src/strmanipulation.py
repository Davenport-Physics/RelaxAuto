#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  strmanipulation.py
#  
#  Copyright 2014 Michael Davenport <Davenport.physics@gmail.com>
#  
#  Permission is hereby granted, free of charge, to any person obtaining a 
#  copy of this software and associated documentation files (the "Software"), 
#  to deal in the Software without restriction, including without limitation the 
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
#  sell copies of the Software, and to permit persons to whom the Software is 
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   

import os

"""

delete_extra_spaces deletes spaces at the end of the string that is passed
to it. How it does this, is it starts at the end of the string, and checks
each member of the string until it finds a non-space character. From there
it returns a substring from that point on.

"""
def delete_extra_spaces(string):
	
	for i in range(len(string)-1, 0, -1):
		
		if string[i] != ' ':
			
			return string[:(i + 1)]


"""

split_by_return must be pass a string variable. This function returns
a list of strings, where each member is added to the list by finding
literal \n within the passed string. Essentially equivalent to string.splitlines()
however, that function does not split by literal \n.

"""					
def split_by_return(string):
	
	lines = []
	
	temp = 0
	for x in range(len(string)):
		
		if string[x] == '\\' and string[x+1] == 'n':
		
			lines.append(string[temp:x])
			temp = x + 2
	
	return lines

"""

When call_grep is called, the string returned seems to be dependent
on the current grep installed. Grep 2.18 requires a function call
to split_by_return. Grep 2.16 requires a different function call,
split_without_return because there are no literal \n characters found in 2.16

"""
def split_without_return(string):
	
	return string.splitlines()


"""

returns a string that deletes literal \t (tab markers). This is more
of a compatibilty function, since different versions of grep return
different types of strings. One string might have a literal \t within
the string, while the other one has strings that are tabbed. 

"""		
def delete_tabs(string):
	
	return string.replace("\\t", "")

"""

get_attribute_substring must be passed a start index, and a string. This
function returns a substring, that has no spaces prior to the first 
non-space character.

"""	
def get_attribute_substring(StartIndex , string):
	
	for i in range(StartIndex, len(string)):
		
		if string[i] != ' ':
		
			return string[i:len(string)-1]
			

"""

the same as get_attribute_substring, only used for when you are
expecting a numerical value to be returned.

Somehow the last character gets truncated, and therefore the precision
of a float for instance, will be one less than expected. Why the above
function works as well, but for string substrings is beyond me at the moment.

"""			
def get_numerical_substring(StartIndex , string):
	
	for i in range(StartIndex, len(string)):
		
		if string[i] != ' ':
			
			return string[i:len(string)]
			

"""

check_for_bad_strings determines if there is any "bad" strings
located within the string that is passed. The reason for this is entirely
to avoid unintentional issues that may result in deleting an entire
directory or deleting an assortment of files that have the same string.

"""
def check_for_bad_strings(filename):
	
	if '-rf' in filename or '*' in filename:
		
		print("Error, -rf or * command found in filename.\nExiting program")
		exit(1)

"""

get_files_which_contain_string is passed a string, which is the local
variable filename.

From there, it determines which files in the current directory of the program,
have similar strings in their filename. It then returns a list of strings
that were found to have a similar string.

"""
def get_files_which_contain_string(filename):
	
	files = []
	
	hold = os.listdir('.')
	
	for x in hold:
		
		if filename in x:
			
			files.append(x)
			
	return files
	
"""

determine_most_recent_file must be passed a list of strings, preferably
that each string represents a file within the current directory. I tend
to use get_files_which_contain_string to get a list of files within the directory,
then call this function to determine which one of those files is the
most recent modified file.

The first statement is a feature in modern python, unfortunately max
did not have the key variable in earlier python versions, so this
script cannot take advantage of any optimization related to that, and instead
opts for a slightly longer method of determining the most recent file.

"""
	
def determine_most_recent_file(files):
	
	try:
		
		return max(files, key = os.path.getctime)
		
	except:

		times = []
		
		for x in files:
			
			times.append(os.path.getctime(x))
			
		maxtime = max(times)
		
		for x in files:
			
			if maxtime == os.path.getctime(x):
				
				return x
				
		return False
