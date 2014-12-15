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

import subprocess as sp

from strmanipulation import *

def call_grep(GrepAttribute,Filename):
		
	#shell=True is a security risk, when the shell commands are
	#determined at runtime. This needs to be changed to
	#popen to eliminate this security hole.
		
	try:
			
		command	= "grep " + str(GrepAttribute) + " " + str(Filename)
		hold	= str(sp.check_output(command, shell=True))
		
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
	
	if '-rf' in filename or '*' in filename:
		
		print("Error, -rf or * command found in filename.\nExiting program")
		exit(1)
		
	else:
		
		try:
			
			command	= "rm " + str(filename)
			hold	= str(sp.checkout_output(command,shell=True))
		
		except:
			
			print("Invalid filename most likely")
			

def make_bsub_job():
		
	try:
			
		command	= "bsub<job"
		hold	= str(sp.check_output(command,shell=True))
			
	except:
			
		print("Failed creating bsub job")
		
	return hold
		
def call_bsub_jobs():
		
	try:
			
		command	= "bsub jobs"
		hold	= str(sp.check_output(command,shell=True))
			
	except:
			
		print("Failed to call bsub. Make sure it is installed")
		
	return hold

