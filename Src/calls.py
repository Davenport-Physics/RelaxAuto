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
		
	lines = []
	
	temp = 0
	for x in range(len(hold)):
		
		if hold[x] == '\\':
		
			if hold[x + 1] == 'n':
				
				lines.append(hold[temp:x])
				temp = x + 2
				
	return lines

def make_bsub_job():
		
	try:
			
		command	= "bsub<job"
		hold	= ""
			
	except:
			
		print("Failed")
		
def call_bsub_jobs():
		
	try:
			
		command	= "bsub jobs"
		hold	= str(sp.check_output(command,shell=True))
			
	except:
			
		print("Failed to call bsub. Make sure it is installed")
		

