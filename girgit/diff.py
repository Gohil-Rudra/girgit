import collections
from . import data
from . import base
from . import Myers
from .Edit_Wrapper import Edit

'''
We will compare the tree of the commit to the tree of its parent commit. 
If a file has one OID in the former tree and a different OID in the latter tree, 
it means that the file was changed (identical files would have had the same OID, 
since the OID is a hash over the content).

Let's create a new module - diff.py. 
This module will contain the code that deals with computing differences between objects. 
We will implement an important function called compare_trees(), this function 
will take a list of trees and will return them grouped by filename. 
This way, for each file we can get all its OIDs in the different trees.

'''
def compare_tree(*trees):
    # take file as input and get all of its oid in different trees well for diff
    # we are only going to use 2 commit(current and prev) so only need 2 trees...

    entries = collections.defaultdict(lambda:[None]*len(trees))
    # It will look like this :
    # {
    #    filename : [oid_in_tree1, oid_in_tree2,...]
    # } with initially all None

    for i , tree in enumerate(trees):
        for path,oid in tree.items():# output of get_tree() function goes here
            entries[path][i] = oid # tree wise oid of the file : abc.txt : [123...,456..., so on]

    for path,oids in entries.items():
        yield path,*oids # return the dictionary

def is_binary(data_bytes):
    return b'\x00' in data_bytes or not data_bytes.isascii()

def diff_blob(o_from,o_to,path="blob"):

    a_file = data.get_object(o_from) if o_from else b""
    b_file = data.get_object(o_to) if o_to else b""

    if is_binary(a_file) or is_binary(b_file):
        return f'Binary files a/{path} and b/{path} differ\n'

    a_lines = a_file.decode().splitlines(keepends=True)
    b_lines = b_file.decode().splitlines(keepends=True)


    output = f'--- a/{path}\n+++ b/{path}\n'

    edits = Myers.Myers(a_lines, b_lines).diff_operations()

    # hunk meta data : @+ .... @-....
    old_start = next((edit.old_line.number for edit in edits if edit.old_line),0)
    old_chunk = sum( 1 for edit in edits if edit.type != "ins")

    new_start = next((edit.new_line.number for edit in edits if edit.new_line), 0)
    new_chunk = sum(1 for edit in edits if edit.type != "del")

    output += f'@@ -{old_start},{old_chunk} +{new_start},{new_chunk} @@\n'

    for edit in edits:
        if edit.type == 'ins':
            output += f'+ {edit.text}'
        elif edit.type == 'del':
            output += f'- {edit.text}'
        else:
            output += f'  {edit.text}'

    return output

def diff_tree(t_from,t_to):
    output = ''
    for path, o_from , o_to in compare_tree(t_from,t_to):
        if o_from != o_to:
            output += diff_blob(o_from,o_to,path)
    return output

