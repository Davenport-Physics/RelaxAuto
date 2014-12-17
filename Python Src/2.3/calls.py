#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  calls.py
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

from strmanipulation import *

def call_grep(GrepAttribute,Filename):
			
	try:
			
		command	= "grep " + str(GrepAttribute) + " " + str(Filename)
		hold = make_popen_call(command)
		
	except:
			
		print("Init file has missing data, please fix it.")
		exit(1)
	
	if len(hold) == 0:
		
		print("No data was found. Possible bad grep attribute. Stopping execution")
		exit(1)	
		
	if ('\\' + 'n') in hold:
		 		
		lines = split_by_return(hold)
	
	else:
		
		lines = split_without_return(hold)
		
		
		
	return lines
	
def delete_file(filename):
	
	check_for_bad_strings(filename)
		
	try:
			
		command	= "rm " + str(filename)
		hold = make_popen_call(command)
		
	except:
			
		print("Invalid filename most likely")
		
			
def delete_file_which_contains_string(filename):
	
	check_for_bad_strings(filename)
	
	try:
		
		files = get_files_which_contain_string(filename)
		
		for name in files:
			
			command = "rm " + str(name)
			hold = make_popen_call(command)
			
	except:
		
		#TODO
		print("Error 42")
				

#TODO possibility that the file is not called job, and therefore
#bsub<job will have no effect
def make_bsub_job():
		
	try:
			
		command	= "bsub<job"
		hold = make_popen_call(command)
			
	except:
			
		print("Failed creating bsub job")
		
	return hold
		
def call_bsub_jobs():
		
	try:
			
		command	= "bsub jobs"
		hold = make_popen_call(command)
			
	except:
			
		print("Failed to call bsub. Make sure it is installed")
		
	return hold

def make_popen_call(command):
	
	process = os.popen(command)
	hold	= str(process.read())
	
	process.close()
	
	return hold
