import argparse
import os
import sys
import textwrap
import subprocess

from . import data
from . import base
from . import diff


def parse_args():

    parser = argparse.ArgumentParser("To execute the git commands")

    subparser = parser.add_subparsers(dest="command")
    subparser.required = True

    oid = base.get_oid
    # we are passing the function itself here... later in add_argument the function is applied on the argument !

    # init
    init_parser = subparser.add_parser("init",help="To initialize a repository",description="Git creates a hidden .git/ directory inside your current folder. That directory is the entire brain of Git for your project.")
    init_parser.set_defaults(func=init)

    # hash-object
    hash_parser = subparser.add_parser("hash-object",help="To hash the file" , description="It will read the file and store it in object database and apply SHA1 from hashlib giving the hex-digest as output")
    hash_parser.add_argument("file")
    hash_parser.set_defaults(func=hash_object)

    # cat-file

    cat_file_parser = subparser.add_parser("cat-file",help="To view stored object",description="It will take input oid to retrieve the file stored at objects/oid")
    cat_file_parser.add_argument("oid",type=oid)
    cat_file_parser.set_defaults(func=cat_file)

    # write-tree

    write_tree_parser = subparser.add_parser("write-tree",help="To hash directory",description="It will take current working directory and store it in /objects")
    write_tree_parser.set_defaults(func=write_tree)

    # read-tree
    read_tree_parser = subparser.add_parser("read-tree",help="To extract the directory in current directory",description="It will take oid and recursively collect files from the trees and  ")
    read_tree_parser.add_argument("tree",type=oid)
    read_tree_parser.set_defaults(func=read_tree)

    # commit
    commit_parser = subparser.add_parser("commit",help="To save the changes",description="It will create a commit object that stores meta data like author,time & date along with type and oid of data")
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument('--message','-m',required=True)

    # log

    log_parser = subparser.add_parser("log",help="To view all commits",description="it iteratively sees the parent oid of an oid and prints each commit")
    log_parser.set_defaults(func=log)
    log_parser.add_argument('oid',nargs='?',type=oid,default='@')

    # checkout

    checkout_parser = subparser.add_parser("checkout",help="To extract a commit implementation to working directory" , description= "It extracts the commit object from get_commit() and uses commit.tree with read_tree to bring the set of directories to working directories.")
    checkout_parser.add_argument('commit')
    checkout_parser.set_defaults(func=checkout)

    # Tagging

    tag_parser = subparser.add_parser("tag",help="To use it as alias of oid in checkout",description="Its hard to remember the oid everytime we want to checkout thus we tag it with a name")
    tag_parser.add_argument('name')
    tag_parser.add_argument('oid',nargs='?',type=oid,default='@')
    tag_parser.set_defaults(func=tag)

    # k

    k_parser = subparser.add_parser("k",help="To visualize the graph",description="We will use graphviz to create the graph similar to gitk")
    k_parser.set_defaults(func=k)

    # branch

    branch_parser = subparser.add_parser("branch",help="To create a new branch",description="Creates a new branch (a reference pointing to a commit). Does not change HEAD.")
    branch_parser.set_defaults(func=branch)
    branch_parser.add_argument('name',nargs='?')
    branch_parser.add_argument('start_point',default='@',type=oid,nargs='?')

    # status

    status_parser = subparser.add_parser("status",help="To see info of current working directory.")
    status_parser.set_defaults(func=status)

    # reset

    reset_parser = subparser.add_parser("reset",help="To move back in commit history",description="reset is different from checkout. Here in reset the symbolic ref HEAD which points to master branch so master is moved back. Whereas in checkout the head move")
    reset_parser.set_defaults(func=reset)
    reset_parser.add_argument('oid',type=oid)

    # show

    show_parser = subparser.add_parser("show",help="To show the difference between previous commit and latest commit",description="That + and - code  we see in github which helps us to read the commit and shows the changes made.")
    show_parser.set_defaults(func=show)
    show_parser.add_argument('oid',nargs='?',type=oid,default='@')
    return parser.parse_args()



def init(args):
    base.init()
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
    refs = {} # from oid to ref_tag dict
    for ref_name,ref in data.iter_refs():
        refs.setdefault(ref.value,[]).append(ref_name)

    for oid in base.iter_commits_and_parents({args.oid}):
        _print_commit(oid,base.get_commit(oid),refs.get(oid,[]))


def checkout(args):
    base.checkout(args.commit)

def tag(args):
    base.create_tag(args.name,args.oid)

def k(args): # Creation of edges for visualization
    dot = "digraph commits{\n"
    oids = set()
    for ref_name,ref in data.iter_refs(deref=False): # Where to Start
        # print(ref_name,ref)
        dot += f'"{ref_name}" [shape=note]\n'
        dot += f'"{ref_name}" -> "{ref.value}"\n'
        if not ref.symbolic:
            oids.add(ref.value)
    for oid in base.iter_commits_and_parents(oids): # Where it leads from the start points
        commit = base.get_commit(oid)
        #print(oid)
        dot += f'"{oid}" [shape=box label="{oid[:10]}..." style=filled]\n'
        if commit.parent:
            #print("Parent ",commit.parent)
            dot += f'"{oid}" -> "{commit.parent}"\n'

    dot += "}"
    print(dot)
    subprocess.run(
        'dot -Tpdf | open -f -a Preview',
        shell=True,
        input = dot,
        text=True
    )

def branch(args):
    if not args.name:
        current = base.get_branch_name()
        for branch_name in base.iter_branch_name():
            prefix = '*' if branch_name == current else ' '
            print(f'{prefix} {branch_name}')
    else:
        base.create_branch(args.name,args.start_point)
        print(f'Branch {args.name} created at {args.start_point[:10]}...')


def status(args):
    branch = base.get_branch_name()
    if branch:
        print(f'On branch {branch}')
    else:
        HEAD = base.get_oid('@')
        print(f'HEAD detached at {HEAD[0:10]}...')

def reset(args):
    base.reset(args.oid)

def _print_commit(oid,commit,refs=None): # here refs is a list not a dict
    refs_str = ','.join(refs) if refs else ""
    print(f'commit : {oid} {refs_str}\n') # print all the refs pointing to that commit.
    print(textwrap.indent(commit.message, '      '))
    print('')

def show(args):
    if not args.oid:
        return
    commit = base.get_commit(args.oid)
    parent_tree = None

    if commit.parent:
        parent_tree = base.get_commit(commit.parent).tree

    _print_commit(args.oid,commit)

    result = diff.diff_tree(base.get_tree(parent_tree),base.get_tree(commit.tree))
    print(result)


def main():
    args = parse_args()
    args.func(args)
    
