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

## @package main
#
#  main file where the automation takes place. Usually this code
#  will not be modified, and should not be modified unless you plan
#  on editing the automation of the program itself.

"""

The main function doesn't have a lot of code to itself, and the reason
for this is because I wanted a program that could be applicable in
different ways, and populating the main function with commands would result
in some inherent difficulties with applying the script to different applications.

So the main function will normally just initialize an object and call a function.

It's a good function to use if you want to test any of the functions throughout
the script, to weed out bugs.

Aside that, by default it initializes an auto object, and calls the
run_automation function, passing a reference (memory address) to the auto object it
initialized

"""

def main():
	
	obj = Auto()
	
	run_automation(obj)
	
	return 0
	
"""

run_automation will begin by determining whether the user wanted
the program to print out information in a verbose manner, hence the use
of the Verbose variable. It does this by calling get_attribute_by_name, and
passing "verbose" to it. get_attribute_by_name will search for an object
that has that name, and return a attribute of that object.

Then the program initializes an object Filename, which gets a single string
or a list of files to be deleted. This is dependent on what the
user provides in the autoinit config file. One object is delete_file_strict
which tells the program that if it sees a file that is verbatim that string
it should delete it. There is a list determined by the delete_file_which_contains
string in the config file, which returns a list of any file that has a portion
of that string in it's filename


PreviousVolume is a object that is initialized to 0.0. It's used to determine
whether an "pseudo-error" has happened. I say pseudo-error, because it's
not an error in the traditional sense, yet it makes the same function
call as if there was an error. The same action happens. mv CONTCAR POSCAR
So the error is determined by whether the previous volume and the current
volume are the same. If they are, then there is a "pseudo-error".

The code then goes into a for loop, which runs a maximum of iterations
defined by the value in the max_iterations object. By default it's 10, if
the config file failed to find a max_iterations attribute

the for loop initially makes a function call to make_bsub_job, which
calls the command line command "bsub<job" which submit's a job to the 
computer cluster.

In while loop, it checks to see if the job is done. This is determined
by making a function call to check_if_job_finished, which determines
whether the queue has a string that is verbatim to the username
defined in the config file. The function returns false, if it finds that
the queue still has a string with the user's username.

The program then checks for errors, by making a function call to check_for_errors.
Afterwards it deletes any files that the user has specified in the config file.
The program is not required to delete any files.

At the very end, it checks to volume difference and whether the program had
any errors. In the event that there wasn't any errors, and the volume difference
is less than or equal to what the user defined in the config file, the
code will break and the program will halt execution, informing the user
that the automated relaxation was finished.

"""		
## The primary function for running the volume automation logic
#
#  @param Auto Object variable
#
#  This function should only ever be called once during the entire
#  execution of the program.
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


"""

check_for_errors begins by determining whether the value returned by
get_attribute_by_name is a string type. If it is, this is 
the error the program will be looking for, when it calls grep.

In the event that it is a string type, the function follows by obtaining a
string of expect file names if "error" is passed to get_attribute_by_name,
then this function will return a name that will not be verbatim to
any file. This name is then passed to get_files_which_contain_string,
which returns a list of files that have the string within their filename.

From there determine_most_recent_file is called, and is passed this list.
It determines which of the file that's located within the list, is the newest
, as in has the greatest time stamp value. This is in the event that the user
decides not provide a delete_file attribute.

Then the function calls call_grep passing CheckError and the NewestFile variables.
call_grep will return a list of strings.

If the error is located within the list of strings, then the function
will call make_call_with_string, and will pass the attribute of the do_when_error
object. By default this is mv CONTCAR POSCAR


"""

## Checks for errors within the volume relaxation automation
#
#  @param Auto object variable
#
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
