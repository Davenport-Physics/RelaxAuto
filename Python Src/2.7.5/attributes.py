#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  attributes.py
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

from strmanipulation import get_attribute_substring

"""

Initially I didn't want to include more than one class within
the design of this program. However as it turned out, the code became
much simpler and more maintainable with the addition of the Attribute
class and it's subclasses.

An Attribute object is the primary way to store related data that is found
within the autoinit config file.

You are required to give each Attribute Object a name. This should
be the name of the attribute identifier in the config file.

The AttributeString variable is the variable that will hold the data
following the attribute identifier.

Each Attribute object has a boolean variable that is by default set to False.
It is usually set to True when the AttributeString is initialized to a variable
other than it's default.

The DefaultAttribute can be passed to each Attribute Object, during
object initialization. The purpose of this variable is to allow
the program to continue executing in the event that there is some
sort of syntax error in the config file. Passing a default value
is not required.

	SUBCLASSES
	
I found that the subclasses further reduced code complexity, in the auto.py
file. The purpose of each subclass should be obvious, if you review the code.

If you suspect that your AttributeString variable is not going to be a string type
then you will want to initialize the corresponding object to Int, Float or boolean.

Each of the classes use a similar method of initilization with the only difference,
being what type AttributeString is.


"""
class Attribute:
	
	def __init__(self,name,DefaultAttribute = False):
		
		self.name				= name
		self.AttributeString	= False
		self.boolean			= False
		self.DefaultAttribute	= DefaultAttribute
		
		
	def initialize_attribute(self,string):
		
		try:
			
			self.set_attribute(get_attribute_substring(len(self.name),string))
			
		except:
			
			print("Could not set attribute for %s" % (self.name))
			
	def set_default_attribute(self):
		
		print("Setting %s to default attribute %s" % (self.name,str(self.DefaultAttribute)))
		self.set_attribute(self.DefaultAttribute)
			
	def set_attribute(self , attribute):
		
		self.AttributeString = attribute
	
	
	def set_boolean(self , boolean):
		
		self.boolean = boolean
	
		
	def get_name(self):
		
		return self.name
	
		
	def get_attribute(self):
		
		return self.AttributeString
	
			
	def get_boolean(self):
		
		return self.boolean
		
		
class IntAttribute(Attribute):
	
	def initialize_attribute(self , string):
		
		try:
			
			temp = int(get_attribute_substring(len(self.name), string))
			self.set_attribute(temp)
			
		except:
			
			self.set_default_attribute()
			
class FloatAttribute(Attribute):
	
	def initialize_attribute(self , string):
		
		try:
			
			temp = float(get_attribute_substring(len(self.name) , string))
			self.set_attribute(temp)
			
		except:
			
			self.set_default_attribute()
			
class BooleanAttribute(Attribute):
	
	def initialize_attribute(self, string):
		
		try:
			
			temp = bool(get_attribute_substring(len(self.name), string))
			self.set_attribute(temp)
			
		except:
			
			self.set_default_attribute()
