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

def get_char_index(character, string):
	
	for i in range(len(string)):
		
		if string[i] == character:
			
			return i

def delete_extra_spaces(string):
	
	for i in range(len(string)-1 ,0 , -1):
		
		if string[i] != ' ':
			
			return string[:(i + 1)]
			
def split_by_return(string):
	
	lines = []
	
	temp = 0
	for x in range(len(string)):
		
		if string[x] == '\\':
		
			if string[x + 1] == 'n':
				
				lines.append(string[temp:x])
				temp = x + 2
	
	return lines
			
def delete_tabs(string):
	
	i = 0
	while i < len(string):
		
		try:
			
			if string[i] == '\\' and string[i+1] == 't':
			
				string = string[i+2:len(string)]
				i = 0
				
			else:
				
				i += 1
			
		except:
			
			pass
			
	return string
			
def get_attribute_substring(StartIndex , x):
	
	for i in range(StartIndex, len(x)):
		
		if x[i] == ' ':
			
			continue
			
		else:
			
			return x[i:len(x)-1]
			
