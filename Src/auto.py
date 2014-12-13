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

from calls import *
	
class auto(object):
	
	def __init__(self):
		
		self.read_init_file()
		self.determine_init_attributes()
	
		self.lines = call_grep(self.GrepAttribute,self.Filename)
					
					
	def read_init_file(self):
		
		fp = open("autoinit", "r+")
		
		self.InitData = []
		
		for x in fp:
			
			self.InitData.append(str(x))
		
		fp.close()
		
	def determine_init_attributes(self):
		
		self.GrepAttribute		= False 
		GrepAttributeFound		= False
		
		self.Filename			= False
		FilenameFound			= False
		
		self.JobFile			= False
		JobFileFound			= False
		
		self.VolumeDifference	= False
		VolumeDifferenceFound	= False
		
		self.MaxIterations		= False
		self.MaxIterationsFound	= False
		
		for x in self.InitData:
			
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
				if GrepAttributeFound == False:
					
					GrepAttributeFound = True
					self.GrepAttribute = get_attribute_substring(len('file') , x)
					
				else:
					
					print("Error, too many find strings")
			
			#Makes the same assumptions as find.		
			elif 'file' in x:
				
				if FilenameFound == False:
					
					FilenameFound	= True
					self.Filename	= get_attribute_substring(len('file') , x)
					
				else:
					
					print("Error, too many file strings")
				
			elif 'check' in x:
				
				print("check not implemented")
				
			elif 'username' in x:
				
				print("Username not implemented\n")
				
			elif 'max_iterations' in x:
				
				if MaxIterationsFound == False:
					
					MaxIterationsFound	= True
					self.MaxIterations	= get_attribute_substring(len('max_iterations'), x)
					
					try:
						
						self.MaxIterations = int(self.MaxIterations)
						
					except:
						
						print("Max Iterations could not be represented as an int." + 
								"\nMax iterations will default to 10 iterations")
								
						self.MaxIterations = 10
				
				else:
					
					print("Too many max_iterations defined")
				
			elif 'volume_difference' in x:
				
				if VolumeDifferenceFound == False:
					
					VolumeDifferenceFound	= True
					self.VolumeDifference	= get_attribute_substring(len('volume_difference') , x)
					
					try:
						
						self.VolumeDifference 	= float(self.VolumeDifference)
					
					except:
						
						print("Volume difference could not be represeted as float." +
								"Please re-execute the \nprogram with required changes,otherwise will default to" +
								" a difference of 0.0\n")
						
						self.VolumeDifference	= 0.0
					
				else:
					
					print("Too many volume difference attributes")
				
			elif 'jobfile' in x:
				
				if JobFileFound == False:
					
					JobFileFound	= True
					self.JobFile	= get_attribute_substring(len('jobfile') , x)
					
				else:
					
					print("Too many Job attributes")
					
					
	#checks to make that specific attributes are within the autoinit
	#file. If not, the program ceases execute, after informing the user
	#of what data is missing.			
	def check_attributes(self):
		
		QuitProgram = False
		
		if self.Filename == False:
			
			print("Missing filename attribute")
			QuitProgram = True
			
		if self.GrepAttribute == False:
			
			print("Missing grep attribute")
			QuitProgram = True
			
		if QuitProgram == True:
			
			print("Please add these attributes to autoinit before runtime")
			quit(1) 
		
	#Prints every line within the lines variable to the terminal
	def print_lines(self):
		
		for x in self.lines:
			
			print(x)

		
def get_attribute_substring(StartIndex , x):
	
	for i in range(StartIndex, len(x)):
		
		if x[i] == ' ':
			
			continue
			
		else:
			
			return x[i:len(x)-1]
			
