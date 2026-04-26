# This module contains higher-level logic of girgit working on top of data.py .
import operator

from . import data
import os

import itertools
import collections

def write_tree(directory="."):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'

            if is_ignored(full):
                continue

            if entry.is_file(follow_symlinks=False):
                # Write file to object
                type_ = 'blob'
                with open (full,'rb') as out:
                    oid = data.hash_object(out.read())

            elif entry.is_dir(follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree(full)

            entries.append((type_,oid,entry.name))

    # Create the tree object and hash it.
    tree = ''.join(f'{type_} {oid} {name}\n' for type_,oid,name in sorted(entries))
    return data.hash_object(tree.encode(),'tree')

def iter_tree_entries(oid):
    if not oid:
        return
    tree = data.get_object(oid,'tree')
    for entry in tree.decode().splitlines():
        type_,oid,name = entry.split(' ',2)
        yield type_,oid,name

def get_tree(oid,base_path = ''):
    result = {}
    for type_,oid,name in iter_tree_entries(oid):
        assert '/' not in name
        assert name not in ('.','..')
        path = base_path + name
        if type_ == 'blob':
            result[path] = oid
        elif type_ == 'tree':
            result.update(get_tree(oid,f'{path}/'))
        else :
            raise Exception(f'Unknown tree entry type : {type_}')
    return result

def read_tree(tree_oid):
    empty_current_dir()
    for path,oid in get_tree(oid=tree_oid,base_path='./').items():
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,'wb') as inp:
            inp.write(data.get_object(oid))

def empty_current_dir():
    for root,dirnames,filenames in os.walk('.',topdown=False):
        for filename in filenames:
            path = os.path.relpath(f'{root}/{filename}')
            if is_ignored(path) or not os.path.isfile(path):
                continue
            os.remove(path)
        for dirname in dirnames:
            path = os.path.relpath(f'{root}/{filename}')
            if is_ignored(path):
                continue

            try :
                os.rmdir(path)
            except OSError,FileNotFoundError:
                pass

def commit(message):
    commit = f'tree {write_tree()}\n'

    HEAD = data.get_HEAD()
    if HEAD:
        commit += f'parent {HEAD}\n'

    commit += '\n'
    commit += f'{message}\n'

    oid = data.hash_object(commit.encode(),'commit')
    data.set_HEAD(oid)
    return oid


Commit = collections.namedtuple('Commit',['tree','parent','message'])

def get_commit(oid):
    parent = None
    commit = data.get_object(oid,'commit').decode()
    lines = iter(commit.splitlines()) # to get the lines one by one

    for line in itertools.takewhile(operator.truth,lines):
        key,value = line.split(' ',1)
        if key == 'tree':
            tree = value
        elif key == 'parent':
            parent = value
        else:
            assert False,f'Unknown Field{key}'

    message = '\n'.join(lines)
    return Commit(tree=tree,parent=parent,message=message)

def is_ignored(path):
    parts = path.split(os.sep)
    return any(p in {'.girgit','.git','.venv','__pycache__'} for p in parts)


