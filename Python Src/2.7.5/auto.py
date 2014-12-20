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
from attributes import *
from strmanipulation import *


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
		self.GrepAttribute		= Attribute("find")
		#Filename
		self.Filename			= Attribute("file")
		#job file
		self.JobFile			= Attribute("jobfile")
		#volume diff
		self.VolumeDifference	= FloatAttribute("volume_difference" , 0.0)
		#Max interations
		self.MaxIterations		= IntAttribute("max_iterations" , 10)
		#User name
		self.Username			= Attribute("username")
		#Program Verbosity
		self.Verbose			= BooleanAttribute("verbose" , True)
		#Delete file
		self.DeleteFile			= Attribute("delete_file_strict")
		#Deletes a file that contains a portion of this string
		self.DeleteFileContains	= Attribute("delete_file_which_contains")
		#check_for_error
		self.ErrorFile			= Attribute("error_file")
		#when_error
		self.DoWhenError		= Attribute("do_when_error")
		#error
		self.ErrorString		= Attribute("error")
		
		
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
				
					i = x.find("#")
					x = str(delete_extra_spaces(x[:i]))
				
			for i in range( len( self.objlist ) ):
				
				if self.objlist[i].get_name() in x and self.objlist[i].get_boolean() == False:
					
					self.objlist[i].initialize_attribute(x)
					self.set_boolean(True)
					
	
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
			self.DoWhenError.set_boolean(False)
			
			
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
	
				
def check_volume_difference(obj):
		
	volume = get_volumes(obj)
	
	if obj.get_attribute_by_name("verbose") == True:
		
		print("Volume 1 = %f, Volume 2 = %f" % (volume[0],volume[1]))	
		print("Volume difference found to be %f" % (abs(volume[0] - volume[1])))
			
		
	if abs(volume[0] - volume[1]) > obj.get_attribute_by_name("volume_difference"):
		
		return False
			
	else:
			
		return True
		
def get_volumes(obj):
	
	lines = call_grep(obj.get_attribute_by_name("find"),obj.get_attribute_by_name("file"))
	
	return find_first_last_volume(lines , obj.get_attribute_by_name("verbose"))
	
	
def get_volume_difference(volume):
	
	return abs(volume[0] - volume[1])

	
def find_first_last_volume(lines , Verbose):
	
	FirstVolume = float(get_numerical_substring(lines[1].find(":")+1,lines[1]))
	LastVolume	= float(get_numerical_substring(lines[-1].find(":")+1,lines[-1]))
	
	return [FirstVolume,LastVolume]

			
def find_min_max_volume(lines,Verbose):
		
	MaxVolume = MinVolume = float(get_attribute_substring(lines[1].find(":")+1, lines[1]))
		
	for x in range(2 , len(lines)):
			
		index	= lines[x].find(":") + 1
		TempMax	= TempMin = float(get_attribute_substring(index,lines[x]))
			
		if TempMax > MaxVolume:
				
			MaxVolume = TempMax
			
		if TempMin < MinVolume:
				
			MinVolume = TempMin
			
	if Verbose == True:
			
		print("Max Volume found to be %f. Min Volume found to be %f" % (MaxVolume,MinVolume))	
			
	return [MaxVolume,MinVolume]
		
		
