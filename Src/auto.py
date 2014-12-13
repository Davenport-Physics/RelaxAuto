#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  auto.py
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

import subprocess as sp

def main():
	
	obj = auto()
	
	obj.print_lines()
	
	return 0
	
class auto(object):
	
	def __init__(self):
		
		self.read_init_file()
		self.determine_init_attributes()
		
		#shell=True is a security risk, when the shell commands are
		#determined at runtime. This needs to be changed to
		#popen to eliminate this security hole.
		
		try:
			command	= "grep " + str(self.grep_attribute) + " " + str(self.file_attribute)
			hold	= str(sp.check_output(command, shell=True))
		
		except:
			
			print("Init file has missing data, please fix it.")
			exit(1)
		
		self.lines = []
	
		temp = 0
		for x in range(len(hold)):
		
			if hold[x] == '\\':
			
				if hold[x + 1] == 'n':
				
					self.lines.append(hold[temp:x])
					temp = x + 2
					
					
	def read_init_file(self):
		
		fp = open("autoinit", "r+")
		
		self.init_data = []
		
		for x in fp:
			
			self.init_data.append(str(x))
		
		fp.close()
		
	def determine_init_attributes(self):
		
		self.grep_attribute		= False 
		grep_attribute_found	= False
		
		self.file_attribute		= False
		file_attribute_found	= False
		
		for x in self.init_data:
			
			#If there is a pound symbol within the line
			#the entire line is considered a comment
			#Later on I might change this, but for the moment
			#this suffices.
			if '#' in x:
				
				continue
				
			elif 'find' in x:
				
				#This portion of the code determines the grep command
				#it is not complex and makes the assumption that between
				#find and your command is a space.
				if grep_attribute_found == False:
					
					grep_attribute_found = True
					
					for i in range( 4 , len(x) ):
						
						if x[i] == ' ':
							
							continue
						
						else:
							
							self.grep_attribute = x[i:len(x)-1]
							break
					
				else:
					
					print("Error, too many find strings")
			
			#Makes the same assumptions as find.		
			elif 'file' in x:
				
				if file_attribute_found == False:
					
					for i in range( 4, len(x) ):
						
						if x[i] == ' ':
							
							continue
								
						else:
							
							self.file_attribute = x[i:len(x)-1]
							break
				
				else:
					
					print("Error, too many file strings")
				
			elif 'check' in x:
				
				print("check not implemented")
				
			elif "username" in x:
				
				print("Username not implemented")
					
				
	
	#Prints every line to the terminal
	def print_lines(self):
		
		for x in self.lines:
			
			print(x)
		

if __name__ == '__main__':
	main()

