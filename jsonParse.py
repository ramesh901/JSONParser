#!/usr/bin/python3
import re
from pprint import pprint
import sys

'''def writeln(*args):
	for arg in args:
		f.write(str(arg))
	f.write("\n")

#-----------------------------------------------------------------------
#
#                    main
#
#-----------------------------------------------------------------------
def main(sourceText):
	global f
	#f = open(outputFilename, "w")
	print("Length of File is",len(sourceText))
	print("Select one of the below:")
	print("1.Scanner")
	print("2.Lexer")
	print("3.Parser")
	print("Press 1 or 2 or 3:")
	a = input()
	f = open(outputFilename, "w")      # open the ouput file
	if (a == 1):
		#fragment start core
		writeln("Here are the characters returned by the scanner:")
		writeln("  line col  character")

		# create a scanner (an instance of the Scanner class)
		scanner.initialize(sourceText)

		#------------------------------------------------------------------
		# Call the scanner's get() method repeatedly
		# to get the characters in the sourceText.
		# Stop when we reach the ENDMARK.
		#------------------------------------------------------------------
		character = scanner.get()       # getfirst Character object from the scanner
		while True:
			writeln(character)
			if character.cargo == scanner.ENDMARK: break
			character = scanner.get()   # getnext
		#fragment stop core

		f.close()  # close the output file
	elif (a == 2):
		writeln("Here are the tokens returned by the lexer:")

		# create an instance of a lexer
		lexer.initialize(sourceText)

		#------------------------------------------------------------------
		# use the lexer.getlist() method repeatedly to get the tokens in
		# the sourceText. Then print the tokens.
		#------------------------------------------------------------------
		while True:
			token = lexer.get()
			writeln(token.show(True))
			if token.type == EOF: break
	else:
		print("your selection is invalid.please select 1 or 2 or 3")
	f.close()'''
def null_parser(data):
	if data[0:4] == "null":
		return [None, data[4:].strip()]

def boolean_parser(data):
	if data[0:4] == "true":
		return [True, data[4:].strip()]
	if data[0:5] == "false":
		return [False, data[5:].strip()]

def string_parser(data):
	#string_branch = ["\"","\\","/","b","f","n","r","t","u"]
	if data[0] == '"':
		data = data[1:]
		slash_pos = data.find('\\')
		#if(slash_pos != -1 and data[slash_pos + 1] not in string_branch):
		#	return None
		pos = data.find('"')
		temp_pos = 0
		while (True):
			pos = pos + temp_pos
			#print("outside ", data," and the pos is ",pos)
			if(data[pos-1] != '\\'):
				#print(data," and the pos is ",pos)
				return [data[:pos], data[pos + 2:].strip()]
			else:
				temp = data[pos + 1:]
				temp_pos = temp.find('"')

def number_parser(data):
	print("number data is: ",data)
	parse_num = re.findall("^(-?(?:\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?)",
                            data)
	if not parse_num:
		return None
	#print(parse_num.type())
	pos = len(str(parse_num))
	print("pos is",pos)
	print("parsed number is:", parse_num)
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

'''
Fix "Pos" in Number parser
Add array parser within value parser
'''
def array_Parser(data):
	parsed_array = []
	if(data[0] != "["):
		return [None, data]
	data = data[1:].strip()
	while True:
		temp = value_parser(data)
		print("temp is: ",temp[0])
		#if temp == None:
		#	return [None,data]
		parsed_array.append(temp[0])
		print("parsed array Is: ",parsed_array)
		data = temp[1].strip()
		if(data[0] == "]"):
			return [parsed_array,data[array_pos+1:].strip()]
		
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

def value_parser(data):
	parsers = [null_parser,number_parser,string_parser,boolean_parser,array_Parser]
	for parser in parsers:
		value = parser(data)
		#print("value is: ",value)
		#print("unparse is: ",unparse)
		if(value is None):
			continue
		else:
			return [value[0],value[1]]
		


if __name__ == "__main__":
	#global f
	data = open(sys.argv[1],"r").read()
	print(data)
	'''
	print("Input data is: ",data)
	a = 'null    sdfadf'
	res = null_parser(a)
	print(res)
	b = 'false   afsdfs   '
	print(boolean_parser(b))
	c = "\"asdfghfk\\\"afd\"success"
	print(string_parser(c))'''
	print(array_Parser(data))
	#outputFilename = "genericScannerDriver_op.txt"
	#f = open(outputFilename, "w")
	#parsers = (null_parser, number_parser, boolean_parser, string_parser, array_parser, object_parser)
	'''parsers = (null_parser, boolean_parser)
	result = []
	for line in data:
		for parser in parsers:
			result = parser(data)
	print(result)
	pprint(result)
	'''

'''
	# Open a file
jFile = open("samp1.json", "r+")
str = jFile.read();
print("Read String is : ", str)


for i in range(len(str)):
	if(str[0] != '{'):
		print('False')
		

print('True')

# Close opend file
jFile.close()
'''