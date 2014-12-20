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

#	class Auto
#
#	During initialization, several function are called to help divide
#	the work load.
#
#	read_init_file, looks for a file called autoinit. It reads every line
#	found within autoinit and places that data into self.InitData which
#	is a list of strings
#
#	determine_init_attributes goes through every line of self.InitData
# 	and looks for a variety of strings within each line, and if one is found
#	it then initializes a corresponding variable.
#
#
#	attributes
#
#	'#' is the probably the most common attribute, and it is the comment
#	indentifier. When this is found within a line, further processing on
#	on that line is done and a new substring is returned without '#' or any
#	data to the right of that.
#
#	'find' tells the program which command to use it when calling grep. Or rather
#	which string of data grep should look for within a file
#
#	'file' tells the program which file to access while grep is being called
#
#	
#	
class Auto(object):
	
	def __init__(self):
		
		self.read_init_file()
		self.init_attribute_objects()
		self.determine_init_attributes()
		self.check_attributes()			
		
					
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
	
		
	def init_attribute_objects(self):
		
		#Grep
		self.GrepAttribute		= Attribute("find","string")
		#Filename
		self.Filename			= Attribute("file","string")
		#job file
		self.JobFile			= Attribute("jobfile","string")
		#volume diff
		self.VolumeDifference	= Attribute("volume_difference","float")
		#Max interations
		self.MaxIterations		= Attribute("max_iterations","int")
		#User name
		self.Username			= Attribute("username","string")
		#Program Verbosity
		self.Verbose			= Attribute("verbose","boolean")
		#Delete file
		self.DeleteFile			= Attribute("delete_file_strict","string")
		#Deletes a file that contains a portion of this string
		self.DeleteFileContains	= Attribute("delete_file_which_contains","string")
		#check_for_error
		self.ErrorFile			= Attribute("error_file","string")
		#when_error
		self.DoWhenError		= Attribute("do_when_error","string")
		#error
		self.ErrorString		= Attribute("error","string")
		
		
		self.objlist = []
		self.objlist.append(self.GrepAttribute)
		self.objlist.append(self.Filename)
		self.objlist.append(self.JobFile)
		self.objlist.append(self.VolumeDifference)
		self.objlist.append(self.MaxIterations)
		self.objlist.append(self.Username)
		self.objlist.append(self.Verbose)
		self.objlist.append(self.DeleteFile)
		self.objlist.append(self.DeleteFileContains)
		self.objlist.append(self.ErrorFile)
		self.objlist.append(self.DoWhenError)
		self.objlist.append(self.ErrorString)
		
		
	def determine_init_attributes(self):
		
		for x in self.InitData:
			
			#You can now have comments anywhere
			if '#' in x:
				
				if x[0] == '#':
					
					continue
					
				else:
				
					i = get_char_index('#' , x)
					x = str(delete_extra_spaces(x[:i]))
				
			for i in range( len( self.objlist ) ):
				
				if self.objlist[i].get_name() in x and self.objlist[i].get_boolean() == False:
					
					
					if 'string' in self.objlist[i].get_attribute_type(): 
						
						self.objlist[i].set_attribute(get_attribute_substring(len(self.objlist[i].get_name()) , x))
						self.objlist[i].set_boolean(True)
						
						
					elif 'float' in self.objlist[i].get_attribute_type():
						
						
						if 'volume_difference' in self.objlist[i].get_name():
							
							self.volume_difference_attribute(x)
						
						
					elif 'int' in self.objlist[i].get_attribute_type():
						
						
						if 'max_iterations' in self.objlist[i].get_name():
							
							self.max_iterations_attribute(x)
							
							
					elif 'boolean' in self.objlist[i].get_attribute_type():
						
						
						if 'verbose' in self.objlist[i].get_name():
							
							self.verbose_attribute(x)
					
	
	#checks to make that specific attributes are within the autoinit
	#file. If not, the program ceases execute, after informing the user
	#of what data is missing.			
	def check_attributes(self):
		
		if self.Filename.get_boolean() == False:
			
			print("Missing filename attribute")
			exit(1)
			
		elif self.GrepAttribute.get_boolean() == False:
			
			print("Missing grep attribute")
			exit(1)
		
		#When one is found to be a boolean type, then this command will not
		#function properly and therefore to prevent it from running. Therefore
		#all three variables are then set to False
		if type(self.ErrorFile.get_attribute()) is bool or type(self.ErrorString.get_attribute()) is bool or type(self.DoWhenError.get_attribute()) is bool:
			
			self.ErrorFile.set_boolean(False)
			self.ErrorString.set_boolean(False)
			self.WhenError.set_boolean(False)
			
			
	def max_iterations_attribute(self , x):
		
		Max = get_attribute_substring(len(self.MaxIterations.get_name()) , x)
		
		try:
						
			self.MaxIterations.set_attribute( int( Max ) )
						
		except:
						
			print("Max Iterations could not be represented as an int." + 
					"\nMax iterations will default to 10 iterations")
								
			self.MaxIterations.set_attribute(10)
			
		return True
	
	
	def volume_difference_attribute(self , x):
		
		Difference = get_attribute_substring(len(self.VolumeDifference.get_name()) , x)
					
		try:
						
			self.VolumeDifference.set_attribute( float( Difference ) )
			
		except:
						
			print("Volume difference could not be represeted as float." +
					"Please re-execute the \nprogram with required changes,otherwise will default to" +
					" a difference of 0.0\n")
			
			self.VolumeDifference.set_attribute(0.0)
			
		return True
	
	
	def verbose_attribute(self , x):
					
		try:
						
			self.Verbose.set_attribute(bool(get_attribute_substring( len('verbose') , x)))
			
			return True
						
		except:
						
			print("Please be sure to capitalize the first letter in True or False")
			
			return False
	
	
	def get_attribute_by_name(self , name):
		
		for i in range( len( self.objlist ) ):
			
			if name in self.objlist[i].get_name():
				
				return self.objlist[i].get_attribute()
				
		if self.Verbose.get_attribute() == True:
			
			print("Did not find corresponding attribute with name %s" % (name))
						
							
	def get_files_to_be_deleted(self):
		
		if type(self.DeleteFile.get_attribute()) is str:
		
			return self.DeleteFile.get_attribute()
			
			
		if type(self.DeleteFileContains.get_attribute()) is str:
			
			return self.DeleteFileContains.get_attribute()

		return False
		
		
	# 1 - literal delete, 2 - delete file that contains string, -1 no deletion
	def get_delete_type(self):
		
		if type(self.DeleteFile.get_attribute()) is str:
			
			return 1
			
		if type(self.DeleteFileContains.get_attribute()) is str:
			
			return 2
			
		return -1
	
		
	def check_for_error(self , x):
		
		if self.ErrorString.get_attribute() in x:
			
			return True
			
		return False
	
		
	def check_if_job_finished(self):
		
		lines = call_bsub_jobs()
		
		if self.Username.get_attribute() in lines:
			
			return False
		
		return True
	
		
