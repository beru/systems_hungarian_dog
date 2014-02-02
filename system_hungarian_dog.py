#!/usr/bin/python

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

builtInTypeNames = "signed unsigned char short int long float double void".split(" ")

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
	
def getIdentifierTypeNames(node):
	return getIdentifierType(node).names
	
def getHungarianPrefix(node):
	basename = ""
	if isArrayDecl(node.type):
		basename += "ap" if isPtrDecl(node.type.type) else "a"
	elif isPtrDecl(node.type):
		basename += "p"
	basename += " ".join(getIdentifierTypeNames(node))
	return basename

def checkIdentifierTypeName(node):
	names = getIdentifierTypeNames(node)
	for name in names:
		if name in builtInTypeNames:
			print("%s %s built-in type name '%s' is used" % (node.coord.file, node.coord.line, " ".join(names)))
			return False
	return True

def checkFunctionArg(node):
#	node.show()
#	dump.var_dump(node)
	if not checkIdentifierTypeName(node):
		return False
	print(node.name)
	basename = "a_" + getHungarianPrefix(node)
	print(basename)
	return True
	
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
	for item in node:
#		dump.var_dump(item)
		if not isDecl(item):
			continue
		if 'static' in item.storage:
			print("%s %d 'static' storage class qualifier is used in function" % (item.coord.file, item.coord.line))
		if not checkIdentifierTypeName(item):
			continue
		print(item.name)
		basename = "l_" + getHungarianPrefix(item)
		print(basename)
		

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
		
	def visit_Struct(self, node):
		for decl in node.decls:
#			dump.var_dump(decl)
			if not checkIdentifierTypeName(decl.type):
				continue
			print(decl.name)
			basename = getHungarianPrefix(decl.type)
			print(basename)
		
	def visit_Typedef(self, node):
#		dump.var_dump(node)
		nd = node.type
		while isinstance(nd, c_ast.TypeDecl):
			nd = nd.type
		if isinstance(nd, c_ast.Struct):
			if not node.name.startswith("st_"):
				print("%s %s struct typedef name should start with 'st_'" % (node.coord.file, node.coord.line))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename  = sys.argv[1]
	else:
		print("please specify directory")
		sys.exit()
	
	ast = parse_file(filename, use_cpp=True)
	Dog().visit(ast)

