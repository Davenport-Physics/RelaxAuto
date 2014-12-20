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

class Attribute:
	
	def __init__(self,name,AttributeType,DefaultAttribute = False):
		
		self.name				= name
		self.AttributeType		= AttributeType
		self.AttributeString	= False
		self.boolean			= False
		self.DefaultAttribute	= DefaultAttribute
		
		
	def initialize_attribute(self,string):
		
		try:
			
			self.set_attribute(get_attribute_substring(len(self.name)),string)
			
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
		
	
	def get_attribute_type(self):
		
		return self.AttributeType
		
		
class IntAttribute(Attribute):
	
	def initialize_attribute(self , string):
		
		try:
			
			temp = int(get_attribute_substring( len(self.name), string) )
			
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
			
			temp = bool(get_attribute_substring(len(self.name)), string)
			self.set_attribute(temp)
			
		except:
			
			self.set_default_attribute()