class Attribute:
	
	def __init__(self,name,AttributeType):
		
		self.name				= name
		self.AttributeType		= AttributeType
		self.AttributeString	= False
		self.boolean			= False	
	
			
	def set_attribute(self,attribute):
		
		self.AttributeString = attribute
	
	
	def set_boolean(self,boolean):
		
		self.boolean = boolean
	
		
	def get_name(self):
		
		return self.name
	
		
	def get_attribute(self):
		
		return self.AttributeString
	
			
	def get_boolean(self):
		
		return self.boolean
		
	
	def get_attribute_type(self):
		
		return self.AttributeType

		
def check_volume_difference(obj):
		
	volume = get_volumes()
	
	if obj.get_attribute_by_name("verbose") == True:
		
		print("Volume 1 = %f, Volume 2 = %f" % (volume[0],volume[1]))	
		print("Volume difference found to be %f" % (abs(volume[0] - volume[1])))
			
		
	if abs(volume[0] - volume[1]) > obj.get_attribute_by_name("volume_difference"):
		
		return False
			
	else:
			
		return True
		
def get_volumes(obj):
	
	lines = call_grep(obj.get_attribute_by_name("find"),obj.get_attribute_by_name("file")
	
	return find_first_last_volume(lines , obj.get_attribute_by_name("verbose"))
	
def get_volume_difference(volume):
	
	return abs(volume[0] - volume[1])

	
def find_first_last_volume(lines , Verbose):
	
	FirstVolume = float(get_numerical_substring(get_char_index(':',lines[1])+1,lines[1]))
	LastVolume	= float(get_numerical_substring(get_char_index(':',lines[len(lines)-1])+1,lines[len(lines)-1]))
	
	return [FirstVolume,LastVolume]

			
def find_min_max_volume(lines,Verbose):
		
	MaxVolume = MinVolume = float(get_attribute_substring(get_char_index(':',lines[1])+1, lines[1]))
		
	for x in range(2 , len(lines)):
			
		index	= get_char_index(':' , lines[x]) + 1
		TempMax	= TempMin = float(get_attribute_substring(index,lines[x]))
			
		if TempMax > MaxVolume:
				
			MaxVolume = TempMax
			
		if TempMin < MinVolume:
				
			MinVolume = TempMin
			
	if Verbose == True:
			
		print("Max Volume found to be %f. Min Volume found to be %f" % (MaxVolume,MinVolume))	
			
	return [MaxVolume,MinVolume]
		
		
