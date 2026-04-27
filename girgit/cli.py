import argparse
import os
import sys
import textwrap

from . import data
from . import base


def parse_args():

    parser = argparse.ArgumentParser("To execute the git commands")

    subparser = parser.add_subparsers(dest="command")
    subparser.required = True

    # init
    init_parser = subparser.add_parser("init",help="To initialize a repository",description="Git creates a hidden .git/ directory inside your current folder. That directory is the entire brain of Git for your project.")
    init_parser.set_defaults(func=init)

    # hash-object
    hash_parser = subparser.add_parser("hash-object",help="To hash the file" , description="It will read the file and store it in object database and apply SHA1 from hashlib giving the hex-digest as output")
    hash_parser.add_argument("file")
    hash_parser.set_defaults(func=hash_object)

    # cat-file

    cat_file_parser = subparser.add_parser("cat-file",help="To view stored object",description="It will take input oid to retrieve the file stored at objects/oid")
    cat_file_parser.add_argument("oid")
    cat_file_parser.set_defaults(func=cat_file)

    # write-tree

    write_tree_parser = subparser.add_parser("write-tree",help="To hash directory",description="It will take current working directory and store it in /objects")
    write_tree_parser.set_defaults(func=write_tree)

    # read-tree
    read_tree_parser = subparser.add_parser("read-tree",help="To extract the directory in current directory",description="It will take oid and recursively collect files from the trees and  ")
    read_tree_parser.add_argument("tree")
    read_tree_parser.set_defaults(func=read_tree)

    # commit
    commit_parser = subparser.add_parser("commit",help="To Save the changes !",description="It will create a commit object that stores meta data like author,time & date along with type and oid of data")
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument('--message','-m',required=True)

    # log

    log_parser = subparser.add_parser("log",help="To view all commits",description="it iteratively sees the parent oid of an oid and prints each commit")
    log_parser.set_defaults(func=log)
    log_parser.add_argument('oid',nargs='?')

    # checkout

    checkout_parser = subparser.add_parser("checkout",help="To extract a commit implementation to working directory" , description= "It extracts the commit object from get_commit() and uses commit.tree with read_tree to bring the set of directories to working directories.")
    checkout_parser.add_argument('oid')
    checkout_parser.set_defaults(func=checkout)

    # Tagging

    tag_parser = subparser.add_parser("tag",help="to use it as alias of oid in checkout",description="Its hard to remember the oid everytime we want to checkout thus we tag it with a name")
    tag_parser.add_argument('name')
    checkout_parser.add_argument('oid',nargs='?')
    tag_parser.set_defaults(func=tag)

    return parser.parse_args()



def init(args):
    data.init()
    print(f'Initialized Empty girgit repo at {os.path.join(os.getcwd(),data.GIT_DIR)}')

def hash_object(args):
    with open(args.file,'rb') as out:
        print(data.hash_object(out.read()))

def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.oid,expected=None))

def write_tree(args):
    print(base.write_tree())

def read_tree(args):
    base.read_tree(args.tree)

def commit(args):
    print(base.commit(args.message))

def log(args):
    oid = args.oid or data.get_ref('HEAD')
    while oid:
        commit = base.get_commit(oid)
        print(f'commit : {oid}\n')
        print(textwrap.indent(commit.message,'      '))
        print('')

        oid = commit.parent


def checkout(args):
    base.checkout(args.oid)

def tag(args):
    oid = data.get_ref('HEAD') or args.oid
    base.create_tag(args.name,oid)

def main():
    args = parse_args()
    args.func(args)
    
