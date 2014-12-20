#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
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

from auto import *
from calls import *  

from time import sleep

def main():
	
	obj = Auto()
	
	run_automation(obj)
	
	return 0		


def test_list_files():
	
	files = get_files_which_contain_string('testvasp')
	
	print(files)

def run_automation(obj):
	
	Verbose = obj.get_attribute_by_name("verbose")
	
	#Filename will hold the string of file/s to be deleted after
	#each iteration
	Filename 		= obj.get_files_to_be_deleted()
	PreviousVolume	= 0.0
	
	for x in range(obj.get_attribute_by_name("max_iterations")):
		
		make_bsub_job()
		
		if Verbose == True:
				
			print("Created Job, waiting to finish.")
		
		interval = 0
		#Waits for the job to be finished
		while obj.check_if_job_finished() == False:
			
			sleep(10)
			interval += 10
			if Verbose == True and interval % 20 == 0:
				
				print("%d seconds have passed" % (interval))
				
			
		if Verbose == True:
			
			print("Job is finished")
					
		HadErrors = check_for_errors(obj)		
		
		if obj.get_delete_type() == 1:
			
			delete_file(Filename)
			
		elif obj.get_delete_type() == 2:
			
			if delete_file_which_contains_string(Filename) == True and Verbose == True:
				
				print("Successfully deleted files which contained the string %s" % (Filename))
			
		
			
		#Once the job is finished, it checks the minimum volume difference
		#If the difference has been met, it breaks the for loop.
		if check_volume_difference(obj) == True and HadErrors == False:
			
			break;
			
		if get_volume_difference(get_volumes(obj)) == PreviousVolume:
			
			make_call_with_string(obj.get_attribute_by_name("do_when_error"))
			
		PreviousVolume = get_volume_difference(get_volumes(obj))
			
		print("Iteration %d complete" % (x + 1))
	
	
	
	print("Automated Relaxation finished")

#Checks to see if there are any errors. If there are, the program
#executes a command line program.	
def check_for_errors(obj):
	
	CheckError = obj.get_attribute_by_name("error")
	if type(CheckError) is str:
			
		File 		= obj.get_attribute_by_name("error_file")
		NewestFile	= determine_most_recent_file(get_files_which_contain_string(File))
		hold 		= call_grep(CheckError , NewestFile)
		
		for x in hold:
			
			if obj.check_for_error(x) == True:
				
				make_call_with_string(obj.get_attribute_by_name("do_when_error"))
				
				return True
				
	return False	
	
def print_lines(lines):
	
	for x in lines:
		
		print(x)
	
if __name__ == '__main__':
	main()
