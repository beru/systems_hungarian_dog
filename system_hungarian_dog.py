#-----------------------------------------------------------------
# system_hungarian_dog.py
#
# Using pycparser for finding out irregular names in C files
# which violates holy coding conventions.
#
# Copyright (C) 2014, berupon
# License: BSD
#-----------------------------------------------------------------
from __future__ import print_function
import sys

import dump

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file

def isDecl(node):
	return isinstance(node, c_ast.Decl)

def isPtrDecl(node):
	return isinstance(node, c_ast.PtrDecl)
	
def isArrayDecl(node):
	return isinstance(node, c_ast.ArrayDecl)
	
def getIdentifierType(node):
	nd = node
	while not isinstance(nd, c_ast.IdentifierType):
		nd = nd.type
	return nd
	
def getIdentifierTypeName(node):
	return getIdentifierType(node).names[0]
	
def getHungarianPrefix(node):
	basename = ""
	if isArrayDecl(node.type):
		basename += "ap" if isPtrDecl(node.type.type) else "a"
	elif isPtrDecl(node.type):
		basename += "p"
	basename += getIdentifierTypeName(node)
	return basename

def checkFunctionArg(node):
#	node.show()
#	dump.var_dump(node)
	print(node.name)
	basename = "a_" + getHungarianPrefix(node)
	print(basename)
	
def checkFunctionDecl(node):
#	node.show()
#	dump.var_dump(node)
	print(node.type.declname)
	retType = getHungarianPrefix(node.type)
	print(retType)
	for arg in node.args.params:
		checkFunctionArg(arg)

def checkFunctionBody(node):
#	print
#	dump.var_dump(node)
	for item in node:
		if not isDecl(item):
			continue
		

# bow-wow
class Dog(c_ast.NodeVisitor):
	
#	def visit_Decl(self, node):
#		node.show()
#		dump.var_dump(node)
#		print(isinstance(node.type, c_ast.PtrDecl))
#		print("%s %s" % (node.name, ""))
	
	def visit_FuncDef(self, node):
#		dump.var_dump(node)
		checkFunctionDecl(node.decl.type)
		checkFunctionBody(node.body.block_items)
		
	def visit_FuncDecl(self, node):
		checkFunctionDecl(node)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename  = sys.argv[1]
	else:
		print("please specify directory")
		sys.exit()
	
	ast = parse_file(filename, use_cpp=True)
	Dog().visit(ast)


