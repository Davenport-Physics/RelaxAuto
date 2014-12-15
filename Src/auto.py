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
from strmanipulation import *
	
class Auto(object):
	
	def __init__(self):
		
		self.read_init_file()
		self.determine_init_attributes()
	
		self.lines = call_grep(self.GrepAttribute,self.Filename)
		
		for x in range(len(self.lines)):
			
			self.lines[x] = delete_tabs(self.lines[x])
					
					
	def read_init_file(self):
		
		try:
		
			fp	= open("autoinit", "r")
		
		except:
			
			print("No autoinit file found. Please be sure to create one")
			exit(1)
		
		self.InitData	= []
		
		for x in fp:
			
			self.InitData.append(str(x))
		
		fp.close()
		
	def determine_init_attributes(self):
		
		#Grep
		self.GrepAttribute		= False 
		GrepAttributeFound		= False
		
		#Filename
		self.Filename			= False
		FilenameFound			= False
		
		#job file
		self.JobFile			= False
		JobFileFound			= False
		
		#volume diff
		self.VolumeDifference	= False
		VolumeDifferenceFound	= False
		
		#Max interations
		self.MaxIterations		= False
		MaxIterationsFound		= False
		
		#User name
		self.Username			= False
		UsernameFound			= False
		
		#Program Verbosity
		self.Verbose			= False
		VerboseFound			= False
		
		#Delete file
		self.DeleteFile			= False
		DeleteFileFound			= False
		
		for x in self.InitData:
			
			#You can now have comments anywhere
			if '#' in x:
				
				if x[0] == '#':
					
					continue
					
				else:
				
					i = get_char_index('#',x)
					x = str(delete_extra_spaces(x[:i]))
				
			if 'find' in x:
				
				#This portion of the code determines the grep command
				#it is not complex and makes the assumption that between
				#find and your command is a space.
				if GrepAttributeFound == False:
					
					GrepAttributeFound = True
					self.GrepAttribute = get_attribute_substring(len('file') , x)
					
				else:
					
					print("Error, too many find strings")
			
			#Makes the same assumptions as find. This is the file that
			#will be access when calling grep	
			elif 'file' in x:
				
				if FilenameFound == False:
					
					FilenameFound	= True
					self.Filename	= get_attribute_substring(len('file') , x)
					
				else:
					
					print("Error, too many file strings")
			
			#Sometimes during an iteration, a file must be deleted
			elif 'delete_file' in x:
				
				if DeleteFileFound == False:
					
					DeleteFileFound = True
					self.DeleteFile = get_attribute_substring(len('delete_file') , x)
					
				else:
					
					print("Too many delete_file attributes found")
				
			elif 'username' in x:
				
				if UsernameFound == False:
					
					UsernameFound = True
					self.Username = get_attribute_substring(len('username'), x)
					
				else:
					
					print("Too many usernames found")
				
				
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
			
			#TODO jobfile needs to be implemented
			elif 'jobfile' in x:
				
				if JobFileFound == False:
					
					JobFileFound	= True
					self.JobFile	= get_attribute_substring(len('jobfile') , x)
					
				else:
					
					print("Too many Job attributes")
			
			#TODO Needs to be implemented throughout the code		
			elif 'verbose' in x:
				
				if VerboseFound == False:
					
					VerboseFound 		= True
					
					try:
						
						self.Verbose	= bool(get_attribute_substring(len('verbose') , x))
						
					except:
						
						print("Please be sure to capitalize the first letter in True or False")
					
				else:
					
					print("Too many verbose attributes found")
					
					
	#checks to make that specific attributes are within the autoinit
	#file. If not, the program ceases execute, after informing the user
	#of what data is missing.			
	def check_attributes(self):
		
		QuitProgram = False
		
		if self.Filename == False:
			
			print("Missing filename attribute")
			QuitProgram = True
			
		elif self.GrepAttribute == False:
			
			print("Missing grep attribute")
			QuitProgram = True
			
		if QuitProgram == True:
			
			print("Please add these attributes to autoinit before runtime")
			quit(1)
			
	
	def get_max_iterations(self):
		
		return self.MaxIterations
		
	def get_verbose(self):
		
		return self.Verbose
		
	def get_files_to_be_deleted(self):
		
		return self.DeleteFile
		
	def check_if_job_finished(self):
		
		lines = call_bsub_jobs()
		
		for x in lines:
			
			if self.Username in x:
				
				return True
		
		return False
		
	def check_volume_difference(self):
		
		lines = call_grep(self.GrepAttribute,self.Filename)
		
		if abs(lines[0] - lines[len(lines)-1]) > self.VolumeDifference:
			
			return False
			
		else:
			
			return True
		
	#Prints every line within the lines variable to the terminal
	def print_lines(self):
		
		try:
			
			for x in self.lines:
			
				print(x)
				
		except:
			
			print("Grep was probably never called")

