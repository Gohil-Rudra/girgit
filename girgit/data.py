import os
import hashlib

from collections import namedtuple

GIT_DIR = '.girgit'

# It deals with creation of .girgit repo
def init():
    os.makedirs(GIT_DIR,exist_ok=True)
    os.makedirs(f'{GIT_DIR}/objects') # Creating the objects repo

# The function of hash_object is to create the file and hash it then output the hexdigest
def hash_object(data,type_='blob'): # We need to find OID and store the file inside objects/oid
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()
    path = f'{GIT_DIR}/objects/{oid}'
    with open(path,'wb') as inp:
        inp.write(obj)
    return oid

def get_object(oid,expected='blob'):
    with open(f'{GIT_DIR}/objects/{oid}','rb') as out:
        obj = out.read()
    type_,null_,content = obj.partition(b'\x00')
    type_ = type_.decode()
    if expected is not None :
        assert type_ == expected , f'Wanted {expected} type , got {type_}'
    return content # This is bytes data

RefValue = namedtuple('RefValue',['symbolic','value'])
def update_ref(ref,value,deref=True):
    # assert not value.symbolic ; we don't need to assert that the ref is non-symbolic as we were writing only oid until now, lets now write the refs_name too
    # here ref is like refs/tags/heads and value is RefValue namedtuple
    ref = get_ref_internal(ref,deref)[0]

    assert value.value

    if value.symbolic:
        value = f'ref: {value.value}'
    else:
        value = value.value

    ref_path = f'{GIT_DIR}/{ref}'
    os.makedirs(os.path.dirname(ref_path),exist_ok=True)
    with open (ref_path,'w') as inp:
        inp.write(value)

def get_ref(ref,deref=True):
    return get_ref_internal(ref,deref)[1]

def get_ref_internal(ref,deref): # Go to the ends of the world and find the last oid referenced in the symbolic_ref chain, iff deref=True
    path = f'{GIT_DIR}/{ref}'
    if os.path.isfile(path):
        with open (path,'r') as out:
            value = out.read().strip()

            symbolic_flag = False
            if value and value.startswith('ref:'): # ref: <ref_name> is how it is stored so
                value = value.split(":",1)[1].strip()
                if deref:
                    return get_ref_internal(value,deref=True)
                else:
                    symbolic_flag = True
            return ref,RefValue(symbolic=symbolic_flag,value=value)

    return ref,RefValue(symbolic=False,value=None)


def iter_refs(prefix='', deref=True):
    refs = ['HEAD']
    for root, _, filenames in os.walk(f'{GIT_DIR}/refs'):
        root = os.path.relpath(root, GIT_DIR).replace(os.sep, '/')
        refs.extend(f'{root}/{file}' for file in filenames)

    for ref_name in refs:
        if not ref_name.startswith(prefix):
            continue
        yield ref_name, get_ref(ref_name, deref=deref)
