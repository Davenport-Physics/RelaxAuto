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
	#obj.print_lines()
	#print(obj.check_volume_difference())
	
	run_automation(obj)
	
	return 0

def run_automation(obj):
	
	Verbose = obj.get_verbose()
	
	#Filename will hold the string of file/s to be deleted after
	#each iteration
	Filename = obj.get_files_to_be_deleted()
	
	for x in range(obj.get_max_iterations()):
		
		make_bsub_job()
		
		if Verbose == True:
				
			print("Created Job, waiting to finish.")
		
		#Waits for the job to be finished
		while obj.check_if_job_finished() == False:
			
			interval = 0
			
			sleep(5)
			if Verbose == True and interval % 10 == 0:
				
				print("%d seconds have passed" % (interval))
				
			interval += 5
				
			
		if Verbose == True:
			
			print("Job is finished")
		
		if obj.get_delete_type() == 1:
			
			delete_file(Filename)
			
		elif obj.get_delete_type() == 2:
			
			delete_file_which_contains_string(Filename)
			
		
			
		#Once the job is finished, it checks the minimum volume difference
		#If the difference has been met, it breaks the for loop.
		if check_volume_difference(obj.get_grep_attribute(),obj.get_filename(),obj.get_volume_difference()) == True:
			
			break;
			
		print("Iteration %d complete" % (x + 1))
	
	
	
	print("Automated Relaxation finished")
	
def print_lines(lines):
	
	for x in lines:
		
		print(x)
	
if __name__ == '__main__':
	main()
