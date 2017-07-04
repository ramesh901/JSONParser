#!/usr/bin/python3
import re
from pprint import pprint
import sys

def null_parser(data):
	if data[0:4] == "null":
		return [None, data[4:].strip()]

def boolean_parser(data):
	if data[0:4] == "true":
		return [True, data[4:].strip()]
	if data[0:5] == "false":
		return [False, data[5:].strip()]

def string_parser(data):
	if data[0] == '"':
		data = data[1:]
		slash_pos = data.find('\\')
		pos = data.find('"')
		temp_pos = 0
		while (True):
			pos = pos + temp_pos
			if(data[pos-1] != '\\'):
				return [data[:pos], data[pos + 1:].strip()]
			else:
				temp = data[pos + 1:]
				temp_pos = temp.find('"')

def number_parser(data):
	parse_num = re.findall("^(-?(?:\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?)",
                            data)
	if not parse_num:
		return None
	pos = len(str(parse_num))
	# if our parse_num is 123 then pos value comes as 7. 
	#It counts brackets and quotes also in the length as ['123'].
	#To avoid it we are subtracting 4
	try:
		return [int(parse_num[0]), data[pos-4:].strip()]
	except ValueError:
		return [float(parse_num[0]), data[pos-4:].strip()]

'''
ARRAY PARSER APPROACH:
TEST CASE 1 : []
TEST CASE 2 : [null]
TEST CASE 3 : [124]
TEST CASE 4 : ["apple"]
TEST CASE 5 : [123 , 324]
TEST CASE 6 : ["apple" , "happy"]
'''

def array_Parser(data):
	parsed_array = []
	if(data[0] != "["):
		return None
	data = data[1:].strip()
	while len(data):
		temp = value_parser(data)
		if temp is None:
			return None
		parsed_array.append(temp[0])
		#print("parsed array Is: ",parsed_array)
		data = temp[1].strip()
		if not len(data):
			return parsed_array
		#print("Remaining data is",data, "and len of data is",len(data))

		if(data[0] == "]"):
			return [parsed_array,data[1:].strip()]
		
		res = comma_parser(data)
		#print("res data is: ",res)
		if(res is None):
			return None
		data = res.strip()
		#print("res strip data is: ",data)
		

def comma_parser(data):
    if(data[0] != ','):
        return data.strip()

    else:
        if(data[1] == ']' or data[1] == '}'):
            raise SyntaxError("Invalid Json , should be followed by value")

        return data[1:].strip()

def colon_parser(data):
    if(data[0] != ':'):
        return None
    else:
        return data[1:].strip()

def value_parser(data):
	parsers = [null_parser,number_parser,string_parser,boolean_parser,
			   array_Parser,object_parser]
	for parser in parsers:
		#print("parser is",parser)
		value = parser(data)
		#print(parser,"value is", value)
		if(value is not None):
			return [value[0],value[1]]

def object_parser(data):
	parsed_obj = {}
	if(data[0] != '{'):
		return None
	data = data[1:].strip()
	while (data[0] != '}'):
		key,value = string_parser(data)
		if key is None:
			return None
		#print("key is",key)
		#print("value is",value)
		char = colon_parser(value)
		if char is None:
			raise SyntaxError(": not found")
		val = value_parser(char)
		if val is not None:
			parsed_obj[key] = val[0]
			#print("PARSED OBJECT IS",parsed_obj)
			char = comma_parser(val[1])
		else:
			return None
		#print("char is",char)
		if char is None:
			raise SyntaxError(", not found")
		data = char
	return [parsed_obj, data[1:]]


if __name__ == "__main__":
	data = open(sys.argv[1],"r").read()
	if value_parser(data) is not None:
		pprint(value_parser(data)[0])
	else:
		print("None")
	