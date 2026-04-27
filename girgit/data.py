import os
import hashlib

GIT_DIR = '.girgit'

# It deals with creation of .girgit repo
def init():
    os.makedirs(GIT_DIR)
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


def update_ref(ref,oid):
    with open (f'{GIT_DIR}/{ref}') as inp:
        inp.write(oid)

def get_ref(ref):
    try:
        with open (f'{GIT_DIR}/{ref}') as out:
            return out.read()
    except (FileNotFoundError,IsADirectoryError):
        return None


