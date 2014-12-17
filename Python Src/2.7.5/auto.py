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
				
			if 'find' in x and GrepAttributeFound == False:
				
				GrepAttributeFound = file_attribute(x)
			
			#Makes the same assumptions as find. This is the file that
			#will be access when calling grep	
			elif 'file' in x and FileFound == False:
				
				FileFound = file_attribute(x)
			
			#Sometimes during an iteration, a file must be deleted
			elif 'delete_file' in x and DeleteFileFound == False:
				
				DeleteFileFound = self.delete_file_attribute(x)
			
				
			elif 'username' in x and UsernameFound == False:
				
				UsernameFound = self.username_attribute(x)
				
				
			elif 'max_iterations' in x and MaxIterationsFound == False:
				
				MaxIterationsFound = self.max_iterations_attribute(x)
			
			
			elif 'volume_difference' in x and VolumeDifferenceFound == False:
				
				VolumeDifferenceFound = self.volume_difference_attribute(x)
			
			
			#TODO jobfile needs to be implemented
			elif 'jobfile' in x and JobFileFound == False:
				
				JobFileFound = self.jobfile_attribute(x)
			
			
			#TODO Needs to be implemented throughout the code		
			elif 'verbose' in x and VerboseFound == False:
				
				VerboseFound = self.verbose_attribute(x)
	
	def find_attribute(self , x):
		
		self.GrepAttribute = get_attribute_substring(len('file') , x)
		
		return True
	
	def file_attribute(self , x):
		
		self.Filename = get_attribute_substring(len('file') , x)
		
		return True
	
	def delete_file_attribute(self , x):
		
		self.DeleteFile = get_attribute_substring(len('delete_file') , x)
		
		return True
	
	def username_attribute(self , x):
		
		self.Username = get_attribute_substring( len('username') , x )
		
		return True
	
	def max_iterations_attribute(self , x):
		
		self.MaxIterations = get_attribute_substring(len('max_iterations') , x)
		
		try:
						
			self.MaxIterations = int(self.MaxIterations)
						
		except:
						
			print("Max Iterations could not be represented as an int." + 
					"\nMax iterations will default to 10 iterations")
								
			self.MaxIterations = 10
			
		return True
	
	def volume_difference_attribute(self , x):
		
		self.VolumeDifference	= get_attribute_substring(len('volume_difference') , x)
					
		try:
						
			self.VolumeDifference 	= float(self.VolumeDifference)
			
		except:
						
			print("Volume difference could not be represeted as float." +
					"Please re-execute the \nprogram with required changes,otherwise will default to" +
					" a difference of 0.0\n")
			
			self.VolumeDifference = 0.0
			
		return True
	
	def jobfile_attribute(self , x):
	
		self.JobFile = get_attribute_substring(len('jobfile') , x)
		
		return True
	
	def verbose_attribute(self , x):
					
		try:
						
			self.Verbose = bool(get_attribute_substring(len('verbose') , x))
			
			return True
						
		except:
						
			print("Please be sure to capitalize the first letter in True or False")
			
			return False
					
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

