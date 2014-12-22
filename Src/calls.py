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

from strmanipulation import *

## @package calls
#
#  System calls

"""

In an effort to maintain compatibility between modern python, and 
python 2.3, throughout this source file there will be several instances
where I call functions that are currently deprecated. This code is
written in the hopes that it runs both on python 2.7.5 and 2.3.x I fully
suspect that this code will run in python 3.x but I have no conducted
any tests myself.

The try-except statement below is this first compatibility patch.
Subprocess is a library that deprecated several functions in the os library.
Unfortunately these subprocess was not included until later, and the
os functions were deprecated in python 2.6

There is a single Global variable SubProcessFound, which allows
the code to determine the correct function to call, given the available
libraries at runtime.

It is be default set as True, and set to false if an exception is found
while trying to import subprocess.

"""

SubProcessFound = True

try:

	import subprocess as sp
	
except:
	
	SubProcessFound = False
	import os
	
"""

When I began naming the functions, I tried to make it as obvious as
possible as to what they do. call_grep by all reasonable assumptions 
should make a system call to grep, and in fact it does. 

In order to effectively use call_grep, you must pass two variables to it.
They do not already have to be strings, as the code type casts both
variables to string.

GrepAttribute is the first command that is appended after "grep ". Naturally,
this variable should be the string that you are interested in searching for.

Filename is then appended afterwards, and as the name suggests, this should
be the name of the file you want to search the GrepAttribute in.

Finally make_call is called, passing this string with the appended
variables. make_call should pass a string variable.The variable hold 
will be set to this string variable. Afterwards, the length of hold
will be checked, and if it's zero the user will be informed that
there was a bad provided grep file. If for some reason there is an
exception here, call_grep will return an empty string.

Then the code splits hold into a list, by either calling the function
split_by_return or split_without_return. The reason for the existence
of both functions is again a compatibility issue. Some versions of grep
will return a string with literal \n and \t within the string, while
others will naturally split the string using carriage returns.

The call_grep function will return a list.

"""	

## Calls the grep function
#
#  @param GrepAttribute is a string variable which will hold the grep string
#  @param Filename is a string variable which will hold the string used during the grep call
#
#  @return returns a list of strings, where each member is a line returned by grep.

def call_grep(GrepAttribute,Filename):
	
		
	try:
			
		command	= "grep " + str(GrepAttribute) + " " + str(Filename)
		hold    = make_call(command)
		
	except:
			
		print("Init file has missing data, please fix it.")
		exit(1)
	
	
	try:
		
		if len(hold) == 0:
		
			print("No data was found. Possible bad grep attribute")
	
	except:
		
		return ""
		
	if ('\\' + 'n') in hold:
		 		
		lines = split_by_return(hold)
	
	else:
		
		lines = split_without_return(hold)
		
		
	return lines

"""

delete_file, requires a variable to be passed to it. It does not have
to be initially a string type, however it is highly suggested if you
want any reasonable applicability to this function.

Before calling the make_call function, this function will check filename
for "bad" strings. What is considered a bad string are strings that can
add unattended behavior such as the '-rf' argument which can delete an
entire directory or '*' which can delete a wide range of files that
have similar strings.

check_for_bad_strings will in fact terminate the execution of the
program if it detects a "bad" string within the filename variable.

In the event that the filename passes, the variable filename will be
typecasted as a string type, and appended to a string "rm ".

"""	

## Deletes a file
#  
#  @param filename is a string variable, which should be verbatim to file that will be deleted
#	
def delete_file(filename):
	
	check_for_bad_strings(filename)
		
	try:
			
		command	= "rm " + str(filename)
		hold	= make_call(command)
		
	except:
			
		print("Invalid filename most likely")
		

"""

delete_file_which_contains_string will delete any files that contain
a similar string in their name.

Like the function delete_file, this function will check for "bad" strings
and determine whether to halt execution or not.

Assuming the function doesn't halt, a call to get_files_which_contain_string
is called, with the filename variable passed to it. This function
will return a list of files that have a similar string within their
filename.

Then the code runs through a for loop, appending each string within
the files list to "rm " and calls make_call.

I realize this adds a lot of overhead to this script, just by the potential
amount of system calls it could do, when a single call with an append "*"
would have sufficed. I may change this later on, but for now it's staying.

"""			
def delete_file_which_contains_string(filename):
	
	check_for_bad_strings(filename)
	
	try:
		
		files = get_files_which_contain_string(filename)
		
		for name in files:
			
			command = "rm " + str(name)
			hold	= make_call(command)
			
	except:
		
		print("Couldn't delete files")
		return False
		
	return True
				

"""

make_bsub_job is a very simple function. You do not pass any data to it,
as it just makes a function call to make_call with string "bsub<job"

TODO possibility that the job file is not called job, and therefore
this system call would have no effect.

"""
def make_bsub_job():
		
	try:
			
		command	= "bsub<job"
		hold	= make_call(command)
			
	except:
			
		print("Failed creating bsub job")
		
	return hold
		
"""

call_bsub_jobs calls the functio make_call with the string "bjobs"

"""		
def call_bsub_jobs():
		
	try:
			
		command	= "bjobs"
		hold	= make_call(command)
		
	except:
			
		print("Failed to call bjobs. Make sure it is installed")
	
	return hold

"""

make_call_with_string, is passed a command variable. This function is
primarily used for the execution of a system call that is defined at runtime.

The config file has one attribute do_when_error, that provides a system
call that uses this function.

The command is of course checked for bad strings, and if execution is not
halted then make_call is called with this command variable passed.

"""

def make_call_with_string(command):
	
	check_for_bad_strings(command)
	
	hold = make_call(command)
	
	return hold

"""

I don't ever recommend calling this function, or the functions
below it directly. Primarily because this function is the primary
function that allows for compatibility between python 2.3 and contemporary
python.

To use this function, I highly recommend that you create another
function that calls this. This other function should check for bad
strings and should do any pre-processing that is required.

make_call will check the global variable SubProcessFound, and if it
is True it will call the function make_subprocess_call that uses
the modern and not deprecated method of making a system call. Otherwise
it will call the function make_popen_call which is deprecated in
contemporary python but the only option in older python versions.

make_call will return a string. It is up to the user to convert it to a
list if they want.

"""
def make_call(command):
	
	global SubProcessFound
	
	hold = ""
	
	if SubProcessFound:
		
		hold = make_subprocess_call(command)
		
	else:
		
		hold = make_popen_call(command)
		
	return hold


def make_subprocess_call(command):
	
	return str(sp.check_output(command,shell=True))


def make_popen_call(command):
	
	process = os.popen(command)
	hold	= str(process.read())
	
	process.close()
	
	return hold

