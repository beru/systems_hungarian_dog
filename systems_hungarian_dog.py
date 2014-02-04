#!/usr/bin/python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------
# systems_hungarian_dog.py
#
# Using pycparser for finding out irregular C code which violates
# holy coding conventions.
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

builtInTypeNames = "signed unsigned char short int long float double void".split(" ")

def printError(*args, **kwargs):
	node = args[0]
	fmt = "ERR %s %s: " + args[1]
	lst = list(args)
	lst[0] = node.coord.file
	lst[1] = node.coord.line
	args = tuple(lst)
	print(fmt % args)

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
#	node.show()
#	dump.var_dump(getIdentifierType(node))
	basename = ""
	if isArrayDecl(node.type):
		basename += "ap" if isPtrDecl(node.type.type) else "a"
	elif isPtrDecl(node.type):
		basename += "p"
	identifierName = " ".join(getIdentifierTypeNames(node))
	# strict check ommited...
	if identifierName.startswith("st_"):
		identifierName = "st"
	elif identifierName.startswith("en_"):
		identifierName = "en"
	
	basename += identifierName
	return basename

def checkIdentifierTypeName(node):
	names = getIdentifierTypeNames(node)
	for name in names:
		if name in builtInTypeNames:
			printError(node, "built-in type '%s' is used", " ".join(names))

def checkFunctionArg(node):
#	node.show()
#	dump.var_dump(node)
	checkIdentifierTypeName(node)
	cow = "a_" + getHungarianPrefix(node)
	if not node.name.startswith(cow):
		printError(node, "argument name '%s' does not follow coding convention", node.name)
	
def checkFunctionDecl(node):
#	node.show()
#	dump.var_dump(node)
	declname = node.type.declname
	cow = getHungarianPrefix(node.type) + "_"
	if not declname.startswith(cow):
		printError(node, "function name '%s' does not follow coding convention", declname)
	if not hasattr(node.args, 'params'):
		return True
	for arg in node.args.params:
		checkFunctionArg(arg)
	
def checkFunctionBody(node):
#	print
	for item in node:
#		dump.var_dump(item)
		if not isDecl(item):
			continue
		if 'static' in item.storage:
			printError(item, "storage class qualifier 'static' inside of a function")
		if isinstance(item.type, c_ast.Struct) or isinstance(item.type, c_ast.Enum):
			continue
		checkIdentifierTypeName(item)
		cow = "l_" + getHungarianPrefix(item)
		if not item.name.startswith(cow):
			printError(item, "local variable name '%s' does not follow coding convention", item.name)
		

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
			checkIdentifierTypeName(decl.type)
			cow = getHungarianPrefix(decl.type)
			if not decl.name.startswith(cow):
				printError(decl, "struct member name '%s' does not follow coding convention", decl.name)
	
	def visit_Enum(self, node):
		print(" ")
	
	def visit_Typedef(self, node):
#		dump.var_dump(node)
		nd = node.type
		while isinstance(nd, c_ast.TypeDecl):
			nd = nd.type
		if isinstance(nd, c_ast.Struct):
			if not node.name.startswith("st_"):
				printError(node, "struct typedef name '%s' does not start with 'st_'", node.name)
		elif isinstance(nd, c_ast.Enum):
			if not node.name.startswith("en_"):
				printError(node, "enum typedef name '%s' does not start with 'en_'", node.name)
		self.generic_visit(node)
		
	def visit_Decl(self, node):
		if isinstance(node.type, c_ast.FuncDecl):
			self.visit_FuncDecl(node.type)
		elif isinstance(node.type, c_ast.Struct):
			self.visit_Struct(node.type)
		elif isinstance(node.type, c_ast.Enum):
			self.visit_Enum(node.type)
		else:
#			dump.var_dump(node)
#			node.type.show()
			checkIdentifierTypeName(node)
			cow = "g_" + getHungarianPrefix(node)
#			print(cow)
			if not node.name.startswith(cow):
				printError(node.type, "global variable name '%s' does not follow coding convention", node.name)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename  = sys.argv[1]
	else:
		print("please specify directory")
		sys.exit()
	
	ast = parse_file(filename, use_cpp=True,
			cpp_args=r'-I../pycparser-master/utils/fake_libc_include')
	Dog().visit(ast)

